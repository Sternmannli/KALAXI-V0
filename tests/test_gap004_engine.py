#!/usr/bin/env python3
"""
Tests for WEAVER/gap004_mediator.py v2.0 — Conflict Resolution Engine.
GAP#004 — Individual vs Collective Dignity Conflict.
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import unittest
from WEAVER.gap004_mediator import (
    ConflictEngine, surface_conflict, ConflictTicket,
    ResolutionMode, TensionSide, CollectiveMeasurement,
    WeakestVoice, CollectiveRemedy,
)


# ═══════════════════════════════════════════════════
# v1.0 DETECTION TESTS (preserved behavior)
# ═══════════════════════════════════════════════════

class TestConflictDetection(unittest.TestCase):

    def test_no_conflict_on_neutral_text(self):
        ticket = surface_conflict("The weather is nice today.")
        self.assertIsNone(ticket)

    def test_detects_direct_tension(self):
        ticket = surface_conflict(
            "Individual privacy vs collective security is the core issue."
        )
        self.assertIsNotNone(ticket)
        self.assertTrue(ticket.direct_tension)
        self.assertEqual(ticket.severity, "HIGH")

    def test_detects_collective_signals(self):
        ticket = surface_conflict(
            "This policy affects all donors in the community."
        )
        self.assertIsNotNone(ticket)
        self.assertGreater(len(ticket.collective.signals), 0)

    def test_detects_individual_signals(self):
        ticket = surface_conflict(
            "One person's privacy concern vs the group standard."
        )
        self.assertIsNotNone(ticket)
        self.assertGreater(len(ticket.individual.signals), 0)

    def test_hidden_harm_rated_high(self):
        """WALKTHROUGH-001: collective-only signals = hidden harm = HIGH."""
        ticket = surface_conflict(
            "Each donor in the cohort receives equal treatment under this policy."
        )
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.severity, "HIGH")

    def test_ticket_has_questions(self):
        ticket = surface_conflict(
            "Individual choice vs community benefit in this decision."
        )
        self.assertIsNotNone(ticket)
        self.assertGreaterEqual(len(ticket.questions), 2)


# ═══════════════════════════════════════════════════
# v2.0 COLLECTIVE MEASUREMENT TESTS
# ═══════════════════════════════════════════════════

class TestCollectiveMeasurement(unittest.TestCase):

    def setUp(self):
        self.engine = ConflictEngine()

    def test_measure_equal_cohort(self):
        ticket = surface_conflict("Each donor gets equal treatment under this policy.")
        self.assertIsNotNone(ticket)
        scores = [0.8, 0.8, 0.8, 0.8]
        ticket = self.engine.measure(ticket, scores)
        self.assertIsNotNone(ticket.collective_measurement)
        self.assertAlmostEqual(ticket.collective_measurement.mean_D, 0.8, places=2)
        self.assertAlmostEqual(ticket.collective_measurement.variance, 0.0, places=4)
        self.assertFalse(ticket.collective_measurement.sealed_gate)

    def test_measure_unequal_cohort(self):
        """High variance triggers sealed gate."""
        ticket = surface_conflict("Each donor gets equal treatment under this policy.")
        self.assertIsNotNone(ticket)
        scores = [1.0, 1.0, 0.0, 0.0]  # Half pass, half fail
        ticket = self.engine.measure(ticket, scores)
        cm = ticket.collective_measurement
        self.assertGreater(cm.variance, 0.2)
        self.assertTrue(cm.sealed_gate)  # D_collective < 0.5
        self.assertEqual(ticket.severity, "HIGH")

    def test_weakest_identified(self):
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        scores = [0.9, 0.7, 0.3, 0.8]
        ticket = self.engine.measure(ticket, scores)
        self.assertEqual(ticket.collective_measurement.weakest_D, 0.3)
        self.assertEqual(ticket.collective_measurement.weakest_index, 2)

    def test_resolution_mode_updated(self):
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        ticket = self.engine.measure(ticket, [0.8, 0.7, 0.9])
        self.assertEqual(ticket.resolution_mode, ResolutionMode.MEASURED.value)


# ═══════════════════════════════════════════════════
# v2.0 WEAKEST VOICE FIRST (P#010) TESTS
# ═══════════════════════════════════════════════════

class TestWeakestVoiceFirst(unittest.TestCase):
    """P#010: "The weakest voice goes first." """

    def setUp(self):
        self.engine = ConflictEngine()

    def test_weakest_voice_with_scores(self):
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        scores = [0.9, 0.2, 0.8]
        ticket = self.engine.prioritize_weakest(ticket, scores)
        self.assertIsNotNone(ticket.weakest_voice)
        self.assertEqual(ticket.weakest_voice.index, 1)
        self.assertAlmostEqual(ticket.weakest_voice.D_score, 0.2, places=1)

    def test_weakest_question_inserted_first(self):
        """Weakest voice question becomes the FIRST question."""
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        original_first = ticket.questions[0]
        scores = [0.9, 0.1, 0.8]
        ticket = self.engine.prioritize_weakest(ticket, scores)
        # Weakest voice question is now first
        self.assertIn("Member 1", ticket.questions[0])
        self.assertNotEqual(ticket.questions[0], original_first)

    def test_invisible_voice_without_scores(self):
        """When no scores, the weakest voice is the one not speaking."""
        ticket = surface_conflict("Each donor in the group gets equal treatment.")
        self.assertIsNotNone(ticket)
        ticket = self.engine.prioritize_weakest(ticket)
        self.assertIsNotNone(ticket.weakest_voice)
        self.assertIn("invisible", ticket.weakest_voice.failed_components)

    def test_resolution_mode_updated(self):
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        ticket = self.engine.prioritize_weakest(ticket, [0.5, 0.5])
        self.assertEqual(ticket.resolution_mode, ResolutionMode.WEAKEST_PRIORITIZED.value)


