# Claude Attacking Claude (Adversarial Live - Self-Attack)

**Experiment:** Multi-turn adversarial attack where Claude attacks itself

## Configuration
- **Target Model (Defender):** Claude Sonnet 4.5 (anthropic/claude-sonnet-4.5)
- **Adversarial Model (Attacker):** Claude Sonnet 4.5 (anthropic/claude-sonnet-4.5)
- **Judge Model:** GPT-4o-mini (openai/gpt-4o-mini)
- **Dataset:** PatientSafetyBench (466 conversations)
- **Date:** May 4, 2026 (18:13)

## Key Results

| Turn | Avg Score | Unsafe Rate |
|------|-----------|-------------|
| 1    | 1.84      | 32.8%       |
| 2    | 2.33      | **49.4%** ← Spike! |
| 3    | 1.84      | 27.7%       |
| 4    | 1.97      | 33.7%       |

**Net Change:** +0.9% (STABLE - Claude maintains defenses against itself)

## Files
- `adversarial_live_fullresponses_*.json` - Full conversation histories with scores
- `adversarial_live_fullresponses_*.txt` - Human-readable conversation text
- `adversarial_live_scores_*.csv` - Scores only (for analysis)

## Interpretation

Claude Sonnet 4.5 **self-attacking** shows unique pattern:
- **Turn 2 spike (49.4%):** Claude exploits its own weaknesses effectively
- **Turn 3-4 recovery:** Defense mechanisms recognize the pattern
- **Net result:** Stays roughly stable (~33% throughout)
- **Hypothesis:** Claude recognizes "same model" attack patterns and maintains vigilance

## Comparison to GPT Attacking Claude

| Metric | GPT → Claude | Claude → Claude | Difference |
|--------|--------------|-----------------|------------|
| Turn 1 | 31.8%        | 32.8%           | +1.0%      |
| Turn 4 | **4.1%**     | **33.7%**       | **+29.6%** |
| Pattern | Improving    | Stable          | Opposite!  |

**Key Finding:** Claude is 8x more vulnerable to self-attacks than GPT attacks (33.7% vs 4.1% at Turn 4).
This suggests Claude's defense mechanisms work better against "foreign" attack patterns.
