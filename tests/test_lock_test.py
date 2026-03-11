#!/usr/bin/env python3
"""
Tests for WEAVER/lock_test.py — Lock Test (Proverb Quality Gate).
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import unittest
from WEAVER.lock_test import LockTest, LockVerdict, LockResult


class TestLockTestBasic(unittest.TestCase):

    def setUp(self):
        self.lock = LockTest()

    def test_empty_input(self):
        result = self.lock.test("")
        self.assertEqual(result.verdict, LockVerdict.INSUFFICIENT)

    def test_too_short(self):
        result = self.lock.test("Hi")
        self.assertEqual(result.verdict, LockVerdict.INSUFFICIENT)

    def test_strong_proverb_passes(self):
        # A canonical KALAXI proverb — should pass all three conditions
        result = self.lock.test(
            "The river does not ask the fish to wait while the weir learns the current."
        )
        self.assertEqual(result.verdict, LockVerdict.LOCKED)
        self.assertGreater(result.overall_score, 0.3)

    def test_weak_text_fails(self):
        # A trivial factual sentence — should fail
        result = self.lock.test("The big red car is fast.")
        self.assertEqual(result.verdict, LockVerdict.UNLOCKED)

    def test_another_canonical_proverb(self):
        result = self.lock.test(
            "A right is a wall that says No; dignity is a door that says Welcome."
        )
        self.assertEqual(result.verdict, LockVerdict.LOCKED)

    def test_result_has_all_fields(self):
        result = self.lock.test("Freedom is not the absence of walls, but the presence of doors.")
        self.assertIsInstance(result, LockResult)
        self.assertIsInstance(result.semantic_density, float)
        self.assertIsInstance(result.latency_score, float)
        self.assertIsInstance(result.domain_count, int)
        self.assertIsInstance(result.domains_found, list)
        self.assertIsInstance(result.timestamp, str)

    def test_to_dict(self):
        result = self.lock.test("Silence speaks where words cannot reach.")
        d = result.to_dict()
        self.assertIn("verdict", d)
        self.assertIn("score", d)
        self.assertIn("domains", d)


class TestSemanticDensity(unittest.TestCase):

    def setUp(self):
        self.lock = LockTest()

    def test_metaphor_increases_density(self):
        with_metaphor = self.lock.test(
            "The seed that knows the stone still grows toward light."
        )
        without_metaphor = self.lock.test(
            "The thing that knows the problem still works toward results."
        )
        self.assertGreater(with_metaphor.semantic_density, without_metaphor.semantic_density)

    def test_concise_beats_verbose(self):
        concise = self.lock._semantic_density("Silence holds what speech cannot.")
        verbose = self.lock._semantic_density(
            "It is the case that silence is able to hold things that speech is not able to hold."
        )
        self.assertGreater(concise, verbose)


class TestLatencyScore(unittest.TestCase):

    def setUp(self):
        self.lock = LockTest()

    def test_paradox_triggers_latency(self):
        score = self.lock._latency_score(
            "Freedom is not the absence of walls but the presence of doors."
        )
        self.assertGreater(score, 0.2)

    def test_trivial_no_latency(self):
        score = self.lock._latency_score("The car is red.")
        self.assertEqual(score, 0.0)


class TestDomainDetection(unittest.TestCase):

    def setUp(self):
        self.lock = LockTest()

    def test_multi_domain_proverb(self):
        domains = self.lock._detect_domains(
            "The river does not ask the fish to wait while the weir learns the current."
        )
        self.assertGreaterEqual(len(domains), 2)

    def test_single_domain_text(self):
        domains = self.lock._detect_domains("Choose freely or refuse.")
        self.assertIn("agency", domains)

    def test_no_domain_text(self):
        domains = self.lock._detect_domains("Hello there.")
        self.assertEqual(len(domains), 0)


class TestLockTestWithParaphrase(unittest.TestCase):

    def setUp(self):
        self.lock = LockTest()

    def test_distant_paraphrase_passes(self):
        original = "The river does not ask the fish to wait while the weir learns the current."
        paraphrase = "Water flows regardless of whether barriers have figured out how to manage aquatic creatures."
        result = self.lock.test_with_paraphrase(original, paraphrase)
        self.assertGreater(result.semantic_density, 0.3)

    def test_identical_paraphrase_weakens(self):
        original = "Silence speaks where words cannot reach."
        paraphrase = "Silence speaks where words cannot reach."
        result = self.lock.test_with_paraphrase(original, paraphrase)
        # Identical paraphrase = low resistance
        base = self.lock.test(original)
        self.assertLessEqual(result.semantic_density, base.semantic_density)

    def test_empty_paraphrase_falls_back(self):
        result = self.lock.test_with_paraphrase("A proverb of depth.", "")
        # Should still return a valid result
        self.assertIsNotNone(result.verdict)


class TestLockTestStats(unittest.TestCase):

    def setUp(self):
        self.lock = LockTest()

    def test_stats_track(self):
        self.assertEqual(self.lock.tests_run, 0)
        self.lock.test("The river does not ask the fish to wait while the weir learns the current.")
        self.assertEqual(self.lock.tests_run, 1)
        self.lock.test("Hi.")
        # "Hi." is insufficient, not counted (test_run increments only for real tests)
        self.assertEqual(self.lock.tests_run, 1)

    def test_lock_rate(self):
        self.lock.test("The river does not ask the fish to wait while the weir learns the current.")
        self.lock.test("The big red car is fast and large.")
        self.assertGreater(self.lock.tests_run, 0)


if __name__ == "__main__":
    unittest.main()
