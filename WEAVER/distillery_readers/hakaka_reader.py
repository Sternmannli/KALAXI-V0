"""
hakaka_reader.py — Extract Hakaka narrative from NARRATIVE/Hakaka_Complete.md.

Reads the source markdown directly, splitting by chapter headers.
Extracts per-chapter voice metrics and structural analysis.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path
from typing import List, Tuple

from WEAVER.distillery import (
    AreaEssence,
    NarrativeChapterEssence,
    NarrativeEssence,
    ROOT,
    SOMATIC_VOCABULARY,
    MATERIAL_VOCABULARY,
    CORE_IMAGES,
)
from WEAVER.distillery_readers.base import BaseReader


# Chapter header patterns
RE_CHAPTER = re.compile(
    r'^(PROLOGUE|CHAPTER\s+\d+|EPILOGUE):\s*(.+)$'
)


class HakakaReader(BaseReader):
    """Extract Hakaka narrative from source markdown."""

    area_name = "hakaka"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.source_path = self.root / "NARRATIVE" / "Hakaka_Complete.md"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.source_path.exists():
            area.meta_essence = "Hakaka_Complete.md not found"
            return area

        text = self.source_path.read_text(encoding="utf-8")
        lines = text.splitlines()

        chapters = self._split_chapters(lines)
        narrative = NarrativeEssence(
            name="Hakaka",
            path="NARRATIVE/Hakaka_Complete.md",
        )

        total_somatic = 0
        total_material = 0
        total_sentences = 0
        total_gaps = 0

        for chapter_num, title, body in chapters:
            sents = self.sentences(body)
            words = self.count_words(body)
            somatic = self.count_vocabulary(body, SOMATIC_VOCABULARY)
            material = self.count_vocabulary(body, MATERIAL_VOCABULARY)
            motifs = self.detect_motifs(body)
            three_beats = sum(1 for s in sents if s.count(",") == 2)
            gaps = body.count("—") + body.count("...") + body.count("…")

            avg_len = words / max(len(sents), 1)

            chapter_essence = NarrativeChapterEssence(
                chapter=chapter_num,
                title=title,
                sentence_count=len(sents),
                avg_sentence_length=round(avg_len, 1),
                core_images=motifs,
                somatic_count=somatic,
                material_count=material,
                three_beat_count=three_beats,
                gap_count=gaps,
                essence=self._distill_chapter(title, body, motifs),
            )
            narrative.chapters.append(chapter_essence)

            total_somatic += somatic
            total_material += material
            total_sentences += len(sents)
            total_gaps += gaps

            # Create EssenceEntry per chapter
            voice_markers = self.detect_voice_markers(body)
            patterns = []
            if somatic > 0:
                patterns.append(f"SOMATIC:{min(somatic / max(words, 1) * 10, 1.0):.2f}")
            if material > 0:
                patterns.append(f"MATERIAL:{min(material / max(words, 1) * 10, 1.0):.2f}")
            if three_beats > 0:
                patterns.append(f"THREE_BEAT:{three_beats / max(len(sents), 1):.2f}")
            if gaps > 0:
                patterns.append(f"GAP:{gaps / max(len(sents), 1):.2f}")

            entry = self.make_entry(
                source_path=f"NARRATIVE/Hakaka_Complete.md::ch{chapter_num}",
                raw_excerpt=body[:500],
                patterns=patterns,
                essence=chapter_essence.essence,
                motifs=motifs,
                voice_markers=voice_markers,
                thermal_state="canonical",
            )
            area.entries.append(entry)

        # Structural arc
        if chapters:
            first_title = chapters[0][1]
            last_title = chapters[-1][1]
            narrative.structural_arc = f"From '{first_title}' to '{last_title}'"
            narrative.voice_register = "mythic, raw, stone-and-bone"
            narrative.essence = (
                "The origin cycle — a nameless girl ties a knot "
                "and builds a civilization from nothing"
            )

        area.statistics = {
            "total_chapters": len(chapters),
            "total_sentences": total_sentences,
            "total_somatic": total_somatic,
            "total_material": total_material,
            "total_gaps": total_gaps,
            "avg_sentence_length": round(
                sum(c.avg_sentence_length for c in narrative.chapters) / max(len(narrative.chapters), 1), 1
            ),
        }

        area.meta_essence = (
            f"Hakaka: {len(chapters)} chapters of origin narrative — "
            f"mythic voice, somatic density {total_somatic}, "
            f"material grounding {total_material}"
        )

        return area

    def _split_chapters(self, lines: List[str]) -> List[Tuple[int, str, str]]:
        """Split the file into (chapter_num, title, body) tuples."""
        chapters = []
        current_num = -1
        current_title = ""
        current_body = []
        header_seen = False

        for line in lines:
            match = RE_CHAPTER.match(line.strip())
            if match:
                # Save previous chapter (only if we've seen a header)
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
                elif header == "EPILOGUE":
                    current_num = 54  # After chapter 53
                else:
                    num_match = re.search(r'\d+', header)
                    current_num = int(num_match.group()) if num_match else -1
            else:
                current_body.append(line)

        # Save last chapter
        if current_body:
            body = "\n".join(current_body).strip()
            if body:
                chapters.append((current_num, current_title, body))

        return chapters

    def _distill_chapter(self, title: str, body: str, motifs: List[str]) -> str:
        """Create a one-line essence for a chapter."""
        # Use first sentence as seed, modified by motifs
        sents = self.sentences(body)
        if not sents:
            return title

        first = sents[0]
        if len(first) > 100:
            first = first[:97] + "..."

        if motifs:
            return f"{title} — {', '.join(motifs[:3])} — {first}"
        return f"{title} — {first}"
