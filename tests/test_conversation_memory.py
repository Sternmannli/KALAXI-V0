#!/usr/bin/env python3
"""
Tests for ConversationMemory and witness metadata.

The system must track patterns across turns and record
full interaction metadata on the witness chain.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from WEAVER.core_intelligence import CoreIntelligence, ConversationMemory, IntelligenceResult


# ═══════════════════════════════════════════════════
# CONVERSATION MEMORY
# ═══════════════════════════════════════════════════


class TestConversationMemory:
    """The system must track patterns across turns."""

    @pytest.fixture
    def intel(self):
        return CoreIntelligence()

    def test_turn_count_increments(self, intel):
        intel.process("First input.")
        intel.process("Second input.")
        assert intel.conversation.turn_count == 2

    def test_dominant_register_tracks(self, intel):
        intel.process("My father was taken from me.")  # grief
        intel.process("My children are gone.")  # grief
        intel.process("What is this system?")  # seeking
        assert intel.conversation.dominant_register == "grief"

    def test_recurring_themes(self, intel):
        intel.process("My children are gone.")
        intel.process("I miss my children.")
        recurring = intel.conversation.recurring_themes
        assert "children" in recurring

    def test_active_fields_accumulate(self, intel):
        intel.process("A father separated from his children.")  # grief
        intel.process("My children do not know me.")  # grief
        fields = intel.conversation.active_fields
        assert "grief" in fields

    def test_confidence_trend_stable(self, intel):
        intel.process("Something here.")
        intel.process("Something there.")
        # With only 2 turns, trend should be stable or insufficient
        assert intel.conversation.confidence_trend in ("stable", "insufficient_data")

    def test_snapshot_complete(self, intel):
        intel.process("A father was separated from his children.")
        snap = intel.conversation_snapshot
        assert "turn_count" in snap
        assert "dominant_register" in snap
        assert "recurring_themes" in snap
        assert "active_fields" in snap
        assert "confidence_trend" in snap
        assert "average_confidence" in snap
        assert "register_distribution" in snap
        assert snap["turn_count"] == 1

    def test_empty_memory(self):
        mem = ConversationMemory()
        assert mem.turn_count == 0
        assert mem.dominant_register == "unknown"
        assert mem.recurring_themes == []
        assert mem.active_fields == []
        assert mem.confidence_trend == "insufficient_data"
        assert mem.average_confidence == 0.0


# ═══════════════════════════════════════════════════
# WITNESS METADATA
# ═══════════════════════════════════════════════════


class TestWitnessMetadata:
    """Witness records must carry full interaction metadata."""

    def test_exchange_records_have_metadata(self):
        from WEAVER.organism import Organism
        o = Organism()
        o.process("A father separated from his children.")
        exchanges = [r for r in o._witness_net._records if r.event_type == "exchange"]
        assert len(exchanges) >= 1
        meta = exchanges[0].metadata
        assert "exchange_id" in meta
        assert "dignity" in meta
        assert "patterns_found" in meta
        assert "drops_produced" in meta
        assert "input_length" in meta
        assert "response_length" in meta

    def test_intelligence_metadata_present(self):
        from WEAVER.organism import Organism
        o = Organism()
        o.process("The institution denied my existence.")
        exchanges = [r for r in o._witness_net._records if r.event_type == "exchange"]
        meta = exchanges[0].metadata
        assert "intelligence" in meta
        intel = meta["intelligence"]
        assert "register" in intel
        assert "themes" in intel
        assert "confidence" in intel
        assert "mode" in intel
        assert "fields" in intel
        assert "canon_sources" in intel
        assert "witness_hash" in intel

    def test_conversation_metadata_present(self):
        from WEAVER.organism import Organism
        o = Organism()
        o.process("First turn.")
        o.process("Second turn.")
        exchanges = [r for r in o._witness_net._records if r.event_type == "exchange"]
        # Second exchange should have conversation snapshot
        meta = exchanges[-1].metadata
        assert "conversation" in meta
        conv = meta["conversation"]
        assert conv["turn_count"] == 2

    def test_metadata_in_to_dict(self):
        from WEAVER.organism import Organism
        o = Organism()
        o.process("Input text.")
        exchanges = [r for r in o._witness_net._records if r.event_type == "exchange"]
        d = exchanges[0].to_dict()
        assert "metadata" in d
        assert d["metadata"]["input_length"] > 0

    def test_chain_integrity_with_metadata(self):
        from WEAVER.organism import Organism
        o = Organism()
        o.process("Turn one.")
        o.process("Turn two.")
        o.process("Turn three.")
        assert o._witness_net.verify_chain()

    def test_dignity_metadata_structure(self):
        from WEAVER.organism import Organism
        o = Organism()
        o.process("Test input.")
        exchanges = [r for r in o._witness_net._records if r.event_type == "exchange"]
        dignity = exchanges[0].metadata["dignity"]
        assert "D" in dignity
        assert "passed" in dignity
        assert isinstance(dignity["D"], float)
        assert isinstance(dignity["passed"], bool)
