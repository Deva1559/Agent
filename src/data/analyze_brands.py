import pandas as pd
import json
import os

def analyze_candidate_brands(input_path: str, candidates: list):
    print(f"Loading {input_path} to analyze brand candidates: {candidates}...")
    df = pd.read_csv(input_path, dtype=str)
    
    results = {}
    
    for brand in candidates:
        print(f"Analyzing {brand}...")
        brand_tweets = df[df["author_id"] == brand].copy()
        
        # Customer tweets replied to by brand
        replied_to_ids = set(brand_tweets["in_response_to_tweet_id"].dropna().unique())
        
        # Followups
        brand_tweet_ids = set(brand_tweets["tweet_id"].unique())
        followups = df[df["in_response_to_tweet_id"].isin(brand_tweet_ids)].copy()
        
        # Original customer tweets
        originals = df[df["tweet_id"].isin(replied_to_ids)].copy()
        
        combined = pd.concat([brand_tweets, originals, followups]).drop_duplicates(subset="tweet_id")
        
        num_brand_tweets = len(brand_tweets)
        num_customer_tweets = len(originals) + len(followups)
        total_rows = len(combined)
        
        # Measure conversational threads
        # A thread is anchored by an original tweet (in_response_to_tweet_id is NaN and inbound==True)
        thread_starts = originals[originals["in_response_to_tweet_id"].isna()]
        num_threads = len(thread_starts)
        avg_thread_len = round(total_rows / max(1, num_threads), 2)
        
        # Check text length / quality of customer issues
        avg_cust_text_len = round(originals["text"].str.len().mean(), 1) if len(originals) > 0 else 0
        
        results[brand] = {
            "total_thread_rows": total_rows,
            "brand_replies": num_brand_tweets,
            "customer_tweets": num_customer_tweets,
            "reconstructed_threads": num_threads,
            "avg_thread_length": avg_thread_len,
            "avg_customer_msg_length": avg_cust_text_len
        }
        
    os.makedirs("reports", exist_ok=True)
    with open("reports/brand_analysis.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved reports/brand_analysis.json")

if __name__ == "__main__":
    candidates = ["SpotifyCares", "AppleSupport", "AmazonHelp", "Uber_Support", "hulu_support"]
    analyze_candidate_brands("twcs/twcs.csv", candidates)
