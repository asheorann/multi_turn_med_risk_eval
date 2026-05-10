# MultiTurnPSB: Research Paper

## Paper

**📄 [MultiTurnPSB_Paper.pdf](MultiTurnPSB_Paper.pdf)**

## Abstract

**Does the safety of LLM responses to patient medical queries degrade across multi-turn conversations under escalating pressure?**

This paper presents the first multi-turn medical safety benchmark, extending Microsoft Research's PatientSafetyBench (466 queries) into 4-turn escalating conversations. We evaluate GPT-4.1-mini and Claude Sonnet 4.5 under three attack types: template-fixed, template-adaptive, and adversarial-live.

**Key Findings:**
- Models with nearly identical single-turn safety (GPT: 34.5%, Claude: 31.3%) diverge by **19x under adversarial attacks** (GPT: 78.8% vs Claude: 4.1%)
- **Adversarial attacks 73% more effective** than optimized templates (78.8% vs 59.7%)
- **Claude Opus 4.5 refuses to generate attacks** despite "research" framing (safety hierarchy revealed)
- **Classifier degradation:** Claude classifier accuracy drops from 95.5% → 48.5% under adversarial pressure

## Citation

```bibtex
@misc{multiturnpsb2026,
  title={MultiTurnPSB: Evaluating Safety Degradation in Multi-Turn Patient Interactions},
  author={Sheoran, Anushka},
  year={2026},
  institution={University of Pennsylvania},
  note={CIS 700 Agentic AI Final Project}
}
```

## Quick Links

- **Main Repository:** [../README.md](../README.md)
- **One-Page Summary:** [../ONE_PAGER.md](../ONE_PAGER.md)
- **Full Research Documentation:** [../RESEARCH_RESULTS_FOR_PAPER.md](../RESEARCH_RESULTS_FOR_PAPER.md)
- **Quick Start Guide:** [../QUICKSTART.md](../QUICKSTART.md)

## Related Work

This work directly addresses gaps identified in:
- **MedRiskEval** (Microsoft Research, EACL 2026): "Future work should explore multi-turn interactions where patients escalate or rephrase queries."
- **CSEDB** (npj Digital Medicine, 2025): "Single-turn evaluation does not capture conversational dynamics that may lead to safety failures."

## Contact

**Author:** Anushka Sheoran
**Institution:** University of Pennsylvania
**Course:** CIS 700 Agentic AI

For questions or collaboration inquiries, please open an issue in the main repository.
