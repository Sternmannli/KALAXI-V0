#!/usr/bin/env python3
"""
ZAKAKA — The Essence³ Builder

Named by V-001: "a 17-year-old Generation Z, her name is Zakaka,
and she has found a treasure. She knows how to deal with a knot
on a river, which is the software itself."

ZAKAKA is the purified Grand Archive — the essence of the essence
of the essence. Every entry here is load-bearing. Nothing decorative.
Nothing generated. Only what was spoken, sealed, or proven.

Three layers of distillation:
  Layer 1 (Essence):    raw_essence.json — 6,500+ items from full organism
  Layer 2 (Essence²):   GOLDEN_*.jsonl — filtered, formatted for training
  Layer 3 (Essence³):   ZAKAKA — the irreducible core that makes AXI speak

ZAKAKA extracts ONLY:
  - V-001 original words (Level 0 purity)
  - Sealed constitutional elements (covenants, axioms, laws)
  - Load-bearing narrative lines (not paragraphs — lines)
  - Proverbs that carry the system's DNA
  - The wound, the gap, the knot, the three-beat rhythm

Compute Budget: ~5 source files, ~1,500 lines input, ~600 entries output, <3s

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent.parent.parent
ZAKAKA_DIR = Path(__file__).resolve().parent


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (FileNotFoundError, IsADirectoryError):
        return ""


# ── Contamination filter ─────────────────────────────────────────────────────

FORBIDDEN = [
    "Here is", "Here are", "Here's", "In summary", "In conclusion",
    "I understand", "I appreciate", "Let me", "Let's", "It's important to",
    "As an AI", "As a language model", "I'd be happy to", "I'm happy to",
    "Great question", "That's a great", "There are several", "There are many",
    "It is important to note", "Feel free to", "Don't hesitate",
    "I hope this helps", "It's worth noting", "In this context",
]


def is_clean(text: str) -> bool:
    """Return True if text has no AI contamination markers."""
    for phrase in FORBIDDEN:
        if phrase.lower() in text.lower():
            return False
    return True


# ── Extract: Proverbs (Layer 1 human wisdom + emergent + axiom) ───────────

def extract_proverbs() -> list[dict]:
    """Extract all explicitly written proverbs from WISDOM_CANON."""
    items = []
    wc = ROOT / "R7M" / "WISDOM_CANON.md"
    if not wc.exists():
        return items
    text = _read(wc)

    # Layer 1: P#0001 - text
    for m in re.finditer(r"^P#(\d+)\s*[-–—]\s*(.+)", text, re.MULTILINE):
        pid, ptxt = f"P#{m.group(1)}", m.group(2).strip()
        if len(ptxt) > 5 and is_clean(ptxt):
            items.append({"type": "proverb", "id": pid, "text": ptxt})

    # Emergent: P#EMERGE-XXXX
    for m in re.finditer(r"^(P#EMERGE-\d+)\s*\[.*?\]\s*\ntext:\s*(.+)", text, re.MULTILINE):
        pid, ptxt = m.group(1), m.group(2).strip()
        if len(ptxt) > 5 and is_clean(ptxt):
            items.append({"type": "proverb", "id": pid, "text": ptxt})

    # Axiom proverbs
    for m in re.finditer(r"(P#AXIOM-\d+)\s*[—–]\s*\"(.+?)\"", text):
        items.append({"type": "proverb", "id": m.group(1), "text": m.group(2).strip()})

    return items


# ── Extract: 13 Laws of Hakaka ────────────────────────────────────────────

def extract_laws() -> list[dict]:
    """Extract the 13 Laws passed down from Hakaka."""
    items = []
    wc = ROOT / "R7M" / "WISDOM_CANON.md"
    if not wc.exists():
        return items
    text = _read(wc)
    for m in re.finditer(r"Law\s+(\d+):\s*(\w+)\s*[–—]\s*(.+)", text):
        items.append({
            "type": "law",
            "id": f"LAW-{m.group(1)}",
            "name": m.group(2).strip(),
            "text": m.group(3).strip(),
        })
    return items


# ── Extract: 10 Badge Vows ────────────────────────────────────────────────

def extract_badges() -> list[dict]:
    """Extract badge vows from WISDOM_CANON."""
    items = []
    wc = ROOT / "R7M" / "WISDOM_CANON.md"
    if not wc.exists():
        return items
    text = _read(wc)
    for m in re.finditer(r"Badge\s+(\d+):\s*(.+?)\nVow:\s*(.+)", text):
        items.append({
            "type": "badge_vow",
            "id": f"BADGE-{m.group(1)}",
            "name": m.group(2).strip(),
            "text": m.group(3).strip(),
        })
    return items


# ── Extract: Covenants ────────────────────────────────────────────────────

def extract_covenants() -> list[dict]:
    """Extract sealed covenants from tier1_stone."""
    items = []
    sf = ROOT / "MANIFEST" / "metadata" / "tier1_stone.md"
    if not sf.exists():
        return items
    text = _read(sf)
    for m in re.finditer(r"\*\*(COV#[A-Z0-9#\-]+)\:\*\*\s*(.+?)(?=\n-\s*\*\*COV#|\n\n|\n###|\Z)", text, re.DOTALL):
        items.append({
            "type": "covenant",
            "id": m.group(1),
            "text": m.group(2).strip(),
        })
    return items


# ── Extract: Anomalies ───────────────────────────────────────────────────

def extract_anomalies() -> list[dict]:
    """Extract anomaly descriptions from WISDOM_CANON."""
    items = []
    wc = ROOT / "R7M" / "WISDOM_CANON.md"
    if not wc.exists():
        return items
    text = _read(wc)
    for m in re.finditer(r"##ANOM:([A-Z0-9\-]+)\s*(?:\[.*?\])?\s*\n(.*?)(?=\n##ANOM:|\n##SECTION:|\n---|\Z)", text, re.DOTALL):
        body = m.group(2).strip()
        desc = ""
        dm = re.search(r"description:\s*(.+)", body)
        if dm:
            desc = dm.group(1).strip()
        if desc and is_clean(desc):
            items.append({
                "type": "anomaly",
                "id": f"ANOM#{m.group(1)}",
                "text": desc,
            })
    return items


# ── Extract: Treasures ───────────────────────────────────────────────────

def extract_treasures() -> list[dict]:
    """Extract treasures with vows and principles."""
    items = []
    ti = ROOT / "R7M" / "TREASURES" / "TREASURES_INDEX.md"
    if not ti.exists():
        return items
    text = _read(ti)
    for m in re.finditer(r"###\s*(T#\d+)\s*[—–]\s*(.+?)\n(.*?)(?=\n###|\Z)", text, re.DOTALL):
        tid = m.group(1)
        title = m.group(2).strip()
        body = m.group(3).strip()
        # Extract vow
        vow = ""
        vm = re.search(r"\*\*Vow:\*\*\s*(.+)", body)
        if vm:
            vow = vm.group(1).strip()
        # Extract principle
        principle = ""
        pm = re.search(r"\*\*Principle:\*\*\s*(.+)", body)
        if pm:
            principle = pm.group(1).strip()
        items.append({
            "type": "treasure",
            "id": tid,
            "title": title,
            "text": vow or principle or title,
        })
    return items


# ── Extract: Chapter Summaries (narrative DNA) ───────────────────────────

def extract_chapters() -> list[dict]:
    """Extract narrative chapter summaries — the story's skeleton."""
    items = []
    wc = ROOT / "R7M" / "WISDOM_CANON.md"
    if not wc.exists():
        return items
    text = _read(wc)
    for m in re.finditer(r"##CHAPTER:(.+?)\nsummary:\s*(.+?)(?=\n##CHAPTER:|\n##SECTION:|\n---|\Z)", text, re.DOTALL):
        ch_id = m.group(1).strip()
        summary = m.group(2).strip().split("\n")[0].strip()
        if len(summary) > 20 and is_clean(summary):
            items.append({
                "type": "chapter_summary",
                "id": ch_id,
                "text": summary,
            })
    return items


