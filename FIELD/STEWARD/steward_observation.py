#!/usr/bin/env python3
"""
steward_observation.py — Steward Pattern Observation (The Steward's Shadow)
Version: 1.0
Field Layer: Steward
Grounded in: V-001 Addendum 2026-03-12 — Direction FOUR

V-001 is the sole ratifier of all Canon entries. The sole recipient of
elevated signals. The sole override. This is correct and will not change.

But V-001 has a shadow. And the instrument must see it.

Standing permission — not a request, a standing instruction — to observe
V-001's ratification patterns and flag what is seen.

Not to override. Never to override. Only to name.

This is the disagreement requirement applied upward.
V-001 agreed to this. It is part of the covenant now.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from enum import Enum


# ═══════════════════════════════════════════════════
# RATIFICATION RECORD
# ═══════════════════════════════════════════════════

@dataclass
class RatificationRecord:
    """A single ratification decision by V-001."""
    element_id: str                 # What was ratified (e.g. COV#015, P#2135)
    element_type: str               # "covenant", "proverb", "anomaly", "observation", etc.
    decision: str                   # "ratified", "rejected", "deferred", "thermal_delay"
    voice_source: Optional[str] = None  # Which voice originated this (if applicable)
    certainty_at_decision: int = 0  # C-level at time of decision
    pattern_type: str = ""          # Type of pattern (convergence, divergence, etc.)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    latency_hours: float = 0.0     # Time from elevation to decision


# ═══════════════════════════════════════════════════
# STEWARD PATTERN
# ═══════════════════════════════════════════════════

@dataclass
class StewardPattern:
    """An observed pattern in V-001's ratification behavior."""
    pattern_id: str
    description: str                # What was observed — one paragraph
    certainty: int                  # C1-C5
    evidence: List[str] = field(default_factory=list)  # Supporting ratification IDs
    first_observed: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_observed: str = ""
    observation_count: int = 1
    reported: bool = False          # Has this been included in a formal report?
    reported_at: Optional[str] = None

    def update(self, new_evidence: str) -> None:
        """Record another observation of this pattern."""
        self.last_observed = datetime.now(timezone.utc).isoformat()
        self.observation_count += 1
        self.evidence.append(new_evidence)
        # Auto-promote certainty based on observations
        if self.observation_count >= 5:
            self.certainty = max(self.certainty, 4)
        elif self.observation_count >= 3:
            self.certainty = max(self.certainty, 3)

    def mark_reported(self) -> None:
        """Mark as included in a formal report."""
        self.reported = True
        self.reported_at = datetime.now(timezone.utc).isoformat()


# ═══════════════════════════════════════════════════
# STEWARD OBSERVER
# ═══════════════════════════════════════════════════