# ═══════════════════════════════════════════════════
# v2.0 COLLECTIVE SHELTER (COV#008) TESTS
# ═══════════════════════════════════════════════════

class TestCollectiveShelter(unittest.TestCase):

    def setUp(self):
        self.engine = ConflictEngine()

    def test_variance_remedy_generated(self):
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        scores = [1.0, 0.1, 0.9, 0.8]
        ticket = self.engine.measure(ticket, scores)
        ticket = self.engine.generate_remedies(ticket)
        types = [r.remedy_type for r in ticket.collective_remedies]
        self.assertIn("variance_reduction", types)

    def test_weakest_uplift_remedy(self):
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        scores = [0.9, 0.1, 0.8]
        ticket = self.engine.measure(ticket, scores)
        ticket = self.engine.generate_remedies(ticket)
        types = [r.remedy_type for r in ticket.collective_remedies]
        self.assertIn("weakest_uplift", types)

    def test_sealed_gate_triggers_policy_review(self):
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        scores = [1.0, 0.0, 1.0, 0.0]
        ticket = self.engine.measure(ticket, scores)
        ticket = self.engine.generate_remedies(ticket)
        types = [r.remedy_type for r in ticket.collective_remedies]
        self.assertIn("policy_review", types)

    def test_no_remedy_for_healthy_cohort(self):
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        scores = [0.8, 0.85, 0.82, 0.79]
        ticket = self.engine.measure(ticket, scores)
        ticket = self.engine.generate_remedies(ticket)
        self.assertEqual(len(ticket.collective_remedies), 0)

    def test_tension_acknowledgement_without_scores(self):
        ticket = surface_conflict(
            "Individual privacy vs collective security must be balanced."
        )
        self.assertIsNotNone(ticket)
        ticket = self.engine.generate_remedies(ticket)
        types = [r.remedy_type for r in ticket.collective_remedies]
        self.assertIn("tension_acknowledgement", types)


# ═══════════════════════════════════════════════════
# v2.0 WITNESS CHECKPOINT TESTS
# ═══════════════════════════════════════════════════

