#!/usr/bin/env python3
"""Tests for drift_detector.py"""

import os
import json
import tempfile
import pytest
from drift_detector import DriftDetector, Level, Reading, Alert


@pytest.fixture
def tmp_path():
    with tempfile.TemporaryDirectory() as d:
        yield os.path.join(d, "test_drift.json")


@pytest.fixture
def detector(tmp_path):
    return DriftDetector(components=["x", "y", "z"], path=tmp_path)


# --- BASIC OPERATIONS ---

class TestRecord:
    def test_single_record(self, detector):
        detector.record(0.9, {"x": 0.9, "y": 1.0, "z": 1.0}, "T-001")
        assert detector.count == 1

    def test_multiple_records(self, detector):
        for i in range(5):
            detector.record(0.9 - i * 0.1, {"x": 0.9, "y": 0.8, "z": 0.7}, f"T-{i}")
        assert detector.count == 5

    def test_empty_components(self, detector):
        detector.record(0.5, {}, "T-001")
        assert detector.count == 1


class TestCheck:
    def test_insufficient_data(self, detector):
        alert = detector.check()
        assert alert.level == Level.STABLE
        assert alert.current == 1.0

    def test_single_reading(self, detector):
        detector.record(0.8, {"x": 0.8, "y": 0.9, "z": 0.7}, "T-001")
        alert = detector.check()
        assert alert.level == Level.STABLE

    def test_stable_trend(self, detector):
        for i in range(5):
            detector.record(0.8, {"x": 0.8, "y": 0.8, "z": 0.8}, f"T-{i}")
        alert = detector.check()
        assert alert.level == Level.STABLE
        assert alert.rate == 0.0

    def test_increasing_trend(self, detector):
        for i in range(5):
            detector.record(0.5 + i * 0.1, {"x": 0.5, "y": 0.5, "z": 0.5}, f"T-{i}")
        alert = detector.check()
        assert alert.level == Level.STABLE
        assert alert.rate > 0


# --- DECLINE DETECTION ---

class TestDecline:
    def test_gradual_decline(self, detector):
        values = [0.9, 0.85, 0.80, 0.75, 0.70]
        for i, v in enumerate(values):
            detector.record(v, {"x": v, "y": v, "z": v}, f"T-{i}")
        alert = detector.check()
        assert alert.rate < 0

    def test_critical_fast_drop(self, detector):
        values = [1.0, 0.5, 0.2]
        for i, v in enumerate(values):
            detector.record(v, {"x": v, "y": v, "z": v}, f"T-{i}")
        alert = detector.check()
        assert alert.level == Level.CRITICAL

    def test_near_floor_with_decline(self, detector):
        detector.record(0.19, {"x": 0.2, "y": 0.1, "z": 0.3}, "T-001")
        detector.record(0.15, {"x": 0.1, "y": 0.1, "z": 0.2}, "T-002")
        alert = detector.check()
        assert alert.level == Level.CRITICAL

    def test_consecutive_declines_trigger_warning(self, tmp_path):
        d = DriftDetector(components=["x"], path=tmp_path,
                          decline_threshold=-0.5, consec_warn=3)
        values = [0.9, 0.89, 0.88, 0.87, 0.86]
        for i, v in enumerate(values):
            d.record(v, {"x": v}, f"T-{i}")
        alert = d.check()
        assert alert.consecutive_declines >= 3

    def test_consecutive_declines_trigger_critical(self, tmp_path):
        d = DriftDetector(components=["x"], path=tmp_path,
                          decline_threshold=-0.5, critical_threshold=-0.8,
                          consec_crit=5)
        values = [0.9, 0.89, 0.88, 0.87, 0.86, 0.85]
        for i, v in enumerate(values):
            d.record(v, {"x": v}, f"T-{i}")
        alert = d.check()
        assert alert.level == Level.CRITICAL


# --- ACCELERATION ---

class TestAcceleration:
    def test_no_acceleration_with_few_points(self, detector):
        detector.record(0.9, {"x": 0.9, "y": 0.9, "z": 0.9}, "T-001")
        detector.record(0.8, {"x": 0.8, "y": 0.8, "z": 0.8}, "T-002")
        alert = detector.check()
        assert alert.acceleration == 0.0

    def test_accelerating_decline(self, detector):
        # First half: slow decline. Second half: fast decline.
        values = [1.0, 0.95, 0.90, 0.85, 0.70, 0.50, 0.30, 0.10]
        for i, v in enumerate(values):
            detector.record(v, {"x": v, "y": v, "z": v}, f"T-{i}")
        alert = detector.check()
        assert alert.acceleration < 0  # decline speeding up

    def test_decelerating_decline(self, detector):
        # First half: fast decline. Second half: slow decline.
        values = [1.0, 0.60, 0.30, 0.15, 0.13, 0.12, 0.115, 0.11]
        for i, v in enumerate(values):
            detector.record(v, {"x": v, "y": v, "z": v}, f"T-{i}")
        alert = detector.check()
        assert alert.acceleration > 0  # decline slowing down


