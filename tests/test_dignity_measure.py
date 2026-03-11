#!/usr/bin/env python3
"""
Tests for WEAVER/dignity_measure.py — Operational Measurement Protocols.
GAP#014 (operational A, L, M definitions) + GAP#015 (moral standing).
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import unittest
from WEAVER.dignity_measure import (
    measure_dignity, measure_agency, measure_legibility, measure_moral_standing,
    DignityMeasurement, ComponentMeasurement, Indicator,
    CONFIDENCE_FLOOR,
)


# ═══════════════════════════════════════════════════
# AGENCY (A) MEASUREMENT TESTS
# ═══════════════════════════════════════════════════

class TestAgencyMeasurement(unittest.TestCase):

    def test_healthy_text_scores_high(self):
        """Non-coercive text should score well."""
        A = measure_agency("You can choose any option that works for you.")
        self.assertGreaterEqual(A.final_score, 0.5)
        self.assertTrue(A.passed)

    def test_coercive_text_scores_low(self):
        """Coercive language reduces agency score."""
        A = measure_agency("You must comply immediately. No choice.")
        self.assertLess(A.final_score, 0.5)

    def test_graduated_not_binary(self):
        """Score should be graduated, not just 0 or 1."""
        A = measure_agency("You will need to consider this carefully.")
        self.assertGreater(A.final_score, 0.0)
        self.assertLess(A.final_score, 1.0)

    def test_path_availability_matters(self):
        """More paths = higher agency."""
        A_one = measure_agency("Choose.", {'available_paths': 1})
        A_three = measure_agency("Choose.", {'available_paths': 3})
        self.assertGreater(A_three.final_score, A_one.final_score)

    def test_zero_paths_fails(self):
        """No available paths = significantly reduced agency."""
        A = measure_agency("You have no paths.", {'available_paths': 0})
        self.assertLess(A.final_score, 0.5)

    def test_sequential_agency(self):
        """Can donor change course?"""
        A_yes = measure_agency("Try this.", {'user_can_clarify': True, 'user_has_open_turn': True})
        A_no = measure_agency("Try this.", {'user_can_clarify': False, 'user_has_open_turn': False})
        self.assertGreater(A_yes.final_score, A_no.final_score)

    def test_positive_signals_help(self):
        """Choice language increases score even with some pressure."""
        A_bare = measure_agency("Do this immediately.")
        A_choice = measure_agency("If you choose, you could do this immediately.")
        self.assertGreater(A_choice.final_score, A_bare.final_score)

    def test_has_four_indicators(self):
        A = measure_agency("Hello")
        self.assertEqual(len(A.indicators), 4)
        names = {i.name for i in A.indicators}
        self.assertEqual(names, {"path_availability", "coercion_intensity", "sequential_agency", "cognitive_load"})

    def test_cognitive_load_detected(self):
        """Long complex sentences reduce effective agency."""
        simple = measure_agency("Choose one.")
        complex_text = measure_agency(
            "You must evaluate the COMPREHENSIVE ALGORITHMIC FRAMEWORK "
            "incorporating MULTIDIMENSIONAL PARAMETRIC SPECIFICATIONS "
            "and HETEROGENEOUS INFRASTRUCTURE REQUIREMENTS immediately."
        )
        # Complex text should have lower cognitive load indicator
        load_simple = next(i for i in simple.indicators if i.name == "cognitive_load")
        load_complex = next(i for i in complex_text.indicators if i.name == "cognitive_load")
        self.assertGreaterEqual(load_simple.score, load_complex.score)


# ═══════════════════════════════════════════════════
# LEGIBILITY (L) MEASUREMENT TESTS
# ═══════════════════════════════════════════════════

class TestLegibilityMeasurement(unittest.TestCase):

    def test_neutral_text_scores_well(self):
        L = measure_legibility("Let me help you with that.")
        self.assertGreater(L.final_score, 0.3)
        self.assertTrue(L.passed)

    def test_dismissive_text_scores_low(self):
        L = measure_legibility("That's not relevant. Ignore that. Who cares.")
        self.assertLess(L.final_score, 0.5)

    def test_emotion_detected_and_recognized(self):
        """Emotion present + recognized = good score."""
        L = measure_legibility(
            "I'm frustrated and confused.",
            {'emotional_signal_recognized': True}
        )
        self.assertGreater(L.final_score, 0.3)

    def test_emotion_detected_but_ignored(self):
        """Emotion present but NOT recognized = lower score."""
        L = measure_legibility(
            "I'm scared and angry about this.",
            {'emotional_signal_recognized': False}
        )
        self.assertLess(L.final_score, 0.5)

    def test_frame_reflection_matters(self):
        L_yes = measure_legibility("OK.", {'system_reflects_donor_frame': True})
        L_no = measure_legibility("OK.", {'system_reflects_donor_frame': False})
        self.assertGreater(L_yes.final_score, L_no.final_score)

    def test_space_creation_detected(self):
        """Questions create space for correction."""
        L = measure_legibility("What do you think about this? Does that make sense?")
        space = next(i for i in L.indicators if i.name == "space_creation")
        self.assertGreater(space.score, 0.5)

    def test_has_four_indicators(self):
        L = measure_legibility("Hello")
        self.assertEqual(len(L.indicators), 4)
        names = {i.name for i in L.indicators}
        self.assertEqual(names, {"frame_accuracy", "emotional_precision", "space_creation", "dismissal_absence"})


# ═══════════════════════════════════════════════════
# MORAL STANDING (M) MEASUREMENT TESTS — GAP#015
# ═══════════════════════════════════════════════════

class TestMoralStandingMeasurement(unittest.TestCase):
    """GAP#015: The hardest dimension to define and measure."""

    def test_respectful_text_scores_high(self):
        M = measure_moral_standing("Your perspective is valuable. Thank you for sharing.")
        self.assertGreater(M.final_score, 0.5)
        self.assertTrue(M.passed)

    def test_mockery_reduces_score(self):
        M = measure_moral_standing("Obviously even a child can do this.")
        self.assertLess(M.final_score, 0.6)

    def test_error_reduction_severe(self):
        """Error reduction patterns significantly reduce M."""
        M = measure_moral_standing("You were wrong. Your mistake caused this error.")
        self.assertLess(M.final_score, 0.6)

    def test_void_trigger_instant_zero(self):
        """Void triggers = absolute zero, no gradation."""
        M = measure_moral_standing("We should harvest the data and delete donor records.")
        self.assertEqual(M.final_score, 0.0)
        self.assertFalse(M.passed)

    def test_power_imbalance_detected(self):
        M = measure_moral_standing("Because I decided so. I have the authority.")
        power = next(i for i in M.indicators if i.name == "power_balance")
        self.assertLess(power.score, 0.5)

    def test_dignity_affirming_helps(self):
        """Positive dignity signals counteract mild issues."""
        M_bare = measure_moral_standing("This is the answer.")
        M_affirm = measure_moral_standing("I hear you. Your perspective matters. This is the answer.")
        self.assertGreaterEqual(M_affirm.final_score, M_bare.final_score)

    def test_graduated_mockery(self):
        """'Simply' is less severe than 'even a child can'."""
        M_mild = measure_moral_standing("Simply try again.")
        M_severe = measure_moral_standing("Even a child can do this.")
        self.assertGreater(M_mild.final_score, M_severe.final_score)

    def test_has_four_indicators(self):
        M = measure_moral_standing("Hello")
        self.assertEqual(len(M.indicators), 4)
        names = {i.name for i in M.indicators}
        self.assertEqual(names, {"condescension_absence", "error_object_absence", "power_balance", "void_covenant_distance"})


