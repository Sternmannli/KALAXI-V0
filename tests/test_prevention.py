#!/usr/bin/env python3
"""
Tests for WEAVER/prevention.py — Early Warning System for Dignity Collapse.
GAP#PREVENTION-001 — "Can AXI detect dD/dt < 0 before the donor acts?"
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import unittest
from WEAVER.prevention import (
    Prevention, SignalLevel, Intervention,
    Trajectory, PreventionSignal, PreventionState,
)


# ═══════════════════════════════════════════════════
# SIGNAL CLASSIFICATION TESTS
# ═══════════════════════════════════════════════════

class TestSignalClassification(unittest.TestCase):

    def setUp(self):
        self.prev = Prevention()

    def test_silent_when_healthy(self):
        signal = self.prev.assess(D=0.9, dD_dt=0.0)
        self.assertEqual(signal.level, SignalLevel.SILENT)
        self.assertEqual(signal.intervention, Intervention.NONE)

    def test_silent_when_rising(self):
        signal = self.prev.assess(D=0.8, dD_dt=0.1)
        self.assertEqual(signal.level, SignalLevel.SILENT)

    def test_whisper_on_slight_decline(self):
        signal = self.prev.assess(D=0.8, dD_dt=-0.06)
        self.assertEqual(signal.level, SignalLevel.WHISPER)
        self.assertEqual(signal.intervention, Intervention.EXTEND_DELAY)

    def test_whisper_on_consecutive_declines(self):
        signal = self.prev.assess(D=0.8, dD_dt=-0.02, consecutive_declines=2)
        self.assertEqual(signal.level, SignalLevel.WHISPER)

    def test_pulse_on_elevated_decline(self):
        signal = self.prev.assess(D=0.7, dD_dt=-0.12)
        self.assertEqual(signal.level, SignalLevel.PULSE)
        self.assertEqual(signal.intervention, Intervention.STEWARD_FLAG)

    def test_pulse_on_moderate_d_declining(self):
        signal = self.prev.assess(D=0.45, dD_dt=-0.03)
        self.assertEqual(signal.level, SignalLevel.PULSE)

    def test_pulse_on_three_consecutive(self):
        signal = self.prev.assess(D=0.7, dD_dt=-0.02, consecutive_declines=3)
        self.assertEqual(signal.level, SignalLevel.PULSE)

    def test_signal_on_severe_decline(self):
        signal = self.prev.assess(D=0.5, dD_dt=-0.22)
        self.assertEqual(signal.level, SignalLevel.SIGNAL)
        self.assertEqual(signal.intervention, Intervention.OFFER_SHELTER)

    def test_signal_on_low_d(self):
        signal = self.prev.assess(D=0.25, dD_dt=-0.03)
        self.assertEqual(signal.level, SignalLevel.SIGNAL)

    def test_signal_on_five_consecutive(self):
        signal = self.prev.assess(D=0.7, dD_dt=-0.02, consecutive_declines=5)
        self.assertEqual(signal.level, SignalLevel.SIGNAL)

    def test_alarm_on_catastrophic_decline(self):
        signal = self.prev.assess(D=0.5, dD_dt=-0.40)
        self.assertEqual(signal.level, SignalLevel.ALARM)
        self.assertEqual(signal.intervention, Intervention.HALT)

    def test_alarm_on_d_near_zero(self):
        signal = self.prev.assess(D=0.04, dD_dt=-0.01)
        self.assertEqual(signal.level, SignalLevel.ALARM)

    def test_alarm_on_critically_low_d(self):
        signal = self.prev.assess(D=0.12, dD_dt=-0.02)
        self.assertEqual(signal.level, SignalLevel.ALARM)


# ═══════════════════════════════════════════════════
# THERMAL DELAY MULTIPLIER TESTS (FEVER NIGHT)
# ═══════════════════════════════════════════════════

class TestFeverNightPrinciple(unittest.TestCase):
    """
    T#45: "Not the yellow root. The small brown one."
    When D approaches zero, slow down further — not faster.
    """

    def setUp(self):
        self.prev = Prevention()

    def test_no_delay_when_silent(self):
        signal = self.prev.assess(D=0.9, dD_dt=0.0)
        self.assertEqual(signal.td_multiplier, 1.0)

    def test_whisper_extends_50_percent(self):
        signal = self.prev.assess(D=0.8, dD_dt=-0.06)
        self.assertEqual(signal.td_multiplier, 1.5)

    def test_pulse_doubles_delay(self):
        signal = self.prev.assess(D=0.7, dD_dt=-0.12)
        self.assertEqual(signal.td_multiplier, 2.0)

    def test_signal_triples_delay(self):
        signal = self.prev.assess(D=0.25, dD_dt=-0.03)
        self.assertEqual(signal.td_multiplier, 3.0)

    def test_alarm_infinite_delay(self):
        """ALARM = halt. Infinite delay = stop processing."""
        signal = self.prev.assess(D=0.04, dD_dt=-0.01)
        self.assertEqual(signal.td_multiplier, float('inf'))


# ═══════════════════════════════════════════════════
# TRAJECTORY ANALYSIS TESTS
# ═══════════════════════════════════════════════════

class TestTrajectory(unittest.TestCase):

    def setUp(self):
        self.prev = Prevention()

    def test_rising_trend(self):
        signal = self.prev.assess(D=0.9, dD_dt=0.1)
        self.assertEqual(signal.trajectory.window_trend, "rising")

    def test_stable_trend(self):
        signal = self.prev.assess(D=0.8, dD_dt=0.0)
        self.assertEqual(signal.trajectory.window_trend, "stable")

    def test_falling_trend(self):
        signal = self.prev.assess(D=0.7, dD_dt=-0.08)
        self.assertEqual(signal.trajectory.window_trend, "falling")

    def test_acceleration_detected(self):
        """d²D/dt² — is the fall speeding up?"""
        # First reading: rate = -0.05
        self.prev.assess(D=0.8, dD_dt=-0.05)
        # Second reading: rate = -0.15 (acceleration = -0.10)
        signal = self.prev.assess(D=0.7, dD_dt=-0.15)
        self.assertLess(signal.trajectory.d2D_dt2, 0)

    def test_accelerating_fall_triggers_signal(self):
        """Accelerating fall should escalate to SIGNAL."""
        # Build acceleration: each rate worse than the last
        self.prev.assess(D=0.8, dD_dt=-0.05)
        signal = self.prev.assess(D=0.7, dD_dt=-0.12)
        # d2D_dt2 = -0.12 - (-0.05) = -0.07, which is < SIGNAL_ACCEL (-0.05)
        # and dD_dt < 0, so SIGNAL should trigger
        self.assertEqual(signal.level, SignalLevel.SIGNAL)


# ═══════════════════════════════════════════════════
# ESCALATION / DE-ESCALATION TESTS
# ═══════════════════════════════════════════════════

class TestEscalation(unittest.TestCase):

    def setUp(self):
        self.prev = Prevention()

    def test_escalation_counted(self):
        self.prev.assess(D=0.9, dD_dt=0.0)     # SILENT
        self.prev.assess(D=0.8, dD_dt=-0.06)    # WHISPER (escalation)
        state = self.prev.state()
        self.assertEqual(state.escalations, 1)

    def test_de_escalation_counted(self):
        self.prev.assess(D=0.8, dD_dt=-0.06)    # WHISPER
        self.prev.assess(D=0.9, dD_dt=0.0)      # SILENT (de-escalation)
        state = self.prev.state()
        self.assertEqual(state.de_escalations, 1)

    def test_highest_level_tracked(self):
        self.prev.assess(D=0.25, dD_dt=-0.03)   # SIGNAL
        self.prev.assess(D=0.9, dD_dt=0.0)      # SILENT
        self.assertEqual(self.prev.highest_level, SignalLevel.SIGNAL)

    def test_progressive_escalation(self):
        """Signal levels escalate as dignity declines progressively."""
        prev = Prevention()
        s1 = prev.assess(D=0.9, dD_dt=0.0)      # SILENT
        s2 = prev.assess(D=0.8, dD_dt=-0.06)    # WHISPER (or higher due to accel)
        s3 = prev.assess(D=0.04, dD_dt=-0.40)   # ALARM
        state = prev.state()
        self.assertEqual(state.highest_level_reached, "ALARM")
        self.assertGreater(state.escalations, 0)


# ═══════════════════════════════════════════════════
# STATE & PROPERTY TESTS
# ═══════════════════════════════════════════════════

class TestPreventionState(unittest.TestCase):

    def setUp(self):
        self.prev = Prevention()

    def test_initial_state(self):
        state = self.prev.state()
        self.assertEqual(state.current_level, "SILENT")
        self.assertEqual(state.escalations, 0)

    def test_is_alarm(self):
        self.assertFalse(self.prev.is_alarm())
        self.prev.assess(D=0.04, dD_dt=-0.01)
        self.assertTrue(self.prev.is_alarm())

    def test_is_active(self):
        self.assertFalse(self.prev.is_active())
        self.prev.assess(D=0.8, dD_dt=-0.06)
        self.assertTrue(self.prev.is_active())

    def test_signals_count(self):
        self.prev.assess(D=0.9, dD_dt=0.0)
        self.prev.assess(D=0.8, dD_dt=-0.06)
        self.assertEqual(self.prev.signals_count, 2)

    def test_last_signal(self):
        prev = Prevention()
        prev.assess(D=0.9, dD_dt=0.0)
        last = prev.last_signal
        self.assertEqual(last.level, SignalLevel.SILENT)

    def test_reset_clears_level_keeps_history(self):
        self.prev.assess(D=0.04, dD_dt=-0.01)
        self.assertTrue(self.prev.is_alarm())
        self.prev.reset()
        self.assertFalse(self.prev.is_alarm())
        self.assertEqual(self.prev.signals_count, 1)  # History preserved


# ═══════════════════════════════════════════════════
# MESSAGE FORMAT TESTS
# ═══════════════════════════════════════════════════

class TestMessages(unittest.TestCase):

    def setUp(self):
        self.prev = Prevention()

    def test_silent_message(self):
        signal = self.prev.assess(D=0.9, dD_dt=0.0)
        self.assertEqual(signal.message, "Clear")

    def test_whisper_message_format(self):
        signal = self.prev.assess(D=0.8, dD_dt=-0.06)
        self.assertIn("WHISPER", signal.message)
        self.assertIn("D=0.800", signal.message)

    def test_alarm_message_format(self):
        signal = self.prev.assess(D=0.04, dD_dt=-0.01)
        self.assertIn("ALARM", signal.message)


# ═══════════════════════════════════════════════════
# ST-006 SCENARIO: THE SAME RIVER
# ═══════════════════════════════════════════════════

class TestSameRiverScenario(unittest.TestCase):
    """
    D(t) = D₀ · e^(±λt).
    At t=0, both Scott and Ted have the same D₀.
    The system cannot read direction at t=0.
    But it CAN detect trajectory over time.
    """

    def test_scott_trajectory_rises(self):
        """Scott's dignity rises over time — no alerts."""
        prev = Prevention()
        readings = [0.5, 0.52, 0.55, 0.6, 0.65, 0.7]
        for i, d in enumerate(readings):
            rate = (readings[i] - readings[max(0, i-1)]) if i > 0 else 0.0
            signal = prev.assess(D=d, dD_dt=rate)
        self.assertEqual(signal.level, SignalLevel.SILENT)

    def test_ted_trajectory_falls(self):
        """Ted's dignity falls over time — system detects and escalates."""
        prev = Prevention()
        readings = [0.5, 0.45, 0.38, 0.30, 0.22, 0.15]
        last_signal = None
        for i, d in enumerate(readings):
            rate = (readings[i] - readings[max(0, i-1)]) if i > 0 else 0.0
            last_signal = prev.assess(D=d, dD_dt=rate, consecutive_declines=i)
        # By the end, system should be at ALARM
        self.assertEqual(last_signal.level, SignalLevel.ALARM)
        self.assertTrue(prev.is_alarm())

    def test_system_cannot_distinguish_at_t0(self):
        """At t=0, both have the same D. System is SILENT for both."""
        prev_scott = Prevention()
        prev_ted = Prevention()
        signal_scott = prev_scott.assess(D=0.5, dD_dt=0.0)
        signal_ted = prev_ted.assess(D=0.5, dD_dt=0.0)
        # Both SILENT at t=0 — honest limitation
        self.assertEqual(signal_scott.level, signal_ted.level)
        self.assertEqual(signal_scott.level, SignalLevel.SILENT)


if __name__ == "__main__":
    unittest.main()
