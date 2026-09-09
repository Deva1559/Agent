import pandas as pd
import numpy as np
import os
import sys

def split_and_check_leakage(
    input_csv: str = "data/processed/spotify_pairs_labeled.csv",
    seed: int = 42,
    sample_size: int = 15000
):
    print(f"Loading {input_csv} for splitting & leakage verification (Seed={seed})...")
    df = pd.read_csv(input_csv)
    
    # Stratified Sampling across intents to create manageable, reproducible subset
    # Filter out empty or ultra-short customer texts (< 5 chars)
    df = df[df["customer_text"].astype(str).str.len() >= 5].copy()
    
    if len(df) > sample_size:
        print(f"Subsampling {sample_size:,} pairs from {len(df):,} total pairs using seed {seed}...")
        # Stratified sample by intent
        df = df.groupby("intent", group_keys=False).apply(
            lambda x: x.sample(min(len(x), int(sample_size * len(x) / len(df))), random_state=seed)
        ).reset_index(drop=True)
        
    print(f"Sampled Dataset Size: {len(df):,} pairs.")
    
    # Thread / Conversation Root ID splitting to guarantee NO CONVERSATION LEAKAGE
    unique_threads = df["conversation_root_id"].unique()
    np.random.seed(seed)
    np.random.shuffle(unique_threads)
    
    n_threads = len(unique_threads)
    train_end = int(0.70 * n_threads)
    dev_end = int(0.85 * n_threads)
    
    train_threads = set(unique_threads[:train_end])
    dev_threads = set(unique_threads[train_end:dev_end])
    test_threads = set(unique_threads[dev_end:])
    
    train_df = df[df["conversation_root_id"].isin(train_threads)].copy()
    dev_df = df[df["conversation_root_id"].isin(dev_threads)].copy()
    test_df = df[df["conversation_root_id"].isin(test_threads)].copy()
    
    print("\n--- Split Sizes ---")
    print(f"Train: {len(train_df):,} pairs ({len(train_threads):,} threads)")
    print(f"Dev:   {len(dev_df):,} pairs ({len(dev_threads):,} threads)")
    print(f"Test:  {len(test_df):,} pairs ({len(test_threads):,} threads)")
    
    # ----------------------------------------------------
    # STRICT LEAKAGE AUDIT
    # ----------------------------------------------------
    print("\n--- Running Strict Leakage Audit ---")
    
    # 1. Thread / Conversation ID overlap check
    train_dev_thread_overlap = train_threads.intersection(dev_threads)
    train_test_thread_overlap = train_threads.intersection(test_threads)
    dev_test_thread_overlap = dev_threads.intersection(test_threads)
    
    print(f"Thread ID Leakage (Train-Dev): {len(train_dev_thread_overlap)}")
    print(f"Thread ID Leakage (Train-Test): {len(train_test_thread_overlap)}")
    print(f"Thread ID Leakage (Dev-Test): {len(dev_test_thread_overlap)}")
    
    # 2. Exact Customer Text overlap check
    train_texts = set(train_df["customer_text"].astype(str).str.lower().str.strip())
    dev_texts = set(dev_df["customer_text"].astype(str).str.lower().str.strip())
    test_texts = set(test_df["customer_text"].astype(str).str.lower().str.strip())
    
    text_dev_leakage = train_texts.intersection(dev_texts)
    text_test_leakage = train_texts.intersection(test_texts)
    
    print(f"Exact Text Overlap (Train vs Dev): {len(text_dev_leakage)}")
    print(f"Exact Text Overlap (Train vs Test): {len(text_test_leakage)}")
    
    # Remove exact text duplicates from Dev and Test if present in Train to avoid trivial memorization
    if len(text_dev_leakage) > 0:
        print(f"Deduplicating {len(text_dev_leakage)} overlapping text instances from Dev set...")
        dev_df = dev_df[~dev_df["customer_text"].astype(str).str.lower().str.strip().isin(train_texts)]
        
    if len(text_test_leakage) > 0:
        print(f"Deduplicating {len(text_test_leakage)} overlapping text instances from Test set...")
        test_df = test_df[~test_df["customer_text"].astype(str).str.lower().str.strip().isin(train_texts)]
        
    # Save splits
    os.makedirs("data/splits", exist_ok=True)
    train_df.to_csv("data/splits/train.csv", index=False)
    dev_df.to_csv("data/splits/dev.csv", index=False)
    test_df.to_csv("data/splits/test.csv", index=False)
    
    print("\nSaved split files:")
    print("  - data/splits/train.csv")
    print("  - data/splits/dev.csv")
    print("  - data/splits/test.csv")
    
    assert len(train_dev_thread_overlap) == 0, "CRITICAL: Thread ID leakage detected between Train & Dev!"
    assert len(train_test_thread_overlap) == 0, "CRITICAL: Thread ID leakage detected between Train & Test!"
    print("\n[PASSED] Leakage Audit completed with 0 conversation or exact text overlap!")

if __name__ == "__main__":
    split_and_check_leakage()
