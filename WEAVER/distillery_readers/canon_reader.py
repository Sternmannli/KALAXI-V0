"""
canon_reader.py — Extract constitutional texts from CANON/.

Three foundational documents:
  FIRST-SIGHT.md — the founding wound
  MASTER_CANON_V1.md — the master canon
  SEALED_GATE_SPEC.md — the sealed gate specification

These are the deepest constitutional texts. Thermal state: canonical.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


CANON_FILES = {
    "FIRST-SIGHT.md": {
        "essence_seed": "The founding wound — a father separated from his children by systems that could not see him",
        "type": "founding_wound",
    },
    "MASTER_CANON_V1.md": {
        "essence_seed": "The master canon — constitutional law governing the entire system",
        "type": "constitution",
    },
    "SEALED_GATE_SPEC.md": {
        "essence_seed": "The sealed gate — absolute prohibitions that override everything",
        "type": "prohibition",
    },
}


class CanonReader(BaseReader):
    """Extract constitutional texts from CANON/."""

    area_name = "canon"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.canon_dir = self.root / "CANON"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.canon_dir.exists():
            area.meta_essence = "CANON directory not found"
            return area

        for filename, meta in CANON_FILES.items():
            filepath = self.canon_dir / filename
            if not filepath.exists():
                continue

            text = filepath.read_text(encoding="utf-8")
            lines = text.splitlines()

            # Extract title
            title = filename.replace(".md", "").replace("_", " ").replace("-", " ")
            for line in lines:
                if line.strip().startswith("# "):
                    title = line.strip()[2:].strip()
                    break

            patterns = [
                f"TYPE:{meta['type']}",
                "CONSTITUTIONAL",
            ]

            # Extract key principles/rules from the text
            principles = self._extract_principles(lines)
            if principles:
                patterns.append(f"PRINCIPLES:{len(principles)}")

            essence = meta["essence_seed"]

            entry = self.make_entry(
                source_path=f"CANON/{filename}",
                raw_excerpt=self.truncate(text, 500),
                patterns=patterns,
                essence=essence,
                motifs=self.detect_motifs(text),
                voice_markers=self.detect_voice_markers(text),
                links=[f"CANON:{filename.replace('.md', '')}"],
                thermal_state="canonical",
            )
            area.entries.append(entry)

        area.statistics = {
            "total_documents": len(area.entries),
            "types": [CANON_FILES[f]["type"] for f in CANON_FILES if (self.canon_dir / f).exists()],
        }

        area.meta_essence = (
            f"{len(area.entries)} constitutional texts — "
            f"the founding wound, the master canon, the sealed gate"
        )

        return area

    @staticmethod
    def _extract_principles(lines):
        """Extract numbered or bulleted principles from canon text."""
        principles = []
        for line in lines:
            stripped = line.strip()
            # Numbered: 1. text, 2. text
            if stripped and stripped[0].isdigit() and ". " in stripped:
                principles.append(stripped)
            # Bulleted: - text
            elif stripped.startswith("- ") and len(stripped) > 10:
                principles.append(stripped)
        return principles
