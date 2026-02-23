#!/usr/bin/env python3
# tend.py – Kalaxi Tending Engine with Canon Integrity

import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta, timezone
import sys

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
THRESHOLD = REPO_ROOT / "THRESHOLD.md"
IDS_JSON = REPO_ROOT / "MANIFEST" / "ids.json"
HEARTBEAT = REPO_ROOT / "MANIFEST" / "heartbeat.md"
COMPOST_DIR = REPO_ROOT / "NARRATIVE" / "Compost"
STEWARD_MIRROR = REPO_ROOT / "STEWARD" / "mirror.md"
SLICE_A = REPO_ROOT / "KALAXI_A_FOUNDATION.txt"
SLICE_B = REPO_ROOT / "KALAXI_B_MODULES_AND_VOICE.txt"
SLICE_C = REPO_ROOT / "KALAXI_C_WISDOM.txt"
SLICE_D = REPO_ROOT / "KALAXI_D_INTERFACE_AND_LEDGER.txt"
CONSTITUTIONAL = [SLICE_A, SLICE_B, SLICE_D]

# Configuration
THERMAL_DAYS = 7
GROWTH_BUDGET = 10          # max seeds per tending session

def load_ids():
    if IDS_JSON.exists():
        with open(IDS_JSON) as f:
            return json.load(f)
    return {"last_id": {"P": 0, "ANOM": 0, "GAP": 0, "W": 0, "COV": 12}, "entries": {}}

def save_ids(data):
    with open(IDS_JSON, "w") as f:
        json.dump(data, f, indent=2)

def compute_hash(text):
    return hashlib.sha256(text.strip().encode()).hexdigest()

def next_id(ids_data, prefix):
    last = ids_data["last_id"].get(prefix, 0)
    nxt = last + 1
    ids_data["last_id"][prefix] = nxt
    return f"{prefix}#{nxt:04d}" if prefix != "P" else f"P#EMERGE-{nxt:04d}"

def register_seed(seed_text, seed_type, provenance, ids_data):
    h = compute_hash(seed_text)
    prefix_map = {"proverb": "P", "anomaly": "ANOM", "gap": "GAP", "wisdom": "W"}
    prefix = prefix_map.get(seed_type, "P")
    new_id = next_id(ids_data, prefix)
    ids_data["entries"][new_id] = {
        "id": new_id,
        "type": seed_type,
        "status": "provisional",
        "created": datetime.now(timezone.utc).isoformat(),
        "provenance": provenance,
        "supersedes": None,
        "hash": h
    }
    save_ids(ids_data)
    return new_id

def check_thermal_delay(timestamp_str):
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', timestamp_str)
    if not match:
        return False
    seed_date = datetime.strptime(match.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - seed_date).days
    return age >= THERMAL_DAYS

def mirror_check():
    if not STEWARD_MIRROR.exists():
        return False
    content = STEWARD_MIRROR.read_text()
    today = datetime.now().strftime("%Y-%m-%d")
    return today in content

def heartbeat():
    open_gaps = 0
    threshold_count = 0
    if THRESHOLD.exists():
        threshold_count = len([l for l in THRESHOLD.read_text().splitlines() if l.strip()])
    compost_count = len(list(COMPOST_DIR.glob("*.md"))) if COMPOST_DIR.exists() else 0
    content = f"""# Canon Heartbeat – {datetime.now().strftime("%Y-%m-%d")}
Open gaps: {open_gaps}
Seeds in THRESHOLD: {threshold_count}
Seeds deferred (last 28d): ?
Seeds ratified (last 28d): ?
Avg thermal delay (last 28d): {THERMAL_DAYS} days
Steward activity (reviews): ?
Silent gaps flagged: []
Compost active size: {compost_count}
Next Turning of the Garden: ?
Notes:
"""
    HEARTBEAT.parent.mkdir(exist_ok=True)
    HEARTBEAT.write_text(content)

def is_constitutional(file):
    return file in CONSTITUTIONAL

def can_commit(file, msg):
    if is_constitutional(file) and "CONFIRMATION: 2/2" not in msg:
        print(f"❌ Blocked: constitutional file {file.name} requires CONFIRMATION: 2/2 in commit message.")
        return False
    return True

def compost_seed(seed_line, reason):
    if not COMPOST_DIR.exists():
        COMPOST_DIR.mkdir(parents=True)
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    fname = COMPOST_DIR / f"COMPOST-{now}.md"
    content = f"""[COMPOSTED {datetime.now().strftime("%Y-%m-%d")}]
Original ID: 
Reason: {reason}
Original text:
> {seed_line}

Latent Patterns Observed:

Mycelial Threads:

Seasonal Notes:

Dignity Seal: This offering was received with gratitude.
"""
    fname.write_text(content)
    print(f"✅ Composted to {fname.name}")

def main():
    if len(sys.argv) < 2:
        print("Usage: tend.py [--thermal-check | --compost | --heartbeat | --mirror-check]")
        return

    cmd = sys.argv[1]

    if cmd == "--thermal-check":
        if not THRESHOLD.exists():
            print("THRESHOLD.md not found.")
            return
        lines = THRESHOLD.read_text().splitlines()
        for line in lines:
            if check_thermal_delay(line):
                print(f"✅ {line}")
            else:
                print(f"⏳ {line}")
        return

    if cmd == "--compost":
        if len(sys.argv) < 4:
            print("Usage: tend.py --compost \"seed line\" \"reason\"")
            return
        seed_line = sys.argv[2]
        reason = sys.argv[3]
        compost_seed(seed_line, reason)
        return

    if cmd == "--heartbeat":
        heartbeat()
        return

    if cmd == "--mirror-check":
        print("✅" if mirror_check() else "❌ Mirror not updated today.")
        return

if __name__ == "__main__":
    main()