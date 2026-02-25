# unified_pillar_detector.py
# Combines all five pillar detectors into a single unified analysis
# To be called by the main Weaver on each donor input

import json
from datetime import datetime

# Import the individual detectors (assumed to be in same directory)
from humour_detector import detect_humour_in_text
from absurdity_detector import detect_absurdity_in_text
from obsession_detector import detect_obsession_in_text
from love_detector import detect_love_in_text
from proverb_compressor import generate_proverb_from_cluster  # we'll use a stub for single‑text; real compression needs clusters

# Pillar weights for wisdom potential (used in thermal delay)
PILLAR_BASE_WEIGHTS = {
    "proverb": 1.0,
    "humour": 0.7,
    "absurdity": 0.9,
    "obsession": 0.8,
    "love": 0.8
}

# Thermal delay base (days) per pillar
PILLAR_BASE_DELAY = {
    "proverb": 7,
    "humour": 3,
    "absurdity": 90,      # held in absurdity queue, indefinite
    "obsession": 14,
    "love": 10
}

def detect_pillars(text, context=None):
    """
    Run all five pillar detectors and return a unified profile.
    """
    profile = {
        "timestamp": datetime.now().isoformat(),
        "text_snippet": text[:200],
        "pillars": {},
        "multi_pillar": False,
        "dominant_pillar": None,
        "wisdom_potential": 0.0,
        "recommended_delay": 7,
        "absurdity_queue": False,
        "metadata": {}
    }
    
    # Love
    love_result = detect_love_in_text(text)
    profile["pillars"]["love"] = {
        "present": love_result["love_type"] != "non-love",
        "score": love_result.get("wisdom_potential", 0),
        "type": love_result["love_type"],
        "details": {
            "intimacy": love_result["intimacy"],
            "passion": love_result["passion"],
            "commitment": love_result["commitment"]
        }
    }
    
    # Humour
    humour_result = detect_humour_in_text(text)
    profile["pillars"]["humour"] = {
        "present": humour_result.get("is_humour", False),
        "score": humour_result.get("wisdom_potential", 0),
        "type": humour_result.get("humour_type"),
        "bv_score": humour_result.get("bv_score", 0),
        "details": {k: humour_result.get(k) for k in ["tension","safety","surprisal"] if k in humour_result}
    }
    
    # Absurdity
    absurd_result = detect_absurdity_in_text(text)
    profile["pillars"]["absurdity"] = {
        "present": absurd_result.get("is_absurd", False),
        "score": absurd_result.get("wisdom_potential", 0),
        "type": absurd_result.get("absurdity_type"),
        "details": absurd_result.get("metadata", {})
    }
    if absurd_result.get("is_absurd", False):
        profile["absurdity_queue"] = True
    
    # Obsession
    obs_result = detect_obsession_in_text(text)
    profile["pillars"]["obsession"] = {
        "present": obs_result.get("is_obsessive", False),
        "score": obs_result.get("wisdom_potential", 0),
        "type": obs_result.get("obsession_type"),
        "details": obs_result.get("metadata", {})
    }
    
    # Proverb candidate – simplified: if text is structurally proverb‑like (e.g., short, metaphorical)
    # In production, you'd run the compressor on a cluster, not a single text.
    # Here we just assign a heuristic score.
    words = text.split()
    proverb_score = 0.0
    if 4 <= len(words) <= 20 and "is" in text.lower():
        proverb_score = 0.6  # weak signal
    profile["pillars"]["proverb"] = {
        "present": proverb_score > 0.5,
        "score": proverb_score,
        "type": "candidate",
        "details": {}
    }
    
    # Count active pillars
    active = [p for p, data in profile["pillars"].items() if data["present"]]
    profile["multi_pillar"] = len(active) > 1
    if active:
        # Dominant pillar is the one with highest score
        profile["dominant_pillar"] = max(active, key=lambda p: profile["pillars"][p]["score"])
    
    # Calculate combined wisdom potential (weighted sum of active pillar scores)
    total = 0.0
    weight_sum = 0.0
    for p in active:
        w = PILLAR_BASE_WEIGHTS.get(p, 1.0)
        total += profile["pillars"][p]["score"] * w
        weight_sum += w
    profile["wisdom_potential"] = round(total / weight_sum if weight_sum else 0, 3)
    
    # Determine recommended thermal delay
    if profile["absurdity_queue"]:
        profile["recommended_delay"] = "indefinite (absurdity queue)"
    else:
        base = PILLAR_BASE_DELAY.get(profile["dominant_pillar"], 7)
        if profile["multi_pillar"]:
            base = int(base * 1.5)
        if profile["wisdom_potential"] > 0.8:
            base = int(base * 1.3)
        profile["recommended_delay"] = max(3, base)
    
    profile["metadata"]["active_pillars"] = active
    return profile

def generate_seed_from_pillars(profile, donor_id=None):
    """
    Generate a provisional seed for THRESHOLD.md based on the pillar profile.
    """
    lines = []
    lines.append(f"[{datetime.now().strftime('%Y-%m-%d')}] -- seed -- [AUTO-DETECTED]")
    for p, data in profile["pillars"].items():
        if data["present"]:
            lines.append(f"   {p.upper()}: {data['type']} (score: {data['score']})")
    lines.append(f"   wisdom potential: {profile['wisdom_potential']}")
    lines.append(f"   recommended delay: {profile['recommended_delay']} days")
    if donor_id:
        lines.append(f"   donor: {donor_id}")
    lines.append("")
    return "\n".join(lines)

# Example usage
if __name__ == "__main__":
    test_text = "I keep thinking about whether I locked the door. I must check it again."
    profile = detect_pillars(test_text)
    print("Unified Pillar Profile:")
    print(json.dumps(profile, indent=2))
    print("\nSeed preview:")
    print(generate_seed_from_pillars(profile))