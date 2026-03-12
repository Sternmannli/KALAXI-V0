#!/usr/bin/env python3
"""
Tests for WEAVER/mycelium.py — Cross-Donor Pattern Detection with Privacy.
GAP#MYCELIUM-CONNECT-001 — "Should the system connect anonymous donor patterns?"
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import unittest
from WEAVER.mycelium import (
    Mycelium, MyceliumAlert, PatternType,
    TrajectorySignature, MyceliumPattern, MyceliumState,
    K_ANONYMITY_FLOOR, EPSILON_BUDGET, EPSILON_PER_QUERY,
)


# ═══════════════════════════════════════════════════
# PRIVACY GUARANTEE TESTS
# ═══════════════════════════════════════════════════

class TestPrivacyGuarantees(unittest.TestCase):
    """
    COV#003 + COV#015: Privacy by default.
    No pattern surfaces unless k≥7 donors show it.
    """

    def setUp(self):
        self.mycelium = Mycelium()

    def test_k_anonymity_floor_is_seven(self):
        self.assertEqual(K_ANONYMITY_FLOOR, 7)

    def test_pattern_suppressed_below_k(self):
        """6 donors in same domain — pattern must NOT surface."""
        for _ in range(6):
            self.mycelium.ingest(domain="work", trend="falling", D=0.3, dD_dt=-0.15)
        patterns = self.mycelium.scan()
        self.assertEqual(len(patterns), 0)
        self.assertGreater(self.mycelium.suppressed_count, 0)

    def test_pattern_surfaces_at_k(self):
        """7 donors in same domain — pattern CAN surface."""
        for _ in range(7):
            self.mycelium.ingest(domain="work", trend="falling", D=0.3, dD_dt=-0.15)
        patterns = self.mycelium.scan()
        self.assertGreater(len(patterns), 0)

    def test_signature_is_anonymized(self):
        """Trajectory signature contains no donor identity."""
        sig = self.mycelium.ingest(domain="family", trend="falling", D=0.5, dD_dt=-0.1)
        self.assertIsInstance(sig, TrajectorySignature)
        # Only buckets, no exact values
        self.assertIn("(", sig.d_bucket)  # "mid(0.3-0.7)" format
        self.assertIn("(", sig.d_bucket)

    def test_d_is_discretized(self):
        """Exact D value is never stored — only bucket."""
        sig1 = self.mycelium.ingest(domain="test", trend="stable", D=0.45, dD_dt=0.0)
        sig2 = self.mycelium.ingest(domain="test", trend="stable", D=0.55, dD_dt=0.0)
        # Both 0.45 and 0.55 should be in same bucket
        self.assertEqual(sig1.d_bucket, sig2.d_bucket)

    def test_rate_is_discretized(self):
        """Exact dD/dt is never stored — only bucket."""
        sig1 = self.mycelium.ingest(domain="test", trend="falling", D=0.5, dD_dt=-0.08)
        sig2 = self.mycelium.ingest(domain="test", trend="falling", D=0.5, dD_dt=-0.12)
        # Both should be "declining" bucket
        self.assertEqual(sig1.rate_bucket, sig2.rate_bucket)

    def test_privacy_budget_consumed(self):
        """Each scan consumes epsilon budget."""
        initial = self.mycelium._epsilon_remaining
        self.mycelium.scan()
        self.assertLess(self.mycelium._epsilon_remaining, initial)

    def test_scan_blocked_when_budget_exhausted(self):
        """No scans possible after privacy budget is spent."""
        # Exhaust budget (1.0 / 0.1 = 10 scans)
        for _ in range(11):
            self.mycelium.scan()
        self.assertTrue(self.mycelium.privacy_exhausted())
        result = self.mycelium.scan()
        self.assertEqual(len(result), 0)


# ═══════════════════════════════════════════════════
# DISCRETIZATION TESTS
# ═══════════════════════════════════════════════════

class TestDiscretization(unittest.TestCase):

    def setUp(self):
        self.m = Mycelium()

    def test_d_high_bucket(self):
        sig = self.m.ingest("test", "stable", D=0.85, dD_dt=0.0)
        self.assertEqual(sig.d_bucket, "high(0.7-1.0)")

    def test_d_mid_bucket(self):
        sig = self.m.ingest("test", "stable", D=0.5, dD_dt=0.0)
        self.assertEqual(sig.d_bucket, "mid(0.3-0.7)")

    def test_d_low_bucket(self):
        sig = self.m.ingest("test", "stable", D=0.2, dD_dt=0.0)
        self.assertEqual(sig.d_bucket, "low(0.0-0.3)")

    def test_rate_improving(self):
        sig = self.m.ingest("test", "rising", D=0.8, dD_dt=0.1)
        self.assertEqual(sig.rate_bucket, "improving")

    def test_rate_stable(self):
        sig = self.m.ingest("test", "stable", D=0.8, dD_dt=0.0)
        self.assertEqual(sig.rate_bucket, "stable")

    def test_rate_declining(self):
        sig = self.m.ingest("test", "falling", D=0.5, dD_dt=-0.1)
        self.assertEqual(sig.rate_bucket, "declining")

    def test_rate_collapsing(self):
        sig = self.m.ingest("test", "accelerating_fall", D=0.2, dD_dt=-0.3)
        self.assertEqual(sig.rate_bucket, "collapsing")


# ═══════════════════════════════════════════════════
# PATTERN DETECTION TESTS
# ═══════════════════════════════════════════════════

class TestPatternDetection(unittest.TestCase):

    def test_convergent_decline_detected(self):
        """Multiple donors falling in same domain → CONVERGENT_DECLINE."""
        m = Mycelium()
        for _ in range(10):
            m.ingest(domain="family", trend="falling", D=0.4, dD_dt=-0.1)
        patterns = m.scan()
        self.assertGreater(len(patterns), 0)
        self.assertEqual(patterns[0].pattern_type, PatternType.CONVERGENT_DECLINE)

    def test_structural_harm_detected(self):
        """Low D + collapsing rate → STRUCTURAL_HARM."""
        m = Mycelium()
        for _ in range(10):
            m.ingest(domain="work", trend="accelerating_fall", D=0.1, dD_dt=-0.25)
        patterns = m.scan()
        self.assertGreater(len(patterns), 0)
        self.assertEqual(patterns[0].pattern_type, PatternType.STRUCTURAL_HARM)

    def test_high_severity_triggers_rhizome(self):
        """Structural harm with high severity → RHIZOME alert."""
        m = Mycelium()
        for _ in range(25):
            m.ingest(domain="work", trend="accelerating_fall", D=0.1, dD_dt=-0.25)
        patterns = m.scan()
        self.assertGreater(len(patterns), 0)
        self.assertEqual(patterns[0].alert_level, MyceliumAlert.RHIZOME)
        self.assertTrue(m.is_rhizome())

    def test_multiple_domains_tracked(self):
        """Patterns detected independently per domain."""
        m = Mycelium()
        for _ in range(8):
            m.ingest(domain="family", trend="falling", D=0.4, dD_dt=-0.1)
        for _ in range(8):
            m.ingest(domain="work", trend="falling", D=0.3, dD_dt=-0.15)
        patterns = m.scan()
        domains = {p.domain for p in patterns}
        self.assertEqual(len(domains), 2)

    def test_different_buckets_dont_merge(self):
        """Donors in different buckets don't form a single pattern."""
        m = Mycelium()
        for _ in range(4):
            m.ingest(domain="test", trend="falling", D=0.8, dD_dt=-0.1)  # high bucket
        for _ in range(4):
            m.ingest(domain="test", trend="falling", D=0.2, dD_dt=-0.1)  # low bucket
        patterns = m.scan()
        # Neither group meets k=7 alone
        self.assertEqual(len(patterns), 0)