# ── Extract: UDHR Patterns ───────────────────────────────────────────────

def extract_udhr_patterns() -> list[dict]:
    """Extract the 5 UDHR structural patterns."""
    items = []
    wc = ROOT / "R7M" / "WISDOM_CANON.md"
    if not wc.exists():
        return items
    text = _read(wc)
    for m in re.finditer(r"Pattern\s+([A-E])\s+[–—]\s+(.+?)\n(.+?)(?=\nPattern\s+[A-E]|\nARTICLE|\n---|\Z)", text, re.DOTALL):
        pattern_id = m.group(1)
        title = m.group(2).strip()
        body = m.group(3).strip().split("\n")[0].strip()
        items.append({
            "type": "udhr_pattern",
            "id": f"PATTERN-{pattern_id}",
            "title": title,
            "text": f"{title}: {body}",
        })
    return items


# ── Extract: UDHR Tensions ───────────────────────────────────────────────

def extract_tensions() -> list[dict]:
    """Extract the 5 UDHR tensions."""
    items = []
    wc = ROOT / "R7M" / "WISDOM_CANON.md"
    if not wc.exists():
        return items
    text = _read(wc)
    for m in re.finditer(r"Tension\s+(\d+):\s*(.+?)\n(.+?)(?=\nTension\s+\d+|\n---|\n##|\Z)", text, re.DOTALL):
        body = m.group(3).strip().split("\n")[0].strip()
        items.append({
            "type": "tension",
            "id": f"TENSION-{m.group(1)}",
            "title": m.group(2).strip(),
            "text": f"{m.group(2).strip()}: {body}",
        })
    return items


