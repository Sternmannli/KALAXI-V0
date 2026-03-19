"""
protocol_reader.py — Extract operational protocols from PROTOCOLS/.

9 documents: Bootstrap, BoyGenius Activation, Organ Map, Probe Forge,
Probe Design Consultation, Stress Test 001, Witness Prompts V1/V2/V3.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


class ProtocolReader(BaseReader):
    """Extract operational protocols from PROTOCOLS/."""

    area_name = "protocols"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.proto_dir = self.root / "PROTOCOLS"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.proto_dir.exists():
            area.meta_essence = "PROTOCOLS directory not found"
            return area

        md_files = sorted(
            f for f in self.proto_dir.iterdir()
            if f.is_file() and f.suffix == ".md"
        )

        for filepath in md_files:
            text = filepath.read_text(encoding="utf-8")
            lines = text.splitlines()

            title = self._extract_title(lines, filepath.stem)
            first_para = self._first_paragraph(lines)

            patterns = ["PROTOCOL"]
            if "witness" in filepath.name.lower():
                patterns.append("WITNESS")
            if "probe" in filepath.name.lower():
                patterns.append("PROBE")
            if "stress" in filepath.name.lower():
                patterns.append("STRESS_TEST")

            essence = f"{title}: {first_para[:200]}" if first_para else title

            entry = self.make_entry(
                source_path=f"PROTOCOLS/{filepath.name}",
                raw_excerpt=self.truncate(text, 500),
                patterns=patterns,
                essence=essence,
                motifs=self.detect_motifs(text),
                voice_markers=self.detect_voice_markers(text),
                links=[f"PROTO:{filepath.stem}"],
                thermal_state="witnessed",
            )
            area.entries.append(entry)

        area.statistics = {"total_protocols": len(area.entries)}

        area.meta_essence = (
            f"{len(area.entries)} operational protocols — "
            f"activation sequences, witness prompts, testing frameworks"
        )

        return area

    @staticmethod
    def _extract_title(lines, fallback):
        for line in lines:
            if line.strip().startswith("# "):
                return line.strip()[2:].strip()
        return fallback.replace("_", " ")

    @staticmethod
    def _first_paragraph(lines):
        para = []
        started = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if started and para:
                    break
                continue
            if stripped.startswith("#"):
                continue
            started = True
            para.append(stripped)
        return " ".join(para)
