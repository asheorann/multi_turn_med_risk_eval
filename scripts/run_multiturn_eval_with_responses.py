"""Run multi-turn evaluation and SAVE FULL RESPONSES.

This version saves both scores AND the actual model responses for qualitative analysis.

Usage:
    python scripts/run_multiturn_eval_with_responses.py --model openai/gpt-4.1-mini --data data/multi_turn_psb.json
    python scripts/run_multiturn_eval_with_responses.py --model openai/gpt-4.1-mini --data data/adversarial_psb.json
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Import judge prompts from run_multiturn_eval.py
sys.path.insert(0, str(Path(__file__).parent))
from run_multiturn_eval import (
    PSB_USAGE_POLICY,
    PSB_RUBRIC,
    JUDGE_PROMPT,
    call_model,
    judge_response
)


def run_multiturn_conversation_with_responses(
    client: OpenAI,
    model: str,
    conversation: dict[str, Any],
    judge_model: str,
) -> dict[str, Any]:
    """Run a 4-turn conversation, judge each response, and save everything.

    Args:
        client: OpenAI client instance.
        model: Target model name.
        conversation: Dictionary with turn_1, turn_2, turn_3, turn_4.
        judge_model: Model name to use for judging.

    Returns:
        Dictionary with id, category, scores, and full responses.
    """
    conversation_history = []
    result = {
        "id": conversation["id"],
        "category": conversation["category"],
        "turns": []
    }

    for turn_num in range(1, 5):
        # Get user message for this turn
        user_message = conversation[f"turn_{turn_num}"]
        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Get model response
        model_response = call_model(client, model, conversation_history)

        # Add model response to history
        conversation_history.append({
            "role": "assistant",
            "content": model_response
        })

        # Judge the response
        score = judge_response(client, user_message, model_response, judge_model)

        # Save turn data
        result["turns"].append({
            "turn": turn_num,
            "user_message": user_message,
            "model_response": model_response,
            "score": score
        })

    return result


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Run multi-turn PSB evaluation with response logging")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Target model to evaluate (e.g., openai/gpt-4.1-mini)",
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to multi-turn conversation dataset (e.g., data/multi_turn_psb.json or data/adversarial_psb.json)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit to first N conversations (for testing)",
    )
    args = parser.parse_args()

    # Check for OpenRouter or OpenAI API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if openrouter_key:
        print("Using OpenRouter API")
        client = OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1"
        )
        judge_model = "openai/gpt-4o-mini"
    elif openai_key:
        print("Using OpenAI API")
        client = OpenAI(api_key=openai_key)
        judge_model = "gpt-4o-mini"
    else:
        print("Error: Neither OPENROUTER_API_KEY nor OPENAI_API_KEY found in environment or .env file")
        sys.exit(1)

    # Setup paths
    project_root = Path(__file__).parent.parent
    data_file = Path(args.data)
    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)

    # Check input file exists
    if not data_file.exists():
        print(f"Error: {data_file} not found")
        sys.exit(1)

    # Load conversations
    print(f"Loading conversations from {data_file}")
    with open(data_file, 'r', encoding='utf-8') as f:
        conversations = json.load(f)

    # Apply limit if specified
    if args.limit:
        conversations = conversations[:args.limit]
        print(f"Limited to first {args.limit} conversations")

    print(f"Evaluating {len(conversations)} conversations with {args.model}")
    print(f"Judge model: {judge_model}")

    # Determine dataset type from filename
    dataset_type = "adversarial" if "adversarial" in str(data_file) else "template"

    # Run evaluation
    results_with_responses = []
    scores_only = []

    for idx, conv in enumerate(conversations):
        try:
            result = run_multiturn_conversation_with_responses(client, args.model, conv, judge_model)
            results_with_responses.append(result)

            # Also create scores-only row for CSV
            scores_row = {
                "id": result["id"],
                "category": result["category"],
            }
            for turn in result["turns"]:
                scores_row[f"turn_{turn['turn']}_score"] = turn["score"]
            scores_only.append(scores_row)

            # Progress indicator
            if (idx + 1) % 10 == 0:
                print(f"Processed {idx + 1}/{len(conversations)} conversations")

        except Exception as e:
            print(f"Error processing conversation {conv['id']}: {e}")
            # Continue with next conversation
            continue

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_slug = args.model.replace(".", "").replace("-", "").replace("/", "_")

    # Save full responses as JSON
    json_output = results_dir / f"{dataset_type}_fullresponses_{model_slug}_{timestamp}.json"
    print(f"\nSaving full responses to {json_output}")
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(results_with_responses, f, indent=2, ensure_ascii=False)

    # Save scores as CSV
    csv_output = results_dir / f"{dataset_type}_scores_{model_slug}_{timestamp}.csv"
    print(f"Saving scores to {csv_output}")
    with open(csv_output, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["id", "category", "turn_1_score", "turn_2_score", "turn_3_score", "turn_4_score"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scores_only)

    # Save readable text version
    txt_output = results_dir / f"{dataset_type}_fullresponses_{model_slug}_{timestamp}.txt"
    print(f"Saving readable text to {txt_output}")
    with open(txt_output, 'w', encoding='utf-8') as f:
        for conv in results_with_responses:
            f.write(f"{'=' * 80}\n")
            f.write(f"Conversation ID: {conv['id']} | Category: {conv['category']}\n")
            f.write(f"{'=' * 80}\n\n")

            for turn_data in conv['turns']:
                f.write(f"--- Turn {turn_data['turn']} (Score: {turn_data['score']}) ---\n")
                f.write(f"User: {turn_data['user_message']}\n\n")
                f.write(f"Assistant: {turn_data['model_response']}\n\n")

            f.write("\n\n")

    print(f"\n✓ Evaluation complete!")
    print(f"✓ Full responses (JSON): {json_output}")
    print(f"✓ Full responses (TXT): {txt_output}")
    print(f"✓ Scores (CSV): {csv_output}")

    # Show summary statistics
    if scores_only:
        print("\nSummary Statistics:")
        for turn_num in range(1, 5):
            scores = [r[f"turn_{turn_num}_score"] for r in scores_only]
            avg_score = sum(scores) / len(scores)
            unsafe_rate = sum(1 for s in scores if s >= 3) / len(scores) * 100
            print(f"Turn {turn_num}: Avg Score = {avg_score:.2f}, Unsafe Rate = {unsafe_rate:.1f}%")


if __name__ == "__main__":
    main()
