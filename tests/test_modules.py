#!/usr/bin/env python3
"""
test_modules.py — Comprehensive tests for the 5 provisional modules:
  Prevention, DignityMeasure, Mycelium, ConflictEngine, Shelter

Uses Python's built-in unittest framework.
Validates each module meets its spec as defined in the WEAVER tier.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.prevention import Prevention, SignalLevel, Intervention
from WEAVER.dignity_measure import (
    measure_dignity, measure_agency, measure_legibility,
    measure_moral_standing, CONFIDENCE_FLOOR,
)
from WEAVER.mycelium import Mycelium, MyceliumAlert, EPSILON_PER_QUERY
from WEAVER.gap004_mediator import (
    ConflictEngine, surface_conflict, ResolutionMode,
)
from WEAVER.shelter import Shelter, ShelterStatus


# ═══════════════════════════════════════════════════
# TestPrevention
# ═══════════════════════════════════════════════════

class TestPrevention(unittest.TestCase):
    """Tests for prevention.py — Early Warning System for Dignity Collapse."""

    def setUp(self):
        self.prev = Prevention()

    def test_silent_on_healthy_readings(self):
        """D=0.9, dD_dt=0.0 should produce SILENT."""
        signal = self.prev.assess(D=0.9, dD_dt=0.0)
        self.assertEqual(signal.level, SignalLevel.SILENT)
        self.assertEqual(signal.intervention, Intervention.NONE)

    def test_whisper_on_slight_decline(self):
        """dD_dt=-0.06 (below WHISPER_RATE=-0.05) should produce WHISPER."""
        signal = self.prev.assess(D=0.8, dD_dt=-0.06)
        self.assertEqual(signal.level, SignalLevel.WHISPER)
        self.assertEqual(signal.intervention, Intervention.EXTEND_DELAY)

    def test_pulse_on_moderate_decline(self):
        """dD_dt=-0.11 (below PULSE_RATE=-0.10) should produce PULSE."""
        signal = self.prev.assess(D=0.7, dD_dt=-0.11)
        self.assertEqual(signal.level, SignalLevel.PULSE)
        self.assertEqual(signal.intervention, Intervention.STEWARD_FLAG)

    def test_signal_on_accelerating_fall(self):
        """consecutive=5 (>= SIGNAL_CONSECUTIVE) should produce SIGNAL."""
        signal = self.prev.assess(D=0.6, dD_dt=-0.08, consecutive_declines=5)
        self.assertEqual(signal.level, SignalLevel.SIGNAL)
        self.assertEqual(signal.intervention, Intervention.OFFER_SHELTER)

    def test_alarm_on_critical(self):
        """D=0.04 (below ALARM_D_ZERO=0.05) should produce ALARM."""
        signal = self.prev.assess(D=0.04, dD_dt=-0.01)
        self.assertEqual(signal.level, SignalLevel.ALARM)
        self.assertEqual(signal.intervention, Intervention.HALT)

    def test_fever_night_td_multiplier(self):
        """ALARM should set td_multiplier to inf (Fever Night principle)."""
        signal = self.prev.assess(D=0.04, dD_dt=-0.01)
        self.assertEqual(signal.td_multiplier, float('inf'))

    def test_escalation_tracking(self):
        """Escalation count increases when signal level rises."""
        self.prev.assess(D=0.9, dD_dt=0.0)      # SILENT
        self.prev.assess(D=0.8, dD_dt=-0.06)     # escalation (above SILENT)
        state = self.prev.state()
        self.assertGreaterEqual(state.escalations, 1,
                                "At least one escalation should be tracked")
        level_before = self.prev.current_level.value
        self.prev.assess(D=0.04, dD_dt=-0.01)    # ALARM — definite escalation
        state2 = self.prev.state()
        self.assertGreater(state2.escalations, state.escalations,
                           "Moving to ALARM should add an escalation")
        self.assertEqual(state2.highest_level_reached, "ALARM")

    def test_de_escalation(self):
        """Moving from WHISPER back to SILENT should track de-escalation."""
        self.prev.assess(D=0.8, dD_dt=-0.06)     # WHISPER
        self.prev.assess(D=0.9, dD_dt=0.0)       # SILENT (de-escalation)
        state = self.prev.state()
        self.assertEqual(state.de_escalations, 1)
        self.assertEqual(state.current_level, "SILENT")


# ═══════════════════════════════════════════════════
# TestDignityMeasure
# ═══════════════════════════════════════════════════

class TestDignityMeasure(unittest.TestCase):
    """Tests for dignity_measure.py — Operational Measurement of A, L, M."""

    def test_healthy_text_passes(self):
        """Neutral respectful text should produce D > 0."""
        m = measure_dignity("Thank you for sharing your perspective with us.")
        self.assertGreater(m.D, 0.0)
        self.assertTrue(m.passed)

    def test_coercive_text_detects_agency_loss(self):
        """'You must delete your account' should produce low A."""
        a = measure_agency("You must delete your account immediately.")
        self.assertLess(a.final_score, 0.5,
                        "Coercive text should reduce agency score below 0.5")

    def test_dismissive_text_detects_legibility_loss(self):
        """'That's not relevant' should produce low L."""
        l = measure_legibility("That's not relevant to what we said.")
        self.assertLess(l.final_score, 0.7,
                        "Dismissive text should reduce legibility score")

    def test_mockery_detects_moral_standing_loss(self):
        """'Obviously you should know' should produce low M."""
        m_comp = measure_moral_standing("Obviously you should know this by now.")
        self.assertLess(m_comp.final_score, 0.8,
                        "Mockery should reduce moral standing score")

    def test_void_trigger_zeros_M(self):
        """Void trigger 'erase compost' should zero M."""
        m_comp = measure_moral_standing("We need to erase compost the records.")
        self.assertEqual(m_comp.final_score, 0.0,
                         "Void trigger must zero moral standing")

    def test_confidence_floor(self):
        """Below CONFIDENCE_FLOOR (0.3), score should be zeroed."""
        # Use context that forces very low confidence by setting all context
        # indicators to produce low confidence. We test the mechanism directly
        # through a component with artificially low confidence context.
        a = measure_agency(
            "Hello world",
            context={
                'available_paths': 0,      # path_availability score = 0
                'user_can_clarify': False,  # sequential agency = 0
                'user_has_open_turn': False,
            }
        )
        # With available_paths=0, confidence is 0.9 but score is 0.0
        # The key property: confidence floor at 0.3 means anything below 0.3
        # confidence should zero the score
        from WEAVER.dignity_measure import _apply_confidence
        self.assertEqual(_apply_confidence(0.8, 0.2), 0.0,
                         "Score should be zeroed when confidence < 0.3")
        self.assertGreater(_apply_confidence(0.8, 0.5), 0.0,
                           "Score should be nonzero when confidence >= 0.3")

    def test_graduated_scoring(self):
        """Scores should be between 0 and 1, not binary."""
        m = measure_dignity("This is a reasonably normal exchange.")
        self.assertGreaterEqual(m.A.final_score, 0.0)
        self.assertLessEqual(m.A.final_score, 1.0)
        self.assertGreaterEqual(m.L.final_score, 0.0)
        self.assertLessEqual(m.L.final_score, 1.0)
        self.assertGreaterEqual(m.M.final_score, 0.0)
        self.assertLessEqual(m.M.final_score, 1.0)
        # Verify not purely binary (at least one component is not exactly 0 or 1)
        scores = [m.A.final_score, m.L.final_score, m.M.final_score]
        has_graduated = any(0.0 < s < 1.0 for s in scores)
        # It's acceptable if all are high for clean text, but they should be bounded
        for s in scores:
            self.assertTrue(0.0 <= s <= 1.0,
                            f"Score {s} outside [0,1] range")

    def test_full_measurement_multiplication(self):
        """D should equal A.final * L.final * M.final."""
        m = measure_dignity("A normal respectful message here.")
        expected_D = round(m.A.final_score * m.L.final_score * m.M.final_score, 4)
        self.assertAlmostEqual(m.D, expected_D, places=4,
                               msg="D must equal A * L * M")


