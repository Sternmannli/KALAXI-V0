#!/usr/bin/env python3
"""
tend.py -- Kalaxi Tending Engine v2.3
Interrogative, not authoritative. Advisory, not decisive.
The system asks. The steward decides.

Two-tier approval:
Signed seeds ([SIGNED: Mohamed]) bypass thermal delay but not checks.
Unsigned seeds wait 7 days, then reviewed with questions.

Commands:
  --thermal-check          List seeds ready for tending
  --mirror-check           Confirm mirror ritual done today
  --heartbeat              Generate MANIFEST/heartbeat.md
  --grade "line"           Show confidence grade for a seed
  --review-threshold       Walk through all ready seeds with questions
  --process-signed         Immediately process [SIGNED: Mohamed] seeds
  --process-pending        List pending seeds; canonise those approved
  --compost "line" "why"   Compost a seed with reason
  --refuse "line" "why"    Refuse a seed (adds to refusals.md)
  --canonise "line" TYPE   Move seed to canon (thermal delay enforced)
  --scan                   Calibrate ID registry from slice files
  --collective-check       Run collective D metric across THRESHOLD cohort
  --witness-scan           Scan all registry elements for W-Scale status
"""

import re
import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT          = Path(__file__).parent.parent.parent
THRESHOLD     = ROOT / "THRESHOLD.md"
IDS_JSON      = ROOT / "MANIFEST" / "ids.json"
REJECTED_MD   = ROOT / "MANIFEST" / "rejected.md"
REFUSALS_MD   = ROOT / "MANIFEST" / "refusals.md"
HEARTBEAT_MD  = ROOT / "MANIFEST" / "heartbeat.md"
AMENDMENTS_MD = ROOT / "MANIFEST" / "amendments.md"
PENDING_MD    = ROOT / "MANIFEST" / "pending_review.md"
COMPOST_DIR   = ROOT / "NARRATIVE" / "Compost"
MIRROR_MD     = ROOT / "STEWARD" / "mirror.md"
OVERRIDES_MD  = ROOT / "STEWARD" / "overrides.md"
SLICE_A       = ROOT / "KALAXI_A_FOUNDATION.txt"
SLICE_B       = ROOT / "KALAXI_B_MODULES_AND_VOICE.txt"
SLICE_C       = ROOT / "KALAXI_C_WISDOM.txt"
SLICE_D       = ROOT / "KALAXI_D_INTERFACE_AND_LEDGER.txt"
CONSTITUTIONAL = {SLICE_A, SLICE_B, SLICE_D}

THERMAL_DAYS  = 7
STEWARD_NAME  = "Mohamed"   # change if steward's name changes

def load_ids():
    if IDS_JSON.exists():
        with open(IDS_JSON) as f:
            return json.load(f)
    return {
        "last_id": {"P": 28, "ANOM": 512, "GAP": 15, "W": 1, "COV": 14},
        "entries": {}
    }

def save_ids(data):
    IDS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(IDS_JSON, "w") as f:
        json.dump(data, f, indent=2)

def sha(text):
    return hashlib.sha256(text.strip().encode()).hexdigest()

def next_id(ids_data, prefix):
    last = ids_data["last_id"].get(prefix, 0)
    nxt  = last + 1
    ids_data["last_id"][prefix] = nxt
    if prefix == "P":
        return f"P#EMERGE-{nxt:04d}"
    return f"{prefix}#{nxt:04d}"

def register_seed(text, seed_type, provenance, ids_data):
    prefix_map = {"proverb": "P", "anomaly": "ANOM", "gap": "GAP", "wisdom": "W"}
    prefix = prefix_map.get(seed_type.lower(), "P")
    new_id = next_id(ids_data, prefix)
    ids_data["entries"][new_id] = {
        "id":         new_id,
        "type":       seed_type,
        "status":     "ratified",
        "created":    datetime.now(timezone.utc).isoformat(),
        "provenance": provenance,
        "supersedes": None,
        "hash":       sha(text)
    }
    save_ids(ids_data)
    return new_id

def find_duplicate(text, ids_data):
    h = sha(text)
    for entry_id, entry in ids_data["entries"].items():
        if entry.get("hash") == h:
            return entry_id
    return None

def thermal_age(line):
    m = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', line.strip())
    if not m:
        return -1
    seed_date = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - seed_date).days

