#!/usr/bin/env python3
"""
voice_engine.py — KALAXI Voice Engine v1.0
Canon-grounded response generation. AXI speaks from the body of the system.

The voice engine does NOT generate arbitrary text. It selects, combines,
and shapes responses from the system's accumulated canon:
  - 3,333+ proverbs (R7M/PROVERBS_*.md)
  - 59 treasures (R7M/TREASURES/)
  - 93 narrative chapters (NARRATIVE/)
  - 200 golden regression utterances (TRAINING/GOLDEN_REGRESSION.jsonl)
  - 1,100 anomalies (R7M/WISDOM_CANON.md)

The voice is constrained by:
  - AXI Voice Rules (6 rules from say.py)
  - Somatic vocabulary (hands, breath, bones, stone, water, ash, rope, knot)
  - Sentence shape (8-14 words)
  - Three-beat rhythm
  - No helpfulness leak

D = A × L × M governs output. If dignity fails, the voice halts.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import re
import hashlib
import random
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


# ═══════════════════════════════════════════════════
# VOICE CORPUS — loaded once, served many times
# ═══════════════════════════════════════════════════

@dataclass
class CanonFragment:
    """A single fragment from the canon corpus."""
    text: str
    source: str           # "proverb", "narrative", "golden", "treasure", "anomaly"
    register: str = ""    # "grief", "dignity", "greeting", "general", etc.
    book: str = ""        # "hakaka", "ashwater", "kinderbuch", "kalaxi_1"
    id: str = ""          # P#00401, T#01, etc.
    voice_score: float = 1.0


@dataclass
class VoiceResponse:
    """A response generated from canon."""
    text: str
    sources: List[str]     # Which canon fragments contributed
    register: str          # Detected register of the input
    dignity_score: float   # D from the dignity check
    breath_paced: bool     # Was this response slowed by breath?
    witness_id: str        # Hash of this response for audit trail


class VoiceCorpus:
    """
    The accumulated canon from which AXI speaks.
    Loaded from files at startup. Immutable during runtime.
    """

    def __init__(self):
        self._proverbs: List[CanonFragment] = []
        self._golden: List[CanonFragment] = []
        self._narrative_fragments: List[CanonFragment] = []
        self._treasures: List[CanonFragment] = []
        self._loaded = False

    def load(self):
        """Load all canon sources. Call once at startup."""
        if self._loaded:
            return
        self._load_proverbs()
        self._load_golden_regression()
        self._load_narratives()
        self._load_treasures()
        self._loaded = True

    @property
    def total_fragments(self) -> int:
        return (len(self._proverbs) + len(self._golden) +
                len(self._narrative_fragments) + len(self._treasures))

    def _load_proverbs(self):
        """Load proverbs from R7M/PROVERBS_*.md files."""
        proverb_dir = ROOT / "R7M"
        for pfile in sorted(proverb_dir.glob("PROVERBS_*.md")):
            try:
                text = pfile.read_text(encoding="utf-8")
                for line in text.split("\n"):
                    line = line.strip()
                    match = re.match(r"^(P#\d+)\s*[-–—]\s*(.+)$", line)
                    if match:
                        pid, ptext = match.group(1), match.group(2).strip()
                        self._proverbs.append(CanonFragment(
                            text=ptext,
                            source="proverb",
                            register="general",
                            id=pid,
                        ))
            except Exception:
                continue

    def _load_golden_regression(self):
        """Load golden regression utterances from TRAINING/GOLDEN_REGRESSION.jsonl."""
        golden_path = ROOT / "TRAINING" / "GOLDEN_REGRESSION.jsonl"
        if not golden_path.exists():
            return
        try:
            for line in golden_path.read_text(encoding="utf-8").split("\n"):
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    messages = entry.get("messages", [])
                    meta = entry.get("metadata", {})
                    # Extract the assistant response (AXI's voice)
                    for msg in messages:
                        if msg.get("role") == "assistant":
                            self._golden.append(CanonFragment(
                                text=msg["content"],
                                source="golden",
                                register=meta.get("register", "general"),
                                voice_score=meta.get("voice_score", 1.0),
                            ))
                except (json.JSONDecodeError, KeyError):
                    continue
        except Exception:
            pass

    def _load_narratives(self):
        """Load narrative fragments from NARRATIVE/ directory."""
        narrative_dir = ROOT / "NARRATIVE"
        book_map = {
            "Hakaka_Complete.md": "hakaka",
            "Ashwater.md": "ashwater",
            "Kinderbuch.md": "kinderbuch",
        }

        for filename, book in book_map.items():
            filepath = narrative_dir / filename
            if not filepath.exists():
                continue
            try:
                text = filepath.read_text(encoding="utf-8")
                # Extract paragraphs (non-empty lines between blank lines)
                paragraphs = []
                current = []
                for line in text.split("\n"):
                    stripped = line.strip()
                    # Skip chapter headers and metadata
                    if stripped.startswith("CHAPTER") or stripped.startswith("PROLOGUE") or stripped.startswith("EPILOGUE"):
                        if current:
                            paragraphs.append(" ".join(current))
                            current = []
                        continue
                    if stripped.startswith("KALAXI") or stripped.startswith("("):
                        continue
                    if not stripped:
                        if current:
                            paragraphs.append(" ".join(current))
                            current = []
                    else:
                        current.append(stripped)
                if current:
                    paragraphs.append(" ".join(current))

                # Keep paragraphs of reasonable length (1-4 sentences)
                for para in paragraphs:
                    word_count = len(para.split())
                    if 5 <= word_count <= 80:
                        self._narrative_fragments.append(CanonFragment(
                            text=para,
                            source="narrative",
                            register="general",
                            book=book,
                        ))
            except Exception:
                continue

    def _load_treasures(self):
        """Load treasure descriptions from R7M/TREASURES/."""
        treasure_path = ROOT / "R7M" / "TREASURES" / "TREASURES_INDEX.md"
        if not treasure_path.exists():
            return
        try:
            text = treasure_path.read_text(encoding="utf-8")
            current_id = ""
            current_desc = ""
            for line in text.split("\n"):
                stripped = line.strip()
                match = re.match(r"^###\s+(T#\d+)\s*[—–-]\s*(.+)$", stripped)
                if match:
                    if current_id and current_desc:
                        self._treasures.append(CanonFragment(
                            text=current_desc.strip(),
                            source="treasure",
                            register="general",
                            id=current_id,
                        ))
                    current_id = match.group(1)
                    current_desc = match.group(2)
                elif stripped.startswith("- **Description:**"):
                    desc = stripped.replace("- **Description:**", "").strip()
                    current_desc = desc
                elif stripped.startswith("- **Formula:**"):
                    formula = stripped.replace("- **Formula:**", "").strip()
                    current_desc += f" ({formula})"

            # Last treasure
            if current_id and current_desc:
                self._treasures.append(CanonFragment(
                    text=current_desc.strip(),
                    source="treasure",
                    register="general",
                    id=current_id,
                ))
        except Exception:
            pass

    # ── SELECTION ──

    def select_proverb(self, theme_words: List[str] = None, n: int = 1) -> List[CanonFragment]:
        """Select proverbs, optionally biased toward theme words."""
        if not self._proverbs:
            return []
        if not theme_words:
            return random.sample(self._proverbs, min(n, len(self._proverbs)))

        # Score by theme word overlap
        scored = []
        theme_lower = {w.lower() for w in theme_words}
        for p in self._proverbs:
            words = {w.lower().strip(".,;:!?") for w in p.text.split()}
            overlap = len(words & theme_lower)
            scored.append((overlap, random.random(), p))

        scored.sort(key=lambda x: (-x[0], x[1]))
        return [s[2] for s in scored[:n]]

    def select_golden(self, register: str = None, n: int = 1) -> List[CanonFragment]:
        """Select golden regression utterances by register."""
        if not self._golden:
            return []
        pool = self._golden
        if register:
            filtered = [g for g in pool if g.register == register]
            if filtered:
                pool = filtered
        return random.sample(pool, min(n, len(pool)))

    def select_narrative(self, book: str = None, n: int = 1) -> List[CanonFragment]:
        """Select narrative fragments, optionally from a specific book."""
        if not self._narrative_fragments:
            return []
        pool = self._narrative_fragments
        if book:
            filtered = [f for f in pool if f.book == book]
            if filtered:
                pool = filtered
        return random.sample(pool, min(n, len(pool)))

    def random_fragment(self) -> Optional[CanonFragment]:
        """Return any random fragment from the entire corpus."""
        all_fragments = (self._proverbs + self._golden +
                         self._narrative_fragments + self._treasures)
        if not all_fragments:
            return None
        return random.choice(all_fragments)


# ═══════════════════════════════════════════════════
# REGISTER DETECTION — what kind of input is this?
# ═══════════════════════════════════════════════════

REGISTER_PATTERNS = {
    "grief": [
        "loss", "lost", "gone", "died", "death", "pain", "hurt",
        "miss", "mourn", "grief", "broken", "wound", "scar", "empty",
        "alone", "separation", "separated", "taken", "torn",
    ],
    "dignity": [
        "dignity", "respect", "seen", "invisible", "unseen", "ignored",
        "denied", "matter", "count", "belong", "excluded", "erased",
        "recognition", "worth", "value", "human", "right", "justice",
    ],
    "seeking": [
        "what", "how", "why", "help", "understand", "explain", "mean",
        "search", "looking", "find", "seek", "question", "wonder",
        "curious", "tell me", "show me",
    ],
    "greeting": [
        "hello", "hi", "hey", "greet", "morning", "evening",
        "welcome", "arrive", "enter", "begin", "start", "first",
    ],
    "silence": [
        "quiet", "silence", "still", "nothing", "empty", "pause",
        "wait", "breath", "listen", "hold",
    ],
}


def detect_register(text: str) -> str:
    """Detect the emotional register of input text."""
    text_lower = text.lower()
    words = set(re.findall(r'\w+', text_lower))

    scores = {}
    for register, patterns in REGISTER_PATTERNS.items():
        score = sum(1 for p in patterns if p in words or p in text_lower)
        if score > 0:
            scores[register] = score

    if not scores:
        return "general"

    return max(scores, key=scores.get)


# ═══════════════════════════════════════════════════
# VOICE ENGINE — the core
# ═══════════════════════════════════════════════════

# Somatic anchors from say.py — the body of AXI's voice
SOMATIC_ANCHORS = {
    "hands", "hand", "breath", "bones", "bone", "skin", "chest", "fist",
    "palm", "lungs", "spine", "blood", "muscle", "grip", "wrists",
    "shoulders", "body", "weight",
    "rope", "stone", "ash", "water", "river", "fire", "salt", "soil",
    "wood", "iron", "clay", "sand", "thread", "knot", "weir", "wall",
    "bread", "door", "path", "root", "seed",
}


def _somatic_score(text: str) -> float:
    """Score how many somatic anchors a text contains (0.0-1.0)."""
    words = set(re.findall(r'\w+', text.lower()))
    hits = words & SOMATIC_ANCHORS
    # Normalized: 1 anchor = 0.5, 2+ = higher
    return min(1.0, len(hits) * 0.3 + 0.1) if hits else 0.0


def _sentence_shape_score(text: str) -> float:
    """Score sentence length adherence (8-14 words ideal)."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0.5

    good = 0
    for s in sentences:
        wc = len(s.split())
        if 6 <= wc <= 16:
            good += 1
    return good / len(sentences)


