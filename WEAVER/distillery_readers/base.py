"""
base.py — Base reader class for Distillery source readers.

Every reader inherits from BaseReader and implements extract() -> AreaEssence.
Shared utilities: pattern extraction, essence distillation, text analysis.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path
from typing import List

from WEAVER.distillery import (
    ROOT,
    EssenceEntry,
    AreaEssence,
    SOMATIC_VOCABULARY,
    MATERIAL_VOCABULARY,
    CORE_IMAGES,
)


class BaseReader:
    """Base class for all Distillery source readers.

    Subclasses must implement:
        area_name: str — the content area name (e.g., "proverbs", "anomalies")
        extract() -> AreaEssence — the extraction logic
    """

    area_name: str = "unknown"

    def __init__(self, root: Path = ROOT):
        self.root = root

    def extract(self) -> AreaEssence:
        """Extract essence from this reader's content area.
        Must be implemented by subclasses."""
        raise NotImplementedError

    # ── Shared text analysis ──────────────────────────────────────

    @staticmethod
    def sentences(text: str) -> List[str]:
        """Split text into sentences."""
        if not text:
            return []
        raw = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in raw if s.strip()]

    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text."""
        return len(text.split()) if text else 0

    @staticmethod
    def count_vocabulary(text: str, vocab: set) -> int:
        """Count occurrences of vocabulary words in text."""
        if not text:
            return 0
        lower = text.lower()
        return sum(1 for word in vocab if word in lower)

    @staticmethod
    def truncate(text: str, max_len: int = 500) -> str:
        """Truncate text for storage in raw_excerpt."""
        if not text or len(text) <= max_len:
            return text or ""
        return text[:max_len] + "..."

    def detect_motifs(self, text: str) -> List[str]:
        """Detect recurring motifs (core images) in text."""
        if not text:
            return []
        lower = text.lower()
        return [img for img in CORE_IMAGES if img in lower]

    def detect_voice_markers(self, text: str) -> List[str]:
        """Detect voice fingerprint markers in text."""
        markers = []
        if not text:
            return markers

        sents = self.sentences(text)
        if not sents:
            return markers

        # Short sentence dominance (< 8 words)
        short = sum(1 for s in sents if self.count_words(s) < 8)
        if short / max(len(sents), 1) > 0.4:
            markers.append("short_sentence_dominant")

        # Somatic vocabulary presence
        if self.count_vocabulary(text, SOMATIC_VOCABULARY) > 0:
            markers.append("somatic_present")

        # Material grounding
        if self.count_vocabulary(text, MATERIAL_VOCABULARY) > 0:
            markers.append("material_grounded")

        # Three-beat rhythm (sentences with 2 commas)
        three_beats = sum(1 for s in sents if s.count(",") == 2)
        if three_beats > 0:
            markers.append("three_beat_rhythm")

        # Gap (em-dash, ellipsis)
        if "—" in text or "..." in text or "…" in text:
            markers.append("gap_present")

        return markers

    def make_entry(
        self,
        source_path: str,
        raw_excerpt: str,
        patterns: List[str],
        essence: str,
        motifs: List[str] = None,
        voice_markers: List[str] = None,
        links: List[str] = None,
        thermal_state: str = "witnessed",
    ) -> EssenceEntry:
        """Create a standardized EssenceEntry."""
        return EssenceEntry(
            source_path=source_path,
            source_area=self.area_name,
            raw_excerpt=self.truncate(raw_excerpt),
            patterns=patterns or [],
            essence=essence,
            motifs=motifs or [],
            voice_markers=voice_markers or [],
            links=links or [],
            thermal_state=thermal_state,
        )
