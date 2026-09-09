# Technical & Evaluation Report: AI Customer Support Agent for SpotifyCares

## 1. Problem Framing
Customer support engineering on social platforms like Twitter requires balancing low latency, high intent classification accuracy, and strict safety guardrails against AI hallucinations. For **SpotifyCares**, customer queries range from straightforward troubleshooting (e.g. song skipping, clean reinstall) to sensitive account security breaches. The goal of this system is to evaluate an end-to-end grounded agent that classifies intents, retrieves historical brand resolutions, drafts replies, and makes transparent auto-handle vs escalation decisions.

---

## 2. Dataset & Intent Taxonomy Design
From the raw Kaggle dataset of ~2.8M tweets (`twcs.csv`), we systematically extracted **88,445 tweets** (26,068 reconstructed multi-turn conversation threads) involving `@SpotifyCares`. 

We established an 8-class domain-specific intent taxonomy + 1 fallback class:
1. `playback_audio_issues`: Song skipping, audio cutoff, playback freezing.
2. `app_crash_technical`: App crashing to home screen, launch failures.
3. `billing_subscription_payment`: Double charges, payment failures, receipts.
4. `student_family_discount`: UNiDAYS student discount verification, Family Plan address matching.
5. `account_access_security`: Password reset, hacked accounts, unauthorized device logins.
6. `offline_local_files`: Disappearing downloaded tracks, local desktop file sync.
7. `content_metadata_playlists`: Wrong artist page tagging, missing albums.
8. `feedback_feature_request`: UI update complaints, shuffle algorithm feedback.
9. `general_inquiry_other`: Ambiguous/uncategorized support queries.

---

## 3. System Architecture
```
Incoming Customer Message
        │
        ▼
Intent Classifier (SentenceTransformers + LogReg / TF-IDF)
        │
        ▼
Predicted Intent + Confidence Score
        │
        ▼
Historical Retrieval Index (Cosine Similarity over 10.5k Historical Cases)
        │
        ▼
Grounded Response Generator (Historical Brand Resolution Evidence)
        │
        ▼
Escalation Policy Engine (Multi-Signal Risk Analysis)
        ├── AUTO-HANDLE
        └── HUMAN ESCALATION (with explicit human-readable reason)
```

---

## 4. Experimental Results & Baseline Comparison

| System | Intent Accuracy | Macro F1 | Groundedness | Helpfulness | Escalation Quality | Overall Rating |
|---|---|---|---|---|---|---|
| **Baseline A (Majority + Generic)** | 39.5% | 0.068 | 5.00 / 5 | 2.00 / 5 | 2.00 / 5 | 2.50 / 5 |
| **Baseline B (TF-IDF + Simple Retrieval)** | **84.5%** | **0.794** | 5.00 / 5 | 4.00 / 5 | 5.00 / 5 | **4.61 / 5** |
| **Proposed (Semantic RAG + Risk Policy)** | 81.5% | 0.754 | 5.00 / 5 | 4.00 / 5 | 4.62 / 5 | 4.51 / 5 |

---

## 5. Human vs. LLM-as-a-Judge Agreement
We evaluated 30 hand-annotated golden evaluation samples comparing human quality ratings against automated judge outputs:
- **Spearman Rank Correlation**: `0.4644` (p = 0.0097)
- **Mean Absolute Error (MAE)**: `0.1967`
- **Finding**: Moderate positive correlation with low absolute error. The judge accurately penalizes hallucinated financial claims but slightly overestimates tone formality compared to human evaluators.

---

## 6. Failure Analysis
See full empirical failure modes in [`reports/failure_analysis.md`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/reports/failure_analysis.md). Key issues stem from surface keyword dominance (`app_crash_technical` vs `playback_audio_issues`) and internet slang noise.

---

## 7. What is Misleading About My Headline Number?
> **Brutally Honest Evaluation Note**:
> While Baseline B achieves an impressive **84.5% intent accuracy** and 4.61/5 overall rating on our test set, **this headline number is optimistic compared to real-world production deployment**. 
> 
> 1. **Class Imbalance**: The dataset contains a high proportion of routine playback queries (`playback_audio_issues` & `account_access_security`), which inflates overall accuracy while minority classes like `app_crash_technical` (Macro F1 ~0.75) perform lower.
> 2. **Short Tweet Nature**: Customer tweets on Twitter are artificially concise (<140 characters). Real email support tickets (like Hiver handles) are multi-paragraph, containing multiple overlapping intent signals that will increase intent confusion.
> 3. **Static Link Stale Knowledge**: Historical retrieval retrieves 2017 links (`spotify.com/nus`) which, while matching historical ground truth, are dead links today.

---

## 8. What Would I Do With One More Week?
1. **Hierarchical Intent Classifier**: Implement a 2-stage classifier (Stage 1: Support vs General Feedback; Stage 2: Specific Sub-intent) to resolve overlap between `playback_audio_issues` and `app_crash_technical`.
2. **FAISS Vector Indexing with Quantization**: Replace exact Cosine Similarity with `faiss-cpu` HNSW index for sub-millisecond retrieval scale.
3. **Active Learning & Human-in-the-loop Interface**: Build an admin review UI where support agents can correct misclassified intent predictions and update historical resolution templates in real-time.
4. **Contextual Slang Normalizer**: Integrate a custom domain pre-processor for Twitter/SMS abbreviations to boost intent F1 on noisy customer queries.
