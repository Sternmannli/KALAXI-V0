# weaver/review.py
# Display candidate seeds in THRESHOLD.md with metadata

import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
THRESHOLD = ROOT / "THRESHOLD.md"

def parse_threshold():
    if not THRESHOLD.exists():
        print("THRESHOLD.md not found.")
        return []

    lines = THRESHOLD.read_text().splitlines()
    candidates = []
    for line in lines:
        if not line.strip():
            continue
        # Look for lines with metadata (CONF, GRADE, DIGNITY)
        if "CONF:" in line or "GRADE:" in line:
            candidates.append(line)
    return candidates

def show_review():
    candidates = parse_threshold()
    if not candidates:
        print("No candidate seeds found with metadata.")
        return

    print("\n" + "="*60)
    print(f"CANDIDATE SEEDS REVIEW – {datetime.now().strftime('%Y-%m-%d')}")
    print("="*60)
    for i, seed in enumerate(candidates, 1):
        print(f"\n--- Candidate {i} ---")
        print(seed)
    print("\n" + "="*60)
    print("To act on a seed, use:")
    print("  tend.py --canonise \"seed line\" TYPE")
    print("  tend.py --compost \"seed line\" \"reason\"")
    print("  tend.py --refuse \"seed line\" \"reason\"")

if __name__ == "__main__":
    show_review()