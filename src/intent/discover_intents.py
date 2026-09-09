import pandas as pd
import json
import re
from collections import Counter
import os

# Define Spotify Customer Support Intent Taxonomy derived from high-frequency keyword & semantic patterns
INTENT_TAXONOMY = {
    "playback_audio_issues": {
        "definition": "Customer experiences song skipping, playback stopping/freezing midway, audio distortion, or silence.",
        "keywords": ["skip", "skipping", "stop", "stopping", "pause", "play", "playing", "freeze", "freezing", "cut out", "audio", "sound", "volume", "buffering"],
        "positive_examples": [
            "Spotify Premium skipping through songs constantly on android tablet & bluetooth speaker.",
            "songs have been stopping midway through and won't restart unless i close and reopen app"
        ],
        "confusable": ["app_crash_technical"],
        "resolution_pattern": "Recommend log out -> restart device -> log back in; clean reinstall; check bluetooth/audio output."
    },
    "app_crash_technical": {
        "definition": "App crashes to home screen, fails to launch, or shows blank/black screen on device startup.",
        "keywords": ["crash", "crashes", "crashing", "black screen", "blank screen", "won't open", "wont open", "launch", "error code"],
        "positive_examples": [
            "My app keeps crashing every time I open a playlist on iOS 11.",
            "Spotify won't launch on Windows 10 after latest update"
        ],
        "confusable": ["playback_audio_issues", "offline_local_files"],
        "resolution_pattern": "Request device OS and Spotify version; provide clean reinstall steps."
    },
    "billing_subscription_payment": {
        "definition": "Issues regarding double charges, payment failures, subscription status, payment methods, or currency issues.",
        "keywords": ["charged", "charge", "billing", "payment", "card", "money", "receipt", "invoice", "bank", "pay", "double charge", "renew"],
        "positive_examples": [
            "I got charged twice for my premium subscription this month.",
            "My payment failed but my bank says money was deducted."
        ],
        "confusable": ["student_family_discount"],
        "resolution_pattern": "Direct user to account page or request DM with registered email/username for backstage account lookup."
    },
    "student_family_discount": {
        "definition": "Queries or issues verifying UNiDAYS student discount, NUS card, or managing Family Plan members/addresses.",
        "keywords": ["student", "unidays", "nus", "discount", "family", "family plan", "address", "verification", "verify"],
        "positive_examples": [
            "I'm having trouble using a nus card for discount please help",
            "Can't invite my sister to my family plan, says address doesn't match"
        ],
        "confusable": ["billing_subscription_payment"],
        "resolution_pattern": "Advise using UNiDAYS link for verification or check family plan owner address matching."
    },
    "account_access_security": {
        "definition": "Inability to log in, forgotten password, unauthorized account access, or account playing on stranger's device.",
        "keywords": ["login", "log in", "password", "hacked", "account", "logged out", "username", "email", "someone else", "stranger"],
        "positive_examples": [
            "Anyone else having issues with their account playing on someone else's device?",
            "Can't log into my account, email not recognized"
        ],
        "confusable": ["billing_subscription_payment"],
        "resolution_pattern": "Advise password reset link; check connected devices; request DM with account details for security review."
    },
    "offline_local_files": {
        "definition": "Downloaded songs disappearing, offline mode not working, or local file sync from desktop to mobile failing.",
        "keywords": ["offline", "download", "downloaded", "downloads", "local files", "greyed out", "grayed out", "sd card"],
        "positive_examples": [
            "All my offline downloaded songs vanished after updating app.",
            "Local files from my PC are greyed out on my phone."
        ],
        "confusable": ["playback_audio_issues"],
        "resolution_pattern": "Verify same Wi-Fi network for local sync; check download limit / storage location settings."
    },
    "content_metadata_playlists": {
        "definition": "Missing songs/albums, wrong artist page tagging, metadata errors, or playlist feedback.",
        "keywords": ["missing song", "wrong artist", "album", "playlist", "shuffle", "artist", "track", "lyrics", "cover art"],
        "positive_examples": [
            "Has anyone else noticed that #iKON has a song under their Spotify profile that isn't theirs?",
            "Why is Taylor Swift's old album missing in my region?"
        ],
        "confusable": ["feedback_feature_request"],
        "resolution_pattern": "Request track/artist links; pass details to content/curation team."
    },
    "feedback_feature_request": {
        "definition": "General praise, complaint about UI redesign/shuffle algorithm, or feature requests.",
        "keywords": ["update", "redesign", "ui", "sucks", "feature", "bring back", "love", "hate", "disappointed", "feedback"],
        "positive_examples": [
            "Idk why but Spotify shuffle algorithm sucks ass",
            "Disappointed there was no #Seal on TBT animal playlist"
        ],
        "confusable": ["content_metadata_playlists"],
        "resolution_pattern": "Acknowledge feedback with thank-you; share Community ideas link or pass to product team."
    }
}

def classify_intent_heuristic(text: str) -> str:
    text_lower = text.lower()
    
    # Priority-based keyword matching for discovery labeling
    scores = {}
    for intent, info in INTENT_TAXONOMY.items():
        score = sum(1 for kw in info["keywords"] if kw in text_lower)
        if score > 0:
            scores[intent] = score
            
    if not scores:
        return "general_inquiry_other"
        
    # Return intent with max matched keywords
    return max(scores, key=scores.get)

def label_spotify_intents(input_csv: str = "data/processed/spotify_pairs.csv"):
    print(f"Assigning initial intent taxonomy to {input_csv}...")
    df = pd.read_csv(input_csv)
    
    df["intent"] = df["customer_text"].astype(str).apply(classify_intent_heuristic)
    
    intent_counts = df["intent"].value_counts().to_dict()
    print("Intent Distribution:")
    for k, v in intent_counts.items():
        print(f"  - {k}: {v:,} ({v/len(df)*100:.2f}%)")
        
    output_path = "data/processed/spotify_pairs_labeled.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved labeled dataset to {output_path}")
    
    # Save taxonomy json for reference
    os.makedirs("configs", exist_ok=True)
    with open("configs/intent_taxonomy.json", "w") as f:
        json.dump(INTENT_TAXONOMY, f, indent=2)
    print("Saved configs/intent_taxonomy.json")

if __name__ == "__main__":
    label_spotify_intents()
