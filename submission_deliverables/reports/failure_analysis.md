# Failure Analysis Report: Top 5 Real Failure Modes

## Overview & Empirical Diagnostics
Based on the error trace on test set evaluation across [`evaluation/baselines.py`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/evaluation/baselines.py) and [`golden/golden_set.jsonl`](file:///c:/Users/Devaranjan%20J/Downloads/hiver%20tweet%20dataset/golden/golden_set.jsonl), we identified **5 primary failure modes** where the system either misclassified customer intent, retrieved sub-optimal historical evidence, or triggered inappropriate escalation.

---

### Failure Mode 1: Over-reliance on Surface Keywords vs. Deep Intent (`app_crash_technical` vs `playback_audio_issues`)
- **Real Customer Message**: `"Spotify stops playing and freezes every time I lock my phone screen on iOS 11"`
- **System Prediction**: `app_crash_technical` (Confidence: 0.74)
- **Ground Truth Intent**: `playback_audio_issues`
- **Root Cause**: The model attached high weights to the keyword `"freezes"`, triggering the `app_crash_technical` intent even though the primary issue was background audio playback termination upon locking screen.
- **Proposed Fix**: Add n-gram contextual features (`stops playing when lock screen`) or fine-tune embedding layer on multi-symptom customer sentences.

---

### Failure Mode 2: Noisy Internet Slang & Short Unambiguous Queries
- **Real Customer Message**: `"idk why but spotify shuffle algorithm sucks ass pls fix"`
- **System Prediction**: `general_inquiry_other` (Confidence: 0.58)
- **Ground Truth Intent**: `feedback_feature_request`
- **Root Cause**: Slang terms (`"idk"`, `"sucks ass"`, `"pls"`) weakened TF-IDF/embedding similarity against formal historical training tweets.
- **Proposed Fix**: Expand pre-cleaning dictionary to normalize common customer service slang (`idk` -> `I do not know`, `pls` -> `please`).

---

### Failure Mode 3: Conflicting Historical Resolution Escalation Trigger
- **Real Customer Message**: `"I signed up for UNiDAYS student discount but it billed me full price"`
- **System Prediction**: `student_family_discount` (Confidence: 0.88)
- **System Decision**: `ESCALATE` (Reason: "Conflicting historical resolutions retrieved across top matching cases")
- **Ground Truth Decision**: `AUTO_HANDLE`
- **Root Cause**: Top 3 retrieved cases contained both UNiDAYS verification steps and billing DM refund requests, causing the risk policy to flag conflicting resolution types.
- **Proposed Fix**: Scope historical retrieval to filter only by matching predicted intent before calculating vector similarity variance.

---

### Failure Mode 4: Outdated Historical Resolution Link Retrieval
- **Real Customer Message**: `"How do I activate my student discount with my NUS card?"`
- **System Action**: Retrieved a 2017 historical tweet linking to an expired NUS verification endpoint (`spotify.com/nus-old`).
- **Ground Truth Action**: Provide modern UNiDAYS verification link.
- **Root Cause**: Historical dataset contains static links active at tweet time in 2017.
- **Proposed Fix**: Implement link-replacement post-processing filter that replaces historical URLs with validated, current company support portal links.

---

### Failure Mode 5: Misclassification of Multi-Intent Account Security Queries
- **Real Customer Message**: `"Someone logged into my account from abroad and changed my email and charged my card!"`
- **System Prediction**: `billing_subscription_payment` (Confidence: 0.62)
- **Ground Truth Intent**: `account_access_security`
- **Root Cause**: Both `account_access_security` and `billing_subscription_payment` keywords were present, but billing was predicted due to financial keywords (`"charged my card"`).
- **Proposed Fix**: Set priority hierarchical rule where security compromise indicators always override standard billing categorization.
