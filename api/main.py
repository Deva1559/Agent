from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
import pickle
import numpy as np
import os
import sys

from src.retrieval.retrieve_history import HistoricalRetriever
from src.escalation.escalation_engine import EscalationPolicy, GroundedResponseGenerator
from sentence_transformers import SentenceTransformer

# Global model state
models = {}

def load_artifacts():
    if "embedder" in models:
        return
    print("Loading models and vector index into memory...")
    models["embedder"] = SentenceTransformer("all-MiniLM-L6-v2")
    
    with open("models/proposed_intent_classifier.pkl", "rb") as f:
        models["classifier"] = pickle.load(f)
        
    retriever = HistoricalRetriever()
    retriever.load_index()
    models["retriever"] = retriever
    
    models["policy"] = EscalationPolicy()
    models["generator"] = GroundedResponseGenerator()
    print("All models loaded successfully!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_artifacts()
    yield
    models.clear()

app = FastAPI(
    title="Hiver AI Support Agent API",
    description="Production-grade AI Support Agent for SpotifyCares with Intent Classification, Historical Retrieval (RAG), and Multi-Signal Escalation.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    message: str

class QueryResponse(BaseModel):
    intent: str
    confidence: float
    reply: str
    decision: str
    escalation_reason: str
    retrieved_cases: List[Dict[str, Any]]

@app.get("/")
def serve_demo():
    if os.path.exists("demo/index.html"):
        return FileResponse("demo/index.html")
    return {"message": "Demo UI file not found. Visit /docs for OpenAPI swagger interface."}

@app.get("/health")
def health_check():
    if "embedder" not in models:
        load_artifacts()
    return {
        "status": "healthy",
        "models_loaded": "classifier" in models and "retriever" in models
    }

@app.post("/predict", response_model=QueryResponse)
def predict_support_ticket(req: QueryRequest):
    if "embedder" not in models:
        load_artifacts()
    if not req.message or len(req.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
    msg = req.message.strip()
    
    # 1. Embed query & classify intent
    query_emb = models["embedder"].encode([msg])
    pred_intent = models["classifier"].predict(query_emb)[0]
    probs = models["classifier"].predict_proba(query_emb)[0]
    confidence = float(np.max(probs))
    
    # 2. Historical Retrieval
    retrieved_cases = models["retriever"].retrieve(msg, k=3, filter_intent=pred_intent)
    
    # 3. Escalation Decision & Reply Generation
    esc_result = models["policy"].evaluate(msg, pred_intent, confidence, retrieved_cases)
    reply = models["generator"].generate_reply(msg, pred_intent, retrieved_cases)
    
    return QueryResponse(
        intent=pred_intent,
        confidence=round(confidence, 4),
        reply=reply,
        decision=esc_result["decision"],
        escalation_reason=esc_result["escalation_reason"],
        retrieved_cases=retrieved_cases
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
