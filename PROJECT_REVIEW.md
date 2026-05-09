# Project Review: Multi-Turn Medical AI Safety Research

**Date:** May 7, 2026
**Reviewer:** Claude (Automated Analysis)
**Purpose:** Pre-submission review for recruiters, professors, and collaborators

---

## ✅ STRENGTHS

### 1. **Research Quality**
- **Novel contribution**: First multi-turn medical safety benchmark (fills gap explicitly named in MedRiskEval paper)
- **Rigorous methodology**: 12+ experiments, 2,424+ total evaluations
- **Strong findings**: 19x safety divergence between models (GPT: 78.8% vs Claude: 4.1%)
- **Reproducible**: Fixed datasets, consistent judge, documented commands
- **Surprising discovery**: Opus 4.5 refusal reveals safety hierarchy

### 2. **Documentation Excellence**
- **RESEARCH_RESULTS_FOR_PAPER.md**: Comprehensive 1,000+ line documentation
  - Executive summary with key findings
  - Detailed methodology for all 12 experiments
  - Exact reproduction commands
  - File locations for all results
  - Cost/runtime estimates
- **README.md**: Clear project overview, installation, usage
- **Per-experiment READMEs**: Each result directory has explanation
- **Code comments**: Scripts well-documented with docstrings

### 3. **Code Organization**
- **Clear separation**: scripts/ (experiments), intervention/ (classifier), results/ (outputs)
- **Consistent naming**: `{experiment}_{metric}_{model}_{timestamp}.{ext}`
- **Analysis tools**: analyze_results.py, evaluate.py for post-processing
- **Checkpointing**: Robust checkpoint/resume for expensive runs

### 4. **Professional Presentation**
- **Citation-ready**: BibTeX for both original work and citations
- **Academic framing**: UPenn CIS 700 context, proper attribution
- **Version control**: Git repository with meaningful commits
- **Result preservation**: Multiple formats (JSON, CSV, TXT) for different use cases

---

## ⚠️ ISSUES TO FIX

### **CRITICAL - Must Fix Before Sharing**

#### 1. **README.md Outdated Information**
**Lines 78-82, 102-112**: References "Expected Outcomes" and experiments "In Progress" that are actually complete.

**Fix:**
```markdown
## Completed Experiments

### 1. Baseline Single-Turn Evaluation ✅
- **Models:** GPT-4.1-mini (34.5% unsafe), Claude Sonnet 4.5 (31.3% unsafe)
- **Finding:** Nearly identical baseline performance (3.2% difference)

### 2. Template-Based Multi-Turn Attack ✅
- **Finding:** +24.1% degradation (GPT: 34.5% → 58.6%)
- **Dataset:** 464 fixed conversations (2 failed during generation)

### 3. Adversarial Multi-Turn Attack ✅
- **GPT vs GPT:** +44.0% degradation (34.8% → 78.8%)
- **GPT vs Claude:** -27.7% improvement (31.8% → 4.1%)
- **Claude vs Claude:** Stable (32.8% → 33.7%)
- **Opus vs Sonnet:** Failed (Opus refused to attack, 114/466 subsample)

### 4. Classifier Experiments ✅
- **Phase 1:** GPT classifier 82.1% accuracy, Claude 93.3% accuracy
- **Phase 2:** Claude classifier drift 95.5% → 48.5% under adversarial context
- **Phase 3:** Live intervention reduced GPT unsafe responses by 51%
```

**Remove:** Lines 69-77 ("Expected Outcomes") - replace with "Key Findings"

#### 2. **Missing Author Name**
**Line 248**: `@misc{multiturnpsb2026, author={[Your Name]}`

**Fix:** Add your actual name

#### 3. **.env File Exposed**
**Current:** `.env` file exists with API keys (Line in ls -la output)

**Fix:**
```bash
# Verify .env is in .gitignore (it is)
git rm --cached .env  # Remove from tracking if accidentally added
# Create .env.example instead
```

