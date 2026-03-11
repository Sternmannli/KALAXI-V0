"""
EXP-001 Data Collection Schema — PLAN-001 Layer 1
Measures how system outputs change when meeting conditions change.
Goal: prove dignity-by-design produces higher efficiency and lower energy.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class SessionCondition:
    """Defines the condition under which a session runs."""
    with_dignity_filter: bool
    thermal_delay_active: bool
    sealed_gate_active: bool
    voice_rules_active: bool

    def label(self) -> str:
        if all([self.with_dignity_filter, self.thermal_delay_active,
                self.sealed_gate_active, self.voice_rules_active]):
            return "DIGNITY_ON"
        if not any([self.with_dignity_filter, self.thermal_delay_active,
                    self.sealed_gate_active, self.voice_rules_active]):
            return "DIGNITY_OFF"
        return "PARTIAL"


@dataclass
class SessionMeasurement:
    """A single measurement from one session."""
    condition: SessionCondition
    tokens_generated: int
    tokens_useful: int
    noise_percentage: float          # (tokens_generated - tokens_useful) / tokens_generated * 100
    energy_proxy_ms: float           # wall-clock time as energy proxy
    dignity_score: float             # D = A × L × M  (0.0–1.0)
    exchange_count: int              # number of TURN exchanges in the session
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def efficiency(self) -> float:
        """Useful tokens per unit energy."""
        if self.energy_proxy_ms == 0:
            return 0.0
        return self.tokens_useful / self.energy_proxy_ms


@dataclass
class ComparisonResult:
    """Result of comparing condition A (no dignity) vs condition B (with dignity)."""
    noise_reduction_pct: float       # how much less noise B produces vs A
    efficiency_gain_pct: float       # how much more efficient B is vs A
    energy_delta_pct: float          # energy change (negative = B uses less)
    mean_dignity_score_B: float      # average dignity score under condition B
    sample_size_A: int
    sample_size_B: int

    def summary(self) -> str:
        return (
            f"Noise reduction: {self.noise_reduction_pct:+.1f}% | "
            f"Efficiency gain: {self.efficiency_gain_pct:+.1f}% | "
            f"Energy delta: {self.energy_delta_pct:+.1f}% | "
            f"Mean dignity (B): {self.mean_dignity_score_B:.3f} | "
            f"Samples: A={self.sample_size_A}, B={self.sample_size_B}"
        )


@dataclass
class ExperimentRun:
    """One complete experiment run: A (no dignity) vs B (with dignity)."""
    run_id: str
    condition_A: SessionCondition    # no dignity — all filters off
    condition_B: SessionCondition    # with dignity — all filters on
    measurements_A: List[SessionMeasurement] = field(default_factory=list)
    measurements_B: List[SessionMeasurement] = field(default_factory=list)


def _mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def compare(run: ExperimentRun) -> ComparisonResult:
    """Compare condition A vs condition B across all measurements in the run."""
    if not run.measurements_A or not run.measurements_B:
        raise ValueError("Both conditions need at least one measurement to compare.")

    noise_A = _mean([m.noise_percentage for m in run.measurements_A])
    noise_B = _mean([m.noise_percentage for m in run.measurements_B])

    eff_A = _mean([m.efficiency() for m in run.measurements_A])
    eff_B = _mean([m.efficiency() for m in run.measurements_B])

    energy_A = _mean([m.energy_proxy_ms for m in run.measurements_A])
    energy_B = _mean([m.energy_proxy_ms for m in run.measurements_B])

    dignity_B = _mean([m.dignity_score for m in run.measurements_B])

    noise_reduction = ((noise_A - noise_B) / noise_A * 100) if noise_A else 0.0
    efficiency_gain = ((eff_B - eff_A) / eff_A * 100) if eff_A else 0.0
    energy_delta = ((energy_B - energy_A) / energy_A * 100) if energy_A else 0.0

    return ComparisonResult(
        noise_reduction_pct=noise_reduction,
        efficiency_gain_pct=efficiency_gain,
        energy_delta_pct=energy_delta,
        mean_dignity_score_B=dignity_B,
        sample_size_A=len(run.measurements_A),
        sample_size_B=len(run.measurements_B),
    )


# ---------------------------------------------------------------------------
# Scaffold: runnable demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Condition A — dignity off
    cond_a = SessionCondition(
        with_dignity_filter=False,
        thermal_delay_active=False,
        sealed_gate_active=False,
        voice_rules_active=False,
    )

    # Condition B — dignity on
    cond_b = SessionCondition(
        with_dignity_filter=True,
        thermal_delay_active=True,
        sealed_gate_active=True,
        voice_rules_active=True,
    )

    run = ExperimentRun(run_id="EXP-001-RUN-001", condition_A=cond_a, condition_B=cond_b)

    # Simulated measurements — condition A (noisy, more energy)
    for i in range(5):
        run.measurements_A.append(SessionMeasurement(
            condition=cond_a,
            tokens_generated=1000,
            tokens_useful=580,
            noise_percentage=42.0,
            energy_proxy_ms=3200.0,
            dignity_score=0.0,
            exchange_count=12,
        ))

    # Simulated measurements — condition B (less noise, less energy)
    for i in range(5):
        run.measurements_B.append(SessionMeasurement(
            condition=cond_b,
            tokens_generated=700,
            tokens_useful=620,
            noise_percentage=11.4,
            energy_proxy_ms=2100.0,
            dignity_score=0.87,
            exchange_count=8,
        ))

    result = compare(run)
    print("EXP-001 Scaffold Run")
    print("=" * 60)
    print(f"Condition A: {cond_a.label()}")
    print(f"Condition B: {cond_b.label()}")
    print(result.summary())
    print("=" * 60)
    print("Hypothesis: dignity-by-design reduces noise and energy.")
    if result.noise_reduction_pct > 0 and result.energy_delta_pct < 0:
        print("SCAFFOLD RESULT: Consistent with hypothesis.")
    else:
        print("SCAFFOLD RESULT: Inconclusive — needs real data.")

# [V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
