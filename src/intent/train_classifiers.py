import pandas as pd
import numpy as np
import pickle
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score, confusion_matrix
from sentence_transformers import SentenceTransformer

def train_and_evaluate_classifiers():
    print("Loading Train, Dev, and Test splits...")
    train_df = pd.read_csv("data/splits/train.csv")
    dev_df = pd.read_csv("data/splits/dev.csv")
    test_df = pd.read_csv("data/splits/test.csv")
    
    X_train_text = train_df["customer_text"].astype(str).values
    y_train = train_df["intent"].values
    
    X_test_text = test_df["customer_text"].astype(str).values
    y_test = test_df["intent"].values
    
    os.makedirs("models", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    metrics_summary = {}
    
    # ----------------------------------------------------
    # BASELINE 1: Majority-Class Classifier (Trivial Baseline)
    # ----------------------------------------------------
    print("\n--- Training Baseline 1: Majority-Class Classifier ---")
    majority_class = train_df["intent"].mode()[0]
    y_pred_b1 = np.full_like(y_test, majority_class)
    
    acc_b1 = accuracy_score(y_test, y_pred_b1)
    macro_f1_b1 = f1_score(y_test, y_pred_b1, average="macro")
    weighted_f1_b1 = f1_score(y_test, y_pred_b1, average="weighted")
    
    print(f"Baseline 1 (Majority) - Test Accuracy: {acc_b1:.4f}, Macro F1: {macro_f1_b1:.4f}, Weighted F1: {weighted_f1_b1:.4f}")
    
    metrics_summary["Baseline_1_Majority"] = {
        "accuracy": round(acc_b1, 4),
        "macro_f1": round(macro_f1_b1, 4),
        "weighted_f1": round(weighted_f1_b1, 4)
    }
    
    # ----------------------------------------------------
    # BASELINE 2: TF-IDF + Logistic Regression (Simple Baseline)
    # ----------------------------------------------------
    print("\n--- Training Baseline 2: TF-IDF + Logistic Regression ---")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train_text)
    X_test_tfidf = vectorizer.transform(X_test_text)
    
    clf_tfidf = LogisticRegression(max_iter=1000, random_state=42)
    clf_tfidf.fit(X_train_tfidf, y_train)
    
    y_pred_b2 = clf_tfidf.predict(X_test_tfidf)
    acc_b2 = accuracy_score(y_test, y_pred_b2)
    macro_f1_b2 = f1_score(y_test, y_pred_b2, average="macro")
    weighted_f1_b2 = f1_score(y_test, y_pred_b2, average="weighted")
    
    print(f"Baseline 2 (TF-IDF + LogReg) - Test Accuracy: {acc_b2:.4f}, Macro F1: {macro_f1_b2:.4f}, Weighted F1: {weighted_f1_b2:.4f}")
    
    metrics_summary["Baseline_2_TFIDF_LogReg"] = {
        "accuracy": round(acc_b2, 4),
        "macro_f1": round(macro_f1_b2, 4),
        "weighted_f1": round(weighted_f1_b2, 4)
    }
    
    # Save Baseline 2 model
    with open("models/tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open("models/tfidf_logreg_model.pkl", "wb") as f:
        pickle.dump(clf_tfidf, f)
        
    # ----------------------------------------------------
    # PROPOSED MODEL: Sentence Transformers Embeddings + Logistic Regression
    # ----------------------------------------------------
    print("\n--- Training Proposed Model: Sentence-Transformers (all-MiniLM-L6-v2) + LogReg ---")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("Encoding Train texts with all-MiniLM-L6-v2...")
    X_train_emb = embedder.encode(X_train_text, show_progress_bar=True, batch_size=64)
    print("Encoding Test texts...")
    X_test_emb = embedder.encode(X_test_text, show_progress_bar=True, batch_size=64)
    
    clf_proposed = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
    clf_proposed.fit(X_train_emb, y_train)
    
    y_pred_proposed = clf_proposed.predict(X_test_emb)
    acc_p = accuracy_score(y_test, y_pred_proposed)
    macro_f1_p = f1_score(y_test, y_pred_proposed, average="macro")
    weighted_f1_p = f1_score(y_test, y_pred_proposed, average="weighted")
    
    print(f"Proposed (Embeddings + LogReg) - Test Accuracy: {acc_p:.4f}, Macro F1: {macro_f1_p:.4f}, Weighted F1: {weighted_f1_p:.4f}")
    
    metrics_summary["Proposed_Semantic_Classifier"] = {
        "accuracy": round(acc_p, 4),
        "macro_f1": round(macro_f1_p, 4),
        "weighted_f1": round(weighted_f1_p, 4)
    }
    
    # Save Proposed Classifier
    with open("models/proposed_intent_classifier.pkl", "wb") as f:
        pickle.dump(clf_proposed, f)
        
    # Save full metrics JSON
    with open("reports/intent_classification_metrics.json", "w") as f:
        json.dump(metrics_summary, f, indent=2)
        
    # Save detailed classification report for proposed model
    report_dict = classification_report(y_test, y_pred_proposed, output_dict=True)
    with open("reports/proposed_classifier_report.json", "w") as f:
        json.dump(report_dict, f, indent=2)
        
    print("\nSaved all model artifacts and reports in models/ and reports/")

if __name__ == "__main__":
    train_and_evaluate_classifiers()
