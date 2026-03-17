#!/usr/bin/env python3
"""
extract_essence.py — Pull all training data from system files.

Sources:
  - Proverbs (3,333+)
  - Wisdom nodes (87)
  - Treasures (59)
  - Narratives: Hakaka, Ashwater, Kinderbuch, KALAXI_1
  - Voice Architecture (31 linguistic principles)
  - Covenants (18)
  - Input Ledger patterns

Output: TRAINING/raw_essence.json — structured extraction ready for format_data.py

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def extract_proverbs() -> list[dict]:
    """Extract proverbs from all proverb files."""
    items = []

    # Main proverb file
    proverb_file = ROOT / "site" / "public" / "data" / "proverbs.json"
    if proverb_file.exists():
        data = json.loads(proverb_file.read_text())
        if isinstance(data, list):
            for p in data:
                text = p.get("text", p) if isinstance(p, dict) else str(p)
                items.append({"type": "proverb", "text": text, "source": "proverbs.json"})
        elif isinstance(data, dict):
            for category, proverbs in data.items():
                if isinstance(proverbs, list):
                    for p in proverbs:
                        text = p.get("text", p) if isinstance(p, dict) else str(p)
                        items.append({"type": "proverb", "text": text, "source": f"proverbs.json/{category}"})

    # HONEY tier proverbs
    for f in (ROOT / "HONEY").rglob("*.json"):
        try:
            data = json.loads(f.read_text())
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "text" in item:
                        items.append({"type": "proverb", "text": item["text"], "source": str(f.relative_to(ROOT))})
        except (json.JSONDecodeError, KeyError):
            pass

    return items


def extract_narratives() -> list[dict]:
    """Extract narrative paragraphs from all books."""
    items = []

    for name in ["hakaka", "ashwater", "kinderbuch", "kalaxi1"]:
        json_path = ROOT / "site" / "public" / "data" / f"{name}.json"
        if not json_path.exists():
            continue

        data = json.loads(json_path.read_text())
        chapters = data if isinstance(data, list) else data.get("chapters", [])

        for ch in chapters:
            if isinstance(ch, dict):
                title = ch.get("title", "")
                content = ch.get("content", ch.get("text", ""))
                if content:
                    # Split into paragraphs, take meaningful ones
                    paragraphs = [p.strip() for p in content.split("\n") if len(p.strip()) > 30]
                    for para in paragraphs:
                        items.append({
                            "type": "narrative",
                            "text": para,
                            "source": f"{name}/{title}",
                            "book": name,
                        })

    return items


def extract_covenants() -> list[dict]:
    """Extract covenants from stone tier."""
    items = []

    stone_file = ROOT / "R7M" / "tier1_stone.md"
    if stone_file.exists():
        text = stone_file.read_text()
        # Find COV# entries
        cov_pattern = re.compile(r"(COV#\d+[A-Z]*)\s*[—–-]\s*(.+?)(?:\n\n|\n(?=COV#)|\Z)", re.DOTALL)
        for match in cov_pattern.finditer(text):
            cov_id = match.group(1)
            cov_text = match.group(2).strip()
            items.append({"type": "covenant", "id": cov_id, "text": cov_text, "source": "tier1_stone.md"})

    return items


def extract_treasures() -> list[dict]:
    """Extract treasures from R7M index."""
    items = []

    r7m_file = ROOT / "site" / "public" / "data" / "r7m-index.json"
    if r7m_file.exists():
        data = json.loads(r7m_file.read_text())
        if isinstance(data, dict) and "tiers" in data:
            tiers = data["tiers"]
            tier_items = tiers.values() if isinstance(tiers, dict) else tiers
            for tier in tier_items:
                if isinstance(tier, dict):
                    for t in tier.get("treasures", []):
                        text = t.get("principle", t.get("description", t.get("title", "")))
                        items.append({
                            "type": "treasure",
                            "id": t.get("id", ""),
                            "text": text,
                            "formula": t.get("formula", t.get("vow", "")),
                            "source": "r7m-index.json",
                        })

    return items


def extract_voice() -> list[dict]:
    """Extract voice principles from Voice Architecture."""
    items = []

    voice_file = ROOT / "VOICE" / "VOICE_ARCHITECTURE_2026-03-14.md"
    if voice_file.exists():
        text = voice_file.read_text()
        # Extract numbered principles or key quotes
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith('"') and line.endswith('"'):
                items.append({"type": "voice_principle", "text": line.strip('"'), "source": "voice_architecture"})
            elif re.match(r"^\d+\.\s+\*\*", line):
                clean = re.sub(r"\*\*", "", line)
                items.append({"type": "voice_principle", "text": clean, "source": "voice_architecture"})

    return items


def main():
    print("Extracting essence from system files...")

    proverbs = extract_proverbs()
    print(f"  Proverbs: {len(proverbs)}")

    narratives = extract_narratives()
    print(f"  Narrative paragraphs: {len(narratives)}")

    covenants = extract_covenants()
    print(f"  Covenants: {len(covenants)}")

    treasures = extract_treasures()
    print(f"  Treasures: {len(treasures)}")

    voice = extract_voice()
    print(f"  Voice principles: {len(voice)}")

    essence = {
        "extracted_at": __import__("datetime").datetime.now().isoformat(),
        "counts": {
            "proverbs": len(proverbs),
            "narratives": len(narratives),
            "covenants": len(covenants),
            "treasures": len(treasures),
            "voice_principles": len(voice),
            "total": len(proverbs) + len(narratives) + len(covenants) + len(treasures) + len(voice),
        },
        "items": proverbs + narratives + covenants + treasures + voice,
    }

    out_path = ROOT / "TRAINING" / "raw_essence.json"
    out_path.write_text(json.dumps(essence, indent=2, ensure_ascii=False))
    print(f"\nTotal: {essence['counts']['total']} items → {out_path}")


if __name__ == "__main__":
    main()
