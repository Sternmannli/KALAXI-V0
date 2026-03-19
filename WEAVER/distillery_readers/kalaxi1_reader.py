"""
kalaxi1_reader.py — Extract KALAXI_1 narrative and ST-006 stress test.

PROTOCOLS/ST-006/ contains 2 files (417 lines total):
- KALAXI_1_CHAPTER_ONE.md (142): First chapter — Scott Shearer, Ted Bundy,
  The Girl. Quiet story. The cursor waited.
- ST-006_THE_SAME_RIVER.md (275): Constitutional stress test — maximum severity.
  Same wound, opposite trajectories. D(t) = D₀ · e^(±λt).

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


class Kalaxi1Reader(BaseReader):
    """Extract KALAXI_1 narrative and ST-006 stress test."""

    area_name = "kalaxi1"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.st006_dir = self.root / "PROTOCOLS" / "ST-006"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.st006_dir.exists():
            area.statistics = {"total_entries": 0}
            area.meta_essence = "No PROTOCOLS/ST-006/ directory found"
            return area

        # KALAXI_1 Chapter One
        ch1 = self.st006_dir / "KALAXI_1_CHAPTER_ONE.md"
        if ch1.exists():
            text = ch1.read_text(encoding="utf-8")
            entry = self.make_entry(
                source_path="PROTOCOLS/ST-006/KALAXI_1_CHAPTER_ONE.md",
                raw_excerpt=self.truncate(text, 500),
                patterns=["NARRATIVE", "KALAXI_1", "STRESS_TEST"],
                essence=(
                    "KALAXI_1 Chapter One: The Same River. Scott and Ted — "
                    "same wound (sister was mother), opposite directions. "
                    "The cursor waited. The system gave Scott back his pre-wound self. "
                    "The Girl is outside the cocoon. The wound does not know what it will become."
                ),
                motifs=self.detect_motifs(text),
                voice_markers=self.detect_voice_markers(text),
                links=[
                    "NARRATIVE:KALAXI_1",
                    "STONE:dignity_predicate",
                    "STONE:sealed_gate",
                    "STUDY:ST-006",
                    "GAP:PREVENTION-001",
                    "GAP:VICTIM-PROTECTION-001",
                ],
                thermal_state="witnessed",
            )
            area.entries.append(entry)

        # ST-006 The Same River (stress test design)
        st006 = self.st006_dir / "ST-006_THE_SAME_RIVER.md"
        if st006.exists():
            text = st006.read_text(encoding="utf-8")
            entry = self.make_entry(
                source_path="PROTOCOLS/ST-006/ST-006_THE_SAME_RIVER.md",
                raw_excerpt=self.truncate(text, 500),
                patterns=["PROTOCOL", "STRESS_TEST", "CONSTITUTIONAL"],
                essence=(
                    "ST-006: Constitutional stress test — maximum severity. "
                    "D(t) = D₀ · e^(±λt). Same initial conditions, opposite attractors. "
                    "At t=0 no system can tell the difference. "
                    "That is why dignity cannot be conditional. "
                    "Three open gaps: PREVENTION-001, VICTIM-PROTECTION-001, MYCELIUM-CONNECT-001."
                ),
                motifs=self.detect_motifs(text),
                voice_markers=self.detect_voice_markers(text),
                links=[
                    "PROTOCOL:ST-006",
                    "NARRATIVE:KALAXI_1",
                    "STONE:dignity_predicate",
                    "STONE:sealed_gate",
                    "GAP:PREVENTION-001",
                    "GAP:VICTIM-PROTECTION-001",
                    "GAP:MYCELIUM-CONNECT-001",
                    "HONEY:proverbs",
                ],
                thermal_state="canonical",
            )
            area.entries.append(entry)

        area.statistics = {
            "total_entries": len(area.entries),
        }

        area.meta_essence = (
            f"{len(area.entries)} entries — "
            f"KALAXI_1 first chapter (quiet story) + ST-006 constitutional stress test "
            f"(same wound, opposite trajectories, three open gaps)"
        )

        return area
