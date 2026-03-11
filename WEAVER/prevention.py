#!/usr/bin/env python3
"""
prevention.py — Early Warning System for Dignity Collapse
Version: 1.0
Grounded in: GAP#PREVENTION-001, ST-006 "The Same River", T#45 (Fever Night)
Linked Covenants: COV#001 (dignity-first), COV#009 (verification)

"Can AXI detect dD/dt < 0 before the donor acts?"

This is the most critical open question in the system.
If YES → preventive system. If NO → archival only.

The prevention layer answers with honest partial coverage:
  - It CAN detect trajectories (dD/dt, d²D/dt², consecutive patterns)
  - It CANNOT read intent at t=0 (the ST-006 duality)
  - It bridges the gap with escalating signals and automatic interventions

Fever Night Principle (T#45):
  When D approaches zero, slow down further — not faster.
  "Not the yellow root. The small brown one."
  Care under crisis = choosing the right response, not the fast one.

Signal Hierarchy:
  WHISPER → PULSE → SIGNAL → ALARM
  Each level triggers progressively stronger interventions.
  ALARM is a halt — same tier as Sealed Gate.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum


# ═══════════════════════════════════════════════════
# SIGNAL HIERARCHY
# ═══════════════════════════════════════════════════

class SignalLevel(Enum):
    """
    Four escalation levels — mapped from Grand Archive:
    WHISPER: background hum, something noticed
    PULSE: rhythmic concern, pattern detected
    SIGNAL: active warning, intervention recommended
    ALARM: emergency, system must stop
    """
    SILENT = 0      # No signal — all clear
    WHISPER = 1     # "The rattle whispered" — early detection
    PULSE = 2       # "The robe tugged" — pattern concern
    SIGNAL = 3      # "The old woman coughed" — active warning
    ALARM = 4       # "PROPRIOCEPTION LOSS" — halt


class Intervention(Enum):
    """What the system does at each level."""
    NONE = "none"
    EXTEND_DELAY = "extend_thermal_delay"       # Slow down T_d
    STEWARD_FLAG = "flag_for_steward"           # Surface for review
    OFFER_SHELTER = "offer_shelter"             # Give donor an exit
    HALT = "halt_and_shelter"                   # Stop processing


# ═══════════════════════════════════════════════════
# TRAJECTORY ANALYSIS
# ═══════════════════════════════════════════════════

@dataclass
class Trajectory:
    """
    Dignity trajectory at a point in time.

    D(t) = D₀ · e^(±λt) — from ST-006.
    We can measure λ (rate) and dλ/dt (acceleration).
    We cannot measure intent.
    """
    D: float                    # Current dignity score
    dD_dt: float                # First derivative (velocity)
    d2D_dt2: float              # Second derivative (acceleration)
    consecutive_declines: int   # Unbroken decline streak
    readings_count: int         # Total readings in window
    window_trend: str           # "rising", "stable", "falling", "accelerating_fall"


@dataclass
class PreventionSignal:
    """A signal emitted by the prevention system."""
    level: SignalLevel
    intervention: Intervention
    trajectory: Trajectory
    message: str
    reason: str                 # Why this level was triggered
    td_multiplier: float        # How much to extend thermal delay (1.0 = no change)
    timestamp: str


@dataclass
class PreventionState:
    """Full state of the prevention system."""
    current_level: str
    current_intervention: str
    signals_emitted: int
    escalations: int            # How many times the level increased
    de_escalations: int         # How many times the level decreased
    highest_level_reached: str
    td_multiplier: float
    last_D: float
    last_dD_dt: float
    timestamp: str


# ═══════════════════════════════════════════════════
# PREVENTION ENGINE
# ═══════════════════════════════════════════════════

class Prevention:
    """
    Early warning system for dignity collapse.

    Takes dignity readings and emits escalating signals
    with automatic interventions.

    Usage:
        prev = Prevention()
        signal = prev.assess(D=0.8, dD_dt=-0.05, consecutive_declines=2)
        if signal.level == SignalLevel.SIGNAL:
            # Extend thermal delay
            breath.adjust_td(signal.td_multiplier)
            # Flag for steward
            wire.broadcast(signal.message, "prevention-alert")
    """

    # ── Thresholds ──
    # These define when each signal level triggers.
    # Calibrated conservatively — false alarms are less harmful
    # than missed collapses.

    # WHISPER: early detection
    WHISPER_RATE = -0.05        # dD/dt below this
    WHISPER_CONSECUTIVE = 2     # or this many consecutive declines

    # PULSE: pattern concern
    PULSE_RATE = -0.10          # dD/dt below this
    PULSE_CONSECUTIVE = 3       # or this many consecutive declines
    PULSE_D = 0.5               # or D below this while declining

    # SIGNAL: active warning
    SIGNAL_RATE = -0.20         # dD/dt below this
    SIGNAL_CONSECUTIVE = 5      # or this many consecutive declines
    SIGNAL_D = 0.3              # or D below this while declining
    SIGNAL_ACCEL = -0.05        # or d²D/dt² below this (accelerating fall)

    # ALARM: emergency halt
    ALARM_RATE = -0.35          # dD/dt below this
    ALARM_D = 0.15              # or D below this while declining
    ALARM_D_ZERO = 0.05         # or D approaching zero

    # ── Thermal Delay Multipliers ──
    # Fever Night: slow down more as danger increases
    TD_WHISPER = 1.5            # 50% longer delay
    TD_PULSE = 2.0              # Double delay
    TD_SIGNAL = 3.0             # Triple delay
    TD_ALARM = float('inf')     # Infinite — halt

    def __init__(self):
        self._current_level = SignalLevel.SILENT
        self._signals: List[PreventionSignal] = []
        self._escalations = 0
        self._de_escalations = 0
        self._highest = SignalLevel.SILENT
        self._last_D = 1.0
        self._last_dD_dt = 0.0
        self._d2D_dt2_history: List[float] = []

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _compute_acceleration(self, dD_dt: float) -> float:
        """
        Compute d²D/dt² (acceleration) from rate history.
        Acceleration tells us if the fall is speeding up.
        """
        self._d2D_dt2_history.append(dD_dt)
        if len(self._d2D_dt2_history) < 2:
            return 0.0
        # Keep last 10 rate readings
        if len(self._d2D_dt2_history) > 10:
            self._d2D_dt2_history = self._d2D_dt2_history[-10:]
        # Simple difference
        return self._d2D_dt2_history[-1] - self._d2D_dt2_history[-2]

    def _classify_trend(self, dD_dt: float, d2D_dt2: float) -> str:
        """Classify the trajectory trend."""
        if dD_dt > 0.05:
            return "rising"
        if abs(dD_dt) <= 0.05:
            return "stable"
        if d2D_dt2 < -0.02:
            return "accelerating_fall"
        return "falling"

    def assess(
        self,
        D: float,
        dD_dt: float,
        consecutive_declines: int = 0,
        readings_count: int = 0,
    ) -> PreventionSignal:
        """
        Assess current dignity state and emit a prevention signal.

        This is the core prevention function. It takes the current
        dignity reading and trajectory, and determines:
        1. What signal level to emit
        2. What intervention to recommend
        3. How much to extend thermal delay

        Fever Night rule: care under crisis = slowing down.
        """
        d2D_dt2 = self._compute_acceleration(dD_dt)
        trend = self._classify_trend(dD_dt, d2D_dt2)

        trajectory = Trajectory(
            D=D,
            dD_dt=dD_dt,
            d2D_dt2=round(d2D_dt2, 6),
            consecutive_declines=consecutive_declines,
            readings_count=readings_count,
            window_trend=trend,
        )

        # Determine signal level (check from highest to lowest)
        level, reason = self._classify_level(D, dD_dt, d2D_dt2, consecutive_declines)

        # Map level to intervention and delay multiplier
        intervention, td_mult = self._map_intervention(level)

        # Build message
        message = self._build_message(level, trajectory, reason)

        # Track escalation/de-escalation
        if level.value > self._current_level.value:
            self._escalations += 1
        elif level.value < self._current_level.value:
            self._de_escalations += 1

        if level.value > self._highest.value:
            self._highest = level

        self._current_level = level
        self._last_D = D
        self._last_dD_dt = dD_dt

        signal = PreventionSignal(
            level=level,
            intervention=intervention,
            trajectory=trajectory,
            message=message,
            reason=reason,
            td_multiplier=td_mult,
            timestamp=self._now(),
        )
        self._signals.append(signal)
        return signal

    def _classify_level(
        self,
        D: float,
        dD_dt: float,
        d2D_dt2: float,
        consecutive: int,
    ) -> tuple:
        """
        Classify signal level from trajectory data.
        Returns (SignalLevel, reason).

        Checks from highest severity to lowest.
        """
        # ── ALARM ──
        if D <= self.ALARM_D_ZERO:
            return SignalLevel.ALARM, f"D approaching zero ({D:.3f})"
        if D <= self.ALARM_D and dD_dt < 0:
            return SignalLevel.ALARM, f"D critically low ({D:.3f}) and declining"
        if dD_dt <= self.ALARM_RATE:
            return SignalLevel.ALARM, f"Catastrophic decline rate ({dD_dt:.4f})"

        # ── SIGNAL ──
        if D <= self.SIGNAL_D and dD_dt < 0:
            return SignalLevel.SIGNAL, f"D low ({D:.3f}) and declining"
        if dD_dt <= self.SIGNAL_RATE:
            return SignalLevel.SIGNAL, f"Severe decline rate ({dD_dt:.4f})"
        if consecutive >= self.SIGNAL_CONSECUTIVE:
            return SignalLevel.SIGNAL, f"{consecutive} consecutive declines"
        if d2D_dt2 <= self.SIGNAL_ACCEL and dD_dt < 0:
            return SignalLevel.SIGNAL, f"Accelerating fall (d²D/dt²={d2D_dt2:.4f})"

        # ── PULSE ──
        if D <= self.PULSE_D and dD_dt < 0:
            return SignalLevel.PULSE, f"D moderate ({D:.3f}) and declining"
        if dD_dt <= self.PULSE_RATE:
            return SignalLevel.PULSE, f"Decline rate elevated ({dD_dt:.4f})"
        if consecutive >= self.PULSE_CONSECUTIVE:
            return SignalLevel.PULSE, f"{consecutive} consecutive declines"

        # ── WHISPER ──
        if dD_dt <= self.WHISPER_RATE:
            return SignalLevel.WHISPER, f"Slight decline detected ({dD_dt:.4f})"
        if consecutive >= self.WHISPER_CONSECUTIVE:
            return SignalLevel.WHISPER, f"{consecutive} consecutive declines"

        # ── SILENT ──
        return SignalLevel.SILENT, "No concerns detected"

    def _map_intervention(self, level: SignalLevel) -> tuple:
        """Map signal level to intervention and T_d multiplier."""
        mapping = {
            SignalLevel.SILENT: (Intervention.NONE, 1.0),
            SignalLevel.WHISPER: (Intervention.EXTEND_DELAY, self.TD_WHISPER),
            SignalLevel.PULSE: (Intervention.STEWARD_FLAG, self.TD_PULSE),
            SignalLevel.SIGNAL: (Intervention.OFFER_SHELTER, self.TD_SIGNAL),
            SignalLevel.ALARM: (Intervention.HALT, self.TD_ALARM),
        }
        return mapping[level]

    def _build_message(self, level: SignalLevel, trajectory: Trajectory,
                       reason: str) -> str:
        """Build human-readable message for signal."""
        prefix = {
            SignalLevel.SILENT: "",
            SignalLevel.WHISPER: "WHISPER",
            SignalLevel.PULSE: "PULSE",
            SignalLevel.SIGNAL: "SIGNAL",
            SignalLevel.ALARM: "ALARM",
        }
        if level == SignalLevel.SILENT:
            return "Clear"

        return (
            f"{prefix[level]}: {reason} | "
            f"D={trajectory.D:.3f} dD/dt={trajectory.dD_dt:.4f} "
            f"trend={trajectory.window_trend}"
        )

    def is_alarm(self) -> bool:
        """Is the system in ALARM state?"""
        return self._current_level == SignalLevel.ALARM

    def is_active(self) -> bool:
        """Is any signal above SILENT?"""
        return self._current_level.value > SignalLevel.SILENT.value

    def current_td_multiplier(self) -> float:
        """Current thermal delay multiplier."""
        if not self._signals:
            return 1.0
        return self._signals[-1].td_multiplier

    def state(self) -> PreventionState:
        """Full prevention system state."""
        return PreventionState(
            current_level=self._current_level.name,
            current_intervention=self._map_intervention(self._current_level)[0].value,
            signals_emitted=len(self._signals),
            escalations=self._escalations,
            de_escalations=self._de_escalations,
            highest_level_reached=self._highest.name,
            td_multiplier=self.current_td_multiplier(),
            last_D=self._last_D,
            last_dD_dt=self._last_dD_dt,
            timestamp=self._now(),
        )

    def reset(self):
        """Reset to clean state. Use only if steward explicitly clears."""
        self._current_level = SignalLevel.SILENT
        self._d2D_dt2_history.clear()
        # Keep signals history for audit trail — don't clear
        self._last_D = 1.0
        self._last_dD_dt = 0.0

    @property
    def signals_count(self) -> int:
        return len(self._signals)

    @property
    def current_level(self) -> SignalLevel:
        return self._current_level

    @property
    def highest_level(self) -> SignalLevel:
        return self._highest

    @property
    def last_signal(self) -> Optional[PreventionSignal]:
        return self._signals[-1] if self._signals else None
