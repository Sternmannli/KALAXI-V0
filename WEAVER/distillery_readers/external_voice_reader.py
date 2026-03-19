"""
external_voice_reader.py — Extract external model responses from EXTERNAL_VOICES/.

9 model directories (CHATGPT, COPILOT, DEEPSEEK, EURIA, GEMINI, GROK, KIMI,
MANUS, PERPLEXITY) plus SUBMISSIONS/. Each contains EV-XXX-MODEL-DATE.md files.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


RE_EV_FILE = re.compile(r'^EV-(\d+)-(.+?)-.*\.md$')


class ExternalVoiceReader(BaseReader):
    """Extract external model responses from EXTERNAL_VOICES/."""

    area_name = "external_voices"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.ev_dir = self.root / "EXTERNAL_VOICES"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.ev_dir.exists():
            area.meta_essence = "EXTERNAL_VOICES directory not found"
            return area

        model_counts = {}

        # Walk all subdirectories for EV-*.md files
        ev_files = sorted(self.ev_dir.rglob("EV-*.md"))

        for filepath in ev_files:
            text = filepath.read_text(encoding="utf-8")
            rel_path = filepath.relative_to(self.root)

            # Extract model name from filename or parent directory
            match = RE_EV_FILE.match(filepath.name)
            if match:
                ev_num = match.group(1)
                model = match.group(2)
            else:
                ev_num = "000"
                model = filepath.parent.name

            model_counts[model] = model_counts.get(model, 0) + 1

            lines = text.splitlines()
            title = self._extract_title(lines, filepath.stem)
            first_para = self._first_paragraph(lines)

            patterns = [f"MODEL:{model}", f"EV:{ev_num}"]
            if "-B-" in filepath.name:
                patterns.append("ROUND_B")

            essence = f"{model} EV-{ev_num}: {first_para[:200]}" if first_para else f"{model} EV-{ev_num}"

            entry = self.make_entry(
                source_path=str(rel_path),
                raw_excerpt=self.truncate(text, 500),
                patterns=patterns,
                essence=essence,
                motifs=self.detect_motifs(text),
                links=[f"EV-{ev_num}", f"MODEL:{model}"],
                thermal_state="witnessed",
            )
            area.entries.append(entry)

        # Also read submissions
        submissions_dir = self.ev_dir / "SUBMISSIONS"
        if submissions_dir.exists():
            for filepath in sorted(submissions_dir.glob("*.md")):
                text = filepath.read_text(encoding="utf-8")
                rel_path = filepath.relative_to(self.root)
                lines = text.splitlines()
                title = self._extract_title(lines, filepath.stem)

                entry = self.make_entry(
                    source_path=str(rel_path),
                    raw_excerpt=self.truncate(text, 500),
                    patterns=["SUBMISSION"],
                    essence=f"Witness submission: {title}",
                    motifs=self.detect_motifs(text),
                    links=["SUBMISSION"],
                    thermal_state="witnessed",
                )
                area.entries.append(entry)

        area.statistics = {
            "total_entries": len(area.entries),
            "model_distribution": model_counts,
            "models_represented": len(model_counts),
        }

        area.meta_essence = (
            f"{len(area.entries)} external voice documents from "
            f"{len(model_counts)} models — multi-model convergence evidence"
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
