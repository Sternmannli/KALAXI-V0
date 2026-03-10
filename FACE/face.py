#!/usr/bin/env python3
"""
face.py — KALAXI FACE Module v1.0
The Steward's Interface. One command, full system view.

Run: python3 FACE/face.py

Shows:
  - System pulse (health, counts, overdue)
  - Witness scan (what has been seen vs unseen)
  - Collective dignity check
  - Pending decisions awaiting steward
  - Next actions

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

THRESHOLD = ROOT / "THRESHOLD.md"
PENDING_MD = ROOT / "MANIFEST" / "pending_review.md"
MIRROR_MD = ROOT / "STEWARD" / "mirror.md"

THERMAL_DAYS = 7


def thermal_age(line):
    m = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', line.strip())
    if not m:
        return -1
    seed_date = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - seed_date).days


def mirror_done_today():
    if not MIRROR_MD.exists():
        return False
    today = datetime.now().strftime("%Y-%m-%d")
    return today in MIRROR_MD.read_text()


def section_pulse():
    """System pulse — vital signs."""
    print(f"\n  {'='*52}")
    print(f"  KALAXI — STEWARD DASHBOARD")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  {'='*52}")

    # Mirror ritual
    if mirror_done_today():
        print(f"\n  Mirror ritual:     DONE")
    else:
        print(f"\n  Mirror ritual:     NOT DONE — tend before you build")

    # Threshold counts
    if not THRESHOLD.exists():
        print(f"  THRESHOLD.md:      MISSING")
        return

    lines = [l for l in THRESHOLD.read_text().splitlines()
             if l.strip().startswith("[20")]

    types = {}
    for line in lines:
        m = re.match(r'\[.*?\] — (\w[\w\-]*)', line)
        if m:
            types.setdefault(m.group(1), []).append(line)

    ready = [l for l in lines if thermal_age(l) >= THERMAL_DAYS]
    waiting = [l for l in lines if 0 <= thermal_age(l) < THERMAL_DAYS]

    print(f"  Seeds total:       {len(lines)}")
    print(f"  Seeds ready:       {len(ready)}")
    print(f"  Seeds resting:     {len(waiting)}")
    print(f"  Seed types:        {len(types)}")


def section_witness():
    """Witness Scale scan — what's been seen?"""
    if not THRESHOLD.exists():
        return

    lines = [l for l in THRESHOLD.read_text().splitlines()
             if l.strip().startswith("[20")]

    overdue = []
    for line in lines:
        age = thermal_age(line)
        has_id = bool(re.search(r'(GAP|ANOM|COV|P|W|EQ|CONST|PROT|SPEC|GOV|TRIAD|DEF|FW|SCALE|AXIOM)#[\w\-]+', line))
        if not has_id and age >= THERMAL_DAYS:
            overdue.append((age, line))

    print(f"\n  {'─'*52}")
    print(f"  WITNESS SCAN")
    print(f"  {'─'*52}")

    if overdue:
        print(f"\n  OVERDUE ({len(overdue)} elements past thermal delay, no ID):")
        for age, line in overdue:
            print(f"    [{age}d] {line[:60]}")
    else:
        print(f"\n  All elements witnessed or within thermal delay.")


def section_collective():
    """Collective dignity across the proverb cohort."""
    try:
        from WEAVER.dignity_check import check_collective_dignity
    except ImportError:
        print(f"\n  Collective D:      IMPORT ERROR")
        return

    if not THRESHOLD.exists():
        return

    lines = [l for l in THRESHOLD.read_text().splitlines()
             if l.strip().startswith("[20") and "proverb" in l.lower()]

    texts = []
    for line in lines:
        m = re.search(r'[„""](.+?)["""]', line)
        if m:
            texts.append(m.group(1))
        else:
            texts.append(line[30:110])

    if not texts:
        return

    result = check_collective_dignity(texts, felt_domain="face-dashboard")

    print(f"\n  {'─'*52}")
    print(f"  COLLECTIVE DIGNITY")
    print(f"  {'─'*52}")

    status = "PASS" if result.passed else "FAIL"
    print(f"\n  D_collective:      {result.D_collective:.4f} ({status})")
    print(f"  Cohort size:       {result.cohort_size}")
    print(f"  Mean D:            {result.mean_D:.4f}")
    print(f"  Variance penalty:  {result.variance_penalty:.4f}")

    if result.sealed_gate_triggered:
        print(f"  SEALED GATE:       TRIGGERED")
        print(f"  COV#008:           ACTIVATED — shelter path required")

    zeros = sum(1 for r in result.individual_results if r.D == 0.0)
    if zeros > 0:
        print(f"  Failed seeds:      {zeros}")


def section_pending():
    """Pending decisions awaiting steward."""
    print(f"\n  {'─'*52}")
    print(f"  PENDING DECISIONS")
    print(f"  {'─'*52}")

    if not PENDING_MD.exists():
        print(f"\n  No pending_review.md found.")
        return

    text = PENDING_MD.read_text()
    pending = []
    resolved = []
    for line in text.splitlines():
        if line.startswith("|") and "pending" in line.lower():
            # Extract seed excerpt
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) >= 2:
                pending.append(cols[1][:50])
        elif line.startswith("|") and "resolved" in line.lower():
            resolved.append(1)

    if pending:
        print(f"\n  AWAITING YOUR DECISION ({len(pending)}):")
        for p in pending:
            print(f"    -> {p}")
    else:
        print(f"\n  All seeds resolved. Nothing pending.")

    print(f"  Previously resolved: {len(resolved)}")


def section_actions():
    """Next actions for the steward."""
    print(f"\n  {'─'*52}")
    print(f"  NEXT ACTIONS")
    print(f"  {'─'*52}")
    print()
    print(f"  1. Feed PLAN-001 — the plan is alive")
    print(f"  2. Ratify proposals: Decay, Dignity-Latency,")
    print(f"     Witness Scale, Proprioception Axiom")
    print(f"  3. Review W#HIRING-001 (wisdom node)")
    print(f"  4. Extract 36 remaining treasures from .docx")
    print()
    print(f"  Quick commands:")
    print(f"    python3 .github/scripts/tend.py --thermal-check")
    print(f"    python3 .github/scripts/tend.py --review-threshold")
    print(f"    python3 .github/scripts/tend.py --collective-check")
    print(f"    python3 .github/scripts/tend.py --witness-scan")
    print(f"    python3 SCRIPTS/health_dashboard.py")

    print(f"\n  {'='*52}")
    print(f"  [V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]")
    print(f"  {'='*52}\n")


def main():
    section_pulse()
    section_witness()
    section_collective()
    section_pending()
    section_actions()


if __name__ == "__main__":
    main()
