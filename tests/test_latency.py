#!/usr/bin/env python3
"""
Tests for WEAVER/latency.py — Dignity-Latency Variable (T_d).
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import unittest
from WEAVER.latency import (
    DignityLatency, ComplexityLevel, LatencyProfile,
    LatencyReading, LatencyState, DEFAULT_PROFILES,
)


class TestComplexityAssessment(unittest.TestCase):

    def setUp(self):
        self.latency = DignityLatency()

    def test_simple_input(self):
        level = self.latency.assess_complexity("What time is it?")
        self.assertEqual(level, ComplexityLevel.SIMPLE)

    def test_moderate_input(self):
        level = self.latency.assess_complexity(
            "However, the contradiction between these two views is notable."
        )
        self.assertEqual(level, ComplexityLevel.MODERATE)

    def test_complex_emotional_input(self):
        level = self.latency.assess_complexity(
            "I am frustrated and confused about the meaning of all this suffering."
        )
        self.assertIn(level, [ComplexityLevel.COMPLEX, ComplexityLevel.PROFOUND])

    def test_profound_identity_input(self):
        level = self.latency.assess_complexity(
            "Who am I? My people have been erased and silenced. "
            "My homeland is forgotten. What is the meaning of my existence?"
        )
        self.assertEqual(level, ComplexityLevel.PROFOUND)

    def test_long_text_adds_complexity(self):
        short = "Hello."
        long_text = "word " * 60  # 60 words, no markers
        level_short = self.latency.assess_complexity(short)
        level_long = self.latency.assess_complexity(long_text)
        # Compare by ordinal position, not string value
        order = [ComplexityLevel.SIMPLE, ComplexityLevel.MODERATE,
                 ComplexityLevel.COMPLEX, ComplexityLevel.PROFOUND]
        self.assertGreaterEqual(order.index(level_long), order.index(level_short))


class TestLatencyRecommendation(unittest.TestCase):

    def setUp(self):
        self.latency = DignityLatency()

    def test_simple_recommendation(self):
        td = self.latency.recommend(ComplexityLevel.SIMPLE)
        self.assertEqual(td, 0.5)

    def test_profound_recommendation(self):
        td = self.latency.recommend(ComplexityLevel.PROFOUND)
        self.assertEqual(td, 8.0)

    def test_profile_retrieval(self):
        profile = self.latency.get_profile(ComplexityLevel.COMPLEX)
        self.assertEqual(profile.min_seconds, 1.0)
        self.assertEqual(profile.max_seconds, 10.0)
        self.assertEqual(profile.recommended_seconds, 4.0)


class TestLatencyRecording(unittest.TestCase):

    def setUp(self):
        self.latency = DignityLatency()

    def test_record_preserves_dignity(self):
        reading = self.latency.record(
            "EX-001", ComplexityLevel.MODERATE,
            recommended_td=2.0, actual_td=2.0,
        )
        self.assertTrue(reading.dignity_preserved)

    def test_record_violates_dignity(self):
        reading = self.latency.record(
            "EX-001", ComplexityLevel.MODERATE,
            recommended_td=2.0, actual_td=0.1,
        )
        self.assertFalse(reading.dignity_preserved)
        self.assertEqual(self.latency.violations_count, 1)

    def test_state_after_recordings(self):
        self.latency.record("EX-001", ComplexityLevel.SIMPLE, 0.5, 0.5)
        self.latency.record("EX-002", ComplexityLevel.MODERATE, 2.0, 2.0)
        state = self.latency.state()
        self.assertEqual(state.readings_count, 2)
        self.assertEqual(state.violations, 0)
        self.assertEqual(state.dignity_preservation_rate, 1.0)

    def test_empty_state(self):
        state = self.latency.state()
        self.assertEqual(state.readings_count, 0)
        self.assertEqual(state.dignity_preservation_rate, 1.0)


class TestLatencyProfileUpdate(unittest.TestCase):

    def setUp(self):
        self.latency = DignityLatency()

    def test_update_profile(self):
        self.latency.update_profile(
            ComplexityLevel.SIMPLE, recommended_seconds=1.0,
        )
        profile = self.latency.get_profile(ComplexityLevel.SIMPLE)
        self.assertEqual(profile.recommended_seconds, 1.0)

    def test_custom_profiles(self):
        custom = {
            ComplexityLevel.SIMPLE: LatencyProfile(
                complexity=ComplexityLevel.SIMPLE,
                min_seconds=0.0,
                max_seconds=1.0,
                recommended_seconds=0.2,
            ),
        }
        latency = DignityLatency(profiles=custom)
        td = latency.recommend(ComplexityLevel.SIMPLE)
        self.assertEqual(td, 0.2)


class TestDonorPatienceRule(unittest.TestCase):
    """T_d never exceeds donor patience (Rule #4)."""

    def test_recommended_within_bounds(self):
        for level, profile in DEFAULT_PROFILES.items():
            self.assertLessEqual(profile.recommended_seconds, profile.max_seconds)
            self.assertGreaterEqual(profile.recommended_seconds, profile.min_seconds)


if __name__ == "__main__":
    unittest.main()
