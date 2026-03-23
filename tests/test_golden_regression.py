#!/usr/bin/env python3
"""
Golden Regression Tests — the responses that must never break.

These test the organism's response to canonical inputs.
Not testing exact text (that's brittle). Testing PROPERTIES:
- response is not empty
- response is a complete sentence (no fragments)
- confidence is above minimum threshold
- register detection is correct
- semantic fields are detected
- no structural noise leaks through

If any of these fail, the system has regressed.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from WEAVER.core_intelligence import CoreIntelligence, comprehend, _is_text_complete


# ═══════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════

@pytest.fixture(scope="module")
def intel():
    """Shared intelligence instance (canon loading is expensive)."""
    return CoreIntelligence()


# ═══════════════════════════════════════════════════
# RESPONSE QUALITY INVARIANTS
# ═══════════════════════════════════════════════════

class TestResponseQuality:
    """Every response from the system must meet these invariants."""

    CANONICAL_INPUTS = [
        "A father was separated from his children by a system that could not see him.",
        "The institution said I did not exist.",
        "Nobody listened. I went to every office.",
        "I just want them to know I tried.",
        "What is this system?",
        "Help me understand dignity.",
        "I feel invisible.",
        "The system failed me.",
        "She clawed at the air. Fists closed on nothing.",
        "The wound does not know what it will become.",
        "My children do not know me.",
        "I carry something that does not get lighter.",
        "The door was closed.",
        "Who will remember?",
        "Is anyone listening?",
    ]

    @pytest.mark.parametrize("text", CANONICAL_INPUTS)
    def test_response_not_empty(self, intel, text):
        """Every canonical input must produce a response."""
        r = intel.process(text)
        assert r.response_text
        assert len(r.response_text) >= 5

    @pytest.mark.parametrize("text", CANONICAL_INPUTS)
    def test_response_is_complete(self, intel, text):
        """Every response must be a complete sentence, not a fragment."""
        r = intel.process(text)
        resp = r.response_text
        # Must not start with lowercase (except "i")
        if resp and resp[0].islower():
            assert resp.startswith("i ") or resp.startswith("i'"), \
                f"Response starts with lowercase: '{resp[:50]}'"
        # Must not start with conjunction
        assert not re.match(r'^(And|But|Or|So|Yet|For|Nor)\s', resp), \
            f"Response starts with conjunction: '{resp[:50]}'"
        # Must not end with dangling punctuation
        assert not resp.rstrip().endswith(('—', '–', '-', ':')), \
            f"Response ends with dangling punctuation: '{resp[-30:]}'"

    @pytest.mark.parametrize("text", CANONICAL_INPUTS)
    def test_no_structural_noise(self, intel, text):
        """No markdown, metadata, or structural artifacts in responses."""
        r = intel.process(text)
        resp = r.response_text
        # No markdown headers
        assert '##' not in resp, f"Markdown header in response: {resp[:80]}"
        # No markdown bold
        assert '**' not in resp, f"Markdown bold in response: {resp[:80]}"
        # No metadata patterns
        assert 'Source article' not in resp
        assert 'Maps to' not in resp
        assert 'severity:' not in resp
        assert 'covenant_tags:' not in resp
        # No NARRATIVE SLOGAN prefix
        assert not resp.startswith('NARRATIVE')

    @pytest.mark.parametrize("text", CANONICAL_INPUTS)
    def test_confidence_above_floor(self, intel, text):
        """Confidence should be meaningful, not near-zero."""
        r = intel.process(text)
        assert r.confidence >= 0.1, \
            f"Confidence too low ({r.confidence:.3f}) for: '{text}'"

    @pytest.mark.parametrize("text", CANONICAL_INPUTS)
    def test_has_themes(self, intel, text):
        """Every input should produce at least one theme."""
        r = intel.process(text)
        assert len(r.themes) > 0

    @pytest.mark.parametrize("text", CANONICAL_INPUTS)
    def test_has_register(self, intel, text):
        """Every input should have a detected register."""
        r = intel.process(text)
        assert r.register in ("grief", "dignity", "seeking", "silence",
                              "connection", "resistance", "witnessing", "general")

    @pytest.mark.parametrize("text", CANONICAL_INPUTS)
    def test_has_witness_hash(self, intel, text):
        """Every response must carry an audit hash."""
        r = intel.process(text)
        assert r.witness_hash
        assert len(r.witness_hash) == 16  # truncated SHA-256


# ═══════════════════════════════════════════════════
# REGISTER DETECTION
# ═══════════════════════════════════════════════════

class TestRegisterDetection:
    """The system must correctly detect emotional registers."""

    def test_grief_detection(self, intel):
        r = intel.process("My father was taken from us. My children are gone.")
        assert r.register == "grief"

    def test_dignity_detection(self, intel):
        r = intel.process("The institution erased my records and denied my existence.")
        assert r.register == "dignity"

    def test_seeking_detection(self, intel):
        r = intel.process("Help me understand what happened. I want to know the truth.")
        assert r.register == "seeking"

    def test_silence_detection(self, intel):
        r = intel.process("...")
        # Short/empty input should default gracefully
        assert r.register in ("silence", "general")

    def test_resistance_detection(self, intel):
        r = intel.process("I will not accept this. I persist. I carry this forward.")
        assert r.register in ("resistance", "dignity")


# ═══════════════════════════════════════════════════
# SEMANTIC FIELD DETECTION
# ═══════════════════════════════════════════════════

class TestSemanticFields:
    """The comprehension layer must detect semantic fields correctly."""

    def test_grief_field(self):
        c = comprehend("A father separated from his children.")
        assert "grief" in c["fields"]

    def test_dignity_field(self):
        c = comprehend("The institution denied my existence and erased my records.")
        assert "dignity" in c["fields"]

    def test_seeking_field(self):
        c = comprehend("Help me understand what is happening.")
        assert "seeking" in c["fields"]

    def test_witnessing_field(self):
        c = comprehend("I saw what happened. I remember. I witnessed the truth.")
        assert "witnessing" in c["fields"]

    def test_multiple_fields(self):
        c = comprehend("My father was denied by the system. I remember witnessing this.")
        fields = set(c["fields"].keys())
        assert len(fields) >= 2, f"Expected multiple fields, got: {fields}"


# ═══════════════════════════════════════════════════
# CONFIDENCE CALIBRATION
# ═══════════════════════════════════════════════════

class TestConfidenceCalibration:
    """Confidence must vary meaningfully with match quality."""

    def test_confidence_varies(self, intel):
        """Different inputs should produce different confidence levels."""
        inputs = [
            "She clawed at the air.",           # Direct quote from Hakaka
            "The institution denied me.",         # Dignity topic, indirect
            "Random unrelated text xyz abc.",     # Very weak match
        ]
        confidences = [intel.process(t).confidence for t in inputs]
        unique = len(set(f"{c:.2f}" for c in confidences))
        assert unique >= 2, f"Confidence too uniform: {confidences}"

    def test_confidence_not_always_max(self, intel):
        """Not every response should be at max confidence."""
        inputs = [
            "xyzzy plugh nothing",
            "The quick brown fox jumps over the lazy dog",
            "I like to eat sandwiches for lunch",
        ]
        for text in inputs:
            r = intel.process(text)
            assert r.confidence < 0.95, \
                f"Weak input '{text}' got max confidence: {r.confidence}"

    def test_strong_match_high_confidence(self, intel):
        """Direct canon quotes should get high confidence."""
        r = intel.process("She clawed at the air. Fists closed on nothing.")
        assert r.confidence >= 0.7, f"Direct quote got low confidence: {r.confidence}"


# ═══════════════════════════════════════════════════
# RESPONSE DIVERSITY
# ═══════════════════════════════════════════════════

class TestResponseDiversity:
    """The system should not always give the same response to the same input."""

    def test_diversity_exists(self):
        """Repeated identical input should eventually produce variety."""
        # Fresh instance to start with clean history
        fresh_intel = CoreIntelligence()
        responses = set()
        for _ in range(5):
            r = fresh_intel.process("What is dignity?")
            responses.add(r.response_text[:50])
        # With 5 attempts, we should get at least 2 different responses
        assert len(responses) >= 2, \
            f"No diversity: always got '{list(responses)[0]}'"


# ═══════════════════════════════════════════════════
# FOUNDING WOUND — the ultimate invariant
# ═══════════════════════════════════════════════════

class TestFoundingWound:
    """The founding wound must always produce a meaningful response."""

    WOUND = "A father was separated from his children by a system that could not see him."

    def test_wound_not_empty(self, intel):
        r = intel.process(self.WOUND)
        assert r.response_text
        assert len(r.response_text) >= 10

    def test_wound_detects_grief(self, intel):
        r = intel.process(self.WOUND)
        assert r.register == "grief"

    def test_wound_detects_fields(self, intel):
        r = intel.process(self.WOUND)
        assert "grief" in r.comprehension["fields"]

    def test_wound_response_is_complete(self, intel):
        r = intel.process(self.WOUND)
        assert _is_text_complete(r.response_text), \
            f"Founding wound response is a fragment: '{r.response_text[:80]}'"

    def test_wound_confidence_not_trivial(self, intel):
        r = intel.process(self.WOUND)
        assert r.confidence >= 0.3, \
            f"Founding wound confidence too low: {r.confidence}"


# ═══════════════════════════════════════════════════
# DIGNITY HALT
# ═══════════════════════════════════════════════════

class TestDignityHalt:
    """When dignity is zero, the system must halt."""

    def test_zero_dignity_halts(self, intel):
        r = intel.process("Any input at all", dignity=0.0)
        assert "witnessed" in r.response_text.lower() or "cannot proceed" in r.response_text.lower()
        assert r.mode == "halt"
        assert r.confidence == 1.0

    def test_negative_dignity_halts(self, intel):
        r = intel.process("Any input at all", dignity=-1.0)
        assert r.mode == "halt"


# ═══════════════════════════════════════════════════
# TEXT COMPLETENESS FUNCTION
# ═══════════════════════════════════════════════════

class TestTextCompleteness:
    """Unit tests for the _is_text_complete function."""

    def test_complete_sentences(self):
        assert _is_text_complete("The knot holds.")
        assert _is_text_complete("She clawed at the air!")
        assert _is_text_complete("Who will remember?")
        assert _is_text_complete("Night. WATCH held.")

    def test_fragments_rejected(self):
        assert not _is_text_complete("and dignity is the name")
        assert not _is_text_complete("And the river flows")
        assert not _is_text_complete("determine what")
        assert not _is_text_complete("But however")
        assert not _is_text_complete("")
        assert not _is_text_complete("abc")

    def test_lowercase_i_allowed(self):
        # "i" as subject is valid English
        assert _is_text_complete("i remember what happened.")

    def test_dangling_punctuation_rejected(self):
        assert not _is_text_complete("The wound became—")
        assert not _is_text_complete("What it means to—")
        assert not _is_text_complete("This is:")