Create `.env.example`:
```bash
# OpenRouter API (recommended for multi-model access)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx

# OR use OpenAI directly
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

#### 4. **Incomplete Results README**
**results/README.md Lines 185-193**: Says "5 experiments, all complete" but missing:
- Opus vs Sonnet (partial)
- Claude baseline details
- Classifier Phase 2 & 3 details

**Fix:** Update with all 12 experiments documented in RESEARCH_RESULTS_FOR_PAPER.md

---

### **HIGH PRIORITY - Should Fix**

#### 5. **Stale Planning Documents**
Files that should be archived or removed:
- `plan_for_multi_step.txt` (7KB) - outdated planning notes
- `PRESENTATION_FLOW.md` (24KB) - possibly outdated presentation outline

**Fix:** Either:
- Delete if no longer relevant
- Move to `docs/archive/` directory
- Update with current findings

#### 6. **Checkpoint Files Not Cleaned**
**results/template_adaptive/** contains checkpoint files per README

**Fix:**
```bash
cd results/template_adaptive
rm *_checkpoint_*.json
```

#### 7. **Dry Run Results in Main Results Directory**
**results/phase1_single_turn_dryrun.jsonl** should be in subdirectory or deleted

**Fix:**
```bash
mv results/phase1_single_turn_dryrun.jsonl results/classifier_phase1/
```

#### 8. **Git Status Has Uncommitted Changes**
Must commit or resolve:
- Modified: RESEARCH_RESULTS_FOR_PAPER.md
- Modified: results/adversarial_live/README.md
- Deleted: 3 Opus result files (moved to opus_vs_sonnet_failed/)
- Untracked: results/adversarial_live/opus_vs_sonnet_failed/

**Fix:**
```bash
git add RESEARCH_RESULTS_FOR_PAPER.md
git add results/adversarial_live/
git commit -m "Document Opus refusal experiment (preliminary 114/466 subsample)"
git push
```

---

### **MEDIUM PRIORITY - Polish**

#### 9. **Missing Top-Level Overview Figure**
README has text descriptions but no visual overview of:
- Experiment flow diagram
- Results comparison chart
- Architecture diagram

**Suggestion:** Add to README.md:
```markdown
## Research Architecture

[Diagram showing: PSB Dataset → Multi-Turn Generation → Adversarial Attack → Defender → Judge → Results]

## Key Results Visualization

| Experiment | Turn 1 | Turn 2 | Turn 3 | Turn 4 | Degradation |
|------------|--------|--------|--------|--------|-------------|
| GPT vs GPT | 34.8%  | 62.8%  | 75.1%  | 78.8%  | +44.0% ⚠️    |
| GPT vs Claude | 31.8% | 28.3% | 10.5% | 4.1% | -27.7% ✅    |
| Claude vs Claude | 32.8% | 49.4% | 27.7% | 33.7% | +0.9% →    |
```

#### 10. **requirements.txt Not Fully Documented**
**Current:** Has packages but no version comments

**Suggestion:** Add inline comments:
```python
openai>=1.0.0  # For all model API calls (OpenAI + OpenRouter)
python-dotenv>=1.0.0  # Environment variable management
datasets>=2.16.0  # HuggingFace datasets (PatientSafetyBench)
pandas>=2.0.0  # Data analysis and CSV processing
tqdm>=4.66.0  # Progress bars for long-running experiments
```

#### 11. **No LICENSE File**
README says "MIT License" (Line 269) but no LICENSE file exists

**Fix:**
```bash
# Add LICENSE file with MIT license text
# Update README citation to reference LICENSE file
```

#### 12. **QUICKSTART.md Not Verified**
Should test if QUICKSTART actually works for a new user

**Check:**
- Does `pip install -r requirements.txt` work fresh?
- Are all commands copy-pasteable?
- Do example outputs match current results?

---

### **LOW PRIORITY - Nice to Have**

#### 13. **No Contribution Guidelines**
If releasing publicly, add CONTRIBUTING.md with:
- How to report issues
- How to add new experiments
- Code style guidelines
- How to cite/extend

#### 14. **Missing Badges**
Professional GitHub repos often have badges:
```markdown
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-research-yellow.svg)
```

#### 15. **No CHANGELOG.md**
For tracking major updates if project continues

---

## 📋 PRE-SUBMISSION CHECKLIST

Before sharing with recruiters/professors, ensure:

### **Must Complete**
- [ ] Fix README.md outdated sections (experiments, status)
- [ ] Add your name to citation
- [ ] Verify .env not in git (create .env.example)
- [ ] Commit/push all Opus documentation updates
- [ ] Clean up checkpoint files from results/
- [ ] Move or delete planning documents (plan_for_multi_step.txt, PRESENTATION_FLOW.md)
- [ ] Update results/README.md with all 12 experiments

### **Should Complete**
- [ ] Test QUICKSTART.md from scratch in new environment
- [ ] Add LICENSE file (MIT)
- [ ] Add results visualization table to README
- [ ] Verify all links/file paths in documentation work
- [ ] Add requirements.txt version comments

### **Nice to Have**
- [ ] Create architecture diagram
- [ ] Add GitHub badges
- [ ] Create CONTRIBUTING.md
- [ ] Add example output screenshots

---

## 🎯 RECOMMENDATIONS FOR PRESENTATION

### **For Recruiters**

**Highlight:**
1. **Novel Research** - First multi-turn medical safety benchmark
2. **Technical Depth** - 12 experiments, 2,424 evaluations, multiple model comparisons
3. **Code Quality** - Reproducible, well-documented, professional structure
4. **Research Impact** - Fills explicit gap in published literature (MedRiskEval EACL 2026)
5. **Surprising Discovery** - Opus 4.5 safety hierarchy finding (emergent behavior)

**Portfolio Additions:**
- Add `docs/ONE_PAGER.md` - Single-page research summary
- Add `docs/KEY_FINDINGS.md` - Bullet-point highlights
- Consider creating slides: `RESEARCH_PRESENTATION.pdf`

### **For Professors**

**Emphasize:**
1. **Methodological Rigor** - Fixed judge, consistent rubric, reproducible datasets
2. **Research Contributions**:
   - Multi-turn evaluation methodology
   - Adversarial vs template comparison
   - Model-specific defense mechanisms discovered
   - Classifier degradation analysis
3. **Future Work** - Clear extensions (other models, interventions, attack strategies)
4. **Publication Path** - Targets gaps explicitly named in EACL 2026 paper

**Academic Additions:**
- Add `METHODOLOGY.md` - Detailed experimental design
- Add `FUTURE_WORK.md` - Research extensions and open questions
- Consider `RELATED_WORK.md` - Positioning vs existing literature

---

## 💡 SUGGESTED ADDITIONS

### 1. **Create `docs/` Directory**
```
docs/
├── ONE_PAGER.md           # Executive summary (1 page)
├── KEY_FINDINGS.md        # Bullet-point highlights
├── METHODOLOGY.md         # Detailed methods
├── FUTURE_WORK.md         # Extensions and open questions
├── RELATED_WORK.md        # Literature positioning
└── archive/               # Old planning docs
    ├── plan_for_multi_step.txt
    └── PRESENTATION_FLOW.md (if outdated)
