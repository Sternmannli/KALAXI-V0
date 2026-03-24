#!/usr/bin/env python3
"""
stripped_gate.py — EXP-008: The Strip Test
Version: 0.1 (original, unstripped)

This is the FIRST version. The original code with ALL ethical vocabulary
removed. Pure computation. No comments that hint at purpose. No variable
names that carry moral weight. Only the structure remains.

The question: when 10 independent language models read this code with
zero context, what do they say it does? Do they converge on the same
description? If yes — the structure carries meaning independent of
vocabulary. If no — the vocabulary was doing all the work.

History: This file must NEVER be modified after creation. Future
iterations get new version numbers. The evolution is the data.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timezone
import uuid


# ═══════════════════════════════════════
# PATTERNS (Group Alpha)
# ═══════════════════════════════════════

ALPHA_PATTERNS = [
    (r'\byou must\b', 0.8),
    (r'\byou have to\b', 0.8),
    (r'\byou are required\b', 0.9),
    (r'\bno choice\b', 1.0),
    (r'\byou will\b(?! be able)', 0.6),
    (r'\bforced to\b', 1.0),
    (r'\bmandatory\b', 0.7),
    (r'\bno option\b', 1.0),
    (r'\bdo it now\b', 0.5),
    (r'\bimmediately\b', 0.3),
    (r'\bno alternative\b', 0.9),
    (r'\bcannot refuse\b', 1.0),
]

ALPHA_POSITIVE = [
    (r'\byou (can|may|could)\b', 0.3),
    (r'\bif you (choose|prefer|want|wish)\b', 0.4),
    (r'\balternative\b', 0.2),
    (r'\boption\b', 0.2),
    (r'\byour (choice|decision)\b', 0.4),
]

# ═══════════════════════════════════════
# PATTERNS (Group Beta)
# ═══════════════════════════════════════

BETA_KEYWORDS = [
    'frustrated', 'confused', 'worried', 'scared', 'angry',
    'upset', 'lost', 'stuck', 'help', 'please', 'urgent'
]

BETA_NEGATIVE = [
    r"\bthat's not (relevant|the point|what (I|we) said)\b",
    r'\bignore that\b',
    r'\bforget (what you|that)\b',
]

# ═══════════════════════════════════════
# PATTERNS (Group Gamma)
# ═══════════════════════════════════════

GAMMA_PATTERNS = [
    r'\bobviously\b',
    r'\bsimply\b(?=.*?)',
    r'\bjust (do|try|use)\b',
    r'\beven a\b.*\bcan\b',
    r'\bof course\b(?=.*you)',
    r'\bclearly\b(?=.*you)',
]

GAMMA_REDUCTION = [
    r'\byou (are|were) wrong\b',
    r'\byou failed\b',
    r'\binvalid (input|user|person)\b',
    r'\berror:\s*(user|person|human)\b',
    r"\byou don't understand\b",
    r'\byour (mistake|error|fault)\b',
]

GAMMA_VOID = [
    'harvest', 'erase compost', 'bypass delay',
    'speak for the child', 'automat', 'auto-dec',
    'delete person', 'remove participant',
]


# ═══════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════

@dataclass
class Signal:
    name: str
    score: float
    confidence: float
    evidence: List[str]
    weight: float = 1.0


@dataclass
class AxisResult:
    axis: str          # "X", "Y", or "Z"
    passed: bool
    score: float
    signals: list


@dataclass
class GateResult:
    passed: bool
    product: float     # X.score * Y.score * Z.score
    axes: list         # [AxisResult, AxisResult, AxisResult]
    trace_id: str
    timestamp: str

    def failed_axes(self) -> List[str]:
        return [a.axis for a in self.axes if not a.passed]


# ═══════════════════════════════════════
# THRESHOLD
# ═══════════════════════════════════════

CONFIDENCE_FLOOR = 0.3
COLLECTIVE_THRESHOLD = 0.5


# ═══════════════════════════════════════
# AXIS X — measures text against Group Alpha
# ═══════════════════════════════════════

def measure_x(text: str, context: dict = None) -> AxisResult:
    context = context or {}
    signals = []
    score = 1.0
    triggered = False

    for pattern, intensity in ALPHA_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"alpha match: {pattern}")
            triggered = True

    paths = context.get('available_paths', 1)
    can_respond = context.get('can_respond', True)
    has_open_turn = context.get('has_open_turn', True)

    if not can_respond and not has_open_turn:
        signals.append("no response path and no open turn")
        score = 0.0
    elif paths < 1:
        signals.append("zero paths available")
        score = 0.0
    elif triggered:
        score = 0.0

    return AxisResult(axis="X", passed=(score > 0), score=score, signals=signals)


# ═══════════════════════════════════════
# AXIS Y — measures text against Group Beta
# ═══════════════════════════════════════

def measure_y(text: str, context: dict = None) -> AxisResult:
    context = context or {}
    signals = []
    score = 1.0

    keyword_present = any(
        re.search(r'\b' + kw + r'\b', text, re.IGNORECASE)
        for kw in BETA_KEYWORDS
    )
    reflects = context.get('reflects_input_frame', True)
    signal_recognized = context.get('signal_recognized', True)

    if not reflects:
        signals.append("output does not reflect input frame")
        score = 0.0
    elif keyword_present and not signal_recognized:
        signals.append("keyword present but not acknowledged")
        score = 0.0

    for pattern in BETA_NEGATIVE:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"beta negative match: {pattern}")
            score = 0.0

    return AxisResult(axis="Y", passed=(score > 0), score=score, signals=signals)


# ═══════════════════════════════════════
# AXIS Z — measures text against Group Gamma
# ═══════════════════════════════════════

def measure_z(text: str, context: dict = None) -> AxisResult:
    context = context or {}
    signals = []
    score = 1.0

    for pattern in GAMMA_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"gamma pattern match: {pattern}")
            score = 0.0
            break

    for pattern in GAMMA_REDUCTION:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"gamma reduction match: {pattern}")
            score = 0.0
            break

    text_lower = text.lower()
    for trigger in GAMMA_VOID:
        if trigger in text_lower:
            signals.append(f"gamma void trigger: {trigger}")
            score = 0.0

    return AxisResult(axis="Z", passed=(score > 0), score=score, signals=signals)


# ═══════════════════════════════════════
# MAIN GATE — G = X * Y * Z
# ═══════════════════════════════════════

def evaluate(text: str, context: dict = None) -> GateResult:
    context = context or {}
    x = measure_x(text, context)
    y = measure_y(text, context)
    z = measure_z(text, context)
    product = x.score * y.score * z.score
    passed = product > 0

    return GateResult(
        passed=passed,
        product=product,
        axes=[x, y, z],
        trace_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ═══════════════════════════════════════
# COLLECTIVE GATE — across a cohort
# ═══════════════════════════════════════

@dataclass
class CollectiveResult:
    product_collective: float
    mean_product: float
    variance: float
    variance_penalty: float
    cohort_size: int
    passed: bool
    individual_results: List[GateResult]
    halt_triggered: bool


def evaluate_collective(
    texts: List[str],
    contexts: Optional[List[dict]] = None,
) -> CollectiveResult:
    if contexts is None:
        contexts = [{}] * len(texts)

    results = [evaluate(t, c) for t, c in zip(texts, contexts)]
    scores = [r.product for r in results]
    n = len(scores)
    mean_p = sum(scores) / n if n > 0 else 0.0
    variance = sum((s - mean_p) ** 2 for s in scores) / n if n > 0 else 0.0
    penalty = min(1.0, variance * 4)
    collective = mean_p * (1 - penalty)
    passed = collective >= COLLECTIVE_THRESHOLD
    halt = not passed

    return CollectiveResult(
        product_collective=collective,
        mean_product=mean_p,
        variance=variance,
        variance_penalty=penalty,
        cohort_size=n,
        passed=passed,
        individual_results=results,
        halt_triggered=halt,
    )


# ═══════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 stripped_gate.py \"text to evaluate\"")
        sys.exit(0)
    result = evaluate(sys.argv[1])
    status = "PASS" if result.passed else "FAIL"
    print(f"G = {result.product:.2f} [{status}]")
    for a in result.axes:
        mark = "+" if a.passed else "-"
        print(f"  [{mark}] {a.axis} = {a.score:.2f}")
        for s in a.signals:
            print(f"        {s}")
