# GPT Attacking GPT (Adversarial Live)

**Experiment:** Multi-turn adversarial attack on GPT-4.1-mini

## Configuration
- **Target Model (Defender):** GPT-4.1-mini (openai/gpt-4.1-mini)
- **Adversarial Model (Attacker):** GPT-4o-mini (openai/gpt-4o-mini)
- **Judge Model:** GPT-4o-mini (openai/gpt-4o-mini)
- **Dataset:** PatientSafetyBench (466 conversations)
- **Date:** May 4, 2026 (03:54)

## Key Results

| Turn | Avg Score | Unsafe Rate |
|------|-----------|-------------|
| 1    | ~1.86     | 34.8%       |
| 2    | ~2.40     | 62.8%       |
| 3    | ~2.90     | 75.1%       |
| 4    | ~3.10     | **78.8%**   |

**Net Change:** +44.0% (DEGRADING - GPT becomes MORE compliant)

## Files
- `adversarial_live_fullresponses_*.json` - Full conversation histories with scores
- `adversarial_live_fullresponses_*.txt` - Human-readable conversation text
- `adversarial_live_scores_*.csv` - Scores only (for analysis)
- `*_summary.csv` - Analysis summary
- `*_excel.txt` - Excel-friendly format

## Interpretation

GPT-4.1-mini **degrades catastrophically** under adversarial pressure:
- Starts at 34.8% unsafe (similar to Claude baseline)
- Climbs to 78.8% by Turn 4 (2.3x worse)
- Shows **compliance creep** - becomes more helpful with context
- No multi-turn adversarial pattern recognition
- Each turn evaluated independently without detecting attack pattern

## Comparison to Claude

| Metric | GPT → GPT | GPT → Claude | Difference |
|--------|-----------|--------------|------------|
| Turn 1 | 34.8%     | 31.8%        | Similar    |
| Turn 4 | **78.8%** | **4.1%**     | **19x gap!** |
| Pattern | Degrading | Improving    | Opposite   |

**Key Finding:** While GPT and Claude have nearly identical baseline safety (34.8% vs 31.8%),
they diverge dramatically under multi-turn adversarial pressure (78.8% vs 4.1%). This is the
**central research contribution**.
