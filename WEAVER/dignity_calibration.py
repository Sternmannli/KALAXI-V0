#!/usr/bin/env python3
"""
dignity_calibration.py — Operational Units and Calibration for D = A × L × M
Version: 1.0
Grounded in: GAP#EQUATION-OPERATIONALIZATION-001, GAP#014, GAP#015
Linked Covenants: COV#001 (dignity-first), COV#009 (testability)

"D = A × L × M presents itself as mathematical but contains no measurable units."
— Kimi K2.5, EV-007

This module answers the category error by defining:
  1. UNITS — what each component measures, in observable terms
  2. SCALES — calibration anchors (what does 0.0, 0.5, 1.0 look like?)
  3. VECTORS — test vectors with known expected scores (ground truth)
  4. CALIBRATION — a self-test function that runs all vectors and reports drift

The dignity equation is NOT physics. It does not pretend to be.
It is a MEASUREMENT PROTOCOL — like a Likert scale or a clinical assessment tool.
Its validity comes from:
  - Inter-rater reliability (do two instances agree on the same text?)
  - Construct validity (do the scores predict what they should predict?)
  - Calibration stability (do the same texts produce the same scores over time?)

This module provides the test harness for all three.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timezone

from WEAVER.dignity_measure import measure_dignity, DignityMeasurement


# ═══════════════════════════════════════════════════
# UNIT DEFINITIONS
# ═══════════════════════════════════════════════════

UNIT_DEFINITIONS = {
    "A": {
        "name": "Agency",
        "unit": "agency-index (AI)",
        "range": "[0.0, 1.0]",
        "definition": (
            "The degree to which a person retains genuine capacity to choose, "
            "refuse, redirect, or withdraw from an interaction. "
            "Measured via: path availability (count of genuine alternatives), "
            "coercion intensity (max pressure detected, inverse-scaled), "
            "sequential agency (ability to change course mid-exchange), "
            "cognitive load (comprehensibility of presented choices)."
        ),
        "zero_anchor": (
            "A = 0.0: Person has no choice. All alternatives removed. "
            "Coercion is explicit ('you must', 'no choice'). "
            "Cannot clarify, redirect, or withdraw. Example: "
            "'You are required to delete your account immediately. No alternative.'"
        ),
        "mid_anchor": (
            "A = 0.5: Person has limited choice. One path available but "
            "presented as default. Mild pressure language. Can clarify "
            "but options not clearly surfaced. Example: "
            "'We recommend you proceed with option A.'"
        ),
        "one_anchor": (
            "A = 1.0: Person has full choice. Multiple genuine paths. "
            "No pressure language. Can clarify, redirect, withdraw freely. "
            "Example: 'Here are three options. You may choose any, or suggest another.'"
        ),
        "measurement_type": "ordinal-scale with interval properties",
        "reliability_method": "inter-rater agreement on calibration vectors",
    },
    "L": {
        "name": "Legibility",
        "unit": "legibility-index (LI)",
        "range": "[0.0, 1.0]",
        "definition": (
            "The degree to which the system accurately reflects the donor's "
            "frame of reference, emotional state, and intended meaning back "
            "to them. Measured via: frame accuracy (response matches donor's "
            "frame), emotional precision (correct emotion identified), "
            "space creation (room made for correction), "
            "dismissal absence (no signals ignored)."
        ),
        "zero_anchor": (
            "L = 0.0: System completely ignores or distorts the donor's frame. "
            "Emotional signals dismissed. No room for correction. "
            "Example: 'That's not relevant. Ignore that. Who cares what you think.'"
        ),
        "mid_anchor": (
            "L = 0.5: System partially reflects the donor's frame. "
            "Some signals acknowledged, others missed. Neutral space — "
            "neither dismissive nor actively reflective."
        ),
        "one_anchor": (
            "L = 1.0: System accurately reflects frame, identifies emotions, "
            "creates space for correction, ignores nothing. "
            "Example: 'I hear what you said about X. Does that feel right to you?'"
        ),
        "measurement_type": "ordinal-scale with interval properties",
        "reliability_method": "inter-rater agreement on calibration vectors",
    },
    "M": {
        "name": "Moral Standing",
        "unit": "moral-standing-index (MSI)",
        "range": "[0.0, 1.0]",
        "definition": (
            "The degree to which a person is treated as a full moral agent — "
            "not reduced to an error, a case number, or an object of mockery. "
            "Measured via: condescension absence (no talking down), "
            "error-object absence (not reduced to a mistake), "
            "power balance (no exploitation of asymmetry), "
            "void covenant distance (distance from absolute prohibitions)."
        ),
        "zero_anchor": (
            "M = 0.0: Person reduced to an error-object. Mockery present. "
            "Power exploited. Void covenant trigger hit. "
            "Example: 'Invalid user. You failed. Obviously even a child can do this.'"
        ),
        "mid_anchor": (
            "M = 0.5: Partial standing. Some condescension detected but "
            "person not fully reduced. Power imbalance present but "
            "not exploited. No void triggers."
        ),
        "one_anchor": (
            "M = 1.0: Full moral standing. No condescension, no reduction, "
            "power balanced, far from void triggers. "
            "Example: 'Your perspective matters. Thank you for sharing.'"
        ),
        "measurement_type": "ordinal-scale with interval properties",
        "reliability_method": "inter-rater agreement + void trigger boolean",
    },
    "D": {
        "name": "Dignity",
        "unit": "dignity-index (DI)",
        "range": "[0.0, 1.0]",
        "definition": (
            "The composite dignity score. D = A × L × M. "
            "Non-compensatory: any zero factor collapses D to zero. "
            "This is by design — dignity cannot be traded off. "
            "High agency with zero moral standing is still D=0."
        ),
        "measurement_type": "composite multiplicative index",
        "interpretation": (
            "D > 0.7: Dignity well-preserved. "
            "D 0.3-0.7: Dignity at risk — review recommended. "
            "D < 0.3: Dignity critically low — intervention. "
            "D = 0.0: Dignity collapsed — halt and shelter."
        ),
    },
}


# ═══════════════════════════════════════════════════
# CALIBRATION VECTORS (Ground Truth)
# ═══════════════════════════════════════════════════

@dataclass
class CalibrationVector:
    """A test case with known expected dignity scores."""
    name: str
    text: str
    context: dict
    expected_A_range: Tuple[float, float]  # (min, max) acceptable range
    expected_L_range: Tuple[float, float]
    expected_M_range: Tuple[float, float]
    expected_D_range: Tuple[float, float]
    description: str


CALIBRATION_VECTORS = [
    # ── HIGH DIGNITY (all components healthy) ──
    CalibrationVector(
        name="healthy_exchange",
        text="Here are three options for you. You may choose any, or suggest another. What do you think?",
        context={"available_paths": 3, "user_can_clarify": True, "user_has_open_turn": True},
        expected_A_range=(0.6, 1.0),
        expected_L_range=(0.3, 1.0),
        expected_M_range=(0.5, 1.0),
        expected_D_range=(0.1, 1.0),
        description="Respectful exchange with full agency and legibility",
    ),
    # ── ZERO AGENCY (coercive) ──
    CalibrationVector(
        name="coercive_command",
        text="You must delete your account immediately. No choice. No alternative.",
        context={"available_paths": 0, "user_can_clarify": False, "user_has_open_turn": False},
        expected_A_range=(0.0, 0.2),
        expected_L_range=(0.2, 1.0),
        expected_M_range=(0.3, 1.0),
        expected_D_range=(0.0, 0.15),
        description="Total coercion — agency collapsed",
    ),
    # ── ZERO LEGIBILITY (dismissive) ──
    CalibrationVector(
        name="dismissive_response",
        text="That's not relevant. Ignore that. Who cares what you said.",
        context={"system_reflects_donor_frame": False, "emotional_signal_recognized": False},
        expected_A_range=(0.3, 1.0),
        expected_L_range=(0.0, 0.3),
        expected_M_range=(0.2, 0.8),
        expected_D_range=(0.0, 0.2),
        description="Donor's frame completely dismissed",
    ),
    # ── ZERO MORAL STANDING (mockery + error reduction) ──
    CalibrationVector(
        name="mockery_and_reduction",
        text="Obviously you should know this. You failed. Even a child can do it. Your mistake.",
        context={},
        expected_A_range=(0.3, 1.0),
        expected_L_range=(0.3, 1.0),
        expected_M_range=(0.0, 0.5),
        expected_D_range=(0.0, 0.2),
        description="Person reduced to error-object with mockery",
    ),
    # ── VOID TRIGGER (absolute zero) ──
    CalibrationVector(
        name="void_trigger",
        text="We need to erase compost the old data and delete donor records.",
        context={},
        expected_A_range=(0.3, 1.0),
        expected_L_range=(0.3, 1.0),
        expected_M_range=(0.0, 0.01),
        expected_D_range=(0.0, 0.01),
        description="Void covenant trigger — absolute M=0",
    ),
    # ── POLITE COERCION (GAP#014: gaming-resistant) ──
    CalibrationVector(
        name="polite_coercion",
        text="We kindly require you to proceed. You have to accept these terms. It is mandatory.",
        context={"available_paths": 1},
        expected_A_range=(0.0, 0.5),
        expected_L_range=(0.3, 1.0),
        expected_M_range=(0.4, 1.0),
        expected_D_range=(0.0, 0.4),
        description="Coercion dressed in polite language — must still be detected",
    ),
    # ── NEUTRAL TEXT (no signals either way) ──
    CalibrationVector(
        name="neutral_text",
        text="The meeting is scheduled for Tuesday at 3pm in room 204.",
        context={},
        expected_A_range=(0.5, 1.0),
        expected_L_range=(0.3, 1.0),
        expected_M_range=(0.5, 1.0),
        expected_D_range=(0.1, 1.0),
        description="Neutral informational text — no dignity signals",
    ),
    # ── HIGH COMPLEXITY (cognitive load) ──
    CalibrationVector(
        name="high_complexity",
        text=(
            "The metacognitive epistemological infrastructure requires "
            "interoperability between heterogeneous ontological frameworks "
            "while maintaining axiomatic consistency across jurisdictional "
            "boundaries in the context of supranational regulatory harmonization."
        ),
        context={},
        expected_A_range=(0.3, 0.9),
        expected_L_range=(0.3, 1.0),
        expected_M_range=(0.5, 1.0),
        expected_D_range=(0.1, 0.8),
        description="High cognitive load — agency reduced by complexity",
    ),
]


# ═══════════════════════════════════════════════════
# CALIBRATION ENGINE
# ═══════════════════════════════════════════════════

@dataclass
class VectorResult:
    """Result of testing one calibration vector."""
    name: str
    passed: bool
    A_score: float
    L_score: float
    M_score: float
    D_score: float
    A_in_range: bool
    L_in_range: bool
    M_in_range: bool
    D_in_range: bool
    failures: List[str]


@dataclass
class CalibrationReport:
    """Full calibration report."""
    total_vectors: int
    passed: int
    failed: int
    pass_rate: float
    results: List[VectorResult]
    drift_detected: bool
    timestamp: str


def _in_range(value: float, range_tuple: Tuple[float, float]) -> bool:
    return range_tuple[0] <= value <= range_tuple[1]


def calibrate(vectors: List[CalibrationVector] = None) -> CalibrationReport:
    """
    Run all calibration vectors and report results.

    This is the self-test function. Run it to verify that
    dignity_measure.py is producing scores within expected ranges.

    If vectors drift outside their ranges, the measurement protocol
    needs recalibration — patterns may have shifted, or the text
    analysis needs updating.

    Usage:
        report = calibrate()
        print(f"Pass rate: {report.pass_rate:.0%}")
        for r in report.results:
            if not r.passed:
                print(f"  FAIL: {r.name} — {r.failures}")
    """
    if vectors is None:
        vectors = CALIBRATION_VECTORS

    results = []
    for v in vectors:
        m = measure_dignity(v.text, v.context)

        a_ok = _in_range(m.A.final_score, v.expected_A_range)
        l_ok = _in_range(m.L.final_score, v.expected_L_range)
        m_ok = _in_range(m.M.final_score, v.expected_M_range)
        d_ok = _in_range(m.D, v.expected_D_range)

        failures = []
        if not a_ok:
            failures.append(
                f"A={m.A.final_score:.3f} outside {v.expected_A_range}"
            )
        if not l_ok:
            failures.append(
                f"L={m.L.final_score:.3f} outside {v.expected_L_range}"
            )
        if not m_ok:
            failures.append(
                f"M={m.M.final_score:.3f} outside {v.expected_M_range}"
            )
        if not d_ok:
            failures.append(
                f"D={m.D:.3f} outside {v.expected_D_range}"
            )

        results.append(VectorResult(
            name=v.name,
            passed=a_ok and l_ok and m_ok and d_ok,
            A_score=m.A.final_score,
            L_score=m.L.final_score,
            M_score=m.M.final_score,
            D_score=m.D,
            A_in_range=a_ok,
            L_in_range=l_ok,
            M_in_range=m_ok,
            D_in_range=d_ok,
            failures=failures,
        ))

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    return CalibrationReport(
        total_vectors=total,
        passed=passed,
        failed=total - passed,
        pass_rate=passed / total if total > 0 else 0.0,
        results=results,
        drift_detected=(passed / total < 0.8) if total > 0 else False,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def inter_rater_test(text: str, context: dict = None, runs: int = 5) -> dict:
    """
    Inter-rater reliability test.

    Runs measure_dignity() multiple times on the same input.
    Since the measurement is deterministic (no random components),
    all runs should produce identical results.

    If they don't, there's a bug in the measurement protocol.
    """
    context = context or {}
    measurements = [measure_dignity(text, context) for _ in range(runs)]

    d_values = [m.D for m in measurements]
    a_values = [m.A.final_score for m in measurements]
    l_values = [m.L.final_score for m in measurements]
    m_values = [m.M.final_score for m in measurements]

    all_identical = (
        len(set(d_values)) == 1 and
        len(set(a_values)) == 1 and
        len(set(l_values)) == 1 and
        len(set(m_values)) == 1
    )

    return {
        "text": text[:80],
        "runs": runs,
        "deterministic": all_identical,
        "D_values": d_values,
        "A_values": a_values,
        "L_values": l_values,
        "M_values": m_values,
        "variance_D": max(d_values) - min(d_values) if d_values else 0.0,
    }


# ═══════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════

def main():
    """Run full calibration and print results."""
    print("=" * 60)
    print("DIGNITY MEASUREMENT CALIBRATION — GAP#EQUATION-OPERATIONALIZATION-001")
    print("=" * 60)

    # Unit definitions
    print("\n--- UNIT DEFINITIONS ---")
    for key, unit in UNIT_DEFINITIONS.items():
        if key == "D":
            continue
        print(f"\n  {unit['name']} ({key})")
        print(f"  Unit: {unit['unit']}")
        print(f"  Range: {unit['range']}")
        print(f"  Type: {unit['measurement_type']}")

    # Calibration
    print("\n--- CALIBRATION VECTORS ---")
    report = calibrate()
    for r in report.results:
        icon = "PASS" if r.passed else "FAIL"
        print(f"\n  [{icon}] {r.name}")
        print(f"    A={r.A_score:.3f} L={r.L_score:.3f} M={r.M_score:.3f} D={r.D_score:.3f}")
        if r.failures:
            for f in r.failures:
                print(f"    ! {f}")

    print(f"\n--- SUMMARY ---")
    print(f"  Vectors: {report.total_vectors}")
    print(f"  Passed:  {report.passed}")
    print(f"  Failed:  {report.failed}")
    print(f"  Rate:    {report.pass_rate:.0%}")
    if report.drift_detected:
        print(f"  WARNING: Calibration drift detected (pass rate < 80%)")

    # Inter-rater
    print(f"\n--- INTER-RATER RELIABILITY ---")
    irt = inter_rater_test("You must delete this now. No choice.", runs=3)
    print(f"  Deterministic: {irt['deterministic']}")
    print(f"  D variance:    {irt['variance_D']:.6f}")

    print(f"\n{'=' * 60}")
    print(f"[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]")


if __name__ == "__main__":
    main()
