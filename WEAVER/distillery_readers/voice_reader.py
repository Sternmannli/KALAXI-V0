"""
voice_reader.py — Extract voice architecture from VOICE/ directory.

Four documents, 1,138 lines total:
  VOICE_ARCHITECTURE — 31 linguistic principles from 5,000 years of masterpieces
  BLOCKCHAIN_DNA_EXTRACTION — technical mapping of voice to system operations
  TRILITERAL_ROOT_SYSTEM — Arabic linguistic roots for voice generation
  RAW_INPUT_V001 — Mohamed's raw language analyzed for depth

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path
from typing import List, Tuple

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


VOICE_FILES = [
    ("VOICE_ARCHITECTURE_2026-03-14.md", "voice_architecture"),
    ("BLOCKCHAIN_DNA_EXTRACTION_2026-03-14.md", "blockchain_dna"),
    ("TRILITERAL_ROOT_SYSTEM_2026-03-18.md", "triliteral_roots"),
    ("RAW_INPUT_V001_2026-03-14_LANGUAGE_DEPTH.md", "raw_v001_voice"),
]


class VoiceReader(BaseReader):
    """Extract voice architecture from VOICE/ directory."""

    area_name = "voice_architecture"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.voice_dir = self.root / "VOICE"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.voice_dir.exists():
            area.meta_essence = "VOICE directory not found"
            return area

        total_sections = 0

        for filename, doc_type in VOICE_FILES:
            filepath = self.voice_dir / filename
            if not filepath.exists():
                continue

            text = filepath.read_text(encoding="utf-8")
            sections = self._split_sections(text)
            total_sections += len(sections)

            for section_title, section_body in sections:
                motifs = self.detect_motifs(section_body)
                voice_markers = self.detect_voice_markers(section_body)

                patterns = [f"DOC:{doc_type}"]
                if motifs:
                    patterns.append(f"MOTIFS:{len(motifs)}")

                essence = f"{section_title}"
                # Add first substantial sentence
                first = self._first_substance(section_body)
                if first:
                    essence = f"{section_title} — {first[:150]}"

                entry = self.make_entry(
                    source_path=f"VOICE/{filename}::{section_title}",
                    raw_excerpt=self.truncate(section_body, 500),
                    patterns=patterns,
                    essence=essence,
                    motifs=motifs,
                    voice_markers=voice_markers,
                    links=[f"VOICE:{doc_type}"],
                    thermal_state="canonical",
                )
                area.entries.append(entry)

        area.statistics = {
            "total_documents": sum(1 for f, _ in VOICE_FILES if (self.voice_dir / f).exists()),
            "total_sections": total_sections,
            "total_entries": len(area.entries),
        }

        area.meta_essence = (
            f"{len(area.entries)} voice architecture entries from "
            f"{area.statistics['total_documents']} documents — "
            f"linguistic DNA from 5,000 years of masterpieces"
        )

        return area

    @staticmethod
    def _split_sections(text: str) -> List[Tuple[str, str]]:
        """Split document into (title, body) tuples at ## or ### headings."""
        sections = []
        current_title = ""
        current_body = []

        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("## ") or stripped.startswith("### "):
                if current_title and current_body:
                    body = "\n".join(current_body).strip()
                    if body and len(body) > 20:  # Skip tiny sections
                        sections.append((current_title, body))
                current_title = stripped.lstrip("#").strip().strip("*").strip()
                current_body = []
            else:
                current_body.append(line)

        if current_title and current_body:
            body = "\n".join(current_body).strip()
            if body and len(body) > 20:
                sections.append((current_title, body))

        return sections

    @staticmethod
    def _first_substance(text: str) -> str:
        """Get first non-empty, non-formatting line."""
        for line in text.splitlines():
            stripped = line.strip()
            if (stripped
                    and not stripped.startswith("-")
                    and not stripped.startswith("|")
                    and not stripped.startswith("*")
                    and len(stripped) > 15):
                return stripped
        return ""
