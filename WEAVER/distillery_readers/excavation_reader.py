"""
excavation_reader.py — Extract excavation records and R7M foundational texts.

R7M/EXCAVATION/ (5 files, 637 lines): provenance maps, terrain maps
R7M/BOOK_OF_BEGINNINGS.txt (49 lines): foundational statements
R7M/KALAXI_SOVEREIGN_CANON.txt (413 lines): sovereign canon
R7M/ESSENCE.md (14 lines): distilled essence

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


class ExcavationReader(BaseReader):
    """Extract excavation records and R7M foundational texts."""

    area_name = "excavation"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.excavation_dir = self.root / "R7M" / "EXCAVATION"
        self.r7m_dir = self.root / "R7M"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        # Excavation files
        if self.excavation_dir.exists():
            for filepath in sorted(self.excavation_dir.glob("*.md")):
                text = filepath.read_text(encoding="utf-8")
                lines = text.splitlines()
                title = self._extract_title(lines, filepath.stem)

                patterns = ["EXCAVATION"]
                if "provenance" in filepath.name.lower():
                    patterns.append("PROVENANCE")
                if "terrain" in filepath.name.lower():
                    patterns.append("TERRAIN")

                first_para = self._first_paragraph(lines)
                essence = f"{title}: {first_para[:200]}" if first_para else title

                entry = self.make_entry(
                    source_path=f"R7M/EXCAVATION/{filepath.name}",
                    raw_excerpt=self.truncate(text, 500),
                    patterns=patterns,
                    essence=essence,
                    motifs=self.detect_motifs(text),
                    links=[f"EXCAVATION:{filepath.stem}"],
                    thermal_state="witnessed",
                )
                area.entries.append(entry)

        # R7M foundational texts
        foundational_files = [
            ("BOOK_OF_BEGINNINGS.txt", "The book of beginnings — cosmology and foundational statements"),
            ("KALAXI_SOVEREIGN_CANON.txt", "The sovereign canon — highest-level canonical statements"),
            ("ESSENCE.md", "Distilled essence of the entire system"),
        ]

        for filename, essence_seed in foundational_files:
            filepath = self.r7m_dir / filename
            if not filepath.exists():
                continue

            text = filepath.read_text(encoding="utf-8")

            entry = self.make_entry(
                source_path=f"R7M/{filename}",
                raw_excerpt=self.truncate(text, 500),
                patterns=["FOUNDATIONAL", "R7M"],
                essence=essence_seed,
                motifs=self.detect_motifs(text),
                voice_markers=self.detect_voice_markers(text),
                links=[f"R7M:{filename.replace('.md', '').replace('.txt', '')}"],
                thermal_state="canonical",
            )
            area.entries.append(entry)

        area.statistics = {
            "excavation_files": sum(1 for e in area.entries if "EXCAVATION" in e.patterns),
            "foundational_files": sum(1 for e in area.entries if "FOUNDATIONAL" in e.patterns),
            "total_entries": len(area.entries),
        }

        area.meta_essence = (
            f"{len(area.entries)} excavation and foundational entries — "
            f"provenance chains, terrain maps, sovereign canon, book of beginnings"
        )

        return area

    @staticmethod
    def _extract_title(lines, fallback):
        for line in lines:
            if line.strip().startswith("# "):
                return line.strip()[2:].strip()
        return fallback.replace("_", " ")

    @staticmethod
    def _first_paragraph(lines):
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
