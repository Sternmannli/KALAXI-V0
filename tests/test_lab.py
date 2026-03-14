#!/usr/bin/env python3
"""
Tests for WEAVER/lab.py — The Science Organ.
Covers classification, rigor assessment, Forge routing, and warnings.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.lab import lab_sense, ScienceType, RigorLevel


# ── Activation ─────────────────────────────────────────────────

def test_lab_activates_on_science():
    r = lab_sense("I observed a pattern in the data")
    assert r.active is True, "Lab should activate on scientific content"


def test_lab_inactive_on_non_science():
    r = lab_sense("Can you make me a sandwich?")
    assert r.active is False, "Lab should not activate on non-science"


# ── Classification ─────────────────────────────────────────────

def test_observation_detected():
    r = lab_sense("I noticed an unexpected pattern that seems anomalous")
    assert ScienceType.OBSERVATION in r.science_types


def test_hypothesis_detected():
    r = lab_sense("My hypothesis is that if we increase X then Y will change")
    assert ScienceType.HYPOTHESIS in r.science_types


def test_experiment_detected():
    r = lab_sense("Run the experiment with a control condition and measure the variable")
    assert ScienceType.EXPERIMENT in r.science_types


def test_result_detected():
    r = lab_sense("The result shows a significant correlation with p-value 0.01")
    assert ScienceType.RESULT in r.science_types


def test_critique_detected():
    r = lab_sense("However this has a limitation and possible confirmation bias")
    assert ScienceType.CRITIQUE in r.science_types


# ── Rigor Assessment ───────────────────────────────────────────

def test_anecdote_rigor():
    r = lab_sense("I noticed something unexpected yesterday")
    assert r.rigor_level == RigorLevel.ANECDOTE


def test_preregistered_rigor():
    r = lab_sense("We preregistered our hypothesis before collecting data in the experiment")
    assert r.rigor_level == RigorLevel.PREREGISTERED


def test_structured_rigor():
    r = lab_sense("The experiment uses a control group with matched baseline and systematic methodology")
    assert r.rigor_level == RigorLevel.STRUCTURED


# ── Forge Routing ──────────────────────────────────────────────

def test_forge_triggered_on_model_testing():
    r = lab_sense("Let's test DeepSeek by sending it a fresh session")
    assert r.forge_needed is True, "Forge should trigger when testing AI models"


def test_forge_not_triggered_on_normal_science():
    r = lab_sense("I want to measure the correlation between variables")
    assert r.forge_needed is False, "Forge should not trigger without model testing"


# ── Rigor Warnings ─────────────────────────────────────────────

def test_certainty_language_warned():
    r = lab_sense("This proves definitely that the hypothesis is correct")
    certainty_warnings = [w for w in r.rigor_warnings if "certainty" in w.lower()]
    assert len(certainty_warnings) > 0, "Should warn on absolute certainty language"


def test_missing_sample_size_warned():
    r = lab_sense("The experiment shows significant results compared to control")
    sample_warnings = [w for w in r.rigor_warnings if "sample size" in w.lower()]
    assert len(sample_warnings) > 0, "Should warn on missing n="


def test_harking_warned():
    r = lab_sense("My hypothesis predicted exactly this result which we found in the data")
    hark_warnings = [w for w in r.rigor_warnings if "preregistration" in w.lower()]
    assert len(hark_warnings) > 0, "Should warn on hypothesis + result without preregistration"


# ── Inventory Links ────────────────────────────────────────────

def test_links_to_exp001():
    r = lab_sense("The efficiency wrapper in condition A vs condition B")
    assert any("EXP-001" in l for l in r.inventory_links), "Should link to EXP-001"


def test_links_to_deepseek_obs():
    r = lab_sense("DeepSeek misidentified itself during the test")
    assert any("DeepSeek" in l for l in r.inventory_links), "Should link to DeepSeek observations"


# ── Log Entry ──────────────────────────────────────────────────

def test_log_entry_exists():
    r = lab_sense("I observed a pattern in the experiment data")
    assert "[LAB" in r.log_entry, "Log entry should start with [LAB"
    assert "Types:" in r.log_entry, "Log should contain type information"


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
