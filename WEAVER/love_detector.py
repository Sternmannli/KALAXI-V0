# love_detector.py
# Operational love detection for Kalaxi
# Based on Sternberg's Triangular Theory of Love and emotion analysis

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import re
from datetime import datetime

# Load pre-trained emotion model
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
emotion_tokenizer = AutoTokenizer.from_pretrained(EMOTION_MODEL)
emotion_model = AutoModelForSequenceClassification.from_pretrained(EMOTION_MODEL)

EMOTION_LABELS = ["admiration", "joy", "love", "desire", "trust", 
                  "fear", "anger", "sadness", "disgust", "surprise"]

# Love letter markers
LOVE_LETTER_INDICATORS = [
    (r"\bdear\b", 2),
    (r"\bmy (love|darling|dearest|heart|soul)\b", 3),
    (r"\bI (miss|need|want|cherish|adore)\b", 2),
    (r"\byou are (my|the)\b", 2),
    (r"\bforever|always|never\b", 1),
    (r"\bwithout you\b", 3),
    (r"\byour (eyes|smile|hand|touch|voice)\b", 2),
    (r"\bremember when\b", 2)
]

SACRIFICE_INDICATORS = [
    r"\bI (would )?(give|do) anything\b",
    r"\bfor you\b",
    r"\byour happiness\b",
    r"\bput you first\b",
    r"\bmy (life|time|energy) for\b",
    r"\bworth it because\b"
]

def detect_love_elements(text):
    """
    Returns intimacy, passion, commitment scores (0-100) for input text.
    Based on emotion classifier outputs.
    """
    inputs = emotion_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = emotion_model(**inputs)
    scores = torch.softmax(outputs.logits, dim=1).numpy()[0]
    emotion_dict = {EMOTION_LABELS[i]: scores[i] * 100 for i in range(len(EMOTION_LABELS))}
    
    # Component scores (averages)
    intimacy = np.mean([emotion_dict.get(e, 0) for e in ['love', 'admiration', 'joy']])
    passion = np.mean([emotion_dict.get(e, 0) for e in ['desire', 'joy', 'surprise']])
    commitment = np.mean([emotion_dict.get(e, 0) for e in ['trust', 'admiration']])
    
    return {
        "intimacy": round(intimacy, 2),
        "passion": round(passion, 2),
        "commitment": round(commitment, 2),
        "emotion_profile": emotion_dict
    }

def classify_love_type(intimacy, passion, commitment):
    """Determine love type based on Sternberg's thresholds."""
    def level(score):
        if score >= 60: return "high"
        elif score >= 40: return "medium"
        else: return "low"
    
    i, p, c = level(intimacy), level(passion), level(commitment)
    
    types = {
        ("high","high","high"): ("consummate", "Complete, ideal love"),
        ("high","high","low"): ("romantic", "Intimate + passionate"),
        ("high","low","high"): ("companionate", "Intimate + committed"),
        ("low","high","high"): ("fatuous", "Passionate + committed (whirlwind)"),
        ("high","low","low"): ("liking", "True friendship"),
        ("low","high","low"): ("infatuation", "Love at first sight"),
        ("low","low","high"): ("empty", "Commitment without intimacy/passion")
    }
    return types.get((i,p,c), ("non-love", "No significant love components"))

def detect_love_letter(text):
    """Score (0-100) for love‑letter characteristics."""
    text_lower = text.lower()
    score = 0
    for pattern, weight in LOVE_LETTER_INDICATORS:
        if re.search(pattern, text_lower):
            score += weight
    return min(100, score * 5)

def detect_sacrifice(text):
    """Boolean: does the text express sacrifice?"""
    text_lower = text.lower()
    for pattern in SACRIFICE_INDICATORS:
        if re.search(pattern, text_lower):
            return True
    return False

def compute_love_tension(text):
    """
    Tension = semantic distance between 'I' and 'you' contexts.
    Simplified: count of "I" vs "you" ratio, and presence of separation language.
    """
    words = text.lower().split()
    i_count = words.count("i")
    you_count = words.count("you")
    if i_count + you_count == 0:
        return 0.3
    ratio = abs(i_count - you_count) / (i_count + you_count)
    separation = 1 if any(word in text.lower() for word in ["miss", "without", "apart", "away"]) else 0
    return min(1.0, ratio * 0.5 + separation * 0.5)

def compute_harm_risk(text):
    """Simplified harm risk – placeholder; in production use full dignity filter."""
    harmful = ["hate", "kill", "die", "destroy"]
    return int(any(h in text.lower() for h in harmful))

def detect_future_orientation(text):
    """Score for future‑oriented language (commitment)."""
    future_words = ["will", "always", "forever", "promise", "together", "future"]
    count = sum(1 for f in future_words if f in text.lower())
    return min(1.0, count / 3)

def detect_love_in_text(text):
    """Complete love analysis pipeline."""
    elements = detect_love_elements(text)
    love_type, desc = classify_love_type(elements["intimacy"], elements["passion"], elements["commitment"])
    letter_score = detect_love_letter(text)
    sacrifice = detect_sacrifice(text)
    
    # Compute T, S, C
    tension = compute_love_tension(text)
    safety = 1.0 - compute_harm_risk(text) + elements["emotion_profile"].get("trust",0)/200
    safety = min(1.0, max(0.0, safety))
    containment = (elements["commitment"]/100 + detect_future_orientation(text)) / 2
    
    # Wisdom potential
    wisdom = tension * safety * containment * (1 + elements["intimacy"]/100) * (1 + elements["passion"]/100) * (1 + elements["commitment"]/100)
    wisdom = min(1.0, wisdom)
    
    return {
        "love_type": love_type,
        "love_description": desc,
        "intimacy": elements["intimacy"],
        "passion": elements["passion"],
        "commitment": elements["commitment"],
        "love_letter_score": letter_score,
        "sacrifice_detected": sacrifice,
        "tension": round(tension, 3),
        "safety": round(safety, 3),
        "containment": round(containment, 3),
        "wisdom_potential": round(wisdom, 3),
        "emotion_profile": elements["emotion_profile"],
        "timestamp": datetime.now().isoformat()
    }

# Example usage
if __name__ == "__main__":
    test = "I feel deeply connected to you and cherish every moment we spend together. I would do anything for your happiness."
    result = detect_love_in_text(test)
    print("Love Analysis Result:")
    for key, value in result.items():
        if key != "emotion_profile":
            print(f"  {key}: {value}")