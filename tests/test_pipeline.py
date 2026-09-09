import pytest
import pandas as pd
import numpy as np
import os
import json
from src.retrieval.retrieve_history import HistoricalRetriever
from src.escalation.escalation_engine import EscalationPolicy, GroundedResponseGenerator
from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_data_cleaning_and_splits():
    assert os.path.exists("data/splits/train.csv")
    assert os.path.exists("data/splits/dev.csv")
    assert os.path.exists("data/splits/test.csv")
    
    train_df = pd.read_csv("data/splits/train.csv")
    assert len(train_df) > 0
    assert "customer_text" in train_df.columns
    assert "intent" in train_df.columns

def test_retrieval_module():
    retriever = HistoricalRetriever()
    retriever.load_index()
    results = retriever.retrieve("Spotify Premium skipping songs", k=3)
    assert len(results) == 3
    assert "similarity_score" in results[0]

def test_escalation_policy():
    policy = EscalationPolicy(min_confidence_threshold=0.70)
    
    # High confidence case
    res1 = policy.evaluate("skipping songs", "playback_audio_issues", 0.95, [{"similarity_score": 0.85}])
    assert res1["decision"] == "auto_handle"
    
    # Low confidence case
    res2 = policy.evaluate("account hacked", "billing_subscription_payment", 0.50, [{"similarity_score": 0.40}])
    assert res2["decision"] == "escalate"
    assert "Low intent confidence score" in res2["escalation_reason"]

def test_api_endpoints():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
    predict_res = client.post("/predict", json={"message": "My Spotify Premium is skipping through songs"})
    assert predict_res.status_code == 200
    data = predict_res.json()
    assert "intent" in data
    assert "decision" in data
    assert "reply" in data

def test_empty_message_validation():
    response = client.post("/predict", json={"message": "   "})
    assert response.status_code == 400
