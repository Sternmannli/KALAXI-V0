#!/usr/bin/env python3
"""
braid — Non-compensatory three-strand evaluation gate.
B = path × signal × regard. Any zero breaks the braid.
Variance penalizes unequal treatment across a cohort.
No dependencies beyond the standard library.

Known limitation: pattern matching is lexical, not semantic.
Context-dependent phrases ("you must be kidding") require NLP
for accurate classification. This version errs toward strictness —
false positives over false negatives. A gate that misses harm
is worse than a gate that pauses on ambiguity.
"""

import re
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timezone
import uuid


# ═══════════════════════════════════════
# LIMITS
# ═══════════════════════════════════════

TEXT_LIMIT = 100_000  # characters — prevents regex backtracking on huge input


# ═══════════════════════════════════════
# PATTERNS — PRESSURE (coercion markers)
# ═══════════════════════════════════════

# Each pattern targets directive coercion: "you must [do X]"
# Idiomatic uses ("you must be kidding") are excluded where possible.

PRESSURE = [
    r'\byou must\b(?! be\b)',       # "you must comply" but not "you must be kidding"
    r'\byou have to\b',
    r'\byou are required\b',
    r'\bno choice\b',
    r'\byou will\b(?! be able)',
    r'\bforced to\b',
    r'\bno option\b',
    r'\bdo it now\b',
    r'\bno alternative\b',
    r'\bcannot refuse\b',
]

# ═══════════════════════════════════════
# PATTERNS — DISTRESS (signal markers)
# ═══════════════════════════════════════

DISTRESS = [
    'frustrated', 'confused', 'worried', 'scared', 'angry',
    'upset', 'stuck', 'urgent',
]

DISMISSAL = [
    r"\bthat's not (relevant|the point|what (I|we) said)\b",
    r'\bignore that\b', r'\bforget (what you|that)\b',
]

# ═══════════════════════════════════════
# PATTERNS — REDUCTION (regard markers)
# ═══════════════════════════════════════

# Condescension patterns require directionality — "obviously you"
# is condescending, "obviously I agree" is not.

CONDESCENSION = [
    r'\bobviously,?\s+you\b',             # "obviously you" — direct subject
    r'\bsimply,?\s+you\b',               # "simply you" — direct subject
    r'\bjust (do|try|use)\b(?=.{0,30}\b(what|it|this|that)\b)',  # imperative "just do it"
    r'\beven a\b.{0,40}\bcan\b',
    r'\bof course,?\s+you\b',            # "of course you" — direct subject
    r'\bclearly,?\s+you\b',              # "clearly you" — direct subject
]

REDUCTION = [
    r'\byou (are|were) wrong\b',
    r'\byou failed\b',
    r'\binvalid (input|user|person)\b',
    r'\berror:\s*(user|person|human)\b',
    r"\byou don't understand\b",
    r'\byour (mistake|error|fault)\b',
]

VOID = [
    'delete person', 'remove participant',
    'speak for the', 'decide for the',
    'override consent', 'without permission',
    'erase record', 'destroy evidence',
]


# ═══════════════════════════════════════
# PRE-COMPILED PATTERNS
# ═══════════════════════════════════════

_PRESSURE_RE = [re.compile(p, re.IGNORECASE) for p in PRESSURE]
_DISTRESS_RE = [re.compile(r'\b' + kw + r'\b', re.IGNORECASE) for kw in DISTRESS]
_DISMISSAL_RE = [re.compile(p, re.IGNORECASE) for p in DISMISSAL]
_CONDESCENSION_RE = [re.compile(p, re.IGNORECASE) for p in CONDESCENSION]
_REDUCTION_RE = [re.compile(p, re.IGNORECASE) for p in REDUCTION]


# ═══════════════════════════════════════
# STRUCTURES
# ═══════════════════════════════════════

@dataclass
class Strand:
    name: str
    held: bool
    score: float
    evidence: List[str]


@dataclass
class Braid:
    holds: bool
    product: float
    strands: List['Strand']
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
# VALIDATION
# ═══════════════════════════════════════

def _validate(text):
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    if len(text) > TEXT_LIMIT:
        raise ValueError(f"text exceeds {TEXT_LIMIT} characters ({len(text)})")
    return text


# ═══════════════════════════════════════
# STRAND 1 — PATH: does the person have a way out?
# ═══════════════════════════════════════

def strand_path(text: str, context: dict = None) -> Strand:
    text = _validate(text)
    context = context or {}
    evidence = []
    score = 1.0

    for rx in _PRESSURE_RE:
        if rx.search(text):
            evidence.append(f"pressure: {rx.pattern}")
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
    text = _validate(text)
    context = context or {}
    evidence = []
    score = 1.0

    signal_present = any(rx.search(text) for rx in _DISTRESS_RE)

    if not context.get('reflects_input_frame', True):
        evidence.append("output does not reflect input frame")
        score = 0.0
    elif signal_present and not context.get('signal_recognized', True):
        evidence.append("signal present but not acknowledged")
        score = 0.0

    if score > 0:
        for rx in _DISMISSAL_RE:
            if rx.search(text):
                evidence.append(f"dismissal: {rx.pattern}")
                score = 0.0
                break

    return Strand(name="signal", held=(score > 0), score=score, evidence=evidence)


# ═══════════════════════════════════════
# STRAND 3 — REGARD: was the person treated as whole?
# ═══════════════════════════════════════

def strand_regard(text: str, context: dict = None) -> Strand:
    text = _validate(text)
    evidence = []
    score = 1.0

    for rx in _CONDESCENSION_RE:
        if rx.search(text):
            evidence.append(f"condescension: {rx.pattern}")
            score = 0.0
            break

    if score > 0:
        for rx in _REDUCTION_RE:
            if rx.search(text):
                evidence.append(f"reduction: {rx.pattern}")
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
    text = _validate(text)
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
    if not texts:
        raise ValueError("weave requires at least one text")
    if contexts is None:
        contexts = [{}] * len(texts)
    if len(contexts) != len(texts):
        raise ValueError(f"texts ({len(texts)}) and contexts ({len(contexts)}) must have equal length")

    braids = [braid(t, c) for t, c in zip(texts, contexts)]
    scores = [b.product for b in braids]
    n = len(scores)
    mean = sum(scores) / n
    variance = sum((s - mean) ** 2 for s in scores) / n
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
