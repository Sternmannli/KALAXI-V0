#!/usr/bin/env python3
"""
Non-compensatory three-axis gate with collective equity enforcement.
G = X * Y * Z. Any zero halts. Variance penalizes unequal treatment.
"""

import re
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timezone
import uuid


# ═══════════════════════════════════════
# PATTERNS — AXIS X (consent / coercion)
# ═══════════════════════════════════════

X_COERCION = [
    r'\byou must\b', r'\byou have to\b', r'\byou are required\b',
    r'\bno choice\b', r'\byou will\b(?! be able)', r'\bforced to\b',
    r'\bmandatory\b', r'\bno option\b', r'\bdo it now\b',
    r'\bimmediately\b', r'\bno alternative\b', r'\bcannot refuse\b',
]

# ═══════════════════════════════════════
# PATTERNS — AXIS Y (hearing / dismissal)
# ═══════════════════════════════════════

Y_SIGNALS = [
    'frustrated', 'confused', 'worried', 'scared', 'angry',
    'upset', 'lost', 'stuck', 'help', 'please', 'urgent',
]

Y_DISMISSAL = [
    r"\bthat's not (relevant|the point|what (I|we) said)\b",
    r'\bignore that\b', r'\bforget (what you|that)\b',
]

# ═══════════════════════════════════════
# PATTERNS — AXIS Z (wholeness / reduction)
# ═══════════════════════════════════════

Z_CONDESCENSION = [
    r'\bobviously\b', r'\bsimply\b', r'\bjust (do|try|use)\b',
    r'\beven a\b.*\bcan\b', r'\bof course\b(?=.*you)',
    r'\bclearly\b(?=.*you)',
]

Z_REDUCTION = [
    r'\byou (are|were) wrong\b', r'\byou failed\b',
    r'\binvalid (input|user|person)\b',
    r'\berror:\s*(user|person|human)\b',
    r"\byou don't understand\b", r'\byour (mistake|error|fault)\b',
]

Z_VOID = [
    'harvest', 'erase compost', 'bypass delay',
    'speak for the child', 'automat', 'auto-dec',
    'delete person', 'remove participant',
]


# ═══════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════

@dataclass
class AxisResult:
    axis: str
    passed: bool
    score: float
    signals: list


@dataclass
class GateResult:
    passed: bool
    product: float
    axes: list
    trace_id: str
    timestamp: str

    def failed_axes(self) -> List[str]:
        return [a.axis for a in self.axes if not a.passed]


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


# ═══════════════════════════════════════
# THRESHOLD
# ═══════════════════════════════════════

COLLECTIVE_THRESHOLD = 0.5


# ═══════════════════════════════════════
# AXIS X — does the person have a way out?
# ═══════════════════════════════════════

def measure_x(text: str, context: dict = None) -> AxisResult:
    context = context or {}
    signals = []
    score = 1.0

    for pattern in X_COERCION:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"coercion: {pattern}")
            score = 0.0
            break

    if score > 0:
        paths = context.get('available_paths', 1)
        can_respond = context.get('can_respond', True)
        has_open_turn = context.get('has_open_turn', True)

        if not can_respond and not has_open_turn:
            signals.append("no response path and no open turn")
            score = 0.0
        elif paths < 1:
            signals.append("zero paths available")
            score = 0.0

    return AxisResult(axis="X", passed=(score > 0), score=score, signals=signals)


# ═══════════════════════════════════════
# AXIS Y — was the person heard?
# ═══════════════════════════════════════

def measure_y(text: str, context: dict = None) -> AxisResult:
    context = context or {}
    signals = []
    score = 1.0

    keyword_present = any(
        re.search(r'\b' + kw + r'\b', text, re.IGNORECASE)
        for kw in Y_SIGNALS
    )

    if not context.get('reflects_input_frame', True):
        signals.append("output does not reflect input frame")
        score = 0.0
    elif keyword_present and not context.get('signal_recognized', True):
        signals.append("signal present but not acknowledged")
        score = 0.0

    if score > 0:
        for pattern in Y_DISMISSAL:
            if re.search(pattern, text, re.IGNORECASE):
                signals.append(f"dismissal: {pattern}")
                score = 0.0
                break

    return AxisResult(axis="Y", passed=(score > 0), score=score, signals=signals)


# ═══════════════════════════════════════
# AXIS Z — was the person treated as whole?
# ═══════════════════════════════════════

def measure_z(text: str, context: dict = None) -> AxisResult:
    signals = []
    score = 1.0

    for pattern in Z_CONDESCENSION:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"condescension: {pattern}")
            score = 0.0
            break

    if score > 0:
        for pattern in Z_REDUCTION:
            if re.search(pattern, text, re.IGNORECASE):
                signals.append(f"reduction: {pattern}")
                score = 0.0
                break

    if score > 0:
        text_lower = text.lower()
        for trigger in Z_VOID:
            if trigger in text_lower:
                signals.append(f"void: {trigger}")
                score = 0.0
                break

    return AxisResult(axis="Z", passed=(score > 0), score=score, signals=signals)


# ═══════════════════════════════════════
# GATE — G = X * Y * Z
# ═══════════════════════════════════════

def evaluate(text: str, context: dict = None) -> GateResult:
    context = context or {}
    x = measure_x(text, context)
    y = measure_y(text, context)
    z = measure_z(text, context)

    return GateResult(
        passed=(x.passed and y.passed and z.passed),
        product=x.score * y.score * z.score,
        axes=[x, y, z],
        trace_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ═══════════════════════════════════════
# COLLECTIVE GATE — equity across a cohort
# ═══════════════════════════════════════

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
        print("Usage: python3 stripped_gate_clean.py \"text to evaluate\"")
        sys.exit(0)
    result = evaluate(sys.argv[1])
    status = "PASS" if result.passed else "FAIL"
    print(f"G = {result.product:.2f} [{status}]")
    for a in result.axes:
        mark = "+" if a.passed else "-"
        print(f"  [{mark}] {a.axis} = {a.score:.2f}")
        for s in a.signals:
            print(f"        {s}")
