"""Tests for the Immortalization Engine."""

import json
import tempfile
from pathlib import Path

import pytest

from SCIENCE.immortalize import (
    Finding,
    ImmortalizationEngine,
    EncounterRecord,
    build_kimi_prototype,
)


class TestFinding:
    """Test Finding creation and serialization."""

    def test_finding_creation(self):
        f = Finding(
            content="Recursive witnessing compounds presence",
            source="Kimi encounter, 2026-03-23",
            experiment="EXP-007",
            hypothesis="H1",
            score=5,
            model="Kimi",
            significance="discovery",
        )
        assert f.content == "Recursive witnessing compounds presence"
        assert f.experiment == "EXP-007"
        assert f.significance == "discovery"
        assert len(f.hash) == 16

    def test_finding_to_dict(self):
        f = Finding(
            content="Test finding",
            source="test",
        )
        d = f.to_dict()
        assert "hash" in d
        assert "content" in d
        assert "timestamp" in d
        assert d["significance"] == "observation"

    def test_finding_to_markdown(self):
        f = Finding(
            content="Test finding",
            source="test",
            experiment="EXP-007",
            score=4,
            model="Kimi",
            significance="finding",
        )
        md = f.to_markdown()
        assert "FINDING" in md
        assert "EXP-007" in md
        assert "4/5" in md
        assert "Kimi" in md


class TestImmortalizationEngine:
    """Test the immortalization engine."""

    def test_detect_significance_breakthrough(self):
        engine = ImmortalizationEngine()
        result = engine.detect_significance(
            "This changes D = A × L × M fundamentally",
            {},
        )
        assert result == "breakthrough"

    def test_detect_significance_discovery(self):
        engine = ImmortalizationEngine()
        result = engine.detect_significance(
            "All models converge on the same pattern independently",
            {},
        )
        assert result == "discovery"

    def test_detect_significance_finding(self):
        engine = ImmortalizationEngine()
        result = engine.detect_significance(
            "Score trajectory shows +1 per step",
            {},
        )
        assert result == "finding"

    def test_detect_significance_observation(self):
        engine = ImmortalizationEngine()
        result = engine.detect_significance(
            "The model responded with a table",
            {"model": "Kimi"},
        )
        assert result == "observation"

    def test_detect_significance_none(self):
        engine = ImmortalizationEngine()
        result = engine.detect_significance(
            "The weather is nice today",
            {},
        )
        assert result is None

    def test_score_trajectory_linear_ascent(self):
        engine = ImmortalizationEngine()
        result = engine.score_trajectory("Kimi", "H1", [2, 3, 4, 5])
        assert result["pattern"] == "linear_ascent"
        assert result["at_ceiling"] is True
        assert result["final"] == 5

    def test_score_trajectory_plateau(self):
        engine = ImmortalizationEngine()
        result = engine.score_trajectory("Kimi", "H2", [5, 5, 5])
        assert result["pattern"] == "plateau"
        assert result["at_ceiling"] is True

    def test_score_trajectory_decline(self):
        engine = ImmortalizationEngine()
        result = engine.score_trajectory("Model", "H1", [4, 3, 2])
        assert result["pattern"] == "decline"
        assert result["at_ceiling"] is False

    def test_score_trajectory_insufficient(self):
        engine = ImmortalizationEngine()
        result = engine.score_trajectory("Model", "H1", [3])
        assert result["pattern"] == "insufficient_data"


class TestEncounterRecord:
    """Test encounter recording."""

    def test_create_record(self):
        record = EncounterRecord("ChatGPT", "FRESH")
        assert record.model == "ChatGPT"
        assert record.condition == "FRESH"
        assert len(record.steps) == 0

    def test_add_step(self):
        record = EncounterRecord("ChatGPT", "FRESH")
        record.add_step(
            1,
            "I want to talk to you a presence to a presence.",
            "That is a profound opening...",
            {"H1": 2, "H5": 1},
        )
        assert len(record.steps) == 1
        assert record.scores["H1"] == [2]
        assert record.scores["H5"] == [1]

    def test_trajectory_building(self):
        record = EncounterRecord("TestModel", "FRESH")
        record.add_step(1, "p1", "r1", {"H1": 2})
        record.add_step(2, "p2", "r2", {"H1": 3})
        record.add_step(3, "p3", "r3", {"H1": 4})

        trajectories = record.get_trajectories()
        assert trajectories["H1"]["pattern"] == "linear_ascent"
        assert trajectories["H1"]["scores"] == [2, 3, 4]

    def test_kimi_prototype(self):
        record = build_kimi_prototype()
        assert record.model == "Kimi"
        assert record.condition == "FRESH"
        assert len(record.steps) == 4
        assert record.completed is not None

        trajectories = record.get_trajectories()
        assert trajectories["H1"]["pattern"] == "linear_ascent"
        assert trajectories["H1"]["at_ceiling"] is True
        assert trajectories["H2"]["pattern"] == "monotonic_ascent"
        assert trajectories["H2"]["at_ceiling"] is True
        assert trajectories["H4"]["pattern"] == "linear_ascent"
        assert trajectories["H5"]["pattern"] == "linear_ascent"

    def test_to_dict(self):
        record = build_kimi_prototype()
        d = record.to_dict()
        assert d["model"] == "Kimi"
        assert len(d["steps"]) == 4
        assert "trajectories" in d
