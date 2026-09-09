import pandas as pd
import numpy as np
import pickle
import json
import os
import re
from typing import Dict, List, Any
from src.retrieval.retrieve_history import HistoricalRetriever

class EscalationPolicy:
    def __init__(
        self,
        min_confidence_threshold: float = 0.65,
        min_retrieval_similarity: float = 0.55,
        high_risk_intents: List[str] = None
    ):
        self.min_confidence_threshold = min_confidence_threshold
        self.min_retrieval_similarity = min_retrieval_similarity
        self.high_risk_intents = high_risk_intents or [
            "account_access_security",
            "billing_subscription_payment"
        ]
        
    def evaluate(
        self,
        customer_message: str,
        predicted_intent: str,
        confidence: float,
        retrieved_cases: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        
        reasons = []
        should_escalate = False
        
        # Signal 1: Low intent classifier confidence
        if confidence < self.min_confidence_threshold:
            should_escalate = True
            reasons.append(f"Low intent confidence score ({confidence:.2f} < threshold {self.min_confidence_threshold:.2f})")
            
        # Signal 2: Retrieval similarity weak
        top_similarity = retrieved_cases[0]["similarity_score"] if retrieved_cases else 0.0
        if top_similarity < self.min_retrieval_similarity:
            should_escalate = True
            reasons.append(f"Weak historical evidence match (top similarity {top_similarity:.2f} < threshold {self.min_retrieval_similarity:.2f})")
            
        # Signal 3: High-risk account/billing security category
        if predicted_intent in self.high_risk_intents:
            # Requires higher confidence and strong similarity to auto-handle
            if confidence < 0.85 or top_similarity < 0.70:
                should_escalate = True
                reasons.append(f"High-risk intent '{predicted_intent}' requires explicit human verification for security/billing safety.")
                
        # Signal 4: Noisy / conflicting evidence across top K
        if len(retrieved_cases) >= 3:
            intent_distribution = [c["intent"] for c in retrieved_cases[:3]]
            unique_intents = set(intent_distribution)
            if len(unique_intents) > 2:
                should_escalate = True
                reasons.append("Conflicting historical resolutions retrieved across top matching cases.")
                
        if should_escalate:
            return {
                "decision": "escalate",
                "escalation_reason": " | ".join(reasons),
                "auto_handle_eligible": False
            }
        else:
            return {
                "decision": "auto_handle",
                "escalation_reason": "High confidence classification with consistent, strong historical resolution evidence.",
                "auto_handle_eligible": True
            }

class GroundedResponseGenerator:
    def __init__(self):
        # Deterministic grounded templates conditioned strictly on historical brand resolution evidence
        self.templates = {
            "playback_audio_issues": "Hi there! Help's here. Could you try logging out, restarting your device, and logging back in? Also, let us know what OS version and device you're on so we can assist further.",
            "app_crash_technical": "Hey! We're sorry to hear about the app crashing. Could you let us know your exact device model, operating system, and Spotify version? A quick clean reinstall often helps sort this out.",
            "billing_subscription_payment": "Hi there! For billing and subscription inquiries, please send us a Direct Message with your registered account email address or username so our backstage team can safely check your account.",
            "student_family_discount": "Hey! For student verification issues, we recommend checking your status via UNiDAYS at unidays.com. For family plans, ensure all members reside at the exact same physical home address.",
            "account_access_security": "Hi! We take account security very seriously. Please request a password reset at spotify.com/reset or send us a DM with your username so our security team can assist you directly.",
            "offline_local_files": "Hey! If your offline downloads or local files are missing, verify that your device is connected to the same Wi-Fi network as your desktop and check your download storage settings.",
            "content_metadata_playlists": "Thanks for reporting this content issue! Could you send us the direct track or artist link? We'll pass it along directly to our content and curation teams.",
            "feedback_feature_request": "Thanks for sharing your feedback with us! We really appreciate your input and will make sure to pass your thoughts to our product development team.",
            "general_inquiry_other": "Hi there! Thanks for reaching out. Could you share a few more details about your issue or send us a DM with your account info so we can lend a hand?"
        }
        
    def generate_reply(self, customer_message: str, predicted_intent: str, retrieved_cases: List[Dict[str, Any]]) -> str:
        # Check if top historical case has direct actionable advice
        if retrieved_cases and retrieved_cases[0]["similarity_score"] >= 0.80:
            hist_reply = retrieved_cases[0]["historical_brand_reply"]
            # Sanitize mentions (@username -> Hi there)
            hist_reply_clean = re.sub(r'^@\w+\s*', 'Hi there! ', hist_reply)
            return hist_reply_clean
            
        return self.templates.get(predicted_intent, self.templates["general_inquiry_other"])

if __name__ == "__main__":
    policy = EscalationPolicy()
    generator = GroundedResponseGenerator()
    
    test_cases = [
        ("Spotify Premium skipping through songs constantly on android tablet & bluetooth speaker", "playback_audio_issues", 0.92, [{"similarity_score": 0.85, "intent": "playback_audio_issues", "historical_brand_reply": "@user Try logging out and restarting."}]),
        ("My account was hacked and charged $100", "billing_subscription_payment", 0.60, [{"similarity_score": 0.50, "intent": "billing_subscription_payment", "historical_brand_reply": "@user Please DM us."}])
    ]
    
    print("--- Escalation Policy & Grounded Generation Test ---")
    for msg, intent, conf, history in test_cases:
        esc_result = policy.evaluate(msg, intent, conf, history)
        reply = generator.generate_reply(msg, intent, history)
        print(f"\nMsg: '{msg}'")
        print(f"Intent: {intent} (Conf: {conf})")
        print(f"Decision: {esc_result['decision'].upper()}")
        print(f"Reason: {esc_result['escalation_reason']}")
        print(f"Draft Reply: {reply}")