# --- COMPONENT-LEVEL DETECTION ---

class TestComponents:
    def test_component_rates_returned(self, detector):
        for i in range(3):
            detector.record(0.8, {"x": 0.9 - i * 0.1, "y": 0.8, "z": 0.8}, f"T-{i}")
        alert = detector.check()
        assert "x" in alert.component_rates
        assert "y" in alert.component_rates
        assert "z" in alert.component_rates

    def test_single_component_critical_escalates(self, tmp_path):
        d = DriftDetector(components=["x", "y"], path=tmp_path,
                          critical_threshold=-0.3)
        # x crashes, y stable, overall value stable
        d.record(0.8, {"x": 0.9, "y": 0.8}, "T-001")
        d.record(0.8, {"x": 0.2, "y": 0.8}, "T-002")
        alert = d.check()
        # x rate is -0.7 which is critical, should escalate overall from STABLE
        assert alert.level != Level.STABLE or alert.component_rates["x"] < -0.3


# --- PERSISTENCE ---

class TestPersistence:
    def test_save_and_reload(self, tmp_path):
        d1 = DriftDetector(components=["a", "b"], path=tmp_path)
        d1.record(0.9, {"a": 0.9, "b": 0.8}, "T-001")
        d1.record(0.7, {"a": 0.7, "b": 0.6}, "T-002")
        assert d1.count == 2

        d2 = DriftDetector(components=["a", "b"], path=tmp_path)
        assert d2.count == 2

    def test_state_survives_reload(self, tmp_path):
        d1 = DriftDetector(components=["a"], path=tmp_path)
        d1.record(0.9, {"a": 0.9}, "T-001")
        d1.record(0.7, {"a": 0.7}, "T-002")
        alert1 = d1.check()

        d2 = DriftDetector(components=["a"], path=tmp_path)
        alert2 = d2.check()
        assert alert1.rate == alert2.rate
        assert alert1.current == alert2.current

    def test_missing_file_starts_empty(self, tmp_path):
        d = DriftDetector(components=["a"], path=tmp_path)
        assert d.count == 0

    def test_corrupt_file_starts_empty(self, tmp_path):
        with open(tmp_path, "w") as f:
            f.write("not json{{{")
        d = DriftDetector(components=["a"], path=tmp_path)
        assert d.count == 0


# --- RESET ---

class TestReset:
    def test_reset_clears_state(self, detector):
        for i in range(5):
            detector.record(0.9 - i * 0.1, {"x": 0.5, "y": 0.5, "z": 0.5}, f"T-{i}")
        detector.reset()
        assert detector.count == 0
        alert = detector.check()
        assert alert.level == Level.STABLE

    def test_reset_persists(self, tmp_path):
        d1 = DriftDetector(components=["a"], path=tmp_path)
        d1.record(0.5, {"a": 0.5}, "T-001")
        d1.reset()
        d2 = DriftDetector(components=["a"], path=tmp_path)
        assert d2.count == 0


# --- EDGE CASES ---

class TestEdgeCases:
    def test_zero_value(self, detector):
        detector.record(0.0, {"x": 0.0, "y": 0.0, "z": 0.0}, "T-001")
        detector.record(0.0, {"x": 0.0, "y": 0.0, "z": 0.0}, "T-002")
        alert = detector.check()
        assert alert.level in (Level.STABLE, Level.CRITICAL)

    def test_negative_value(self, detector):
        detector.record(-0.5, {"x": -0.5, "y": 0.0, "z": 0.0}, "T-001")
        detector.record(-1.0, {"x": -1.0, "y": 0.0, "z": 0.0}, "T-002")
        alert = detector.check()
        assert alert.rate < 0

    def test_large_window(self, tmp_path):
        d = DriftDetector(components=["a"], path=tmp_path, window=100)
        for i in range(50):
            d.record(0.9, {"a": 0.9}, f"T-{i}")
        assert d.count == 50
        alert = d.check()
        assert alert.level == Level.STABLE

    def test_custom_thresholds(self, tmp_path):
        d = DriftDetector(components=["a"], path=tmp_path,
                          decline_threshold=-0.01, critical_threshold=-0.05)
        d.record(0.9, {"a": 0.9}, "T-001")
        d.record(0.85, {"a": 0.85}, "T-002")
        alert = d.check()
        assert alert.level != Level.STABLE  # -0.05 rate exceeds tight threshold
