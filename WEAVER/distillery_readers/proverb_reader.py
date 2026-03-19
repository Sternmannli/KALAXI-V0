"""
proverb_reader.py — Extract all proverbs from R7M/WISDOM_CANON.md.

Parses both regular proverbs (P#XXXX - text) and emergent proverbs
(P#EMERGE-XXXX [PROVISIONAL] with metadata fields).
Captures LAYER context for each proverb.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path
from typing import List, Tuple

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


# Regex for regular proverbs: P#0001 - text  or  P#3328 – "text"
RE_PROVERB = re.compile(
    r'^(P#\d{4})\s*[-–]\s*"?(.+?)"?\s*$'
)

# Regex for emergent proverbs: P#EMERGE-0001 [PROVISIONAL]
RE_EMERGE = re.compile(
    r'^(P#EMERGE-\d{4})\s*\[PROVISIONAL\]'
)

# Regex for LAYER headers
RE_LAYER = re.compile(
    r'^LAYER\s+(\w+):\s+(.+?)(?:\s+\(P#.+\))?\s*$'
)

# Wisdom theme keywords for clustering
THEME_KEYWORDS = {
    "dignity": ["dignity", "worth", "respect", "person", "human"],
    "agency": ["choose", "act", "decide", "own", "power", "will"],
    "legibility": ["see", "read", "hear", "witness", "visible", "recognize"],
    "wound": ["wound", "break", "hurt", "pain", "scar", "heal"],
    "flow": ["river", "water", "flow", "stream", "current", "tide"],
    "knot": ["knot", "tie", "bind", "thread", "rope", "weave"],
    "witness": ["witness", "testify", "record", "remember", "presence"],
    "silence": ["silence", "quiet", "still", "pause", "breath", "gap"],
    "time": ["time", "season", "wait", "patience", "pace", "slow"],
    "craft": ["build", "make", "tool", "hand", "skill", "work"],
}


class ProverbReader(BaseReader):
    """Extract all proverbs from R7M/WISDOM_CANON.md."""

    area_name = "proverbs"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.source_path = self.root / "R7M" / "WISDOM_CANON.md"

    def extract(self) -> AreaEssence:
        """Parse all proverbs and emergent proverbs from WISDOM_CANON.md."""
        area = AreaEssence(area=self.area_name)

        if not self.source_path.exists():
            area.meta_essence = "WISDOM_CANON.md not found"
            return area

        text = self.source_path.read_text(encoding="utf-8")
        lines = text.splitlines()

        current_layer = "unknown"
        entries = []
        emerge_entries = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Track current layer
            layer_match = RE_LAYER.match(line)
            if layer_match:
                current_layer = layer_match.group(1).lower()

            # Regular proverb
            proverb_match = RE_PROVERB.match(line)
            if proverb_match:
                pid = proverb_match.group(1)
                ptext = proverb_match.group(2).strip().rstrip('"')
                entries.append((pid, ptext, current_layer))
                i += 1
                continue

            # Emergent proverb (multi-line)
            emerge_match = RE_EMERGE.match(line)
            if emerge_match:
                pid = emerge_match.group(1)
                ptext, source, covenants = self._parse_emerge_block(lines, i + 1)
                emerge_entries.append((pid, ptext, source, covenants))
                i += 1
                continue

            i += 1

        # Build EssenceEntries for regular proverbs
        for pid, ptext, layer in entries:
            themes = self._classify_themes(ptext)
            motifs = self.detect_motifs(ptext)
            voice_markers = self.detect_voice_markers(ptext)

            entry = self.make_entry(
                source_path=f"R7M/WISDOM_CANON.md::{pid}",
                raw_excerpt=ptext,
                patterns=[f"LAYER:{layer}"] + [f"THEME:{t}" for t in themes],
                essence=ptext,  # Proverbs ARE their own essence
                motifs=motifs,
                voice_markers=voice_markers,
                links=[pid],
                thermal_state="canonical",
            )
            area.entries.append(entry)

        # Build EssenceEntries for emergent proverbs
        for pid, ptext, source, covenants in emerge_entries:
            themes = self._classify_themes(ptext)
            motifs = self.detect_motifs(ptext)
            links = [pid] + covenants

            entry = self.make_entry(
                source_path=f"R7M/WISDOM_CANON.md::{pid}",
                raw_excerpt=ptext,
                patterns=["PROVISIONAL"] + [f"THEME:{t}" for t in themes],
                essence=ptext,
                motifs=motifs,
                voice_markers=self.detect_voice_markers(ptext),
                links=links,
                thermal_state="witnessed",  # provisional = not yet canonical
            )
            area.entries.append(entry)

        # Statistics
        area.statistics = {
            "total_proverbs": len(entries),
            "emergent_proverbs": len(emerge_entries),
            "total_extracted": len(area.entries),
            "layers": self._count_layers(entries),
            "theme_distribution": self._theme_distribution(area.entries),
        }

        # Meta-patterns
        if area.entries:
            all_themes = []
            for e in area.entries:
                all_themes.extend(
                    p.split(":")[1] for p in e.patterns if p.startswith("THEME:")
                )
            if all_themes:
                from collections import Counter
                top = Counter(all_themes).most_common(3)
                area.meta_patterns = [f"{t}:{c}" for t, c in top]

        area.meta_essence = (
            f"{len(area.entries)} proverbs extracted from WISDOM_CANON.md — "
            f"the system's compressed wisdom across {len(set(l for _, _, l in entries))} layers"
        )

        return area

    def _parse_emerge_block(
        self, lines: List[str], start: int
    ) -> Tuple[str, str, List[str]]:
        """Parse metadata fields after an EMERGE proverb header."""
        ptext = ""
        source = ""
        covenants = []

        for i in range(start, min(start + 5, len(lines))):
            line = lines[i].strip()
            if not line:
                break
            if line.startswith("text:"):
                ptext = line[5:].strip()
            elif line.startswith("source:"):
                source = line[7:].strip()
            elif line.startswith("linked_covenants:"):
                raw = line[17:].strip().strip("[]")
                covenants = [c.strip() for c in raw.split(",") if c.strip()]

        return ptext, source, covenants

    @staticmethod
    def _classify_themes(text: str) -> List[str]:
        """Classify a proverb into themes based on keyword presence."""
        lower = text.lower()
        themes = []
        for theme, keywords in THEME_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                themes.append(theme)
        return themes if themes else ["general"]

    @staticmethod
    def _count_layers(entries: List[Tuple[str, str, str]]) -> dict:
        """Count proverbs per layer."""
        counts = {}
        for _, _, layer in entries:
            counts[layer] = counts.get(layer, 0) + 1
        return counts

    @staticmethod
    def _theme_distribution(entries) -> dict:
        """Count entries per theme."""
        dist = {}
        for entry in entries:
            for p in entry.patterns:
                if p.startswith("THEME:"):
                    theme = p.split(":")[1]
                    dist[theme] = dist.get(theme, 0) + 1
        return dist
