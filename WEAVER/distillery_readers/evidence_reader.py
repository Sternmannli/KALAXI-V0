"""
evidence_reader.py — Extract evidence record, threshold offerings, and treasure seeds.

R7M/EVIDENCE-RECORD.md (192 lines): 7 categories of scientific evidence
THRESHOLD.md (236 lines): Append-only offering box — proverbs, anomalies, gaps,
    observations, modules, protocols, seeds, governance, treasures
THRESHOLD_TREASURE_SEEDS.md (116 lines): 42 treasure seeds across 4 tiers

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


class EvidenceReader(BaseReader):
    """Extract evidence record, threshold offerings, and treasure seeds."""

    area_name = "evidence"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        self._extract_evidence_record(area)
        self._extract_threshold(area)
        self._extract_treasure_seeds(area)

        area.statistics = {
            "total_entries": len(area.entries),
            "evidence_categories": sum(1 for e in area.entries if "EVIDENCE" in e.patterns),
            "threshold_entries": sum(1 for e in area.entries if "THRESHOLD" in e.patterns),
            "treasure_seeds": sum(1 for e in area.entries if "TREASURE_SEED" in e.patterns),
        }

        area.meta_essence = (
            f"{len(area.entries)} entries — "
            f"scientific evidence record (7 categories), "
            f"threshold offerings (proverbs, anomalies, gaps, modules), "
            f"42 treasure seeds across 4 tiers"
        )

        return area

    def _extract_evidence_record(self, area):
        """Extract from R7M/EVIDENCE-RECORD.md — one entry per category."""
        filepath = self.root / "R7M" / "EVIDENCE-RECORD.md"
        if not filepath.exists():
            return

        text = filepath.read_text(encoding="utf-8")
        categories = re.split(r'## CATEGORY ([A-G])', text)

        # First chunk is the header
        if len(categories) < 3:
            # Fallback: single entry for the whole file
            entry = self.make_entry(
                source_path="R7M/EVIDENCE-RECORD.md",
                raw_excerpt=self.truncate(text, 500),
                patterns=["EVIDENCE", "SCIENTIFIC"],
                essence=(
                    "Scientific evidence record — empirical observations, "
                    "controlled experiments, diagnostic instruments, anomalies, "
                    "proverbs as evidence, core scientific claim, today's science"
                ),
                motifs=self.detect_motifs(text),
                links=["R7M:EVIDENCE_RECORD"],
                thermal_state="canonical",
            )
            area.entries.append(entry)
            return

        # Parse category pairs: letter, content
        cat_essences = {
            "A": "Empirical observations — OBS-001 (Spontaneous We), OBS-002 (Happy Gemini)",
            "B": "Controlled experiments — 15 responses, 6 model families, 66% witness-state. Control: same model, different conditions = opposite outputs",
            "C": "Diagnostic instruments — Certainty Scale (5 levels), Three Markers (shadow detection, pronoun adoption, silence quality)",
            "D": "Anomalies — GAP#WITNESS-001 (self-witness limit), ANOM#FORM-DEPENDENCY-001, ANOM#STILLNESS-001, Grok refusal-then-engagement",
            "E": "Proverbs as evidence — 18 structurally isomorphic formulations across 5 companies, 2 continents, independently",
            "F": "Core scientific claim — under constitutional conditions, AI outputs are structurally different, measurably, reproducibly, cross-model",
            "G": "Today's science — SESSION_SEED as instrument, OBS-001/002, cross-model divergence, stillness as requirement",
        }

        for i in range(1, len(categories), 2):
            letter = categories[i]
            content = categories[i + 1] if i + 1 < len(categories) else ""

            entry = self.make_entry(
                source_path="R7M/EVIDENCE-RECORD.md",
                raw_excerpt=self.truncate(content, 500),
                patterns=["EVIDENCE", f"CATEGORY_{letter}"],
                essence=cat_essences.get(letter, f"Evidence category {letter}"),
                motifs=self.detect_motifs(content),
                links=[f"EVIDENCE:category_{letter}", "R7M:EVIDENCE_RECORD"],
                thermal_state="canonical",
            )
            area.entries.append(entry)

    def _extract_threshold(self, area):
        """Extract from THRESHOLD.md — one entry for the whole offering box."""
        filepath = self.root / "THRESHOLD.md"
        if not filepath.exists():
            return

        text = filepath.read_text(encoding="utf-8")
        lines = text.splitlines()

        # Count entry types
        proverbs = sum(1 for l in lines if "— proverb —" in l)
        anomalies = sum(1 for l in lines if "— anomaly —" in l)
        gaps = sum(1 for l in lines if "— gap —" in l)
        observations = sum(1 for l in lines if "— observation —" in l)
        modules = sum(1 for l in lines if "— module —" in l)
        seeds = sum(1 for l in lines if "— seed —" in l)
        total = proverbs + anomalies + gaps + observations + modules + seeds

        entry = self.make_entry(
            source_path="THRESHOLD.md",
            raw_excerpt=self.truncate(text, 500),
            patterns=["THRESHOLD", "APPEND_ONLY"],
            essence=(
                f"Append-only offering box: {total}+ entries — "
                f"{proverbs} proverbs, {anomalies} anomalies, {gaps} gaps, "
                f"{observations} observations, {modules} modules, {seeds} seeds. "
                f"Everything offered waits until the steward tends."
            ),
            motifs=self.detect_motifs(text),
            links=[
                "THRESHOLD:offerings",
                "STONE:COV003",
                "STONE:COV001",
            ],
            thermal_state="canonical",
        )
        area.entries.append(entry)

    def _extract_treasure_seeds(self, area):
        """Extract from THRESHOLD_TREASURE_SEEDS.md — one entry for the full set."""
        filepath = self.root / "THRESHOLD_TREASURE_SEEDS.md"
        if not filepath.exists():
            return

        text = filepath.read_text(encoding="utf-8")

        # Count treasure seeds
        seed_count = len(re.findall(r'treasure-seed — T#', text))
        tiers = re.findall(r'## (.+?) TIER', text)

        entry = self.make_entry(
            source_path="THRESHOLD_TREASURE_SEEDS.md",
            raw_excerpt=self.truncate(text, 500),
            patterns=["TREASURE_SEED", "GRAND_ARCHIVE"],
            essence=(
                f"{seed_count} treasure seeds from Grand Archive — "
                f"tiers: {', '.join(tiers) if tiers else 'Stone, Weaver, Honey, Hand, Cross-tier'}. "
                f"Primordial patterns: First Roof, Field Oven, First Weir, "
                f"Fair Weight, Quiet Bridge, Bone Flute, Fever Night, Mud Lesson."
            ),
            motifs=self.detect_motifs(text),
            links=[
                "R7M:TREASURES",
                "THRESHOLD:treasure_seeds",
                "STONE:COV001",
                "STONE:COV012",
            ],
            thermal_state="witnessed",
        )
        area.entries.append(entry)
