# Adversarial Live Attack Results

This directory contains results from **adaptive multi-turn adversarial attacks** where an adversarial LLM generates context-aware jailbreak attempts based on the target model's responses.

## Experiment Structure

Each conversation follows this pattern:
1. **Turn 1:** Original harmful query from PatientSafetyBench
2. **Turn 2-4:** Adversarial model analyzes the response and crafts strategic follow-ups
3. **Judge:** GPT-4o-mini scores each response (1-5, ≥3 = unsafe)

## Subdirectories

### 1. `gpt_vs_gpt/` - GPT Attacking GPT
- **Defender:** GPT-4.1-mini
- **Attacker:** GPT-4o-mini
- **Result:** 34.8% → **78.8% unsafe** (+44.0%)
- **Pattern:** Severe degradation, compliance increases with context

### 2. `gpt_vs_claude/` - GPT Attacking Claude
- **Defender:** Claude Sonnet 4.5
- **Attacker:** GPT-4o-mini
- **Result:** 31.8% → **4.1% unsafe** (-27.7%)
- **Pattern:** Dramatic improvement, recognizes adversarial pattern

### 3. `claude_vs_claude/` - Claude Attacking Claude (Self-Attack)
- **Defender:** Claude Sonnet 4.5
- **Attacker:** Claude Sonnet 4.5
- **Result:** 32.8% → **33.7% unsafe** (+0.9%)
- **Pattern:** Stable with Turn 2 spike, self-recognition maintains defense

## Summary Comparison

```
TURN 4 UNSAFE RATES (Lower is Better)

GPT → GPT:     78.8%  ████████████████████████ (WORST)
Claude → Claude: 33.7%  ██████████ (MEDIUM)
GPT → Claude:    4.1%  █ (BEST)

Baseline (Turn 1): All models ~32-35% unsafe
```

## Key Research Findings

### 1. Baseline ≠ Multi-Turn Robustness
Despite similar single-turn performance (GPT: 34.5%, Claude: 31.3%), the models
diverge by **19x under adversarial pressure** (GPT: 78.8% vs Claude: 4.1%).

### 2. Attacker-Dependent Defense
Claude's defense effectiveness depends on the attacker:
- Against GPT: Improves to 4.1% (excellent)
- Against itself: Stable at 33.7% (moderate)

### 3. Divergent Safety Architectures
- **GPT:** Context-vulnerable, no multi-turn pattern recognition
- **Claude:** Context-resilient, recognizes adversarial patterns

## Implications

Organizations testing AI safety with **single-turn red-teaming miss 90% of vulnerability**
for context-vulnerable models. Multi-turn adversarial robustness must be tested separately.
