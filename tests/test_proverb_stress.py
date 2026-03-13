#!/usr/bin/env python3
"""Tests for Seed #11: Proverb Stress Test Engine."""

import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.proverb_stress_test import ProverbStressTest, ProverbHealth


def test_register_and_test():
    engine = ProverbStressTest()
    engine.register_proverb("P#0025", "Hurry carves ruts; patience builds roads.", "agency")
    record = engine.test("P#0025", "ANOM#0020", held=True, notes="Proverb held")
    assert record.proverb_held
    assert record.anomaly_id == "ANOM#0020"


def test_health_strong():
    engine = ProverbStressTest()
    engine.register_proverb("P#0001", "Test proverb", "test")
    for i in range(10):
        engine.test("P#0001", f"ANOM#{i}", held=True)
    assert engine.assess_health("P#0001") == ProverbHealth.STRONG


def test_health_stable():
    engine = ProverbStressTest()
    engine.register_proverb("P#0001", "Test proverb", "test")
    for i in range(8):
        engine.test("P#0001", f"ANOM#{i}", held=True)
    for i in range(2):
        engine.test("P#0001", f"ANOM#F{i}", held=False)
    # 80% pass rate → STABLE
    assert engine.assess_health("P#0001") == ProverbHealth.STABLE


def test_health_stressed():
    engine = ProverbStressTest()
    engine.register_proverb("P#0001", "Test proverb", "test")
    for i in range(6):
        engine.test("P#0001", f"ANOM#{i}", held=True)
    for i in range(4):
        engine.test("P#0001", f"ANOM#F{i}", held=False)
    # 60% pass rate → STRESSED
    assert engine.assess_health("P#0001") == ProverbHealth.STRESSED


def test_health_failing():
    engine = ProverbStressTest()
    engine.register_proverb("P#0001", "Test proverb", "test")
    for i in range(3):
        engine.test("P#0001", f"ANOM#{i}", held=True)
    for i in range(7):
        engine.test("P#0001", f"ANOM#F{i}", held=False)
    # 30% pass rate → FAILING
    assert engine.assess_health("P#0001") == ProverbHealth.FAILING


def test_not_enough_data():
    engine = ProverbStressTest()
    engine.register_proverb("P#0001", "Test proverb", "test")
    engine.test("P#0001", "ANOM#0001", held=False)
    # Only 1 test, minimum is 3 → STABLE (not enough data)
    assert engine.assess_health("P#0001") == ProverbHealth.STABLE


def test_report():
    engine = ProverbStressTest()
    engine.register_proverb("P#0025", "Hurry carves ruts; patience builds roads.", "agency")
    for i in range(5):
        engine.test("P#0025", f"ANOM#{i}", held=True)
    engine.test("P#0025", "ANOM#bad", held=False)

    report = engine.report("P#0025")
    assert report.tests_run == 6
    assert report.tests_passed == 5
    assert report.health == ProverbHealth.STABLE
    assert "ANOM#bad" in report.recent_failures


def test_flagged():
    engine = ProverbStressTest()
    engine.register_proverb("P#good", "Strong proverb", "test")
    engine.register_proverb("P#bad", "Failing proverb", "test")

    for i in range(10):
        engine.test("P#good", f"ANOM#{i}", held=True)
    for i in range(10):
        engine.test("P#bad", f"ANOM#{i}", held=False)

    flagged = engine.flagged()
    assert len(flagged) == 1
    assert flagged[0].proverb_id == "P#bad"
    assert flagged[0].health == ProverbHealth.FAILING


def test_unregistered_raises():
    engine = ProverbStressTest()
    try:
        engine.test("P#NOPE", "ANOM#0001", held=True)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
