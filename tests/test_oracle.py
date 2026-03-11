#!/usr/bin/env python3
"""
Tests for WEAVER/oracle.py — The Oracle (Self-Audit Layer).
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import unittest
from WEAVER.oracle import (
    Oracle, WitnessScale, WitnessLevel, WitnessRecord,
    check_proprioception, RelayStatus, ProprioceptionResult,
    AuditSeverity, OracleReport,
)


# ═══════════════════════════════════════════════════
# WITNESS SCALE TESTS
# ═══════════════════════════════════════════════════

class TestWitnessScaleBasic(unittest.TestCase):

    def setUp(self):
        self.ws = WitnessScale()

    def test_register_at_w0(self):
        record = self.ws.register("P#0001", "proverb")
        self.assertEqual(record.level, WitnessLevel.UNSEEN)
        self.assertEqual(record.element_type, "proverb")

    def test_register_duplicate_returns_existing(self):
        r1 = self.ws.register("P#0001")
        r2 = self.ws.register("P#0001")
        self.assertIs(r1, r2)

    def test_process_moves_to_w1(self):
        self.ws.register("P#0001")
        record = self.ws.process("P#0001")
        self.assertEqual(record.level, WitnessLevel.PASSED)

    def test_flag_moves_to_w2(self):
        self.ws.register("P#0001")
        self.ws.process("P#0001")
        record = self.ws.flag("P#0001")
        self.assertEqual(record.level, WitnessLevel.FLAGGED)

    def test_steward_sees_moves_to_w3(self):
        self.ws.register("P#0001")
        self.ws.process("P#0001")
        record = self.ws.steward_sees("P#0001", "session-1")
        self.assertEqual(record.level, WitnessLevel.SEEN)
        self.assertEqual(record.sessions_seen, 1)

    def test_steward_holds_moves_to_w4(self):
        self.ws.register("P#0001")
        self.ws.steward_sees("P#0001", "session-1")
        record = self.ws.steward_holds("P#0001", "session-2")
        self.assertEqual(record.level, WitnessLevel.HELD)

    def test_steward_embodies_moves_to_w5(self):
        self.ws.register("P#0001")
        self.ws.steward_sees("P#0001")
        record = self.ws.steward_embodies("P#0001", decision="ratified COV#015")
        self.assertEqual(record.level, WitnessLevel.EMBODIED)


class TestWitnessScaleRules(unittest.TestCase):

    def setUp(self):
        self.ws = WitnessScale()

    def test_non_decreasing_from_w3(self):
        """Rule 1: Once W-3+, cannot go below W-3."""
        self.ws.register("P#0001")
        self.ws.steward_sees("P#0001")
        # Try to downgrade — should be silently refused
        record = self.ws.transition("P#0001", WitnessLevel.PASSED)
        self.assertEqual(record.level, WitnessLevel.SEEN)  # Still W-3

    def test_no_backwards_movement(self):
        """Cannot go from W-2 to W-1."""
        self.ws.register("P#0001")
        self.ws.process("P#0001")
        self.ws.flag("P#0001")
        record = self.ws.transition("P#0001", WitnessLevel.PASSED)
        self.assertEqual(record.level, WitnessLevel.FLAGGED)  # Still W-2

    def test_transitions_are_logged(self):
        """Rule 2: Transitions are append-only."""
        self.ws.register("P#0001")
        self.ws.process("P#0001")
        self.ws.steward_sees("P#0001")
        self.assertEqual(self.ws.total_transitions, 2)

    def test_nonexistent_transition_returns_none(self):
        result = self.ws.transition("DOES_NOT_EXIST", WitnessLevel.SEEN)
        self.assertIsNone(result)


class TestWitnessScaleSurfacing(unittest.TestCase):

    def setUp(self):
        self.ws = WitnessScale(thermal_delay_cycles=3)

    def test_surfacing_after_thermal_delay(self):
        """Critical Threshold Rule: W-0/W-1 beyond delay triggers surfacing."""
        self.ws.register("P#0001")
        self.ws.process("P#0001")
        # Tick past thermal delay
        for _ in range(4):
            surfaced = self.ws.tick()
        self.assertIn("P#0001", surfaced)
        # Should now be flagged (W-2)
        record = self.ws.get("P#0001")
        self.assertEqual(record.level, WitnessLevel.FLAGGED)

    def test_seen_elements_not_surfaced(self):
        self.ws.register("P#0001")
        self.ws.steward_sees("P#0001")
        for _ in range(5):
            surfaced = self.ws.tick()
        self.assertNotIn("P#0001", surfaced)


class TestWitnessScaleQueries(unittest.TestCase):

    def setUp(self):
        self.ws = WitnessScale()
        self.ws.register("P#0001", "proverb")
        self.ws.register("P#0002", "anomaly")
        self.ws.register("P#0003", "covenant")
        self.ws.process("P#0001")
        self.ws.steward_sees("P#0002")

    def test_distribution(self):
        dist = self.ws.distribution()
        self.assertEqual(dist["UNSEEN"], 1)   # P#0003
        self.assertEqual(dist["PASSED"], 1)   # P#0001
        self.assertEqual(dist["SEEN"], 1)     # P#0002

    def test_unwatched(self):
        unwatched = self.ws.unwatched()
        ids = [r.element_id for r in unwatched]
        self.assertIn("P#0001", ids)
        self.assertIn("P#0003", ids)
        self.assertNotIn("P#0002", ids)

    def test_witnessed(self):
        witnessed = self.ws.witnessed()
        ids = [r.element_id for r in witnessed]
        self.assertIn("P#0002", ids)
        self.assertEqual(len(witnessed), 1)


# ═══════════════════════════════════════════════════
# PROPRIOCEPTION TESTS
# ═══════════════════════════════════════════════════

class TestProprioception(unittest.TestCase):

    def test_healthy_relay(self):
        result = check_proprioception(True, True, True)
        self.assertEqual(result.status, RelayStatus.HEALTHY)
        self.assertFalse(result.halt_required)

    def test_degraded_relay(self):
        result = check_proprioception(True, False, True)
        self.assertEqual(result.status, RelayStatus.DEGRADED)
        self.assertFalse(result.halt_required)

    def test_interrupted_relay_halts(self):
        """AXIOM: If relay interrupted, system must halt."""
        result = check_proprioception(False, False, False)
        self.assertEqual(result.status, RelayStatus.INTERRUPTED)
        self.assertTrue(result.halt_required)

    def test_single_failure_not_halt(self):
        result = check_proprioception(False, True, True)
        self.assertFalse(result.halt_required)


# ═══════════════════════════════════════════════════
# ORACLE SELF-AUDIT TESTS
# ═══════════════════════════════════════════════════

class TestOracleAudit(unittest.TestCase):

    def setUp(self):
        self.oracle = Oracle(thermal_delay_cycles=5)

    def test_healthy_audit(self):
        report = self.oracle.audit()
        self.assertEqual(report.overall_health, "healthy")
        self.assertEqual(report.cycle, 1)

    def test_critical_drift_detected(self):
        report = self.oracle.audit(drift_rate=-0.2, drift_level="critical")
        severities = [f.severity for f in report.findings]
        self.assertIn(AuditSeverity.CRITICAL, severities)
        self.assertEqual(report.overall_health, "critical")

    def test_colonial_creep_detected(self):
        report = self.oracle.audit(
            drift_rate=-0.1,
            voice_score=0.3,
            srvp_score=0.2,
        )
        self.assertGreater(report.colonial_creep_risk, 0.3)

    def test_halt_on_proprioception_loss(self):
        self.oracle.check_relay(False, False, False)
        report = self.oracle.audit()
        self.assertEqual(report.overall_health, "halted")
        halt_findings = [f for f in report.findings if f.severity == AuditSeverity.HALT]
        self.assertGreater(len(halt_findings), 0)

    def test_unwatched_elements_flagged(self):
        # Register many elements, don't witness any
        for i in range(10):
            self.oracle.witness.process(f"P#{i:04d}", "proverb")
        report = self.oracle.audit()
        self.assertEqual(report.unwatched_count, 10)
        # Should have a witness_scale finding
        ws_findings = [f for f in report.findings if f.check_name == "witness_scale"]
        self.assertGreater(len(ws_findings), 0)

    def test_report_summary(self):
        report = self.oracle.audit()
        summary = report.summary()
        self.assertIn("ORACLE REPORT", summary)
        self.assertIn("HEALTHY", summary)

    def test_audit_cycle_increments(self):
        self.oracle.audit()
        self.oracle.audit()
        self.assertEqual(self.oracle.audit_cycle, 2)

    def test_latency_dignity_warning(self):
        report = self.oracle.audit(latency_dignity_rate=0.5)
        lt_findings = [f for f in report.findings if f.check_name == "latency_dignity"]
        self.assertGreater(len(lt_findings), 0)

    def test_voice_warning(self):
        report = self.oracle.audit(voice_score=0.3)
        voice_findings = [f for f in report.findings if f.check_name == "voice_integrity"]
        self.assertGreater(len(voice_findings), 0)


class TestOracleIntegration(unittest.TestCase):
    """Test Oracle with Witness Scale + Proprioception together."""

    def test_full_lifecycle(self):
        oracle = Oracle(thermal_delay_cycles=2)

        # Register elements
        oracle.witness.process("P#0001", "proverb")
        oracle.witness.process("ANOM#0001", "anomaly")

        # Steward witnesses one
        oracle.witness.steward_sees("P#0001", "session-1")

        # Check relay
        oracle.check_relay(True, True, True)

        # Run audit
        report = oracle.audit()
        self.assertEqual(report.proprioception, "healthy")
        self.assertEqual(report.unwatched_count, 1)  # ANOM#0001

        # Witness distribution should show the split
        dist = report.witness_distribution
        self.assertEqual(dist["SEEN"], 1)
        self.assertGreater(dist["PASSED"], 0)


if __name__ == "__main__":
    unittest.main()
