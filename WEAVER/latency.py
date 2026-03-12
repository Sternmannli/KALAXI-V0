#!/usr/bin/env python3
"""
latency.py — Dignity-Latency Variable (T_d)
Version: 1.0
Grounded in: FOUNDATIONS/dignity_latency.md (Structural Proposal)
Linked Covenants: COV#001 (dignity-first), COV#NEW-B (thermal delay)

The system should not respond at maximum compute velocity, but at
Biological Velocity. If an interaction is complex, the system must
simulate the "breath" of the weir.

Rules:
  1. T_d is proportional to interaction complexity
  2. T_d is a structural feature, not a performance bug
  3. T_d preserves the Breath module — the system waits
  4. T_d never exceeds donor patience (no coercive waiting)
  5. T_d is calibrated per interaction type

"A system that responds faster than a human can think has already
collapsed the human into a data point."

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import copy
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Optional
from enum import Enum


class ComplexityLevel(Enum):
    """Interaction complexity levels."""
    SIMPLE = "simple"           # Factual, short, clear
    MODERATE = "moderate"       # Multi-part, some nuance
    COMPLEX = "complex"        # Emotional, philosophical, contested
    PROFOUND = "profound"       # Identity-touching, grief, existential


@dataclass
class LatencyProfile:
    """T_d configuration for an interaction type."""
    complexity: ComplexityLevel
    min_seconds: float          # Minimum latency (floor)
    max_seconds: float          # Maximum latency (ceiling — donor patience)
    recommended_seconds: float  # Recommended latency


# Default latency profiles (calibrated per interaction type)
DEFAULT_PROFILES = {
    ComplexityLevel.SIMPLE: LatencyProfile(
        complexity=ComplexityLevel.SIMPLE,
        min_seconds=0.0,
        max_seconds=2.0,
        recommended_seconds=0.5,
    ),
    ComplexityLevel.MODERATE: LatencyProfile(
        complexity=ComplexityLevel.MODERATE,
        min_seconds=0.5,
        max_seconds=5.0,
        recommended_seconds=2.0,
    ),
    ComplexityLevel.COMPLEX: LatencyProfile(
        complexity=ComplexityLevel.COMPLEX,
        min_seconds=1.0,
        max_seconds=10.0,
        recommended_seconds=4.0,
    ),
    ComplexityLevel.PROFOUND: LatencyProfile(
        complexity=ComplexityLevel.PROFOUND,
        min_seconds=2.0,
        max_seconds=30.0,
        recommended_seconds=8.0,
    ),
}


@dataclass
class LatencyReading:
    """A single latency measurement."""
    exchange_id: str
    complexity: ComplexityLevel
    recommended_td: float
    actual_td: float
    dignity_preserved: bool     # Was T_d sufficient?
    timestamp: str


@dataclass
class LatencyState:
    """State of the latency tracker."""
    readings_count: int
    avg_complexity: str
    avg_recommended_td: float
    avg_actual_td: float
    dignity_preservation_rate: float
    violations: int             # Times system responded too fast


class DignityLatency:
    """
    Tracks and recommends dignity-preserving response latency (T_d).

    Usage:
        latency = DignityLatency()
        complexity = latency.assess_complexity("deep philosophical question")
        td = latency.recommend(complexity)
        # ... system waits td seconds ...
        latency.record(exchange_id, complexity, td, actual_response_time)
    """

    # Complexity detection patterns
    EMOTIONAL_MARKERS = [
        r'\b(frustrated|confused|worried|scared|angry|upset|lost|stuck)\b',
        r'\b(grief|mourning|loss|dying|death|pain|suffering)\b',
        r'\b(love|trust|betray|abandon|lonely|shame|guilt)\b',
    ]

    PHILOSOPHICAL_MARKERS = [
        r'\b(meaning|purpose|existence|consciousness|truth|justice)\b',
        r'\b(freedom|dignity|rights|ethics|morality|soul)\b',
        r'\b(what does it mean|why do we|what is the point)\b',
    ]

    COMPLEXITY_MARKERS = [
        r'\b(however|nevertheless|on the other hand|contradiction)\b',
        r'\b(both true|paradox|tension between|dilemma)\b',
        r'\b(if.*then.*but|although.*yet)\b',
    ]

    IDENTITY_MARKERS = [
        r'\b(who am i|my identity|my culture|my people)\b',
        r'\b(belong|homeland|roots|ancestors|heritage)\b',
        r'\b(erase|silence|invisible|forgotten|unseen)\b',
    ]

    def __init__(self, profiles: Dict[ComplexityLevel, LatencyProfile] = None):
        self._profiles = profiles or copy.deepcopy(DEFAULT_PROFILES)
        self._readings: List[LatencyReading] = []
        self._violations = 0

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def assess_complexity(self, text: str) -> ComplexityLevel:
        """
        Assess the complexity level of an input.

        Scans for emotional, philosophical, identity, and structural
        complexity markers. Higher marker density = higher complexity.
        """
        text_lower = text.lower()
        score = 0

        # Check each category of markers
        for pattern in self.EMOTIONAL_MARKERS:
            if re.search(pattern, text_lower):
                score += 2

        for pattern in self.PHILOSOPHICAL_MARKERS:
            if re.search(pattern, text_lower):
                score += 2

        for pattern in self.COMPLEXITY_MARKERS:
            if re.search(pattern, text_lower):
                score += 1

        for pattern in self.IDENTITY_MARKERS:
            if re.search(pattern, text_lower):
                score += 3  # Identity-touching gets highest weight

        # Length also contributes (longer = more complex)
        word_count = len(text.split())
        if word_count > 50:
            score += 1
        if word_count > 100:
            score += 1

        # Map score to complexity level
        if score >= 6:
            return ComplexityLevel.PROFOUND
        elif score >= 3:
            return ComplexityLevel.COMPLEX
        elif score >= 1:
            return ComplexityLevel.MODERATE
        else:
            return ComplexityLevel.SIMPLE

    def recommend(self, complexity: ComplexityLevel) -> float:
        """
        Get the recommended T_d for a given complexity level.

        Returns recommended seconds of latency.
        """
        profile = self._profiles.get(complexity, DEFAULT_PROFILES[ComplexityLevel.SIMPLE])
        return profile.recommended_seconds

    def get_profile(self, complexity: ComplexityLevel) -> LatencyProfile:
        """Get the full latency profile for a complexity level."""
        return self._profiles.get(complexity, DEFAULT_PROFILES[ComplexityLevel.SIMPLE])

    def record(self, exchange_id: str, complexity: ComplexityLevel,
               recommended_td: float, actual_td: float) -> LatencyReading:
        """
        Record a latency measurement.

        Checks if actual response time met the minimum T_d for this complexity.
        """
        profile = self._profiles.get(complexity, DEFAULT_PROFILES[ComplexityLevel.SIMPLE])

        # Dignity preserved if actual T_d >= minimum for this complexity
        dignity_preserved = actual_td >= profile.min_seconds

        if not dignity_preserved:
            self._violations += 1

        reading = LatencyReading(
            exchange_id=exchange_id,
            complexity=complexity,
            recommended_td=recommended_td,
            actual_td=actual_td,
            dignity_preserved=dignity_preserved,
            timestamp=self._now(),
        )
        self._readings.append(reading)
        return reading

    def state(self) -> LatencyState:
        """Full latency tracker state."""
        if not self._readings:
            return LatencyState(
                readings_count=0,
                avg_complexity="none",
                avg_recommended_td=0.0,
                avg_actual_td=0.0,
                dignity_preservation_rate=1.0,
                violations=0,
            )

        # Compute averages
        complexities = [r.complexity.value for r in self._readings]
        most_common = max(set(complexities), key=complexities.count)
        avg_rec = sum(r.recommended_td for r in self._readings) / len(self._readings)
        avg_act = sum(r.actual_td for r in self._readings) / len(self._readings)
        preserved = sum(1 for r in self._readings if r.dignity_preserved)
        rate = preserved / len(self._readings)

        return LatencyState(
            readings_count=len(self._readings),
            avg_complexity=most_common,
            avg_recommended_td=round(avg_rec, 2),
            avg_actual_td=round(avg_act, 2),
            dignity_preservation_rate=round(rate, 4),
            violations=self._violations,
        )

    def update_profile(self, complexity: ComplexityLevel,
                       min_seconds: float = None, max_seconds: float = None,
                       recommended_seconds: float = None):
        """Update a latency profile (calibration per interaction type)."""
        profile = self._profiles.get(complexity)
        if profile is None:
            return
        if min_seconds is not None:
            profile.min_seconds = min_seconds
        if max_seconds is not None:
            profile.max_seconds = max_seconds
        if recommended_seconds is not None:
            profile.recommended_seconds = recommended_seconds

    @property
    def violations_count(self) -> int:
        return self._violations

    @property
    def readings_count(self) -> int:
        return len(self._readings)
