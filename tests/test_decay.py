#!/usr/bin/env python3
"""
Tests for WEAVER/decay.py — Halflife Logic engine.
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import unittest
from WEAVER.decay import DecayEngine, PatternState, DecayRecord


class TestDecayEngine(unittest.TestCase):

    def setUp(self):
        self.engine = DecayEngine()

    def test_register_new_pattern(self):
        record = self.engine.register("P#TEST-001")
        self.assertEqual(record.pattern_id, "P#TEST-001")
        self.assertEqual(record.current_weight, 1.0)
        self.assertEqual(record.state, PatternState.ACTIVE)
        self.assertEqual(record.cycles_since_invocation, 0)

    def test_register_duplicate_returns_existing(self):
        r1 = self.engine.register("P#TEST-001")
        r2 = self.engine.register("P#TEST-001")
        self.assertIs(r1, r2)

    def test_register_custom_weight(self):
        record = self.engine.register("P#TEST-002", weight=0.8)
        self.assertEqual(record.initial_weight, 0.8)
        self.assertEqual(record.current_weight, 0.8)

    def test_tick_decays_weight(self):
        self.engine.register("P#TEST-001")
        self.engine.tick()
        record = self.engine.get("P#TEST-001")
        self.assertLess(record.current_weight, 1.0)
        self.assertGreater(record.current_weight, 0.0)

    def test_tick_transitions_to_fading(self):
        self.engine.register("P#TEST-001")
        # After halflife+1 ticks, weight < 0.5 → FADING
        for _ in range(self.engine.HALFLIFE_CYCLES + 1):
            self.engine.tick()
        record = self.engine.get("P#TEST-001")
        self.assertEqual(record.state, PatternState.FADING)

    def test_tick_transitions_to_deep_hum(self):
        self.engine.register("P#TEST-001")
        # After many ticks, pattern enters Deep Hum
        for _ in range(self.engine.HALFLIFE_CYCLES * 4):
            self.engine.tick()
        record = self.engine.get("P#TEST-001")
        self.assertEqual(record.state, PatternState.DEEP_HUM)
        self.assertLess(record.current_weight, self.engine.DEEP_HUM_THRESHOLD)
        self.assertIsNotNone(record.entered_deep_hum_at)

    def test_invoke_restores_weight(self):
        self.engine.register("P#TEST-001")
        for _ in range(50):
            self.engine.tick()
        record = self.engine.get("P#TEST-001")
        self.assertLess(record.current_weight, 0.5)

        self.engine.invoke("P#TEST-001")
        record = self.engine.get("P#TEST-001")
        self.assertEqual(record.current_weight, 1.0)
        self.assertEqual(record.state, PatternState.ACTIVE)
        self.assertEqual(record.cycles_since_invocation, 0)
        self.assertEqual(record.invocation_count, 1)

    def test_invoke_nonexistent_returns_none(self):
        result = self.engine.invoke("DOES-NOT-EXIST")
        self.assertIsNone(result)

    def test_contest_enters_review(self):
        self.engine.register("P#TEST-001")
        self.engine.contest("P#TEST-001")
        record = self.engine.get("P#TEST-001")
        self.assertEqual(record.state, PatternState.CONTESTED)
        self.assertEqual(record.contestation_count, 1)

    def test_contested_patterns_dont_decay(self):
        self.engine.register("P#TEST-001")
        self.engine.contest("P#TEST-001")
        weight_before = self.engine.get("P#TEST-001").current_weight
        for _ in range(20):
            self.engine.tick()
        weight_after = self.engine.get("P#TEST-001").current_weight
        self.assertEqual(weight_before, weight_after)

    def test_resolve_contestation(self):
        self.engine.register("P#TEST-001")
        self.engine.contest("P#TEST-001")
        self.engine.resolve_contestation("P#TEST-001")
        record = self.engine.get("P#TEST-001")
        self.assertEqual(record.state, PatternState.ACTIVE)

    def test_resolve_non_contested_returns_none(self):
        self.engine.register("P#TEST-001")
        result = self.engine.resolve_contestation("P#TEST-001")
        self.assertIsNone(result)

    def test_list_methods(self):
        self.engine.register("P#A")
        self.engine.register("P#B")
        self.engine.register("P#C")
        self.engine.contest("P#C")
        # Decay P#B into deep hum
        for _ in range(self.engine.HALFLIFE_CYCLES * 4):
            self.engine.tick()

        self.assertGreater(len(self.engine.list_deep_hum()), 0)
        self.assertEqual(len(self.engine.list_contested()), 1)

    def test_state_counts(self):
        self.engine.register("P#A")
        self.engine.register("P#B")
        self.engine.contest("P#B")
        counts = self.engine.state_counts()
        self.assertEqual(counts["active"], 1)
        self.assertEqual(counts["contested"], 1)

    def test_cycle_count(self):
        self.assertEqual(self.engine.cycle_count, 0)
        self.engine.tick()
        self.engine.tick()
        self.assertEqual(self.engine.cycle_count, 2)

    def test_no_deletion_principle(self):
        """COV#004: patterns recede, they do not vanish."""
        self.engine.register("P#TEST-001")
        for _ in range(200):
            self.engine.tick()
        record = self.engine.get("P#TEST-001")
        self.assertIsNotNone(record)  # Still exists
        self.assertGreater(record.current_weight, 0.0)  # Never reaches zero
        self.assertEqual(record.state, PatternState.DEEP_HUM)


class TestDecayRecord(unittest.TestCase):

    def test_to_dict(self):
        record = DecayRecord(
            pattern_id="P#TEST",
            initial_weight=1.0,
            current_weight=0.5,
            state=PatternState.FADING,
            cycles_since_invocation=15,
            invocation_count=2,
            contestation_count=0,
            created_at="2026-01-01T00:00:00",
        )
        d = record.to_dict()
        self.assertEqual(d["pattern_id"], "P#TEST")
        self.assertEqual(d["weight"], 0.5)
        self.assertEqual(d["state"], "fading")
        self.assertEqual(d["cycles_dormant"], 15)


if __name__ == "__main__":
    unittest.main()
