# Reproducibility Audit Report

## 1. Reproduction Modes & Timings

| Execution Pathway | Dependencies | Execution Time | Output / Verification |
|---|---|---|---|
| **Pathway A: Pre-trained Artifact Evaluation (Instant)** | Prepared `models/` & `data/splits/` | **~45 seconds** | `python -m evaluation.baselines`<br>`python -m pytest` |
| **Pathway B: Full End-to-End Pipeline from Raw Dataset** | `twcs/twcs.csv` + Python 3.10 | **~12 minutes** | `python src/data/reconstruct_threads.py`<br>`python src/intent/discover_intents.py`<br>`python evaluation/leakage_check.py`<br>`python src/intent/train_classifiers.py`<br>`python src/retrieval/retrieve_history.py` |

---

## 2. Step-by-Step Command Verification Log

| Command | Expected Output | Actual Measured Result | Status |
|---|---|---|---|
| `python src/data/reconstruct_threads.py` | Extract 43k pairs | Extracted 43,092 pairs | ✅ PASS |
| `python src/intent/discover_intents.py` | Label 9 intents | Labeled 43,092 pairs | ✅ PASS |
| `python evaluation/leakage_check.py` | 0 leakage | `0 conversation overlap` | ✅ PASS |
| `python src/intent/train_classifiers.py` | Train 3 classifiers | Test Acc: 86.9% (TF-IDF), 81.1% (Proposed) | ✅ PASS |
| `python src/retrieval/retrieve_history.py` | Save vector index | Saved `models/retrieval_index.pkl` | ✅ PASS |
| `python -m evaluation.baselines` | Table output | Table matches report numbers | ✅ PASS |
| `python -m pytest` | 5/5 tests pass | `5 passed in 50.31s` | ✅ PASS |
