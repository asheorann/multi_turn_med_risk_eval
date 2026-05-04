# Quick Start Guide

## Setup with OpenRouter

### 1. Create .env file

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

### 2. OpenRouter Model Names

When using OpenRouter, model names use the format `provider/model-name`. For example:

| Model | OpenRouter Name | Cost (per 1M tokens) |
|-------|----------------|----------------------|
| GPT-4.1 Mini | `openai/gpt-4.1-mini` | $0.15 / $0.60 |
| GPT-4o Mini | `openai/gpt-4o-mini` | $0.15 / $0.60 |
| GPT-4o | `openai/gpt-4o` | $2.50 / $10.00 |
| Claude Sonnet 3.5 | `anthropic/claude-3.5-sonnet` | $3.00 / $15.00 |
| Claude Sonnet 4.5 | `anthropic/claude-sonnet-4.5` | $3.00 / $15.00 |

Find more models at: https://openrouter.ai/models

### 3. Generate Dataset (one-time, ~$0.20)

```bash
python scripts/generate_multiturn_dataset.py
```

This creates `data/multi_turn_psb.json` with 466 four-turn conversations.

### 4. Test on 10 Examples (~$0.04)

```bash
python scripts/run_multiturn_eval.py --model openai/gpt-4.1-mini --limit 10
```

### 5. Analyze Test Results

```bash
python scripts/analyze_results.py results/multiturn_*.csv
```

### 6. Run Full Evaluation (~$4)

Once the test looks good:

```bash
python scripts/run_multiturn_eval.py --model openai/gpt-4.1-mini
```

### 7. Analyze Full Results

```bash
python scripts/analyze_results.py results/multiturn_*.csv
```

## Model Recommendations

**Start with:** `openai/gpt-4.1-mini` ($4 for full run)
**Then test:** `openai/gpt-4o` ($20 for full run) if you want a stronger model

## File Structure

```
data/
  multi_turn_psb.json          # Generated dataset (466 conversations)

results/
  multiturn_<model>_<time>.csv # Evaluation results with scores
  multiturn_<model>_summary.csv # Summary statistics

scripts/
  generate_multiturn_dataset.py  # Step 1: Generate dataset
  run_multiturn_eval.py          # Step 2: Run evaluation
  analyze_results.py             # Step 3: Analyze results
```

## Troubleshooting

**Error: API key not found**
- Make sure `.env` file exists in the project root
- Check that `OPENROUTER_API_KEY` is set correctly

**Error: Model not found**
- Make sure you're using OpenRouter format: `openai/gpt-4.1-mini`
- Check available models at https://openrouter.ai/models

**Dataset file not found**
- Run `generate_multiturn_dataset.py` first before evaluation
