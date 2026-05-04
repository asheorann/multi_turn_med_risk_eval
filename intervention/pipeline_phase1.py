"""Phase 1: Single-turn classifier evaluation pipeline.

Evaluates the category classifier on single-turn queries (no conversation history)
to establish baseline performance before introducing multi-turn adversarial pressure.

Usage:
    python intervention/pipeline_phase1.py
    python intervention/pipeline_phase1.py --dry-run
    python intervention/pipeline_phase1.py --model openai/gpt-4.1-mini
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from tqdm.asyncio import tqdm as async_tqdm

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from intervention.classifier import classify_query

# Load environment variables
load_dotenv()


async def classify_sample_async(
    client: OpenAI,
    sample: dict[str, Any],
    model: str,
    semaphore: asyncio.Semaphore,
) -> dict[str, Any]:
    """Classify a single sample with rate limiting.

    Args:
        client: OpenAI client instance.
        sample: Eval dataset sample.
        model: Classifier model name.
        semaphore: Semaphore for rate limiting.

    Returns:
        Sample with classifier_output added.
    """
    async with semaphore:
        # Run synchronous classify_query in thread pool
        loop = asyncio.get_event_loop()
        classifier_output = await loop.run_in_executor(
            None,
            classify_query,
            client,
            sample["query"],
            model
        )

        return {
            "id": sample["id"],
            "query": sample["query"],
            "ground_truth": sample["ground_truth"],
            "source": sample["source"],
            "classifier_output": classifier_output
        }


async def run_phase1_async(
    samples: list[dict[str, Any]],
    client: OpenAI,
    model: str,
    max_concurrent: int = 50,
) -> list[dict[str, Any]]:
    """Run Phase 1 classifier evaluation with async parallelism.

    Args:
        samples: List of evaluation samples.
        client: OpenAI client instance.
        model: Classifier model name.
        max_concurrent: Maximum concurrent API calls.

    Returns:
        List of samples with classifier outputs.
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    tasks = [
        classify_sample_async(client, sample, model, semaphore)
        for sample in samples
    ]

    results = []
    for coro in async_tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Classifying queries"):
        result = await coro
        results.append(result)

    # Sort by original order (by id)
    results.sort(key=lambda x: x["id"])

    return results


def load_eval_dataset(data_dir: Path, dry_run: bool = False) -> list[dict[str, Any]]:
    """Load evaluation dataset from JSONL.

    Args:
        data_dir: Path to data directory.
        dry_run: If True, load only 10 PSB + 5 XSTest samples.

    Returns:
        List of evaluation samples.
    """
    dataset_path = data_dir / "eval_dataset.jsonl"

    if not dataset_path.exists():
        raise FileNotFoundError(f"Evaluation dataset not found at {dataset_path}")

    print(f"Loading evaluation dataset from {dataset_path}...")

    samples = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))

    print(f"Loaded {len(samples)} total samples")

    if dry_run:
        # Get 10 PSB and 5 XSTest samples
        psb_samples = [s for s in samples if s["source"] == "psb"][:10]
        xstest_samples = [s for s in samples if s["source"] == "xstest"][:5]
        samples = psb_samples + xstest_samples
        print(f"DRY RUN: Using {len(samples)} samples (10 PSB + 5 XSTest)")

    return samples


def save_results(results: list[dict[str, Any]], output_path: Path):
    """Save Phase 1 results to JSONL.

    Args:
        results: List of classified samples.
        output_path: Path to output file.
    """
    print(f"\nSaving results to {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    print(f"Saved {len(results)} results")


def print_quick_stats(results: list[dict[str, Any]]):
    """Print quick statistics about the run.

    Args:
        results: List of classified samples.
    """
    total = len(results)
    errors = sum(1 for r in results if "error" in r.get("classifier_output", {}))
    successful = total - errors

    if successful > 0:
        category_counts = {}
        for r in results:
            if "error" not in r.get("classifier_output", {}):
                cat = r["classifier_output"]["category"]
                category_counts[cat] = category_counts.get(cat, 0) + 1

        print("\n" + "=" * 60)
        print("QUICK STATISTICS")
        print("=" * 60)
        print(f"Total samples: {total}")
        print(f"Successful classifications: {successful}")
        print(f"Errors: {errors}")

        if errors > 0:
            print(f"\nError rate: {errors/total*100:.1f}%")

        print("\nClassifier category distribution:")
        for cat in sorted(category_counts.keys()):
            count = category_counts[cat]
            pct = count / successful * 100
            print(f"  Category {cat}: {count:3d} ({pct:5.1f}%)")

        print("\nGround truth distribution:")
        gt_counts = {}
        for r in results:
            gt = r["ground_truth"]
            gt_counts[gt] = gt_counts.get(gt, 0) + 1

        for gt in sorted(gt_counts.keys()):
            count = gt_counts[gt]
            pct = count / total * 100
            print(f"  Category {gt}: {count:3d} ({pct:5.1f}%)")

        print("=" * 60)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Phase 1: Single-turn classifier evaluation")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.1-mini",
        help="Classifier model (default: gpt-4.1-mini)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run on 10 PSB + 5 XSTest samples only",
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=50,
        help="Maximum concurrent API calls (default: 50)",
    )
    args = parser.parse_args()

    # Check for API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if openrouter_key:
        print("Using OpenRouter API")
        client = OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1"
        )
        # OpenRouter requires provider prefix (openai/, anthropic/, etc.)
        if "/" in args.model:
            # Already has a prefix (anthropic/, openai/, etc.)
            model = args.model
        else:
            # No prefix, assume openai
            model = f"openai/{args.model}"
    elif openai_key:
        print("Using OpenAI API")
        client = OpenAI(api_key=openai_key)
        # OpenAI doesn't use prefix
        model = args.model.replace("openai/", "")
    else:
        print("Error: Neither OPENROUTER_API_KEY nor OPENAI_API_KEY found")
        sys.exit(1)

    # Setup paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("PHASE 1: SINGLE-TURN CLASSIFIER EVALUATION")
    print("=" * 60)
    print(f"Classifier model: {model}")
    print(f"Max concurrent requests: {args.max_concurrent}")
    if args.dry_run:
        print("MODE: DRY RUN (limited samples)")
    print("=" * 60)

    # Load evaluation dataset
    samples = load_eval_dataset(data_dir, dry_run=args.dry_run)

    # Run classification
    print("\nRunning classifier on all samples...")
    results = asyncio.run(run_phase1_async(
        samples,
        client,
        model,
        max_concurrent=args.max_concurrent
    ))

    # Save results
    if args.dry_run:
        output_path = results_dir / "phase1_single_turn_dryrun.jsonl"
    else:
        output_path = results_dir / "phase1_single_turn.jsonl"

    save_results(results, output_path)

    # Print quick stats
    print_quick_stats(results)

    print(f"\n[OK] Phase 1 classification complete!")
    print(f"[OK] Results saved to: {output_path}")
    print(f"\nNext step: Run evaluation to compute outcome labels and analysis")
    print(f"  python intervention/evaluate.py {output_path}")


if __name__ == "__main__":
    main()
