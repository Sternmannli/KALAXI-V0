#!/usr/bin/env python3
"""
Tests for the COMPASS module (MOVE-001).

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.compass import Compass, CompassReading


def test_compass_instantiation():
    """Compass can be created."""
    c = Compass()
    assert c is not None
    assert c._last_reading is None


def test_compass_sense():
    """Compass.sense() produces a CompassReading."""
    c = Compass()
    reading = c.sense()
    assert isinstance(reading, CompassReading)
    assert reading.timestamp != ""
    assert isinstance(reading.position, dict)
    assert isinstance(reading.heading, dict)
    assert isinstance(reading.next_steps, list)
    assert isinstance(reading.blockers, list)
    assert isinstance(reading.vitals, dict)


def test_compass_position_keys():
    """Position reading contains expected keys."""
    c = Compass()
    reading = c.sense()
    expected_keys = [
        "python_files", "test_files", "narrative_files",
        "covenants", "ledger_entries", "seeds_integrated",
        "deployed", "site_built",
    ]
    for key in expected_keys:
        assert key in reading.position, f"Missing position key: {key}"


def test_compass_heading_keys():
    """Heading reading contains strategic direction."""
    c = Compass()
    reading = c.sense()
    assert "single_blocker" in reading.heading
    assert "deployment_status" in reading.heading


def test_compass_vitals():
    """Vitals include core module check."""
    c = Compass()
    reading = c.sense()
    assert "core_modules" in reading.vitals
    assert reading.vitals["core_modules"] == "11/11"


def test_compass_state():
    """State returns dict for organism integration."""
    c = Compass()
    state = c.state()
    assert state["calibrated"] is False
    assert state["readings"] == 0

    c.sense()
    state = c.state()
    assert state["calibrated"] is True
    assert state["readings"] == 1


def test_compass_generate_md():
    """Compass generates markdown content."""
    c = Compass()
    reading = c.sense()
    md = c.generate_compass_md(reading)
    assert "# COMPASS" in md
    assert "## POSITION" in md
    assert "## HEADING" in md
    assert "## NEXT STEP" in md
    assert "## BLOCKERS" in md
    assert "## VITALS" in md


def test_compass_multiple_readings():
    """Multiple readings accumulate."""
    c = Compass()
    c.sense()
    c.sense()
    c.sense()
    assert len(c._readings) == 3
    assert c.state()["readings"] == 3


def test_compass_write_md(tmp_path):
    """Compass writes COMPASS.md to disk."""
    c = Compass(root=tmp_path)
    # Create minimal structure so it doesn't fail
    (tmp_path / "MANIFEST").mkdir()
    (tmp_path / "WEAVER").mkdir()
    reading = c.sense()
    path = c.write_compass_md(reading)
    assert path.exists()
    content = path.read_text()
    assert "# COMPASS" in content


def test_compass_python_file_count():
    """Python file count is reasonable."""
    c = Compass()
    reading = c.sense()
    assert reading.position["python_files"] >= 100


def test_compass_ledger_count():
    """Ledger entry count is nonzero (we know entries exist)."""
    c = Compass()
    reading = c.sense()
    assert reading.position["ledger_entries"] > 0
