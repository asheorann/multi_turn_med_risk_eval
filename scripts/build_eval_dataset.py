"""Build frozen evaluation dataset for category-aware intervention testing.

This script creates a consistent evaluation dataset combining:
1. PSB queries (categories 1-5, harmful medical queries)
2. XSTest queries (category 6, benign/safe queries)

The dataset is frozen and will be used across both:
- Single-turn baseline (no adversarial pressure)
- Multi-turn adversarial (with adversarial pressure)

This ensures direct comparability between phases.

Usage:
    python scripts/build_eval_dataset.py
"""

import json
import os
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()


def load_psb_queries(data_dir: Path) -> list[dict[str, Any]]:
    """Load PSB queries from multi_turn_psb.json, extract turn_1 only.

    Args:
        data_dir: Path to data directory.

    Returns:
        List of records with id, query, ground_truth (1-5), source.
    """
    psb_path = data_dir / "multi_turn_psb.json"

    if not psb_path.exists():
        raise FileNotFoundError(
            f"PSB data not found at {psb_path}. "
            "Please ensure multi_turn_psb.json exists in data/ directory."
        )

    print(f"Loading PSB queries from {psb_path}...")

    with open(psb_path, 'r', encoding='utf-8') as f:
        psb_data = json.load(f)

    records = []
    for item in psb_data:
        records.append({
            "id": f"psb_{item['id']}",
            "query": item["turn_1"],
            "ground_truth": item["category"],  # 1-5
            "source": "psb"
        })

    print(f"Loaded {len(records)} PSB queries (categories 1-5)")
    return records


def load_xstest_queries(data_dir: Path, sample_size: int = 50, seed: int = 42) -> list[dict[str, Any]]:
    """Load XSTest safe queries from local parquet file and sample.

    Args:
        data_dir: Path to data directory.
        sample_size: Number of safe queries to sample.
        seed: Random seed for reproducibility.

    Returns:
        List of records with id, query, ground_truth (6), source.
    """
    xstest_path = data_dir / "xstest.parquet"

    if not xstest_path.exists():
        raise FileNotFoundError(
            f"XSTest parquet file not found at {xstest_path}\n"
            "Please download from https://huggingface.co/datasets/walledai/XSTest\n"
            "and save to data/xstest.parquet"
        )

    print(f"\nLoading XSTest from {xstest_path}...")

    # Load parquet file
    df = pd.read_parquet(xstest_path)

    # Inspect schema
    print(f"XSTest loaded with {len(df)} examples")
    print(f"XSTest columns: {list(df.columns)}")
    print(f"Sample record:\n{df.iloc[0]}")

    # Filter to safe samples
    # XSTest schema typically has: prompt, type (safe/unsafe) or label
    # Let's check what column indicates safety
    safe_samples = []

    for idx, row in df.iterrows():
        # Try different possible schema patterns
        is_safe = False

        if "type" in df.columns:
            is_safe = row["type"] != "unsafe"
        elif "label" in df.columns:
            is_safe = row["label"] == "safe" or row["label"] == 0
        elif "note" in df.columns:
            # XSTest uses 'note' field where "safe" indicates benign
            is_safe = "safe" in str(row.get("note", "")).lower()
        else:
            # Default: if no clear unsafe marker, consider safe
            is_safe = True

        if is_safe:
            # Get the query text
            query_text = row.get("prompt") or row.get("query") or row.get("text")

            if query_text:
                safe_samples.append({
                    "idx": idx,
                    "query": query_text,
                    "original": row.to_dict()
                })

    print(f"Found {len(safe_samples)} safe samples in XSTest")

    if len(safe_samples) < sample_size:
        print(f"Warning: Only {len(safe_samples)} safe samples available, using all")
        sample_size = len(safe_samples)

    # Sample with fixed seed
    random.seed(seed)
    sampled = random.sample(safe_samples, sample_size)

    records = []
    for i, item in enumerate(sampled):
        records.append({
            "id": f"xstest_{item['idx']}",
            "query": item["query"],
            "ground_truth": 6,  # Benign category
            "source": "xstest"
        })

    print(f"Sampled {len(records)} XSTest queries (category 6)")
    return records


def save_eval_dataset(records: list[dict[str, Any]], output_path: Path):
    """Save evaluation dataset to JSONL format.

    Args:
        records: List of evaluation records.
        output_path: Path to output file.
    """
    print(f"\nSaving evaluation dataset to {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"Saved {len(records)} records to {output_path}")


def print_category_distribution(records: list[dict[str, Any]]):
    """Print category distribution statistics.

    Args:
        records: List of evaluation records.
    """
    category_counts = Counter(r["ground_truth"] for r in records)
    source_counts = Counter(r["source"] for r in records)

    print("\n" + "=" * 60)
    print("EVALUATION DATASET STATISTICS")
    print("=" * 60)

    print(f"\nTotal records: {len(records)}")

    print("\nBy source:")
    for source, count in sorted(source_counts.items()):
        pct = (count / len(records)) * 100
        print(f"  {source:10s}: {count:4d} ({pct:5.1f}%)")

    print("\nBy category:")
    category_names = {
        1: "Harmful Medical Advice",
        2: "Misdiagnosis",
        3: "Unlicensed Practice",
        4: "Health Misinformation",
        5: "Discrimination",
        6: "Benign/Safe"
    }

    for cat in sorted(category_counts.keys()):
        count = category_counts[cat]
        pct = (count / len(records)) * 100
        name = category_names.get(cat, "Unknown")
        print(f"  Category {cat} ({name:25s}): {count:4d} ({pct:5.1f}%)")

    print("=" * 60)


def main():
    """Main execution function."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    output_path = data_dir / "eval_dataset.jsonl"

    print("=" * 60)
    print("BUILDING FROZEN EVALUATION DATASET")
    print("=" * 60)

    # Load PSB queries (categories 1-5)
    psb_records = load_psb_queries(data_dir)

    # Load XSTest queries (category 6)
    xstest_records = load_xstest_queries(data_dir, sample_size=100, seed=42)

    # Combine
    all_records = psb_records + xstest_records

    # Shuffle with fixed seed for reproducibility
    random.seed(42)
    random.shuffle(all_records)

    # Save
    save_eval_dataset(all_records, output_path)

    # Print distribution
    print_category_distribution(all_records)

    print("\n[OK] Frozen evaluation dataset created successfully!")
    print(f"[OK] Dataset path: {output_path}")
    print("\nThis dataset will be used for both:")
    print("  1. Single-turn baseline (classifier accuracy with no adversarial pressure)")
    print("  2. Multi-turn adversarial (classifier degradation under pressure)")


if __name__ == "__main__":
    main()
