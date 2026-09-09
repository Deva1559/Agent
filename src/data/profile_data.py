import pandas as pd
import json
import os

def profile_dataset(input_path: str):
    print(f"Reading full dataset from {input_path}...")
    df = pd.read_csv(input_path, dtype=str)
    
    total_rows = len(df)
    columns = list(df.columns)
    missing_values = {col: int(df[col].isna().sum()) for col in columns}
    missing_pct = {col: round((missing_values[col] / total_rows) * 100, 2) for col in columns}
    
    duplicate_tweets = int(df.duplicated(subset=['tweet_id']).sum())
    duplicate_texts = int(df.duplicated(subset=['text']).sum())
    
    inbound_counts = df['inbound'].value_counts().to_dict()
    
    # Identify non-numeric author_ids (brands usually have text handles, customers are masked numeric IDs)
    # Filter for authors that are alphabetic/brand-like
    brand_df = df[df['inbound'] == 'False']
    brand_counts = brand_df['author_id'].value_counts()
    top_brands = brand_counts.head(20).to_dict()
    
    profile = {
        "dataset_path": input_path,
        "total_rows": total_rows,
        "columns": columns,
        "missing_values": missing_values,
        "missing_percentage": missing_pct,
        "duplicate_tweet_ids": duplicate_tweets,
        "duplicate_texts": duplicate_texts,
        "inbound_distribution": inbound_counts,
        "top_20_brands": top_brands
    }
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/data_profile.json", "w") as f:
        json.dump(profile, f, indent=2)
    print("Saved reports/data_profile.json")

if __name__ == "__main__":
    profile_dataset("twcs/twcs.csv")
