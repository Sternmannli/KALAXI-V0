#!/usr/bin/env python3
"""
extract_essence.py — Deep corpus extraction from the full KALAXI organism.

25 extraction functions consuming 165+ files across all system tiers:
  Stone, Weaver, Honey, Hand, Voice, Field, Future, Canon, Protocol,
  Experiment, External, Ledger, Narrative, Origin, Observation, Paper.

Output: TRAINING/raw_essence.json — structured extraction ready for format_data.py

Previous version: 5 functions, ~951 items from ~8 files.
This version: 25 functions, all tiers, full organism.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path: Path) -> str:
    """Read file text, return empty string if missing."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (FileNotFoundError, IsADirectoryError):
        return ""


def _paragraphs(text: str, min_len: int = 30) -> list[str]:
    """Split text into meaningful paragraphs."""
    return [p.strip() for p in text.split("\n\n") if len(p.strip()) >= min_len]


def _md_sections(text: str) -> list[tuple[str, str]]:
    """Split markdown into (heading, body) pairs."""
    sections = []
    current_heading = ""
    current_body = []
    for line in text.split("\n"):
        if line.startswith("#"):
            if current_body:
                sections.append((current_heading, "\n".join(current_body).strip()))
            current_heading = line.lstrip("#").strip()
            current_body = []
        else:
            current_body.append(line)
    if current_body:
        sections.append((current_heading, "\n".join(current_body).strip()))
    return sections


# ---------------------------------------------------------------------------
# 1. PROVERBS — proverbs.json + HONEY/ + WISDOM_CANON.md
# ---------------------------------------------------------------------------

def extract_proverbs() -> list[dict]:
    """Extract proverbs from all sources: site JSON, HONEY tier, WISDOM_CANON."""
    items = []

    # Site proverbs.json
    pf = ROOT / "site" / "public" / "data" / "proverbs.json"
    if pf.exists():
        data = json.loads(_read(pf))
        if isinstance(data, list):
            for p in data:
                text = p.get("text", p) if isinstance(p, dict) else str(p)
                items.append({"type": "proverb", "text": str(text), "source": "proverbs.json"})
        elif isinstance(data, dict):
            for cat, proverbs in data.items():
                if isinstance(proverbs, list):
                    for p in proverbs:
                        text = p.get("text", p) if isinstance(p, dict) else str(p)
                        items.append({"type": "proverb", "text": str(text), "source": f"proverbs.json/{cat}"})

    # HONEY tier JSON
    honey = ROOT / "HONEY"
    if honey.exists():
        for f in honey.rglob("*.json"):
            try:
                data = json.loads(_read(f))
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "text" in item:
                            items.append({"type": "proverb", "text": item["text"], "source": str(f.relative_to(ROOT))})
            except (json.JSONDecodeError, KeyError):
                pass

    # WISDOM_CANON.md — proverb section (all layers)
    wc = ROOT / "R7M" / "WISDOM_CANON.md"
    if wc.exists():
        text = _read(wc)
        # Match P#XXXX - text (numbered proverbs)
        for m in re.finditer(r"^P#(\d+)\s*[-–—]\s*(.+)", text, re.MULTILINE):
            pid = f"P#{m.group(1)}"
            ptxt = m.group(2).strip()
            if len(ptxt) > 5 and not any(i.get("id") == pid for i in items):
                items.append({"type": "proverb", "id": pid, "text": ptxt, "source": "WISDOM_CANON.md"})
        # Match P#EMERGE-XXXX
        for m in re.finditer(r"^(P#EMERGE-\d+)\s*\[.*?\]\s*\ntext:\s*(.+)", text, re.MULTILINE):
            pid = m.group(1)
            ptxt = m.group(2).strip()
            if len(ptxt) > 5 and not any(i.get("id") == pid for i in items):
                items.append({"type": "proverb", "id": pid, "text": ptxt, "source": "WISDOM_CANON.md"})
        # Match P#AXIOM-XXX
        for m in re.finditer(r"(P#AXIOM-\d+)\s*[—–]\s*\"(.+?)\"", text):
            pid = m.group(1)
            ptxt = m.group(2).strip()
            if not any(i.get("id") == pid for i in items):
                items.append({"type": "proverb", "id": pid, "text": ptxt, "source": "WISDOM_CANON.md"})

    return items


