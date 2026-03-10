#!/usr/bin/env python3
"""
sip.py — Symmetric Integration Protocol (SIP)
Version: 1.0
Grounded in: KALAXI_B §SIP

Measures whether the KALAXI system is integrating symmetrically —
that no component dominates, no voice is silenced, no module
accumulates power at the expense of others.

Three metrics:
  WVPS — Weighted Voice Participation Score (≥0.90 required)
    Are all modules contributing? Is any module silent?

  GDI — Governance Distribution Index (≥0.85 required)
    Is decision-making distributed? Is any module hoarding control?

  HSR — Harmony-Stress Ratio (≥0.95 required)
    Is the system in harmony or under stress? Are stress levels
    distributed evenly or concentrated?

All three must meet threshold for SIP compliance.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Optional


# SIP Thresholds (from spec)
WVPS_THRESHOLD = 0.90
GDI_THRESHOLD = 0.85
HSR_THRESHOLD = 0.95

# The 9 core modules
CORE_MODULES = ["CHECK", "FACE", "KEEP", "WIRE", "BREATH", "SAY", "OUT", "TURN", "WEAVE"]


@dataclass
class ModuleVoice:
    """Participation record for a single module."""
    module_name: str
    messages_sent: int = 0
    messages_received: int = 0
    decisions_made: int = 0
    decisions_deferred: int = 0
    stress_events: int = 0
    last_active: str = ""


@dataclass
class WVPSResult:
    """Weighted Voice Participation Score."""
    score: float
    passed: bool
    module_scores: Dict[str, float]
    silent_modules: List[str]
    dominant_modules: List[str]


@dataclass
class GDIResult:
    """Governance Distribution Index."""
    score: float
    passed: bool
    entropy: float
    max_entropy: float
    concentration: Dict[str, float]


@dataclass
class HSRResult:
    """Harmony-Stress Ratio."""
    score: float
    passed: bool
    harmony_score: float
    stress_score: float
    stress_distribution: Dict[str, float]


@dataclass
class SIPResult:
    """Full SIP compliance result."""
    compliant: bool
    wvps: WVPSResult
    gdi: GDIResult
    hsr: HSRResult
    timestamp: str
    notes: List[str] = field(default_factory=list)

    def summary(self) -> str:
        status = "COMPLIANT" if self.compliant else "NON-COMPLIANT"
        lines = [
            f"SIP {status}",
            f"  WVPS: {self.wvps.score:.4f} {'PASS' if self.wvps.passed else 'FAIL'} (≥{WVPS_THRESHOLD})",
            f"  GDI:  {self.gdi.score:.4f} {'PASS' if self.gdi.passed else 'FAIL'} (≥{GDI_THRESHOLD})",
            f"  HSR:  {self.hsr.score:.4f} {'PASS' if self.hsr.passed else 'FAIL'} (≥{HSR_THRESHOLD})",
        ]
        if self.wvps.silent_modules:
            lines.append(f"  Silent modules: {', '.join(self.wvps.silent_modules)}")
        if self.wvps.dominant_modules:
            lines.append(f"  Dominant modules: {', '.join(self.wvps.dominant_modules)}")
        return "\n".join(lines)


class SIPEvaluator:
    """
    Evaluates symmetric integration across the organism.

    Usage:
        sip = SIPEvaluator()
        sip.record_activity("WIRE", messages_sent=5, messages_received=3)
        sip.record_activity("CHECK", decisions_made=2)
        sip.record_activity("BREATH", stress_events=1)
        ...
        result = sip.evaluate()
    """

    def __init__(self):
        self._voices: Dict[str, ModuleVoice] = {
            m: ModuleVoice(module_name=m) for m in CORE_MODULES
        }

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def record_activity(self, module_name: str, messages_sent: int = 0,
                        messages_received: int = 0, decisions_made: int = 0,
                        decisions_deferred: int = 0, stress_events: int = 0):
        """Record activity for a module."""
        if module_name not in self._voices:
            self._voices[module_name] = ModuleVoice(module_name=module_name)

        v = self._voices[module_name]
        v.messages_sent += messages_sent
        v.messages_received += messages_received
        v.decisions_made += decisions_made
        v.decisions_deferred += decisions_deferred
        v.stress_events += stress_events
        v.last_active = self._now()

    def compute_wvps(self) -> WVPSResult:
        """
        Weighted Voice Participation Score.

        Measures whether all modules are participating.
        Perfect score = all modules equally active.
        """
        activities = {}
        for name, v in self._voices.items():
            total = v.messages_sent + v.messages_received + v.decisions_made
            activities[name] = total

        total_activity = sum(activities.values())
        if total_activity == 0:
            # No activity — all modules equally silent (score = 1.0 if all at 0)
            return WVPSResult(
                score=1.0, passed=True,
                module_scores={m: 0.0 for m in self._voices},
                silent_modules=list(self._voices.keys()),
                dominant_modules=[],
            )

        # Compute participation share for each module
        n = len(self._voices)
        expected_share = 1.0 / n if n > 0 else 0
        module_scores = {}
        for name, activity in activities.items():
            share = activity / total_activity if total_activity > 0 else 0
            module_scores[name] = round(share, 4)

        # WVPS = 1 - mean absolute deviation from expected share
        deviations = [abs(share - expected_share) for share in module_scores.values()]
        mean_deviation = sum(deviations) / len(deviations) if deviations else 0
        # Normalize: max deviation = (n-1)/n ≈ 0.89 for 9 modules
        max_possible_deviation = (n - 1) / n if n > 1 else 1
        normalized_deviation = mean_deviation / max_possible_deviation if max_possible_deviation > 0 else 0
        wvps = round(1.0 - normalized_deviation, 4)

        # Identify silent and dominant modules
        silent = [m for m, s in module_scores.items() if s == 0 and total_activity > 0]
        dominant = [m for m, s in module_scores.items() if s > expected_share * 3]

        return WVPSResult(
            score=wvps,
            passed=wvps >= WVPS_THRESHOLD,
            module_scores=module_scores,
            silent_modules=silent,
            dominant_modules=dominant,
        )

    def compute_gdi(self) -> GDIResult:
        """
        Governance Distribution Index.

        Uses Shannon entropy of decision-making across modules.
        Higher entropy = more distributed governance.
        """
        decisions = {}
        for name, v in self._voices.items():
            decisions[name] = v.decisions_made + v.decisions_deferred

        total_decisions = sum(decisions.values())
        if total_decisions == 0:
            return GDIResult(
                score=1.0, passed=True,
                entropy=0.0, max_entropy=0.0,
                concentration={m: 0.0 for m in self._voices},
            )

        # Shannon entropy
        n = len(decisions)
        probabilities = [d / total_decisions for d in decisions.values() if d > 0]
        entropy = -sum(p * math.log2(p) for p in probabilities) if probabilities else 0
        max_entropy = math.log2(n) if n > 0 else 0

        # Normalize to [0, 1]
        gdi = round(entropy / max_entropy if max_entropy > 0 else 0, 4)

        # Concentration
        concentration = {
            name: round(d / total_decisions, 4) if total_decisions > 0 else 0
            for name, d in decisions.items()
        }

        return GDIResult(
            score=gdi,
            passed=gdi >= GDI_THRESHOLD,
            entropy=round(entropy, 4),
            max_entropy=round(max_entropy, 4),
            concentration=concentration,
        )

    def compute_hsr(self) -> HSRResult:
        """
        Harmony-Stress Ratio.

        Ratio of total activity to stress events.
        High ratio = mostly harmony, little stress.
        """
        total_activity = 0
        total_stress = 0
        stress_dist = {}

        for name, v in self._voices.items():
            activity = v.messages_sent + v.messages_received + v.decisions_made
            total_activity += activity
            total_stress += v.stress_events
            stress_dist[name] = v.stress_events

        if total_activity == 0 and total_stress == 0:
            return HSRResult(
                score=1.0, passed=True,
                harmony_score=1.0, stress_score=0.0,
                stress_distribution={m: 0 for m in self._voices},
            )

        # HSR = activity / (activity + stress * weight)
        # Stress is weighted more heavily
        stress_weight = 5.0
        denominator = total_activity + (total_stress * stress_weight)
        hsr = round(total_activity / denominator if denominator > 0 else 0, 4)

        return HSRResult(
            score=hsr,
            passed=hsr >= HSR_THRESHOLD,
            harmony_score=round(total_activity / (total_activity + 1), 4),
            stress_score=round(total_stress / (total_activity + 1), 4),
            stress_distribution=stress_dist,
        )

    def evaluate(self) -> SIPResult:
        """Run full SIP evaluation."""
        wvps = self.compute_wvps()
        gdi = self.compute_gdi()
        hsr = self.compute_hsr()

        compliant = wvps.passed and gdi.passed and hsr.passed

        notes = []
        if not wvps.passed:
            notes.append(f"WVPS below threshold: {wvps.score:.4f} < {WVPS_THRESHOLD}")
        if not gdi.passed:
            notes.append(f"GDI below threshold: {gdi.score:.4f} < {GDI_THRESHOLD}")
        if not hsr.passed:
            notes.append(f"HSR below threshold: {hsr.score:.4f} < {HSR_THRESHOLD}")
        if wvps.silent_modules:
            notes.append(f"Silent modules detected: {', '.join(wvps.silent_modules)}")

        return SIPResult(
            compliant=compliant,
            wvps=wvps,
            gdi=gdi,
            hsr=hsr,
            timestamp=self._now(),
            notes=notes,
        )

    def reset(self):
        """Reset all module activity records."""
        self._voices = {
            m: ModuleVoice(module_name=m) for m in CORE_MODULES
        }
