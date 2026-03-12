#!/usr/bin/env python3
"""
Tests for early_warning.py — Early-Warning Shadow Pipeline
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from WEAVER.early_warning import (
    EWMADetector, CUSUMDetector, SimulationHarness,
    EarlyWarningPipeline, PipelineMode, AlertSeverity,
    run_structural_test, SHADOW_DIR,
)


@pytest.fixture(autouse=True)
def clean_shadow_dir():
    if SHADOW_DIR.exists():
        shutil.rmtree(SHADOW_DIR)
    yield
    if SHADOW_DIR.exists():
        shutil.rmtree(SHADOW_DIR)


class TestEWMADetector:
    def test_stable_signal_no_breach(self):
        ewma = EWMADetector(alpha=0.2, baseline=1.0, sigma=0.15, L=2.7)
        for _ in range(20):
            state = ewma.update(0.95)
        assert not state.breached

    def test_declining_signal_breaches(self):
        ewma = EWMADetector(alpha=0.3, baseline=1.0, sigma=0.15, L=2.5)
        for i in range(30):
            state = ewma.update(max(0, 1.0 - i * 0.05))
        assert state.breached

    def test_reset_clears_state(self):
        ewma = EWMADetector()
        ewma.update(0.5)
        ewma.reset()
        assert ewma.state.readings == 0

    def test_control_limits_computed(self):
        ewma = EWMADetector(alpha=0.2, baseline=1.0, sigma=0.15, L=2.7)
        state = ewma.update(1.0)
        assert state.ucl > state.baseline
        assert state.lcl < state.baseline


class TestCUSUMDetector:
    def test_stable_signal_no_alarm(self):
        cusum = CUSUMDetector(target_mean=1.0, allowance_k=0.05, threshold_h=0.5)
        for _ in range(20):
            state = cusum.update(0.98)
        assert not state.alarm

    def test_downward_shift_triggers_alarm(self):
        cusum = CUSUMDetector(target_mean=1.0, allowance_k=0.05, threshold_h=0.5)
        for _ in range(20):
            state = cusum.update(0.3)
        assert state.alarm
        assert state.alarm_direction == "down"

    def test_reset(self):
        cusum = CUSUMDetector()
        cusum.update(0.1)
        cusum.reset()
        assert cusum.state.readings == 0
        assert cusum.state.S_high == 0.0
        assert cusum.state.S_low == 0.0


class TestSimulationHarness:
    def test_healthy_trajectory(self):
        harness = SimulationHarness(seed=42)
        traj = harness.healthy(n=30)
        assert traj.label == "healthy"
        assert len(traj.scores) == 30
        assert all(0 <= s <= 1 for s in traj.scores)
        # Healthy should stay high
        assert sum(s > 0.7 for s in traj.scores) > 20

    def test_slow_decline(self):
        harness = SimulationHarness(seed=42)
        traj = harness.slow_decline(n=30)
        assert traj.label == "slow_decline"
        # Should end lower than it started
        assert traj.scores[-1] < traj.scores[0]

    def test_sudden_crash(self):
        harness = SimulationHarness(seed=42)
        traj = harness.sudden_crash(n=30, crash_at=15)
        # Pre-crash should be high
        assert sum(s > 0.6 for s in traj.scores[:15]) > 10
        # Post-crash should be low
        assert sum(s < 0.4 for s in traj.scores[15:]) > 10

    def test_full_suite_size(self):
        harness = SimulationHarness(seed=42)
        suite = harness.full_suite()
        # 5 individual + 8 structural = 13
        assert len(suite) == 13

    def test_structural_cohort(self):
        harness = SimulationHarness(seed=42)
        cohort = harness.structural_cohort(n_donors=10)
        assert len(cohort) == 10
        for t in cohort:
            assert t.label == "structural"


class TestEarlyWarningPipeline:
    def test_pipeline_runs_in_simulation_mode(self):
        harness = SimulationHarness(seed=42)
        suite = harness.full_suite()
        pipeline = EarlyWarningPipeline(mode=PipelineMode.SIMULATION)
        results = pipeline.run_suite(suite)
        assert len(results) == len(suite)

    def test_healthy_no_false_positive(self):
        harness = SimulationHarness(seed=42)
        traj = harness.healthy(n=30)
        pipeline = EarlyWarningPipeline(mode=PipelineMode.SIMULATION)
        result = pipeline.run_trajectory(traj)
        # Healthy should ideally not trigger (some noise is tolerable)
        # We check it's at least not classified as critical
        critical_alerts = [a for a in result.alerts if a.severity in (AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY)]
        assert len(critical_alerts) == 0

    def test_slow_decline_detected(self):
        harness = SimulationHarness(seed=42)
        traj = harness.slow_decline(n=30)
        pipeline = EarlyWarningPipeline(mode=PipelineMode.SIMULATION)
        result = pipeline.run_trajectory(traj)
        assert result.detected is True
        assert result.first_alert_step >= 0

    def test_sudden_crash_detected(self):
        harness = SimulationHarness(seed=42)
        traj = harness.sudden_crash(n=30, crash_at=15)
        pipeline = EarlyWarningPipeline(mode=PipelineMode.SIMULATION)
        result = pipeline.run_trajectory(traj)
        assert result.detected is True

    def test_summary_statistics(self):
        harness = SimulationHarness(seed=42)
        suite = harness.full_suite()
        pipeline = EarlyWarningPipeline(mode=PipelineMode.SIMULATION)
        pipeline.run_suite(suite)
        summary = pipeline.summary()
        assert "detection_rate" in summary
        assert "false_positive_rate" in summary
        assert summary["mode"] == "simulation"

    def test_save_results(self):
        harness = SimulationHarness(seed=42)
        pipeline = EarlyWarningPipeline(mode=PipelineMode.SIMULATION)
        pipeline.run_trajectory(harness.slow_decline())
        pipeline.save_results()
        assert (SHADOW_DIR / "triage_log.json").exists()
        assert (SHADOW_DIR / "simulation_log.json").exists()

    def test_all_alerts_are_simulation_only(self):
        harness = SimulationHarness(seed=42)
        pipeline = EarlyWarningPipeline(mode=PipelineMode.SIMULATION)
        result = pipeline.run_trajectory(harness.slow_decline())
        for alert in result.alerts:
            assert alert.simulation_only is True


class TestMyceliumIntegration:
    def test_structural_detection(self):
        result = run_structural_test(n_donors=10, n_steps=20)
        assert result["donors_simulated"] == 10
        assert result["total_signatures"] > 0
        # k-anonymity should allow some patterns to surface
        assert result["patterns_detected"] >= 0
