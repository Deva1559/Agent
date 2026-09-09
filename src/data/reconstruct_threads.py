import pandas as pd
import json
import re
import os

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # Remove HTML entities like &amp;, &gt;, &lt;
    text = text.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
    # Clean multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def reconstruct_and_clean(input_path: str = "twcs/twcs.csv", brand: str = "SpotifyCares"):
    print(f"Reconstructing conversation threads for {brand} from {input_path}...")
    df = pd.read_csv(input_path, dtype=str)
    
    # Clean text column
    df["text_clean"] = df["text"].apply(clean_text)
    
    # All tweets by brand
    brand_tweets = df[df["author_id"] == brand].copy()
    
    # Customer parent tweets replied to by brand
    parent_ids = set(brand_tweets["in_response_to_tweet_id"].dropna().unique())
    parent_tweets = df[df["tweet_id"].isin(parent_ids)].copy()
    
    # Customer followups replying to brand tweets
    brand_tweet_ids = set(brand_tweets["tweet_id"].unique())
    followup_tweets = df[df["in_response_to_tweet_id"].isin(brand_tweet_ids)].copy()
    
    # Merge all relevant tweets
    combined = pd.concat([brand_tweets, parent_tweets, followup_tweets]).drop_duplicates(subset="tweet_id")
    
    # Link parent-child pairs to build turn-1 customer queries and brand resolutions
    # A customer support pair: (Customer message -> Brand response)
    # 1. Direct pairs where Brand replied to Customer (in_response_to_tweet_id = customer_tweet_id)
    pairs = []
    
    # Index for fast lookup
    tweet_dict = combined.set_index("tweet_id").to_dict("index")
    
    for b_id, b_row in brand_tweets.iterrows():
        parent_id = b_row["in_response_to_tweet_id"]
        if pd.notna(parent_id) and parent_id in tweet_dict:
            parent_tweet = tweet_dict[parent_id]
            # Ensure parent is from customer (inbound == True)
            if parent_tweet["inbound"] == "True":
                pairs.append({
                    "pair_id": f"{parent_id}_{b_row['tweet_id']}",
                    "conversation_root_id": parent_id if pd.isna(parent_tweet["in_response_to_tweet_id"]) else parent_tweet["in_response_to_tweet_id"],
                    "customer_tweet_id": parent_id,
                    "customer_author_id": parent_tweet["author_id"],
                    "customer_text": parent_tweet["text_clean"],
                    "customer_created_at": parent_tweet["created_at"],
                    "brand_tweet_id": b_row["tweet_id"],
                    "brand_author_id": brand,
                    "brand_text": b_row["text_clean"],
                    "brand_created_at": b_row["created_at"]
                })
                
    pairs_df = pd.DataFrame(pairs)
    print(f"Extracted {len(pairs_df):,} Customer-Brand interaction pairs.")
    
    os.makedirs("data/processed", exist_ok=True)
    pairs_df.to_csv("data/processed/spotify_pairs.csv", index=False)
    print("Saved data/processed/spotify_pairs.csv")

if __name__ == "__main__":
    reconstruct_and_clean()