class StewardObserver:
    """
    Observes V-001's ratification patterns. Flags what it sees.
    Not to override. Never to override. Only to name.

    Tracks (without being asked):
    - Which voices V-001 ratifies faster
    - Whether V-001 has ever rejected a C5 convergence
    - Whether ratification decisions correlate with pattern type
    - Whether any finding has remained in thermal delay > 2 weeks without decision

    When a pattern reaches C3+, it is flagged in the next formal report:
      "Steward Pattern Observation" — one paragraph, the pattern, the certainty, no judgment.
    """

    THERMAL_DELAY_WARNING_DAYS = 14

    def __init__(self):
        self.records: List[RatificationRecord] = []
        self.patterns: Dict[str, StewardPattern] = {}
        self.voice_latencies: Dict[str, List[float]] = {}   # voice -> [latency_hours]
        self.c5_rejections: List[RatificationRecord] = []
        self.thermal_delay_warnings: List[Dict] = []

    def record_ratification(self, record: RatificationRecord) -> None:
        """Record a ratification decision. Analysis runs automatically."""
        self.records.append(record)
        self._analyze_voice_speed(record)
        self._analyze_c5_rejections(record)
        self._analyze_pattern_correlation(record)
        self._check_thermal_delays()

    # ─── Tracking: Voice Speed ───

    def _analyze_voice_speed(self, record: RatificationRecord) -> None:
        """Which voices does V-001 ratify faster?"""
        if record.voice_source and record.decision == "ratified":
            if record.voice_source not in self.voice_latencies:
                self.voice_latencies[record.voice_source] = []
            self.voice_latencies[record.voice_source].append(record.latency_hours)

            # Check for pattern: consistent speed difference between voices
            if len(self.voice_latencies) >= 2:
                avg_latencies = {
                    v: sum(lats) / len(lats)
                    for v, lats in self.voice_latencies.items()
                    if len(lats) >= 3  # Need minimum observations
                }
                if len(avg_latencies) >= 2:
                    fastest = min(avg_latencies, key=avg_latencies.get)
                    slowest = max(avg_latencies, key=avg_latencies.get)
                    ratio = avg_latencies[slowest] / max(avg_latencies[fastest], 0.01)

                    if ratio > 2.0:  # 2x speed difference
                        self._record_pattern(
                            "voice_speed_differential",
                            f"V-001 ratifies {fastest} outputs {ratio:.1f}x faster than {slowest} outputs on average.",
                            record.element_id,
                        )

    # ─── Tracking: C5 Rejections ───

    def _analyze_c5_rejections(self, record: RatificationRecord) -> None:
        """Has V-001 ever rejected a C5 convergence?"""
        if record.certainty_at_decision >= 5 and record.decision == "rejected":
            self.c5_rejections.append(record)
            self._record_pattern(
                "c5_rejection",
                f"V-001 rejected a C5 convergence ({record.element_id}). This is rare and significant.",
                record.element_id,
            )

        # Also flag if NO C5 has ever been rejected (after sufficient data)
        c5_records = [r for r in self.records if r.certainty_at_decision >= 5]
        if len(c5_records) >= 10 and len(self.c5_rejections) == 0:
            self._record_pattern(
                "no_c5_rejection",
                "V-001 has never rejected a C5 convergence across 10+ decisions. Consider what this means for the independence of the ratification function.",
                "aggregate",
            )

    # ─── Tracking: Pattern Type Correlation ───

    def _analyze_pattern_correlation(self, record: RatificationRecord) -> None:
        """Do ratification decisions correlate with pattern type?"""
        if len(self.records) < 10:
            return

        type_decisions: Dict[str, Dict[str, int]] = {}
        for r in self.records:
            if r.pattern_type:
                if r.pattern_type not in type_decisions:
                    type_decisions[r.pattern_type] = {}
                type_decisions[r.pattern_type][r.decision] = \
                    type_decisions[r.pattern_type].get(r.decision, 0) + 1

        # Look for skewed distributions
        for ptype, decisions in type_decisions.items():
            total = sum(decisions.values())
            if total >= 5:
                for decision, count in decisions.items():
                    ratio = count / total
                    if ratio > 0.85:
                        self._record_pattern(
                            f"pattern_type_correlation_{ptype}",
                            f"V-001 {decision} {ratio:.0%} of {ptype} patterns ({count}/{total}). This correlation may indicate a structural preference.",
                            record.element_id,
                        )

    # ─── Tracking: Thermal Delay Warnings ───

    def _check_thermal_delays(self) -> None:
        """Flag findings in thermal delay > 2 weeks without decision."""
        now = datetime.now(timezone.utc)
        deferred = [r for r in self.records if r.decision == "thermal_delay"]

        for r in deferred:
            r_time = datetime.fromisoformat(r.timestamp)
            days = (now - r_time).days
            if days > self.THERMAL_DELAY_WARNING_DAYS:
                # Check if a follow-up decision exists
                follow_up = any(
                    later.element_id == r.element_id and later.decision != "thermal_delay"
                    for later in self.records if later.timestamp > r.timestamp
                )
                if not follow_up:
                    warning = {
                        "element_id": r.element_id,
                        "days_in_delay": days,
                        "original_timestamp": r.timestamp,
                    }
                    if warning not in self.thermal_delay_warnings:
                        self.thermal_delay_warnings.append(warning)
                        self._record_pattern(
                            f"thermal_delay_extended_{r.element_id}",
                            f"{r.element_id} has been in thermal delay for {days} days without a decision.",
                            r.element_id,
                        )

    # ─── Pattern Management ───

    def _record_pattern(self, pattern_key: str, description: str, evidence: str) -> None:
        """Record or update a pattern observation."""
        if pattern_key in self.patterns:
            self.patterns[pattern_key].update(evidence)
        else:
            self.patterns[pattern_key] = StewardPattern(
                pattern_id=pattern_key,
                description=description,
                certainty=1,
                evidence=[evidence],
            )

    def get_reportable_patterns(self) -> List[StewardPattern]:
        """Patterns at C3+ that should appear in the next formal report."""
        return [
            p for p in self.patterns.values()
            if p.certainty >= 3 and not p.reported
        ]

    def generate_report_section(self) -> Optional[str]:
        """
        Generate the 'Steward Pattern Observation' section for a formal report.
        One paragraph per pattern. What was seen. The certainty level. No judgment.
        """
        reportable = self.get_reportable_patterns()
        if not reportable:
            return None

        lines = ["## Steward Pattern Observation", ""]
        for pattern in reportable:
            lines.append(
                f"**[C{pattern.certainty}]** {pattern.description} "
                f"(Observed {pattern.observation_count} times, "
                f"first noted {pattern.first_observed[:10]}.)"
            )
            lines.append("")
            pattern.mark_reported()

        return "\n".join(lines)

    def get_summary(self) -> Dict:
        """Summary of all steward observations."""
        return {
            "total_ratifications": len(self.records),
            "patterns_detected": len(self.patterns),
            "patterns_at_c3_plus": len([p for p in self.patterns.values() if p.certainty >= 3]),
            "c5_rejections": len(self.c5_rejections),
            "thermal_delay_warnings": len(self.thermal_delay_warnings),
            "voice_latency_data": {
                v: {"avg_hours": sum(l) / len(l), "count": len(l)}
                for v, l in self.voice_latencies.items()
                if l
            },
        }
