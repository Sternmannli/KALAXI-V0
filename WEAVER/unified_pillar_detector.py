# unified_pillar_detector.py
# Combines all five pillar detectors into a single unified analysis
# To be called by the main Weaver on each donor input

import json
from datetime import datetime

# Import the individual detectors (WEAVER package)
# These detectors require heavy ML dependencies (torch, transformers, sentence-transformers).
# When those deps are unavailable, we use lightweight regex-based fallbacks that provide
# basic detection rather than returning silent neutrals.
import re

# ── Lightweight regex-based pillar detection (no ML dependencies) ──

def _lightweight_humour(text):
    """Regex-based humour detection: irony markers, laughter, self-deprecation."""
    text_lower = text.lower()
    signals = 0
    # Laughter and amusement
    if re.search(r'\b(haha|lol|lmao|rofl|😂|😄|🤣)\b', text_lower):
        signals += 2
    # Irony markers
    if re.search(r'\b(ironi[c]|sarcas[mt]|kidding|joking|tongue.in.cheek)\b', text_lower):
        signals += 2
    # Self-deprecation
    if re.search(r'\b(i.m (such|so|really) (bad|stupid|terrible|hopeless))\b', text_lower):
        signals += 1
    # Absurd juxtaposition (very short + very long sentence in same text)
    if re.search(r'[!?]{2,}', text):
        signals += 1
    is_humour = signals >= 2
    return {
        "is_humour": is_humour,
        "humour_type": "regex-detected" if is_humour else "none",
        "wisdom_potential": min(signals * 0.2, 0.8) if is_humour else 0,
        "bv_score": min(signals * 0.15, 0.6),
        "detection_method": "lightweight_regex",
    }

def _lightweight_absurdity(text):
    """Regex-based absurdity detection: contradictions, impossible claims."""
    text_lower = text.lower()
    signals = 0
    # Contradictions
    if re.search(r'\b(but also|yet somehow|impossible.{0,20}(but|yet|still))\b', text_lower):
        signals += 2
    # Paradox markers
    if re.search(r'\b(paradox|absurd|nonsense|kafka|catch.22|ouroboros)\b', text_lower):
        signals += 2
    # Impossible claims
    if re.search(r'\b(always never|never always|everything nothing|infinite.{0,10}zero)\b', text_lower):
        signals += 2
    is_absurd = signals >= 2
    return {
        "is_absurd": is_absurd,
        "absurdity_type": "regex-detected" if is_absurd else "none",
        "wisdom_potential": min(signals * 0.25, 0.9) if is_absurd else 0,
        "metadata": {"detection_method": "lightweight_regex", "signals": signals},
    }

def _lightweight_obsession(text):
    """Regex-based obsession detection: repetition, fixation markers."""
    text_lower = text.lower()
    # Word repetition (same word 3+ times)
    words = re.findall(r'\b\w{4,}\b', text_lower)
    word_counts = {}
    for w in words:
        word_counts[w] = word_counts.get(w, 0) + 1
    repeated = {w: c for w, c in word_counts.items() if c >= 3}
    signals = len(repeated)
    # Fixation markers
    if re.search(r'\b(always|every time|can.t stop|obsess|fixat|haunt|recurring|again and again)\b', text_lower):
        signals += 1
    is_obsessive = signals >= 2
    return {
        "is_obsessive": is_obsessive,
        "obsession_type": "regex-detected" if is_obsessive else "none",
        "wisdom_potential": min(signals * 0.2, 0.8) if is_obsessive else 0,
        "metadata": {"detection_method": "lightweight_regex", "repeated_words": list(repeated.keys())[:5]},
    }

def _lightweight_love(text):
    """Regex-based love detection: intimacy, passion, commitment markers."""
    text_lower = text.lower()
    intimacy = len(re.findall(r'\b(love|dear|close|hold|embrace|tender|gentle|warm|care|cherish)\b', text_lower))
    passion = len(re.findall(r'\b(desire|yearn|miss|ache|burn|fire|heart|soul|dream)\b', text_lower))
    commitment = len(re.findall(r'\b(forever|always|promise|vow|covenant|faithful|loyal|together)\b', text_lower))
    total = intimacy + passion + commitment
    if total >= 2:
        love_type = "intimacy" if intimacy >= passion and intimacy >= commitment else \
                    "passion" if passion >= commitment else "commitment"
    else:
        love_type = "non-love"
    return {
        "love_type": love_type,
        "wisdom_potential": min(total * 0.15, 0.9) if total >= 2 else 0,
        "intimacy": min(intimacy * 0.2, 1.0),
        "passion": min(passion * 0.2, 1.0),
        "commitment": min(commitment * 0.2, 1.0),
        "detection_method": "lightweight_regex",
    }


# ── Import ML detectors with lightweight fallback ──

try:
    from WEAVER.humour_detector import detect_humour_in_text
except (ImportError, Exception):
    detect_humour_in_text = _lightweight_humour

try:
    from WEAVER.absurdity_detector import detect_absurdity_in_text
except (ImportError, Exception):
    detect_absurdity_in_text = _lightweight_absurdity

try:
    from WEAVER.obsession_detector import detect_obsession_in_text
except (ImportError, Exception):
    detect_obsession_in_text = _lightweight_obsession

try:
    from WEAVER.love_detector import detect_love_in_text
except (ImportError, Exception):
    detect_love_in_text = _lightweight_love

try:
    from WEAVER.proverb_compressor import generate_proverb_from_cluster
except (ImportError, Exception):
    def generate_proverb_from_cluster(cluster):
        return None

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