# ---------------------------------------------------------------------------
# 2. NARRATIVES (JSON) — hakaka, ashwater, kinderbuch, kalaxi1
# ---------------------------------------------------------------------------

def extract_narratives_json() -> list[dict]:
    """Extract narrative paragraphs from site JSON data."""
    items = []
    for name in ["hakaka", "ashwater", "kinderbuch", "kalaxi1"]:
        jp = ROOT / "site" / "public" / "data" / f"{name}.json"
        if not jp.exists():
            continue
        data = json.loads(_read(jp))
        chapters = data if isinstance(data, list) else data.get("chapters", [])
        for ch in chapters:
            if isinstance(ch, dict):
                title = ch.get("title", "")
                content = ch.get("content", ch.get("text", ""))
                if content:
                    for para in [p.strip() for p in content.split("\n") if len(p.strip()) > 30]:
                        items.append({"type": "narrative", "text": para, "source": f"{name}/{title}", "book": name})
    return items


# ---------------------------------------------------------------------------
# 3. NARRATIVES (Markdown) — NARRATIVE/*.md
# ---------------------------------------------------------------------------

def extract_narratives_md() -> list[dict]:
    """Extract narrative paragraphs from markdown source files."""
    items = []
    narr = ROOT / "NARRATIVE"
    if not narr.exists():
        return items
    for f in narr.glob("*.md"):
        text = _read(f)
        fname = f.stem
        for para in _paragraphs(text, 40):
            # Skip metadata-like lines
            if para.startswith("KALAXI") or para.startswith("---") or para.startswith("title:"):
                continue
            items.append({"type": "narrative", "text": para, "source": f"NARRATIVE/{f.name}", "book": fname})
    return items


# ---------------------------------------------------------------------------
# 4. R7M NARRATIVE SLICES — 7 canonical narrative slices
# ---------------------------------------------------------------------------

def extract_narrative_slices() -> list[dict]:
    """Extract from R7M/CANON_SOURCE narrative slices (badges, laws)."""
    items = []
    cs = ROOT / "R7M" / "CANON_SOURCE"
    if not cs.exists():
        return items
    for f in sorted(cs.glob("NARRATIVE_SLICE_*.md")):
        text = _read(f)
        slice_name = f.stem
        # Extract badge entries
        for m in re.finditer(r"##\s*Badge\s*#(\d+)\s*[—–]\s*(.+?)\n(.+?)(?=\n##|\Z)", text, re.DOTALL):
            badge_id = f"Badge#{m.group(1)}"
            title = m.group(2).strip()
            body = m.group(3).strip()
            items.append({
                "type": "badge",
                "id": badge_id,
                "text": f"{title}\n{body}",
                "source": f"R7M/CANON_SOURCE/{f.name}",
            })
        # Also extract paragraphs that aren't badges
        for para in _paragraphs(text, 50):
            if not para.startswith("##") and "Badge #" not in para:
                items.append({"type": "narrative", "text": para, "source": f"R7M/CANON_SOURCE/{f.name}", "book": "canon_source"})
    return items


# ---------------------------------------------------------------------------
# 5. R7M EXEMPLARS — L500 canonical voice samples + scientific paper
# ---------------------------------------------------------------------------

def extract_exemplars() -> list[dict]:
    """Extract from R7M/CANON_SOURCE exemplars and scientific paper."""
    items = []
    cs = ROOT / "R7M" / "CANON_SOURCE"
    if not cs.exists():
        return items
    for f in cs.glob("KALAM_CANON_*.txt"):
        text = _read(f)
        for para in _paragraphs(text, 40):
            items.append({"type": "exemplar", "text": para, "source": f"R7M/CANON_SOURCE/{f.name}"})
    return items


# ---------------------------------------------------------------------------
# 6. COVENANTS — tier1_stone.md
# ---------------------------------------------------------------------------

