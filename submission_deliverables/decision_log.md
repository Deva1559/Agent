# Decision Log (Final Summary)

## Decision 001: Brand Selection — Choosing `SpotifyCares` over `AmazonHelp` / `AppleSupport`
- **Date**: 2026-09-09
- **Decision**: Select `SpotifyCares` as the target support brand.
- **Choice**: `SpotifyCares` (88,445 tweets, 26,068 threads).
- **Reason**: High signal-to-noise ratio in software/subscription troubleshooting workflows (troubleshooting app crashes, billing, student discounts) with explicit historical resolution steps.

---

## Decision 002: Intent Taxonomy Size & Structure
- **Date**: 2026-09-09
- **Decision**: Establish an 8-class domain-specific support taxonomy for Spotify + 1 catch-all (`general_inquiry_other`).
- **Reason**: Covers 100% of customer query space while maintaining high inter-class distinctness for classification and retrieval.

---

## Decision 003: Thread-Level Conversation Splitting to Prevent Data Leakage
- **Date**: 2026-09-09
- **Decision**: Split train/dev/test datasets strictly at the `conversation_root_id` level rather than random tweet-level sampling.
- **Reason**: Random tweet splitting leaks context (follow-up tweets from the same customer-agent exchange appear in both train and test), inflating accuracy metrics artificially.

---

## Decision 004: SentenceTransformers (`all-MiniLM-L6-v2`) Embedding Model
- **Date**: 2026-09-09
- **Decision**: Use `all-MiniLM-L6-v2` for lightweight semantic embeddings on CPU.
- **Reason**: Fast 384-dimensional vector encoding on CPU with strong semantic similarity performance for short text.

---

## Decision 005: Multi-Signal Risk-Based Escalation Engine
- **Date**: 2026-09-09
- **Decision**: Build an explicit multi-signal policy evaluate (intent confidence + retrieval similarity + security risk flag + resolution conflict).
- **Reason**: Simple confidence thresholds fail on high-risk account breach or billing refund cases.

---

## Decision 006: Deterministic Grounded Templates vs Unconstrained LLM Generation
- **Date**: 2026-09-09
- **Decision**: Ground replies strictly in historical resolution evidence or deterministic templates.
- **Reason**: Unconstrained generative LLMs risk hallucinating unsupported financial promises or invalid refund policies.

---

## Decision 007: 192-Sample Stratified Golden Set Construction
- **Date**: 2026-09-09
- **Decision**: Create 192 hand-annotated examples stratified by intent and difficulty (easy/medium/hard).
- **Reason**: Provides statistical evaluation coverage without synthetic label fabrication.

---

## Decision 008: Human vs. LLM-as-a-Judge Validation (30-sample subset)
- **Date**: 2026-09-09
- **Decision**: Calculate Spearman rank correlation and MAE between human quality ratings and judge outputs.
- **Reason**: Validates judge reliability before relying on automated evaluation scores.

---

## Decision 009: In-Memory Cosine Similarity vs Heavy Vector Databases
- **Date**: 2026-09-09
- **Decision**: Use scikit-learn cosine similarity over numpy matrices rather than installing Milvus or Qdrant.
- **Reason**: Keeps repository lightweight and runnable in under 15 minutes without external daemon services.

---

## Decision 010: FastAPI + Lightweight Single-Page HTML/JS Demo UI
- **Date**: 2026-09-09
- **Decision**: Serve API via FastAPI and UI via lightweight single-page frontend.
- **Reason**: Maximum evaluator clarity without node_modules dependency bloat.
