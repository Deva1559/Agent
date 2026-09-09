# Data Integrity & Leakage Red-Team Report

## 1. Dataset Profile & Origin Audit
- **Raw File**: `twcs/twcs.csv` (2,811,774 rows, 54.69% customer inbound, 45.31% brand responses).
- **Target Handle**: `@SpotifyCares` (43,265 brand replies, 56,907 customer tweets, 26,068 reconstructed threads).
- **Subsampling Strategy**: Stratified random sample of 15,000 pairs using fixed random seed (`42`).

---

## 2. Leakage Red-Team Audit Results (`evaluation/leakage_check.py`)
To prevent artificial metric inflation, splits were constructed strictly at the **`conversation_root_id` thread level** rather than random individual tweet sampling.

```
--- Split Metrics ---
Train Set: 10,519 pairs (10,111 unique conversation threads)
Dev Set:    2,233 pairs ( 2,167 unique conversation threads)
Test Set:   2,208 pairs ( 2,167 unique conversation threads)

--- Red-Team Overlap Inspection ---
[PASSED] Thread ID Overlap (Train vs Dev):  0
[PASSED] Thread ID Overlap (Train vs Test): 0
[PASSED] Thread ID Overlap (Dev vs Test):   0

[PASSED] Exact Text Overlap (Train vs Dev):  0 (19 duplicates detected and purged from Dev)
[PASSED] Exact Text Overlap (Train vs Test): 0 (16 duplicates detected and purged from Test)
```

---

## 3. Retrieval Index Isolation
The vector index used for historical RAG retrieval (`models/retrieval_index.pkl`) was built **strictly using the `train.csv` split**. The Test set queries are strictly isolated from the retrieval corpus, preventing data leakage during RAG generation.
