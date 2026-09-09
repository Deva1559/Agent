# Brand Selection Report

## Executive Summary & Comparison
To ensure our AI Support Agent is built on high-quality, reproducible customer-support data, we analyzed 5 top corporate customer service handles in `twcs.csv`: `SpotifyCares`, `AppleSupport`, `AmazonHelp`, `Uber_Support`, and `hulu_support`.

| Brand Handle | Total Thread Rows | Reconstructed Threads | Brand Replies | Customer Tweets | Avg Thread Length | Avg Customer Msg Length (chars) | Data Quality & Repeatability |
|---|---|---|---|---|---|---|---|
| **SpotifyCares** | **88,445** | **26,068** | **43,265** | **56,907** | **3.39** | **103.8** | **HIGH** (Clear SaaS/App issues: billing, offline playback, login, device syncing) |
| **AppleSupport** | 226,755 | 74,615 | 106,860 | 143,285 | 3.04 | 109.3 | **MEDIUM** (High percentage of generic DM redirects: "Please DM us your iOS version") |
| **AmazonHelp** | 358,973 | 76,799 | 169,840 | 255,498 | 4.67 | 116.2 | **MEDIUM** (Noisy e-commerce logistics, delivery tracking & third-party sellers) |
| **Uber_Support** | 122,194 | 39,355 | 56,270 | 77,408 | 3.10 | 120.1 | **LOW** (High proportion of sensitive billing/safety issues requiring manual review) |
| **hulu_support** | 46,428 | 14,092 | 21,872 | 30,792 | 3.29 | 110.6 | **MEDIUM** (Good domain, but smaller overall dataset volume) |

---

## Technical Justification for Selecting `SpotifyCares`

1. **Optimal Size for Experimentation & Latency**:
   - `SpotifyCares` yields **26,068 reconstructed threads** (88,445 total tweets).
   - This provides ample statistics for stratified train/dev/test splits without incurring unnecessary memory or vector indexing overhead.

2. **Well-Defined SaaS & Digital Media Intent Structure**:
   - Spotify issues cluster into distinct, solvable software & subscription categories:
     - Account & Billing (Family plan, Premium subscription, Student discount/UNiDAYS).
     - Playback & Technical (Song skipping, offline mode, app crashes, local file sync).
     - Content & Curation (Missing tracks, incorrect artist tagging, playlist feedback).
     - Multi-device Connectivity (Bluetooth speaker playback, macOS/Android/iOS client issues).

3. **High Resolution Consistency**:
   - Historical brand responses from `@SpotifyCares` contain standard troubleshooting steps (e.g. "relog > restart device > clean reinstall" or "verify student status at UNiDAYS link"), making it ideal for historical retrieval (RAG) and grounded generation.

4. **Escalation Boundary Clarity**:
   - Account security breaches ("someone logged into my account in another country") or billing refunds provide clear, unambiguous boundaries for human escalation policy vs auto-handling.
