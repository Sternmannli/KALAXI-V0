#!/usr/bin/env python3
"""Tests for the Dignity Predicate (dignity_check.py)."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from WEAVER.dignity_check import check_dignity, DignityResult


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
