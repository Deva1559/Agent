# Golden Evaluation Set Labeling & Sampling Guide

## 1. Overview
The Golden Evaluation Set consists of **192 hand-curated and verified customer support queries** extracted from the test dataset split (`data/splits/test.csv`). It serves as the benchmark for intent classification, historical retrieval relevance, response generation, and escalation evaluation.

## 2. Sampling Strategy
To ensure realistic coverage of production scenarios:
- **Stratified Intent Distribution**: Exactly ~22 representative samples per intent class across all 9 taxonomy categories.
- **Difficulty Tiering**:
  - **Easy**: Clear keyword structure and standard length (40–120 characters).
  - **Medium**: Multi-clause customer queries describing multiple symptoms (>120 characters).
  - **Hard**: Short/ambiguous queries (<35 characters), heavy internet slang/typos (`pls`, `thx`, `sucks`), or multi-intent customer complaints.

## 3. Taxonomy Definition & Rules

| Intent Class | Definition | Annotation Criteria | Confusable With |
|---|---|---|---|
| `playback_audio_issues` | Song skipping, audio cutoff, playback freeze | Mentions skipping, audio cutting out, bluetooth speaker issues | `app_crash_technical` |
| `app_crash_technical` | App closes to home screen or blank/black screen | Explicit app crash on launch or after update | `playback_audio_issues` |
| `billing_subscription_payment`| Double charge, payment failure, credit card | Payment deductions, receipts, bank charges | `student_family_discount` |
| `student_family_discount` | UNiDAYS, student discount, Family Plan address | NUS student verification, family member invites | `billing_subscription_payment` |
| `account_access_security` | Login errors, compromised/hacked account | Password reset failures, unauthorized logins | `billing_subscription_payment` |
| `offline_local_files` | Downloaded songs missing, local PC file sync | Offline downloads disappearing, greyed out tracks | `playback_audio_issues` |
| `content_metadata_playlists` | Wrong artist tagging, missing albums, lyrics | Wrong song under artist page, missing catalog items | `feedback_feature_request` |
| `feedback_feature_request` | UI complaints, shuffle algorithm complaints | Expresses dissatisfaction with app update/UI | `content_metadata_playlists` |
| `general_inquiry_other` | General customer service inquiries | Ambiguous or non-actionable queries | Any |

## 4. Handling Ambiguity & Disagreements
- If a customer mentions both **billing** and **account login**, label as `account_access_security` if login prevents account management; otherwise label as `billing_subscription_payment`.
- All hard edge cases are explicitly flagged with `difficulty: "hard"` for failure mode analysis.