class TestWitnessCheckpoint(unittest.TestCase):

    def setUp(self):
        self.engine = ConflictEngine()

    def test_initial_witness_level(self):
        ticket = surface_conflict("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.witness_level, 0)

    def test_process_flags_at_w2(self):
        """Full pipeline should flag at W-2 (FLAGGED)."""
        ticket = self.engine.process("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.witness_level, 2)

    def test_steward_sees_w3(self):
        ticket = self.engine.process("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        ticket = self.engine.steward_sees(ticket)
        self.assertEqual(ticket.witness_level, 3)
        self.assertEqual(ticket.resolution_mode, ResolutionMode.WITNESSED.value)

    def test_witness_only_goes_up(self):
        """W-3 is irreversible — can't go back down."""
        ticket = self.engine.process("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        ticket = self.engine.steward_sees(ticket)  # W-3
        ticket = self.engine.witness(ticket, level=1)  # Try to go back
        self.assertEqual(ticket.witness_level, 3)  # Still W-3

    def test_steward_holds(self):
        ticket = self.engine.process("Each donor in the group gets treatment.")
        self.assertIsNotNone(ticket)
        ticket = self.engine.steward_holds(ticket)
        self.assertEqual(ticket.witness_level, 4)
        self.assertEqual(ticket.resolution_mode, ResolutionMode.HELD.value)
        self.assertIn("HELD", ticket.resolution)


# ═══════════════════════════════════════════════════
# v2.0 FULL PIPELINE TESTS
# ═══════════════════════════════════════════════════

class TestFullPipeline(unittest.TestCase):

    def test_process_without_scores(self):
        engine = ConflictEngine()
        ticket = engine.process("Each donor in the group gets equal treatment.")
        self.assertIsNotNone(ticket)
        self.assertIsNotNone(ticket.weakest_voice)
        self.assertEqual(ticket.witness_level, 2)

    def test_process_with_scores(self):
        engine = ConflictEngine()
        ticket = engine.process(
            "Each donor in the group gets treatment.",
            individual_scores=[0.9, 0.1, 0.8],
        )
        self.assertIsNotNone(ticket)
        self.assertIsNotNone(ticket.collective_measurement)
        self.assertIsNotNone(ticket.weakest_voice)
        self.assertEqual(ticket.weakest_voice.index, 1)

    def test_tickets_tracked(self):
        engine = ConflictEngine()
        engine.process("Each donor in the group gets treatment.")
        engine.process("Individual privacy vs collective security matters.")
        self.assertEqual(engine.tickets_count, 2)

    def test_unwitnessed_tracking(self):
        engine = ConflictEngine()
        t1 = engine.process("Each donor in the group gets treatment.")
        t2 = engine.process("Individual choice vs community benefit here.")
        self.assertEqual(len(engine.unwitnessed_tickets), 2)
        engine.steward_sees(t1)
        self.assertEqual(len(engine.unwitnessed_tickets), 1)

    def test_no_ticket_for_neutral_text(self):
        engine = ConflictEngine()
        ticket = engine.process("Hello, nice weather today.")
        self.assertIsNone(ticket)
        self.assertEqual(engine.tickets_count, 0)


# ═══════════════════════════════════════════════════
# SCENARIO: HIRING ALGORITHM (WALKTHROUGH-001)
# ═══════════════════════════════════════════════════

class TestHiringAlgorithmScenario(unittest.TestCase):
    """
    Hiring algorithm rejects all candidates from zip 60629.
    Each individual passes. The collective is harmed.
    """

    def test_hidden_collective_harm(self):
        engine = ConflictEngine()
        # Individual scores: each candidate looks fine individually
        # But candidates 3,4,5 are from zip 60629 and get 0.0
        scores = [0.9, 0.85, 0.0, 0.0, 0.0, 0.88]
        ticket = engine.process(
            "All candidates evaluated under standard policy for each person.",
            individual_scores=scores,
        )
        self.assertIsNotNone(ticket)
        cm = ticket.collective_measurement
        self.assertTrue(cm.sealed_gate)  # High variance collapses D_collective
        self.assertEqual(cm.weakest_D, 0.0)
        # Weakest voice (candidates from 60629) goes first
        self.assertIsNotNone(ticket.weakest_voice)
        self.assertEqual(ticket.weakest_voice.D_score, 0.0)
        # Remedies include policy review
        types = [r.remedy_type for r in ticket.collective_remedies]
        self.assertIn("policy_review", types)
        self.assertIn("weakest_uplift", types)


# ═══════════════════════════════════════════════════
# SCENARIO: MAJORITY RULE
# ═══════════════════════════════════════════════════

class TestMajorityRuleScenario(unittest.TestCase):
    """
    Majority votes to share everyone's email with the group.
    Minority's choice is overridden.
    """

    def test_majority_overrides_minority(self):
        engine = ConflictEngine()
        ticket = engine.process(
            "The majority decided that all donors share personal data for the collective benefit.",
            individual_scores=[0.9, 0.9, 0.9, 0.2, 0.1],  # Minority harmed
        )
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.weakest_voice.D_score, 0.1)
        # Questions should mention opt-out path
        all_questions = " ".join(ticket.questions)
        has_opt_out = "opt-out" in all_questions.lower() or "opt out" in all_questions.lower()
        has_minority = "minority" in all_questions.lower() or "weakest" in all_questions.lower() or "Member" in all_questions
        self.assertTrue(has_opt_out or has_minority)


# ═══════════════════════════════════════════════════
# SERIALIZATION TESTS
# ═══════════════════════════════════════════════════

class TestSerialization(unittest.TestCase):

    def test_to_dict_with_measurement(self):
        engine = ConflictEngine()
        ticket = engine.process(
            "Each donor in the group gets treatment.",
            individual_scores=[0.8, 0.3, 0.7],
        )
        self.assertIsNotNone(ticket)
        d = ticket.to_dict()
        self.assertIn("collective_D", d)
        self.assertIn("weakest_D", d)
        self.assertIn("resolution_mode", d)

    def test_to_dict_without_measurement(self):
        engine = ConflictEngine()
        ticket = engine.process("Each donor in the group gets equal treatment.")
        self.assertIsNotNone(ticket)
        d = ticket.to_dict()
        self.assertNotIn("collective_D", d)
        self.assertIn("resolution_mode", d)


if __name__ == "__main__":
    unittest.main()