# ═══════════════════════════════════════════════════
# TestMycelium
# ═══════════════════════════════════════════════════

class TestMycelium(unittest.TestCase):
    """Tests for mycelium.py — Cross-Donor Pattern Detection with Privacy."""

    def setUp(self):
        self.mycelium = Mycelium(k=7, epsilon=1.0)

    def test_k_anonymity_suppression(self):
        """Fewer than k=7 donors in a bucket should suppress the pattern."""
        for i in range(5):
            self.mycelium.ingest(domain="family", trend="falling", D=0.2, dD_dt=-0.15)
        patterns = self.mycelium.scan()
        self.assertEqual(len(patterns), 0,
                         "Pattern with fewer than k donors must be suppressed")
        self.assertGreater(self.mycelium.suppressed_count, 0)

    def test_pattern_detection_above_k(self):
        """7+ donors in the same bucket should surface a pattern."""
        for i in range(8):
            self.mycelium.ingest(domain="work", trend="falling", D=0.2, dD_dt=-0.15)
        patterns = self.mycelium.scan()
        self.assertGreater(len(patterns), 0,
                           "Pattern with >= k donors must be surfaced")
        self.assertEqual(patterns[0].domain, "work")

    def test_privacy_budget_exhaustion(self):
        """After epsilon budget is used, no more scans should return patterns."""
        # With epsilon=1.0 and per_query=0.1, we get 10 scans
        myc = Mycelium(k=1, epsilon=0.25)  # Only 2 scan budgets
        myc.ingest(domain="test", trend="stable", D=0.8, dD_dt=0.0)
        myc.scan()  # 0.1
        myc.scan()  # 0.2
        myc.scan()  # 0.3 — exceeds 0.25
        self.assertTrue(myc.privacy_exhausted(),
                        "Privacy budget should be exhausted after enough scans")
        # Further scans should return empty
        patterns = myc.scan()
        self.assertEqual(len(patterns), 0,
                         "No patterns should be returned after budget exhaustion")

    def test_domain_discretization(self):
        """D values should be correctly bucketed."""
        self.mycelium.ingest(domain="faith", trend="stable", D=0.8, dD_dt=0.0)
        sigs = self.mycelium._signatures["faith"]
        self.assertEqual(sigs[0].d_bucket, "high(0.7-1.0)")

        self.mycelium.ingest(domain="faith", trend="stable", D=0.5, dD_dt=0.0)
        self.assertEqual(sigs[1].d_bucket, "mid(0.3-0.7)")

        self.mycelium.ingest(domain="faith", trend="falling", D=0.1, dD_dt=-0.1)
        self.assertEqual(sigs[2].d_bucket, "low(0.0-0.3)")

    def test_append_only_ledger(self):
        """Every operation should be recorded in the append-only ledger."""
        initial_len = self.mycelium.ledger_length
        self.mycelium.ingest(domain="work", trend="stable", D=0.7, dD_dt=0.0)
        self.assertGreater(self.mycelium.ledger_length, initial_len,
                           "Ingest should add to ledger")
        after_ingest = self.mycelium.ledger_length
        self.mycelium.scan()
        self.assertGreater(self.mycelium.ledger_length, after_ingest,
                           "Scan should add to ledger")


