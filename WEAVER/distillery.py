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
    # Session C — implemented

    def extract_patterns(self, text: str, source_type: str = "general") -> List[str]:
        """Extract structural patterns from text.

        Different source types activate different marker sets:
        - v001: corrections, instructions, preferences, principles, revelations
        - v002: reports, discoveries, failures, builds
        - narrative: somatic vocabulary, material vocabulary, core images
        - wisdom: principles + resonance (proverb-like patterns)
        - constitutional: instructions + principles (law-like patterns)
        - general: all V-001 + V-002 markers at reduced weight

        Returns list of pattern labels like 'CORRECTION:0.72', 'INSTRUCTION:0.85'.
        Only patterns with score > 0.0 are returned.
        """
        if not text or not text.strip():
            return []

        results = []

        if source_type == "v001":
            # V-001 input: corrections, instructions, preferences, principles, revelations
            marker_sets = [
                ("CORRECTION", V001_CORRECTION_MARKERS),
                ("INSTRUCTION", V001_INSTRUCTION_MARKERS),
                ("PREFERENCE", V001_PREFERENCE_MARKERS),
                ("PRINCIPLE", V001_PRINCIPLE_MARKERS),
                ("REVELATION", V001_REVELATION_MARKERS),
            ]
            for label, markers in marker_sets:
                score = self._score_markers(text, markers)
                if score > 0.0:
                    results.append(f"{label}:{score:.2f}")

        elif source_type == "v002":
            # V-002 output: reports, discoveries, failures, builds
            marker_sets = [
                ("REPORT", V002_REPORT_MARKERS),
                ("DISCOVERY", V002_DISCOVERY_MARKERS),
                ("FAILURE", V002_FAILURE_MARKERS),
                ("BUILD", V002_BUILD_MARKERS),
            ]
            for label, markers in marker_sets:
                score = self._score_markers(text, markers)
                if score > 0.0:
                    results.append(f"{label}:{score:.2f}")

        elif source_type == "narrative":
            # Narrative text: somatic body, material grounding, core images
            word_count = max(self._count_words(text), 1)
            somatic = self._count_vocabulary(text, SOMATIC_VOCABULARY)
            material = self._count_vocabulary(text, MATERIAL_VOCABULARY)
            images = self._count_vocabulary(text, CORE_IMAGES)

            if somatic > 0:
                density = min(somatic / word_count * 10, 1.0)
                results.append(f"SOMATIC:{density:.2f}")
            if material > 0:
                density = min(material / word_count * 10, 1.0)
                results.append(f"MATERIAL:{density:.2f}")
            if images > 0:
                density = min(images / word_count * 10, 1.0)
                results.append(f"CORE_IMAGE:{density:.2f}")

            # Three-beat rhythm: sentences with exactly 3 clauses (comma-separated)
            sentences = self._sentences(text)
            if sentences:
                three_beats = sum(
                    1 for s in sentences if s.count(",") == 2
                )
                if three_beats > 0:
                    freq = min(three_beats / len(sentences), 1.0)
                    results.append(f"THREE_BEAT:{freq:.2f}")

            # Gap detection: em-dash, ellipsis, or "—" as pause/silence
            gap_count = text.count("—") + text.count("...") + text.count("…")
            if gap_count > 0:
                freq = min(gap_count / max(len(sentences), 1), 1.0)
                results.append(f"GAP:{freq:.2f}")

        elif source_type == "wisdom":
            # Wisdom/proverb text: principles + resonance patterns
            marker_sets = [
                ("PRINCIPLE", V001_PRINCIPLE_MARKERS),
                ("INSTRUCTION", V001_INSTRUCTION_MARKERS),
            ]
            for label, markers in marker_sets:
                score = self._score_markers(text, markers)
                if score > 0.0:
                    results.append(f"{label}:{score:.2f}")
            # Also check for core images (proverbs often use them)
            images = self._count_vocabulary(text, CORE_IMAGES)
            if images > 0:
                density = min(images / max(self._count_words(text), 1) * 10, 1.0)
                results.append(f"CORE_IMAGE:{density:.2f}")

        elif source_type == "constitutional":
            # Constitutional text: instructions + principles (law-like)
            marker_sets = [
                ("INSTRUCTION", V001_INSTRUCTION_MARKERS),
                ("PRINCIPLE", V001_PRINCIPLE_MARKERS),
                ("CORRECTION", V001_CORRECTION_MARKERS),
            ]
            for label, markers in marker_sets:
                score = self._score_markers(text, markers)
                if score > 0.0:
                    results.append(f"{label}:{score:.2f}")

        else:
            # General: run all V-001 and V-002 markers
            all_sets = [
                ("CORRECTION", V001_CORRECTION_MARKERS),
                ("INSTRUCTION", V001_INSTRUCTION_MARKERS),
                ("PREFERENCE", V001_PREFERENCE_MARKERS),
                ("PRINCIPLE", V001_PRINCIPLE_MARKERS),
                ("REVELATION", V001_REVELATION_MARKERS),
                ("REPORT", V002_REPORT_MARKERS),
                ("DISCOVERY", V002_DISCOVERY_MARKERS),
                ("FAILURE", V002_FAILURE_MARKERS),
                ("BUILD", V002_BUILD_MARKERS),
            ]
            for label, markers in all_sets:
                score = self._score_markers(text, markers)
                if score > 0.0:
                    results.append(f"{label}:{score:.2f}")

        return results

    # ── Step 1C: extract_essence_line() ──────────────────────────────
    # Session D — implemented

    def extract_essence_line(self, text: str, patterns: List[str]) -> str:
        """Distill text into one line of meaning (not summary — the meaning).

        Strategy: score each sentence against the detected patterns.
        The load-bearing sentence is the one most aligned with what
        the text IS (instruction, correction, narrative image, etc.).

        Scoring factors:
        1. Pattern alignment — sentence matches the dominant pattern type
        2. Brevity bonus — shorter sentences carry more weight (V-001 voice)
        3. Position — first and last sentences get a slight boost
        4. Density — more canonical vocabulary per word = more load-bearing

        Limitation: this picks the best existing sentence, not a creative
        rewrite. Automated extraction without an LLM cannot rephrase.
        """
        if not text or not text.strip():
            return ""

        sentences = self._sentences(text)
        if not sentences:
            # No sentence boundaries found — return truncated text
            return text.strip()[:200]

        if len(sentences) == 1:
            return sentences[0]

        # Parse dominant pattern type from patterns list
        # patterns look like "CORRECTION:0.72", "INSTRUCTION:0.85"
        dominant_type = ""
        dominant_score = 0.0
        for p in patterns:
            if ":" in p:
                ptype, pscore = p.split(":", 1)
                try:
                    sc = float(pscore)
                    if sc > dominant_score:
                        dominant_score = sc
                        dominant_type = ptype
                except ValueError:
                    pass

        # Build marker list for the dominant pattern type
        type_to_markers = {
            "CORRECTION": V001_CORRECTION_MARKERS,
            "INSTRUCTION": V001_INSTRUCTION_MARKERS,
            "PREFERENCE": V001_PREFERENCE_MARKERS,
            "PRINCIPLE": V001_PRINCIPLE_MARKERS,
            "REVELATION": V001_REVELATION_MARKERS,
            "REPORT": V002_REPORT_MARKERS,
            "DISCOVERY": V002_DISCOVERY_MARKERS,
            "FAILURE": V002_FAILURE_MARKERS,
            "BUILD": V002_BUILD_MARKERS,
            "SOMATIC": SOMATIC_VOCABULARY,
            "MATERIAL": MATERIAL_VOCABULARY,
            "CORE_IMAGE": CORE_IMAGES,
        }
        dominant_markers = type_to_markers.get(dominant_type, [])

        # Score each sentence
        best_sentence = sentences[0]
        best_score = -1.0

        for i, sent in enumerate(sentences):
            score = 0.0
            word_count = max(self._count_words(sent), 1)

            # Factor 1: pattern alignment (0-1)
            if dominant_markers:
                score += self._score_markers(sent, dominant_markers) * 2.0

            # Factor 2: brevity bonus — sentences 4-14 words score highest
            # Fragments (1-2 words) are penalized hard — "No." or "Stop."
            # are not essence, they are punctuation
            if 4 <= word_count <= 14:
                score += 1.0
            elif word_count <= 2:
                score -= 1.0  # Heavy penalty for fragments
            elif word_count == 3:
                score += 0.3
            else:
                # Diminishing score as length increases past 14
                score += max(0.1, 1.0 - (word_count - 14) * 0.05)

            # Factor 3: position — first and last sentences get a boost
            if i == 0:
                score += 0.5
            elif i == len(sentences) - 1:
                score += 0.3

            # Factor 4: canonical vocabulary density
            canon_hits = self._count_vocabulary(sent, CORE_IMAGES)
            canon_hits += self._count_vocabulary(sent, SOMATIC_VOCABULARY)
            if canon_hits > 0:
                score += min(canon_hits / word_count * 5, 1.0)

            if score > best_score:
                best_score = score
                best_sentence = sent

        return best_sentence

    # ── Step 1D: link_to_canon() ─────────────────────────────────────
    # Session E — implemented

    # Proverb cache — loaded once, reused across calls
    _proverb_cache: Optional[List[Dict]] = None

    # Stop words — too common to be meaningful for matching
    _STOP_WORDS = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "shall", "can",
        "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "as", "into", "through", "during", "before", "after", "it",
        "its", "this", "that", "these", "those", "i", "you", "he",
        "she", "we", "they", "me", "him", "her", "us", "them", "my",
        "your", "his", "our", "their", "not", "no", "and", "but",
        "or", "if", "then", "than", "so", "up", "out", "about",
    }

    def _load_proverbs(self) -> List[Dict]:
        """Load proverbs from site data. Cached after first load."""
        if Distillery._proverb_cache is not None:
            return Distillery._proverb_cache
        proverbs_path = ROOT / "site" / "public" / "data" / "proverbs.json"
        if proverbs_path.exists():
            Distillery._proverb_cache = json.loads(proverbs_path.read_text())
        else:
            Distillery._proverb_cache = []
        return Distillery._proverb_cache

    def _meaningful_words(self, text: str) -> set:
        """Extract meaningful (non-stop) words from text."""
        words = set(re.findall(r'[a-z]+', text.lower()))
        return words - self._STOP_WORDS

    def link_to_canon(self, text: str, patterns: List[str]) -> List[str]:
        """Connect extracted content to canonical elements.

        Two matching strategies:
        1. Proverb text overlap — keyword match against 166 proverbs
           in site/public/data/proverbs.json. Requires 2+ meaningful
           shared words for a link.
        2. Pattern-type inference — PRINCIPLE/INSTRUCTION patterns
           suggest covenant links; narrative patterns suggest treasure links.

        Returns list of canonical ID strings like 'P#0042', 'COV#003'.
        Capped at 5 links to avoid noise.
        """
        if not text or not text.strip():
            return []

        links = []
        text_words = self._meaningful_words(text)

        # Strategy 1: proverb text overlap
        proverbs = self._load_proverbs()
        for proverb in proverbs:
            proverb_text = proverb.get("text", "")
            proverb_words = self._meaningful_words(proverb_text)
            overlap = text_words & proverb_words
            # Require 2+ meaningful shared words (not just "begin" or "step")
            if len(overlap) >= 2:
                links.append(proverb["id"])

        # Strategy 2: pattern-type inference
        pattern_types = set()
        for p in patterns:
            if ":" in p:
                ptype = p.split(":")[0]
                pattern_types.add(ptype)

        if "PRINCIPLE" in pattern_types or "INSTRUCTION" in pattern_types:
            links.append("COV:linked")  # General covenant association
        if "SOMATIC" in pattern_types or "MATERIAL" in pattern_types:
            links.append("T:linked")    # Treasure association (narrative voice)
        if "FAILURE" in pattern_types:
            links.append("CORRECTION_LOG:linked")

        # Cap at 5 to avoid noise
        return links[:5]

    # ── Step 1E: metabolize_entry() ──────────────────────────────────
    # Session E — implemented

    def metabolize_entry(self, entry) -> Optional[EssenceEntry]:
        """Orchestrate full metabolization of a single ledger entry.

        Pipeline: extract_patterns → extract_essence_line → link_to_canon
        Then creates an EssenceEntry and returns it.

        Does NOT call ledger.metabolize() — that is done in batch by
        the caller (metabolize_ledger or distill_all) to avoid per-entry saves.

        Args:
            entry: An InputEntry from the ledger (has .raw_text, .voice, .entry_id)
        Returns:
            EssenceEntry if text is non-empty, None otherwise.
        """
        text = getattr(entry, "raw_text", "")
        if not text or not text.strip():
            return None

        # Determine source type from voice
        voice = getattr(entry, "voice", "")
        if voice == "V-001":
            source_type = "v001"
        elif voice == "V-002":
            source_type = "v002"
        else:
            source_type = "general"

        # Pipeline
        patterns = self.extract_patterns(text, source_type)
        essence = self.extract_essence_line(text, patterns)
        links = self.link_to_canon(text, patterns)

        # Extract motifs and voice markers from patterns
        motifs = []
        voice_markers = []
        for p in patterns:
            ptype = p.split(":")[0] if ":" in p else p
            if ptype in ("CORE_IMAGE", "SOMATIC", "MATERIAL"):
                motifs.append(ptype)
            elif ptype in ("CORRECTION", "INSTRUCTION", "PRINCIPLE", "REVELATION"):
                voice_markers.append(ptype)

        return EssenceEntry(
            source_path=getattr(entry, "entry_id", "unknown"),
            source_area="ledger",
            raw_excerpt=text[:500],
            patterns=patterns,
            essence=essence,
            motifs=motifs,
            voice_markers=voice_markers,
            links=links,
            thermal_state="witnessed",
        )

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
