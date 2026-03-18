#!/usr/bin/env python3
# wisdom_mirror.py – Reflects a donor's patterns back to them

import sys
import json
from datetime import datetime
from pathlib import Path

# Import pillar detectors (assume they are importable)
sys.path.append('.')
try:
    from WEAVER.humour_detector import detect_humour_in_text
    from WEAVER.absurdity_detector import detect_absurdity_in_text
    from WEAVER.obsession_detector import detect_obsession_in_text
    from WEAVER.love_detector import detect_love_in_text
    from WEAVER.proverb_compressor import generate_proverb_from_cluster  # we might use it
    from WEAVER.unified_pillar_detector import detect_pillars
except ImportError:
    # If running standalone, we'll use stubs
    print("Warning: Pillar detectors not found. Using dummy data.")
    def detect_humour_in_text(t): return {"is_humour": False, "humour_type": "none", "wisdom_potential": 0.0}
    def detect_absurdity_in_text(t): return {"is_absurd": False, "absurdity_type": "none", "wisdom_potential": 0.0}
    def detect_obsession_in_text(t): return {"is_obsessive": False, "obsession_type": "none", "wisdom_potential": 0.0}
    def detect_love_in_text(t): return {"love_type": "non-love", "wisdom_potential": 0.0}
    def detect_pillars(t): return {"pillars": {}, "wisdom_potential": 0.0, "dominant_pillar": None}

def generate_mirror(donor_id, messages):
    """
    messages: list of dicts with keys 'text' and 'timestamp'
    Returns a string reflection.
    """
    if not messages:
        return "The canon has not yet received your voice. When you speak, the river listens."

    # Run pillar detection on each message
    humour_count = 0
    absurd_count = 0
    obsession_count = 0
    love_count = 0
    total_wisdom = 0.0
    for msg in messages:
        text = msg['text']
        h = detect_humour_in_text(text)
        if h.get('is_humour'):
            humour_count += 1
            total_wisdom += h.get('wisdom_potential', 0)
        a = detect_absurdity_in_text(text)
        if a.get('is_absurd'):
            absurd_count += 1
            total_wisdom += a.get('wisdom_potential', 0)
        o = detect_obsession_in_text(text)
        if o.get('is_obsessive'):
            obsession_count += 1
            total_wisdom += o.get('wisdom_potential', 0)
        lv = detect_love_in_text(text)
        if lv.get('love_type') != 'non-love':
            love_count += 1
            total_wisdom += lv.get('wisdom_potential', 0)
        # unified pillar could also be used
        up = detect_pillars(text)
        # we can incorporate later

    n = len(messages)
    lines = []
    lines.append(f"## Wisdom Mirror for Donor {donor_id}")
    lines.append(f"*Reflection generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    lines.append(f"You have shared {n} messages with the canon.")

    if humour_count > n/3:
        lines.append("Your words often carry a lightness – humour threads through your voice. The canon smiles with you.")
    elif humour_count > 0:
        lines.append("Occasionally, a glint of humour appears in your words. The canon notes it.")

    if absurd_count > 0:
        lines.append("You touch upon the absurd – the gaps that cannot be closed. The Echo Stone holds these for you.")

    if obsession_count > 0:
        lines.append("Certain themes return in your words, again and again. The canon witnesses your persistence.")
        if obsession_count > n/2:
            lines.append("This recurring pattern may be a gift or a weight. The mirror reflects, it does not judge.")

    if love_count > 0:
        if love_count > n/2:
            lines.append("Your contributions are suffused with care – for others, for ideas, for the world. The canon feels this warmth.")
        else:
            lines.append("Moments of care appear in your voice. They are received.")

    avg_wisdom = total_wisdom / n if n>0 else 0
    lines.append(f"\nYour average wisdom potential: {avg_wisdom:.3f}")

    if avg_wisdom > 0.7:
        lines.append("Your patterns are rich with potential. The river will remember them.")
    elif avg_wisdom > 0.4:
        lines.append("Your voice carries steady meaning. The river flows with it.")
    else:
        lines.append("Your presence is noted. Every drop counts.")

    lines.append("\nThe knot breathes. The river remembers.")

    return "\n".join(lines)

def demo():
    """Demo with a dummy donor."""
    dummy_messages = [
        {"text": "I keep thinking about whether I locked the door. I must check it again.", "timestamp": "2026-02-25 10:00"},
        {"text": "I feel deeply connected to you and cherish every moment.", "timestamp": "2026-02-25 11:00"},
        {"text": "The universe is silent, yet I keep asking. This gap cannot be closed.", "timestamp": "2026-02-25 12:00"},
    ]
    print(generate_mirror("DEMO", dummy_messages))

if __name__ == "__main__":
    # If run with argument, treat as donor ID and read messages from a file? For simplicity, just run demo.
    demo()