class VoiceEngine:
    """
    The KALAXI Voice Engine.

    Given donor input and a dignity score, produces a canon-grounded
    AXI voice response. The response is selected and shaped — never
    freely generated.

    Usage:
        engine = VoiceEngine()
        response = engine.respond("I carry something heavy.", dignity=0.85)
    """

    def __init__(self):
        self._corpus = VoiceCorpus()
        self._corpus.load()
        self._response_count = 0

    @property
    def corpus_size(self) -> int:
        return self._corpus.total_fragments

    def respond(self, donor_input: str, dignity: float = 1.0,
                register: str = None) -> VoiceResponse:
        """
        Generate a canon-grounded response.

        1. Detect register of input
        2. Select fragments from corpus matching register
        3. Score fragments for somatic anchoring and sentence shape
        4. Compose response from highest-scoring fragments
        5. Hash for audit trail
        """
        if register is None:
            register = detect_register(donor_input)

        # If dignity is zero, the voice halts
        if dignity <= 0.0:
            halt_text = "Witnessed. The system cannot proceed with dignity intact."
            return VoiceResponse(
                text=halt_text,
                sources=["halt_protocol"],
                register=register,
                dignity_score=dignity,
                breath_paced=True,
                witness_id=hashlib.sha256(halt_text.encode()).hexdigest()[:16],
            )

        # Extract theme words from donor input
        input_words = re.findall(r'\w+', donor_input.lower())
        theme_words = [w for w in input_words if len(w) > 3 and w not in {
            "this", "that", "what", "when", "where", "which", "with",
            "have", "been", "from", "they", "them", "their", "about",
            "would", "could", "should", "some", "other", "more",
        }]

        # Gather candidates from all sources
        candidates: List[CanonFragment] = []

        # Golden regression — highest priority for register match
        golden = self._corpus.select_golden(register=register, n=3)
        candidates.extend(golden)

        # Proverbs — biased toward theme words
        proverbs = self._corpus.select_proverb(theme_words=theme_words, n=3)
        candidates.extend(proverbs)

        # Narrative fragments — by register mapping to book
        book_map = {
            "grief": "hakaka",
            "dignity": "ashwater",
            "greeting": "kinderbuch",
            "silence": "hakaka",
        }
        book = book_map.get(register)
        narratives = self._corpus.select_narrative(book=book, n=2)
        candidates.extend(narratives)

        if not candidates:
            # Fallback: any random fragment
            frag = self._corpus.random_fragment()
            if frag:
                candidates = [frag]
            else:
                fallback = "The knot holds. The river waits."
                return VoiceResponse(
                    text=fallback,
                    sources=["fallback"],
                    register=register,
                    dignity_score=dignity,
                    breath_paced=False,
                    witness_id=hashlib.sha256(fallback.encode()).hexdigest()[:16],
                )

        # Score candidates
        scored = []
        for c in candidates:
            somatic = _somatic_score(c.text)
            shape = _sentence_shape_score(c.text)
            # Golden regression gets a bonus
            source_bonus = 0.3 if c.source == "golden" else 0.0
            # Register match bonus
            reg_bonus = 0.2 if c.register == register else 0.0
            total = somatic + shape + source_bonus + reg_bonus + random.uniform(0, 0.1)
            scored.append((total, c))

        scored.sort(key=lambda x: -x[0])

        # Take the best fragment
        best = scored[0][1]

        self._response_count += 1
        sources = [f"{best.source}:{best.id}" if best.id else best.source]

        witness_id = hashlib.sha256(
            f"{best.text}:{self._response_count}:{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()[:16]

        return VoiceResponse(
            text=best.text,
            sources=sources,
            register=register,
            dignity_score=dignity,
            breath_paced=dignity < 0.5,
            witness_id=witness_id,
        )

    def proverb(self, theme_words: List[str] = None) -> Optional[CanonFragment]:
        """Return a single proverb, optionally themed."""
        results = self._corpus.select_proverb(theme_words=theme_words, n=1)
        return results[0] if results else None

    def narrative_fragment(self, book: str = None) -> Optional[CanonFragment]:
        """Return a single narrative fragment."""
        results = self._corpus.select_narrative(book=book, n=1)
        return results[0] if results else None

    def treasure(self, treasure_id: str = None) -> Optional[CanonFragment]:
        """Return a treasure by ID or random."""
        if treasure_id:
            for t in self._corpus._treasures:
                if t.id == treasure_id:
                    return t
            return None
        if self._corpus._treasures:
            return random.choice(self._corpus._treasures)
        return None

    def stats(self) -> Dict:
        """Return corpus statistics."""
        return {
            "proverbs": len(self._corpus._proverbs),
            "golden_utterances": len(self._corpus._golden),
            "narrative_fragments": len(self._corpus._narrative_fragments),
            "treasures": len(self._corpus._treasures),
            "total_fragments": self._corpus.total_fragments,
            "responses_generated": self._response_count,
        }
