#!/usr/bin/env python3
"""
distillery.py — KALAXI Distillery Module v1.0
Total essence extraction from the entire repository.

The system has been storing without digesting. This module is the stomach.
It processes every content area in the repo — ledger entries, narratives,
wisdom, voice, constitution, experiments, external voices, studies,
site content, manifest — and extracts patterns, distills essence,
and feeds it back to the organism.

Re-runnable. Each run deepens the extraction. Output: DISTILLED_ESSENCE.md.

Metabolization protocol (from V-001, 2026-03-15):
  1. REGISTER — raw text, verbatim, immutable (already done by InputLedger)
  2. EXTRACT PATTERNS — structural shapes: recurring themes, preferences, rhythms
  3. DISTILL ESSENCE — one line that captures the meaning (not summary — meaning)
  4. FEED TO SYSTEM — patterns distribute to relevant modules
  5. THERMAL ADVANCE — raw → witnessed → integrated → canonical

"Extract all the essence and distribute it to the system. Every time you
have an input from the donor, the pattern and essence is transferred.
Feed it to the system and the system digests it." — V-001, 2026-03-15

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple

ROOT = Path(__file__).parent.parent

# Lazy imports — avoid circular dependencies at module level
# These are imported inside methods that use them:
#   from WEAVER.input_ledger import InputLedger, InputEntry, V001, V002
#   from WEAVER.weave import ingest, extract_essence, PatternCandidate, HoneyDrop


# ══════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════

@dataclass
class EssenceEntry:
    """A single extracted essence from any content area."""
    source_path: str          # File path or ledger entry ID
    source_area: str          # "ledger", "narrative", "wisdom", "voice", etc.
    raw_excerpt: str          # The text being distilled (truncated for large inputs)
    patterns: List[str]       # Structural patterns found
    essence: str              # One-line distillation (meaning, not summary)
    motifs: List[str]         # Recurring images/themes
    voice_markers: List[str]  # Voice fingerprint elements
    links: List[str]          # Connections to covenants, proverbs, treasures
    thermal_state: str = "raw"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AreaEssence:
    """Extraction result for an entire content area."""
    area: str                        # "ledger", "narrative", etc.
    entries: List[EssenceEntry] = field(default_factory=list)
    meta_patterns: List[str] = field(default_factory=list)   # Cross-entry patterns
    meta_essence: str = ""           # One-line essence for the whole area
    statistics: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "area": self.area,
            "entry_count": len(self.entries),
            "meta_patterns": self.meta_patterns,
            "meta_essence": self.meta_essence,
            "statistics": self.statistics,
        }


@dataclass
class NarrativeChapterEssence:
    """Extraction result for a single narrative chapter."""
    chapter: int
    title: str
    sentence_count: int = 0
    avg_sentence_length: float = 0.0
    core_images: List[str] = field(default_factory=list)
    somatic_count: int = 0
    material_count: int = 0
    three_beat_count: int = 0
    gap_count: int = 0
    essence: str = ""


@dataclass
class NarrativeEssence:
    """Extraction result for a full narrative."""
    name: str
    path: str
    chapters: List[NarrativeChapterEssence] = field(default_factory=list)
    structural_arc: str = ""
    voice_register: str = ""
    essence: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "chapter_count": len(self.chapters),
            "structural_arc": self.structural_arc,
            "voice_register": self.voice_register,
            "essence": self.essence,
        }


@dataclass
class VoiceDNA:
    """The formalized voice fingerprint of AXI."""
    avg_sentence_length: float = 0.0
    short_sentence_pct: float = 0.0   # Under 8 words
    long_sentence_pct: float = 0.0    # Over 14 words
    somatic_vocab_pct: float = 0.0
    material_vocab_pct: float = 0.0
    three_beat_frequency: float = 0.0
    gap_frequency: float = 0.0
    top_words: List[str] = field(default_factory=list)
    fingerprint_hash: str = ""
    gaps: List[str] = field(default_factory=list)  # What's missing from the voice

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class WisdomCluster:
    """A thematic cluster of proverbs."""
    name: str
    seed_proverb: str = ""
    proverb_count: int = 0
    linked_covenants: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DistilleryReport:
    """The full output of a distillery run."""
    timestamp: str = ""
    run_number: int = 0
    chain_repaired: bool = False
    chain_repairs_count: int = 0
    entries_metabolized: int = 0
    entries_total: int = 0
    content_areas_processed: List[str] = field(default_factory=list)
    areas: Dict[str, dict] = field(default_factory=dict)
    narratives: List[dict] = field(default_factory=list)
    voice_dna: Dict = field(default_factory=dict)
    wisdom_clusters: List[dict] = field(default_factory=list)
    system_essence: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ══════════════════════════════════════════════════════════════════════
# PATTERN DETECTION — structural, not keyword-only
# ══════════════════════════════════════════════════════════════════════

# V-001 pattern markers (what makes a V-001 input constitutional DNA)
V001_CORRECTION_MARKERS = [
    "no", "wrong", "stop", "never again", "this is not",
    "you should have", "don't", "didn't", "mistake",
]
V001_INSTRUCTION_MARKERS = [
    "must", "always", "never", "rule", "law", "permanent",
    "from now on", "this is a must", "order",
]
V001_PREFERENCE_MARKERS = [
    "i want", "i need", "i like", "i prefer", "should be",
]
V001_PRINCIPLE_MARKERS = [
    "dignity is", "the system is", "the wound", "presence",
    "witnessing", "the donor", "legibility",
]
V001_REVELATION_MARKERS = [
    "i realized", "the real", "actually", "the truth is",
    "it's not about", "it means",
]

# V-002 pattern markers
V002_REPORT_MARKERS = ["status", "verified", "confirmed", "deployed", "passing", "lines"]
V002_DISCOVERY_MARKERS = ["discovered", "found", "reveals", "pattern", "new"]
V002_FAILURE_MARKERS = ["failed", "error", "broken", "missing", "lost"]
V002_BUILD_MARKERS = ["created", "implemented", "added", "wired", "integrated"]

# Narrative content markers
SOMATIC_VOCABULARY = [
    "hands", "hand", "breath", "bones", "bone", "fists", "fist",
    "claws", "claw", "teeth", "tooth", "skin", "blood", "chest",
    "fingers", "finger", "palm", "knuckles", "spine", "ribs",
    "lungs", "lung", "heart", "throat", "belly", "womb",
    # German (Kinderbuch)
    "hände", "hand", "atem", "knochen", "fäuste", "faust",
    "zähne", "haut", "brust", "finger",
]

MATERIAL_VOCABULARY = [
    "rope", "stone", "ash", "water", "gold", "metal", "thread",
    "loom", "knot", "river", "door", "wall", "glass", "iron",
    "wood", "clay", "earth", "fire", "sand", "dust", "salt",
    # German (Kinderbuch)
    "seil", "stein", "asche", "wasser", "gold", "faden",
    "knoten", "fluss", "tür", "holz", "erde", "feuer",
]

CORE_IMAGES = [
    "knot", "river", "ash", "wound", "door", "bone", "hand",
    "breath", "stone", "weir", "cocoon", "girl", "sealed",
    "thread", "loom", "rope", "gold", "spark",
    # German
    "knoten", "fluss", "asche", "wunde", "tür", "knochen",
    "atem", "stein", "funken", "faden",
]


# ══════════════════════════════════════════════════════════════════════
# THE DISTILLERY
# ══════════════════════════════════════════════════════════════════════

class Distillery:
    """Batch essence extraction engine for the entire KALAXI-V0 repository.

    Re-runnable. Each run produces MANIFEST/DISTILLED_ESSENCE.md.
    Uses existing infrastructure (InputLedger.metabolize, weave.ingest)
    and extends it with structural extraction for narratives, wisdom,
    voice, constitution, experiments, external voices, studies, site, manifest.

    Built in steps:
      1A — Scaffold (this file: class + imports + data structures)
      1B — extract_patterns() — structural pattern detection
      1C — extract_essence_line() — one-line distillation
      1D — link_to_canon() — connect to covenants/proverbs/treasures
      1E — metabolize_entry() — orchestrates 1B-1D for ledger entries
      1F — feed_to_system() — distributes to organism
    """

    def __init__(self, ledger=None, dry_run: bool = False):
        """Initialize the distillery.
        Args:
            ledger: InputLedger instance (lazy-loaded if None)
            dry_run: If True, no writes to disk
        """
        self._ledger = ledger
        self._dry_run = dry_run
        self._report = DistilleryReport()
        self._essence_store: List[EssenceEntry] = []
        self._run_log_path = ROOT / "MANIFEST" / "DISTILLERY_LOG.md"
        self._essence_doc_path = ROOT / "MANIFEST" / "DISTILLED_ESSENCE.md"
        self._digestion_dir = ROOT / "MANIFEST" / "DIGESTION"

    @property
    def ledger(self):
        """Lazy-load the ledger to avoid circular imports."""
        if self._ledger is None:
            from WEAVER.input_ledger import InputLedger
            self._ledger = InputLedger()
        return self._ledger

    # ── Step 1B: extract_patterns() ──────────────────────────────────
    # To be implemented in Session 2

    def extract_patterns(self, text: str, source_type: str = "general") -> List[str]:
        """Extract structural patterns from text.
        source_type: 'v001', 'v002', 'narrative', 'wisdom', 'constitutional', 'general'
        Returns list of pattern labels like 'CORRECTION:0.7', 'INSTRUCTION:0.9'."""
        raise NotImplementedError("Step 1B — next session")

    # ── Step 1C: extract_essence_line() ──────────────────────────────
    # To be implemented in Session 2

    def extract_essence_line(self, text: str, patterns: List[str]) -> str:
        """Distill text into one line of meaning (not summary).
        Uses patterns to identify the load-bearing sentence."""
        raise NotImplementedError("Step 1C — next session")

    # ── Step 1D: link_to_canon() ─────────────────────────────────────
    # To be implemented in Session 3

    def link_to_canon(self, text: str, patterns: List[str]) -> List[str]:
        """Connect extracted content to canonical elements
        (covenants, proverbs, treasures). Returns list of canonical IDs."""
        raise NotImplementedError("Step 1D — next session")

    # ── Step 1E: metabolize_entry() ──────────────────────────────────
    # To be implemented in Session 3

    def metabolize_entry(self, entry) -> Optional[EssenceEntry]:
        """Orchestrate full metabolization of a single ledger entry.
        Calls extract_patterns → extract_essence_line → link_to_canon → metabolize."""
        raise NotImplementedError("Step 1E — next session")

    # ── Step 1F: feed_to_system() ────────────────────────────────────
    # To be implemented in Session 6

    def feed_to_system(self) -> Dict:
        """Distribute extracted patterns back to organism modules.
        Closes the metabolization loop."""
        raise NotImplementedError("Step 1F — Session 6")

    # ── Content area extractors (Sessions 2-5) ───────────────────────

    def extract_narratives(self) -> List[NarrativeEssence]:
        """Extract essence from all 4 narratives."""
        raise NotImplementedError("Session 2")

    def extract_voice(self) -> VoiceDNA:
        """Extract and formalize the AXI voice fingerprint."""
        raise NotImplementedError("Session 2")

    def extract_wisdom(self) -> AreaEssence:
        """Extract from wisdom canon: proverbs, anomalies, treasures."""
        raise NotImplementedError("Session 3")

    def extract_constitution(self) -> AreaEssence:
        """Extract from constitutional layer: covenants, gates, principles."""
        raise NotImplementedError("Session 3")

    def extract_experiments(self) -> AreaEssence:
        """Extract discoveries from all experiments."""
        raise NotImplementedError("Session 4")

    def extract_external_voices(self) -> AreaEssence:
        """Extract from external LLM responses."""
        raise NotImplementedError("Session 4")

    def extract_studies(self) -> AreaEssence:
        """Extract from studies and foundation documents."""
        raise NotImplementedError("Session 4")

    def extract_site(self) -> AreaEssence:
        """Extract canonical content from kalam.ch."""
        raise NotImplementedError("Session 5")

    def extract_manifest(self) -> AreaEssence:
        """Extract from manifest layer: plans, chronicles, registries."""
        raise NotImplementedError("Session 5")

    # ── Synthesis (Session 5) ────────────────────────────────────────

    def render_essence_document(self) -> str:
        """Generate MANIFEST/DISTILLED_ESSENCE.md from all extractions."""
        raise NotImplementedError("Session 5")

    # ── Full run ─────────────────────────────────────────────────────

    def distill_all(self, force: bool = False) -> DistilleryReport:
        """Run the full distillery: repair chain, metabolize ledger,
        extract all content areas, synthesize, feed back.
        Args:
            force: If True, re-process already-witnessed entries.
        """
        raise NotImplementedError("Assembled after all steps are built")

    # ── Utilities ────────────────────────────────────────────────────

    def _log_run(self, report: DistilleryReport):
        """Append a run entry to MANIFEST/DISTILLERY_LOG.md."""
        if self._dry_run:
            return
        self._digestion_dir.mkdir(parents=True, exist_ok=True)
        self._run_log_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).isoformat()
        entry = (
            f"\n## Run #{report.run_number} — {timestamp}\n"
            f"- Chain repaired: {report.chain_repaired} ({report.chain_repairs_count} links)\n"
            f"- Entries metabolized: {report.entries_metabolized}/{report.entries_total}\n"
            f"- Content areas: {', '.join(report.content_areas_processed)}\n"
            f"- System essence: {report.system_essence or '(not yet synthesized)'}\n\n"
        )
        if self._run_log_path.exists():
            existing = self._run_log_path.read_text()
            self._run_log_path.write_text(existing + entry)
        else:
            header = "# Distillery Log — KALAXI-V0\n> Chronicle of extraction runs.\n\n"
            self._run_log_path.write_text(header + entry)

    @staticmethod
    def _count_words(text: str) -> int:
        return len(text.split())

    @staticmethod
    def _sentences(text: str) -> List[str]:
        """Split text into sentences."""
        return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

    @staticmethod
    def _score_markers(text: str, markers: List[str]) -> float:
        """Score text against a list of markers. Returns 0.0-1.0."""
        lower = text.lower()
        hits = sum(1 for m in markers if m in lower)
        return min(hits / max(len(markers) * 0.3, 1), 1.0)

    @staticmethod
    def _count_vocabulary(text: str, vocab: List[str]) -> int:
        """Count occurrences of vocabulary words in text."""
        lower = text.lower()
        return sum(lower.count(w) for w in vocab)