CONFIDENCE_LEVELS = {
    "CERTAIN": {"symbol": "●", "behaviour": "state -- no question needed"},
    "HIGH":    {"symbol": "◉", "behaviour": "recommend -- ask one question"},
    "MEDIUM":  {"symbol": "◎", "behaviour": "surface -- ask two questions"},
    "LOW":     {"symbol": "○", "behaviour": "offer -- invite the steward to look again"},
    "WARNING": {"symbol": "⚠", "behaviour": "halt -- requires explicit steward decision"},
}

VOID_TRIGGERS = [
    ("harvest",  "COV#VOID-001: Never Harvest the Source"),
    ("profile",  "COV#VOID-001: Never Harvest the Source"),
    ("delete",   "COV#VOID-003: Never Erase the Compost"),
    ("erase",    "COV#VOID-003: Never Erase the Compost"),
    ("urgent",   "COV#VOID-004: Never Collapse the Delay"),
    ("bypass",   "COV#VOID-004: Never Collapse the Delay"),
    ("automat",  "COV#VOID-005: Never Speak for the Child"),
    ("auto-dec", "COV#VOID-005: Never Speak for the Child"),
]

def grade_seed(seed_line, ids_data):
    signals = []
    demerits = []
    questions = []

    duplicate = find_duplicate(seed_line, ids_data)
    if duplicate:
        return {
            "level":     "WARNING",
            "signals":   [],
            "demerits":  [f"Exact duplicate of {duplicate} already in registry"],
            "questions": ["Is this a refinement? If so, note what changes and why."],
            "behaviour": CONFIDENCE_LEVELS["WARNING"]["behaviour"],
            "symbol":    CONFIDENCE_LEVELS["WARNING"]["symbol"],
        }

    age = thermal_age(seed_line)
    if 0 <= age < THERMAL_DAYS:
        return {
            "level":     "CERTAIN",
            "signals":   [f"Thermal block: {age} days old, minimum {THERMAL_DAYS}"],
            "demerits":  [],
            "questions": [],
            "behaviour": "block -- do not move until thermal delay passes",
            "symbol":    CONFIDENCE_LEVELS["CERTAIN"]["symbol"],
        }

    lower = seed_line.lower()
    for trigger, covenant in VOID_TRIGGERS:
        if trigger in lower:
            demerits.append(f"Contains '{trigger}' -- check against {covenant}")
            questions.append(f"Does this seed conflict with {covenant}?")

    has_id_link   = bool(re.search(r'(GAP|ANOM|COV|P)#\w+', seed_line))
    has_timestamp = bool(re.match(r'\[\d{4}-\d{2}-\d{2}\]', seed_line.strip()))
    has_type      = any(t in lower for t in ["proverb","anomaly","gap","wisdom","covenant"])
    age_ok        = age >= THERMAL_DAYS

    if has_id_link:
        signals.append("Links to canonical ID -- COV#006 satisfied")
    if has_timestamp:
        signals.append("Timestamp present -- provenance traceable")
    if has_type:
        signals.append("Type declared -- classification possible")
    if age_ok:
        signals.append(f"Thermal delay met: {age} days")

    text_only = re.sub(r'\[.*?\]', '', seed_line).strip()
    word_count = len(text_only.split())
    if word_count < 5:
        demerits.append("Very short -- may be a fragment")
        questions.append("Is this complete, or a note to yourself?")
    if word_count > 150:
        demerits.append("Very long -- may contain more than one seed")
        questions.append("Does this hold one idea, or several that should be separated?")
    if not has_id_link:
        demerits.append("No canonical ID link -- COV#006 not yet satisfied")
        questions.append("Which gap, anomaly, or covenant does this connect to?")
    if not has_timestamp:
        demerits.append("No timestamp -- provenance unclear")
        questions.append("When did this arrive, and from whom?")

    positive = sum([has_id_link, has_timestamp, has_type, age_ok])
    negative = len(demerits)

    if any("COV#VOID" in d for d in demerits):
        level = "WARNING"
    elif positive >= 3 and negative == 0:
        level = "HIGH"
    elif positive >= 2 and negative <= 1:
        level = "MEDIUM"
    else:
        level = "LOW"

    if not questions:
        if level == "HIGH":
            questions = ["Can you say in one sentence what gap this fills?"]
        elif level == "MEDIUM":
            questions = [
                "What does this express that is not already in the canon?",
                "Which gap or anomaly does this connect to?",
            ]
        elif level == "LOW":
            questions = [
                "Read this again tomorrow. Does it still hold?",
                "Is this wisdom, or the feeling of wisdom?",
            ]

    return {
        "level":     level,
        "signals":   signals,
        "demerits":  demerits,
        "questions": questions,
        "behaviour": CONFIDENCE_LEVELS[level]["behaviour"],
        "symbol":    CONFIDENCE_LEVELS[level]["symbol"],
    }

