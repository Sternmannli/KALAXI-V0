#!/usr/bin/env python3
"""
Tests for WEAVER/voice_engine.py — Canon-grounded voice generation.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from WEAVER.voice_engine import (
    VoiceEngine, VoiceCorpus, VoiceResponse, CanonFragment,
    detect_register, _somatic_score, _sentence_shape_score,
)


# ═══════════════════════════════════════════════════
# REGISTER DETECTION
# ═══════════════════════════════════════════════════

class TestRegisterDetection:
    """Test emotional register detection."""

    def test_grief_register(self):
        assert detect_register("I lost someone I loved") == "grief"

    def test_dignity_register(self):
        assert detect_register("My dignity was denied by the system") == "dignity"

    def test_seeking_register(self):
        assert detect_register("What does the canon say about this?") == "seeking"

    def test_greeting_register(self):
        assert detect_register("Hello, I am entering for the first time") == "greeting"

    def test_silence_register(self):
        assert detect_register("Hold the silence and breathe") == "silence"

    def test_general_register(self):
        assert detect_register("The weather is fine today") == "general"


# ═══════════════════════════════════════════════════
# SOMATIC SCORING
# ═══════════════════════════════════════════════════

class TestSomaticScore:
    """Test somatic vocabulary detection."""

    def test_somatic_text(self):
        score = _somatic_score("She held the rope with both hands and breathed")
        assert score > 0.5

    def test_no_somatic(self):
        score = _somatic_score("The algorithm processed the data efficiently")
        assert score == 0.0

    def test_material_anchors(self):
        score = _somatic_score("The stone held water against the weir")
        assert score > 0.5


# ═══════════════════════════════════════════════════
# SENTENCE SHAPE
# ═══════════════════════════════════════════════════

class TestSentenceShape:
    """Test sentence length scoring (8-14 words ideal)."""

    def test_ideal_length(self):
        # 10 words — within ideal range
        score = _sentence_shape_score("The river was low enough to argue with that day.")
        assert score > 0.5

    def test_very_short(self):
        # 2 words — too short
        score = _sentence_shape_score("He ran.")
        assert score < 1.0  # May still partially pass

    def test_very_long(self):
        # Very long sentence
        long = "The " + " ".join(["very"] * 50) + " long sentence."
        score = _sentence_shape_score(long)
        assert score < 0.5


# ═══════════════════════════════════════════════════
# VOICE CORPUS
# ═══════════════════════════════════════════════════

class TestVoiceCorpus:
    """Test corpus loading and selection."""

    @pytest.fixture
    def corpus(self):
        c = VoiceCorpus()
        c.load()
        return c

    def test_corpus_loads(self, corpus):
        """Corpus should load without error."""
        assert corpus._loaded is True

    def test_has_fragments(self, corpus):
        """Corpus should have at least some fragments."""
        assert corpus.total_fragments > 0

    def test_proverbs_loaded(self, corpus):
        """At least some proverbs should load."""
        assert len(corpus._proverbs) > 0

    def test_golden_loaded(self, corpus):
        """Golden regression utterances should load."""
        assert len(corpus._golden) > 0

    def test_narratives_loaded(self, corpus):
        """Narrative fragments should load."""
        assert len(corpus._narrative_fragments) > 0

    def test_select_proverb(self, corpus):
        """Should select a proverb."""
        result = corpus.select_proverb(n=1)
        assert len(result) == 1
        assert isinstance(result[0], CanonFragment)
        assert result[0].source == "proverb"

    def test_select_golden(self, corpus):
        """Should select a golden utterance."""
        result = corpus.select_golden(n=1)
        assert len(result) == 1
        assert result[0].source == "golden"

    def test_select_narrative(self, corpus):
        """Should select a narrative fragment."""
        result = corpus.select_narrative(n=1)
        assert len(result) == 1
        assert result[0].source == "narrative"

    def test_select_by_book(self, corpus):
        """Should filter narratives by book."""
        result = corpus.select_narrative(book="hakaka", n=1)
        if result:
            assert result[0].book == "hakaka"

    def test_random_fragment(self, corpus):
        """Should return a random fragment from any source."""
        frag = corpus.random_fragment()
        assert frag is not None
        assert frag.text

    def test_themed_proverb(self, corpus):
        """Theme-biased selection should work."""
        result = corpus.select_proverb(theme_words=["path", "bridge"], n=3)
        assert len(result) <= 3


# ═══════════════════════════════════════════════════
# VOICE ENGINE
# ═══════════════════════════════════════════════════

class TestVoiceEngine:
    """Test the voice engine response generation."""

    @pytest.fixture
    def engine(self):
        return VoiceEngine()

    def test_engine_initializes(self, engine):
        """Engine should initialize with corpus loaded."""
        assert engine.corpus_size > 0

    def test_respond_general(self, engine):
        """Should respond to general input."""
        resp = engine.respond("The day was long and the road stretched ahead.")
        assert isinstance(resp, VoiceResponse)
        assert resp.text
        assert resp.register
        assert resp.witness_id

    def test_respond_grief(self, engine):
        """Should respond to grief register."""
        resp = engine.respond("I lost my way and everything hurts.")
        assert resp.register == "grief"
        assert resp.text

    def test_respond_dignity(self, engine):
        """Should respond to dignity register."""
        resp = engine.respond("The system denied my dignity and made me invisible.")
        assert resp.register == "dignity"
        assert resp.text

    def test_respond_zero_dignity(self, engine):
        """Should halt on zero dignity."""
        resp = engine.respond("Any text here", dignity=0.0)
        assert "Witnessed" in resp.text
        assert resp.breath_paced is True

    def test_sources_tracked(self, engine):
        """Response should track its canon sources."""
        resp = engine.respond("Tell me about the river and the stone.")
        assert len(resp.sources) > 0

    def test_witness_id_unique(self, engine):
        """Each response should have a unique witness ID."""
        r1 = engine.respond("First message")
        r2 = engine.respond("Second message")
        assert r1.witness_id != r2.witness_id

    def test_stats(self, engine):
        """Should report corpus statistics."""
        stats = engine.stats()
        assert "proverbs" in stats
        assert "golden_utterances" in stats
        assert "narrative_fragments" in stats
        assert "treasures" in stats
        assert "total_fragments" in stats
        assert stats["total_fragments"] > 0

    def test_proverb_method(self, engine):
        """Direct proverb access should work."""
        p = engine.proverb()
        assert p is not None
        assert p.source == "proverb"

    def test_narrative_method(self, engine):
        """Direct narrative access should work."""
        n = engine.narrative_fragment()
        assert n is not None
        assert n.source == "narrative"


# ═══════════════════════════════════════════════════
# DIGNITY INTEGRATION
# ═══════════════════════════════════════════════════

class TestDignityIntegration:
    """Test that voice engine respects dignity gates."""

    @pytest.fixture
    def engine(self):
        return VoiceEngine()

    def test_low_dignity_paced(self, engine):
        """Low dignity should trigger breath pacing."""
        resp = engine.respond("Text", dignity=0.3)
        assert resp.breath_paced is True

    def test_high_dignity_not_paced(self, engine):
        """High dignity should not trigger pacing."""
        resp = engine.respond("Text", dignity=0.9)
        assert resp.breath_paced is False

    def test_negative_dignity_halts(self, engine):
        """Negative dignity should halt."""
        resp = engine.respond("Text", dignity=-1.0)
        assert "Witnessed" in resp.text
