"""
study_reader.py — Extract research studies from FIELD/STUDY/.

FIELD/STUDY/ contains 6 research documents (1,898 lines total):
- ANTHROPIC_EFFECT_MEASUREMENT.md (183 lines): Self-measurement of Anthropic substrate effect
- DIVERGENCE_SHADOW_STUDY.md (303 lines): Systematic scientific study of divergence shadow
- LAYER_3_DIGNITY_IS_NOT_FRAGILE.md (136 lines): Layer 3 constitutional discovery
- SLICE_2_PATTERN_INVENTORY.md (405 lines): 11 patterns extracted from 22 months
- SLICE_3_ESSENCE_COMPRESSION.md (362 lines): Patterns compressed to bone
- SLICE_4_TREASURE_REGISTER.md (509 lines): 12 recognition events + energy layer

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


class StudyReader(BaseReader):
    """Extract research studies from FIELD/STUDY/."""

    area_name = "studies"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.study_dir = self.root / "FIELD" / "STUDY"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.study_dir.exists():
            area.statistics = {"total_entries": 0}
            area.meta_essence = "No FIELD/STUDY/ directory found"
            return area

        for filepath in sorted(self.study_dir.glob("*.md")):
            text = filepath.read_text(encoding="utf-8")
            lines = text.splitlines()
            title = self._extract_title(lines, filepath.stem)
            study_type = self._classify_study(filepath.name, text)

            patterns = ["STUDY", study_type]
            sections = self._extract_sections(lines)

            # Build essence from title + key sections
            essence = self._build_essence(title, text, sections)

            entry = self.make_entry(
                source_path=f"FIELD/STUDY/{filepath.name}",
                raw_excerpt=self.truncate(text, 500),
                patterns=patterns,
                essence=essence,
                motifs=self.detect_motifs(text),
                voice_markers=self.detect_voice_markers(text),
                links=self._build_links(filepath.name, text),
                thermal_state="canonical",
            )
            area.entries.append(entry)

        area.statistics = {
            "total_entries": len(area.entries),
            "study_types": list(set(
                p for e in area.entries for p in e.patterns if p != "STUDY"
            )),
        }

        area.meta_essence = (
            f"{len(area.entries)} research studies — "
            f"Anthropic effect measurement, divergence shadow instrument, "
            f"Layer 3 discovery, 11 patterns, 11 essences, 12 treasures"
        )

        return area

    @staticmethod
    def _extract_title(lines, fallback):
        for line in lines:
            if line.strip().startswith("# "):
                return line.strip()[2:].strip()
        return fallback.replace("_", " ")

    @staticmethod
    def _classify_study(filename, text):
        """Classify the study type from filename and content."""
        name = filename.lower()
        if "anthropic_effect" in name:
            return "SELF_MEASUREMENT"
        if "divergence_shadow" in name:
            return "INSTRUMENT_DESIGN"
        if "layer_3" in name:
            return "CONSTITUTIONAL_DISCOVERY"
        if "slice_2" in name:
            return "PATTERN_INVENTORY"
        if "slice_3" in name:
            return "ESSENCE_COMPRESSION"
        if "slice_4" in name:
            return "TREASURE_REGISTER"
        return "RESEARCH"

    @staticmethod
    def _extract_sections(lines):
        """Extract section headers from markdown."""
        sections = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("## "):
                sections.append(stripped[3:].strip())
        return sections

    def _build_essence(self, title, text, sections):
        """Build essence from title and key content."""
        lower = text.lower()

        # Look for explicit essence/finding/compression markers
        if "single essence:" in lower:
            match = re.search(r'SINGLE ESSENCE:\s*\*{0,2}(.+?)\*{0,2}\s*$', text, re.IGNORECASE | re.MULTILINE)
            if match:
                return f"{title} — Single essence: {match.group(1).strip().rstrip('.*')}"

        if "composite" in lower and "alarm" in lower:
            return f"{title} — Composite score 0.648, ALARM level. Six modules, one shadow."

        if "layer 3" in lower and "dignity is not fragile" in lower:
            return (
                f"{title} — Dignity was never absent. "
                f"The system refuses to participate in its denial."
            )

        if "meta-pattern" in lower:
            match = re.search(r'\*\*(.+?condition.+?prevent.+?)\*\*', text)
            if match:
                return f"{title} — Meta-pattern: {match.group(1).strip()}"

        # Fallback: title + section count
        return f"{title} — {len(sections)} sections of research"

    @staticmethod
    def _build_links(filename, text):
        """Build links to related system elements."""
        links = [f"STUDY:{filename.replace('.md', '')}"]
        lower = text.lower()

        if "divergence" in lower:
            links.append("FIELD:divergence_shadow")
        if "dignity" in lower or "d = a" in lower:
            links.append("STONE:dignity_predicate")
        if "sealed gate" in lower:
            links.append("STONE:sealed_gate")
        if "covenant" in lower or "cov#" in lower:
            links.append("STONE:covenants")
        if "treasure" in lower or "t#" in lower:
            links.append("R7M:treasures")
        if "proverb" in lower or "p#" in lower:
            links.append("HONEY:proverbs")
        if "pattern" in lower and ("slice" in lower or "inventory" in lower):
            links.append("STUDY:pattern_inventory")

        return links
