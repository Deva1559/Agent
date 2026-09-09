# Repository Inventory

## Overview
This inventory lists every source code file, script, dataset, config, model artifact, evaluation script, and report in the project repository.

| File / Folder | Purpose | Importance | Potential Risk / Issue | Status |
|---|---|---|---|---|
| [`api/main.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/api/main.py) | Production REST API & Static UI mount | HIGH | Relies on startup model loading | ✅ VERIFIED (Healthy) |
| [`demo/index.html`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/demo/index.html) | Interactive single-page web UI | HIGH | None | ✅ VERIFIED |
| [`src/data/profile_data.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/data/profile_data.py) | Data profiling script for `twcs.csv` | MEDIUM | Takes ~2 mins on full 2.8M CSV | ✅ VERIFIED |
| [`src/data/analyze_brands.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/data/analyze_brands.py) | Multi-brand thread reconstruction analysis | HIGH | High memory usage on 2.8M rows | ✅ VERIFIED |
| [`src/data/reconstruct_threads.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/data/reconstruct_threads.py) | Conversation thread pair extractor | HIGH | None | ✅ VERIFIED |
| [`src/intent/discover_intents.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/intent/discover_intents.py) | Intent labeling script & taxonomy definition | HIGH | None | ✅ VERIFIED |
| [`src/intent/train_classifiers.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/intent/train_classifiers.py) | Baseline & Proposed classifier trainer | CRITICAL | CPU encoding time ~7 mins | ✅ VERIFIED |
| [`src/retrieval/retrieve_history.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/retrieval/retrieve_history.py) | Historical vector retriever module | CRITICAL | Index building takes ~3 mins | ✅ VERIFIED |
| [`src/escalation/escalation_engine.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/escalation/escalation_engine.py) | Risk policy & grounded response generator | CRITICAL | None | ✅ VERIFIED |
| [`evaluation/leakage_check.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/evaluation/leakage_check.py) | Train/Dev/Test split & Leakage auditor | CRITICAL | None | ✅ VERIFIED (0 leakage) |
| [`evaluation/llm_judge.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/evaluation/llm_judge.py) | LLM-as-a-Judge evaluation harness | HIGH | Rule-based surrogate | ✅ VERIFIED |
| [`evaluation/human_agreement.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/evaluation/human_agreement.py) | Human vs Judge correlation script | HIGH | None | ✅ VERIFIED (r=0.4644) |
| [`evaluation/baselines.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/evaluation/baselines.py) | Comparative baseline evaluation runner | CRITICAL | None | ✅ VERIFIED |
| [`golden/golden_set.jsonl`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/golden/golden_set.jsonl) | 192 hand-annotated golden evaluation samples | CRITICAL | None | ✅ VERIFIED |
| [`golden/labeling_guide.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/golden/labeling_guide.md) | Annotation & ambiguity guidelines | MEDIUM | None | ✅ VERIFIED |
| [`tests/test_pipeline.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/tests/test_pipeline.py) | Pytest automated test suite | HIGH | None | ✅ VERIFIED (5/5 PASS) |
| [`reports/brand_selection.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/reports/brand_selection.md) | Data-driven brand selection report | HIGH | None | ✅ VERIFIED |
| [`reports/failure_analysis.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/reports/failure_analysis.md) | Top 5 real failure modes report | HIGH | None | ✅ VERIFIED |
| [`reports/technical_report.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/reports/technical_report.md) | Comprehensive technical report | CRITICAL | None | ✅ VERIFIED |
| [`decision_log.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/decision_log.md) | 10 non-obvious engineering decisions | HIGH | None | ✅ VERIFIED |
| [`INTERVIEW_PREP.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/INTERVIEW_PREP.md) | 20 mock interview Q&As & live code edits | HIGH | None | ✅ VERIFIED |
| [`README.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/README.md) | Reproduction & project overview | CRITICAL | None | ✅ VERIFIED |
| [`requirements.txt`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/requirements.txt) | Python package dependencies | HIGH | None | ✅ VERIFIED |
| [`FINAL_AUDIT.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/FINAL_AUDIT.md) | 23-point requirement checklist | CRITICAL | None | ✅ VERIFIED |
