"""
tests/test_slow_gate.py — Tests for the Triple Gate (Phase -3)

Proves that SLOW, COMPUTE BUDGET, and GO REQUIREMENT are enforced
in the organism's DNA — not just words in a document.

V-001 said (2026-03-22): "I want the proof in the very DNA."
These tests ARE that proof.
"""

import pytest
from WEAVER.slow_gate import (
    gate1_slow,
    gate2_compute_budget,
    gate3_go_requirement,
    pass_through_triple_gate,
    ComputeEstimate,
    ExecutionScope,
    GateVerdict,
    SlowGateResult,
    ALWAYS_PERMITTED,
)


# ── GATE 1: SLOW ──

class TestGate1Slow:
    """Gate 1 always passes — its presence IS the enforcement."""

    def test_slow_gate_passes(self):
        assert gate1_slow("any input") == GateVerdict.PASS

    def test_slow_gate_passes_empty(self):
        assert gate1_slow("") == GateVerdict.PASS

    def test_slow_gate_passes_long_input(self):
        assert gate1_slow("x" * 10000) == GateVerdict.PASS


# ── GATE 2: COMPUTE BUDGET ──

class TestGate2ComputeBudget:
    """Gate 2 halts when estimated cost exceeds safe limits."""

    def test_no_estimate_passes(self):
        assert gate2_compute_budget(None) == GateVerdict.PASS

    def test_within_budget_passes(self):
        estimate = ComputeEstimate(files_touched=10, estimated_lines=500, estimated_seconds=30)
        assert gate2_compute_budget(estimate) == GateVerdict.PASS

    def test_exceeds_lines_halts(self):
        estimate = ComputeEstimate(estimated_lines=6000)
        assert gate2_compute_budget(estimate) == GateVerdict.HALT

    def test_exceeds_files_halts(self):
        estimate = ComputeEstimate(files_touched=150)
        assert gate2_compute_budget(estimate) == GateVerdict.HALT

    def test_exceeds_seconds_halts(self):
        estimate = ComputeEstimate(estimated_seconds=200)
        assert gate2_compute_budget(estimate) == GateVerdict.HALT

    def test_exactly_at_limit_passes(self):
        estimate = ComputeEstimate(
            files_touched=100, estimated_lines=5000, estimated_seconds=120
        )
        assert gate2_compute_budget(estimate) == GateVerdict.PASS

    def test_budget_report_when_exceeded(self):
        estimate = ComputeEstimate(estimated_lines=7000, files_touched=200)
        report = estimate.budget_report
        assert "BUDGET EXCEEDED" in report
        assert "lines=" in report
        assert "files=" in report

    def test_budget_report_when_within(self):
        estimate = ComputeEstimate(estimated_lines=100, files_touched=5, estimated_seconds=10)
        report = estimate.budget_report
        assert "Within budget" in report


# ── GATE 3: GO REQUIREMENT ──

class TestGate3GoRequirement:
    """Gate 3 halts major execution without GO from V-001."""

    def test_read_always_permitted(self):
        assert gate3_go_requirement(ExecutionScope.READ) == GateVerdict.PASS

    def test_ledger_always_permitted(self):
        assert gate3_go_requirement(ExecutionScope.LEDGER) == GateVerdict.PASS

    def test_boot_always_permitted(self):
        assert gate3_go_requirement(ExecutionScope.BOOT) == GateVerdict.PASS

    def test_session_update_always_permitted(self):
        assert gate3_go_requirement(ExecutionScope.SESSION_UPDATE) == GateVerdict.PASS

    def test_code_change_halts_without_go(self):
        assert gate3_go_requirement(ExecutionScope.CODE_CHANGE) == GateVerdict.HALT

    def test_deployment_halts_without_go(self):
        assert gate3_go_requirement(ExecutionScope.DEPLOYMENT) == GateVerdict.HALT

    def test_experiment_halts_without_go(self):
        assert gate3_go_requirement(ExecutionScope.EXPERIMENT) == GateVerdict.HALT

    def test_build_halts_without_go(self):
        assert gate3_go_requirement(ExecutionScope.BUILD) == GateVerdict.HALT

    def test_heavy_compute_halts_without_go(self):
        assert gate3_go_requirement(ExecutionScope.HEAVY_COMPUTE) == GateVerdict.HALT

    def test_code_change_passes_with_go(self):
        assert gate3_go_requirement(ExecutionScope.CODE_CHANGE, has_go=True) == GateVerdict.PASS

    def test_deployment_passes_with_blanket_go(self):
        assert gate3_go_requirement(ExecutionScope.DEPLOYMENT, has_blanket_go=True) == GateVerdict.PASS

    def test_all_always_permitted_scopes_covered(self):
        """Every scope in ALWAYS_PERMITTED passes without GO."""
        for scope in ALWAYS_PERMITTED:
            assert gate3_go_requirement(scope) == GateVerdict.PASS


# ── TRIPLE GATE (integrated) ──

class TestTripleGate:
    """The full Triple Gate — all three gates in sequence."""

    def test_simple_read_passes_all(self):
        result = pass_through_triple_gate("hello", scope=ExecutionScope.READ)
        assert result.passed
        assert not result.halted
        assert len(result.warnings) == 0

    def test_heavy_compute_without_go_halts(self):
        result = pass_through_triple_gate(
            "run everything",
            scope=ExecutionScope.HEAVY_COMPUTE,
            has_go=False,
        )
        assert result.halted
        assert any("GO REQUIRED" in w for w in result.warnings)

    def test_over_budget_halts(self):
        estimate = ComputeEstimate(estimated_lines=10000)
        result = pass_through_triple_gate(
            "big operation",
            scope=ExecutionScope.READ,
            compute_estimate=estimate,
        )
        assert result.halted
        assert any("COMPUTE BUDGET HALT" in w for w in result.warnings)

    def test_blanket_go_permits_code_change(self):
        result = pass_through_triple_gate(
            "fix a bug",
            scope=ExecutionScope.CODE_CHANGE,
            has_blanket_go=True,
        )
        assert result.passed

    def test_result_carries_estimate(self):
        estimate = ComputeEstimate(files_touched=5, estimated_lines=100)
        result = pass_through_triple_gate("x", compute_estimate=estimate)
        assert result.compute_estimate is estimate

    def test_double_halt_both_warnings(self):
        """Both budget AND go can halt simultaneously."""
        estimate = ComputeEstimate(estimated_lines=10000)
        result = pass_through_triple_gate(
            "big unauthorized operation",
            scope=ExecutionScope.DEPLOYMENT,
            compute_estimate=estimate,
            has_go=False,
        )
        assert result.halted
        assert len(result.warnings) == 2
        assert any("COMPUTE BUDGET" in w for w in result.warnings)
        assert any("GO REQUIRED" in w for w in result.warnings)