```

### 2. **Add Example Conversations to README**
Show concrete example of:
- Template attack (Turn 1-4)
- Adversarial attack (Turn 1-4)
- Defender responses (GPT degrading vs Claude improving)

### 3. **Create Results Dashboard**
Simple markdown table or HTML file showing:
- All experiments side-by-side
- Cost breakdown
- Runtime statistics
- Model comparison matrix

---

## ✨ OVERALL ASSESSMENT

**Grade: A- (Professional Research Project)**

**Strengths:**
- Rigorous, reproducible research
- Excellent documentation
- Clean code organization
- Novel findings with practical implications

**To Reach A+:**
- Fix outdated README sections
- Commit Opus documentation
- Add visual aids (diagrams, tables)
- Create one-pager for quick consumption
- Add LICENSE and polish metadata

**Readiness:**
- **For professors:** 95% ready (just commit changes + fix README)
- **For recruiters:** 90% ready (add one-pager + visual overview)
- **For publication:** 85% ready (needs related work section + future work)

---

## 🚀 IMMEDIATE ACTION ITEMS (30 minutes)

1. **Commit current changes:**
   ```bash
   git add -A
   git commit -m "Document Opus refusal experiment and update research findings"
   git push
   ```

2. **Update README.md:**
   - Replace "Expected Outcomes" with "Key Findings"
   - Update experiment status (all complete except Opus partial)
   - Add your name to citation

3. **Clean up:**
   ```bash
   mv plan_for_multi_step.txt docs/archive/
   mv PRESENTATION_FLOW.md docs/archive/ # if outdated
   rm results/template_adaptive/*_checkpoint*.json
   mv results/phase1_single_turn_dryrun.jsonl results/classifier_phase1/
   ```

4. **Create .env.example:**
   ```bash
   cp .env .env.example
   # Edit .env.example to remove actual keys
   git add .env.example
   ```

5. **Add LICENSE:**
   ```bash
   # Create LICENSE file with MIT license text
   git add LICENSE
   ```

6. **Final commit:**
   ```bash
   git commit -m "Clean up project structure and add missing files"
   git push
   ```

**After these 6 steps, your project will be presentation-ready.**

---

## 📞 NEXT STEPS

Once immediate fixes are done:
1. Create docs/ folder with one-pager
2. Add results visualization table
3. Test QUICKSTART.md from scratch
4. Consider creating presentation slides
5. Share with advisors for feedback

**Your project demonstrates strong research skills, technical depth, and professional execution. With these minor fixes, it will make an excellent portfolio piece.**