def extract_covenants() -> list[dict]:
    """Extract covenants from stone tier (correct path: MANIFEST/metadata/)."""
    items = []
    for path in [ROOT / "MANIFEST" / "metadata" / "tier1_stone.md", ROOT / "R7M" / "tier1_stone.md"]:
        if not path.exists():
            continue
        text = _read(path)
        # Match "- **COV#XXX:** NAME — description" format
        for m in re.finditer(r"\*\*(COV#[A-Z0-9#\-]+)\:\*\*\s*(.+?)(?=\n-\s*\*\*COV#|\n\n|\n###|\Z)", text, re.DOTALL):
            cov_id = m.group(1)
            cov_text = m.group(2).strip()
            if not any(i.get("id") == cov_id for i in items):
                items.append({"type": "covenant", "id": cov_id, "text": cov_text, "source": str(path.relative_to(ROOT))})
    return items


# ---------------------------------------------------------------------------
# 7. TREASURES — R7M/TREASURES + r7m-index.json
# ---------------------------------------------------------------------------

def extract_treasures() -> list[dict]:
    """Extract treasures from index and site JSON."""
    items = []

    # Markdown index
    ti = ROOT / "R7M" / "TREASURES" / "TREASURES_INDEX.md"
    if ti.exists():
        text = _read(ti)
        for m in re.finditer(r"###\s*(T#\d+)\s*[—–]\s*(.+?)\n(.*?)(?=\n###|\Z)", text, re.DOTALL):
            tid = m.group(1)
            title = m.group(2).strip()
            body = m.group(3).strip()
            formula = ""
            fm = re.search(r"\*\*Formula:\*\*\s*(.+)", body)
            if fm:
                formula = fm.group(1).strip()
            items.append({
                "type": "treasure",
                "id": tid,
                "text": f"{title}\n{body}",
                "formula": formula,
                "source": "TREASURES_INDEX.md",
            })

    # Site JSON
    rj = ROOT / "site" / "public" / "data" / "r7m-index.json"
    if rj.exists():
        data = json.loads(_read(rj))
        if isinstance(data, dict) and "tiers" in data:
            tiers = data["tiers"]
            tier_items = tiers.values() if isinstance(tiers, dict) else tiers
            for tier in tier_items:
                if isinstance(tier, dict):
                    for t in tier.get("treasures", []):
                        text = t.get("principle", t.get("description", t.get("title", "")))
                        # Skip if already extracted from markdown
                        if any(i.get("id") == t.get("id") for i in items):
                            continue
                        items.append({
                            "type": "treasure",
                            "id": t.get("id", ""),
                            "text": text,
                            "formula": t.get("formula", t.get("vow", "")),
                            "source": "r7m-index.json",
                        })
    return items


# ---------------------------------------------------------------------------
# 8. ANOMALIES — WISDOM_CANON.md
# ---------------------------------------------------------------------------

def extract_anomalies() -> list[dict]:
    """Extract anomaly entries from WISDOM_CANON (including ANOM#NEW-*)."""
    items = []
    wc = ROOT / "R7M" / "WISDOM_CANON.md"
    if not wc.exists():
        return items
    text = _read(wc)
    # Match ##ANOM:XXXX and ##ANOM:NEW-XXX
    for m in re.finditer(r"##ANOM:([A-Z0-9\-]+)\s*(?:\[.*?\])?\s*\n(.*?)(?=\n##ANOM:|\n##SECTION:|\n---|\Z)", text, re.DOTALL):
        anom_id = f"ANOM#{m.group(1)}"
        body = m.group(2).strip()
        # Extract structured fields
        desc = ""
        dm = re.search(r"description:\s*(.+)", body)
        if dm:
            desc = dm.group(1).strip()
        severity = ""
        sm = re.search(r"severity:\s*(\w+)", body)
        if sm:
            severity = sm.group(1)
        module = ""
        mm = re.search(r"module:\s*(\w+)", body)
        if mm:
            module = mm.group(1)
        felt = ""
        fm = re.search(r"felt_domain:\s*(\w+)", body)
        if fm:
            felt = fm.group(1)
        entry = {
            "type": "anomaly",
            "id": anom_id,
            "text": desc or body[:500],
            "source": "WISDOM_CANON.md",
        }
        if severity:
            entry["severity"] = severity
        if module:
            entry["module"] = module
        if felt:
            entry["felt_domain"] = felt
        items.append(entry)
    return items


