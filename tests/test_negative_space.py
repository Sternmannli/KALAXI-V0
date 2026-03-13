#!/usr/bin/env python3
"""Tests for Seed #9: Negative Space Index."""

import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.negative_space import NegativeSpaceIndex, SilenceType


def test_dormant_domain():
    nsi = NegativeSpaceIndex()
    nsi.register_domain("agency")
    nsi.register_domain("legibility")

    # Observe agency but not legibility for several cycles
    for _ in range(4):
        nsi.observe("agency")
        nsi.tick()

    report = nsi.report()
    assert report.dormant_domains == 1
    assert report.total_silences >= 1


def test_no_silence_when_active():
    nsi = NegativeSpaceIndex()
    nsi.register_domain("agency")

    for _ in range(5):
        nsi.observe("agency")
        nsi.tick()

    report = nsi.report()
    assert report.dormant_domains == 0


def test_missing_pattern():
    nsi = NegativeSpaceIndex()
    nsi.register_expected_pattern("tension", "COV#001")
    nsi.tick()

    report = nsi.report()
    assert report.missing_patterns == 1


def test_pattern_appears():
    nsi = NegativeSpaceIndex()
    nsi.register_expected_pattern("tension", "COV#001")

    nsi.observe("tension")
    nsi.tick()

    # After observing the pattern, it should no longer be missing
    nsi.tick()
    report = nsi.report()
    assert report.missing_patterns == 0


def test_silent_voice():
    nsi = NegativeSpaceIndex()
    nsi.register_voice("donor-001")

    # Voice is never heard
    for _ in range(4):
        nsi.tick()

    report = nsi.report()
    assert report.silent_voices == 1


def test_voice_heard():
    nsi = NegativeSpaceIndex()
    nsi.register_voice("donor-001")

    for _ in range(3):
        nsi.observe("donor-001")
        nsi.tick()

    report = nsi.report()
    assert report.silent_voices == 0


def test_unasked_question():
    nsi = NegativeSpaceIndex()
    nsi.register_question("Who is most affected?", "COV#006 weakest-voice-first")
    nsi.tick()
    nsi.tick()

    report = nsi.report()
    assert report.unasked_questions == 1


def test_question_answered():
    nsi = NegativeSpaceIndex()
    nsi.register_question("Who is most affected?", "COV#006")
    nsi.mark_question_asked("Who is most affected?")
    nsi.tick()

    report = nsi.report()
    assert report.unasked_questions == 0


def test_blindness_score_increases():
    nsi = NegativeSpaceIndex()
    nsi.register_domain("agency")
    nsi.register_domain("legibility")
    nsi.register_domain("moral_standing")

    # Never observe anything
    for _ in range(10):
        nsi.tick()

    report = nsi.report()
    assert report.blindness_score > 0.5


def test_empty_index():
    nsi = NegativeSpaceIndex()
    nsi.tick()
    report = nsi.report()
    assert report.total_silences == 0
    assert report.blindness_score == 0.0


def test_critical_silences():
    nsi = NegativeSpaceIndex()
    nsi.register_domain("forgotten")

    # Many cycles of silence
    for _ in range(15):
        nsi.tick()

    report = nsi.report()
    assert report.critical_silences >= 1


def test_reset():
    nsi = NegativeSpaceIndex()
    nsi.register_domain("agency")
    for _ in range(5):
        nsi.tick()
    assert nsi.cycle == 5

    nsi.reset()
    assert nsi.cycle == 0
    assert nsi.silences_count == 0


def test_report_recommendation():
    nsi = NegativeSpaceIndex()
    nsi.register_domain("forgotten")
    for _ in range(15):
        nsi.tick()

    report = nsi.report()
    assert "CRITICAL" in report.recommendation


def test_top_silences_limited():
    nsi = NegativeSpaceIndex()
    for i in range(10):
        nsi.register_domain(f"domain-{i}")
    for _ in range(5):
        nsi.tick()

    report = nsi.report()
    assert len(report.top_silences) <= 5
