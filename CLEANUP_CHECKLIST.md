# Pre-Submission Cleanup Checklist

**Date:** May 7, 2026
**Status:** Ready to clean up for recruiters/professors

---

## ✅ MUST DO (10 minutes)

### 1. Archive Old Planning Documents
```powershell
# Create archive directory
mkdir docs\archive

# Move old files
move plan_for_multi_step.txt docs\archive\
# Check if PRESENTATION_FLOW.md is outdated - if yes:
move PRESENTATION_FLOW.md docs\archive\
```

### 2. Clean Python Cache
```powershell
# Remove __pycache__ directories
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Remove .pyc files
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
```

### 3. Remove Checkpoint Files
```powershell
# Remove template_adaptive checkpoints
Remove-Item results\template_adaptive\*_checkpoint*.json -ErrorAction SilentlyContinue
```

### 4. Move Dry Run Results
```powershell
# Move to proper subdirectory
move results\phase1_single_turn_dryrun.jsonl results\classifier_phase1\
```

### 5. Create .env.example (if not exists)
```powershell
# Create .env.example
@"
# OpenRouter API (recommended for multi-model access)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx

# OR use OpenAI directly
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# Instructions:
# 1. Copy this file to .env
# 2. Replace the xxx values with your actual API keys
# 3. Never commit .env to git
"@ | Out-File -FilePath .env.example -Encoding utf8
```

### 6. Verify .env is NOT tracked in git
```powershell
git status | Select-String ".env"
# Should show nothing OR only .env.example
```

### 7. Add LICENSE File
Create `LICENSE` with MIT license text from: https://choosealicense.com/licenses/mit/

Or use this:
```powershell
@"
MIT License

Copyright (c) 2026 Anushka Sheoran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"@ | Out-File -FilePath LICENSE -Encoding utf8
```

---

## ✅ COMMIT CHANGES (5 minutes)

### 8. Stage All Changes
```powershell
git add -A
```

### 9. Review What Will Be Committed
```powershell
git status
# Should show:
#   - Modified: README.md (updated)
#   - Modified: RESEARCH_RESULTS_FOR_PAPER.md (Opus docs)
#   - Modified: results/adversarial_live/README.md
#   - New: results/adversarial_live/opus_vs_sonnet_failed/
#   - New: ONE_PAGER.md
#   - New: PROJECT_REVIEW.md
#   - New: CLEANUP_CHECKLIST.md
#   - New: LICENSE
#   - New: .env.example
#   - Deleted: old planning docs (if moved)
```

### 10. Commit Everything
```powershell
git commit -m "Finalize project for presentation: update docs, add Opus findings, clean structure"
```

### 11. Push to GitHub
```powershell
git push
```

---

## 📋 VERIFICATION CHECKLIST

After cleanup, verify:

- [ ] `.env` is NOT in git (only `.env.example` should be tracked)
- [ ] No `__pycache__` directories visible
- [ ] No checkpoint files in results/
- [ ] `LICENSE` file exists
- [ ] `ONE_PAGER.md` has your name (Anushka Sheoran) ✓
- [ ] `README.md` updated with completed experiments ✓
- [ ] All changes committed and pushed to GitHub
- [ ] Old planning docs in `docs/archive/` or deleted
- [ ] Project looks clean in file explorer

---

## 🎯 FINAL CHECKS BEFORE SHARING

### For GitHub/Portfolio:
1. Visit your GitHub repo URL
2. Check that README.md displays correctly
3. Verify ONE_PAGER.md renders nicely
4. Ensure RESEARCH_RESULTS_FOR_PAPER.md is accessible
5. Confirm no sensitive info (API keys) visible

### For Recruiters:
- [ ] GitHub repo is public
- [ ] README has clear overview
- [ ] ONE_PAGER.md can be sent as standalone document
- [ ] Code is well-commented
- [ ] Results are organized and documented

### For Professors:
- [ ] RESEARCH_RESULTS_FOR_PAPER.md is comprehensive
- [ ] Methodology clearly documented
- [ ] All experiments reproducible
- [ ] Citations included
- [ ] Future work identified

---

## 🚀 YOU'RE DONE!

Your project is now **presentation-ready** for:
- ✅ Recruiters (technical depth + clean code)
- ✅ Professors (rigorous research + documentation)
- ✅ Collaborators (reproducible + well-organized)

**Next:** Share your GitHub link and send `ONE_PAGER.md` to anyone who asks about your research!