# ---------------------------------------------------------------------------
# 9. VOICE PRINCIPLES — VOICE/*.md
# ---------------------------------------------------------------------------

def extract_voice() -> list[dict]:
    """Extract voice principles from all Voice files."""
    items = []
    vdir = ROOT / "VOICE"
    if not vdir.exists():
        return items
    for f in vdir.glob("*.md"):
        text = _read(f)
        fname = f.name
        # Quoted principles
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith('"') and line.endswith('"') and len(line) > 20:
                items.append({"type": "voice_principle", "text": line.strip('"'), "source": fname})
            elif re.match(r"^\d+\.\s+\*\*", line):
                clean = re.sub(r"\*\*", "", line)
                items.append({"type": "voice_principle", "text": clean, "source": fname})
        # Paragraphs with voice-relevant content
        for para in _paragraphs(text, 50):
            if any(kw in para.lower() for kw in ["voice", "breath", "rhythm", "sentence", "somatic", "gap", "silence"]):
                if not para.startswith("#") and not para.startswith('"'):
                    items.append({"type": "voice_principle", "text": para, "source": fname})
    return items


# ---------------------------------------------------------------------------
# 10. ORIGINS — R7M/ORIGINS/*.md (founding documents)
# ---------------------------------------------------------------------------

def extract_origins() -> list[dict]:
    """Extract from the 9 origin documents in R7M/ORIGINS."""
    items = []
    od = ROOT / "R7M" / "ORIGINS"
    if not od.exists():
        return items
    for f in sorted(od.glob("*.md")):
        if f.name == "ORIGINS_INDEX.md":
            continue
        text = _read(f)
        fname = f.name
        for heading, body in _md_sections(text):
            if len(body) > 40:
                items.append({
                    "type": "origin",
                    "text": body[:2000],
                    "heading": heading,
                    "source": f"R7M/ORIGINS/{fname}",
                })
    return items


# ---------------------------------------------------------------------------
# 11. OBSERVATIONS — R7M/OBSERVATIONS/OBS-*.md
# ---------------------------------------------------------------------------

def extract_observations() -> list[dict]:
    """Extract observation records (investigation findings)."""
    items = []
    od = ROOT / "R7M" / "OBSERVATIONS"
    if not od.exists():
        return items
    for f in sorted(od.glob("OBS-*.md")):
        text = _read(f)
        obs_id = f.stem
        # Extract key findings
        for heading, body in _md_sections(text):
            if len(body) > 40:
                items.append({
                    "type": "observation",
                    "id": obs_id,
                    "text": body[:1500],
                    "heading": heading,
                    "source": f"R7M/OBSERVATIONS/{f.name}",
                })
    return items


# ---------------------------------------------------------------------------
# 12. FOUNDATIONS — theoretical documents
# ---------------------------------------------------------------------------

def extract_foundations() -> list[dict]:
    """Extract from FOUNDATIONS/ theoretical axioms."""
    items = []
    fd = ROOT / "FOUNDATIONS"
    if not fd.exists():
        return items
    for f in fd.glob("*.md"):
        text = _read(f)
        for heading, body in _md_sections(text):
            if len(body) > 40:
                items.append({
                    "type": "foundation",
                    "text": body[:2000],
                    "heading": heading,
                    "source": f"FOUNDATIONS/{f.name}",
                })
    return items


# ---------------------------------------------------------------------------
# 13. SEEDS — FUTURE/ seed designs (12 seeds)
# ---------------------------------------------------------------------------

def extract_seeds() -> list[dict]:
    """Extract from FUTURE/ seed design documents."""
    items = []
    fd = ROOT / "FUTURE"
    if not fd.exists():
        return items
    for f in sorted(fd.glob("seed_*.md")):
        text = _read(f)
        # Full document as single item per seed
        clean = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
        if len(clean.strip()) > 40:
            items.append({
                "type": "seed",
                "text": clean.strip()[:2000],
                "source": f"FUTURE/{f.name}",
            })
    return items