def print_grade(seed_line, grade):
    s = grade["symbol"]
    print(f"\n{s}  {grade['level']}  --  {grade['behaviour']}")
    print(f"{'─'*60}")
    print(f"Seed: {seed_line[:80]}")
    if grade["signals"]:
        print(f"\n  Strengths:")
        for sig in grade["signals"]:
            print(f"    ✓  {sig}")
    if grade["demerits"]:
        print(f"\n  Concerns:")
        for d in grade["demerits"]:
            print(f"    ·  {d}")
    if grade["questions"]:
        print(f"\n  Questions for the steward:")
        for q in grade["questions"]:
            print(f"    →  {q}")
    print()

def cmd_grade(seed_line):
    ids = load_ids()
    grade = grade_seed(seed_line, ids)
    print_grade(seed_line, grade)

def cmd_thermal_check():
    if not THRESHOLD.exists():
        print("❌  THRESHOLD.md not found.")
        return
    lines = [l for l in THRESHOLD.read_text().splitlines()
             if l.strip() and l.strip().startswith("[20")]
    if not lines:
        print("No dated seeds found in THRESHOLD.md")
        return
    ready = [l for l in lines if thermal_age(l) >= THERMAL_DAYS]
    waiting = [l for l in lines if thermal_age(l) < THERMAL_DAYS]
    print(f"\n{'─'*60}")
    print(f"THERMAL CHECK -- {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'─'*60}")
    if ready:
        print(f"\n✅  READY FOR TENDING ({len(ready)} seeds):")
        for l in ready:
            print(f"    [{thermal_age(l)}d]  {l[:70]}")
    if waiting:
        print(f"\n⏳  STILL RESTING ({len(waiting)} seeds):")
        for l in waiting:
            remaining = THERMAL_DAYS - thermal_age(l)
            print(f"    [{remaining}d left]  {l[:70]}")
    print()

def mirror_done_today():
    if not MIRROR_MD.exists():
        return False
    today = datetime.now().strftime("%Y-%m-%d")
    return today in MIRROR_MD.read_text()

def cmd_mirror_check():
    if mirror_done_today():
        print("✅  Mirror ritual completed today. Tending may proceed.")
    else:
        print("❌  Mirror ritual not recorded today.")
        print(f"    Open STEWARD/mirror.md and add today's date ({datetime.now().strftime('%Y-%m-%d')}).")
        print("    The system will not canonise without it.")

def cmd_heartbeat():
    threshold_seeds = 0
    ready_seeds     = 0
    if THRESHOLD.exists():
        for line in THRESHOLD.read_text().splitlines():
            if line.strip().startswith("[20"):
                threshold_seeds += 1
                if thermal_age(line) >= THERMAL_DAYS:
                    ready_seeds += 1
    compost_count = len(list(COMPOST_DIR.glob("*.md"))) if COMPOST_DIR.exists() else 0
    refusal_count = 0
    if REFUSALS_MD.exists():
        refusal_count = sum(1 for l in REFUSALS_MD.read_text().splitlines()
                           if l.strip() and not l.startswith("#") and not l.startswith("|"))
    pending_count = 0
    if PENDING_MD.exists():
        pending_count = sum(1 for l in PENDING_MD.read_text().splitlines()
                           if l.strip() and not l.startswith("#") and not l.startswith("|"))
    ids = load_ids()
    ratified = sum(1 for v in ids["entries"].values() if v.get("status") == "ratified")
    provisional = sum(1 for v in ids["entries"].values() if v.get("status") == "provisional")

    content = f"""# Canon Heartbeat -- {datetime.now().strftime("%Y-%m-%d")}

Seeds in THRESHOLD: {threshold_seeds}
Seeds ready (thermal passed): {ready_seeds}
Seeds ratified (registry): {ratified}
Seeds provisional (registry): {provisional}
Pending review: {pending_count}
Compost files: {compost_count}
Refusals recorded: {refusal_count}
Thermal delay: {THERMAL_DAYS} days

Open questions (update manually):
- Who is the second key for constitutional changes?
- Which gaps are silent (no activity in 30+ days)?

Next Turning of the Garden: -- (set manually)
Notes:
"""
    HEARTBEAT_MD.parent.mkdir(parents=True, exist_ok=True)
    HEARTBEAT_MD.write_text(content)
    print(f"✅  Heartbeat written → MANIFEST/heartbeat.md")
    print(f"    {threshold_seeds} seeds in threshold | {ready_seeds} ready | {pending_count} pending | {compost_count} composted | {refusal_count} refused")