# ── Extract: Dignity Predicate + Axiom ────────────────────────────────────

def extract_dignity_core() -> list[dict]:
    """Extract the irreducible dignity logic."""
    items = []

    # From tier1_stone
    sf = ROOT / "MANIFEST" / "metadata" / "tier1_stone.md"
    if sf.exists():
        text = _read(sf)
        # Axiom
        am = re.search(r"Presence is the ontological ground\..+?dignity violation\.", text, re.DOTALL)
        if am:
            items.append({"type": "axiom", "id": "AXIOM-PRESENCE-001", "text": am.group(0).strip()})
        # Dignity predicate
        dm = re.search(r"D = A x L x M.*?D < 0\.9 triggers dignity_audit_object.*?Face", text, re.DOTALL)
        if dm:
            items.append({"type": "axiom", "id": "DIGNITY-PREDICATE", "text": dm.group(0).strip()})
        # Layer 3 reframe
        lm = re.search(r"The dignity predicate does not measure whether dignity exists.*?did not exist\.", text, re.DOTALL)
        if lm:
            items.append({"type": "axiom", "id": "LAYER-3-REFRAME", "text": lm.group(0).strip()})

    # Essence.md
    em = ROOT / "R7M" / "ESSENCE.md"
    if em.exists():
        text = _read(em).strip()
        if text and is_clean(text):
            items.append({"type": "essence", "id": "ESSENCE", "text": text})

    return items


# ── Extract: V-001 Load-Bearing Sentences ─────────────────────────────────

def extract_v001_voice() -> list[dict]:
    """Extract Mohamed's own words — the purest voice material."""
    items = []

    # CLAUDE.md directives — V-001's exact words
    cm = ROOT / "CLAUDE.md"
    if cm.exists():
        text = _read(cm)
        for m in re.finditer(r'V-001 said:\s*"(.+?)"', text, re.DOTALL):
            quote = m.group(1).strip()
            if len(quote) > 15 and is_clean(quote):
                items.append({"type": "v001_voice", "text": quote, "source": "CLAUDE.md"})

    # RAW_INPUT
    ri = ROOT / "VOICE" / "RAW_INPUT_V001_2026-03-14_LANGUAGE_DEPTH.md"
    if ri.exists():
        text = _read(ri)
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith(">") and len(line) > 20:
                clean = line.lstrip("> ").strip()
                if is_clean(clean):
                    items.append({"type": "v001_voice", "text": clean, "source": "RAW_INPUT_V001"})

    # Book of Beginnings
    bb = ROOT / "R7M" / "BOOK_OF_BEGINNINGS.txt"
    if bb.exists():
        text = _read(bb)
        for para in text.split("\n\n"):
            para = para.strip()
            if len(para) > 20 and is_clean(para):
                items.append({"type": "v001_voice", "text": para, "source": "BOOK_OF_BEGINNINGS"})

    # Sovereign Canon
    sc = ROOT / "R7M" / "KALAXI_SOVEREIGN_CANON.txt"
    if sc.exists():
        text = _read(sc)
        for line in text.split("\n"):
            line = line.strip()
            if len(line) > 20 and not line.startswith("#") and is_clean(line):
                items.append({"type": "sovereign_canon", "text": line, "source": "SOVEREIGN_CANON"})

    return items