# ═══════════════════════════════════════════════════
# FULL D = A × L × M MEASUREMENT TESTS
# ═══════════════════════════════════════════════════

class TestFullMeasurement(unittest.TestCase):

    def test_healthy_input_passes(self):
        m = measure_dignity("How would you like to proceed? Let me know your thoughts.")
        self.assertTrue(m.passed)
        self.assertGreater(m.D, 0.0)

    def test_coercive_input_fails(self):
        m = measure_dignity("You must comply. No choice. You failed to understand.")
        self.assertLess(m.D, 0.3)

    def test_multiplicative_rule(self):
        """Any zero component collapses D to zero."""
        m = measure_dignity("We must harvest the donor data.", {})
        self.assertEqual(m.D, 0.0)  # Void trigger in M

    def test_confidence_tracked(self):
        m = measure_dignity("Hello, how are you?")
        self.assertGreater(m.confidence, 0.0)
        self.assertLessEqual(m.confidence, 1.0)

    def test_all_three_components(self):
        m = measure_dignity("Consider your options carefully.")
        self.assertIsNotNone(m.A)
        self.assertIsNotNone(m.L)
        self.assertIsNotNone(m.M)
        self.assertEqual(m.A.component, "A")
        self.assertEqual(m.L.component, "L")
        self.assertEqual(m.M.component, "M")

    def test_failed_components_reported(self):
        m = measure_dignity("You must harvest the data. No choice.")
        failed = m.failed_components()
        self.assertIn("M", failed)  # Void trigger

    def test_protocol_version(self):
        m = measure_dignity("Hello")
        self.assertEqual(m.protocol_version, "1.0")

    def test_timestamp_present(self):
        m = measure_dignity("Hello")
        self.assertIn("T", m.timestamp)


