#!/usr/bin/env python3
"""
lock_test.py — The Lock Test (Proverb Quality Gate)
Version: 1.0
Grounded in: T#30 (PROT#LOCK-001), FOUNDATIONS/paremiology.md
Linked Covenants: COV#006 (proverb linkage), COV#009 (testability)

A proverb passes the Lock Test only if:
  1. The steward cannot paraphrase it without semantic loss
  2. It triggers response latency in the reader (complexity/depth)
  3. It links across at least two domains

"A proverb that can be said another way was never a proverb."

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional, Dict
from enum import Enum


class LockVerdict(Enum):
    LOCKED = "locked"           # Passes all three conditions
    UNLOCKED = "unlocked"       # Fails one or more conditions
    INSUFFICIENT = "insufficient"  # Not enough data to test


# Felt domains for cross-domain detection
DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    "agency": [
        "choose", "decide", "act", "control", "power", "free", "will",
        "consent", "refuse", "stop", "voice", "speak", "silence",
    ],
    "legibility": [
        "see", "understand", "read", "clear", "visible", "hidden",
        "transparent", "opaque", "mirror", "reflect", "name", "frame",
    ],
    "moral": [
        "right", "wrong", "justice", "fair", "dignity", "worth",
        "sacred", "profane", "good", "evil", "mercy", "cruel",
    ],
    "temporal": [
        "wait", "time", "season", "grow", "decay", "cycle",
        "patience", "hurry", "slow", "fast", "moment", "eternal",
    ],
    "relational": [
        "together", "apart", "connect", "separate", "bridge", "wall",
        "community", "lonely", "belong", "exile", "welcome", "door",
    ],
    "existential": [
        "exist", "being", "nothing", "meaning", "purpose", "void",
        "death", "life", "birth", "soul", "spirit", "consciousness",
    ],
    "ecological": [
        "river", "seed", "garden", "root", "tree", "soil",
        "rain", "wind", "fire", "stone", "mountain", "ocean",
    ],
    "epistemic": [
        "know", "truth", "doubt", "certain", "uncertain", "wisdom",
        "ignorance", "learn", "forget", "remember", "question", "answer",
    ],
}

# Paraphrase synonym clusters — words that are easy substitutions
SYNONYM_CLUSTERS = [
    {"big", "large", "great", "vast", "enormous", "huge"},
    {"small", "little", "tiny", "minute", "slight"},
    {"fast", "quick", "rapid", "swift", "speedy"},
    {"slow", "gradual", "unhurried", "deliberate"},
    {"strong", "powerful", "mighty", "potent", "forceful"},
    {"weak", "feeble", "frail", "fragile"},
    {"good", "fine", "excellent", "worthy", "noble"},
    {"bad", "poor", "terrible", "wretched"},
    {"begin", "start", "commence", "initiate"},
    {"end", "finish", "conclude", "cease", "stop"},
    {"speak", "say", "tell", "utter", "voice"},
    {"see", "observe", "witness", "behold", "perceive"},
    {"walk", "travel", "journey", "wander", "roam"},
    {"think", "consider", "ponder", "reflect", "contemplate"},
    {"hide", "conceal", "obscure", "bury", "mask"},
    {"show", "reveal", "expose", "display", "uncover"},
]

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "can", "could", "must", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "and", "but", "or", "nor", "not", "no", "so", "yet", "if", "then",
    "than", "that", "this", "it", "its", "who", "which", "what", "where",
    "when", "how", "all", "each", "every", "both", "few", "more", "most",
}


@dataclass
class LockResult:
    """Result of running the Lock Test on a proverb."""
    proverb: str
    verdict: LockVerdict
    semantic_density: float     # 0-1: how resistant to paraphrase
    latency_score: float        # 0-1: how much it triggers reflection
    domain_count: int           # Number of domains touched
    domains_found: List[str]    # Which domains
    overall_score: float        # Combined 0-1 score
    passed_conditions: List[str]
    failed_conditions: List[str]
    timestamp: str

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict.value,
            "score": round(self.overall_score, 3),
            "density": round(self.semantic_density, 3),
            "latency": round(self.latency_score, 3),
            "domains": self.domain_count,
            "domains_found": self.domains_found,
            "passed": self.passed_conditions,
            "failed": self.failed_conditions,
        }


class LockTest:
    """
    The Lock Test — proverb quality gate.

    Usage:
        lock = LockTest()
        result = lock.test("The river does not ask the fish to wait.")
        if result.verdict == LockVerdict.LOCKED:
            print("Proverb passes the Lock Test")

        # With explicit paraphrase comparison:
        result = lock.test_with_paraphrase(original, paraphrase)
    """

    # Thresholds
    DENSITY_THRESHOLD = 0.4     # Minimum semantic density to pass
    LATENCY_THRESHOLD = 0.15    # Minimum latency trigger to pass
    MIN_DOMAINS = 2             # Minimum domains for cross-domain linking

    def __init__(self):
        self._tests_run = 0
        self._locked_count = 0

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _content_words(self, text: str) -> List[str]:
        """Extract content words (non-stopwords) from text."""
        words = re.findall(r'\b[a-z]+\b', text.lower())
        return [w for w in words if w not in STOPWORDS and len(w) > 2]

    def _semantic_density(self, text: str) -> float:
        """
        Measure how resistant a text is to paraphrase.

        High density = each word carries irreplaceable meaning.
        Computed as: (irreplaceable words / total content words)

        A word is "replaceable" if it belongs to a common synonym cluster.
        Proverbs with high metaphor density and unusual word combinations
        score higher because their words resist substitution.
        """
        content = self._content_words(text)
        if not content:
            return 0.0

        replaceable = 0
        for word in content:
            for cluster in SYNONYM_CLUSTERS:
                if word in cluster and len(cluster) > 2:
                    replaceable += 1
                    break

        irreplaceable_ratio = 1.0 - (replaceable / len(content))

        # Unique content word ratio (higher diversity = harder to paraphrase)
        unique_ratio = len(set(content)) / len(content) if content else 0.0

        # Base score combines irreplaceability and uniqueness
        base = (irreplaceable_ratio * 0.5) + (unique_ratio * 0.3)

        # Bonus for conciseness — shorter proverbs are denser
        word_count = len(text.split())
        if word_count <= 15:
            base += 0.1
        elif word_count <= 25:
            base += 0.05

        # Bonus for structural features that resist paraphrase
        # Contrast/opposition
        if any(w in text.lower() for w in ["not", "but", "without", "never", "nor"]):
            base += 0.05
        # Metaphor markers (concrete nouns in abstract context)
        if any(w in text.lower() for w in [
            "river", "stone", "fire", "seed", "root", "door",
            "wall", "bridge", "path", "rain", "wind", "weir",
        ]):
            base += 0.1

        return min(1.0, base)

    def _latency_score(self, text: str) -> float:
        """
        Measure how much a text triggers reflective pause.

        Uses markers similar to DignityLatency but tuned for proverbs.
        Proverbs that provoke thought score higher.
        """
        text_lower = text.lower()
        score = 0.0

        # Paradox / tension markers
        paradox_patterns = [
            r'\b(not|never|without)\b.*\b(but|yet|still|already)\b',
            r'\b(asks?|waits?|knows?)\b.*\b(not|never|without)\b',
        ]
        for p in paradox_patterns:
            if re.search(p, text_lower):
                score += 0.2

        # Contrast / opposition structure (A is X; B is Y)
        if re.search(r';', text) or re.search(r'\bbut\b', text_lower):
            score += 0.1

        # Question-evoking structure (implicit questions)
        if any(w in text_lower for w in ["who", "what", "why", "how", "where", "when"]):
            score += 0.15

        # Negation in unexpected context (defamiliarization)
        if re.search(r'\bdoes not\b|\bcannot\b|\bnever\b', text_lower):
            score += 0.1

        # Abstract concepts requiring interpretation
        abstract_markers = [
            "meaning", "dignity", "freedom", "justice", "truth",
            "silence", "absence", "presence", "gap", "threshold",
        ]
        abstract_count = sum(1 for m in abstract_markers if m in text_lower)
        score += min(0.3, abstract_count * 0.1)

        # Compression (much meaning in few words)
        content = self._content_words(text)
        total_words = len(text.split())
        if total_words > 0:
            content_ratio = len(content) / total_words
            if content_ratio > 0.5 and total_words <= 15:
                score += 0.15  # High content density in short form

        return min(1.0, score)

    def _detect_domains(self, text: str) -> List[str]:
        """Detect which felt domains a text touches."""
        text_lower = text.lower()
        found = []
        for domain, keywords in DOMAIN_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                found.append(domain)
        return found

    def test(self, proverb: str) -> LockResult:
        """
        Run the full Lock Test on a proverb.

        Three conditions:
          1. Semantic density >= threshold (resists paraphrase)
          2. Latency score >= threshold (triggers reflection)
          3. Domain count >= 2 (links across domains)
        """
        if not proverb or len(proverb.strip()) < 5:
            return LockResult(
                proverb=proverb or "",
                verdict=LockVerdict.INSUFFICIENT,
                semantic_density=0.0,
                latency_score=0.0,
                domain_count=0,
                domains_found=[],
                overall_score=0.0,
                passed_conditions=[],
                failed_conditions=["insufficient_text"],
                timestamp=self._now(),
            )

        self._tests_run += 1

        density = self._semantic_density(proverb)
        latency = self._latency_score(proverb)
        domains = self._detect_domains(proverb)
        domain_count = len(domains)

        passed = []
        failed = []

        if density >= self.DENSITY_THRESHOLD:
            passed.append("semantic_density")
        else:
            failed.append("semantic_density")

        if latency >= self.LATENCY_THRESHOLD:
            passed.append("latency_trigger")
        else:
            failed.append("latency_trigger")

        if domain_count >= self.MIN_DOMAINS:
            passed.append("cross_domain")
        else:
            failed.append("cross_domain")

        verdict = LockVerdict.LOCKED if len(failed) == 0 else LockVerdict.UNLOCKED
        overall = (density + latency + min(1.0, domain_count / self.MIN_DOMAINS)) / 3.0

        if verdict == LockVerdict.LOCKED:
            self._locked_count += 1

        return LockResult(
            proverb=proverb,
            verdict=verdict,
            semantic_density=density,
            latency_score=latency,
            domain_count=domain_count,
            domains_found=domains,
            overall_score=overall,
            passed_conditions=passed,
            failed_conditions=failed,
            timestamp=self._now(),
        )

    def test_with_paraphrase(self, original: str, paraphrase: str) -> LockResult:
        """
        Enhanced Lock Test using an actual paraphrase for comparison.

        If word overlap between original and paraphrase is high,
        the proverb was too easy to paraphrase — it fails.
        """
        base_result = self.test(original)

        if base_result.verdict == LockVerdict.INSUFFICIENT:
            return base_result

        if not paraphrase or len(paraphrase.strip()) < 5:
            return base_result

        # Measure paraphrase distance
        orig_words = set(self._content_words(original))
        para_words = set(self._content_words(paraphrase))

        if not orig_words or not para_words:
            return base_result

        overlap = len(orig_words & para_words) / len(orig_words | para_words)
        paraphrase_resistance = 1.0 - overlap

        # Blend with existing density score
        enhanced_density = (base_result.semantic_density + paraphrase_resistance) / 2.0

        # Re-evaluate
        passed = []
        failed = []

        if enhanced_density >= self.DENSITY_THRESHOLD:
            passed.append("semantic_density")
        else:
            failed.append("semantic_density")

        if base_result.latency_score >= self.LATENCY_THRESHOLD:
            passed.append("latency_trigger")
        else:
            failed.append("latency_trigger")

        if base_result.domain_count >= self.MIN_DOMAINS:
            passed.append("cross_domain")
        else:
            failed.append("cross_domain")

        verdict = LockVerdict.LOCKED if len(failed) == 0 else LockVerdict.UNLOCKED
        overall = (enhanced_density + base_result.latency_score +
                   min(1.0, base_result.domain_count / self.MIN_DOMAINS)) / 3.0

        return LockResult(
            proverb=original,
            verdict=verdict,
            semantic_density=enhanced_density,
            latency_score=base_result.latency_score,
            domain_count=base_result.domain_count,
            domains_found=base_result.domains_found,
            overall_score=overall,
            passed_conditions=passed,
            failed_conditions=failed,
            timestamp=self._now(),
        )

    @property
    def tests_run(self) -> int:
        return self._tests_run

    @property
    def locked_count(self) -> int:
        return self._locked_count

    @property
    def lock_rate(self) -> float:
        if self._tests_run == 0:
            return 0.0
        return self._locked_count / self._tests_run