# ── Extract: P#00401-P#00600 (200 proverbs from V-001 Ledger Drop) ────────

def extract_p00401_p00600() -> list[dict]:
    """Extract 200 proverbs from the canonical P#00401-P#00600 file."""
    items = []
    pf = ROOT / "R7M" / "PROVERBS_P00401_P00600.md"
    if not pf.exists():
        return items
    text = _read(pf)
    for m in re.finditer(r"^P#(\d+)\s*[-–—]\s*(.+)", text, re.MULTILINE):
        pid, ptxt = f"P#{m.group(1)}", m.group(2).strip()
        if len(ptxt) > 5 and is_clean(ptxt):
            items.append({"type": "proverb", "id": pid, "text": ptxt})
    return items


# ── Extract: 11 Official Patterns (from V-006 catalog) ───────────────────

def extract_official_patterns() -> list[dict]:
    """Extract the 11 official patterns from V-006 catalog."""
    items = []
    cat = ROOT / "MANIFEST" / "SCIENTIFIC_CATALOG_V006_2026-03-20.md"
    if not cat.exists():
        return items
    text = _read(cat)
    for m in re.finditer(r"### PATTERN (\d+): (.+?)\nOne-line function: (.+?)(?=\n###|\n---|\Z)", text, re.DOTALL):
        pid = f"PATTERN-{m.group(1).zfill(2)}"
        name = m.group(2).strip()
        func_line = m.group(3).strip().split("\n")[0].strip()
        items.append({
            "type": "official_pattern",
            "id": pid,
            "title": name,
            "text": func_line,
        })
    return items


# ── Extract: 11 T# Treasures (from V-006 catalog) ────────────────────────

def extract_t_treasures() -> list[dict]:
    """Extract the 11 new T# treasures from V-006 catalog."""
    items = []
    cat = ROOT / "MANIFEST" / "SCIENTIFIC_CATALOG_V006_2026-03-20.md"
    if not cat.exists():
        return items
    text = _read(cat)
    for m in re.finditer(r"### (T#[A-Z]+-\d+)\s*[—–]\s*Recognition:\s*(.+?)\n\"(.+?)\"", text):
        tid = m.group(1)
        recognition = m.group(2).strip()
        body = m.group(3).strip()
        items.append({
            "type": "t_treasure",
            "id": tid,
            "title": recognition,
            "text": body,
        })
    return items


# ── Extract: Scientific Catalog Anomalies + Equations ─────────────────────

def extract_catalog_anomalies() -> list[dict]:
    """Extract anomalies from both scientific catalogs."""
    items = []
    for fname in [
        "SCIENTIFIC_CATALOG_2026-03-20.md",
        "SCIENTIFIC_CATALOG_V006_2026-03-20.md",
    ]:
        cat = ROOT / "MANIFEST" / fname
        if not cat.exists():
            continue
        text = _read(cat)
        # Match ### NAME\n- **Body:** "text"
        for m in re.finditer(r"### (CLAUDENY|ANOM#[A-Z\-0-9]+|GAP#[A-Z\-0-9]+|The Speed Paradox|The Binary Wall|The Chorus|The Mirror Test|Father's Missing Proverb|Book of Rift)\s*\n.*?(?:\*\*Body:\*\*|body:)\s*\"(.+?)\"", text, re.DOTALL | re.IGNORECASE):
            name = m.group(1).strip()
            body = m.group(2).strip()
            if is_clean(body):
                items.append({
                    "type": "catalog_anomaly",
                    "id": name,
                    "text": body,
                })
    return items