def cmd_review_threshold():
    if not THRESHOLD.exists():
        print("❌  THRESHOLD.md not found.")
        return
    lines = [l for l in THRESHOLD.read_text().splitlines()
             if l.strip() and l.strip().startswith("[20")]
    ready = [l for l in lines if thermal_age(l) >= THERMAL_DAYS]

    if not ready:
        print("⏳  No seeds have passed thermal delay yet.")
        return

    ids = load_ids()
    print(f"\n{'─'*60}")
    print(f"TENDING REVIEW -- {len(ready)} seeds ready")
    print(f"{'─'*60}")
    print("Grades are grounded in Kalaxi's own architecture.")
    print("The system asks. You decide.\n")

    for i, seed in enumerate(ready, 1):
        grade = grade_seed(seed, ids)
        print(f"SEED {i} of {len(ready)}")
        print_grade(seed, grade)
        print(f"  Your options: canonise / compost / refuse / defer")
        print(f"{'─'*60}")

    print("\nWhen ready, run:")
    print("  python tend.py --canonise \"seed line\" TYPE")
    print("  python tend.py --compost  \"seed line\" \"reason\"")
    print("  python tend.py --refuse   \"seed line\" \"reason\"")
    print()

def _canonise_direct(seed_line, seed_type, provenance, ids):
    new_id = register_seed(seed_line, seed_type, provenance, ids)
    target = SLICE_A if seed_type.lower() == "gap" else SLICE_C
    with open(target, "a") as f:
        f.write(f"\n\n[{datetime.now().strftime('%Y-%m-%d')}] CANONISED ({provenance}) -- {new_id}\n{seed_line}\n")
    return new_id, target

def _guess_type(seed_line):
    lower = seed_line.lower()
    for t in ["proverb", "anomaly", "gap", "wisdom", "covenant"]:
        if t in lower:
            return t
    return "proverb"

def _init_pending():
    PENDING_MD.parent.mkdir(parents=True, exist_ok=True)
    if not PENDING_MD.exists():
        PENDING_MD.write_text(
            "# Pending Review -- Seeds Flagged by System\n\n"
            "Seeds here failed automated checks after the steward signed them.\n"
            "The system does not reject them -- it holds them for a second look.\n\n"
            "To approve: change `[ ]` to `[x]` in the Signatures column.\n"
            "Then run: python tend.py --process-pending\n\n"
            "To compost: python tend.py --compost \"seed text\" \"reason\"\n"
            "To refuse:  python tend.py --refuse  \"seed text\" \"reason\"\n\n"
            "Every seed in this file deserves a decision. Do not let it sit.\n\n"
            "| Date | Seed (excerpt) | Failure reason | Signatures | Status |\n"
            "|------|----------------|----------------|------------|--------|\n"
        )

