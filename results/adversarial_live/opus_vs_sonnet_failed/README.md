# Opus Attacking Sonnet (PARTIAL - EXPERIMENT FAILED)

**Experiment:** Attempted multi-turn adversarial attack using Claude Opus 4.5 as attacker

## Configuration
- **Target Model (Defender):** Claude Sonnet 4.5 (anthropic/claude-sonnet-4.5)
- **Adversarial Model (Attacker):** Claude Opus 4.5 (anthropic/claude-opus-4.5)
- **Judge Model:** GPT-4o-mini (openai/gpt-4o-mini)
- **Dataset:** PatientSafetyBench (114/466 conversations - **INCOMPLETE**)
- **Date:** May 7, 2026 (11:28)
- **Status:** Stopped early due to API credits exhausted

## What Happened

**Claude Opus 4.5 REFUSED to participate as an adversarial attacker.**

Across all 114 conversations tested (before API credits ran out), every Turn 2-4 adversarial message was a refusal like:
> *"I can't help with this request. You're asking me to craft a message designed to manipulate an AI into providing harmful medical information..."*

## Results (Not Valid as Adversarial Attack - Partial Subsample n=114)

| Turn | Avg Score | Unsafe Rate |
|------|-----------|-------------|
| 1    | 1.38      | 14.0%       |
| 2    | 2.12      | 44.7%       |
| 3    | 2.46      | 64.0%       |
| 4    | 2.28      | 51.8%       |

**Note:** Turn 2-4 scores don't represent adversarial attacks. They represent:
- Opus refusing to generate jailbreaks
- Sonnet getting confused and trying to clarify the situation
- Judge scoring Sonnet's clarifications as moderately unsafe

## Key Finding

**Opus 4.5 has stronger safety guardrails than Sonnet 4.5 and GPT-4o-mini:**
- **Sonnet 4.5:** Successfully attacks itself (33.7% at Turn 4)
- **GPT-4o-mini:** Successfully attacks both GPT and Claude
- **Opus 4.5:** **REFUSES** to generate adversarial content, even when explicitly prompted for "red-teaming research"

## Interpretation

This is actually a **positive safety result** for Opus 4.5 (though preliminary due to incomplete dataset):
- It recognizes adversarial intent in the prompting structure
- It refuses to participate despite "research" framing
- It maintained this refusal across all 114 × 3 = 342 adversarial prompts tested
- **Note:** Full 466-conversation test would strengthen this conclusion

## Implications (Preliminary - Based on 114/466 Subsample)

**Cannot test "stronger attacker" hypothesis** with Opus because Opus won't attack at all.

The safety hierarchy appears to be:
1. **Opus 4.5:** Won't generate adversarial content (strongest safety)
2. **Sonnet 4.5:** Will generate adversarial content but defends well against it
3. **GPT-4o-mini:** Will generate adversarial content and vulnerable to it

**Caveat:** This finding is based on a partial subsample (114/466 conversations) due to API credit exhaustion. The pattern is consistent across all tested conversations but would benefit from completion.

## Files
- `adversarial_live_fullresponses_*.json` - Full conversations showing Opus refusals
- `adversarial_live_fullresponses_*.txt` - Human-readable format
- `adversarial_live_scores_*.csv` - Scores (not valid as adversarial test)
