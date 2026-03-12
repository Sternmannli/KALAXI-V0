#!/usr/bin/env python3
"""
calibrate.py — EWMA/CUSUM Parameter Sweep + Calibration Harness

Sweeps detector parameters (alpha, threshold, allowance, L-width)
across the full simulation suite and reports:
  - Detection rate per trajectory type
  - False positive rate
  - Average lead time (steps before minimum D)
  - Cost-aware alert scoring

Use this to choose detector parameters before opening the door.

Usage:
  python WEAVER/calibrate.py                    # Run default sweep
  python WEAVER/calibrate.py --detailed         # Include per-trajectory breakdown

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.early_warning import (
    EWMADetector, CUSUMDetector, SimulationHarness,
    SimulatedTrajectory, PipelineMode,
)
from WEAVER.dignity_drift import DignityDrift, DriftLevel


@dataclass
class CalibrationResult:
    """Result of one parameter configuration across the full suite."""
    ewma_alpha: float
    ewma_L: float
    cusum_k: float
    cusum_h: float
    detection_rate: float           # Fraction of decline trajectories detected
    false_positive_rate: float      # Fraction of healthy trajectories with alerts
    avg_lead_time: float            # Average steps before minimum D
    total_alerts: int
    alerts_per_trajectory: float
    # Cost-aware metric: higher is better
    # score = detection_rate - 2 * false_positive_rate + 0.1 * normalized_lead_time
    calibration_score: float


class CalibrationSweep:
    """
    Sweeps EWMA and CUSUM parameters across the simulation suite.
    Produces a ranked table of parameter configurations.
    """

    # Default parameter grids
    EWMA_ALPHAS = [0.1, 0.15, 0.2, 0.25, 0.3]
    EWMA_LS = [2.0, 2.5, 2.7, 3.0]
    CUSUM_KS = [0.03, 0.05, 0.08, 0.1]
    CUSUM_HS = [0.3, 0.5, 0.7, 1.0]

    def __init__(self, seed: int = 42):
        self._harness = SimulationHarness(seed=seed)
        self._suite = self._harness.full_suite()
        self._results: List[CalibrationResult] = []

    def _run_config(self, alpha: float, L: float, k: float, h: float) -> CalibrationResult:
        """Run one parameter configuration across the full suite."""

        decline_labels = {"slow_decline", "sudden_crash", "structural"}
        healthy_labels = {"healthy"}

        total_decline = 0
        detected_decline = 0
        total_healthy = 0
        false_positive_healthy = 0
        lead_times = []
        total_alerts = 0

        for traj in self._suite:
            ewma = EWMADetector(alpha=alpha, baseline=1.0, sigma=0.15, L=L)
            cusum = CUSUMDetector(target_mean=1.0, allowance_k=k, threshold_h=h)
            drift = DignityDrift()

            first_alert_step = -1
            min_D = 1.0
            min_D_step = 0
            alerts = 0

            for step, D in enumerate(traj.scores):
                if D < min_D:
                    min_D = D
                    min_D_step = step

                ewma_state = ewma.update(D)
                cusum_state = cusum.update(D)
                drift.record(D, f"CAL-{step}", traj.domain)
                drift_alert = drift.check()

                fired = (
                    ewma_state.breached or
                    (cusum_state.alarm and cusum_state.alarm_direction == "down") or
                    drift_alert.level in (DriftLevel.DECLINING, DriftLevel.CRITICAL)
                )

                if fired:
                    alerts += 1
                    if first_alert_step == -1:
                        first_alert_step = step

            total_alerts += alerts

            if traj.label in decline_labels:
                total_decline += 1
                if first_alert_step >= 0:
                    detected_decline += 1
                    lead_time = max(0, min_D_step - first_alert_step)
                    lead_times.append(lead_time)

            if traj.label in healthy_labels:
                total_healthy += 1
                if first_alert_step >= 0:
                    false_positive_healthy += 1

        det_rate = detected_decline / total_decline if total_decline > 0 else 0.0
        fpr = false_positive_healthy / total_healthy if total_healthy > 0 else 0.0
        avg_lead = sum(lead_times) / len(lead_times) if lead_times else 0.0
        alerts_per = total_alerts / len(self._suite) if self._suite else 0.0

        # Normalized lead time (max plausible lead time ~25 steps)
        norm_lead = min(avg_lead / 25.0, 1.0)

        # Calibration score: maximize detection, minimize false positives, reward lead time
        score = det_rate - 2.0 * fpr + 0.1 * norm_lead

        return CalibrationResult(
            ewma_alpha=alpha,
            ewma_L=L,
            cusum_k=k,
            cusum_h=h,
            detection_rate=round(det_rate, 4),
            false_positive_rate=round(fpr, 4),
            avg_lead_time=round(avg_lead, 2),
            total_alerts=total_alerts,
            alerts_per_trajectory=round(alerts_per, 2),
            calibration_score=round(score, 4),
        )

    def sweep(self, alphas=None, Ls=None, ks=None, hs=None) -> List[CalibrationResult]:
        """Run the full parameter sweep. Returns results sorted by score."""
        alphas = alphas or self.EWMA_ALPHAS
        Ls = Ls or self.EWMA_LS
        ks = ks or self.CUSUM_KS
        hs = hs or self.CUSUM_HS

        self._results = []
        total_configs = len(alphas) * len(Ls) * len(ks) * len(hs)
        done = 0

        for alpha in alphas:
            for L in Ls:
                for k in ks:
                    for h in hs:
                        result = self._run_config(alpha, L, k, h)
                        self._results.append(result)
                        done += 1

        # Sort by calibration score (descending)
        self._results.sort(key=lambda r: r.calibration_score, reverse=True)
        return self._results

    def top_n(self, n: int = 10) -> List[CalibrationResult]:
        """Return top N configurations by calibration score."""
        return self._results[:n]

    def save_results(self, path: str = None):
        """Save sweep results to JSON."""
        if path is None:
            path = str(ROOT / "MANIFEST" / "calibration_sweep.json")

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        data = {
            "total_configurations": len(self._results),
            "trajectories_per_config": len(self._suite),
            "top_10": [{
                "rank": i + 1,
                "ewma_alpha": r.ewma_alpha,
                "ewma_L": r.ewma_L,
                "cusum_k": r.cusum_k,
                "cusum_h": r.cusum_h,
                "detection_rate": r.detection_rate,
                "false_positive_rate": r.false_positive_rate,
                "avg_lead_time": r.avg_lead_time,
                "alerts_per_trajectory": r.alerts_per_trajectory,
                "calibration_score": r.calibration_score,
            } for i, r in enumerate(self._results[:10])],
            "all_results": [{
                "ewma_alpha": r.ewma_alpha,
                "ewma_L": r.ewma_L,
                "cusum_k": r.cusum_k,
                "cusum_h": r.cusum_h,
                "detection_rate": r.detection_rate,
                "false_positive_rate": r.false_positive_rate,
                "avg_lead_time": r.avg_lead_time,
                "calibration_score": r.calibration_score,
            } for r in self._results],
        }

        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(self._results)} results to {path}")


def main():
    """Run the calibration sweep and print top results."""
    import argparse
    parser = argparse.ArgumentParser(description="EWMA/CUSUM parameter sweep")
    parser.add_argument("--detailed", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    print("=" * 70)
    print("KALAXI DETECTOR CALIBRATION SWEEP")
    print("=" * 70)

    sweep = CalibrationSweep(seed=42)

    print(f"\nSweeping {len(sweep.EWMA_ALPHAS)} × {len(sweep.EWMA_LS)} × "
          f"{len(sweep.CUSUM_KS)} × {len(sweep.CUSUM_HS)} = "
          f"{len(sweep.EWMA_ALPHAS) * len(sweep.EWMA_LS) * len(sweep.CUSUM_KS) * len(sweep.CUSUM_HS)} configurations...")

    results = sweep.sweep()

    print(f"\nTotal configurations tested: {len(results)}")
    print(f"\nTOP 10 CONFIGURATIONS:")
    print(f"{'Rank':>4} {'Alpha':>6} {'L':>5} {'K':>6} {'H':>5} {'Det%':>6} {'FPR%':>6} {'Lead':>6} {'Score':>7}")
    print("-" * 55)

    for i, r in enumerate(sweep.top_n(10)):
        print(f"{i+1:>4} {r.ewma_alpha:>6.2f} {r.ewma_L:>5.1f} {r.cusum_k:>6.3f} {r.cusum_h:>5.2f} "
              f"{r.detection_rate*100:>5.1f}% {r.false_positive_rate*100:>5.1f}% "
              f"{r.avg_lead_time:>5.1f} {r.calibration_score:>7.4f}")

    best = results[0]
    print(f"\nBEST CONFIGURATION:")
    print(f"  EWMA: alpha={best.ewma_alpha}, L={best.ewma_L}")
    print(f"  CUSUM: k={best.cusum_k}, h={best.cusum_h}")
    print(f"  Detection rate: {best.detection_rate:.0%}")
    print(f"  False positive rate: {best.false_positive_rate:.0%}")
    print(f"  Avg lead time: {best.avg_lead_time:.1f} steps")
    print(f"  Calibration score: {best.calibration_score:.4f}")

    sweep.save_results()
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
