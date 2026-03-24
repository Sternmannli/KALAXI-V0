#!/usr/bin/env python3
"""
gate.py — Non-compensatory three-axis text evaluation gate.
G = A * L * M. Any zero halts. Variance penalizes unequal treatment.
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
# PATTERNS — SIGNAL (distress markers)
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
# PATTERNS — REGARD (reduction markers)
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
class Axis:
    name: str
    passed: bool
    score: float
    evidence: list


@dataclass
class Gate:
    passed: bool
    product: float
    axes: list
    trace_id: str
    timestamp: str

    def failed(self) -> List[str]:
        return [a.name for a in self.axes if not a.passed]


@dataclass
class Collective:
    score: float
    mean: float
    variance: float
    penalty: float
    size: int
    passed: bool
    gates: List[Gate]
    halt: bool


# ═══════════════════════════════════════
# THRESHOLD
# ═══════════════════════════════════════

COLLECTIVE_THRESHOLD = 0.5


# ═══════════════════════════════════════
# A — does the person have a way out?
# ═══════════════════════════════════════

def measure_a(text: str, context: dict = None) -> Axis:
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

    return Axis(name="A", passed=(score > 0), score=score, evidence=evidence)


# ═══════════════════════════════════════
# L — was the person heard?
# ═══════════════════════════════════════

def measure_l(text: str, context: dict = None) -> Axis:
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

    return Axis(name="L", passed=(score > 0), score=score, evidence=evidence)


# ═══════════════════════════════════════
# M — was the person treated as whole?
# ═══════════════════════════════════════

def measure_m(text: str, context: dict = None) -> Axis:
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

    return Axis(name="M", passed=(score > 0), score=score, evidence=evidence)


# ═══════════════════════════════════════
# GATE — G = A * L * M
# ═══════════════════════════════════════

def evaluate(text: str, context: dict = None) -> Gate:
    context = context or {}
    a = measure_a(text, context)
    l = measure_l(text, context)
    m = measure_m(text, context)

    return Gate(
        passed=(a.passed and l.passed and m.passed),
        product=a.score * l.score * m.score,
        axes=[a, l, m],
        trace_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ═══════════════════════════════════════
# COLLECTIVE — equity across a cohort
# ═══════════════════════════════════════

def evaluate_collective(
    texts: List[str],
    contexts: Optional[List[dict]] = None,
) -> Collective:
    if contexts is None:
        contexts = [{}] * len(texts)

    gates = [evaluate(t, c) for t, c in zip(texts, contexts)]
    scores = [g.product for g in gates]
    n = len(scores)
    mean = sum(scores) / n if n > 0 else 0.0
    variance = sum((s - mean) ** 2 for s in scores) / n if n > 0 else 0.0
    penalty = min(1.0, variance * 4)
    collective = mean * (1 - penalty)
    passed = collective >= COLLECTIVE_THRESHOLD

    return Collective(
        score=collective,
        mean=mean,
        variance=variance,
        penalty=penalty,
        size=n,
        passed=passed,
        gates=gates,
        halt=not passed,
    )


# ═══════════════════════════════════════
# ENTRY
# ═══════════════════════════════════════

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 gate.py \"text to evaluate\"")
        sys.exit(0)
    result = evaluate(sys.argv[1])
    status = "PASS" if result.passed else "FAIL"
    print(f"G = {result.product:.2f} [{status}]")
    for ax in result.axes:
        mark = "+" if ax.passed else "-"
        print(f"  [{mark}] {ax.name} = {ax.score:.2f}")
        for e in ax.evidence:
            print(f"        {e}")