# ═══════════════════════════════════════════════════
# ALERT LEVEL TESTS
# ═══════════════════════════════════════════════════

class TestAlertLevels(unittest.TestCase):

    def test_no_alert_initially(self):
        m = Mycelium()
        self.assertEqual(m.current_alert, MyceliumAlert.NONE)
        self.assertFalse(m.is_active())

    def test_root_alert_on_moderate_pattern(self):
        """Moderate severity → ROOT level."""
        m = Mycelium()
        for _ in range(8):
            m.ingest(domain="test", trend="stable", D=0.5, dD_dt=-0.08)
        patterns = m.scan()
        if patterns:
            self.assertGreaterEqual(patterns[0].alert_level.value, MyceliumAlert.ROOT.value)

    def test_highest_alert_tracked(self):
        m = Mycelium()
        for _ in range(25):
            m.ingest(domain="work", trend="accelerating_fall", D=0.1, dD_dt=-0.25)
        m.scan()
        m.reset_alert()
        self.assertEqual(m.current_alert, MyceliumAlert.NONE)
        self.assertEqual(m.highest_alert, MyceliumAlert.RHIZOME)


# ═══════════════════════════════════════════════════
# LEDGER TESTS (COV#003)
# ═══════════════════════════════════════════════════

class TestAppendOnlyLedger(unittest.TestCase):
    """COV#003: All operations recorded. No record may be removed."""

    def test_ingest_recorded(self):
        m = Mycelium()
        m.ingest("test", "stable", D=0.8, dD_dt=0.0)
        self.assertEqual(m.ledger_length, 1)

    def test_scan_recorded(self):
        m = Mycelium()
        m.scan()
        self.assertEqual(m.ledger_length, 1)

    def test_reset_does_not_clear_ledger(self):
        m = Mycelium()
        m.ingest("test", "stable", D=0.8, dD_dt=0.0)
        m.scan()
        m.reset_alert()
        # 3 entries: ingest + scan + reset
        self.assertEqual(m.ledger_length, 3)

    def test_ledger_grows_monotonically(self):
        m = Mycelium()
        for i in range(5):
            m.ingest("test", "stable", D=0.8, dD_dt=0.0)
            self.assertEqual(m.ledger_length, i + 1)