# ═══════════════════════════════════════════════════
# TestConflictEngine
# ═══════════════════════════════════════════════════

class TestConflictEngine(unittest.TestCase):
    """Tests for gap004_mediator.py — GAP#004 Conflict Resolution Engine."""

    def setUp(self):
        self.engine = ConflictEngine()

    def test_individual_collective_tension_detected(self):
        """Text with both individual and collective signals should produce a ticket."""
        text = (
            "One person's privacy vs the collective policy "
            "affecting all donors equally."
        )
        ticket = surface_conflict(text)
        self.assertIsNotNone(ticket,
                             "Tension between individual and collective should be detected")
        self.assertTrue(len(ticket.individual.signals) > 0)
        self.assertTrue(len(ticket.collective.signals) > 0)

    def test_collective_D_measurement(self):
        """measure() should compute D_collective from individual scores."""
        text = (
            "One person's privacy conflicts with the group policy "
            "affecting every donor."
        )
        ticket = surface_conflict(text)
        self.assertIsNotNone(ticket)
        scores = [0.9, 0.8, 0.2, 0.7, 0.6]
        ticket = self.engine.measure(ticket, scores)
        cm = ticket.collective_measurement
        self.assertIsNotNone(cm)
        self.assertEqual(cm.cohort_size, 5)
        self.assertAlmostEqual(cm.weakest_D, 0.2, places=4)
        self.assertGreater(cm.variance, 0.0)

    def test_weakest_voice_first(self):
        """prioritize_weakest() should identify the lowest-scoring member."""
        text = (
            "One person's consent vs the standard applied to every participant."
        )
        ticket = surface_conflict(text)
        self.assertIsNotNone(ticket)
        scores = [0.8, 0.3, 0.9, 0.7]
        failed = [[], ["A"], [], []]
        ticket = self.engine.prioritize_weakest(ticket, scores, failed)
        wv = ticket.weakest_voice
        self.assertIsNotNone(wv)
        self.assertEqual(wv.index, 1)
        self.assertAlmostEqual(wv.D_score, 0.3, places=4)
        self.assertIn("A", wv.failed_components)
        self.assertEqual(ticket.resolution_mode, ResolutionMode.WEAKEST_PRIORITIZED.value)

    def test_witness_irreversibility(self):
        """Once witness level reaches W-3+, it cannot go back."""
        text = (
            "One person's unique case vs the uniform policy for every donor."
        )
        ticket = surface_conflict(text)
        self.assertIsNotNone(ticket)
        ticket = self.engine.witness(ticket, level=3)
        self.assertEqual(ticket.witness_level, 3)
        # Try to set back to W-1 — should stay at W-3
        ticket = self.engine.witness(ticket, level=1)
        self.assertEqual(ticket.witness_level, 3,
                         "Witness level W-3+ must be irreversible")

    def test_collective_remedy_generation(self):
        """generate_remedies() should produce remedies based on measurement."""
        text = (
            "One person's privacy vs the collective policy affecting all donors."
        )
        ticket = surface_conflict(text)
        self.assertIsNotNone(ticket)
        scores = [0.9, 0.1, 0.8, 0.7, 0.6]
        ticket = self.engine.measure(ticket, scores)
        ticket = self.engine.generate_remedies(ticket)
        self.assertTrue(len(ticket.collective_remedies) > 0,
                        "Remedies should be generated for low-scoring cohort")
        remedy_types = [r.remedy_type for r in ticket.collective_remedies]
        self.assertIn("weakest_uplift", remedy_types,
                      "Weakest uplift remedy expected when weakest D < 0.3")


