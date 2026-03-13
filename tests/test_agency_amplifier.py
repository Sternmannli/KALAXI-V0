#!/usr/bin/env python3
"""Tests for Seed #12: Agency Amplifier."""

import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.agency_amplifier import AgencyAmplifier, AgencyScore


def test_basic_agency_score():
    amp = AgencyAmplifier()
    score = amp.measure("EX-001", V=0.8, F=0.6, C=0.7, U=0.9)
    assert 0.74 < score.A < 0.76  # (0.8+0.6+0.7+0.9)/4 = 0.75
    assert score.weakest == "affordability"
    assert not score.is_collapsed


def test_zero_collapses_agency():
    amp = AgencyAmplifier()
    score = amp.measure("EX-002", V=0.8, F=0.0, C=0.7, U=0.9)
    assert score.A == 0.0
    assert score.is_collapsed
    assert score.weakest == "affordability"


def test_perfect_agency():
    amp = AgencyAmplifier()
    score = amp.measure("EX-003", V=1.0, F=1.0, C=1.0, U=1.0)
    assert score.A == 1.0
    assert not score.is_collapsed


def test_clamping():
    amp = AgencyAmplifier()
    score = amp.measure("EX-004", V=1.5, F=-0.3, C=0.5, U=0.5)
    assert score.visibility == 1.0
    assert score.affordability == 0.0
    assert score.is_collapsed  # F was clamped to 0


def test_report():
    amp = AgencyAmplifier()
    amp.measure("EX-001", V=0.8, F=0.3, C=0.7, U=0.9)
    amp.measure("EX-002", V=0.6, F=0.4, C=0.5, U=0.8)
    amp.measure("EX-003", V=0.9, F=0.0, C=0.8, U=0.7)  # collapse

    report = amp.report()
    assert report["status"] == "ok"
    assert report["measurements"] == 3
    assert report["collapses"] == 1
    assert report["systemic_weakness"] == "affordability"
    assert "cost" in report["recommendation"].lower() or "recourse" in report["recommendation"].lower()


def test_report_empty():
    amp = AgencyAmplifier()
    report = amp.report()
    assert report["status"] == "no_data"


def test_to_dict():
    amp = AgencyAmplifier()
    score = amp.measure("EX-005", V=0.5, F=0.5, C=0.5, U=0.5)
    d = score.to_dict()
    assert d["A"] == 0.5
    assert d["exchange_id"] == "EX-005"
    assert not d["collapsed"]


def test_reset():
    amp = AgencyAmplifier()
    amp.measure("EX-001", V=0.8, F=0.6, C=0.7, U=0.9)
    assert amp.scores_count == 1
    amp.reset()
    assert amp.scores_count == 0