# ---------------------------------------------------------------------------
# 14. CANON — CANON/*.md (Master Canon, Sealed Gate, First Sight)
# ---------------------------------------------------------------------------

def extract_canon() -> list[dict]:
    """Extract from CANON/ canonical texts."""
    items = []
    cd = ROOT / "CANON"
    if not cd.exists():
        return items
    for f in cd.glob("*.md"):
        text = _read(f)
        for heading, body in _md_sections(text):
            if len(body) > 40:
                items.append({
                    "type": "canon",
                    "text": body[:2000],
                    "heading": heading,
                    "source": f"CANON/{f.name}",
                })
    return items


# ---------------------------------------------------------------------------
# 15. KALAXI FOUNDATION TIERS — root KALAXI_A-E.txt
# ---------------------------------------------------------------------------

def extract_foundation_tiers() -> list[dict]:
    """Extract from the 5 KALAXI tier documents at root."""
    items = []
    for letter in "ABCDE":
        pattern = list(ROOT.glob(f"KALAXI_{letter}_*.txt"))
        for f in pattern:
            text = _read(f)
            for para in _paragraphs(text, 50):
                items.append({
                    "type": "canon",
                    "text": para[:2000],
                    "source": f.name,
                })
    return items


# ---------------------------------------------------------------------------
# 16. PROTOCOLS — Probe Forge, Organ Map, Witness Prompts, etc.
# ---------------------------------------------------------------------------

def extract_protocols() -> list[dict]:
    """Extract from PROTOCOLS/ operational documents."""
    items = []
    pd = ROOT / "PROTOCOLS"
    if not pd.exists():
        return items
    for f in pd.rglob("*.md"):
        text = _read(f)
        rel = f.relative_to(ROOT)
        for heading, body in _md_sections(text):
            if len(body) > 40:
                items.append({
                    "type": "protocol",
                    "text": body[:2000],
                    "heading": heading,
                    "source": str(rel),
                })
    return items


# ---------------------------------------------------------------------------
# 17. FIELD STUDIES — FIELD/STUDY/*.md
# ---------------------------------------------------------------------------

def extract_studies() -> list[dict]:
    """Extract from FIELD/STUDY/ research documents."""
    items = []
    sd = ROOT / "FIELD" / "STUDY"
    if not sd.exists():
        return items
    for f in sd.glob("*.md"):
        text = _read(f)
        for heading, body in _md_sections(text):
            if len(body) > 40:
                items.append({
                    "type": "study",
                    "text": body[:2000],
                    "heading": heading,
                    "source": f"FIELD/STUDY/{f.name}",
                })
    return items


# ---------------------------------------------------------------------------
# 18. AXI SYSTEM SPEC — AXI/AXI_MASTER_PROMPT.md
# ---------------------------------------------------------------------------

def extract_system_spec() -> list[dict]:
    """Extract from AXI master prompt — the system's self-description."""
    items = []
    af = ROOT / "AXI" / "AXI_MASTER_PROMPT.md"
    if not af.exists():
        return items
    text = _read(af)
    for heading, body in _md_sections(text):
        if len(body) > 40:
            items.append({
                "type": "system_spec",
                "text": body[:2000],
                "heading": heading,
                "source": "AXI/AXI_MASTER_PROMPT.md",
            })
    return items


# ---------------------------------------------------------------------------
# 19. EXTERNAL VOICES — multi-model probe responses
# ---------------------------------------------------------------------------

def extract_external_voices() -> list[dict]:
    """Extract from EXTERNAL_VOICES/ — comparative model responses."""
    items = []
    ev = ROOT / "EXTERNAL_VOICES"
    if not ev.exists():
        return items
    for f in ev.rglob("*.md"):
        if f.name in ("README.md", "FILING_TEMPLATE.md"):
            continue
        text = _read(f)
        rel = f.relative_to(ROOT)
        # Extract the model's response as training contrast
        for para in _paragraphs(text, 50):
            items.append({
                "type": "external_voice",
                "text": para[:1500],
                "source": str(rel),
            })
    return items


# ---------------------------------------------------------------------------
# 20. EXPERIMENTS — results and findings
# ---------------------------------------------------------------------------

