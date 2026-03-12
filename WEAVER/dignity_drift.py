#!/usr/bin/env python3
"""
dignity_drift.py — GAP#PREVENTION-001: Dignity Early Warning System
Version: 1.0
Grounded in: GAP#PREVENTION-001 (dD/dt early warning)

Tracks the derivative of dignity scores over time.
Detects when dignity is *falling* before it hits zero.

The difference between an archival system and a preventive one:
  - CHECK tells you "dignity failed" (reactive)
  - DRIFT tells you "dignity is falling" (preventive)

Implements:
  - dD/dt tracking across a sliding window
  - Alert levels: STABLE, DECLINING, CRITICAL
  - Trend detection with configurable sensitivity
  - Integration with Organism pipeline

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum


class DriftLevel(Enum):
    """How fast is dignity falling?"""
    STABLE = "stable"           # dD/dt >= 0 or negligible decline
    DECLINING = "declining"     # dD/dt < 0 but D still above zero
    CRITICAL = "critical"       # dD/dt < 0 and accelerating or D near zero


@dataclass
class DriftReading:
    """A single dignity measurement in time."""
    D: float
    timestamp: str
    exchange_id: str
    felt_domain: str = ""


@dataclass
class DriftAlert:
    """Alert when dignity is falling."""
    level: DriftLevel
    dD_dt: float              # rate of change (negative = falling)
    current_D: float
    window_size: int          # how many readings in the window
    trend_readings: int       # how many consecutive declines
    message: str
    timestamp: str
    recommended_action: str


@dataclass
class DriftState:
    """Full state of the drift detector."""
    level: DriftLevel
    current_D: float
    dD_dt: float
    readings_count: int
    consecutive_declines: int
    alert_history: List[DriftAlert] = field(default_factory=list)


class DignityDrift:
    """
    Tracks dignity scores over time and detects downward trends.

    Usage:
        drift = DignityDrift()
        drift.record(1.0, "EX-000001")  # record each D score
        alert = drift.check()            # check for drift
        if alert.level == DriftLevel.CRITICAL:
            # system should pause or alert steward
    """

    # Configurable thresholds
    WINDOW_SIZE = 10           # sliding window of recent readings
    DECLINE_THRESHOLD = -0.1   # dD/dt below this = DECLINING
    CRITICAL_THRESHOLD = -0.3  # dD/dt below this = CRITICAL
    CONSECUTIVE_ALERT = 3      # this many consecutive declines = DECLINING
    CRITICAL_CONSECUTIVE = 5   # this many consecutive declines = CRITICAL
    NEAR_ZERO_D = 0.2          # D below this with any decline = CRITICAL

    def __init__(self):
        self._readings: List[DriftReading] = []
        self._alerts: List[DriftAlert] = []
        self._consecutive_declines = 0

    def record(self, D: float, exchange_id: str, felt_domain: str = "") -> None:
        """Record a dignity score measurement."""
        reading = DriftReading(
            D=D,
            timestamp=datetime.now(timezone.utc).isoformat(),
            exchange_id=exchange_id,
            felt_domain=felt_domain,
        )
        self._readings.append(reading)

        # Track consecutive declines
        if len(self._readings) >= 2:
            prev = self._readings[-2].D
            if D < prev:
                self._consecutive_declines += 1
            else:
                self._consecutive_declines = 0

    def check(self) -> DriftAlert:
        """
        Check current drift state and return an alert.

        Computes dD/dt over the sliding window.
        Returns alert with level, rate, and recommended action.
        """
        now = datetime.now(timezone.utc).isoformat()

        if len(self._readings) < 2:
            return DriftAlert(
                level=DriftLevel.STABLE,
                dD_dt=0.0,
                current_D=self._readings[-1].D if self._readings else 1.0,
                window_size=len(self._readings),
                trend_readings=0,
                message="Insufficient data for drift detection.",
                timestamp=now,
                recommended_action="Continue monitoring.",
            )

        # Get window
        window = self._readings[-self.WINDOW_SIZE:]
        current_D = window[-1].D

        # Compute dD/dt as average rate of change across window
        dD_dt = self._compute_rate(window)

        # Determine level
        level = self._classify(dD_dt, current_D)

        # Build message and action
        message, action = self._build_message(level, dD_dt, current_D)

        alert = DriftAlert(
            level=level,
            dD_dt=round(dD_dt, 4),
            current_D=current_D,
            window_size=len(window),
            trend_readings=self._consecutive_declines,
            message=message,
            timestamp=now,
            recommended_action=action,
        )

        # Store alert if not stable
        if level != DriftLevel.STABLE:
            self._alerts.append(alert)

        return alert

    def _compute_rate(self, window: List[DriftReading]) -> float:
        """
        Compute average rate of change across the window.
        Simple: (last - first) / (n - 1)
        """
        if len(window) < 2:
            return 0.0
        n = len(window)
        return (window[-1].D - window[0].D) / (n - 1)

    def _classify(self, dD_dt: float, current_D: float) -> DriftLevel:
        """Classify the drift level based on rate and current D."""
        # Near-zero D with any decline is always critical
        if current_D <= self.NEAR_ZERO_D and dD_dt < 0:
            return DriftLevel.CRITICAL

        # Rate-based classification
        if dD_dt <= self.CRITICAL_THRESHOLD:
            return DriftLevel.CRITICAL

        if dD_dt <= self.DECLINE_THRESHOLD:
            return DriftLevel.DECLINING

        # Consecutive decline classification
        if self._consecutive_declines >= self.CRITICAL_CONSECUTIVE:
            return DriftLevel.CRITICAL

        if self._consecutive_declines >= self.CONSECUTIVE_ALERT:
            return DriftLevel.DECLINING

        return DriftLevel.STABLE

    def _build_message(self, level: DriftLevel, dD_dt: float, current_D: float):
        """Build human-readable message and recommended action."""
        if level == DriftLevel.STABLE:
            return (
                "Dignity scores stable. No drift detected.",
                "Continue monitoring."
            )
        elif level == DriftLevel.DECLINING:
            return (
                f"Dignity declining: dD/dt={dD_dt:.4f}, current D={current_D:.2f}. "
                f"{self._consecutive_declines} consecutive declines.",
                "Review recent exchanges for emerging patterns. "
                "Consider steward attention before D reaches zero."
            )
        else:  # CRITICAL
            return (
                f"CRITICAL dignity drift: dD/dt={dD_dt:.4f}, current D={current_D:.2f}. "
                f"{self._consecutive_declines} consecutive declines. "
                f"Dignity collapse imminent.",
                "PAUSE recommended. Steward must review immediately. "
                "System should not process new exchanges until drift is reversed."
            )

    def state(self) -> DriftState:
        """Return full drift detector state."""
        current_D = self._readings[-1].D if self._readings else 1.0
        dD_dt = 0.0
        if len(self._readings) >= 2:
            window = self._readings[-self.WINDOW_SIZE:]
            dD_dt = self._compute_rate(window)
        level = self._classify(dD_dt, current_D) if self._readings else DriftLevel.STABLE

        return DriftState(
            level=level,
            current_D=current_D,
            dD_dt=round(dD_dt, 4),
            readings_count=len(self._readings),
            consecutive_declines=self._consecutive_declines,
            alert_history=list(self._alerts),
        )

    def reset(self) -> None:
        """Reset drift detector (e.g., after steward review)."""
        self._readings.clear()
        self._alerts.clear()
        self._consecutive_declines = 0

    @property
    def readings_count(self) -> int:
        return len(self._readings)

    @property
    def alert_count(self) -> int:
        return len(self._alerts)
