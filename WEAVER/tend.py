#!/usr/bin/env python3
# tend.py – Steward tending interface for Kalaxi
# Run with: python tend.py [--review] [--list] [--ratify SEED_ID] [--compost SEED_ID]

import os
import re
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Paths (relative to repository root)
REPO_ROOT = Path(__file__).parent.parent
THRESHOLD_PATH = REPO_ROOT / "THRESHOLD.md"
STEWARD_MIRROR = REPO_ROOT / "STEWARD" / "mirror.md"
CANON_C_PATH = REPO_ROOT / "KALAXI_C_WISDOM.txt"
MANIFEST_RECEIPTS = REPO_ROOT / "MANIFEST" / "receipts"

# Ensure receipts directory exists
MANIFEST_RECEIPTS.mkdir(parents=True, exist_ok=True)

# Thermal delay configuration (days)
DELAY_CONFIG = {
    "standard": 7,
    "humour": 14,
    "absurdity": None,  # indefinite
    "obsession": 14,
    "love": 10,
    "proverb": 7
}

def read_threshold():
    """Parse THRESHOLD.md and return list of seed dicts."""
    if not THRESHOLD_PATH.exists():
        return []
    with open(THRESHOLD_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    seeds = []
    # Simple parser: each seed starts with a timestamp line like [YYYY-MM-DD HH:MM] -- seed --
    seed_blocks = re.split(r'\n(?=\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] -- seed --)', content)
    for block in seed_blocks:
        if not block.strip():
            continue
        lines = block.strip().split('\n')
        # First line contains timestamp
        match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] -- seed --', lines[0])
        if not match:
            continue
        timestamp_str = match.group(1)
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
        # Extract metadata lines
        metadata = {}
        text_lines = []
        for line in lines[1:]:
            if line.startswith("   "):
                # metadata line
                parts = line.strip().split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    value = parts[1].strip()
                    metadata[key] = value
            else:
                text_lines.append(line)
        text = "\n".join(text_lines).strip()
        seeds.append({
            "timestamp": timestamp,
            "text": text,
            "metadata": metadata,
            "raw_block": block
        })
    return seeds

def check_mirror_ritual():
    """Verify that mirror.md exists and has an entry within the last 24 hours."""
    if not STEWARD_MIRROR.exists():
        print("ERROR: STEWARD/mirror.md not found. Run the Mirror Ritual first.")
        return False
    with open(STEWARD_MIRROR, "r", encoding="utf-8") as f:
        content = f.read()
    # Look for most recent entry (assuming entries are separated by ## or similar)
    # Format expected: **Timestamp:** YYYY-MM-DD HH:MM
    timestamps = re.findall(r'\*\*Timestamp:\*\*\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', content)
    if not timestamps:
        print("ERROR: No timestamp found in mirror.md. Please include a timestamp line like:")
        print('  **Timestamp:** 2026-02-25 23:57')
        return False
    latest = max(datetime.strptime(ts, "%Y-%m-%d %H:%M") for ts in timestamps)
    if datetime.now() - latest > timedelta(hours=24):
        print(f"ERROR: Last mirror.md entry ({latest}) is older than 24 hours. Update before tending.")
        return False
    return True

def seed_is_ready(seed):
    """Check if seed has aged beyond its thermal delay."""
    delay_str = seed["metadata"].get("recommended delay", "7 days")
    if "indefinite" in delay_str:
        return False  # absurdity seeds never become ready through time alone
    # Extract number of days (e.g., "7 days" → 7)
    match = re.search(r'\d+', delay_str)
    if not match:
        return False
    days = int(match.group())
    age = datetime.now() - seed["timestamp"]
    return age.days >= days

def list_pending():
    """List all seeds in THRESHOLD.md with their status."""
    seeds = read_threshold()
    if not seeds:
        print("No seeds in THRESHOLD.md.")
        return
    print("\n=== Pending Seeds ===\n")
    for i, seed in enumerate(seeds):
        ready = seed_is_ready(seed)
        status = "READY" if ready else "pending"
        print(f"[{i}] {seed['timestamp'].strftime('%Y-%m-%d %H:%M')} – {status}")
        print(f"    {seed['text'][:80]}...")
        print(f"    Metadata: {seed['metadata']}\n")

def review_all():
    """Interactive review of ready seeds."""
    if not check_mirror_ritual():
        return
    seeds = read_threshold()
    ready_seeds = [s for s in seeds if seed_is_ready(s)]
    if not ready_seeds:
        print("No seeds ready for review.")
        return
    print(f"\n=== {len(ready_seeds)} seed(s) ready for review ===\n")
    for idx, seed in enumerate(ready_seeds):
        print(f"\n--- Seed {idx} ---")
        print(f"Timestamp: {seed['timestamp']}")
        print(f"Text: {seed['text']}")
        print(f"Metadata: {seed['metadata']}")
        action = input("\nAction: (r)atify, (c)ompost, (s)kip: ").strip().lower()
        if action == 'r':
            ratify_seed(seed)
        elif action == 'c':
            compost_seed(seed)
        else:
            print("Skipped.\n")

def ratify_seed(seed):
    """Append ratified proverb to canon and remove from THRESHOLD."""
    # Generate receipt
    receipt = {
        "seed_id": f"seed_{seed['timestamp'].strftime('%Y%m%d%H%M%S')}",
        "text": seed['text'],
        "ratified_at": datetime.now().isoformat(),
        "metadata": seed['metadata']
    }
    receipt_file = MANIFEST_RECEIPTS / f"ratify_{receipt['seed_id']}.json"
    with open(receipt_file, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
    
    # Append to proverb canon (KALAXI_C_WISDOM.txt)
    with open(CANON_C_PATH, "a", encoding="utf-8") as f:
        # Find the next available P# number (simplified: just append with date)
        f.write(f"\nP#NEW: {seed['text']}  # ratified {datetime.now().date()}\n")
    
    # Remove from THRESHOLD.md (rewrite file without this seed)
    remove_seed_from_threshold(seed)
    print(f"Ratified. Receipt saved to {receipt_file}")

def compost_seed(seed):
    """Move seed to compost archive."""
    compost_dir = REPO_ROOT / "NARRATIVE" / "compost"
    compost_dir.mkdir(parents=True, exist_ok=True)
    filename = f"compost_{seed['timestamp'].strftime('%Y%m%d%H%M%S')}.txt"
    compost_file = compost_dir / filename
    with open(compost_file, "w", encoding="utf-8") as f:
        f.write(f"# Composted Seed\nTimestamp: {seed['timestamp']}\nText:\n{seed['text']}\nMetadata:\n{seed['metadata']}\n")
    remove_seed_from_threshold(seed)
    print(f"Composted to {compost_file}")

def remove_seed_from_threshold(seed):
    """Rewrite THRESHOLD.md excluding the given seed block."""
    with open(THRESHOLD_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Replace the seed's raw block with nothing
    new_content = content.replace(seed["raw_block"], "")
    # Clean up extra blank lines
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    with open(THRESHOLD_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tend.py [--list] [--review]")
        sys.exit(1)
    if "--list" in sys.argv:
        list_pending()
    elif "--review" in sys.argv:
        review_all()
    else:
        print("Unknown option.")