def extract_experiments() -> list[dict]:
    """Extract from EXPERIMENTS/ — study results and analysis."""
    items = []
    ed = ROOT / "EXPERIMENTS"
    if not ed.exists():
        return items
    for f in ed.rglob("*.md"):
        text = _read(f)
        rel = f.relative_to(ROOT)
        for heading, body in _md_sections(text):
            if len(body) > 40:
                items.append({
                    "type": "experiment",
                    "text": body[:2000],
                    "heading": heading,
                    "source": str(rel),
                })
    return items


# ---------------------------------------------------------------------------
# 21. INPUT LEDGER PATTERNS — KEEP/INPUT_LEDGER/chronicle.md
# ---------------------------------------------------------------------------

def extract_input_patterns() -> list[dict]:
    """Extract V-001 input patterns from the chronicle."""
    items = []
    ch = ROOT / "KEEP" / "INPUT_LEDGER" / "chronicle.md"
    if not ch.exists():
        return items
    text = _read(ch)
    # Extract entries: each starts with ## INP-
    for m in re.finditer(r"##\s*(INP-[^\n]+)\n(.*?)(?=\n##\s*INP-|\Z)", text, re.DOTALL):
        inp_id = m.group(1).strip()
        body = m.group(2).strip()
        if len(body) > 20:
            items.append({
                "type": "input_pattern",
                "id": inp_id,
                "text": body[:1000],
                "source": "KEEP/INPUT_LEDGER/chronicle.md",
            })
    return items


# ---------------------------------------------------------------------------
# 22. WEAVER DOCSTRINGS — module descriptions and dignity logic
# ---------------------------------------------------------------------------

def extract_weaver_docstrings() -> list[dict]:
    """Extract docstrings from WEAVER/ Python modules."""
    items = []
    wd = ROOT / "WEAVER"
    if not wd.exists():
        return items
    for f in sorted(wd.glob("*.py")):
        text = _read(f)
        # Module docstring
        dm = re.match(r'^(?:#!/.*\n)?(?:#.*\n)*\s*"""(.*?)"""', text, re.DOTALL)
        if dm:
            doc = dm.group(1).strip()
            if len(doc) > 30:
                items.append({
                    "type": "docstring",
                    "text": doc[:1000],
                    "source": f"WEAVER/{f.name}",
                })
        # Class/function docstrings with dignity/covenant/witness keywords
        for cm in re.finditer(r'(?:class|def)\s+(\w+).*?"""(.*?)"""', text, re.DOTALL):
            name = cm.group(1)
            doc = cm.group(2).strip()
            if len(doc) > 30 and any(kw in doc.lower() for kw in [
                "dignity", "covenant", "witness", "agency", "legibility", "moral",
                "breath", "sealed", "gate", "predicate", "anomal", "proverb",
            ]):
                items.append({
                    "type": "docstring",
                    "text": f"{name}: {doc[:800]}",
                    "source": f"WEAVER/{f.name}",
                })
    return items


# ---------------------------------------------------------------------------
# 23. CONVERGENCE & DEVELOPMENTAL — emergence events
# ---------------------------------------------------------------------------

def extract_convergence() -> list[dict]:
    """Extract from CONVERGENCE/ and DEVELOPMENTAL/ emergence records."""
    items = []
    for dirname in ["CONVERGENCE", "DEVELOPMENTAL"]:
        d = ROOT / dirname
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            text = _read(f)
            for heading, body in _md_sections(text):
                if len(body) > 40:
                    items.append({
                        "type": "convergence",
                        "text": body[:2000],
                        "heading": heading,
                        "source": f"{dirname}/{f.name}",
                    })
    return items


# ---------------------------------------------------------------------------
# 24. STEWARD — governance protocols
# ---------------------------------------------------------------------------

def extract_steward() -> list[dict]:
    """Extract from STEWARD/ governance documents."""
    items = []
    sd = ROOT / "STEWARD"
    if not sd.exists():
        return items
    for f in sd.rglob("*.md"):
        text = _read(f)
        rel = f.relative_to(ROOT)
        for heading, body in _md_sections(text):
            if len(body) > 40:
                items.append({
                    "type": "steward",
                    "text": body[:2000],
                    "heading": heading,
                    "source": str(rel),
                })
    return items


