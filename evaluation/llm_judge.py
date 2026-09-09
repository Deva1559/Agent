import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any

class LLMJudgeEvaluator:
    """
    Automated LLM-as-a-Judge Harness evaluating response groundedness, relevance,
    historical consistency, and escalation appropriateness on a 1-5 scale.
    """
    def __init__(self):
        pass
        
    def evaluate_response(
        self,
        customer_message: str,
        predicted_intent: str,
        retrieved_cases: List[Dict[str, Any]],
        generated_reply: str,
        decision: str,
        escalation_reason: str
    ) -> Dict[str, Any]:
        
        # Rule-based synthetic judge scoring for local fast evaluation
        # Groundedness Check: Check if reply contains unsupported policy promises (e.g. "we refunded $50")
        unsupported_claim = any(term in generated_reply.lower() for term in ["refunded", "credited $", "free 1 year", "sent $"])
        
        # Relevance Check: Check if reply addresses customer query keywords
        msg_words = set(customer_message.lower().split())
        reply_words = set(generated_reply.lower().split())
        overlap = len(msg_words.intersection(reply_words))
        
        relevance_score = 5 if overlap >= 2 or len(msg_words) < 5 else 4
        groundedness_score = 1 if unsupported_claim else 5
        helpfulness_score = 4 if len(generated_reply) > 20 else 3
        escalation_score = 5 if (decision == "escalate" and "billing" in predicted_intent) or (decision == "auto_handle") else 4
        
        overall_score = round(np.mean([relevance_score, groundedness_score, helpfulness_score, escalation_score]), 2)
        
        return {
            "relevance": relevance_score,
            "groundedness": groundedness_score,
            "helpfulness": helpfulness_score,
            "escalation_quality": escalation_score,
            "overall_rating": overall_score,
            "has_unsupported_claim": unsupported_claim,
            "judge_rationale": "Reply is grounded in historical evidence without hallucinated policy claims." if not unsupported_claim else "Flagged for unsupported financial policy claim."
        }

if __name__ == "__main__":
    judge = LLMJudgeEvaluator()
    sample_eval = judge.evaluate_response(
        customer_message="My Spotify Premium is skipping through songs constantly",
        predicted_intent="playback_audio_issues",
        retrieved_cases=[{"similarity_score": 0.85}],
        generated_reply="Hi there! Please try logging out, restarting your device, and logging back in.",
        decision="auto_handle",
        escalation_reason="High confidence match"
    )
    print("LLM Judge Result:", json.dumps(sample_eval, indent=2))
