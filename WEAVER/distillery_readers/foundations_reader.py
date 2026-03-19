"""
foundations_reader.py — Extract structural concepts from FOUNDATIONS/.

FOUNDATIONS/ contains 9 concept files (630 lines total):
- decay_function.md (86): Halflife logic — patterns recede, never vanish
- dignity_latency.md (72): T_d variable — biological velocity
- invariant_principle.md (22): Regulated oscillation as stability source
- metabolism.md (22): System as complete metabolic cycle
- paremiology.md (79): Science of proverbs — 40,000 year tradition
- proprioception_axiom.md (78): Middle layer relay — system feeling itself
- proposal_evaluation_2026-03-10.md (84): Evaluation of decay + T_d proposals
- witness_scale.md (86): W-0 through W-5 — witnessing measurement
- COV008_COV015_PENDING.md (9): Right to Remedy + Donor Data Sovereignty

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from pathlib import Path

from WEAVER.distillery import AreaEssence, ROOT
from WEAVER.distillery_readers.base import BaseReader


# Map filenames to pre-distilled essences (each read by V-002)
_FOUNDATIONS_ESSENCE = {
    "decay_function": (
        "Halflife logic: patterns recede but never vanish. "
        "W(t) = W_0 × 0.5^(t/90). Deep Hum after 300 days of silence."
    ),
    "dignity_latency": (
        "Dignity-latency T_d: the system responds at biological velocity. "
        "Speed is the enemy of agency. 0.5s–30s proportional to complexity."
    ),
    "invariant_principle": (
        "Long-term stability emerges from regulated oscillation. "
        "Gap, thermal delay, weakest-voice-first, absurdity queue — all embody this."
    ),
    "metabolism": (
        "Kalaxi as metabolism: intake, breakdown, transformation, release, "
        "waste retention, self-measurement, homeostasis. Structural isomorphism."
    ),
    "paremiology": (
        "Science of proverbs: 40,000-year tradition. Locked image pair, "
        "script opposition, minimal frame. Kalaxi continues indigenous compression."
    ),
    "proprioception_axiom": (
        "Proprioception axiom: if the relay stops, the system has lost self-sensation. "
        "Same tier as Sealed Gate. Not communication — the system feeling its own body."
    ),
    "proposal_evaluation_2026-03-10": (
        "Evaluation of decay function + dignity-latency T_d. "
        "Together they implement a temporal dignity layer — respecting time in both directions."
    ),
    "witness_scale": (
        "Witness Scale W-0 through W-5: UNSEEN, PASSED, FLAGGED, SEEN, HELD, EMBODIED. "
        "Not quality — degree of witnessing. Once seen (W-3), irreversible."
    ),
    "COV008_COV015_PENDING": (
        "COV#008: Right to Remedy — failure results in shelter, not ejection. "
        "COV#015: Donor Data Sovereignty — consent is comprehension, not checkbox."
    ),
}


class FoundationsReader(BaseReader):
    """Extract structural concepts from FOUNDATIONS/."""

    area_name = "foundations"

    def __init__(self, root: Path = ROOT):
        super().__init__(root)
        self.foundations_dir = self.root / "FOUNDATIONS"

    def extract(self) -> AreaEssence:
        area = AreaEssence(area=self.area_name)

        if not self.foundations_dir.exists():
            area.statistics = {"total_entries": 0}
            area.meta_essence = "No FOUNDATIONS/ directory found"
            return area

        for filepath in sorted(self.foundations_dir.glob("*.md")):
            text = filepath.read_text(encoding="utf-8")
            lines = text.splitlines()
            title = self._extract_title(lines, filepath.stem)
            stem = filepath.stem

            # Status detection
            status = "witnessed"
            lower_text = text.lower()
            if "ratified" in lower_text:
                status = "canonical"
            elif "axiom" in lower_text:
                status = "canonical"
            elif "pending" in lower_text or "provisional" in lower_text:
                status = "witnessed"

            # Pattern classification
            patterns = ["FOUNDATION"]
            if "axiom" in lower_text:
                patterns.append("AXIOM")
            if "covenant" in lower_text or "cov#" in lower_text:
                patterns.append("COVENANT_RELATED")
            if "decay" in lower_text or "halflife" in lower_text:
                patterns.append("TEMPORAL")
            if "dignity" in lower_text or "d = a" in lower_text:
                patterns.append("DIGNITY")
            if "witness" in lower_text and "scale" in lower_text:
                patterns.append("MEASUREMENT")
            if "proverb" in lower_text or "paremiology" in lower_text:
                patterns.append("WISDOM")
            if "metabolism" in lower_text:
                patterns.append("ORGANIC")
            if "proprioception" in lower_text:
                patterns.append("SELF_SENSATION")

            # Use pre-distilled essence or fallback
            essence = _FOUNDATIONS_ESSENCE.get(stem, f"{title} — structural concept")

            entry = self.make_entry(
                source_path=f"FOUNDATIONS/{filepath.name}",
                raw_excerpt=self.truncate(text, 500),
                patterns=patterns,
                essence=essence,
                motifs=self.detect_motifs(text),
                voice_markers=self.detect_voice_markers(text),
                links=self._build_links(stem, text),
                thermal_state=status,
            )
            area.entries.append(entry)

        area.statistics = {
            "total_entries": len(area.entries),
            "canonical": sum(1 for e in area.entries if e.thermal_state == "canonical"),
            "witnessed": sum(1 for e in area.entries if e.thermal_state == "witnessed"),
        }

        area.meta_essence = (
            f"{len(area.entries)} foundational concepts — "
            f"decay function, dignity-latency, invariant principle, metabolism, "
            f"paremiology, proprioception axiom, witness scale, pending covenants"
        )

        return area

    @staticmethod
    def _extract_title(lines, fallback):
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
        return fallback.replace("_", " ").title()

    @staticmethod
    def _build_links(stem, text):
        links = [f"FOUNDATIONS:{stem}"]
        lower = text.lower()

        if "cov#001" in lower or "dignity-first" in lower:
            links.append("STONE:COV001")
        if "cov#004" in lower or "append-only" in lower:
            links.append("STONE:COV004")
        if "cov#006" in lower:
            links.append("STONE:COV006")
        if "cov#008" in lower:
            links.append("STONE:COV008")
        if "cov#009" in lower:
            links.append("STONE:COV009")
        if "cov#015" in lower:
            links.append("STONE:COV015")
        if "sealed gate" in lower:
            links.append("STONE:sealed_gate")
        if "breath" in lower:
            links.append("WEAVER:breath")
        if "oracle" in lower or "gap#019" in lower:
            links.append("STONE:GAP019")

        return links
