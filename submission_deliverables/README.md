# Hiver AI Customer Support Agent - SpotifyCares

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Hiver SDE Internship Take-Home Project**: A measurable, reproducible, grounded AI Customer Support Agent built on real `@SpotifyCares` Twitter support conversations.

---

## 🚀 Headline Benchmark Results

| System | Intent Accuracy | Macro F1 | Groundedness | Helpfulness | Escalation Quality | Overall Rating |
|---|---|---|---|---|---|---|
| **Baseline A (Majority + Generic)** | 39.5% | 0.068 | 5.00 / 5 | 2.00 / 5 | 2.00 / 5 | 2.50 / 5 |
| **Baseline B (TF-IDF + Simple Retrieval)** | **84.5%** | **0.794** | **5.00 / 5** | **4.00 / 5** | **5.00 / 5** | **4.61 / 5** |
| **Proposed (Semantic RAG + Risk Policy)** | 81.5% | 0.754 | 5.00 / 5 | 4.00 / 5 | 4.62 / 5 | 4.51 / 5 |

*All experiments evaluated on an independent 192-sample stratified Golden Evaluation Set with 0 conversation leakage.*

---

## ⚡ Reproduce Headline Results in < 15 Minutes

### 1. Environment Setup
```powershell
# Clone workspace & install dependencies
pip install -r requirements.txt
```

### 2. Run Data Pipeline & Leakage Audit
```powershell
# Profile raw twcs.csv & reconstruct Spotify conversation threads
python src/data/reconstruct_threads.py
python src/intent/discover_intents.py
python evaluation/leakage_check.py
```

### 3. Train Models & Build Vector Retrieval Index
```powershell
python src/intent/train_classifiers.py
python src/retrieval/retrieve_history.py
```

### 4. Run End-to-End Evaluation & Benchmarks
```powershell
python -m evaluation.baselines
python -m evaluation.human_agreement
```

### 5. Launch REST API & Demo UI
```powershell
python -m api.main
# Open demo/index.html in any browser
```

---

## 🏗 System Architecture
```
Incoming Customer Query
        │
        ▼
Intent Classifier (TF-IDF / SentenceTransformers)
        │
        ▼
Predicted Intent + Confidence
        │
        ▼
Historical Retrieval Index (Top-3 Cosine Similarity Match)
        │
        ▼
Grounded Response Generator
        │
        ▼
Multi-Signal Escalation Engine ---> [ AUTO-HANDLE ] or [ ESCALATE ] (with Reason)
```

---

## ⚠️ What is Misleading About My Headline Number?
While Baseline B achieves an **84.5% intent accuracy**, this headline number has production limitations:
1. **Class Imbalance**: Common playback queries dominate the dataset, inflating overall accuracy while minority intents perform lower.
2. **Short Tweet Format**: Twitter messages are concise (<140 chars). Multi-paragraph customer emails contain overlapping signals that increase intent confusion.
3. **Static 2017 Links**: Historical retrieval matches 2017 URLs (`spotify.com/nus`) which are inactive today.

---

## 📁 Key Documentation & Deliverables
- [`reports/technical_report.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/reports/technical_report.md) — Comprehensive Engineering & Evaluation Report.
- [`decision_log.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/decision_log.md) — 10 Engineering Decisions & Trade-offs.
- [`reports/failure_analysis.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/reports/failure_analysis.md) — Top 5 Real Failure Modes with Hypotheses.
- [`INTERVIEW_PREP.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/INTERVIEW_PREP.md) — 20 Hiver Interviewer Questions & Defense Answers.
- [`golden/golden_set.jsonl`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/golden/golden_set.jsonl) — 192 Hand-Annotated Golden Evaluation Samples.