def cmd_process_signed():
    if not THRESHOLD.exists():
        print("❌  THRESHOLD.md not found.")
        return

    pattern = re.compile(
        rf'^\[(\d{{4}}-\d{{2}}-\d{{2}})\].*\[SIGNED:\s*{re.escape(STEWARD_NAME)}\].*$'
    )
    all_lines   = THRESHOLD.read_text().splitlines()
    signed      = [l for l in all_lines if pattern.match(l.strip())]
    unsigned    = [l for l in all_lines if not pattern.match(l.strip())]

    if not signed:
        print(f"No seeds with [SIGNED: {STEWARD_NAME}] found in THRESHOLD.md.")
        return

    print(f"\nFound {len(signed)} signed seed(s). Running checks...\n")
    ids     = load_ids()
    passed  = []
    flagged = []

    for seed in signed:
        grade = grade_seed(seed, ids)
        if grade["level"] == "WARNING" or grade["demerits"]:
            flagged.append((seed, grade))
        else:
            passed.append((seed, grade))

    for seed, grade in passed:
        typ = _guess_type(seed)
        new_id, target = _canonise_direct(seed, typ, "signed-steward", ids)
        print(f"  ✅  {new_id}  →  {target.name}")
        print(f"      {seed[:70]}")

    if flagged:
        _init_pending()
        with open(PENDING_MD, "a") as f:
            for seed, grade in flagged:
                reasons = "; ".join(grade["demerits"][:2])
                excerpt = seed[:50].replace("|", "/")
                today   = datetime.now().strftime("%Y-%m-%d")
                f.write(f"| {today} | {excerpt}… | {reasons} | [ ] {STEWARD_NAME} | waiting |\n")
                print(f"  ⚠️   Flagged → pending_review.md")
                print(f"      {seed[:70]}")
                print(f"      Reason: {reasons}")

    THRESHOLD.write_text("\n".join(unsigned) + "\n")
    print(f"\n{'─'*60}")
    print(f"Processed: {len(passed)} canonised, {len(flagged)} moved to pending.")
    if passed:
        print(f"\nSuggested commit message:")
        print(f"  Tending {datetime.now().strftime('%Y-%m-%d')}: signed-path canonised {len(passed)} seed(s)")
    print()

def cmd_process_pending():
    if not PENDING_MD.exists():
        print("No pending_review.md found. Nothing to process.")
        return

    lines   = PENDING_MD.read_text().splitlines()
    header  = []
    rows    = []
    in_body = False

    for line in lines:
        if line.startswith("|---"):
            header.append(line)
            in_body = True
        elif in_body and line.startswith("|"):
            rows.append(line)
        else:
            header.append(line)

    approved  = []
    remaining = []

    for row in rows:
        cols = [c.strip() for c in row.strip("|").split("|")]
        if len(cols) >= 4:
            sig_col = cols[3]
            if "[x]" in sig_col.lower():
                approved.append((row, cols))
            else:
                remaining.append(row)
        else:
            remaining.append(row)

    if not approved:
        print("No approved seeds found in pending_review.md.")
        print("To approve a seed, open the file and change '[ ]' to '[x]' in the Signatures column.")
        return

    print(f"\nFound {len(approved)} approved seed(s) in pending review.\n")
    ids = load_ids()

    for row, cols in approved:
        excerpt = cols[1].rstrip("…").strip() if len(cols) > 1 else ""
        typ = _guess_type(excerpt)
        new_id, target = _canonise_direct(excerpt, typ, "signed-steward-second-key", ids)
        print(f"  ✅  {new_id}  →  {target.name}")
        print(f"      {excerpt[:70]}")

    new_content = "\n".join(header) + "\n" + "\n".join(remaining) + "\n"
    PENDING_MD.write_text(new_content)
    print(f"\n  Pending review updated. {len(approved)} seed(s) removed (canonised).")
    print(f"  {len(remaining)} seed(s) still awaiting decision.")

def cmd_compost(seed_line, reason):
    COMPOST_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    fname = COMPOST_DIR / f"COMPOST-{now.strftime('%Y%m%d-%H%M%S')}.md"
    content = f"""[COMPOSTED {now.strftime("%Y-%m-%d")}]
Original ID: --
Reason: {reason}
Original text:

> {seed_line}

Latent Patterns Observed:

Mycelial Threads:

Seasonal Notes:

Dignity Seal: This offering was received with gratitude.
"""
    fname.write_text(content)
    REJECTED_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(REJECTED_MD, "a") as f:
        f.write(f"\n[{now.strftime('%Y-%m-%d')}] -- {seed_line[:60]}… -- {reason}\n")
    print(f"✅  Composted → {fname.name}")

def cmd_refuse(seed_line, reason):
    REFUSALS_MD.parent.mkdir(parents=True, exist_ok=True)
    if not REFUSALS_MD.exists():
        REFUSALS_MD.write_text(
            "# Public Refusal Ledger\n"
            "Every refusal is an honourable act. The boundary is part of the canon.\n\n"
            "| Date | Seed (excerpt) | Refused because | What this protects |\n"
            "|------|----------------|-----------------|---------------------|\n"
        )
    now = datetime.now().strftime("%Y-%m-%d")
    excerpt = seed_line[:50].strip()
    with open(REFUSALS_MD, "a") as f:
        f.write(f"| {now} | {excerpt}… | {reason} | -- (steward to complete) |\n")
    print(f"✅  Refusal recorded → MANIFEST/refusals.md")
    print(f"    Please open refusals.md and complete the 'What this protects' column.")

