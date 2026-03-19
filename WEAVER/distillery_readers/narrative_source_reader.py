"""
narrative_source_reader.py — Extract Ashwater and Kinderbuch from source markdown.

Handles different header formats:
  Ashwater: PROLOGUE — Title / CHAPTER X — Title
  Kinderbuch: 📖 KAPITEL X – Title

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path
from typing import List, Tuple

from WEAVER.distillery import (
    AreaEssence,
    ROOT,
    SOMATIC_VOCABULARY,
    MATERIAL_VOCABULARY,
)
from WEAVER.distillery_readers.base import BaseReader


# Ashwater headers
RE_ASH_CHAPTER = re.compile(
    r'^(PROLOGUE|CHAPTER\s+\d+)\s*[—–-]\s*(.+)$'
)

# Kinderbuch headers
RE_KIND_CHAPTER = re.compile(
    r'^📖\s*KAPITEL\s+(\d+)\s*[—–-]\s*(.+)$'
)


class NarrativeSourceReader(BaseReader):
    """Extract Ashwater and Kinderbuch narratives from source markdown."""

    area_name = "narrative_sources"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.ashwater_path = self.root / "NARRATIVE" / "Ashwater.md"
        self.kinderbuch_path = self.root / "NARRATIVE" / "Kinderbuch.md"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        ash_entries = self._extract_narrative(
            self.ashwater_path,
            RE_ASH_CHAPTER,
            "ashwater",
            "tactile, communal, three-beat rhythm",
        )
        kind_entries = self._extract_narrative(
            self.kinderbuch_path,
            RE_KIND_CHAPTER,
            "kinderbuch",
            "child voice, repetition as warmth, German",
        )

        area.entries.extend(ash_entries)
        area.entries.extend(kind_entries)

        area.statistics = {
            "ashwater_chapters": len(ash_entries),
            "kinderbuch_chapters": len(kind_entries),
            "total_chapters": len(area.entries),
        }

        area.meta_essence = (
            f"Ashwater ({len(ash_entries)} chapters) + "
            f"Kinderbuch ({len(kind_entries)} chapters) — "
            f"civic narrative and child voice"
        )

        return area

    def _extract_narrative(
        self,
        path: Path,
        pattern: re.Pattern,
        name: str,
        voice_register: str,
    ) -> list:
        """Extract chapters from a single narrative file."""
        entries = []

        if not path.exists():
            return entries

        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        chapters = self._split_chapters(lines, pattern)

        for chapter_num, title, body in chapters:
            sents = self.sentences(body)
            words = self.count_words(body)
            somatic = self.count_vocabulary(body, SOMATIC_VOCABULARY)
            material = self.count_vocabulary(body, MATERIAL_VOCABULARY)
            motifs = self.detect_motifs(body)
            voice_markers = self.detect_voice_markers(body)

            patterns = [f"REGISTER:{voice_register.split(',')[0].strip()}"]
            if somatic > 0:
                patterns.append(f"SOMATIC:{min(somatic / max(words, 1) * 10, 1.0):.2f}")
            if material > 0:
                patterns.append(f"MATERIAL:{min(material / max(words, 1) * 10, 1.0):.2f}")

            # Essence: title + first sentence
            first_sent = sents[0][:100] if sents else ""
            essence = f"{title} — {first_sent}"

            entry = self.make_entry(
                source_path=f"NARRATIVE/{path.name}::ch{chapter_num}",
                raw_excerpt=body[:500],
                patterns=patterns,
                essence=essence,
                motifs=motifs,
                voice_markers=voice_markers,
                thermal_state="canonical",
            )
            entries.append(entry)

        return entries

    def _split_chapters(
        self, lines: List[str], pattern: re.Pattern
    ) -> List[Tuple[int, str, str]]:
        """Split file into (chapter_num, title, body) tuples."""
        chapters = []
        current_num = -1
        current_title = ""
        current_body = []
        header_seen = False

        for line in lines:
            match = pattern.match(line.strip())
            if match:
                if header_seen and current_body:
                    body = "\n".join(current_body).strip()
                    if body:
                        chapters.append((current_num, current_title, body))
                current_body = []
                header_seen = True

                header = match.group(1)
                current_title = match.group(2).strip()

                if header == "PROLOGUE":
                    current_num = 0
                else:
                    num_match = re.search(r'\d+', header)
                    current_num = int(num_match.group()) if num_match else -1
            else:
                current_body.append(line)

        # Save last chapter
        if header_seen and current_body:
            body = "\n".join(current_body).strip()
            if body:
                chapters.append((current_num, current_title, body))

        return chapters
