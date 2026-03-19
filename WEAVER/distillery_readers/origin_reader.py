"""
origin_reader.py — Extract origin documents from R7M/ORIGINS/.

Foundational thinking predating the Grand Archive. 10 documents spanning
May 2024 to September 2025. The mycelium.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


RE_DATE = re.compile(r'(\d{4}-\d{2}-\d{2}|\d{4}-\d{2}-XX|\d{4}-XX)')


class OriginReader(BaseReader):
    """Extract origin documents from R7M/ORIGINS/."""

    area_name = "origins"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.origins_dir = self.root / "R7M" / "ORIGINS"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.origins_dir.exists():
            area.meta_essence = "ORIGINS directory not found"
            return area

        files = sorted(
            f for f in self.origins_dir.iterdir()
            if f.is_file() and f.suffix == ".md" and f.name != "ORIGINS_INDEX.md"
        )

        # Also extract index as its own entry
        index_path = self.origins_dir / "ORIGINS_INDEX.md"
        if index_path.exists():
            idx_text = index_path.read_text(encoding="utf-8")
            entry = self.make_entry(
                source_path="R7M/ORIGINS/ORIGINS_INDEX.md",
                raw_excerpt=self.truncate(idx_text, 500),
                patterns=["INDEX", "ARCHAEOLOGY"],
                essence="The deep archive index — mycelium map of everything predating the Grand Archive",
                motifs=self.detect_motifs(idx_text),
                links=["ORIGINS-INDEX"],
                thermal_state="canonical",
            )
            area.entries.append(entry)

        for filepath in files:
            text = filepath.read_text(encoding="utf-8")
            lines = text.splitlines()

            # Extract title from first heading or filename
            title = self._extract_title(lines, filepath.stem)
            date = self._extract_date(filepath.name)

            patterns = [f"DATE:{date}"] if date else []

            # First paragraph as essence seed
            first_para = self._first_paragraph(lines)
            essence = f"{title}: {first_para[:200]}" if first_para else title

            entry = self.make_entry(
                source_path=f"R7M/ORIGINS/{filepath.name}",
                raw_excerpt=self.truncate(text, 500),
                patterns=patterns,
                essence=essence,
                motifs=self.detect_motifs(text),
                voice_markers=self.detect_voice_markers(text),
                links=[f"ORIGIN:{filepath.stem}"],
                thermal_state="canonical",
            )
            area.entries.append(entry)

        area.statistics = {
            "total_documents": len(area.entries),
            "date_range": "2024-05 to 2025-09",
        }

        area.meta_essence = (
            f"{len(area.entries)} origin documents — "
            f"the mycelium predating the Grand Archive (May 2024 – Sep 2025)"
        )

        return area

    @staticmethod
    def _extract_title(lines, fallback: str) -> str:
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
        return fallback.replace("_", " ")

    @staticmethod
    def _extract_date(filename: str) -> str:
        match = RE_DATE.search(filename)
        return match.group(1) if match else ""

    @staticmethod
    def _first_paragraph(lines) -> str:
        """Get first non-empty, non-heading paragraph."""
        para = []
        started = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if started and para:
                    break
                continue
            if stripped.startswith("#"):
                continue
            started = True
            para.append(stripped)
        return " ".join(para)