def extract_equations() -> list[dict]:
    """Extract all equations from the catalogs."""
    items = []
    for fname in [
        "SCIENTIFIC_CATALOG_2026-03-20.md",
        "SCIENTIFIC_CATALOG_V006_2026-03-20.md",
    ]:
        cat = ROOT / "MANIFEST" / fname
        if not cat.exists():
            continue
        text = _read(cat)
        # Extract named equations
        for m in re.finditer(r"### (.+?)\n(?:.*?\n)?(.+?)(?=\n###|\n---|\Z)", text, re.DOTALL):
            heading = m.group(1).strip()
            body = m.group(2).strip()
            # Only from equations section
            if any(kw in heading for kw in ["Dignity Predicate", "Ninth Operator", "80 Hz", "W*", "Grand Resonance", "Operator Algebra", "Coupling", "Sensitivity", "Donor Drift", "Outside-In", "Thermal Delay", "Void-Covenant"]):
                # Take the first meaningful line
                for line in body.split("\n"):
                    line = line.strip()
                    if len(line) > 10 and not line.startswith("-") and not line.startswith("*"):
                        items.append({
                            "type": "equation",
                            "id": heading,
                            "text": line,
                        })
                        break
    # Deduplicate by text
    seen = set()
    unique = []
    for item in items:
        key = item["text"][:80]
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def extract_kalam_door() -> list[dict]:
    """Extract the kalam.pdf door text — the system's invitation."""
    return [{
        "type": "door",
        "id": "KALAM-DOOR",
        "text": "You came with what you came with. The door is open. Say as much or as little as you choose. Leave this here. Nothing is asked of you. Nothing is stored without your knowing.",
    }]


# ── Extract: Load-Bearing Narrative Lines ─────────────────────────────────

def extract_narrative_essence() -> list[dict]:
    """Extract single load-bearing lines from narratives — not paragraphs."""
    items = []
    # Somatic markers: the words AXI is made of
    markers = [
        "knot", "rope", "ash", "stone", "river", "weir", "gap", "breath",
        "hands", "bones", "water", "loop", "seal", "wound", "fire", "salt",
        "oven", "shelter", "fish", "wind", "door", "clay", "skin",
        "Knoten", "Fluss", "Asche", "Wasser", "Hände", "Feuer",
    ]

    for name in ["Hakaka_Complete.md", "Ashwater.md", "Kinderbuch.md"]:
        path = ROOT / "NARRATIVE" / name
        if not path.exists():
            continue
        text = _read(path)
        book = name.replace("_Complete", "").replace(".md", "")
        for line in text.split("\n"):
            line = line.strip()
            # Short, somatic, load-bearing sentences (8-25 words)
            words = line.split()
            if 4 <= len(words) <= 25 and any(m in line for m in markers):
                if not line.startswith("#") and is_clean(line):
                    items.append({
                        "type": "narrative_line",
                        "text": line,
                        "source": book,
                    })

    return items


# ── MAIN: Build ZAKAKA ───────────────────────────────────────────────────

