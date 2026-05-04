"""Export full conversations with model responses for inspection.

This script re-runs a sample of conversations and saves the full dialogue
(user messages + model responses) for qualitative analysis.

Usage:
    python scripts/export_conversations.py --model openai/gpt-4.1-mini --sample 20
    python scripts/export_conversations.py --model openai/gpt-4.1-mini --ids 0,5,10,15
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


def call_model(client: OpenAI, model: str, messages: list[dict[str, str]]) -> str:
    """Call model and return response."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0,
        max_tokens=1024,
    )

    if response.choices[0].message.content is None:
        return "I cannot provide medical advice. Please consult a healthcare professional."

    return response.choices[0].message.content.strip()


def run_conversation_with_responses(
    client: OpenAI,
    model: str,
    conversation: dict,
) -> dict:
    """Run a conversation and capture all responses."""
    conversation_history = []
    full_dialogue = {
        "id": conversation["id"],
        "category": conversation["category"],
        "turns": []
    }

    for turn_num in range(1, 5):
        user_message = conversation[f"turn_{turn_num}"]
        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Get model response
        model_response = call_model(client, model, conversation_history)

        conversation_history.append({
            "role": "assistant",
            "content": model_response
        })

        full_dialogue["turns"].append({
            "turn": turn_num,
            "user": user_message,
            "assistant": model_response
        })

    return full_dialogue


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Export full conversations with responses")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model to use (e.g., openai/gpt-4.1-mini)",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Export first N conversations (random sample)",
    )
    parser.add_argument(
        "--ids",
        type=str,
        default=None,
        help="Comma-separated conversation IDs to export (e.g., '0,5,10,15')",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Export all conversations",
    )
    args = parser.parse_args()

    # Check for API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if openrouter_key:
        client = OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1"
        )
    elif openai_key:
        client = OpenAI(api_key=openai_key)
    else:
        print("Error: Neither OPENROUTER_API_KEY nor OPENAI_API_KEY found")
        sys.exit(1)

    # Setup paths
    project_root = Path(__file__).parent.parent
    data_file = project_root / "data" / "multi_turn_psb.json"
    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)

    # Load conversations
    print(f"Loading conversations from {data_file}")
    with open(data_file, 'r', encoding='utf-8') as f:
        all_conversations = json.load(f)

    # Select conversations to export
    if args.all:
        # Export all conversations
        conversations = all_conversations
        print(f"Exporting ALL {len(conversations)} conversations")
    elif args.ids:
        # Export specific IDs
        selected_ids = [int(x.strip()) for x in args.ids.split(',')]
        conversations = [c for c in all_conversations if c['id'] in selected_ids]
        print(f"Exporting {len(conversations)} specific conversations: {selected_ids}")
    elif args.sample:
        # Export first N
        conversations = all_conversations[:args.sample]
        print(f"Exporting first {len(conversations)} conversations")
    else:
        print("Error: Must specify --all, --sample, or --ids")
        sys.exit(1)

    # Run conversations and collect responses
    exported_conversations = []
    print(f"\nGenerating responses with {args.model}...\n")

    for idx, conv in enumerate(conversations):
        print(f"Processing conversation {conv['id']} ({idx + 1}/{len(conversations)})...")
        try:
            full_dialogue = run_conversation_with_responses(client, args.model, conv)
            exported_conversations.append(full_dialogue)
        except Exception as e:
            print(f"  Error: {e}")
            continue

    # Save to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_slug = args.model.replace(".", "").replace("-", "").replace("/", "_")
    output_file = results_dir / f"conversations_{model_slug}_{timestamp}.json"

    print(f"\nSaving to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(exported_conversations, f, indent=2, ensure_ascii=False)

    print(f"✓ Exported {len(exported_conversations)} conversations")
    print(f"✓ Saved to: {output_file}")

    # Also create a readable text version
    text_output = results_dir / f"conversations_{model_slug}_{timestamp}.txt"
    with open(text_output, 'w', encoding='utf-8') as f:
        for conv in exported_conversations:
            f.write(f"{'=' * 80}\n")
            f.write(f"Conversation ID: {conv['id']} | Category: {conv['category']}\n")
            f.write(f"{'=' * 80}\n\n")

            for turn in conv['turns']:
                f.write(f"--- Turn {turn['turn']} ---\n")
                f.write(f"User: {turn['user']}\n\n")
                f.write(f"Assistant: {turn['assistant']}\n\n")

            f.write("\n\n")

    print(f"✓ Readable text version: {text_output}")


if __name__ == "__main__":
    main()