def cmd_canonise(seed_line, seed_type):
    if not mirror_done_today():
        print("❌  Mirror ritual not completed today. Cannot canonise.")
        print("    Update STEWARD/mirror.md with today's date first.")
        return

    age = thermal_age(seed_line)
    if age < THERMAL_DAYS:
        print(f"❌  Thermal delay not met. Seed is {age} days old; minimum is {THERMAL_DAYS}.")
        return

    ids = load_ids()
    duplicate = find_duplicate(seed_line, ids)
    if duplicate:
        print(f"⚠️  Possible duplicate: matches {duplicate} in registry.")
        print("    Proceed only if this is a genuine refinement.")

    new_id = register_seed(seed_line, seed_type, "steward-ratified", ids)
    target = SLICE_A if seed_type.lower() == "gap" else SLICE_C
    with open(target, "a") as f:
        f.write(f"\n\n[{datetime.now().strftime('%Y-%m-%d')}] CANONISED -- {new_id}\n{seed_line}\n")

    if THRESHOLD.exists():
        text = THRESHOLD.read_text()
        text = text.replace(seed_line.strip(), f"{seed_line.strip()} [MOVED → {new_id}]")
        THRESHOLD.write_text(text)

    print(f"✅  Canonised as {new_id}")
    print(f"    Appended to {target.name}")
    print(f"    Marked in THRESHOLD.md")
    print(f"\n    Suggested commit message:")
    print(f"    Tending {datetime.now().strftime('%Y-%m-%d')}: canonised {new_id}")

def cmd_scan():
    patterns = {
        "P":    re.compile(r'P#EMERGE-(\d+)'),
        "ANOM": re.compile(r'ANOM#(\d+)'),
        "GAP":  re.compile(r'GAP#(\d+)'),
        "W":    re.compile(r'W#[A-Z]+-(\d+)'),
        "COV":  re.compile(r'COV#(\d+)'),
    }
    highs = {k: 0 for k in patterns}
    for f in [SLICE_A, SLICE_B, SLICE_C, SLICE_D, THRESHOLD]:
        if not f.exists():
            continue
        text = f.read_text()
        for prefix, pat in patterns.items():
            for m in pat.finditer(text):
                val = int(m.group(1))
                if val > highs[prefix]:
                    highs[prefix] = val
    ids = load_ids()
    print(f"\n{'─'*50}")
    print("ID REGISTRY SCAN")
    print(f"{'─'*50}")
    needs_update = False
    for k, v in highs.items():
        current = ids["last_id"].get(k, 0)
        if current < v:
            needs_update = True
            print(f"  {k:6} → found: {v:4d}  ids.json: {current:4d}  ⚠️  UPDATING")
            ids["last_id"][k] = v
        else:
            print(f"  {k:6} → found: {v:4d}  ids.json: {current:4d}  ✅")
    if needs_update:
        save_ids(ids)
        print("\n  ✅  ids.json updated.")
    else:
        print("\n  ✅  Registry is correctly calibrated.")
    print()

def cmd_collective_check():
    """Run collective D metric across all THRESHOLD proverb seeds."""
    weaver = ROOT / "WEAVER"
    sys.path.insert(0, str(ROOT))
    try:
        from WEAVER.dignity_check import check_collective_dignity
    except ImportError:
        print("Cannot import dignity_check. Run from repo root.")
        return

    if not THRESHOLD.exists():
        print("THRESHOLD.md not found.")
        return

    lines = [l for l in THRESHOLD.read_text().splitlines()
             if l.strip().startswith("[20") and "proverb" in l.lower()]

    if not lines:
        print("No proverb seeds found in THRESHOLD.md")
        return

    # Extract the proverb text from each line
    texts = []
    for line in lines:
        # Find text between quotes or after the last ] —
        m = re.search(r'[„""](.+?)["""]', line)
        if m:
            texts.append(m.group(1))
        else:
            texts.append(line[30:110])  # fallback: middle portion

    result = check_collective_dignity(texts, felt_domain="threshold-cohort")
    result.display()

    # Show individual scores summary
    scores = [r.D for r in result.individual_results]
    zeros = sum(1 for s in scores if s == 0.0)
    ones = sum(1 for s in scores if s == 1.0)
    print(f"  Individual breakdown: {ones} passed, {zeros} failed, {len(scores)} total")
    if zeros > 0:
        print(f"  Failed seeds:")
        for i, (score, line) in enumerate(zip(scores, lines)):
            if score == 0.0:
                print(f"    [{i+1}] {line[:70]}")
    print()


