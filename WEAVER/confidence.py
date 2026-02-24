# weaver/confidence.py
# Simple confidence scoring based on frequency and diversity

def compute_confidence(pattern):
    """
    pattern: dict with keys: count, sources (optional)
    returns confidence score 0.0–1.0
    """
    base = pattern.get("count", 1) / 10.0
    if base > 1.0:
        base = 1.0
    
    # Bonus for multiple sources (if we track them later)
    sources = pattern.get("sources", 1)
    diversity_bonus = min(0.2, (sources - 1) * 0.1)
    
    confidence = base + diversity_bonus
    return min(1.0, confidence)

def confidence_grade(score):
    if score >= 0.9:
        return "HIGH"
    elif score >= 0.7:
        return "MEDIUM"
    elif score >= 0.5:
        return "LOW"
    else:
        return "WARNING"