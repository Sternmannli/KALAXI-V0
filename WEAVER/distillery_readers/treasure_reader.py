"""
treasure_reader.py — Extract all treasures from R7M/TREASURES/TREASURES_INDEX.md.

Parses ### T#XX — Title blocks with fields: Formula, Description, Structure,
Metrics, Protocol, Implementation, Covenants, Tier, etc.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path
from typing import List, Dict

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


RE_TREASURE = re.compile(r'^###\s+(T#\d+)\s*[—–-]\s*(.+)$')
RE_FIELD = re.compile(r'^\s*-\s*\*\*(.+?):?\*\*:?\s*(.*)$')


class TreasureReader(BaseReader):
    """Extract all treasures from TREASURES_INDEX.md."""

    area_name = "treasures"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.source_path = self.root / "R7M" / "TREASURES" / "TREASURES_INDEX.md"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.source_path.exists():
            area.meta_essence = "TREASURES_INDEX.md not found"
            return area

        text = self.source_path.read_text(encoding="utf-8")
        lines = text.splitlines()

        treasures = self._parse_treasures(lines)
        tier_counts = {}

        for t in treasures:
            tid = t["id"]
            title = t["title"]
            desc = t.get("Description", t.get("description", ""))
            tier = t.get("Tier", t.get("tier", "unknown"))
            covenants_raw = t.get("Covenants", t.get("covenants", ""))
            formula = t.get("Formula", t.get("Simplified", ""))
            structure = t.get("Structure", "")

            # Parse covenants list
            covenants = []
            if covenants_raw:
                covenants = [c.strip() for c in covenants_raw.split(",") if c.strip()]

            # Track tier
            tier_key = tier.split("(")[0].strip() if tier else "unknown"
            tier_counts[tier_key] = tier_counts.get(tier_key, 0) + 1

            # Build patterns
            patterns = [f"TIER:{tier_key}"]
            if formula:
                patterns.append("HAS_FORMULA")
            if structure:
                patterns.append("HAS_STRUCTURE")

            # Essence: title + description
            essence = f"{title}: {desc[:200]}" if desc else title

            # Links
            links = [tid] + covenants

            entry = self.make_entry(
                source_path=f"R7M/TREASURES/TREASURES_INDEX.md::{tid}",
                raw_excerpt=self._format_treasure(t),
                patterns=patterns,
                essence=essence,
                motifs=self.detect_motifs(desc),
                links=links,
                thermal_state="canonical",
            )
            area.entries.append(entry)

        area.statistics = {
            "total_treasures": len(treasures),
            "tier_distribution": tier_counts,
        }

        area.meta_patterns = [f"tier:{k}:{v}" for k, v in sorted(tier_counts.items(), key=lambda x: -x[1])]

        area.meta_essence = (
            f"{len(treasures)} treasures extracted — "
            f"Grand Archive recoveries across {len(tier_counts)} tiers"
        )

        return area

    def _parse_treasures(self, lines: List[str]) -> List[Dict]:
        """Parse all ### T#XX blocks."""
        treasures = []
        current = None

        for line in lines:
            match = RE_TREASURE.match(line.strip())
            if match:
                if current:
                    treasures.append(current)
                current = {
                    "id": match.group(1),
                    "title": match.group(2).strip(),
                }
                continue

            if current is None:
                continue

            field_match = RE_FIELD.match(line)
            if field_match:
                key = field_match.group(1).strip()
                value = field_match.group(2).strip()
                current[key] = value

        if current:
            treasures.append(current)

        return treasures

    @staticmethod
    def _format_treasure(t: Dict) -> str:
        """Format treasure for raw_excerpt."""
        parts = [f"{t['id']} — {t['title']}"]
        if t.get("Description"):
            parts.append(t["Description"][:200])
        if t.get("Formula") or t.get("Simplified"):
            parts.append(f"Formula: {t.get('Formula', t.get('Simplified', ''))}")
        return " | ".join(parts)
