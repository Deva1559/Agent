# Hiver Submission Checklist & Verification Gate

## Mandatory Criteria Verification

- [x] **REQ-01: Intent classification from real brand data** — [`src/intent/discover_intents.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/intent/discover_intents.py)
- [x] **REQ-02: Reply generation grounded in historical resolutions** — [`src/escalation/escalation_engine.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/escalation/escalation_engine.py)
- [x] **REQ-03: Auto-handle vs escalation with stated reason** — [`src/escalation/escalation_engine.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/escalation/escalation_engine.py)
- [x] **REQ-04: Runnable repository** — [`README.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/README.md) & [`api/main.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/api/main.py)
- [x] **REQ-05: README reproduces results in < 15 minutes** — [`README.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/README.md)
- [x] **REQ-06: Golden set of 150-250 hand-labeled examples** — [`golden/golden_set.jsonl`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/golden/golden_set.jsonl) (192 queries)
- [x] **REQ-07: Automated evaluation metrics** — [`evaluation/baselines.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/evaluation/baselines.py)
- [x] **REQ-08: LLM-as-a-judge for reply quality** — [`evaluation/llm_judge.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/evaluation/llm_judge.py)
- [x] **REQ-09: Evidence of LLM-judge vs human agreement** — [`evaluation/human_agreement.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/evaluation/human_agreement.py) (`r=0.4644`)
- [x] **REQ-10: Results against 2 baselines (trivial & simple)** — [`evaluation/baselines.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/evaluation/baselines.py)
- [x] **REQ-11: Top 5 real failure modes** — [`reports/failure_analysis.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/reports/failure_analysis.md)
- [x] **REQ-12: Mandatory section "What is misleading about my headline number?"** — [`reports/technical_report.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/reports/technical_report.md)
- [x] **REQ-13: "What would I do with one more week?"** — [`reports/technical_report.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/reports/technical_report.md)
- [x] **REQ-14: 10 non-obvious engineering decisions** — [`decision_log.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/decision_log.md)

## Status: ALL 14 CRITERIA PASSED ✅
