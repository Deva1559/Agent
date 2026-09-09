import pandas as pd
import numpy as np
import pickle
import json
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class HistoricalRetriever:
    def __init__(self, index_path: str = "models/retrieval_index.pkl"):
        self.index_path = index_path
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.corpus_df = None
        self.corpus_embeddings = None
        
    def build_index(self, train_csv: str = "data/splits/train.csv"):
        print(f"Building Historical Retrieval Index from {train_csv}...")
        self.corpus_df = pd.read_csv(train_csv)
        
        texts = self.corpus_df["customer_text"].astype(str).values
        print(f"Encoding {len(texts):,} historical training cases with all-MiniLM-L6-v2...")
        self.corpus_embeddings = self.embedder.encode(texts, show_progress_bar=True, batch_size=64)
        
        os.makedirs("models", exist_ok=True)
        with open(self.index_path, "wb") as f:
            pickle.dump({
                "df": self.corpus_df,
                "embeddings": self.corpus_embeddings
            }, f)
        print(f"Saved retrieval index to {self.index_path}")
        
    def load_index(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index file {self.index_path} not found. Run build_index first.")
        with open(self.index_path, "rb") as f:
            data = pickle.load(f)
            self.corpus_df = data["df"]
            self.corpus_embeddings = data["embeddings"]
            
    def retrieve(self, query_text: str, k: int = 5, filter_intent: str = None):
        if self.corpus_embeddings is None:
            self.load_index()
            
        query_emb = self.embedder.encode([query_text])
        similarities = cosine_similarity(query_emb, self.corpus_embeddings)[0]
        
        if filter_intent and filter_intent != "general_inquiry_other":
            # Filter candidates by predicted intent to boost precision
            intent_mask = (self.corpus_df["intent"] == filter_intent).values
            similarities = np.where(intent_mask, similarities, similarities * 0.5)
            
        top_k_indices = np.argsort(similarities)[::-1][:k]
        
        results = []
        for idx in top_k_indices:
            row = self.corpus_df.iloc[idx]
            results.append({
                "historical_customer_text": str(row["customer_text"]),
                "historical_brand_reply": str(row["brand_text"]),
                "intent": str(row["intent"]),
                "similarity_score": round(float(similarities[idx]), 4),
                "conversation_root_id": str(row["conversation_root_id"])
            })
            
        return results

if __name__ == "__main__":
    retriever = HistoricalRetriever()
    retriever.build_index("data/splits/train.csv")
    
    # Quick test query
    sample_query = "Spotify Premium is skipping songs constantly on my bluetooth speaker"
    matches = retriever.retrieve(sample_query, k=3)
    print("\n--- Test Query Matches ---")
    print("Query:", sample_query)
    for i, m in enumerate(matches, 1):
        print(f"\nMatch {i} (Similarity: {m['similarity_score']}):")
        print("  Cust:", m["historical_customer_text"])
        print("  Brand:", m["historical_brand_reply"])
