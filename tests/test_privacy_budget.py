#!/usr/bin/env python3
"""
Tests for privacy_budget.py — Global epsilon accounting.
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from WEAVER.privacy_budget import PrivacyBudget, EPSILON_TOTAL_BUDGET, K_ANONYMITY_FLOOR


class TestPrivacyBudget:
    def test_initial_state(self):
        pb = PrivacyBudget()
        state = pb.state()
        assert state.total_budget == EPSILON_TOTAL_BUDGET
        assert state.consumed == 0.0
        assert state.remaining == EPSILON_TOTAL_BUDGET
        assert state.status == "healthy"

    def test_consume_reduces_remaining(self):
        pb = PrivacyBudget(total_budget=1.0)
        entry = pb.consume(0.1, "mycelium", "pattern_scan")
        assert entry is not None
        assert entry.epsilon_consumed == 0.1
        assert pb.remaining == pytest.approx(0.9, abs=1e-6)

    def test_consume_tracks_cumulative(self):
        pb = PrivacyBudget(total_budget=1.0)
        pb.consume(0.1, "mycelium", "scan1")
        pb.consume(0.2, "out", "export1")
        assert pb.state().consumed == pytest.approx(0.3, abs=1e-6)

    def test_cannot_exceed_budget(self):
        pb = PrivacyBudget(total_budget=0.5)
        pb.consume(0.4, "mycelium", "scan1")
        entry = pb.consume(0.2, "mycelium", "scan2")  # Would exceed
        assert entry is None
        assert pb.remaining == pytest.approx(0.1, abs=1e-6)

    def test_exhaustion_auto_locks(self):
        pb = PrivacyBudget(total_budget=0.2)
        pb.consume(0.2, "mycelium", "scan1")
        assert pb.is_exhausted
        assert pb.is_locked
        entry = pb.consume(0.01, "mycelium", "scan2")
        assert entry is None

    def test_k_anonymity_below_floor_denied(self):
        pb = PrivacyBudget()
        entry = pb.consume(0.1, "mycelium", "scan", k_achieved=3)
        assert entry is None  # k=3 < k_floor=7

    def test_k_anonymity_at_floor_accepted(self):
        pb = PrivacyBudget()
        entry = pb.consume(0.1, "mycelium", "scan", k_achieved=7)
        assert entry is not None

    def test_manual_lock_unlock(self):
        pb = PrivacyBudget(total_budget=1.0)
        pb.consume(0.1, "mycelium", "scan")
        pb.lock("steward emergency")
        assert pb.is_locked
        entry = pb.consume(0.1, "mycelium", "scan2")
        assert entry is None
        pb.unlock("steward")
        assert not pb.is_locked
        entry = pb.consume(0.1, "mycelium", "scan3")
        assert entry is not None

    def test_cannot_unlock_exhausted(self):
        pb = PrivacyBudget(total_budget=0.1)
        pb.consume(0.1, "mycelium", "scan")
        assert pb.is_exhausted
        result = pb.unlock("steward")
        assert result is False
        assert pb.is_locked

    def test_consumption_by_module(self):
        pb = PrivacyBudget()
        pb.consume(0.1, "mycelium", "scan1")
        pb.consume(0.2, "out", "export1")
        pb.consume(0.05, "mycelium", "scan2")
        by_mod = pb.consumption_by_module()
        assert by_mod["mycelium"] == pytest.approx(0.15, abs=1e-6)
        assert by_mod["out"] == pytest.approx(0.2, abs=1e-6)

    def test_status_transitions(self):
        pb = PrivacyBudget(total_budget=1.0)
        assert pb.state().status == "healthy"
        pb.consume(0.75, "mycelium", "big_scan")
        assert pb.state().status == "warning"
        pb.consume(0.2, "mycelium", "scan2")
        assert pb.state().status == "critical"
        pb.consume(0.05, "mycelium", "scan3")
        assert pb.state().status == "exhausted"

    def test_advanced_composition_bound(self):
        # Advanced composition is tighter than basic for large n
        # At n=100, ε=0.1: basic = 10.0, advanced should be much less
        n = 100
        eps = 0.1
        basic = n * eps  # = 10.0
        advanced = PrivacyBudget.advanced_composition_bound(n, eps)
        assert advanced < basic

    def test_save_and_load_ledger(self):
        pb = PrivacyBudget(total_budget=1.0)
        pb.consume(0.1, "mycelium", "scan1")
        pb.consume(0.2, "out", "export1")
        pb.save_ledger()

        pb2 = PrivacyBudget()
        pb2.load_ledger()
        assert pb2.state().consumed == pytest.approx(0.3, abs=1e-6)
        assert pb2.remaining == pytest.approx(0.7, abs=1e-6)


class TestCalibrationSweep:
    def test_sweep_runs(self):
        from WEAVER.calibrate import CalibrationSweep
        sweep = CalibrationSweep(seed=42)
        # Run a tiny sweep (2x1x1x1 = 2 configs)
        results = sweep.sweep(alphas=[0.2, 0.3], Ls=[2.7], ks=[0.05], hs=[0.5])
        assert len(results) == 2
        # Results should be sorted by score descending
        assert results[0].calibration_score >= results[1].calibration_score

    def test_sweep_metrics_valid(self):
        from WEAVER.calibrate import CalibrationSweep
        sweep = CalibrationSweep(seed=42)
        results = sweep.sweep(alphas=[0.2], Ls=[2.7], ks=[0.05], hs=[0.5])
        r = results[0]
        assert 0.0 <= r.detection_rate <= 1.0
        assert 0.0 <= r.false_positive_rate <= 1.0
        assert r.avg_lead_time >= 0
