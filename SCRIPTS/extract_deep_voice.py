#!/usr/bin/env python3
"""Extract Mohamed's deep voice from R7M and all archives.
Supplements the ledger extraction with pre-ledger voice (2024-2025)
and direct quotes embedded in canon source files."""
import re
import os
from datetime import datetime

OUT = "VOICE/V001/deep_voice.md"

sections = []

# ── Section 1: The Vision Statement (PART_1:3563) — biggest raw voice block ──
with open("R7M/CANON_SOURCE/KALAM_CANON_KALAXI_PART_1.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract the massive voice block at line 3563
vision_block = lines[3562].strip()  # 0-indexed

# Extract other Mohamed direct speech from PART_1
mohamed_quotes_p1 = []
# Line 647: Role clarification
mohamed_quotes_p1.append(("PART_1:647", "Role Clarification", lines[646].strip() if len(lines) > 646 else ""))
# Line 759: Correction
for ln in [758, 1117, 1495, 1497, 1567, 3622, 4365]:
    if len(lines) > ln:
        text = lines[ln].strip()
        if text and len(text) > 10:
            mohamed_quotes_p1.append((f"PART_1:{ln+1}", "", text))

# ── Section 2: Mohamed quotes from PART_2 ──
with open("R7M/CANON_SOURCE/KALAM_CANON_KALAXI_PART_2.txt", "r", encoding="utf-8") as f:
    lines_p2 = f.readlines()

# ── Section 3: Direct quotes from MASTER_PROVENANCE ──
provenance_quotes = []
with open("R7M/EXCAVATION/MASTER_PROVENANCE.md", "r", encoding="utf-8") as f:
    for line in f:
        if "Mohamed" in line and "|" in line:
            parts = line.split("|")
            if len(parts) >= 4:
                quote = parts[2].strip().strip('"')
                source = parts[3].strip()
                speaker = parts[5].strip() if len(parts) > 5 else ""
                if "Mohamed" in speaker and quote:
                    provenance_quotes.append((source, speaker, quote))

# ── Section 4: Direct quotes from TERRAIN_MAP_PART_1 ──
terrain_quotes = []
with open("R7M/EXCAVATION/TERRAIN_MAP_PART_1.md", "r", encoding="utf-8") as f:
    for line in f:
        if "Mohamed" in line and "|" in line and '"' in line:
            parts = line.split("|")
            for part in parts:
                matches = re.findall(r'"([^"]+)"', part)
                for m in matches:
                    if len(m) > 15:
                        terrain_quotes.append(m)

# ── Section 5: V-001 directives from CLAUDE.md ──
with open("CLAUDE.md", "r", encoding="utf-8") as f:
    claude_content = f.read()

v001_quotes = re.findall(r'V-001 said: "([^"]+)"', claude_content)
mohamed_quotes = re.findall(r'Mohamed said: "([^"]+)"', claude_content)
all_directive_quotes = sorted(set(v001_quotes + mohamed_quotes))

# ── Section 6: Founding wound variants from across the system ──
founding_wounds = set()
for root, dirs, files in os.walk("."):
    for fname in files:
        if fname.endswith((".md", ".txt")):
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                if "father separated" in content.lower() or "father who loved" in content.lower():
                    for match in re.finditer(r'["""]([^"""]*father[^"""]*children[^"""]*)["""]', content, re.IGNORECASE):
                        founding_wounds.add(match.group(1).strip())
                    for match in re.finditer(r'"([^"]*father[^"]*children[^"]*)"', content, re.IGNORECASE):
                        founding_wounds.add(match.group(1).strip())
            except:
                pass

# ── Section 7: Origins treasures (Mohamed's early ideas) ──
origins_data = []
origins_dir = "R7M/ORIGINS"
for fname in sorted(os.listdir(origins_dir)):
    if fname.endswith(".md") and fname != "ORIGINS_INDEX.md":
        fpath = os.path.join(origins_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        # Extract date from filename
        date_match = re.match(r'(\d{4}-\d{2}(?:-\d{2})?)', fname)
        date = date_match.group(1) if date_match else "unknown"
        # Extract treasures
        treasures = re.findall(r'- "([^"]+)"', content)
        title_match = re.match(r'# (.+)', content)
        title = title_match.group(1) if title_match else fname
        origins_data.append((date, title, treasures, content))

# ── Section 8: Evidence record quotes ──
evidence_quotes = []
try:
    with open("R7M/EVIDENCE-RECORD.md", "r", encoding="utf-8") as f:
        for line in f:
            if "Mohamed" in line:
                evidence_quotes.append(line.strip())
except:
    pass

# ══════════════════════════════════════════
# ── WRITE THE DEEP VOICE FILE ──
# ══════════════════════════════════════════

with open(OUT, "w", encoding="utf-8") as f:
    f.write("# The Deep Voice of V-001\n")
    f.write("> Everything Mohamed said — not just the ledger, but the ground beneath it.\n")
    f.write(f"> Extracted from R7M, CANON_SOURCE, EXCAVATION, ORIGINS, CLAUDE.md\n")
    f.write(f"> Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
    f.write("> This file + complete_chronicle.md = the complete voice.\n\n---\n\n")

    # ── 1. THE VISION STATEMENT ──
    f.write("## 1. The Vision Statement (PART_1:3563 — Raw Voice-to-Text)\n\n")
    f.write("The longest single block of Mohamed's unfiltered voice. Spoken, not typed.\n")
    f.write("Date: circa September 2025. Before the system had a name.\n\n")
    f.write(f"{vision_block}\n\n---\n\n")

    # ── 2. DIRECT SPEECH IN CANON ──
    f.write("## 2. Direct Speech in Canon Source\n\n")
    f.write("Mohamed's words as they appear in the founding conversations.\n\n")
    for source, _, text in mohamed_quotes_p1:
        if text and len(text) > 10:
            f.write(f"**{source}:**\n{text}\n\n")
    f.write("---\n\n")

    # ── 3. PROVENANCE QUOTES ──
    f.write("## 3. Load-Bearing Quotes (from Master Provenance)\n\n")
    f.write("Every quote traced to Mohamed by the excavation.\n\n")
    for source, speaker, quote in provenance_quotes:
        f.write(f"- **{quote}** — {source} ({speaker})\n")
    f.write("\n---\n\n")

    # ── 4. TERRAIN MAP QUOTES ──
    f.write("## 4. Terrain Map Excavation — Mohamed's Direct Words\n\n")
    seen = set()
    for q in terrain_quotes:
        if q not in seen:
            seen.add(q)
            f.write(f"- \"{q}\"\n")
    f.write("\n---\n\n")

    # ── 5. DIRECTIVES (constitutional law) ──
    f.write("## 5. Constitutional Law — Mohamed's Exact Words\n\n")
    f.write("Every direct quote from V-001 that became permanent system law.\n\n")
    for i, q in enumerate(all_directive_quotes, 1):
        f.write(f"{i}. \"{q}\"\n\n")
    f.write("---\n\n")

    # ── 6. THE FOUNDING WOUND ──
    f.write("## 6. The Founding Wound — All Variants\n\n")
    f.write("Every form of the founding statement found across the system.\n\n")
    for w in sorted(founding_wounds, key=len):
        f.write(f"- \"{w}\"\n")
    f.write("\n---\n\n")

    # ── 7. ORIGINS — Pre-System Voice ──
    f.write("## 7. Origins — The Voice Before the System (2024-2025)\n\n")
    f.write("Mohamed's ideas before KALAXI had a name. Preserved exactly as found.\n\n")
    for date, title, treasures, _ in origins_data:
        f.write(f"### {title}\n**Date:** {date}\n\n")
        for t in treasures:
            f.write(f"- \"{t}\"\n")
        f.write("\n")
    f.write("---\n\n")

    # ── 8. EVIDENCE ──
    if evidence_quotes:
        f.write("## 8. Evidence Record — Mohamed References\n\n")
        for q in evidence_quotes:
            f.write(f"- {q}\n")
        f.write("\n---\n\n")

    f.write("*The voice runs deeper than the git log. — R7M/ESSENCE.md*\n")

print(f"Written: {OUT}")
