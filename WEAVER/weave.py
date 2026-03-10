#!/usr/bin/env python3
"""
weave.py — KALAXI WEAVE Module v1.0
Pattern Synthesis. The organic growth engine.

Extracts patterns from donor inputs, links them to existing wisdom,
and generates honey drops. Weave is how the canon feeds on what donors bring.

Organic growth rules:
  - Every donor input is a canonical element.
  - Weave extracts pattern only. Identity is never stored.
  - Honey drops are provisional until reviewed by a human.
  - Weave never auto-ratifies. It proposes. Humans decide.
  - The wisdom mirror shows donors what their rain has fed.

HoneyDrop protocol:
  Daily: H/O/L ritual <= 60 seconds
  Weekly: synthesis session 75 minutes
  Clang tests: psi/sigma <= 1
  Four-lens review before promotion to canon

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


@dataclass
class PatternCandidate:
    text: str
    source_hash: str  # Hash of donor input — identity never stored
    pattern_type: str  # "resonance", "tension", "echo", "anomaly"
    confidence: float  # 0.0-1.0
    linked_ids: list = field(default_factory=list)


@dataclass
class HoneyDrop:
    essence: str
    source_hashes: list  # Multiple inputs can converge
    drop_type: str  # "proverb", "anomaly", "gap", "wisdom"
    confidence: float
    linked_covenants: list = field(default_factory=list)
    provisional: bool = True  # Always provisional until human review


@dataclass
class WisdomMirrorReflection:
    """What the donor's rain has fed — anonymized, distilled, returned as gift."""
    donor_hash: str
    patterns_contributed: int
    drops_influenced: int
    themes: list
    reflection_text: str


# Pattern detection keywords — grounded in canon
RESONANCE_MARKERS = [
    "always", "never", "must", "cannot", "every time",
    "the same", "repeats", "pattern", "cycle",
]

TENSION_MARKERS = [
    "but", "however", "yet", "despite", "although",
    "conflict", "contradiction", "paradox", "tension",
]

ECHO_MARKERS = [
    "reminds me", "like when", "similar to", "echoes",
    "the same way", "just as", "mirrors",
]

ANOMALY_MARKERS = [
    "strange", "unexpected", "shouldn't", "first time",
    "never before", "broke", "failed", "exception",
]


def _sha(text):
    return hashlib.sha256(text.strip().encode()).hexdigest()


def _score_markers(text, markers):
    """Count how many markers appear in text, normalized to 0-1."""
    lower = text.lower()
    hits = sum(1 for m in markers if m in lower)
    return min(hits / max(len(markers) * 0.3, 1), 1.0)


def ingest(donor_input):
    """
    Ingest donor input and extract pattern candidates.
    Identity is never stored — only the hash and the pattern.
    """
    source_hash = _sha(donor_input)
    candidates = []

    # Score against each pattern type
    scores = {
        "resonance": _score_markers(donor_input, RESONANCE_MARKERS),
        "tension": _score_markers(donor_input, TENSION_MARKERS),
        "echo": _score_markers(donor_input, ECHO_MARKERS),
        "anomaly": _score_markers(donor_input, ANOMALY_MARKERS),
    }

    for pattern_type, confidence in scores.items():
        if confidence > 0.0:
            candidates.append(PatternCandidate(
                text=donor_input,
                source_hash=source_hash,
                pattern_type=pattern_type,
                confidence=confidence,
            ))

    return candidates


def extract_essence(pattern_candidates):
    """
    Distill pattern candidates into honey drops.
    Multiple patterns can converge into a single drop.
    """
    if not pattern_candidates:
        return []

    drops = []

    # Group by pattern type
    by_type = {}
    for pc in pattern_candidates:
        by_type.setdefault(pc.pattern_type, []).append(pc)

    for ptype, candidates in by_type.items():
        # Take the highest-confidence candidate per type
        best = max(candidates, key=lambda c: c.confidence)

        if best.confidence < 0.1:
            continue  # Too weak to form a drop

        # Map pattern type to drop type
        drop_type_map = {
            "resonance": "proverb",
            "tension": "gap",
            "echo": "wisdom",
            "anomaly": "anomaly",
        }

        drop = HoneyDrop(
            essence=best.text[:200],  # Essence is a distilled excerpt
            source_hashes=[c.source_hash for c in candidates],
            drop_type=drop_type_map.get(ptype, "wisdom"),
            confidence=best.confidence,
            provisional=True,  # Always. Weave never auto-ratifies.
        )
        drops.append(drop)

    return drops


