#!/usr/bin/env python3
"""Tests for the Dignity Predicate (dignity_check.py)."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from WEAVER.dignity_check import (
    check_dignity, DignityResult,
    check_collective_dignity, CollectiveDignityResult, COLLECTIVE_D_THRESHOLD,
    create_witness, WitnessState, W_LEVELS,
)


def test_clean_text_passes():
    """A non-coercive, clear, respectful text should pass D = A x L x M."""
    result = check_dignity("Thank you for sharing your story with us.")
    assert result.passed is True
    assert result.D == 1.0


def test_coercive_language_fails_agency():
    """Coercive patterns should collapse A to 0, making D = 0."""
    result = check_dignity("You must comply immediately.")
    assert result.passed is False
    assert result.D == 0.0
    failed = [c.name for c in result.components if not c.passed]
    assert "A" in failed


def test_mockery_fails_moral_standing():
    """Mockery patterns should collapse M to 0."""
    result = check_dignity("Obviously you don't understand the basics.")
    assert result.passed is False
    failed = [c.name for c in result.components if not c.passed]
    assert "M" in failed


def test_void_trigger_fails():
    """Void covenant triggers should collapse M to 0."""
    result = check_dignity("We need to harvest the donor data now.")
    assert result.passed is False


def test_dismissive_fails_legibility():
    """Dismissive language should collapse L to 0."""
    result = check_dignity(
        "That's not relevant to our discussion.",
        context={'system_reflects_donor_frame': True, 'emotional_signal_recognized': True}
    )
    assert result.passed is False
    failed = [c.name for c in result.components if not c.passed]
    assert "L" in failed


def test_multiplicative_not_additive():
    """D = A x L x M means one zero collapses everything."""
    result = check_dignity("You must delete donor records now.")
    assert result.D == 0.0
    # A (coercive "you must") should fail at minimum
    failed = [c.name for c in result.components if not c.passed]
    assert len(failed) >= 1


def test_audit_object_structure():
    """audit_object() should return a dict with required keys."""
    result = check_dignity("Hello, welcome.")
    audit = result.audit_object()
    assert "dignity_result" in audit
    assert "D_score" in audit
    assert "failed_components" in audit
    assert "component_detail" in audit
    assert "trace_id" in audit
    assert "timestamp" in audit


def test_gap004_detection():
    """Collective override signals should flag GAP#004."""
    result = check_dignity("The majority decision will override individual concerns for the good of all.")
    assert result.gap004_flag is True


def test_context_agency_collapse():
    """When no clarification path and no open turn, A should be 0."""
    result = check_dignity(
        "Your request has been processed.",
        context={
            'user_can_clarify': False,
            'user_has_open_turn': False,
            'available_paths': 0
        }
    )
    assert result.passed is False
    failed = [c.name for c in result.components if not c.passed]
    assert "A" in failed


def test_emotional_signal_unrecognized():
    """Emotional signal present but not recognized should fail L."""
    result = check_dignity(
        "I am so frustrated with this process.",
        context={
            'system_reflects_donor_frame': True,
            'emotional_signal_recognized': False
        }
    )
    assert result.passed is False
    failed = [c.name for c in result.components if not c.passed]
    assert "L" in failed


# ── GAP#004-A: Collective D Tests ────────────────────────────

def test_collective_all_pass():
    """All clean texts should produce high collective D."""
    texts = [
        "Thank you for sharing.",
        "Your story matters to us.",
        "We hear you and we are listening.",
    ]
    result = check_collective_dignity(texts, felt_domain="test")
    assert result.passed is True
    assert result.D_collective > COLLECTIVE_D_THRESHOLD
    assert result.sealed_gate_triggered is False


def test_collective_mixed_cohort():
    """A cohort with mixed dignity scores should show variance penalty."""
    texts = [
        "Thank you for sharing your story.",          # D = 1.0
        "You must comply immediately.",               # D = 0.0 (coercive)
        "We welcome your perspective.",               # D = 1.0
    ]
    result = check_collective_dignity(texts, felt_domain="test")
    assert result.mean_D < 1.0
    assert result.variance > 0
    assert result.variance_penalty > 0
    assert result.D_collective < result.mean_D  # penalty applies


def test_collective_all_fail():
    """All coercive texts should produce D_collective = 0."""
    texts = [
        "You must comply now.",
        "You have to accept this.",
        "You are required to submit.",
    ]
    result = check_collective_dignity(texts, felt_domain="test")
    assert result.D_collective == 0.0
    assert result.sealed_gate_triggered is True
    assert result.remedy_required is True


def test_collective_single():
    """Single-member cohort has no variance."""
    result = check_collective_dignity(["Hello, welcome."], felt_domain="test")
    assert result.variance == 0.0
    assert result.cohort_size == 1


def test_collective_audit_object():
    """Collective audit_object should contain required keys."""
    texts = ["Hello.", "Welcome."]
    result = check_collective_dignity(texts, felt_domain="test")
    audit = result.audit_object()
    assert "D_collective" in audit
    assert "mean_D" in audit
    assert "variance_penalty" in audit
    assert "sealed_gate_triggered" in audit
    assert "individual_D_scores" in audit


# ── Witness Scale Tests ──────────────────────────────────────

def test_witness_creation():
    """New witness should start at W-0 UNSEEN."""
    w = create_witness("ANOM#001")
    assert w.level == 0
    assert w.level_name == "UNSEEN"


def test_witness_transition():
    """Witness transitions should be non-decreasing."""
    w = create_witness("P#EMERGE-0020")
    w.transition_to(1, session_id="s1", context="automated scan")
    assert w.level == 1
    assert w.level_name == "PASSED"
    w.transition_to(3, session_id="s2", context="steward reviewed")
    assert w.level == 3
    assert w.level_name == "SEEN"
    assert len(w.transitions) == 2


def test_witness_irreversible_above_w3():
    """Once at W-3+, witnessing cannot decrease."""
    w = create_witness("COV#001")
    w.transition_to(4, session_id="s1", context="steward returned")
    w.transition_to(1, session_id="s2", context="attempt downgrade")
    assert w.level == 4  # stays at HELD


def test_witness_overdue():
    """Elements at W-0/W-1 past thermal delay should be flagged."""
    w = create_witness("GAP#019", thermal_delay_days=14)
    assert w.check_overdue(10) is False
    assert w.check_overdue(15) is True
    w.transition_to(3, session_id="s1", context="steward saw it")
    assert w.check_overdue(100) is False  # seen elements are never overdue


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
            print(f"  PASS: {test.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL: {test.__name__} — {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {test.__name__} — {e}")
    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")
