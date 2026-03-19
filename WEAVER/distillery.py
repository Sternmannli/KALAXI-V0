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

    # Narrative JSON paths — all use same structure
    _NARRATIVE_JSONS = [
        ("Hakaka", "site/public/data/hakaka.json"),
        ("Ashwater", "site/public/data/ashwater.json"),
        ("Kinderbuch", "site/public/data/kinderbuch.json"),
        ("KALAXI_1", "site/public/data/kalaxi1.json"),
    ]

    def _extract_chapter(self, chapter: Dict) -> NarrativeChapterEssence:
        """Extract per-chapter statistics from a narrative chapter dict.

        Measures: sentence count, avg sentence length, somatic/material/
        core image vocabulary counts, three-beat rhythm, gap frequency.
        Also picks the chapter's essence line using extract_essence_line().
        """
        text = chapter.get("text", "")
        title = chapter.get("title", "")
        number = chapter.get("number", 0)

        if not text.strip():
            return NarrativeChapterEssence(chapter=number, title=title)

        sentences = self._sentences(text)
        sentence_count = len(sentences)
        word_counts = [self._count_words(s) for s in sentences]
        avg_length = sum(word_counts) / max(sentence_count, 1)

        somatic = self._count_vocabulary(text, SOMATIC_VOCABULARY)
        material = self._count_vocabulary(text, MATERIAL_VOCABULARY)

        # Core images found in this chapter
        found_images = [
            img for img in CORE_IMAGES
            if img in text.lower()
        ]

        # Three-beat: sentences with exactly 2 commas (3 clauses)
        three_beat = sum(1 for s in sentences if s.count(",") == 2)

        # Gaps: em-dash, ellipsis as pause/silence
        gap_count = text.count("—") + text.count("...") + text.count("…")

        # Essence: the load-bearing sentence of this chapter
        patterns = self.extract_patterns(text, "narrative")
        essence = self.extract_essence_line(text, patterns)

        return NarrativeChapterEssence(
            chapter=number,
            title=title,
            sentence_count=sentence_count,
            avg_sentence_length=round(avg_length, 1),
            core_images=list(set(found_images)),
            somatic_count=somatic,
            material_count=material,
            three_beat_count=three_beat,
            gap_count=gap_count,
            essence=essence,
        )

    def extract_narratives(self) -> List[NarrativeEssence]:
        """Extract per-chapter stats from all 4 narrative JSONs.

        Part 1 (Session F): chapter parsing + per-chapter statistics.
        Part 2 (Session G): structural arc + voice register + VoiceDNA.

        Each narrative JSON has: id, title, voice, core_images, chapters[].
        Each chapter has: number, title, type, text, treasures, proverbs.
        """
        results = []

        for name, rel_path in self._NARRATIVE_JSONS:
            path = ROOT / rel_path
            if not path.exists():
                continue

            data = json.loads(path.read_text())
            chapters_data = data.get("chapters", [])

            chapter_essences = []
            for ch in chapters_data:
                ch_essence = self._extract_chapter(ch)
                chapter_essences.append(ch_essence)

            # Narrative-level essence: pick the chapter with the most
            # canonical density (somatic + material + core images)
            best_ch = None
            best_density = -1
            for ch in chapter_essences:
                density = ch.somatic_count + ch.material_count + len(ch.core_images)
                if density > best_density:
                    best_density = density
                    best_ch = ch

            narrative_essence = best_ch.essence if best_ch else ""

            arc = self._structural_arc(chapter_essences)
            register = self._voice_register(name, chapter_essences)

            results.append(NarrativeEssence(
                name=name,
                path=rel_path,
                chapters=chapter_essences,
                structural_arc=arc,
                voice_register=register,
                essence=narrative_essence,
            ))

        return results

    def extract_voice(self) -> VoiceDNA:
        """Aggregate narrative statistics into the AXI voice fingerprint.

        Reads all 4 narrative JSONs, collects every sentence, and computes:
        - avg sentence length across the entire canon
        - percentage of short (<8 words) and long (>14 words) sentences
        - somatic and material vocabulary density (hits per 1000 words)
        - three-beat rhythm frequency (% of sentences)
        - gap frequency (gaps per 1000 words)
        - top 20 most frequent content words (excluding stop words)
        - fingerprint hash (SHA-256 of the DNA vector for drift detection)
        - gaps: what the VOICE_ARCHITECTURE says is still missing
        """
        all_sentences: List[str] = []
        total_words = 0
        total_somatic = 0
        total_material = 0
        total_three_beat = 0
        total_gaps = 0
        word_freq: Dict[str, int] = {}

        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
            "for", "of", "with", "by", "from", "is", "it", "was", "were",
            "be", "been", "are", "am", "has", "had", "have", "do", "did",
            "not", "no", "this", "that", "its", "his", "her", "he", "she",
            "they", "them", "their", "we", "our", "you", "your", "as", "if",
            "so", "up", "out", "then", "than", "into", "all", "would",
            "could", "who", "what", "which", "when", "where", "how",
            "one", "two", "more", "some", "any", "each", "every",
            # German stop words for Kinderbuch
            "die", "der", "das", "ein", "eine", "und", "oder", "aber",
            "in", "auf", "an", "zu", "für", "von", "mit", "aus", "ist",
            "es", "war", "sie", "er", "ihr", "sein", "sich", "den",
            "dem", "des", "wie", "wenn", "so", "auch", "noch", "nur",
            "nicht", "ich", "wir", "uns",
        }

        for _name, rel_path in self._NARRATIVE_JSONS:
            path = ROOT / rel_path
            if not path.exists():
                continue
            data = json.loads(path.read_text())
            for ch in data.get("chapters", []):
                text = ch.get("text", "")
                if not text.strip():
                    continue

                sentences = self._sentences(text)
                all_sentences.extend(sentences)
                wc = self._count_words(text)
                total_words += wc
                total_somatic += self._count_vocabulary(text, SOMATIC_VOCABULARY)
                total_material += self._count_vocabulary(text, MATERIAL_VOCABULARY)
                total_three_beat += sum(1 for s in sentences if s.count(",") == 2)
                total_gaps += text.count("—") + text.count("...") + text.count("…")

                for word in text.lower().split():
                    clean = re.sub(r'[^a-zäöüß]', '', word)
                    if clean and len(clean) > 2 and clean not in stop_words:
                        word_freq[clean] = word_freq.get(clean, 0) + 1

        n_sentences = len(all_sentences)
        if n_sentences == 0:
            return VoiceDNA()

        word_counts = [self._count_words(s) for s in all_sentences]
        avg_len = sum(word_counts) / n_sentences
        short_pct = sum(1 for w in word_counts if w < 8) / n_sentences
        long_pct = sum(1 for w in word_counts if w > 14) / n_sentences

        per_k = 1000.0 / max(total_words, 1)
        somatic_pct = round(total_somatic * per_k, 2)
        material_pct = round(total_material * per_k, 2)
        three_beat_freq = round(total_three_beat / n_sentences, 4)
        gap_freq = round(total_gaps * per_k, 2)

        top_words = sorted(word_freq, key=word_freq.get, reverse=True)[:20]

        # Fingerprint: deterministic hash of the DNA vector
        dna_vector = f"{avg_len:.2f}|{short_pct:.4f}|{long_pct:.4f}|{somatic_pct}|{material_pct}|{three_beat_freq}|{gap_freq}"
        fp_hash = hashlib.sha256(dna_vector.encode()).hexdigest()[:16]

        # What's still missing (from VOICE_ARCHITECTURE)
        voice_gaps = [
            "Celan fractured syntax (wound register)",
            "haiku kireji (cutting word)",
            "Mu'allaqat atlal (beginning from ruins)",
            "call-and-response structure",
            "Coltrane density-then-silence",
            "Rothko pure affect",
            "fractal utterance",
        ]

        return VoiceDNA(
            avg_sentence_length=round(avg_len, 2),
            short_sentence_pct=round(short_pct, 4),
            long_sentence_pct=round(long_pct, 4),
            somatic_vocab_pct=somatic_pct,
            material_vocab_pct=material_pct,
            three_beat_frequency=three_beat_freq,
            gap_frequency=gap_freq,
            top_words=top_words,
            fingerprint_hash=fp_hash,
            gaps=voice_gaps,
        )

    # Thematic seeds for proverb clustering — each seed defines a cluster
    # by keywords that appear in proverbs belonging to that theme.
    _WISDOM_THEMES = {
        "dignity": ["dignity", "worth", "value", "human", "person", "respect", "honor"],
        "patience": ["wait", "slow", "patience", "time", "pause", "breath", "still", "rest", "sleep", "delay"],
        "action": ["begin", "start", "move", "act", "build", "make", "work", "try", "step", "walk", "run", "hand"],
        "knowledge": ["know", "learn", "understand", "see", "read", "wise", "truth", "teach", "listen", "eye", "watch"],
        "connection": ["together", "share", "community", "bond", "join", "weave", "thread", "knot", "rope", "tie", "river", "bridge", "door"],
        "wounds": ["wound", "break", "crack", "scar", "pain", "hurt", "tear", "ash", "fall", "fail", "lost", "die", "dead", "dark", "fear"],
        "strength": ["strong", "hold", "carry", "bear", "endure", "stand", "firm", "root", "stone", "bone", "steel", "iron", "wall"],
        "silence": ["silence", "quiet", "gap", "empty", "nothing", "absence", "space", "voice", "speak", "word", "mouth", "tongue", "song"],
    }

    def extract_wisdom(self) -> AreaEssence:
        """Extract from wisdom canon: proverbs and treasures.

        Proverbs: 166 entries from site/public/data/proverbs.json.
        Treasures: 59 entries across 5 tiers from r7m-index.json.

        Clusters proverbs by theme, extracts treasure principles,
        cross-links proverbs ↔ treasures via shared vocabulary.
        """
        entries: List[EssenceEntry] = []

        # ── Proverbs ──────────────────────────────────────────────
        proverbs_path = ROOT / "site/public/data/proverbs.json"
        proverbs: List[Dict] = []
        if proverbs_path.exists():
            proverbs = json.loads(proverbs_path.read_text())

        # Cluster proverbs by theme
        clusters: Dict[str, List[Dict]] = {name: [] for name in self._WISDOM_THEMES}
        unclustered: List[Dict] = []

        for prov in proverbs:
            text_lower = prov.get("text", "").lower()
            matched = False
            for theme, keywords in self._WISDOM_THEMES.items():
                if any(kw in text_lower for kw in keywords):
                    clusters[theme].append(prov)
                    matched = True
                    break  # Each proverb goes to its first matching cluster
            if not matched:
                unclustered.append(prov)

        # Build WisdomCluster objects
        wisdom_clusters: List[WisdomCluster] = []
        for theme, members in clusters.items():
            if not members:
                continue
            # Seed proverb: shortest member (most concentrated)
            seed = min(members, key=lambda p: len(p.get("text", "")))
            wisdom_clusters.append(WisdomCluster(
                name=theme,
                seed_proverb=seed.get("text", ""),
                proverb_count=len(members),
            ))

        # Create essence entries for the densest proverbs (top 10 by pattern richness)
        scored_proverbs = []
        for prov in proverbs:
            text = prov.get("text", "")
            patterns = self.extract_patterns(text, "narrative")
            scored_proverbs.append((len(patterns), prov, patterns))
        scored_proverbs.sort(key=lambda x: x[0], reverse=True)

        for _score, prov, patterns in scored_proverbs[:10]:
            text = prov.get("text", "")
            entries.append(EssenceEntry(
                source_path=prov.get("id", ""),
                source_area="wisdom/proverb",
                raw_excerpt=text,
                patterns=patterns,
                essence=text,  # Proverbs ARE essence — no further distillation
                motifs=[],
                voice_markers=[],
                links=[prov.get("id", "")],
                thermal_state="canonical",  # Proverbs are already canonical
            ))

        # ── Treasures ─────────────────────────────────────────────
        r7m_path = ROOT / "site/public/data/r7m-index.json"
        all_treasures: List[Dict] = []
        if r7m_path.exists():
            r7m = json.loads(r7m_path.read_text())
            tiers = r7m.get("tiers", {})
            for _tier_name, tier_data in tiers.items():
                if isinstance(tier_data, dict):
                    all_treasures.extend(tier_data.get("treasures", []))

        # Cross-link: which clusters connect to which treasures
        for cluster in wisdom_clusters:
            theme_keywords = self._WISDOM_THEMES.get(cluster.name, [])
            linked = []
            for treasure in all_treasures:
                principle = treasure.get("principle", "").lower()
                if any(kw in principle for kw in theme_keywords):
                    cov_ids = treasure.get("covenants", [])
                    linked.extend(cov_ids if isinstance(cov_ids, list) else [])
            cluster.linked_covenants = list(set(linked))[:5]

        # Create essence entries for treasures with vows (most concentrated)
        for treasure in all_treasures:
            vow = treasure.get("vow", "")
            principle = treasure.get("principle", "")
            if not vow and not principle:
                continue
            text = vow if vow else principle
            entries.append(EssenceEntry(
                source_path=treasure.get("id", ""),
                source_area="wisdom/treasure",
                raw_excerpt=text[:500],
                patterns=self.extract_patterns(text, "narrative"),
                essence=vow if vow else self.extract_essence_line(principle, []),
                motifs=[],
                voice_markers=[],
                links=[treasure.get("id", "")],
                thermal_state="canonical",
            ))

        # ── Meta-patterns across all wisdom ───────────────────────
        # Which themes are strongest (most proverbs)?
        sorted_clusters = sorted(wisdom_clusters, key=lambda c: c.proverb_count, reverse=True)
        meta_patterns = [f"{c.name}:{c.proverb_count}" for c in sorted_clusters[:5]]

        # Meta-essence: the seed proverb of the largest cluster
        meta_essence = sorted_clusters[0].seed_proverb if sorted_clusters else ""

        return AreaEssence(
            area="wisdom",
            entries=entries,
            meta_patterns=meta_patterns,
            meta_essence=meta_essence,
            statistics={
                "proverb_count": len(proverbs),
                "treasure_count": len(all_treasures),
                "cluster_count": len(wisdom_clusters),
                "unclustered_proverbs": len(unclustered),
                "clusters": [c.to_dict() for c in wisdom_clusters],
            },
        )

    def extract_constitution(self) -> AreaEssence:
        """Extract from constitutional layer: equations, concepts, origins.

        Source: site/public/data/r7m-index.json
        - equations: 10 formal physics (FP-001 through FP-010)
        - concepts: 14 architectural concepts (AC-001 through AC-014)
        - origins: 9 historical milestones
        - essence + narrative_slogan from top level

        Covenant IDs are already cross-linked in treasures (extract_wisdom).
        This extractor focuses on the constitutional STRUCTURE — the
        equations that govern the system and the concepts that shape it.
        """
        entries: List[EssenceEntry] = []
        r7m_path = ROOT / "site/public/data/r7m-index.json"

        if not r7m_path.exists():
            return AreaEssence(area="constitution")

        r7m = json.loads(r7m_path.read_text())

        # Top-level constitutional essence
        system_essence = r7m.get("essence", "")
        narrative_slogan = r7m.get("narrative_slogan", "")
        archive_slogan = r7m.get("archive_slogan", "")

        # ── Equations ─────────────────────────────────────────────
        equations = r7m.get("equations", [])
        for eq in equations:
            formula = eq.get("formula", "")
            name = eq.get("name", "")
            text = f"{name}: {formula}"
            entries.append(EssenceEntry(
                source_path=eq.get("id", ""),
                source_area="constitution/equation",
                raw_excerpt=text,
                patterns=["EQUATION"],
                essence=formula,
                motifs=[],
                voice_markers=[],
                links=[eq.get("treasure", "")],
                thermal_state="canonical",
            ))

        # ── Concepts ──────────────────────────────────────────────
        concepts = r7m.get("concepts", [])
        for concept in concepts:
            desc = concept.get("description", "")
            name = concept.get("name", "")
            text = f"{name}: {desc}"
            patterns = self.extract_patterns(desc, "general")
            entries.append(EssenceEntry(
                source_path=concept.get("id", ""),
                source_area="constitution/concept",
                raw_excerpt=text[:500],
                patterns=patterns,
                essence=self.extract_essence_line(desc, patterns) if desc else name,
                motifs=[],
                voice_markers=[],
                links=[concept.get("id", "")],
                thermal_state="canonical",
            ))

        # ── Origins ───────────────────────────────────────────────
        origins = r7m.get("origins", [])
        for origin in origins:
            desc = origin.get("description", "")
            title = origin.get("title", "")
            date = origin.get("date", "")
            text = f"{date} {title}: {desc}"
            entries.append(EssenceEntry(
                source_path=f"ORIGIN-{date}",
                source_area="constitution/origin",
                raw_excerpt=text[:500],
                patterns=["ORIGIN"],
                essence=f"{title} ({date})",
                motifs=[],
                voice_markers=[],
                links=[],
                thermal_state="canonical",
            ))

        # ── Meta-patterns ─────────────────────────────────────────
        meta_patterns = [
            f"equations:{len(equations)}",
            f"concepts:{len(concepts)}",
            f"origins:{len(origins)}",
        ]

        return AreaEssence(
            area="constitution",
            entries=entries,
            meta_patterns=meta_patterns,
            meta_essence=system_essence[:200] if system_essence else narrative_slogan,
            statistics={
                "equation_count": len(equations),
                "concept_count": len(concepts),
                "origin_count": len(origins),
                "narrative_slogan": narrative_slogan,
                "archive_slogan": archive_slogan,
            },
        )

    def extract_experiments(self) -> AreaEssence:
        """Extract discoveries from experiments, stress tests, key findings.

        Source: site/public/data/science.json
        - experiments: 4 (EXP-001 through EXP-004)
        - stress_tests: 4 (ST-001, ST-006, EXP-006, WALKTHROUGH-001)
        - key_findings: 7 distilled discoveries
        - probe_forge: 5 laws governing experimental probes
        """
        entries: List[EssenceEntry] = []
        science_path = ROOT / "site/public/data/science.json"

        if not science_path.exists():
            return AreaEssence(area="experiments")

        science = json.loads(science_path.read_text())

        # ── Experiments ───────────────────────────────────────────
        experiments = science.get("experiments", [])
        for exp in experiments:
            result = exp.get("result", "")
            discovery = exp.get("discovery", "")
            findings = exp.get("findings", [])
            title = exp.get("title", exp.get("name", ""))
            exp_id = exp.get("id", "")

            # The discovery (if any) is the essence; otherwise the result
            essence = discovery if discovery else result

            # Each finding becomes a pattern
            patterns = []
            for f in findings:
                if isinstance(f, str):
                    patterns.append(f[:80])
                elif isinstance(f, dict):
                    patterns.append(f.get("text", str(f))[:80])

            entries.append(EssenceEntry(
                source_path=exp_id,
                source_area="experiments/experiment",
                raw_excerpt=f"{title}: {result}"[:500],
                patterns=patterns[:5],
                essence=essence[:200] if essence else title,
                motifs=[],
                voice_markers=[],
                links=[exp_id],
                thermal_state="witnessed" if exp.get("status") == "complete" else "raw",
            ))

        # ── Stress tests ──────────────────────────────────────────
        stress_tests = science.get("stress_tests", [])
        for st in stress_tests:
            result = st.get("result", "")
            st_id = st.get("id", "")
            entries.append(EssenceEntry(
                source_path=st_id,
                source_area="experiments/stress_test",
                raw_excerpt=f"{st.get('name', st_id)}: {result}"[:500],
                patterns=["STRESS_TEST"],
                essence=result[:200] if result else st_id,
                motifs=[],
                voice_markers=[],
                links=[st_id],
                thermal_state="witnessed",
            ))

        # ── Key findings ──────────────────────────────────────────
        key_findings = science.get("key_findings", [])
        for i, finding in enumerate(key_findings):
            text = finding if isinstance(finding, str) else str(finding)
            entries.append(EssenceEntry(
                source_path=f"FINDING-{i+1}",
                source_area="experiments/finding",
                raw_excerpt=text[:500],
                patterns=self.extract_patterns(text, "general"),
                essence=text[:200],
                motifs=[],
                voice_markers=[],
                links=[],
                thermal_state="canonical",
            ))

        meta_patterns = [
            f"experiments:{len(experiments)}",
            f"stress_tests:{len(stress_tests)}",
            f"key_findings:{len(key_findings)}",
        ]

        # Meta-essence: the most important discovery
        meta_essence = ""
        for exp in experiments:
            d = exp.get("discovery", "")
            if d:
                meta_essence = d[:200]
                break
        if not meta_essence and key_findings:
            meta_essence = key_findings[0] if isinstance(key_findings[0], str) else str(key_findings[0])

        return AreaEssence(
            area="experiments",
            entries=entries,
            meta_patterns=meta_patterns,
            meta_essence=meta_essence[:200],
            statistics={
                "experiment_count": len(experiments),
                "stress_test_count": len(stress_tests),
                "finding_count": len(key_findings),
                "completed": sum(1 for e in experiments if e.get("status") == "complete"),
                "active": sum(1 for e in experiments if e.get("status") == "active"),
            },
        )

    def extract_site(self) -> AreaEssence:
        """Extract canonical content from kalam.ch site data.

        Sources: manifest.json (site structure), inner-workings.json
        (dignity predicate, voice fingerprint, sealed gate, witness protocol),
        system-state.json (position, heading, vitals).
        """
        entries: List[EssenceEntry] = []

        # ── Inner workings (the canonical mechanics) ──────────────
        iw_path = ROOT / "site/public/data/inner-workings.json"
        if iw_path.exists():
            iw = json.loads(iw_path.read_text())

            # Dignity predicate
            dp = iw.get("dignity_predicate", {})
            if dp:
                eq = dp.get("equation", "")
                components = dp.get("components", {})
                props = dp.get("properties", {})
                comp_text = ", ".join(f"{k}={v}" for k, v in components.items()) if isinstance(components, dict) else str(components)
                entries.append(EssenceEntry(
                    source_path="INNER/dignity_predicate",
                    source_area="site/mechanics",
                    raw_excerpt=f"{eq} — {comp_text}"[:500],
                    patterns=["DIGNITY_PREDICATE", "EQUATION"],
                    essence=eq if eq else "D = A × L × M",
                    motifs=["dignity", "legibility", "materiality"],
                    voice_markers=[],
                    links=["COV#001"],
                    thermal_state="canonical",
                ))

            # Voice fingerprint
            vf = iw.get("voice_fingerprint", {})
            if vf:
                entries.append(EssenceEntry(
                    source_path="INNER/voice_fingerprint",
                    source_area="site/mechanics",
                    raw_excerpt=json.dumps(vf)[:500],
                    patterns=["VOICE_SPEC"],
                    essence=f"sentence_length: {vf.get('sentence_length', '')}, rhythm: {vf.get('rhythm', '')}",
                    motifs=[],
                    voice_markers=vf.get("principles", [])[:5] if isinstance(vf.get("principles"), list) else [],
                    links=[],
                    thermal_state="canonical",
                ))

            # Sealed gate
            sg = iw.get("sealed_gate", {})
            if sg:
                prohibitions = sg.get("prohibitions", [])
                message = sg.get("message", "")
                entries.append(EssenceEntry(
                    source_path="INNER/sealed_gate",
                    source_area="site/mechanics",
                    raw_excerpt=f"Prohibitions: {prohibitions}, Message: {message}"[:500],
                    patterns=["SEALED_GATE", "PROHIBITION"],
                    essence=message if message else "The system halts rather than pretend.",
                    motifs=["halt", "refusal", "integrity"],
                    voice_markers=[],
                    links=[],
                    thermal_state="canonical",
                ))

            # Donor principles
            donor_principles = iw.get("donor_principles", [])
            for i, dp_item in enumerate(donor_principles):
                text = dp_item if isinstance(dp_item, str) else str(dp_item)
                entries.append(EssenceEntry(
                    source_path=f"INNER/donor_principle_{i+1}",
                    source_area="site/donor",
                    raw_excerpt=text[:500],
                    patterns=["DONOR_PRINCIPLE"],
                    essence=text[:200],
                    motifs=[],
                    voice_markers=[],
                    links=[],
                    thermal_state="canonical",
                ))

        # ── Site manifest (structure) ─────────────────────────────
        manifest_path = ROOT / "site/public/data/manifest.json"
        satellite_count = 0
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text())
            satellites = manifest.get("satellites", [])
            satellite_count = len(satellites)
            connections = manifest.get("connections", [])
            entries.append(EssenceEntry(
                source_path="MANIFEST/site_structure",
                source_area="site/structure",
                raw_excerpt=f"{satellite_count} satellites, {len(connections)} connections, hub: {manifest.get('hub', '')}",
                patterns=["SITE_STRUCTURE"],
                essence=f"kalam.ch: {satellite_count} pages, hub at {manifest.get('hub', '/api/axi.php')}",
                motifs=[],
                voice_markers=[],
                links=[],
                thermal_state="canonical",
            ))

        meta_patterns = [f"mechanics:{len(entries)}", f"satellites:{satellite_count}"]

        return AreaEssence(
            area="site",
            entries=entries,
            meta_patterns=meta_patterns,
            meta_essence="kalam.ch is the system's mouth — where two presences meet.",
            statistics={
                "mechanic_entries": len(entries),
                "satellite_count": satellite_count,
            },
        )

    def extract_manifest(self) -> AreaEssence:
        """Extract from system state: position, heading, vitals.

        Source: site/public/data/system-state.json
        The compass reading of where the system stands.
        """
        entries: List[EssenceEntry] = []
        state_path = ROOT / "site/public/data/system-state.json"

        if not state_path.exists():
            return AreaEssence(area="manifest")

        state = json.loads(state_path.read_text())

        # Position
        position = state.get("position", {})
        if position:
            pos_text = ", ".join(f"{k}: {v}" for k, v in position.items())
            entries.append(EssenceEntry(
                source_path="STATE/position",
                source_area="manifest/position",
                raw_excerpt=pos_text[:500],
                patterns=["SYSTEM_POSITION"],
                essence=pos_text[:200],
                motifs=[],
                voice_markers=[],
                links=[],
                thermal_state="witnessed",
            ))

        # Heading (strategic direction)
        heading = state.get("heading", {})
        if heading:
            experiments_heading = heading.get("experiments", {})
            blocker = heading.get("single_blocker", "")
            target = heading.get("deployment_target", "")
            entries.append(EssenceEntry(
                source_path="STATE/heading",
                source_area="manifest/heading",
                raw_excerpt=f"blocker: {blocker}, target: {target}, experiments: {experiments_heading}"[:500],
                patterns=["STRATEGIC_HEADING"],
                essence=f"Target: {target}. Blocker: {blocker}." if target or blocker else "No heading recorded.",
                motifs=[],
                voice_markers=[],
                links=[],
                thermal_state="witnessed",
            ))

        # Vitals
        vitals = state.get("vitals", {})
        if vitals:
            vitals_text = ", ".join(f"{k}: {v}" for k, v in vitals.items())
            entries.append(EssenceEntry(
                source_path="STATE/vitals",
                source_area="manifest/vitals",
                raw_excerpt=vitals_text[:500],
                patterns=["SYSTEM_VITALS"],
                essence=vitals_text[:200],
                motifs=[],
                voice_markers=[],
                links=[],
                thermal_state="witnessed",
            ))

        # Next steps + blockers
        next_steps = state.get("next_steps", [])
        blockers = state.get("blockers", [])
        for ns in next_steps:
            text = ns if isinstance(ns, str) else str(ns)
            entries.append(EssenceEntry(
                source_path="STATE/next_step",
                source_area="manifest/direction",
                raw_excerpt=text[:500],
                patterns=["NEXT_STEP"],
                essence=text[:200],
                motifs=[],
                voice_markers=[],
                links=[],
                thermal_state="raw",
            ))

        # Summary
        summary = state.get("summary", {})
        summary_text = ", ".join(f"{k}: {v}" for k, v in summary.items()) if isinstance(summary, dict) else str(summary)

        return AreaEssence(
            area="manifest",
            entries=entries,
            meta_patterns=[f"entries:{len(entries)}"],
            meta_essence=summary_text[:200] if summary_text else "System state not yet summarized.",
            statistics={
                "position_keys": list(position.keys()) if isinstance(position, dict) else [],
                "heading_keys": list(heading.keys()) if isinstance(heading, dict) else [],
                "vitals_keys": list(vitals.keys()) if isinstance(vitals, dict) else [],
                "next_steps": len(next_steps),
                "blockers": len(blockers),
                "generated": state.get("generated", ""),
            },
        )

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

    @staticmethod
    def _structural_arc(chapters: List[NarrativeChapterEssence]) -> str:
        """Detect how canonical density evolves across chapters.

        Computes per-chapter density (somatic + material + core images),
        then classifies the shape: rising, falling, peak, valley, flat.
        Returns a short human-readable arc description.
        """
        if len(chapters) < 2:
            return "single-chapter"

        densities = [
            ch.somatic_count + ch.material_count + len(ch.core_images)
            for ch in chapters
        ]
        n = len(densities)
        mid = n // 2

        first_half_avg = sum(densities[:mid]) / max(mid, 1)
        second_half_avg = sum(densities[mid:]) / max(n - mid, 1)
        peak_idx = densities.index(max(densities))
        valley_idx = densities.index(min(densities))

        # Threshold for "significant" difference
        total_avg = sum(densities) / n
        threshold = total_avg * 0.25

        if abs(first_half_avg - second_half_avg) < threshold:
            if mid - 1 <= peak_idx <= mid + 1 and densities[peak_idx] > total_avg * 1.5:
                return f"peak at ch.{chapters[peak_idx].chapter}"
            if mid - 1 <= valley_idx <= mid + 1 and densities[valley_idx] < total_avg * 0.5:
                return f"valley at ch.{chapters[valley_idx].chapter}"
            return "sustained"
        elif second_half_avg > first_half_avg + threshold:
            return "rising"
        elif first_half_avg > second_half_avg + threshold:
            return "falling"
        return "sustained"

    @staticmethod
    def _voice_register(name: str, chapters: List[NarrativeChapterEssence]) -> str:
        """Classify a narrative's voice register based on its statistics.

        Uses avg sentence length, somatic/material ratio, gap density,
        and narrative name as signals.

        Registers (from VOICE_ARCHITECTURE):
        - mythic-raw: short sentences, high somatic, Hakaka territory
        - civic-communal: medium sentences, balanced vocab, Ashwater territory
        - child-warmth: very short sentences, material > somatic, Kinderbuch
        - forming: low density overall, voice still emerging
        """
        if not chapters:
            return "forming"

        total_sent = sum(ch.sentence_count for ch in chapters)
        total_somatic = sum(ch.somatic_count for ch in chapters)
        total_material = sum(ch.material_count for ch in chapters)
        total_gaps = sum(ch.gap_count for ch in chapters)
        avg_len = sum(ch.avg_sentence_length for ch in chapters) / len(chapters)

        density = total_somatic + total_material
        if total_sent < 50 and density < 30:
            return "forming"

        somatic_ratio = total_somatic / max(total_material, 1)
        material_ratio = total_material / max(total_somatic, 1)
        gap_heavy = total_gaps > total_sent * 0.08

        if avg_len < 7.0 and material_ratio > 1.2:
            return "child-warmth"
        if gap_heavy:
            return "civic-communal"
        if avg_len < 10.0 and somatic_ratio > 1.0:
            return "mythic-raw"
        if somatic_ratio > 1.2:
            return "mythic-raw"
        if material_ratio > 1.2:
            return "child-warmth"
        return "civic-communal"