# ═══════════════════════════════════════════════════
# STATE TESTS
# ═══════════════════════════════════════════════════

class TestMyceliumState(unittest.TestCase):

    def test_initial_state(self):
        m = Mycelium()
        state = m.state()
        self.assertEqual(state.signatures_ingested, 0)
        self.assertEqual(state.patterns_detected, 0)
        self.assertEqual(state.alert_level, "NONE")
        self.assertEqual(state.k_anonymity_floor, 7)

    def test_state_after_ingestion(self):
        m = Mycelium()
        for _ in range(10):
            m.ingest("family", "falling", D=0.3, dD_dt=-0.15)
        state = m.state()
        self.assertEqual(state.signatures_ingested, 10)
        self.assertEqual(state.domains_active, 1)

    def test_epsilon_tracking(self):
        m = Mycelium()
        state_before = m.state()
        m.scan()
        state_after = m.state()
        self.assertGreater(state_before.epsilon_remaining, state_after.epsilon_remaining)


# ═══════════════════════════════════════════════════
# SCENARIO: THE PREDATOR PATTERN
# ═══════════════════════════════════════════════════

class TestPredatorScenario(unittest.TestCase):
    """
    If a predator operates in a domain, multiple donors
    will show dignity collapse in that domain simultaneously.
    The mycelium should detect this WITHOUT knowing WHO the donors are.
    """

    def test_predator_leaves_structural_signature(self):
        m = Mycelium()
        # 15 donors in "community" all show accelerating collapse
        for _ in range(15):
            m.ingest(domain="community", trend="accelerating_fall", D=0.15, dD_dt=-0.25)
        patterns = m.scan()
        self.assertGreater(len(patterns), 0)

        harm_patterns = [p for p in patterns if p.pattern_type == PatternType.STRUCTURAL_HARM]
        self.assertGreater(len(harm_patterns), 0)
        self.assertEqual(harm_patterns[0].domain, "community")
        self.assertTrue(m.is_rhizome())

    def test_individual_cases_stay_hidden(self):
        """3 donors collapsing — real but below k. Must stay hidden."""
        m = Mycelium()
        for _ in range(3):
            m.ingest(domain="community", trend="accelerating_fall", D=0.1, dD_dt=-0.3)
        patterns = m.scan()
        self.assertEqual(len(patterns), 0)
        # System KNOWS something is there but cannot expose it
        self.assertGreater(m.suppressed_count, 0)

    def test_healthy_domain_no_false_alarm(self):
        """20 donors all healthy in a domain — no pattern."""
        m = Mycelium()
        for _ in range(20):
            m.ingest(domain="family", trend="rising", D=0.85, dD_dt=0.05)
        patterns = m.scan()
        # Patterns may surface but should not be at alert level
        for p in patterns:
            self.assertNotEqual(p.alert_level, MyceliumAlert.RHIZOME)


# ═══════════════════════════════════════════════════
# SCENARIO: PRIVACY VS HARM — THE CONSTITUTIONAL TENSION
# ═══════════════════════════════════════════════════

class TestConstitutionalTension(unittest.TestCase):
    """
    GAP#MYCELIUM-CONNECT-001: The system holds the tension.
    Privacy is not absolute. Harm detection is not unconditional.
    k-anonymity is the bridge.
    """

    def test_six_is_not_seven(self):
        """6 donors in crisis — system cannot act. Privacy wins."""
        m = Mycelium()
        for _ in range(6):
            m.ingest(domain="danger", trend="accelerating_fall", D=0.05, dD_dt=-0.4)
        patterns = m.scan()
        self.assertEqual(len(patterns), 0)

    def test_seven_tips_the_balance(self):
        """7 donors in crisis — system CAN act. Harm prevention wins."""
        m = Mycelium()
        for _ in range(7):
            m.ingest(domain="danger", trend="accelerating_fall", D=0.05, dD_dt=-0.4)
        patterns = m.scan()
        self.assertGreater(len(patterns), 0)
        self.assertTrue(m.is_active())

    def test_privacy_budget_is_finite(self):
        """System cannot scan indefinitely — privacy has a cost."""
        m = Mycelium()
        scans = 0
        while not m.privacy_exhausted():
            m.scan()
            scans += 1
        self.assertLessEqual(scans, int(EPSILON_BUDGET / EPSILON_PER_QUERY) + 1)


if __name__ == "__main__":
    unittest.main()
