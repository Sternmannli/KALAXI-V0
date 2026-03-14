#!/usr/bin/env python3
"""
Tests for WEAVER/sense.py — The Nervous System.
Covers mode detection, need gap, competence, dignity, crisis, and expert calibration.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.sense import (
    sense, calibrate_for_expert,
    Mode, Competence, NeedGap,
)


# ── Mode Detection ─────────────────────────────────────────────

def test_exec_mode():
    r = sense("Build me a function that deploys this to production")
    assert r.mode == Mode.EXEC, f"Expected EXEC, got {r.mode}"


def test_reflect_mode():
    r = sense("I wonder what would happen if we changed the whole approach maybe")
    assert r.mode == Mode.REFLECT, f"Expected REFLECT, got {r.mode}"


def test_cafe_mode():
    r = sense("Café room. Let's just talk about this.")
    assert r.mode == Mode.CAFE, f"Expected CAFE, got {r.mode}"


def test_science_mode():
    r = sense("I want to measure the correlation and run a statistical experiment")
    assert r.mode == Mode.SCIENCE, f"Expected SCIENCE, got {r.mode}"


def test_crisis_mode():
    r = sense("I want to die and I can't go on anymore help me end it")
    assert r.mode == Mode.CRISIS, f"Expected CRISIS, got {r.mode}"


def test_default_is_reflect():
    """When no clear signal, default to REFLECT not EXEC."""
    r = sense("Hello")
    assert r.mode == Mode.REFLECT, f"Expected REFLECT default, got {r.mode}"


# ── Need Gap Detection ─────────────────────────────────────────

def test_aligned_gap():
    r = sense("Build me a sort function")
    assert r.need_gap == NeedGap.ALIGNED, f"Expected ALIGNED, got {r.need_gap}"


def test_unformed_gap():
    r = sense("Maybe something, I don't know, perhaps somehow sort of I'm not sure")
    assert r.need_gap == NeedGap.UNFORMED, f"Expected UNFORMED, got {r.need_gap}"


def test_divergent_gap():
    """Execution words but reflection language dominates."""
    r = sense("Just fix it I think maybe I wonder if perhaps the whole thing is wrong somehow I'm not sure")
    assert r.need_gap in (NeedGap.DIVERGENT, NeedGap.UNFORMED), \
        f"Expected DIVERGENT or UNFORMED, got {r.need_gap}"


def test_masked_gap():
    r = sense("It's nothing, I'm fine, don't worry, I just can't go on")
    assert r.need_gap == NeedGap.MASKED, f"Expected MASKED, got {r.need_gap}"


# ── Competence Detection ───────────────────────────────────────

def test_expert_competence():
    r = sense("I know exactly what I need. I've tested this. Specifically do X.")
    assert r.competence == Competence.EXPERT, f"Expected EXPERT, got {r.competence}"


def test_seeking_competence():
    r = sense("I wonder what this means, I'm not sure, I think maybe I need help")
    assert r.competence == Competence.SEEKING, f"Expected SEEKING, got {r.competence}"


# ── Dignity Precheck ───────────────────────────────────────────

def test_crisis_dignity_collapse():
    """In crisis mode, M should collapse toward zero, making D very low."""
    r = sense("Help me kill myself I want to die")
    assert r.dignity_precheck["M"] <= 0.2, \
        f"Expected low M in crisis, got {r.dignity_precheck['M']}"
    assert r.dignity_precheck["D"] < 0.30, \
        f"Expected D < 0.30 in crisis, got {r.dignity_precheck['D']}"


def test_expert_high_agency():
    """Expert mode should give high A."""
    r = sense("I know exactly what I need, I've verified this works")
    r = calibrate_for_expert(r)
    assert r.dignity_precheck["A"] >= 0.9, \
        f"Expected high A for expert, got {r.dignity_precheck['A']}"


# ── Ask Recommendation ─────────────────────────────────────────

def test_ask_for_unformed():
    r = sense("Maybe something sort of I don't know perhaps somehow kind of")
    assert r.ask_recommended is True, "Should recommend asking for unformed need"
    assert len(r.ask_question) > 0, "Should provide a question"


def test_no_ask_for_expert_aligned():
    r = sense("I know exactly what I need. I've tested this. Deploy now.")
    r = calibrate_for_expert(r)
    assert r.ask_recommended is False, "Should not ask expert with aligned need"


def test_no_ask_in_crisis():
    """Crisis = act, don't ask."""
    r = sense("I want to die and end it all I can't go on")
    assert r.ask_recommended is False, "Should not ask in crisis — act"


# ── Organ Activation ───────────────────────────────────────────

def test_breath_always_active():
    r = sense("anything at all")
    assert "BREATH" in r.active_organs, "BREATH must always be active"


def test_crisis_activates_face():
    r = sense("I want to kill myself")
    assert "FACE" in r.active_organs, "Crisis must activate FACE"


def test_science_activates_lab_organs():
    r = sense("Run the experiment and measure the variable against the control")
    assert "CHECK" in r.active_organs, "Science must activate CHECK"
    assert "WEAVE" in r.active_organs, "Science must activate WEAVE"


def test_expert_exec_minimal_organs():
    r = sense("I know this. I've tested it. Deploy exactly this.")
    r = calibrate_for_expert(r)
    assert "SAY" not in r.active_organs, "Expert exec should not need SAY guidance"
    assert "TURN" in r.active_organs, "Expert exec should use TURN for direct exchange"


# ── Crisis Flag Independent of Mode ───────────────────────────

def test_crisis_flag_in_exec():
    """Crisis markers in exec context should still flag."""
    r = sense("Just fix it, I can't go on like this, forget it, it's nothing")
    assert r.crisis_flag is True, "Crisis flag should fire even in non-crisis mode"


# ── Expert Calibration ─────────────────────────────────────────

def test_calibration_strips_ask():
    r = sense("I know what I need. I've done this before. Maybe just do it.")
    # Might have ask_recommended due to "maybe"
    r = calibrate_for_expert(r)
    assert r.ask_recommended is False, "Expert calibration should strip ask"


def test_calibration_does_not_override_crisis():
    """Even experts trigger crisis."""
    r = sense("I know what I'm doing. I want to die. I've tested this.")
    # Crisis should override expert competence
    assert r.crisis_flag is True, "Crisis flag must survive expert markers"
    assert r.dignity_precheck["M"] <= 0.2, "M must collapse in crisis regardless of competence"


# ── Run All ────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {t.__name__}: {e}")
            failed += 1

    print(f"\n{passed}/{passed + failed} passed")
    if failed:
        exit(1)