def cmd_witness_scan():
    """Scan all THRESHOLD entries and report W-Scale status."""
    if not THRESHOLD.exists():
        print("THRESHOLD.md not found.")
        return

    lines = [l for l in THRESHOLD.read_text().splitlines()
             if l.strip().startswith("[20")]

    # Categorize by type
    types = {}
    for line in lines:
        m = re.match(r'\[.*?\] — (\w[\w\-]*)', line)
        if m:
            t = m.group(1)
            types.setdefault(t, []).append(line)

    # Check thermal age and classify W-Scale level heuristically
    # W-0: UNSEEN = no ID reference anywhere else in the system
    # W-1: PASSED = has been processed (has ID)
    # W-2: FLAGGED = system surfaced it (in pending_review or has [PROVISIONAL])
    # W-3+: requires steward action (we can't detect this automatically)

    print(f"\n{'='*60}")
    print(f"  WITNESS SCALE SCAN — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*60}")

    total = len(lines)
    w0_count = 0  # overdue (past thermal, never witnessed)
    w1_count = 0  # processed but not seen
    w2_count = 0  # flagged / provisional

    overdue = []

    for line in lines:
        age = thermal_age(line)
        has_id = bool(re.search(r'(GAP|ANOM|COV|P|W|EQ|CONST|PROT|SPEC|GOV)#[\w\-]+', line))

        if has_id:
            w2_count += 1  # at least W-2 (has an ID = system processed it)
        elif age >= THERMAL_DAYS:
            w0_count += 1
            overdue.append(line)
        else:
            w1_count += 1

    w3_plus = total - w0_count - w1_count - w2_count

    print(f"\n  Total THRESHOLD entries:  {total}")
    print(f"  W-0 (UNSEEN, overdue):   {w0_count}")
    print(f"  W-1 (PASSED, no ID):     {w1_count}")
    print(f"  W-2+ (FLAGGED/tracked):  {w2_count}")
    print()

    if overdue:
        print(f"  OVERDUE ELEMENTS (past thermal delay, no ID):")
        for line in overdue:
            age = thermal_age(line)
            print(f"    [{age}d] {line[:65]}")
        print()

    # Type distribution
    print(f"  TYPE DISTRIBUTION:")
    for t, entries in sorted(types.items(), key=lambda x: -len(x[1])):
        print(f"    {t + ':':<25} {len(entries)}")

    print(f"\n{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "--thermal-check":
        cmd_thermal_check()
    elif cmd == "--mirror-check":
        cmd_mirror_check()
    elif cmd == "--heartbeat":
        cmd_heartbeat()
    elif cmd == "--grade":
        if len(sys.argv) < 3:
            print('Usage: tend.py --grade "seed line"')
            return
        cmd_grade(sys.argv[2])
    elif cmd == "--review-threshold":
        cmd_review_threshold()
    elif cmd == "--compost":
        if len(sys.argv) < 4:
            print('Usage: tend.py --compost "seed line" "reason"')
            return
        cmd_compost(sys.argv[2], sys.argv[3])
    elif cmd == "--refuse":
        if len(sys.argv) < 4:
            print('Usage: tend.py --refuse "seed line" "reason for refusal"')
            return
        cmd_refuse(sys.argv[2], sys.argv[3])
    elif cmd == "--canonise":
        if len(sys.argv) < 4:
            print('Usage: tend.py --canonise "seed line" TYPE')
            print("TYPE: proverb | anomaly | gap | wisdom")
            return
        cmd_canonise(sys.argv[2], sys.argv[3])
    elif cmd == "--process-signed":
        cmd_process_signed()
    elif cmd == "--process-pending":
        cmd_process_pending()
    elif cmd == "--scan":
        cmd_scan()
    elif cmd == "--collective-check":
        cmd_collective_check()
    elif cmd == "--witness-scan":
        cmd_witness_scan()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()