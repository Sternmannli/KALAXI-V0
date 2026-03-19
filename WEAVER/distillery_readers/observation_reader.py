"""
observation_reader.py — Extract observations from R7M/OBSERVATIONS/.

Each OBS-XXX.md is an empirical observation of AI system behavior.
Varying formats but consistent: title, date, voice, condition, observation/finding.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path
from typing import List, Dict

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


RE_OBS_FILE = re.compile(r'^OBS-(\d+)\.md$')
RE_TITLE = re.compile(r'^#\s+OBS-\d+\s*[—–-]\s*(.+)$')


class ObservationReader(BaseReader):
    """Extract empirical observations from R7M/OBSERVATIONS/."""

    area_name = "observations"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.obs_dir = self.root / "R7M" / "OBSERVATIONS"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.obs_dir.exists():
            area.meta_essence = "OBSERVATIONS directory not found"
            return area

        obs_files = sorted(
            f for f in self.obs_dir.iterdir()
            if f.is_file() and RE_OBS_FILE.match(f.name)
        )

        for obs_file in obs_files:
            obs_id = RE_OBS_FILE.match(obs_file.name).group(1)
            text = obs_file.read_text(encoding="utf-8")
            lines = text.splitlines()

            title = self._extract_title(lines)
            metadata = self._extract_metadata(lines)
            body = text

            # Evidence directory
            evidence_dir = self.obs_dir / f"OBS-{obs_id}-evidence"
            has_evidence = evidence_dir.exists() and any(evidence_dir.iterdir())

            patterns = []
            if metadata.get("classification"):
                patterns.append(f"CLASSIFICATION:{metadata['classification']}")
            if metadata.get("status"):
                patterns.append(f"STATUS:{metadata['status']}")
            if has_evidence:
                patterns.append("HAS_EVIDENCE")

            # Essence: title + key finding
            essence = title
            significance = metadata.get("significance", "")
            if significance:
                essence = f"{title} — {significance[:150]}"

            entry = self.make_entry(
                source_path=f"R7M/OBSERVATIONS/OBS-{obs_id}.md",
                raw_excerpt=self.truncate(body, 500),
                patterns=patterns,
                essence=essence,
                motifs=self.detect_motifs(body),
                voice_markers=[],
                links=[f"OBS-{obs_id}"],
                thermal_state="witnessed",
            )
            area.entries.append(entry)

        area.statistics = {
            "total_observations": len(area.entries),
            "with_evidence": sum(
                1 for e in area.entries if "HAS_EVIDENCE" in e.patterns
            ),
        }

        area.meta_essence = (
            f"{len(area.entries)} empirical observations — "
            f"documented instances of AI system behavior under KALAXI conditions"
        )

        return area

    @staticmethod
    def _extract_title(lines: List[str]) -> str:
        """Extract title from first heading."""
        for line in lines:
            match = RE_TITLE.match(line.strip())
            if match:
                return match.group(1).strip()
        return "Untitled observation"

    @staticmethod
    def _extract_metadata(lines: List[str]) -> Dict:
        """Extract key metadata fields from observation."""
        metadata = {}
        for line in lines:
            stripped = line.strip()
            lower = stripped.lower()

            # Bold field format: **Key:** Value
            bold_match = re.match(r'^\*\*(.+?):?\*\*:?\s*(.+)$', stripped)
            if bold_match:
                key = bold_match.group(1).strip().lower()
                value = bold_match.group(2).strip()
                metadata[key] = value
                continue

            # Simple field format: Key: Value
            if ":" in stripped and not stripped.startswith("#"):
                key, _, value = stripped.partition(":")
                key = key.strip().lower()
                value = value.strip()
                if key in ("date", "voice", "condition", "status",
                           "classification", "significance", "analyst"):
                    metadata[key] = value

        return metadata
