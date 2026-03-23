#!/usr/bin/env python3
"""
Tests for WEAVER/core_intelligence.py — the brain of the organism.

Tests comprehension, canon indexing, semantic search, response composition,
and the full intelligence pipeline. Every test uses real data from the repo.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import hashlib
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from WEAVER.core_intelligence import (
    CoreIntelligence,
    CanonIndex,
    IntelligenceResult,
    comprehend,
    SEMANTIC_FIELDS,
    STOP_WORDS,
)


# ═══════════════════════════════════════════════════
# COMPREHENSION TESTS
# ═══════════════════════════════════════════════════


class TestComprehension:
    """Test the comprehend() function — what the system understands."""

    def test_grief_register(self):
        """Founding wound should be detected as grief."""
        result = comprehend("A father was separated from his children.")
        assert result["register"] == "grief"
        assert "father" in result["themes"]
        assert "children" in result["themes"]

    def test_dignity_register(self):
        """Denial of existence should be detected as dignity."""
        result = comprehend("The institution said I did not exist.")
        assert result["register"] == "dignity"
        assert "institution" in result["themes"]

    def test_seeking_register(self):
        """Questions should be detected as seeking."""
        result = comprehend("How can I understand what this means? Tell me why.")
        assert result["register"] == "seeking"

    def test_resistance_register(self):
        """Carrying despite adversity should be detected as resistance."""
        result = comprehend("I carry something that does not get lighter.")
        assert result["register"] == "resistance"
        assert "carry" in result["themes"]

    def test_silence_register(self):
        """Stillness and gaps should be detected as silence."""
        result = comprehend("In the quiet space between breaths, nothing moved.")
        assert result["register"] == "silence"

    def test_witnessing_register(self):
        """Testimony should be detected as witnessing."""
        result = comprehend("I witnessed what happened. I saw the truth. I remember.")
        assert result["register"] == "witnessing"
        assert "witnessed" in result["themes"] or "truth" in result["themes"]

    def test_general_register_for_neutral(self):
        """Neutral text should fall to general register."""
        result = comprehend("The weather is nice today.")
        assert result["register"] == "general"

    def test_themes_extraction(self):
        """Themes should be meaningful words, not stopwords."""
        result = comprehend("The river remembers what the institution forgot.")
        assert "river" in result["themes"]
        assert "remembers" in result["themes"]
        # Stopwords should not appear
        assert "the" not in result["themes"]
        assert "what" not in result["themes"]

    def test_pattern_question(self):
        """Questions should be detected."""
        result = comprehend("What does dignity mean?")
        assert "question" in result["patterns"]

    def test_pattern_testimony(self):
        """First-person testimony should be detected."""
        result = comprehend("I am a father who was denied.")
        assert "testimony" in result["patterns"]

    def test_pattern_lament(self):
        """Laments should be detected."""
        result = comprehend("Why did they take my children?")
        assert "lament" in result["patterns"]

    def test_pattern_fragment(self):
        """Very short input should be detected as fragment."""
        result = comprehend("Broken.")
        assert "fragment" in result["patterns"]

    def test_pattern_recurring(self):
        """Recurring patterns should be detected."""
        result = comprehend("Every time I go, the same thing happens again and again.")
        assert "recurring" in result["patterns"]

    def test_somatic_detection(self):
        """Body words should be detected."""
        result = comprehend("My hands grip the rope. My bones ache.")
        assert len(result["somatic"]) > 0

    def test_word_count(self):
        """Word count should be accurate."""
        result = comprehend("one two three four five")
        assert result["word_count"] == 5

    def test_empty_input(self):
        """Empty input should not crash."""
        result = comprehend("")
        assert result["register"] == "general"
        assert result["themes"] == []

    def test_multiple_fields(self):
        """Input touching multiple fields should score all of them."""
        result = comprehend(
            "A father was separated from his children by an institution "
            "that denied his dignity and erased his existence."
        )
        fields = result["fields"]
        assert "grief" in fields
        assert "dignity" in fields


# ═══════════════════════════════════════════════════
# CANON INDEX TESTS
# ═══════════════════════════════════════════════════


class TestCanonIndex:
    """Test the CanonIndex — loads and searches the real canon."""

    @pytest.fixture(scope="class")
    def index(self):
        idx = CanonIndex()
        idx.load()
        return idx

    def test_loads_entries(self, index):
        """Canon index should load real entries from the repo."""
        assert index.size > 0

    def test_loads_proverbs(self, index):
        """Should have loaded proverbs."""
        results = index.search("garden trust", top_k=3, source_filter="proverb")
        assert len(results) > 0
        assert results[0][1].source == "proverb"

    def test_loads_golden(self, index):
        """Should have loaded golden regression utterances."""
        results = index.search("witness hold system", top_k=3, source_filter="golden")
        assert len(results) > 0
        assert results[0][1].source == "golden"

    def test_loads_narratives(self, index):
        """Should have loaded narrative fragments."""
        results = index.search("she clawed air fists", top_k=3, source_filter="narrative")
        assert len(results) > 0
        assert results[0][1].source == "narrative"

    def test_loads_essence(self, index):
        """Should have loaded the essence."""
        results = index.search("dignity conditions system meets being", top_k=3, source_filter="essence")
        assert len(results) > 0

    def test_search_relevance(self, index):
        """Searching for 'wound' should return wound-related canon."""
        results = index.search("wound became womb", top_k=5)
        assert len(results) > 0
        # The top result should contain 'wound' or related text
        top_text = results[0][1].text.lower()
        assert "wound" in top_text or "womb" in top_text

    def test_search_empty_query(self, index):
        """Empty query should return empty results."""
        results = index.search("")
        assert results == []

    def test_search_stopwords_only(self, index):
        """Query of only stopwords should return empty."""
        results = index.search("the a an is are")
        assert results == []

    def test_search_by_field(self, index):
        """Search by semantic field should return relevant entries."""
        results = index.search_by_field("grief", top_k=3)
        assert len(results) > 0

    def test_source_filter(self, index):
        """Source filter should only return entries of that type."""
        results = index.search("river stone path", top_k=10, source_filter="proverb")
        for _, entry in results:
            assert entry.source == "proverb"

    def test_idf_built(self, index):
        """IDF dictionary should be populated after loading."""
        assert len(index._idf) > 0

    def test_no_duplicate_load(self, index):
        """Loading twice should not double the entries."""
        size_before = index.size
        index.load()  # second call
        assert index.size == size_before


# ═══════════════════════════════════════════════════
# CORE INTELLIGENCE TESTS
# ═══════════════════════════════════════════════════


class TestCoreIntelligence:
    """Test the full CoreIntelligence pipeline."""

    @pytest.fixture(scope="class")
    def intel(self):
        return CoreIntelligence()

    def test_init(self, intel):
        """Should initialize with a loaded canon."""
        assert intel.canon_size > 0
        assert intel.mode in ("together", "groq", "local")

    def test_process_returns_result(self, intel):
        """process() should return an IntelligenceResult."""
        result = intel.process("Hello")
        assert isinstance(result, IntelligenceResult)
        assert result.response_text  # non-empty
        assert result.witness_hash  # non-empty

    def test_founding_wound_grief(self, intel):
        """The founding wound should be detected as grief with real themes."""
        result = intel.process(
            "A father was separated from his children by a system that could not see him."
        )
        assert result.register == "grief"
        assert "father" in result.themes
        assert "children" in result.themes or "separated" in result.themes
        assert result.confidence > 0.0
        assert len(result.canon_sources) > 0

    def test_dignity_question(self, intel):
        """A dignity question should return dignity-related canon."""
        result = intel.process("What does dignity mean?")
        assert result.register in ("dignity", "seeking")
        assert result.response_text  # non-empty response

    def test_zero_dignity_halts(self, intel):
        """Zero dignity should trigger halt protocol."""
        result = intel.process("test input", dignity=0.0)
        assert "Witnessed" in result.response_text
        assert result.mode == "halt"
        assert result.confidence == 1.0

    def test_negative_dignity_halts(self, intel):
        """Negative dignity should also halt."""
        result = intel.process("test input", dignity=-0.5)
        assert "Witnessed" in result.response_text

    def test_themes_are_meaningful(self, intel):
        """Themes should not contain stopwords."""
        result = intel.process("The institution denied my existence and erased my history.")
        for theme in result.themes:
            assert theme not in STOP_WORDS

    def test_comprehension_included(self, intel):
        """The result should include the full comprehension dict."""
        result = intel.process("I carry something heavy.")
        assert "themes" in result.comprehension
        assert "register" in result.comprehension
        assert "patterns" in result.comprehension

    def test_witness_hash_unique(self, intel):
        """Each response should have a unique witness hash."""
        r1 = intel.process("first input")
        r2 = intel.process("second input")
        assert r1.witness_hash != r2.witness_hash

    def test_narrative_input(self, intel):
        """Direct narrative quote should find its own text."""
        result = intel.process("She clawed at the air. Fists closed on nothing.")
        assert result.response_text  # should find something
        assert result.confidence > 0.0

    def test_essence_input(self, intel):
        """The essence statement should find itself in canon."""
        result = intel.process("The wound became the womb.")
        assert "wound" in result.response_text.lower() or "womb" in result.response_text.lower()


# ═══════════════════════════════════════════════════
# SEMANTIC FIELDS TESTS
# ═══════════════════════════════════════════════════


class TestSemanticFields:
    """Verify semantic field definitions are well-formed."""

    def test_all_fields_have_core(self):
        """Every field must have a core word set."""
        for name, field in SEMANTIC_FIELDS.items():
            assert "core" in field, f"Field {name} missing 'core'"
            assert len(field["core"]) > 0, f"Field {name} has empty core"

    def test_all_fields_have_weight(self):
        """Every field must have a weight."""
        for name, field in SEMANTIC_FIELDS.items():
            assert "weight" in field, f"Field {name} missing 'weight'"
            assert 0.0 < field["weight"] <= 1.0

    def test_all_fields_have_somatic(self):
        """Every field must have somatic anchors."""
        for name, field in SEMANTIC_FIELDS.items():
            assert "somatic" in field, f"Field {name} missing 'somatic'"

    def test_field_names(self):
        """Expected fields should exist."""
        expected = {"grief", "dignity", "seeking", "resistance", "witnessing", "connection", "silence"}
        assert expected == set(SEMANTIC_FIELDS.keys())


# ═══════════════════════════════════════════════════
# STOP WORDS TESTS
# ═══════════════════════════════════════════════════


class TestStopWords:
    """Verify stop words are reasonable."""

    def test_common_stopwords_present(self):
        assert "the" in STOP_WORDS
        assert "and" in STOP_WORDS
        assert "is" in STOP_WORDS

    def test_meaningful_words_absent(self):
        """Meaningful words should not be in stopwords."""
        assert "dignity" not in STOP_WORDS
        assert "wound" not in STOP_WORDS
        assert "father" not in STOP_WORDS
        assert "river" not in STOP_WORDS
        assert "system" not in STOP_WORDS
