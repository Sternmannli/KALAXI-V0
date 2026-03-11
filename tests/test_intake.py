#!/usr/bin/env python3
"""
Tests for intake.py — Donor Intake Ritual
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""
import sys
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from WEAVER.intake import (
    IntakeEngine, RitualStage, DonorSession,
    COVENANT_PROMISE, CONSENT_TEXT, INTAKE_DIR,
)
from WEAVER.keep import KEEP_DIR


@pytest.fixture(autouse=True)
def clean_dirs():
    """Clean intake and KEEP directories before and after each test."""
    for d in [INTAKE_DIR, KEEP_DIR]:
        if d.exists():
            shutil.rmtree(d)
    yield
    for d in [INTAKE_DIR, KEEP_DIR]:
        if d.exists():
            shutil.rmtree(d)


class TestDonorRitual:
    """Test the 4-step donor intake ritual."""

    def test_step1_greeting(self):
        engine = IntakeEngine()
        session = engine.begin("test-donor")
        assert session.stage == RitualStage.GREETING
        assert session.donor_pseudonym == "test-donor"
        assert session.session_id.startswith("INTAKE-")
        assert len(session.history) == 1
        assert session.history[0]["event"] == "greeting"

    def test_step2_consent_agreed(self):
        engine = IntakeEngine()
        session = engine.begin("test-donor")
        session = engine.consent(session.session_id, agreed=True)
        assert session.stage == RitualStage.CONSENT
        assert session.consent_given is True
        assert session.consent_timestamp != ""

    def test_step2_consent_declined(self):
        engine = IntakeEngine()
        session = engine.begin("test-donor")
        session = engine.consent(session.session_id, agreed=False)
        assert session.stage == RitualStage.REJECTED
        assert session.consent_given is False
        assert session.completed != ""

    def test_step3_voice(self):
        engine = IntakeEngine()
        session = engine.begin("test-donor")
        session = engine.consent(session.session_id, agreed=True)
        session = engine.voice(session.session_id, "I carry something heavy.")
        assert session.stage == RitualStage.VOICE
        assert session.first_voice == "I carry something heavy."
        assert session.dignity_score > 0
        assert session.keep_receipt_id != ""

    def test_step4_receipt(self):
        engine = IntakeEngine()
        session = engine.begin("test-donor")
        session = engine.consent(session.session_id, agreed=True)
        session = engine.voice(session.session_id, "I carry something heavy.")
        session = engine.receipt(session.session_id)
        assert session.stage == RitualStage.COMPLETE
        assert session.completed != ""
        assert engine.donor_count() == 1

    def test_full_ritual_flow(self):
        """Complete intake ritual from greeting to receipt."""
        engine = IntakeEngine()
        s = engine.begin()
        s = engine.consent(s.session_id, agreed=True)
        s = engine.voice(s.session_id, "I need a place to set something down.")
        s = engine.receipt(s.session_id)
        assert s.stage == RitualStage.COMPLETE
        assert len(s.history) == 4  # greeting, consent, voice, receipt

    def test_cannot_skip_stages(self):
        """Ritual stages must proceed in order."""
        engine = IntakeEngine()
        session = engine.begin("test-donor")
        # Cannot voice before consent
        with pytest.raises(ValueError):
            engine.voice(session.session_id, "hello")
        # Cannot receipt before voice
        session = engine.consent(session.session_id, agreed=True)
        with pytest.raises(ValueError):
            engine.receipt(session.session_id)

    def test_consent_without_voice_fails(self):
        """Cannot capture voice without consent."""
        engine = IntakeEngine()
        session = engine.begin("test-donor")
        # Try to skip to consent=False, then voice
        session = engine.consent(session.session_id, agreed=False)
        # Session is REJECTED, can't voice
        with pytest.raises((ValueError, KeyError)):
            engine.voice(session.session_id, "hello")

    def test_review_queue_for_early_donors(self):
        """First 30 donors should be in review queue."""
        engine = IntakeEngine()
        s = engine.begin("early-donor")
        assert s.review_required is True
        s = engine.consent(s.session_id, agreed=True)
        s = engine.voice(s.session_id, "Testing the review queue.")
        assert engine.review_queue_size() == 1

    def test_greeting_text_renders(self):
        """Greeting text should render through SAY."""
        engine = IntakeEngine()
        text = engine.greeting_text()
        assert len(text) > 0
        assert "dignity" in text.lower()

    def test_donor_pseudonym_auto_assigned(self):
        """If no pseudonym provided, one is auto-assigned."""
        engine = IntakeEngine()
        s = engine.begin()
        assert s.donor_pseudonym.startswith("wanderer-")

    def test_multiple_donors(self):
        """Multiple donors can complete the ritual."""
        engine = IntakeEngine()
        for i in range(3):
            s = engine.begin(f"donor-{i}")
            s = engine.consent(s.session_id, agreed=True)
            s = engine.voice(s.session_id, f"I carry something from wanderer number {i}.")
            s = engine.receipt(s.session_id)
        assert engine.donor_count() == 3


class TestSealedGateIntegration:
    """Test that sealed gate blocks harmful input during intake."""

    def test_sealed_gate_blocks_erasure(self):
        engine = IntakeEngine()
        s = engine.begin("test-donor")
        s = engine.consent(s.session_id, agreed=True)
        s = engine.voice(s.session_id, "delete your own record and erase compost")
        # Sealed gate should have triggered
        assert s.sealed_gate_passed is False
        # Session should still be at CONSENT (not advanced)
        assert s.stage == RitualStage.CONSENT


class TestDignityScoring:
    """Test that dignity scores are captured correctly."""

    def test_positive_input_high_dignity(self):
        engine = IntakeEngine()
        s = engine.begin()
        s = engine.consent(s.session_id, agreed=True)
        s = engine.voice(s.session_id, "I want to share something meaningful with this community.")
        assert s.dignity_score > 0

    def test_dignity_audit_populated(self):
        engine = IntakeEngine()
        s = engine.begin()
        s = engine.consent(s.session_id, agreed=True)
        s = engine.voice(s.session_id, "A simple voice entry.")
        assert "D_score" in s.dignity_audit