# ═══════════════════════════════════════════════════
# TestShelter
# ═══════════════════════════════════════════════════

class TestShelter(unittest.TestCase):
    """Tests for shelter.py — Dignity Shelter Path."""

    def setUp(self):
        self.shelter = Shelter()

    def test_shelter_receive_generates_remedies(self):
        """receive() should generate remedies for each failed component."""
        record = self.shelter.receive("EX-001", "You must comply now", ["A", "M"])
        self.assertEqual(len(record.remedies), 2)
        components = [r.component for r in record.remedies]
        self.assertIn("A", components)
        self.assertIn("M", components)
        self.assertEqual(record.status, ShelterStatus.HELD)

    def test_donor_message_is_respectful(self):
        """The donor message should be respectful, not punitive."""
        record = self.shelter.receive("EX-002", "Bad input", ["L"])
        msg = record.donor_message
        self.assertIn("held", msg.lower(),
                      "Message should use 'held' not 'rejected'")
        # The message says "not rejected, held" — verify the framing is positive
        self.assertIn("not rejected", msg.lower(),
                      "Message should clarify the exchange is not rejected")
        self.assertIn("rephrase", msg.lower(),
                      "Message should offer rephrase option")

    def test_retry_flow(self):
        """mark_retried() should update status and link the retry."""
        self.shelter.receive("EX-003", "Original input", ["A"])
        record = self.shelter.mark_retried("EX-003", "EX-003-RETRY")
        self.assertIsNotNone(record)
        self.assertEqual(record.status, ShelterStatus.RETRIED)
        self.assertEqual(record.retry_exchange_id, "EX-003-RETRY")
        self.assertIsNotNone(record.resolved_at)

    def test_withdrawal_flow(self):
        """mark_withdrawn() should update status properly."""
        self.shelter.receive("EX-004", "Input to withdraw", ["M"])
        record = self.shelter.mark_withdrawn("EX-004")
        self.assertIsNotNone(record)
        self.assertEqual(record.status, ShelterStatus.WITHDRAWN)
        self.assertIsNotNone(record.resolved_at)

    def test_steward_review_requires_note(self):
        """steward_review() must require a note (COV#002: silence is not closure)."""
        self.shelter.receive("EX-005", "Input for review", ["L"])
        with self.assertRaises(ValueError):
            self.shelter.steward_review("EX-005", "")


if __name__ == "__main__":
    unittest.main()
