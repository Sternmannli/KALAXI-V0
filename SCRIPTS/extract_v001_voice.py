#!/usr/bin/env python3
"""Extract all V-001 entries from the Input Ledger into VOICE/V001/."""
import json
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(BASE, "KEEP", "INPUT_LEDGER", "index.json")
OUT = os.path.join(BASE, "VOICE", "V001")

print(f"Reading {INDEX}...")
with open(INDEX, "r", encoding="utf-8") as f:
    data = json.load(f)

entries = [e for e in data["entries"] if e.get("voice") == "V-001"]
entries.sort(key=lambda e: e.get("timestamp", ""))

print(f"Found {len(entries)} V-001 entries out of {data['total_entries']} total.")

# --- 1. Complete Chronicle (chronological, readable) ---
chronicle_path = os.path.join(OUT, "complete_chronicle.md")
by_month = {}
essences = []

with open(chronicle_path, "w", encoding="utf-8") as f:
    f.write("# The Voice of V-001 — Complete Chronicle\n")
    f.write(f"> {len(entries)} inputs. Every word, verbatim. Chronological.\n")
    f.write("> This file is generated from the Input Ledger. Append-only source.\n\n")
    f.write("---\n\n")

    for i, e in enumerate(entries):
        eid = e.get("entry_id", f"UNKNOWN-{i}")
        ts = e.get("timestamp", "unknown")
        raw = e.get("raw_text", "")
        ctx = e.get("context", "")
        tags = ", ".join(e.get("tags", []))
        essence = e.get("essence", "")

        # Parse month
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            month_key = dt.strftime("%Y-%m")
            date_str = dt.strftime("%Y-%m-%d %H:%M UTC")
        except:
            month_key = "unknown"
            date_str = ts

        # Build entry block
        block = f"## {eid}\n"
        block += f"**{date_str}** · {ctx}\n\n"
        if raw.strip():
            block += f"{raw.strip()}\n\n"
        if essence:
            block += f"*Essence: {essence}*\n\n"
        block += "---\n\n"

        f.write(block)

        # Collect by month
        if month_key not in by_month:
            by_month[month_key] = []
        by_month[month_key].append(block)

        # Collect essence
        if essence:
            essences.append(f"**{eid}** ({date_str}): {essence}")
        elif raw.strip():
            # Use first 100 chars of raw text as essence if no essence exists
            short = raw.strip()[:120].replace("\n", " ")
            essences.append(f"**{eid}** ({date_str}): {short}...")

print(f"Written: {chronicle_path} ({len(entries)} entries)")

# --- 2. By-month files ---
month_dir = os.path.join(OUT, "by_month")
os.makedirs(month_dir, exist_ok=True)
for month_key, blocks in sorted(by_month.items()):
    month_path = os.path.join(month_dir, f"{month_key}.md")
    with open(month_path, "w", encoding="utf-8") as f:
        f.write(f"# V-001 Voice — {month_key}\n")
        f.write(f"> {len(blocks)} inputs this month.\n\n---\n\n")
        for block in blocks:
            f.write(block)
    print(f"Written: {month_path} ({len(blocks)} entries)")

# --- 3. Essence file ---
essence_path = os.path.join(OUT, "essence.md")
with open(essence_path, "w", encoding="utf-8") as f:
    f.write("# V-001 — Essence of Every Input\n")
    f.write(f"> {len(essences)} distilled lines. One per input.\n\n---\n\n")
    for line in essences:
        f.write(f"- {line}\n")
print(f"Written: {essence_path} ({len(essences)} lines)")

# --- 4. Stats ---
print(f"\nDone. {len(entries)} V-001 entries organized into:")
print(f"  - complete_chronicle.md (full text)")
print(f"  - {len(by_month)} monthly files in by_month/")
print(f"  - essence.md ({len(essences)} one-liners)")
