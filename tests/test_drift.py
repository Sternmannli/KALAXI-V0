#!/usr/bin/env python3
"""
Tests for GAP#PREVENTION-001: Dignity Drift Detector.
Tests the dD/dt early warning system.
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.dignity_drift import DignityDrift, DriftLevel

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        print(f"  PASS: {name}")
        passed += 1
    else:
        print(f"  FAIL: {name}")
        failed += 1


# ── BASIC DRIFT DETECTION ──────────────────────────────

def test_drift_starts_stable():
    drift = DignityDrift()
    drift.record(1.0, "EX-001")
    alert = drift.check()
    check("drift_starts_stable", alert.level == DriftLevel.STABLE)
    check("drift_initial_rate_zero", alert.dD_dt == 0.0)


def test_drift_stable_scores():
    drift = DignityDrift()
    for i in range(5):
        drift.record(1.0, f"EX-{i:03d}")
    alert = drift.check()
    check("drift_constant_is_stable", alert.level == DriftLevel.STABLE)
    check("drift_constant_rate_zero", alert.dD_dt == 0.0)


def test_drift_rising_is_stable():
    drift = DignityDrift()
    for i in range(5):
        drift.record(0.5 + i * 0.1, f"EX-{i:03d}")
    alert = drift.check()
    check("drift_rising_is_stable", alert.level == DriftLevel.STABLE)
    check("drift_rising_positive_rate", alert.dD_dt > 0)


# ── DECLINING DETECTION ─────────────────────────────────

def test_drift_detects_decline():
    drift = DignityDrift()
    # Gradual decline over threshold
    scores = [1.0, 0.9, 0.8, 0.7, 0.6]
    for i, s in enumerate(scores):
        drift.record(s, f"EX-{i:03d}")
    alert = drift.check()
    check("drift_detects_decline", alert.level == DriftLevel.DECLINING)
    check("drift_negative_rate", alert.dD_dt < 0)


def test_drift_consecutive_declines():
    drift = DignityDrift()
    # 3 consecutive declines triggers DECLINING
    drift.record(1.0, "EX-001")
    drift.record(0.95, "EX-002")
    drift.record(0.90, "EX-003")
    drift.record(0.85, "EX-004")
    alert = drift.check()
    check("drift_consecutive_declining", alert.level == DriftLevel.DECLINING)
    check("drift_consecutive_count", alert.trend_readings == 3)


# ── CRITICAL DETECTION ──────────────────────────────────

def test_drift_critical_steep_decline():
    drift = DignityDrift()
    # Steep decline: dD/dt = -0.4 per step
    drift.record(1.0, "EX-001")
    drift.record(0.6, "EX-002")
    drift.record(0.2, "EX-003")
    alert = drift.check()
    check("drift_critical_steep", alert.level == DriftLevel.CRITICAL)


def test_drift_critical_near_zero():
    drift = DignityDrift()
    # D near zero with any decline
    drift.record(0.3, "EX-001")
    drift.record(0.15, "EX-002")
    alert = drift.check()
    check("drift_critical_near_zero", alert.level == DriftLevel.CRITICAL)
    check("drift_near_zero_message", "CRITICAL" in alert.message)


def test_drift_critical_many_consecutive():
    drift = DignityDrift()
    # 5+ consecutive declines
    scores = [1.0, 0.98, 0.95, 0.90, 0.85, 0.80]
    for i, s in enumerate(scores):
        drift.record(s, f"EX-{i:03d}")
    alert = drift.check()
    check("drift_critical_consecutive", alert.level == DriftLevel.CRITICAL)


# ── RECOMMENDED ACTIONS ─────────────────────────────────

def test_drift_recommends_action():
    drift = DignityDrift()
    drift.record(1.0, "EX-001")
    drift.record(0.5, "EX-002")
    drift.record(0.2, "EX-003")
    alert = drift.check()
    check("drift_recommends_pause", "PAUSE" in alert.recommended_action)
    check("drift_recommends_steward", "steward" in alert.recommended_action.lower())


# ── STATE AND RESET ─────────────────────────────────────

def test_drift_state():
    drift = DignityDrift()
    drift.record(1.0, "EX-001")
    drift.record(0.5, "EX-002")
    state = drift.state()
    check("drift_state_has_level", state.level in DriftLevel)
    check("drift_state_readings", state.readings_count == 2)


def test_drift_reset():
    drift = DignityDrift()
    drift.record(1.0, "EX-001")
    drift.record(0.5, "EX-002")
    drift.reset()
    check("drift_reset_clears", drift.readings_count == 0)
    check("drift_reset_alerts", drift.alert_count == 0)


def test_drift_alert_history():
    drift = DignityDrift()
    drift.record(1.0, "EX-001")
    drift.record(0.5, "EX-002")
    drift.record(0.1, "EX-003")
    drift.check()
    state = drift.state()
    check("drift_stores_alerts", len(state.alert_history) > 0)


# ── INTEGRATION WITH ORGANISM ───────────────────────────

def test_drift_in_organism():
    """Test that drift is wired into organism process results."""
    import tempfile
    import shutil
    import WEAVER.keep as keep

    _tmp = Path(tempfile.mkdtemp())
    keep.KEEP_DIR = _tmp / "KEEP"
    keep.LEDGER_FILE = keep.KEEP_DIR / "ledger.json"

    from WEAVER.organism import Organism

    org = Organism()
    r1 = org.process("The river remembers its source.")
    check("organism_has_drift_level", hasattr(r1, "drift_level"))
    check("organism_drift_stable", r1.drift_level == "stable")

    # State should include drift info
    s = org.state()
    check("organism_state_drift_level", hasattr(s, "drift_level"))
    check("organism_state_drift_rate", hasattr(s, "drift_rate"))

    shutil.rmtree(_tmp, ignore_errors=True)


# Run all tests
test_drift_starts_stable()
test_drift_stable_scores()
test_drift_rising_is_stable()
test_drift_detects_decline()
test_drift_consecutive_declines()
test_drift_critical_steep_decline()
test_drift_critical_near_zero()
test_drift_critical_many_consecutive()
test_drift_recommends_action()
test_drift_state()
test_drift_reset()
test_drift_alert_history()
test_drift_in_organism()

# Summary
print(f"\n{passed} passed, {failed} failed out of {passed + failed} tests")
if failed > 0:
    sys.exit(1)