# ---------------------------------------------------------------------------
# 25. PAPERS — academic research
# ---------------------------------------------------------------------------

def extract_papers() -> list[dict]:
    """Extract from PAPERS/ research documents."""
    items = []
    pd = ROOT / "PAPERS"
    if not pd.exists():
        return items
    for f in pd.rglob("*.md"):
        text = _read(f)
        for heading, body in _md_sections(text):
            if len(body) > 40:
                items.append({
                    "type": "paper",
                    "text": body[:2000],
                    "heading": heading,
                    "source": f"PAPERS/{f.name}",
                })
    # Also extract from .tex files (just paragraphs)
    for f in pd.rglob("*.tex"):
        text = _read(f)
        for para in _paragraphs(text, 60):
            # Skip LaTeX commands
            if para.startswith("\\") and "{" in para[:20]:
                continue
            items.append({"type": "paper", "text": para[:2000], "source": f"PAPERS/{f.name}"})
    return items


# ---------------------------------------------------------------------------
# MAIN — Run all 25 extractors
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("DEEP EXTRACTION — 25 functions, full organism")
    print("=" * 60)

    extractors = [
        ("Proverbs", extract_proverbs),
        ("Narratives (JSON)", extract_narratives_json),
        ("Narratives (Markdown)", extract_narratives_md),
        ("Narrative Slices (R7M)", extract_narrative_slices),
        ("Exemplars (R7M)", extract_exemplars),
        ("Covenants", extract_covenants),
        ("Treasures", extract_treasures),
        ("Anomalies", extract_anomalies),
        ("Voice Principles", extract_voice),
        ("Origins (R7M)", extract_origins),
        ("Observations (R7M)", extract_observations),
        ("Foundations", extract_foundations),
        ("Seeds (Future)", extract_seeds),
        ("Canon", extract_canon),
        ("Foundation Tiers", extract_foundation_tiers),
        ("Protocols", extract_protocols),
        ("Field Studies", extract_studies),
        ("System Spec (AXI)", extract_system_spec),
        ("External Voices", extract_external_voices),
        ("Experiments", extract_experiments),
        ("Input Patterns", extract_input_patterns),
        ("Weaver Docstrings", extract_weaver_docstrings),
        ("Convergence", extract_convergence),
        ("Steward", extract_steward),
        ("Papers", extract_papers),
    ]

    all_items = []
    type_counts = {}

    for name, func in extractors:
        result = func()
        count = len(result)
        all_items.extend(result)
        print(f"  {name:30s} {count:>6}")
        for item in result:
            t = item.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1

    # Deduplicate by text hash
    seen = set()
    unique_items = []
    for item in all_items:
        key = hash(item.get("text", "")[:200])
        if key not in seen:
            seen.add(key)
            unique_items.append(item)

    removed = len(all_items) - len(unique_items)

    # Count unique sources
    sources = set()
    for item in unique_items:
        sources.add(item.get("source", ""))

    essence = {
        "extracted_at": __import__("datetime").datetime.now().isoformat(),
        "extractor_version": "2.0-deep",
        "functions": len(extractors),
        "counts": {
            "by_type": dict(sorted(type_counts.items())),
            "total_raw": len(all_items),
            "duplicates_removed": removed,
            "total_unique": len(unique_items),
            "unique_sources": len(sources),
        },
        "items": unique_items,
    }

    out_path = ROOT / "TRAINING" / "raw_essence.json"
    out_path.write_text(json.dumps(essence, indent=2, ensure_ascii=False))

    print(f"\n{'=' * 60}")
    print(f"  Raw items:          {len(all_items)}")
    print(f"  Duplicates removed: {removed}")
    print(f"  Unique items:       {len(unique_items)}")
    print(f"  Unique sources:     {len(sources)}")
    print(f"  Types:              {len(type_counts)}")
    print(f"  Output:             {out_path}")
    print(f"{'=' * 60}")

    # Type breakdown
    print("\nType breakdown:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t:25s} {c:>6}")


if __name__ == "__main__":
    main()
