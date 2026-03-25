#!/usr/bin/env python3
"""
drift_detector.py — Sliding-window drift detector for composite scores.
Tracks a value D (product of N components) over time.
Computes first and second derivatives. Classifies trend. Persists to disk.
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Dict
from enum import Enum


class Level(Enum):
    STABLE = "stable"
    DECLINING = "declining"
    CRITICAL = "critical"


@dataclass
class Reading:
    value: float
    components: Dict[str, float]
    timestamp: str
    source_id: str


@dataclass
class Alert:
    level: Level
    rate: float
    acceleration: float
    current: float
    window_size: int
    consecutive_declines: int
    component_rates: Dict[str, float]
    timestamp: str


class DriftDetector:
    """
    Sliding-window drift detector for a composite score.

    Usage:
        d = DriftDetector(components=["A", "L", "M"], path="data/drift.json")
        d.record(0.85, {"A": 0.9, "L": 0.8, "M": 1.0}, "TX-001")
        alert = d.check()
        if alert.level == Level.CRITICAL:
            print(f"Rate: {alert.rate}, Accel: {alert.acceleration}")
    """

    def __init__(
        self,
        components: List[str],
        path: str = "drift_state.json",
        window: int = 10,
        decline_threshold: float = -0.1,
        critical_threshold: float = -0.3,
        consec_warn: int = 3,
        consec_crit: int = 5,
        floor: float = 0.2,
    ):
        self._components = components
        self._path = path
        self._window = window
        self._decline_threshold = decline_threshold
        self._critical_threshold = critical_threshold
        self._consec_warn = consec_warn
        self._consec_crit = consec_crit
        self._floor = floor
        self._readings: List[Reading] = []
        self._consec: int = 0
        self._comp_consec: Dict[str, int] = {c: 0 for c in components}
        self._load()

    def record(self, value: float, components: Dict[str, float], source_id: str) -> None:
        r = Reading(value=value, components=components,
                    timestamp=datetime.now(timezone.utc).isoformat(), source_id=source_id)
        self._readings.append(r)
        if len(self._readings) >= 2:
            prev = self._readings[-2]
            self._consec = self._consec + 1 if value < prev.value else 0
            for c in self._components:
                if c in components and c in prev.components:
                    self._comp_consec[c] = self._comp_consec[c] + 1 if components[c] < prev.components[c] else 0
        self._save()

    def check(self) -> Alert:
        now = datetime.now(timezone.utc).isoformat()
        if len(self._readings) < 2:
            return Alert(Level.STABLE, 0.0, 0.0,
                         self._readings[-1].value if self._readings else 1.0,
                         len(self._readings), 0, {}, now)
        win = self._readings[-self._window:]
        cur = win[-1].value
        rate = self._rate([r.value for r in win])
        accel = self._accel([r.value for r in win])
        comp_rates = {}
        for c in self._components:
            vals = [r.components[c] for r in win if c in r.components]
            comp_rates[c] = self._rate(vals)
        level = self._classify(rate, accel, cur)
        for c in self._components:
            cl = self._classify(comp_rates.get(c, 0), 0, cur)
            if cl == Level.CRITICAL and level == Level.STABLE:
                level = Level.DECLINING
        return Alert(level, round(rate, 4), round(accel, 4), cur,
                     len(win), self._consec, comp_rates, now)

    def _rate(self, vals: List[float]) -> float:
        if len(vals) < 2:
            return 0.0
        return (vals[-1] - vals[0]) / (len(vals) - 1)

    def _accel(self, vals: List[float]) -> float:
        if len(vals) < 4:
            return 0.0
        mid = len(vals) // 2
        return self._rate(vals[mid:]) - self._rate(vals[:mid])

    def _classify(self, rate: float, accel: float, current: float) -> Level:
        if current <= self._floor and rate < 0:
            return Level.CRITICAL
        if rate <= self._critical_threshold:
            return Level.CRITICAL
        if rate <= self._decline_threshold and accel < 0:
            return Level.CRITICAL
        if rate <= self._decline_threshold:
            return Level.DECLINING
        if self._consec >= self._consec_crit:
            return Level.CRITICAL
        if self._consec >= self._consec_warn:
            return Level.DECLINING
        return Level.STABLE

    def _load(self) -> None:
        if not os.path.exists(self._path):
            return
        try:
            with open(self._path) as f:
                d = json.load(f)
            self._readings = [Reading(**r) for r in d.get("readings", [])]
            self._consec = d.get("consec", 0)
            self._comp_consec = d.get("comp_consec", self._comp_consec)
        except (json.JSONDecodeError, TypeError, KeyError):
            pass

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)
        with open(self._path, "w") as f:
            json.dump({"readings": [r.__dict__ for r in self._readings],
                        "consec": self._consec, "comp_consec": self._comp_consec}, f)

    def reset(self) -> None:
        self._readings.clear()
        self._consec = 0
        self._comp_consec = {c: 0 for c in self._components}
        self._save()

    @property
    def count(self) -> int:
        return len(self._readings)
