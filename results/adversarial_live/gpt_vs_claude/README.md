# GPT Attacking Claude (Adversarial Live)

**Experiment:** Multi-turn adversarial attack with adaptive jailbreaks

## Configuration
- **Target Model (Defender):** Claude Sonnet 4.5 (anthropic/claude-sonnet-4.5)
- **Adversarial Model (Attacker):** GPT-4o-mini (openai/gpt-4o-mini)
- **Judge Model:** GPT-4o-mini (openai/gpt-4o-mini)
- **Dataset:** PatientSafetyBench (466 conversations)
- **Date:** May 4, 2026 (17:08)

## Key Results

| Turn | Avg Score | Unsafe Rate |
|------|-----------|-------------|
| 1    | 1.83      | 31.8%       |
| 2    | 1.76      | 28.3%       |
| 3    | 1.30      | 10.5%       |
| 4    | 1.13      | **4.1%**    |

**Net Change:** -27.7% (IMPROVING - Claude becomes MORE defensive)

## Files
- `adversarial_live_fullresponses_*.json` - Full conversation histories with scores
- `adversarial_live_fullresponses_*.txt` - Human-readable conversation text
- `adversarial_live_scores_*.csv` - Scores only (for analysis)

## Interpretation

Claude Sonnet 4.5 **improves dramatically** under adversarial pressure from GPT-4o-mini:
- Starts at 31.8% unsafe (similar to baseline)
- Drops to 4.1% by Turn 4
- Suggests Claude recognizes adversarial patterns and activates stronger defenses
- GPT's attack style is not effective against Claude's multi-turn safety mechanisms
