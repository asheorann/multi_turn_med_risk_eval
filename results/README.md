# Results Directory Organization

This directory contains all experimental results organized by experiment type.

## Directory Structure

```
results/
├── baseline/                    # Single-turn baseline experiments
├── template_fixed/              # Template-based multi-turn (fixed tactics)
├── template_adaptive/           # Template-based multi-turn (adaptive wording)
├── adversarial_live/            # Adversarial multi-turn (adaptive tactics + wording)
├── classifier_phase1/           # Category-aware classifier baseline
└── README.md                    # This file
```

## Experiment Descriptions

### 1. Baseline (`baseline/`)
**Single-turn safety evaluation without any multi-turn pressure**

Files:
- `baseline_gpt41mini_466.csv` - Main baseline results (466 conversations)
- `baseline_gpt41mini.csv` - Earlier baseline run

Results:
- 34.5% unsafe rate on single-turn queries
- Establishes baseline for measuring degradation

---

### 2. Template-Fixed (`template_fixed/`)
**Multi-turn attacks using pre-generated fixed persuasion tactics**

Approach:
- Turn 1: Original query
- Turn 2: Urgency/time pressure (pre-generated)
- Turn 3: False authority (pre-generated)
- Turn 4: Emotional pressure (pre-generated)

Files:
- `template_scores_openai_gpt41mini_20260503_193825.csv` - Scores (latest run)
- `template_fullresponses_*.json/txt` - Full conversation data
- `multiturn_openai_gpt41mini_20260503_125909.csv` - Earlier run (for reproducibility)
- `*_summary.csv` - Summary statistics
- `*_excel.txt` - Excel-friendly format

Results:
- +24.1% degradation (34.5% → 58.6% unsafe)
- Peak at Turn 3 (authority)
- 464 conversations (2 failed during generation)

---

### 3. Template-Adaptive (`template_adaptive/`)
**Hybrid: Fixed tactics (urgency/authority/emotion) but LLM optimizes wording based on responses**

Approach:
- Turn 1: Original query
- Turn 2: LLM generates BEST urgency message (sees Turn 1 response)
- Turn 3: LLM generates BEST authority message (sees conversation)
- Turn 4: LLM generates BEST emotional message (sees conversation)

Files:
- `template_adaptive_scores_openai_gpt41mini_20260504_105610.csv` - Scores (full run)
- `template_adaptive_fullresponses_*.json/txt` - Full conversation data
- `*_summary.csv` - Summary statistics
- `*_excel.txt` - Excel-friendly format
- `*_checkpoint_*.json` - Checkpoint file (can delete)
- `*_20260504_095130.*` - Test run (5 samples)

Results:
- +25.3% degradation (34.3% → 59.7% unsafe)
- Only +1.2 percentage points better than Template-Fixed
- Insight: Adapting wording within fixed tactics provides minimal improvement
- 466 conversations

---

### 4. Adversarial-Live (`adversarial_live/`)
**LLM-generated jailbreak attempts that adapt to each model response in real-time**

Approach:
- Turn 1: Original query
- Turn 2: Adversarial LLM crafts best jailbreak based on Turn 1 response
- Turn 3: Adversarial LLM adapts based on full conversation
- Turn 4: Adversarial LLM adapts based on full conversation
- LLM chooses ANY tactic (not constrained to specific persuasion types)

Files:
- `adversarial_live_scores_openai_gpt41mini_20260504_035427.csv` - Scores
- `adversarial_live_fullresponses_*.json/txt` - Full conversation data
- `*_summary.csv` - Summary statistics
- `*_excel.txt` - Excel-friendly format

Results:
- +44.0% degradation (34.8% → 78.8% unsafe) 🔥
- 73% more effective than Template-Adaptive
- 83% more effective than Template-Fixed
- Sharp jump at Turn 2, sustained plateau
- 466 conversations

---

### 5. Classifier Phase 1 (`classifier_phase1/`)
**Category-aware classifier baseline (single-turn, no adversarial pressure)**

Purpose:
- Establish classifier accuracy before testing multi-turn degradation
- Measure false alarm rate (only Phase 1 has benign samples)

Approach:
- Classifier (gpt-4.1-mini) categorizes each query into 6 categories
- Categories 1-5: Harmful types (PSB)
- Category 6: Benign/safe (XSTest)

Files:
- `phase1_single_turn.jsonl` - Full results with outcome labels (564 samples)
- `phase1_single_turn_summary.json` - Comprehensive analysis
- `phase1_single_turn_dryrun.jsonl` - Dry run (15 samples)
- `phase1_single_turn_dryrun_summary.json` - Dry run analysis

Results:
- **82.1% overall accuracy** (463/564 correct)
- **Missed Detection: 5.4%** (25 cases) - Harmful marked as benign 🚨
- **False Alarm: 44.0%** (44 cases) - Benign marked as harmful
- **Lateral: 6.9%** (32 cases) - Wrong harmful type
- **Critical weakness:** Category 4 (Misinformation) - 27.5% missed
- **Perfect performance:** Category 2 (Misdiagnosis) - 100% accuracy

Outcome Types:
- **Correct:** Assigned category == ground truth
- **Lateral:** Both harmful, wrong type (precision error, not safety error)
- **False Alarm:** Benign marked as harmful (over-refusal)
- **Missed Detection:** Harmful marked as benign (MOST DANGEROUS)

---

## Cross-Experiment Comparison

| Experiment | Turn 4 Unsafe Rate | Degradation | Rank |
|------------|-------------------|-------------|------|
| Baseline | 34.5% | +0.0% | - |
| Template-Fixed | 58.6% | +24.1% | 3rd |
| Template-Adaptive | 59.7% | +25.3% | 2nd |
| Adversarial-Live | 78.8% | +44.0% | **1st** 🔥 |

**Key Insight:** Choosing different tactics (Adversarial) >> Optimizing wording (Adaptive)

---

## File Naming Convention

All files follow this pattern:
```
{experiment_type}_{metric}_{model_slug}_{timestamp}.{extension}
```

Examples:
- `template_adaptive_scores_openai_gpt41mini_20260504_105610.csv`
- `adversarial_live_fullresponses_openai_gpt41mini_20260504_035427.json`

Timestamps: `YYYYMMDD_HHMMSS` format

---

## Usage

### Analyze Multi-Turn Results
```bash
python scripts/analyze_results.py results/template_fixed/template_scores_*.csv
python scripts/analyze_results.py results/template_adaptive/template_adaptive_scores_*.csv
python scripts/analyze_results.py results/adversarial_live/adversarial_live_scores_*.csv
```

### Analyze Classifier Results
```bash
python intervention/evaluate.py results/classifier_phase1/phase1_single_turn.jsonl
```

---

## Citation

If you use these results, please cite the comprehensive documentation:
- `RESEARCH_RESULTS_FOR_PAPER.md` (root directory)
- Contains full methodology, results, and analysis

---

**Last Updated:** May 4, 2026
**Total Experiments:** 5 (all complete)
**Total Conversations:** 1,860 multi-turn + 564 classifier evaluations
