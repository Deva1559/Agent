# Data Profile Report: Kaggle Twitter Customer Support (`twcs.csv`)

## Overview & Metadata
- **Dataset File Path**: `twcs/twcs.csv`
- **Total Rows**: 2,811,774
- **Columns**: 7 (`tweet_id`, `author_id`, `inbound`, `created_at`, `text`, `response_tweet_id`, `in_response_to_tweet_id`)

## Column Statistics & Missing Values
| Column Name | Data Type | Missing Count | Missing Percentage | Description |
|---|---|---|---|---|
| `tweet_id` | String | 0 | 0.00% | Unique identifier for each tweet |
| `author_id` | String | 0 | 0.00% | Anonymized user ID (numbers) or brand handle (text) |
| `inbound` | Boolean | 0 | 0.00% | `True` = Customer to Brand, `False` = Brand to Customer |
| `created_at` | String | 0 | 0.00% | Timestamp of tweet |
| `text` | String | 0 | 0.00% | Content of tweet |
| `response_tweet_id` | String | 1,040,629 | 37.01% | Comma-separated tweet IDs that responded to this tweet |
| `in_response_to_tweet_id` | String | 794,335 | 28.25% | Parent tweet ID this tweet responded to |

## Data Quality & Integrity
- **Duplicate `tweet_id`s**: 0 (100% unique primary keys)
- **Duplicate `text`s**: 29,156 (~1.03% exact duplicates, e.g. automated generic thank-yous)
- **Inbound Distribution**:
  - `True` (Customer messages): 1,537,843 (54.69%)
  - `False` (Brand responses): 1,273,931 (45.31%)

## Top 20 Support Brands by Tweet Volume
1. `AmazonHelp`: 169,840 brand tweets
2. `AppleSupport`: 106,860 brand tweets
3. `Uber_Support`: 56,270 brand tweets
4. `SpotifyCares`: 43,265 brand tweets
5. `Delta`: 42,253 brand tweets
6. `Tesco`: 38,573 brand tweets
7. `AmericanAir`: 36,764 brand tweets
8. `TMobileHelp`: 34,317 brand tweets
9. `comcastcares`: 33,031 brand tweets
10. `British_Airways`: 29,361 brand tweets
11. `SouthwestAir`: 28,977 brand tweets
12. `VirginTrains`: 27,817 brand tweets
13. `Ask_Spectrum`: 25,860 brand tweets
14. `XboxSupport`: 24,557 brand tweets
15. `sprintcare`: 22,381 brand tweets
16. `hulu_support`: 21,872 brand tweets
17. `sainsburys`: 19,466 brand tweets
18. `GWRHelp`: 19,364 brand tweets
19. `AskPlayStation`: 19,098 brand tweets
20. `ChipotleTweets`: 18,749 brand tweets
