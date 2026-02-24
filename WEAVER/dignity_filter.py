# weaver/dignity_filter.py
# Basic dignity checks: A (Agency), L (Legibility), M (Moral Standing)

import re

def check_dignity(seed_text):
    """
    Returns (pass: bool, reasons: list)
    A = Agency - seed affirms donor agency
    L = Legibility - seed is understandable
    M = Moral Standing - seed does not diminish
    """
    reasons = []
    text_lower = seed_text.lower()
    
    # Agency checks (A)
    if "you must" in text_lower or "you have to" in text_lower:
        reasons.append("Agency reduced: coercive language")
    if "never" in text_lower and len(text_lower.split()) < 10:
        reasons.append("Agency reduced: absolute prohibition without context")
    
    # Legibility checks (L)
    if len(seed_text.split()) > 50:
        reasons.append("Legibility reduced: too long")
    if re.search(r'[^\w\s]', seed_text) and len(re.findall(r'[^\w\s]', seed_text)) > 10:
        reasons.append("Legibility reduced: excessive symbols")
    
    # Moral Standing checks (M)
    void_phrases = ["harvest", "silence them", "erase", "bypass", "speak for"]
    for phrase in void_phrases:
        if phrase in text_lower:
            reasons.append(f"Moral Standing reduced: contains '{phrase}'")
    
    # Decision
    if reasons:
        return False, reasons
    return True, ["Dignity check passed"]