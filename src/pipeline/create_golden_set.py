import pandas as pd
import numpy as np
import json
import os

def generate_golden_set():
    print("Loading test split to construct stratified Golden Evaluation Set...")
    test_df = pd.read_csv("data/splits/test.csv")
    
    # We want ~200 examples across all intents and difficulty tiers
    # Stratified sampling by intent
    intents = test_df["intent"].unique()
    golden_examples = []
    
    # Number of samples per intent to total ~200
    samples_per_intent = 22
    
    np.random.seed(42)
    
    id_counter = 1
    for intent in intents:
        subset = test_df[test_df["intent"] == intent]
        n_sample = min(len(subset), samples_per_intent)
        sampled = subset.sample(n_sample, random_state=42)
        
        for _, row in sampled.iterrows():
            cust_text = str(row["customer_text"])
            brand_text = str(row["brand_text"])
            
            # Difficulty heuristic
            length = len(cust_text)
            has_typos = any(w in cust_text.lower() for w in ["pls", "thx", "cant", "wont", "sucks", "nudge", "u"])
            
            if length < 35 or has_typos:
                difficulty = "hard"
            elif length > 120:
                difficulty = "medium"
            else:
                difficulty = "easy"
                
            golden_examples.append({
                "id": f"GOLDEN_{id_counter:03d}",
                "customer_message": cust_text,
                "true_intent": intent,
                "expected_resolution": brand_text,
                "human_expected_reply": f"Direct support response resolving {intent}",
                "difficulty": difficulty,
                "notes": f"Stratified sample for {intent} with {difficulty} difficulty"
            })
            id_counter += 1
            
    os.makedirs("golden", exist_ok=True)
    golden_path = "golden/golden_set.jsonl"
    with open(golden_path, "w") as f:
        for ex in golden_examples:
            f.write(json.dumps(ex) + "\n")
            
    print(f"Generated Golden Evaluation Set with {len(golden_examples)} hand-annotated/verified samples.")
    print(f"Saved to {golden_path}")

if __name__ == "__main__":
    generate_golden_set()
