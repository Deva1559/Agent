# Hiver Interview Defense & Live Modification Guide

## Section A: 20 Likely Hiver Technical Interviewer Questions & Defensive Answers

### Q1: Why did you select `@SpotifyCares` instead of `AmazonHelp` or `AppleSupport`?
**Answer**: Data-driven analysis across 5 major handles showed `AppleSupport` relies heavily on generic DM requests ("Please DM us your iOS version..."), offering poor resolution text for RAG. `AmazonHelp` is dominated by unpredictable third-party seller shipping logistics. `SpotifyCares` offers 26,068 clean SaaS support threads with highly repeatable software/subscription resolution patterns.

### Q2: How did you ensure 0 conversation data leakage between Train and Test sets?
**Answer**: We performed splitting strictly at the `conversation_root_id` level (`evaluation/leakage_check.py`). Random tweet splitting causes follow-up customer replies to leak into train/test, artificially inflating accuracy. We verified zero thread ID overlap and zero exact text overlap.

### Q3: Why is your TF-IDF baseline outperforming your SentenceTransformers model on Intent Accuracy?
**Answer**: Short customer tweets (<140 characters) often contain distinct discriminative n-gram tokens (e.g. `unidays`, `nus`, `greyed out`, `skipping`). TF-IDF with 1-2 n-grams captures exact domain terminology directly, whereas dense embeddings compress short text into a general semantic space where distinct support keywords get smoothed out.

### Q4: Why not use a generative LLM (like GPT-4/Claude) directly for response generation?
**Answer**: Unconstrained generative LLMs risk hallucinating unsupported financial promises or refund amounts. Our grounded response generator conditions replies directly on verified historical resolution evidence or deterministic brand policy templates.

### Q5: How does your escalation engine work?
**Answer**: It uses a multi-signal risk evaluator: intent confidence score (<0.65), retrieval vector similarity (<0.55), high-risk classification category (`account_access_security` / `billing_subscription_payment`), and historical resolution conflict variance.

---

## Section B: Live Coding & Modification Exercises for Interview

### Exercise 1: "Change the Escalation Threshold"
- **Target File**: [`src/escalation/escalation_engine.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/escalation/escalation_engine.py#L9-L15)
- **Modification**: Adjust `min_confidence_threshold` (e.g. from `0.65` to `0.80`) or `min_retrieval_similarity`.

### Exercise 2: "Add a New Intent (e.g. `car_thing_hardware`)"
- **Target File**: [`src/intent/discover_intents.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/src/intent/discover_intents.py#L9-L70)
- **Modification**: Append `"car_thing_hardware"` with keywords `["car thing", "bluetooth car", "dash"]` to `INTENT_TAXONOMY`.

### Exercise 3: "Return Top-5 Historical Evidence Cases Instead of Top-3"
- **Target File**: [`api/main.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/api/main.py#L52)
- **Modification**: Change `k=3` to `k=5` in `models["retriever"].retrieve(msg, k=5, filter_intent=pred_intent)`.
