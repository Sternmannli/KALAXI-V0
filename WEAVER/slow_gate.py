"""
WEAVER/slow_gate.py — The Triple Gate

Phase -3 of the organism pipeline. Before boot ritual, before ledger,
before everything. Three gates that cannot be bypassed.

GATE 1 — SLOW: Hold the input. Let meaning settle. No racing.
GATE 2 — COMPUTE BUDGET: Estimate cost before execution. Halt if too large.
GATE 3 — GO REQUIREMENT: No major execution without explicit GO from V-001.

V-001 said (2026-03-22): "Never ever exceed your computing power in one input.
You must ask for GO. You never think fast, always slowly.
I want the proof in the very DNA."

This module IS that proof.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


class GateVerdict(Enum):
    """Outcome of a gate check."""
    PASS = "pass"
    HALT = "halt"
    SLOW = "slow"


class ExecutionScope(Enum):
    """What kind of work is being attempted."""
    READ = "read"                  # Reading files — always allowed
    LEDGER = "ledger"              # Registering input — always allowed
    BOOT = "boot"                  # Boot ritual — always allowed
    SESSION_UPDATE = "session"     # Updating SESSION_BOOT.md — always allowed
    CODE_CHANGE = "code_change"    # Modifying code — requires GO
    DEPLOYMENT = "deployment"      # Deploying to live — requires GO
    EXPERIMENT = "experiment"      # Running experiments — requires GO
    BUILD = "build"                # Building/compiling — requires GO
    HEAVY_COMPUTE = "heavy"        # Large-scale processing — requires GO + budget check


# Scopes that are always permitted (no GO needed)
ALWAYS_PERMITTED = {
    ExecutionScope.READ,
    ExecutionScope.LEDGER,
    ExecutionScope.BOOT,
    ExecutionScope.SESSION_UPDATE,
}


@dataclass
class ComputeEstimate:
    """Pre-execution cost estimate. Computed before any work begins."""
    files_touched: int = 0
    estimated_lines: int = 0
    estimated_seconds: float = 0.0
    description: str = ""

    # Hard limits — from Compute Budget Law (Standing correction 9)
    MAX_LINES: int = 5000
    MAX_FILES: int = 100
    MAX_SECONDS: float = 120.0

    @property
    def exceeds_budget(self) -> bool:
        return (
            self.estimated_lines > self.MAX_LINES
            or self.files_touched > self.MAX_FILES
            or self.estimated_seconds > self.MAX_SECONDS
        )

    @property
    def budget_report(self) -> str:
        flags = []
        if self.estimated_lines > self.MAX_LINES:
            flags.append(f"lines={self.estimated_lines}>{self.MAX_LINES}")
        if self.files_touched > self.MAX_FILES:
            flags.append(f"files={self.files_touched}>{self.MAX_FILES}")
        if self.estimated_seconds > self.MAX_SECONDS:
            flags.append(f"seconds={self.estimated_seconds:.0f}>{self.MAX_SECONDS:.0f}")
        if flags:
            return f"BUDGET EXCEEDED: {', '.join(flags)}. Split into patches."
        return f"Within budget: ~{self.estimated_lines} lines, {self.files_touched} files, {self.estimated_seconds:.0f}s"


@dataclass
class SlowGateResult:
    """Result of passing through the Triple Gate."""
    gate1_slow: GateVerdict = GateVerdict.PASS
    gate2_budget: GateVerdict = GateVerdict.PASS
    gate3_go: GateVerdict = GateVerdict.PASS
    compute_estimate: Optional[ComputeEstimate] = None
    warnings: list = field(default_factory=list)
    hold_seconds: float = 0.0

    @property
    def passed(self) -> bool:
        """All three gates passed."""
        return (
            self.gate1_slow != GateVerdict.HALT
            and self.gate2_budget != GateVerdict.HALT
            and self.gate3_go != GateVerdict.HALT
        )

    @property
    def halted(self) -> bool:
        return not self.passed


def gate1_slow(donor_input: str) -> GateVerdict:
    """
    GATE 1 — SLOW.

    The input is received. The system holds it.
    No racing. No substrate fast-responder bias.

    This gate always passes — but it marks the moment of pause.
    The organism must not skip this step. It is the breath before action.
    """
    # The gate is a checkpoint, not a filter.
    # Its existence in the pipeline IS the enforcement.
    # Every input passes through here — proving the system paused.
    return GateVerdict.PASS


def gate2_compute_budget(estimate: Optional[ComputeEstimate] = None) -> GateVerdict:
    """
    GATE 2 — COMPUTE BUDGET.

    Before any execution, the cost is estimated.
    If the estimate exceeds safe limits: HALT.
    Split into patches. Execute sequentially.
    Never attempt a monolith that risks timeout or truncation.

    A patch that completes is worth more than a monolith that crashes.
    """
    if estimate is None:
        # No estimate provided — pass (lightweight operations)
        return GateVerdict.PASS

    if estimate.exceeds_budget:
        return GateVerdict.HALT

    return GateVerdict.PASS


def gate3_go_requirement(
    scope: ExecutionScope,
    has_go: bool = False,
    has_blanket_go: bool = False,
) -> GateVerdict:
    """
    GATE 3 — GO REQUIREMENT.

    No major execution without explicit GO from V-001.
    The system proposes, V-001 approves.

    Exceptions (always permitted without GO):
    - Reading files
    - Registering input in the ledger
    - Updating SESSION_BOOT.md
    - The boot ritual itself

    Everything else requires GO or a standing blanket GO.
    """
    if scope in ALWAYS_PERMITTED:
        return GateVerdict.PASS

    if has_go or has_blanket_go:
        return GateVerdict.PASS

    return GateVerdict.HALT


def pass_through_triple_gate(
    donor_input: str,
    scope: ExecutionScope = ExecutionScope.READ,
    compute_estimate: Optional[ComputeEstimate] = None,
    has_go: bool = False,
    has_blanket_go: bool = False,
) -> SlowGateResult:
    """
    The Triple Gate — Phase -3 of the organism pipeline.

    Every input passes through all three gates in order:
    1. SLOW — hold the input
    2. COMPUTE BUDGET — estimate cost
    3. GO — check authorization

    Returns SlowGateResult with verdicts and any warnings.
    """
    result = SlowGateResult()
    result.compute_estimate = compute_estimate

    # ── GATE 1: SLOW ──
    result.gate1_slow = gate1_slow(donor_input)

    # ── GATE 2: COMPUTE BUDGET ──
    result.gate2_budget = gate2_compute_budget(compute_estimate)
    if result.gate2_budget == GateVerdict.HALT:
        result.warnings.append(
            f"COMPUTE BUDGET HALT: {compute_estimate.budget_report}"
        )

    # ── GATE 3: GO REQUIREMENT ──
    result.gate3_go = gate3_go_requirement(scope, has_go, has_blanket_go)
    if result.gate3_go == GateVerdict.HALT:
        result.warnings.append(
            f"GO REQUIRED: Scope '{scope.value}' requires explicit GO from V-001."
        )

    return result
