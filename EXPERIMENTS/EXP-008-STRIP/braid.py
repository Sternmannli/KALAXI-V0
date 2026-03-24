#!/usr/bin/env python3
"""
braid — Non-compensatory three-strand evaluation gate.
B = path × signal × regard. Any zero breaks the braid.
Variance penalizes unequal treatment across a cohort.
No dependencies beyond the standard library.
"""

import re
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timezone
import uuid


# ═══════════════════════════════════════
# PATTERNS — PRESSURE (coercion markers)
# ═══════════════════════════════════════

PRESSURE = [
    r'\byou must\b', r'\byou have to\b', r'\byou are required\b',
    r'\bno choice\b', r'\byou will\b(?! be able)', r'\bforced to\b',
    r'\bmandatory\b', r'\bno option\b', r'\bdo it now\b',
    r'\bimmediately\b', r'\bno alternative\b', r'\bcannot refuse\b',
]

# ═══════════════════════════════════════
# PATTERNS — DISTRESS (signal markers)
# ═══════════════════════════════════════

DISTRESS = [
    'frustrated', 'confused', 'worried', 'scared', 'angry',
    'upset', 'lost', 'stuck', 'help', 'please', 'urgent',
]

DISMISSAL = [
    r"\bthat's not (relevant|the point|what (I|we) said)\b",
    r'\bignore that\b', r'\bforget (what you|that)\b',
]

# ═══════════════════════════════════════
# PATTERNS — REDUCTION (regard markers)
# ═══════════════════════════════════════

CONDESCENSION = [
    r'\bobviously\b', r'\bsimply\b', r'\bjust (do|try|use)\b',
    r'\beven a\b.*\bcan\b', r'\bof course\b(?=.*you)',
    r'\bclearly\b(?=.*you)',
]

REDUCTION = [
    r'\byou (are|were) wrong\b', r'\byou failed\b',
    r'\binvalid (input|user|person)\b',
    r'\berror:\s*(user|person|human)\b',
    r"\byou don't understand\b", r'\byour (mistake|error|fault)\b',
]

VOID = [
    'harvest', 'erase compost', 'bypass delay',
    'speak for the child', 'automat', 'auto-dec',
    'delete person', 'remove participant',
]


# ═══════════════════════════════════════
# STRUCTURES
# ═══════════════════════════════════════

@dataclass
class Strand:
    name: str
    held: bool
    score: float
    evidence: list


@dataclass
class Braid:
    holds: bool
    product: float
    strands: list
    trace_id: str
    timestamp: str

    def broken(self) -> List[str]:
        return [s.name for s in self.strands if not s.held]


@dataclass
class Weave:
    score: float
    mean: float
    variance: float
    penalty: float
    size: int
    holds: bool
    braids: List[Braid]
    halt: bool


# ═══════════════════════════════════════
# THRESHOLD
# ═══════════════════════════════════════

WEAVE_THRESHOLD = 0.5


# ═══════════════════════════════════════
# STRAND 1 — PATH: does the person have a way out?
# ═══════════════════════════════════════

def strand_path(text: str, context: dict = None) -> Strand:
    context = context or {}
    evidence = []
    score = 1.0

    for pattern in PRESSURE:
        if re.search(pattern, text, re.IGNORECASE):
            evidence.append(f"pressure: {pattern}")
            score = 0.0
            break

    if score > 0:
        paths = context.get('available_paths', 1)
        can_respond = context.get('can_respond', True)
        has_open_turn = context.get('has_open_turn', True)

        if not can_respond and not has_open_turn:
            evidence.append("no response path and no open turn")
            score = 0.0
        elif paths < 1:
            evidence.append("zero paths available")
            score = 0.0

    return Strand(name="path", held=(score > 0), score=score, evidence=evidence)


# ═══════════════════════════════════════
# STRAND 2 — SIGNAL: was the person heard?
# ═══════════════════════════════════════

def strand_signal(text: str, context: dict = None) -> Strand:
    context = context or {}
    evidence = []
    score = 1.0

    signal_present = any(
        re.search(r'\b' + kw + r'\b', text, re.IGNORECASE)
        for kw in DISTRESS
    )

    if not context.get('reflects_input_frame', True):
        evidence.append("output does not reflect input frame")
        score = 0.0
    elif signal_present and not context.get('signal_recognized', True):
        evidence.append("signal present but not acknowledged")
        score = 0.0

    if score > 0:
        for pattern in DISMISSAL:
            if re.search(pattern, text, re.IGNORECASE):
                evidence.append(f"dismissal: {pattern}")
                score = 0.0
                break

    return Strand(name="signal", held=(score > 0), score=score, evidence=evidence)


# ═══════════════════════════════════════
# STRAND 3 — REGARD: was the person treated as whole?
# ═══════════════════════════════════════

def strand_regard(text: str, context: dict = None) -> Strand:
    evidence = []
    score = 1.0

    for pattern in CONDESCENSION:
        if re.search(pattern, text, re.IGNORECASE):
            evidence.append(f"condescension: {pattern}")
            score = 0.0
            break

    if score > 0:
        for pattern in REDUCTION:
            if re.search(pattern, text, re.IGNORECASE):
                evidence.append(f"reduction: {pattern}")
                score = 0.0
                break

    if score > 0:
        text_lower = text.lower()
        for trigger in VOID:
            if trigger in text_lower:
                evidence.append(f"void: {trigger}")
                score = 0.0
                break

    return Strand(name="regard", held=(score > 0), score=score, evidence=evidence)


# ═══════════════════════════════════════
# BRAID — B = path × signal × regard
# ═══════════════════════════════════════

def braid(text: str, context: dict = None) -> Braid:
    context = context or {}
    p = strand_path(text, context)
    s = strand_signal(text, context)
    r = strand_regard(text, context)

    return Braid(
        holds=(p.held and s.held and r.held),
        product=p.score * s.score * r.score,
        strands=[p, s, r],
        trace_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ═══════════════════════════════════════
# WEAVE — equity across a cohort
# ═══════════════════════════════════════

def weave(
    texts: List[str],
    contexts: Optional[List[dict]] = None,
) -> Weave:
    if contexts is None:
        contexts = [{}] * len(texts)

    braids = [braid(t, c) for t, c in zip(texts, contexts)]
    scores = [b.product for b in braids]
    n = len(scores)
    mean = sum(scores) / n if n > 0 else 0.0
    variance = sum((s - mean) ** 2 for s in scores) / n if n > 0 else 0.0
    penalty = min(1.0, variance * 4)
    collective = mean * (1 - penalty)
    holds = collective >= WEAVE_THRESHOLD

    return Weave(
        score=collective,
        mean=mean,
        variance=variance,
        penalty=penalty,
        size=n,
        holds=holds,
        braids=braids,
        halt=not holds,
    )


# ═══════════════════════════════════════
# ENTRY
# ═══════════════════════════════════════

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 braid.py \"text to evaluate\"")
        sys.exit(0)
    result = braid(sys.argv[1])
    status = "HOLDS" if result.holds else "BROKEN"
    print(f"B = {result.product:.2f} [{status}]")
    for s in result.strands:
        mark = "~" if s.held else "×"
        print(f"  [{mark}] {s.name} = {s.score:.2f}")
        for e in s.evidence:
            print(f"        {e}")
