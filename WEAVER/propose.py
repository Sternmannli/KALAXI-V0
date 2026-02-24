# weaver/propose.py
# Generate candidate seeds from patterns and append to THRESHOLD.md

import json
from pathlib import Path
from datetime import datetime
from dignity_filter import check_dignity
from confidence import compute_confidence, confidence_grade

ROOT = Path(__file__).parent.parent
PATTERNS_FILE = ROOT / "MANIFEST" / "patterns.json"
THRESHOLD = ROOT / "THRESHOLD.md"

def propose_seeds():
    if not PATTERNS_FILE.exists():
        print("No patterns.json found.")
        return

    with open(PATTERNS_FILE) as f:
        patterns = json.load(f)

    new_seeds = []
    for p in patterns:
        # Skip if already proposed (you can add a flag later)
        keyword = p.get("keyword")
        count = p.get("count", 0)
        if count < 3:
            continue

        # Generate a simple proverb seed
        seed_text = f"[{datetime.now().strftime('%Y-%m-%d')}] -- proverb -- The word '{keyword}' appears {count} times. Perhaps it carries meaning."
        
        # Run dignity filter
        ok, reasons = check_dignity(seed_text)
        if not ok:
            print(f"Seed for '{keyword}' failed dignity: {reasons}")
            continue

        # Compute confidence
        conf = compute_confidence(p)
        grade = confidence_grade(conf)

        # Build metadata line
        metadata = f" -- SOURCE:pattern -- CONF:{conf:.2f} -- GRADE:{grade} -- DIGNITY:pass"
        full_line = seed_text + metadata

        # Append to THRESHOLD
        with open(THRESHOLD, "a") as f:
            f.write(full_line + "\n")
        
        new_seeds.append(keyword)
        print(f"Added seed for '{keyword}'")

    print(f"Proposed {len(new_seeds)} new seeds.")

if __name__ == "__main__":
    propose_seeds()