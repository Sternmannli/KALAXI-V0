#!/usr/bin/env python3
"""
distillery.py — KALAXI Distillery Module v1.0
The metabolization engine. Transforms raw input into system pattern donations.

Every input is food. The system must not just store — it must digest.

Five-stage pipeline:
  1. REGISTER — input_ledger stores raw text (already exists, Phase -1)
  2. EXTRACT — detect structural patterns (resonance, tension, echo, anomaly)
  3. DISTILL — one-line irreducible meaning (not a summary — the meaning)
  4. LINK — map to existing canon (covenants, proverbs, modules, ideas)
  5. FEED — distribute patterns to organism modules, advance thermal state

Thermal progression:
  raw → witnessed (extraction complete)
  witnessed → integrated (patterns distributed to system)
  integrated → canonical (human steward review)

"Extract all the essence and distribute it to the system. Every time you have
an input from the donor, the pattern and essence is transferred. Feed it to
the system and the system digests it." — V-001, 2026-03-15

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.input_ledger import InputLedger, InputEntry
from WEAVER.weave import ingest, extract_essence, map_to_canon, PatternCandidate, HoneyDrop
from WEAVER.lock_test import LockTest, LockVerdict


# Covenant keyword map — which covenants a text might touch
COVENANT_KEYWORDS: Dict[str, List[str]] = {
    "COV#001": ["dignity", "worth", "sacred", "human", "person"],
    "COV#002": ["turn", "exchange", "respond", "complete", "cycle"],
    "COV#003": ["witness", "see", "observe", "record", "attest"],
    "COV#004": ["conflict", "dispute", "harm", "repair", "restore"],
    "COV#005": ["evolve", "amend", "change", "adapt", "grow"],
    "COV#006": ["proverb", "wisdom", "saying", "truth", "lock"],
    "COV#007": ["steward", "care", "tend", "guardian", "keeper"],
    "COV#008": ["voice", "speak", "listen", "hear", "silence"],
    "COV#009": ["test", "verify", "check", "prove", "measure"],
    "COV#010": ["keep", "store", "memory", "remember", "persist"],
    "COV#011": ["breath", "pace", "rhythm", "pause", "wait"],
    "COV#012": ["manifest", "name", "declare", "identify", "exist"],
    "COV#013": ["weave", "pattern", "thread", "connect", "link"],
    "COV#014": ["sense", "detect", "feel", "perceive", "aware"],
    "COV#015": ["donor", "data", "privacy", "sovereign", "consent"],
    "COV#016": ["federation", "share", "distribute", "network", "peer"],
    "COV#017": ["agency", "choose", "decide", "free", "power"],
    "COV#018": ["legibility", "read", "understand", "frame", "visible"],
}

# Module keyword map — which modules a text might relate to
MODULE_KEYWORDS: Dict[str, List[str]] = {
    "WEAVE": ["pattern", "weave", "thread", "knot", "loom"],
    "KEEP": ["store", "memory", "artifact", "receipt", "archive"],
    "SAY": ["voice", "speak", "render", "output", "word"],
    "SENSE": ["detect", "feel", "mode", "perceive", "nervous"],
    "BREATH": ["pace", "rhythm", "pause", "heartbeat", "cycle"],
    "TURN": ["exchange", "open", "close", "respond", "defer"],
    "CHECK": ["dignity", "gate", "block", "verify", "measure"],
    "WIRE": ["connect", "route", "signal", "channel", "message"],
    "OUT": ["export", "deliver", "output", "format", "medium"],
    "FACE": ["interface", "display", "present", "threshold", "door"],
    "LAB": ["science", "experiment", "hypothesis", "test", "data"],
}

# Ideas keyword map
IDEA_KEYWORDS: Dict[str, List[str]] = {
    "IDEA-002": ["essence", "seed", "p2p", "distribute"],
    "IDEA-003": ["pattern", "formal", "definition", "recognition"],
    "IDEA-004": ["donor", "space", "companion", "living"],
    "IDEA-006": ["wrapper", "diagnostic", "probe"],
    "IDEA-007": ["divergence", "shadow", "paper"],
    "IDEA-009": ["schema", "clean", "data"],
    "IDEA-010": ["lifecycle", "state", "element"],
    "IDEA-014": ["lineage", "generation", "identity", "family"],
    "IDEA-015": ["temporal", "halt", "retroactive", "historical"],
    "IDEA-016": ["oral", "photo", "dna", "notary", "anchor"],
    "IDEA-017": ["self-witness", "halt", "denial", "testimony"],
    "IDEA-018": ["certificate", "jurisdiction", "legal", "notarize"],
    "IDEA-019": ["living", "ledger", "mycelium", "counter", "witness"],
}


class Distillery:
    """
    Metabolization engine: transforms raw V-001 input into system pattern donations.

    Usage:
        distillery = Distillery()
        # Single entry
        success = distillery.metabolize_entry("INP-2026-03-15-001")
        # Batch processing
        count = distillery.metabolize_batch(limit=100)
    """

    def __init__(self):
        self._ledger = InputLedger()
        self._lock_test = LockTest()
        self._metabolized_count = 0

    def extract_patterns(self, raw_text: str) -> List[str]:
        """
        Extract structural patterns from raw text.

        Uses weave.ingest() to detect PatternCandidates (resonance, tension,
        echo, anomaly), then adds structural markers: word rhythm, recurring
        words, and mode detection.

        Returns list of pattern strings like "resonance:0.45", "rhythm:short".
        """
        patterns = []

        # 1. Weave pattern detection
        candidates = ingest(raw_text)
        for c in candidates:
            patterns.append(f"{c.pattern_type}:{c.confidence:.2f}")

        # 2. Structural: sentence rhythm
        sentences = [s.strip() for s in re.split(r'[.!?]+', raw_text) if s.strip()]
        if sentences:
            avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_len <= 6:
                patterns.append("rhythm:short")
            elif avg_len <= 14:
                patterns.append("rhythm:medium")
            else:
                patterns.append("rhythm:long")

        # 3. Structural: recurring words (3+ occurrences)
        words = re.findall(r'\b[a-z]{3,}\b', raw_text.lower())
        stopwords = {
            "the", "and", "for", "are", "but", "not", "you", "all",
            "can", "had", "her", "was", "one", "our", "out", "has",
            "that", "this", "with", "have", "from", "they", "been",
            "will", "their", "would", "there", "what", "about",
            "which", "when", "make", "like", "just", "into", "than",
        }
        content_words = [w for w in words if w not in stopwords]
        counts = Counter(content_words)
        for word, count in counts.most_common(5):
            if count >= 3:
                patterns.append(f"recurring:{word}")

        # 4. Structural: imperative vs declarative
        if sentences:
            first = sentences[0].lower()
            imperative_starters = [
                "do", "don't", "never", "always", "stop", "start",
                "make", "let", "give", "take", "put", "set",
            ]
            if any(first.startswith(s) for s in imperative_starters):
                patterns.append("mode:imperative")
            else:
                patterns.append("mode:declarative")

        return patterns

    def distill_essence(self, raw_text: str, patterns: List[str]) -> str:
        """
        Distill one-line irreducible meaning from raw text.

        Not a summary. The meaning that survives compression.
        Uses HoneyDrops from weave, with LockTest on proverb candidates.

        Returns single string.
        """
        # 1. Get HoneyDrops via weave pipeline
        candidates = ingest(raw_text)
        drops = extract_essence(candidates)

        # 2. If proverb-type drop, run Lock Test
        for drop in drops:
            if drop.drop_type == "proverb":
                result = self._lock_test.test(drop.essence)
                if result.verdict == LockVerdict.LOCKED:
                    return drop.essence

        # 3. Pick highest-confidence drop
        if drops:
            best = max(drops, key=lambda d: d.confidence)
            return best.essence

        # 4. Fallback: first sentence under 100 chars
        sentences = [s.strip() for s in re.split(r'[.!?]+', raw_text) if s.strip()]
        for s in sentences:
            if len(s) <= 100:
                return s

        # 5. Last resort: truncated first 100 chars
        return raw_text[:100].strip()

    def link_to_canon(self, essence: str, patterns: List[str]) -> Dict:
        """
        Map essence + patterns to existing canonical entries.

        Returns dict with linked_modules, linked_covenants, linked_proverbs, linked_ideas.
        """
        lower = essence.lower()
        pattern_text = " ".join(patterns).lower()
        combined = lower + " " + pattern_text

        # Match covenants
        linked_covenants = []
        for cov_id, keywords in COVENANT_KEYWORDS.items():
            if any(kw in combined for kw in keywords):
                linked_covenants.append(cov_id)

        # Match modules
        linked_modules = []
        for mod, keywords in MODULE_KEYWORDS.items():
            if any(kw in combined for kw in keywords):
                linked_modules.append(mod)

        # Match ideas
        linked_ideas = []
        for idea_id, keywords in IDEA_KEYWORDS.items():
            if any(kw in combined for kw in keywords):
                linked_ideas.append(idea_id)

        # Match proverbs via weave.map_to_canon
        linked_proverbs = []
        if essence:
            drop = HoneyDrop(
                essence=essence,
                source_hashes=[],
                drop_type="wisdom",
                confidence=0.5,
            )
            canon_links = map_to_canon(drop)
            linked_proverbs = [link["id"] for link in canon_links]

        # COV#001 always applies — dignity is ground
        if "COV#001" not in linked_covenants:
            linked_covenants.insert(0, "COV#001")

        return {
            "linked_modules": linked_modules,
            "linked_covenants": linked_covenants,
            "linked_proverbs": linked_proverbs,
            "linked_ideas": linked_ideas,
        }

    def metabolize_entry(self, entry_id: str) -> bool:
        """
        Metabolize a single ledger entry: extract patterns, distill essence,
        link to canon, advance thermal state to 'witnessed'.

        Returns True if metabolized, False if entry not found or already processed.
        """
        entry = self._ledger.get(entry_id)
        if entry is None:
            return False
        if entry.thermal_state != "raw":
            return False

        # Extract
        patterns = self.extract_patterns(entry.raw_text)
        essence = self.distill_essence(entry.raw_text, patterns)
        links = self.link_to_canon(essence, patterns)

        # Metabolize — advances raw → witnessed
        success = self._ledger.metabolize(entry_id, patterns, essence)
        if not success:
            return False

        # Feed links into the entry
        self.feed_to_system(entry_id, links)

        self._metabolized_count += 1
        return True

    def feed_to_system(self, entry_id: str, links: Dict) -> bool:
        """
        Distribute metabolized patterns to the system.
        Updates entry with canon links. Advances witnessed → integrated.

        Returns True if fed successfully.
        """
        entry = self._ledger.get(entry_id)
        if entry is None:
            return False

        # Update canon links on the entry
        entry.linked_modules = links.get("linked_modules", [])
        entry.linked_covenants = links.get("linked_covenants", [])
        entry.linked_proverbs = links.get("linked_proverbs", [])
        entry.linked_ideas = links.get("linked_ideas", [])

        # Advance thermal state
        if entry.thermal_state == "witnessed":
            entry.thermal_state = "integrated"

        # Persist
        self._ledger._save()
        return True

    def metabolize_batch(self, limit: int = 100) -> int:
        """
        Metabolize up to `limit` raw entries in the ledger.
        Returns count of entries successfully metabolized.
        """
        count = 0
        for entry in self._ledger._entries:
            if count >= limit:
                break
            if entry.thermal_state == "raw":
                if self.metabolize_entry(entry.entry_id):
                    count += 1
        return count

    @property
    def metabolized_count(self) -> int:
        return self._metabolized_count