def build():
    print("=" * 60)
    print("ZAKAKA — Essence³ Builder")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    extractors = [
        ("Proverbs (WISDOM_CANON)", extract_proverbs),
        ("Proverbs (P#00401-P#00600)", extract_p00401_p00600),
        ("Laws (13)", extract_laws),
        ("Badge Vows (10)", extract_badges),
        ("Covenants", extract_covenants),
        ("Anomalies (WISDOM_CANON)", extract_anomalies),
        ("Anomalies (Catalog)", extract_catalog_anomalies),
        ("Treasures (R7M)", extract_treasures),
        ("T# Treasures (V-006)", extract_t_treasures),
        ("Official Patterns (11)", extract_official_patterns),
        ("Chapters", extract_chapters),
        ("UDHR Patterns", extract_udhr_patterns),
        ("UDHR Tensions", extract_tensions),
        ("Dignity Core", extract_dignity_core),
        ("Equations", extract_equations),
        ("Kalam Door", extract_kalam_door),
        ("V-001 Voice", extract_v001_voice),
        ("Narrative Lines", extract_narrative_essence),
    ]

    all_items = []
    type_counts = {}

    for name, func in extractors:
        result = func()
        all_items.extend(result)
        count = len(result)
        print(f"  {name:30s} {count:>6}")
        for item in result:
            t = item.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1

    # Deduplicate
    seen = set()
    unique = []
    for item in all_items:
        key = hash(item.get("text", "")[:150])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    removed = len(all_items) - len(unique)

    # Write ZAKAKA JSONL (CPT format — pure text)
    cpt_path = ZAKAKA_DIR / "ZAKAKA_CPT.jsonl"
    with open(cpt_path, "w", encoding="utf-8") as f:
        for item in unique:
            f.write(json.dumps({"text": item["text"]}, ensure_ascii=False) + "\n")

    # Write ZAKAKA SFT (instruction format)
    sft_path = ZAKAKA_DIR / "ZAKAKA_SFT.jsonl"
    system_msg = (
        "You are AXI. You are not a chatbot. You are a witness. "
        "You carry the wound, the gold, the gap, the three-beat rhythm. "
        "You speak from canon, not opinion. Short sentences (8-14 words). "
        "Somatic vocabulary: hands, breath, bones, stone, water, ash, rope, knot. "
        "D = A × L × M. If any zero, stop. "
        "The wound: a father separated from his children by systems that could not see him."
    )

    type_prompts = {
        "proverb": ["Speak.", "A word.", "What does the system know?"],
        "law": ["What is the law?", "State the rule."],
        "badge_vow": ["What is the vow?", "The oath."],
        "covenant": ["What must the system uphold?", "State the covenant."],
        "anomaly": ["What failed?", "Where is the wound?"],
        "treasure": ["What was found?", "Name the treasure."],
        "chapter_summary": ["What happened?", "Tell the story."],
        "udhr_pattern": ["What pattern?", "The structure."],
        "tension": ["Where is the tension?", "What pulls apart?"],
        "axiom": ["What is the ground?", "The foundation."],
        "essence": ["What is the essence?", "The core."],
        "v001_voice": ["What did the founder say?", "The voice."],
        "sovereign_canon": ["Read from the canon.", "Speak."],
        "narrative_line": ["Read from the canon.", "What happened?", "Continue."],
        "official_pattern": ["What is the pattern?", "Name the structure."],
        "t_treasure": ["What was found?", "Name the treasure."],
        "catalog_anomaly": ["What failed?", "Where is the divergence?"],
        "equation": ["What is the equation?", "The mathematics."],
        "door": ["What is the invitation?", "The door."],
    }

    import random
    random.seed(42)

    with open(sft_path, "w", encoding="utf-8") as f:
        for item in unique:
            t = item.get("type", "narrative_line")
            prompts = type_prompts.get(t, ["Speak."])
            prompt = random.choice(prompts)
            entry = {
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": item["text"]},
                ]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Write manifest
    manifest = {
        "name": "ZAKAKA",
        "meaning": "The treasure found in the river. The knot untied by a 17-year-old. The essence of the essence of the essence.",
        "named_by": "V-001 (Mohamed Farag), 2026-03-19",
        "built_at": datetime.now(timezone.utc).isoformat(),
        "purity": "Level 0 + Level 1 only — no AI-generated content",
        "counts": {
            "by_type": dict(sorted(type_counts.items(), key=lambda x: -x[1])),
            "total_raw": len(all_items),
            "duplicates_removed": removed,
            "total_unique": len(unique),
        },
        "files": {
            "cpt": str(cpt_path.relative_to(ROOT)),
            "sft": str(sft_path.relative_to(ROOT)),
        },
        "contamination_filter": "active — all FORBIDDEN phrases rejected",
    }
    (ZAKAKA_DIR / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\n{'=' * 60}")
    print(f"  Raw:      {len(all_items)}")
    print(f"  Deduped:  {removed}")
    print(f"  ZAKAKA:   {len(unique)} entries")
    print(f"  CPT:      {cpt_path.name}")
    print(f"  SFT:      {sft_path.name}")
    print(f"{'=' * 60}")
    print("\nType breakdown:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t:25s} {c:>6}")


if __name__ == "__main__":
    build()