def map_to_canon(honey_drop, canon_ids=None):
    """
    Map a honey drop to existing canonical entries.
    Returns list of candidate links (IDs the drop may connect to).
    """
    if canon_ids is None:
        # Try to load from ids.json
        ids_path = ROOT / "MANIFEST" / "ids.json"
        if ids_path.exists():
            import json
            with open(ids_path) as f:
                canon_ids = json.load(f).get("entries", {})
        else:
            canon_ids = {}

    links = []
    lower = honey_drop.essence.lower()

    # Simple keyword matching against existing entries
    for entry_id, entry in canon_ids.items():
        entry_type = entry.get("type", "").lower()
        if entry_type == honey_drop.drop_type:
            links.append({
                "id": entry_id,
                "type": entry_type,
                "match": "type_match",
            })

    return links[:10]  # Cap at 10 candidates


def propose_proverb(pattern_text):
    """
    Propose an emergent proverb from a pattern.
    Returns a provisional proverb entry — never auto-ratified.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    source_hash = _sha(pattern_text)

    return {
        "type": "proverb",
        "status": "PROVISIONAL",
        "text": pattern_text,
        "source_hash": source_hash,
        "proposed": now,
        "ratified": None,  # Humans decide
        "covenants": ["COV#001", "COV#006"],
        "note": "Proposed by WEAVE module. Awaiting steward review.",
    }


def propose_anomaly(pattern_text, severity="MEDIUM"):
    """
    Propose an emergent anomaly from a pattern.
    Returns a provisional anomaly entry — never auto-ratified.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    source_hash = _sha(pattern_text)

    return {
        "type": "anomaly",
        "status": "PROVISIONAL",
        "text": pattern_text,
        "severity": severity,
        "source_hash": source_hash,
        "proposed": now,
        "ratified": None,
        "covenants": ["COV#001"],
        "note": "Proposed by WEAVE module. Awaiting steward review.",
    }


def wisdom_mirror(donor_input_hash, all_drops=None):
    """
    Show the donor what their rain has fed — anonymized, distilled, returned as gift.
    The mirror never reveals identity, only pattern.
    """
    if all_drops is None:
        all_drops = []

    # Find drops this donor contributed to
    contributed = [
        d for d in all_drops
        if donor_input_hash in d.source_hashes
    ]

    themes = list(set(d.drop_type for d in contributed))

    if not contributed:
        reflection = "Your rain has entered the soil. The mycelium listens."
    elif len(contributed) == 1:
        reflection = f"Your offering touched one {contributed[0].drop_type}. It is resting in the threshold."
    else:
        reflection = (
            f"Your rain fed {len(contributed)} patterns across {len(themes)} "
            f"theme{'s' if len(themes) > 1 else ''}. "
            f"The garden remembers what you gave, even if it cannot say your name."
        )

    return WisdomMirrorReflection(
        donor_hash=donor_input_hash,
        patterns_contributed=len(contributed),
        drops_influenced=len(contributed),
        themes=themes,
        reflection_text=reflection,
    )


def brittleness_check(sensitivity, flexibility):
    """
    Brittleness Guard: psi/sigma <= 1.
    Sensitivity must never outrun flexibility.
    Returns (passed, ratio).
    """
    if flexibility == 0:
        return (False, float('inf'))
    ratio = sensitivity / flexibility
    return (ratio <= 1.0, ratio)


def defect_budget_check(total_entries, defect_count):
    """
    Defect Budget: 2-5% epsilon-greedy exploration.
    The canon must maintain deliberate imperfection.
    Returns (in_range, percentage).
    """
    if total_entries == 0:
        return (True, 0.0)
    pct = (defect_count / total_entries) * 100
    return (2.0 <= pct <= 5.0, pct)
