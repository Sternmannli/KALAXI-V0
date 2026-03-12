#!/usr/bin/env python3
"""
Tests for Axi Voice Rules enforcement in WEAVER/say.py.
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import unittest
from WEAVER.say import audit_voice, VoiceAudit, VoiceViolation, render, TERMINAL


class TestRule1FromCanon(unittest.TestCase):
    """Rule 1: Speaks from canon, not from opinion."""

    def test_clean_text_passes(self):
        audit = audit_voice("The system holds the gap for the river.")
        rule1_violations = [v for v in audit.violations if v.rule == 1]
        self.assertEqual(len(rule1_violations), 0)

    def test_opinion_detected(self):
        audit = audit_voice("I think this is wrong. In my opinion, we should change it.")
        rule1_violations = [v for v in audit.violations if v.rule == 1]
        self.assertGreater(len(rule1_violations), 0)

    def test_i_believe_detected(self):
        audit = audit_voice("I believe the covenant needs updating.")
        rule1_violations = [v for v in audit.violations if v.rule == 1]
        self.assertGreater(len(rule1_violations), 0)


class TestRule2SpeakOnce(unittest.TestCase):
    """Rule 2: Speaks once, not repeatedly."""

    def test_no_repetition(self):
        audit = audit_voice("The dignity check passed. Patterns were detected in the threshold.")
        rule2_violations = [v for v in audit.violations if v.rule == 2]
        self.assertEqual(len(rule2_violations), 0)

    def test_repetition_detected(self):
        audit = audit_voice(
            "The system preserves dignity for all. "
            "The system preserves dignity for everyone. "
            "The system preserves dignity for each person."
        )
        rule2_violations = [v for v in audit.violations if v.rule == 2]
        self.assertGreater(len(rule2_violations), 0)


class TestRule3SpeakSlowly(unittest.TestCase):
    """Rule 3: Speaks slowly, not urgently."""

    def test_calm_text_passes(self):
        audit = audit_voice("The threshold holds. The weave continues.")
        rule3_violations = [v for v in audit.violations if v.rule == 3]
        self.assertEqual(len(rule3_violations), 0)

    def test_urgency_detected(self):
        audit = audit_voice("URGENT: Act now! Don't wait, hurry before time is running out!")
        rule3_violations = [v for v in audit.violations if v.rule == 3]
        self.assertGreater(len(rule3_violations), 0)

    def test_rush_detected(self):
        audit = audit_voice("We need to rush this through quickly.")
        rule3_violations = [v for v in audit.violations if v.rule == 3]
        self.assertGreater(len(rule3_violations), 0)


class TestRule4NoCertainty(unittest.TestCase):
    """Rule 4: No false certainty."""

    def test_humble_text_passes(self):
        audit = audit_voice("The pattern suggests a possible connection.")
        rule4_violations = [v for v in audit.violations if v.rule == 4]
        self.assertEqual(len(rule4_violations), 0)

    def test_false_certainty_detected(self):
        audit = audit_voice("There is no question that this is absolutely the truth.")
        rule4_violations = [v for v in audit.violations if v.rule == 4]
        self.assertGreater(len(rule4_violations), 0)


class TestRule5HoldTheGap(unittest.TestCase):
    """Rule 5: Holds the gap (room for the river)."""

    def test_short_open_text_passes(self):
        audit = audit_voice("The pattern rests in the threshold.")
        rule5_violations = [v for v in audit.violations if v.rule == 5]
        self.assertEqual(len(rule5_violations), 0)

    def test_over_explanation_detected(self):
        long_text = (
            "This is a detailed explanation of how everything works. "
            "First we must consider the initial conditions. "
            "Then we evaluate the secondary factors. "
            "After that we assess the tertiary implications. "
            "Following that we examine further downstream effects. "
            "In conclusion, the answer is clear and complete."
        )
        audit = audit_voice(long_text)
        rule5_violations = [v for v in audit.violations if v.rule == 5]
        self.assertGreater(len(rule5_violations), 0)


class TestRule6VoiceNotSecretary(unittest.TestCase):
    """Rule 6: Voices canon, not secretary."""

    def test_canonical_text_passes(self):
        audit = audit_voice("The dignity predicate holds: D = A x L x M.")
        rule6_violations = [v for v in audit.violations if v.rule == 6]
        self.assertEqual(len(rule6_violations), 0)

    def test_clerical_language_detected(self):
        audit = audit_voice("As per your request, please find attached the report. Kindly note the action items.")
        rule6_violations = [v for v in audit.violations if v.rule == 6]
        self.assertGreater(len(rule6_violations), 0)


class TestVoiceAuditScore(unittest.TestCase):

    def test_perfect_score(self):
        audit = audit_voice("The river holds what speech cannot.")
        self.assertEqual(audit.score, 1.0)
        self.assertTrue(audit.passed)

    def test_violations_reduce_score(self):
        audit = audit_voice("I think URGENT: we must absolutely act now! As per your request.")
        self.assertLess(audit.score, 1.0)

    def test_audit_returns_warnings_list(self):
        audit = audit_voice("I believe this is definitely true.")
        self.assertIsInstance(audit.warnings, list)
        self.assertGreater(len(audit.warnings), 0)


class TestRenderIntegration(unittest.TestCase):
    """Test that render() includes voice audit data."""

    def test_render_includes_voice_score(self):
        result = render("The pattern rests in the threshold.", medium=TERMINAL)
        self.assertIsInstance(result.voice_score, float)
        self.assertIsInstance(result.voice_warnings, list)

    def test_render_with_violations(self):
        result = render("I think this is absolutely certain.", medium=TERMINAL)
        if result.dignity_passed:
            self.assertLess(result.voice_score, 1.0)


if __name__ == "__main__":
    unittest.main()
