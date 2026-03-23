#!/usr/bin/env python3
# echo_stone.py – Witness for unresolvable absurd seeds

import json
from datetime import datetime
from pathlib import Path

ABSURDITY_QUEUE = Path(__file__).parent.parent / "ABSURDITY_QUEUE.md"

def log_absurd_seed(seed_text, metadata=None):
    """Append an absurd seed to the queue with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    seed_id = f"ABSURD_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    # Simple Markdown table row
    row = f"| {timestamp} | {seed_id} | {seed_text[:50]}... | |\n"
    with open(ABSURDITY_QUEUE, "a") as f:
        f.write(row)
    return seed_id

def reflect(seed_id, reflection):
    """Add steward reflection to an absurd seed.

    Appends the reflection to the absurdity queue as a follow-up entry.
    The seed_id links it to the original absurd seed.
    """
    if not seed_id or not reflection:
        return False
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    row = f"| {timestamp} | {seed_id} | REFLECTION: {reflection[:80]} | steward |\n"
    with open(ABSURDITY_QUEUE, "a") as f:
        f.write(row)
    return True

if __name__ == "__main__":
    # Example usage
    test_seed = "The universe is silent, yet I keep asking. This gap cannot be closed."
    sid = log_absurd_seed(test_seed)
    print(f"Logged absurd seed: {sid}")