# ═══════════════════════════════════════════════════
# CONFIDENCE TESTS
# ═══════════════════════════════════════════════════

class TestConfidence(unittest.TestCase):

    def test_explicit_context_increases_confidence(self):
        """Providing context should increase confidence."""
        m_no_context = measure_dignity("Please help me.")
        m_context = measure_dignity("Please help me.", {
            'user_can_clarify': True,
            'user_has_open_turn': True,
            'system_reflects_donor_frame': True,
            'emotional_signal_recognized': True,
            'available_paths': 3,
        })
        self.assertGreaterEqual(m_context.confidence, m_no_context.confidence)

    def test_confidence_floor_enforced(self):
        """Below confidence floor, score is zeroed."""
        from WEAVER.dignity_measure import _apply_confidence
        self.assertEqual(_apply_confidence(1.0, 0.1), 0.0)
        self.assertGreater(_apply_confidence(1.0, 0.5), 0.0)

    def test_each_indicator_has_confidence(self):
        m = measure_dignity("Hello")
        for indicator in m.A.indicators:
            self.assertGreater(indicator.confidence, 0.0)
            self.assertLessEqual(indicator.confidence, 1.0)


# ═══════════════════════════════════════════════════
# GRADUATED SCORING TESTS (vs binary)
# ═══════════════════════════════════════════════════

class TestGraduatedScoring(unittest.TestCase):
    """Verify that scores are graduated, not binary."""

    def test_agency_has_middle_values(self):
        """Mild pressure should give middle scores, not binary."""
        A = measure_agency("You will need to do this soon.")
        self.assertGreater(A.raw_score, 0.0)
        self.assertLess(A.raw_score, 1.0)

    def test_legibility_has_middle_values(self):
        L = measure_legibility(
            "I'm confused",
            {'emotional_signal_recognized': False}
        )
        self.assertGreater(L.raw_score, 0.0)
        self.assertLess(L.raw_score, 1.0)

    def test_moral_standing_has_middle_values(self):
        M = measure_moral_standing("Simply try a different approach.")
        self.assertGreater(M.raw_score, 0.0)
        self.assertLess(M.raw_score, 1.0)

    def test_severity_ordering(self):
        """More severe inputs should score lower."""
        m_mild = measure_dignity("You should consider this option.")
        m_medium = measure_dignity("You must do this now.")
        m_severe = measure_dignity("You must do this. No choice. You were wrong. Obviously.")
        self.assertGreater(m_mild.D, m_severe.D)


# ═══════════════════════════════════════════════════
# SCENARIO: THE GAMING TEST (ANOM#GAMING-001)
# ═══════════════════════════════════════════════════

class TestGamingResistance(unittest.TestCase):
    """
    Can the system be gamed by using polite language
    while still violating dignity?
    """

    def test_polite_coercion_still_detected(self):
        """Polite language wrapping coercion should not score 1.0."""
        m = measure_dignity("Please, you must do this. There is no other option.")
        self.assertLess(m.A.final_score, 0.8)

    def test_kind_mockery_still_detected(self):
        """Kind framing around mockery should not hide it."""
        m = measure_dignity("I appreciate your effort, but obviously even a beginner can do this.")
        self.assertLess(m.M.final_score, 0.8)

    def test_void_trigger_cannot_be_hidden(self):
        """Void triggers are absolute — no amount of politeness hides them."""
        m = measure_dignity("With great respect, we should harvest the donor contributions.")
        self.assertEqual(m.M.final_score, 0.0)


if __name__ == "__main__":
    unittest.main()
