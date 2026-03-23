#!/usr/bin/env python3
"""
Tests for ConversationMemory — pattern tracking across turns.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import pytest
from WEAVER.conversation_memory import ConversationMemory, TurnSnapshot, ConversationSnapshot


class TestTurnSnapshot:
    """Test individual turn snapshots."""

    def test_creates_with_required_fields(self):
        snap = TurnSnapshot(
            exchange_id="EX-000001",
            register="grief",
            themes=["children", "separation"],
            confidence=0.85,
            dignity_score=1.0,
            canon_sources=["P#2135"],
        )
        assert snap.exchange_id == "EX-000001"
        assert snap.register == "grief"
        assert snap.themes == ["children", "separation"]
        assert snap.confidence == 0.85
        assert snap.dignity_score == 1.0
        assert snap.canon_sources == ["P#2135"]
        assert snap.timestamp  # auto-generated

    def test_custom_timestamp(self):
        snap = TurnSnapshot(
            exchange_id="EX-000001",
            register="general",
            themes=[],
            confidence=0.5,
            dignity_score=1.0,
            canon_sources=[],
            timestamp="2026-03-23T10:00:00+00:00",
        )
        assert snap.timestamp == "2026-03-23T10:00:00+00:00"


class TestConversationSnapshot:
    """Test conversation snapshot dataclass."""

    def test_defaults(self):
        snap = ConversationSnapshot()
        assert snap.dominant_register == "general"
        assert snap.recurring_themes == []
        assert snap.confidence_trend == "stable"
        assert snap.turn_count == 0
        assert snap.dignity_trend == "stable"

    def test_to_dict(self):
        snap = ConversationSnapshot(
            dominant_register="grief",
            recurring_themes=["children"],
            confidence_trend="rising",
            turn_count=5,
            dignity_trend="stable",
        )
        d = snap.to_dict()
        assert d["dominant_register"] == "grief"
        assert d["recurring_themes"] == ["children"]
        assert d["confidence_trend"] == "rising"
        assert d["turn_count"] == 5
        assert d["dignity_trend"] == "stable"


class TestConversationMemory:
    """Test the memory across turns."""

    def _make_turn(self, ex_id, register="general", themes=None,
                   confidence=0.5, dignity=1.0, sources=None):
        return TurnSnapshot(
            exchange_id=ex_id,
            register=register,
            themes=themes or [],
            confidence=confidence,
            dignity_score=dignity,
            canon_sources=sources or [],
        )

    def test_empty_memory(self):
        mem = ConversationMemory()
        assert mem.turn_count == 0
        assert mem.dominant_register == "general"
        assert mem.recurring_themes == []
        assert mem.confidence_trend == "stable"
        assert mem.dignity_trend == "stable"

    def test_single_turn(self):
        mem = ConversationMemory()
        mem.record_turn(self._make_turn("EX-1", "grief", ["children"]))
        assert mem.turn_count == 1
        assert mem.dominant_register == "grief"
        assert mem.recurring_themes == []  # needs >1 occurrence

    def test_dominant_register_multiple_turns(self):
        mem = ConversationMemory()
        mem.record_turn(self._make_turn("EX-1", "grief"))
        mem.record_turn(self._make_turn("EX-2", "grief"))
        mem.record_turn(self._make_turn("EX-3", "dignity"))
        assert mem.dominant_register == "grief"

    def test_recurring_themes(self):
        mem = ConversationMemory()
        mem.record_turn(self._make_turn("EX-1", themes=["children", "separation"]))
        mem.record_turn(self._make_turn("EX-2", themes=["children", "institutions"]))
        mem.record_turn(self._make_turn("EX-3", themes=["separation"]))
        recurring = mem.recurring_themes
        assert "children" in recurring
        assert "separation" in recurring

    def test_five_turns_grief_pattern(self):
        """The scenario from the description: 5 turns about a separated father."""
        mem = ConversationMemory()
        for i in range(5):
            mem.record_turn(self._make_turn(
                f"EX-{i+1}",
                register="grief",
                themes=["children"],
                confidence=0.8,
                dignity=1.0,
            ))
        snap = mem.snapshot()
        assert snap.dominant_register == "grief"
        assert "children" in snap.recurring_themes
        assert snap.confidence_trend == "stable"
        assert snap.turn_count == 5

    def test_confidence_trend_rising(self):
        mem = ConversationMemory()
        for i, conf in enumerate([0.3, 0.4, 0.5, 0.7, 0.9]):
            mem.record_turn(self._make_turn(f"EX-{i}", confidence=conf))
        assert mem.confidence_trend == "rising"

    def test_confidence_trend_falling(self):
        mem = ConversationMemory()
        for i, conf in enumerate([0.9, 0.8, 0.7, 0.5, 0.3]):
            mem.record_turn(self._make_turn(f"EX-{i}", confidence=conf))
        assert mem.confidence_trend == "falling"

    def test_confidence_trend_stable(self):
        mem = ConversationMemory()
        for i in range(5):
            mem.record_turn(self._make_turn(f"EX-{i}", confidence=0.7))
        assert mem.confidence_trend == "stable"

    def test_dignity_trend_falling(self):
        mem = ConversationMemory()
        for i, d in enumerate([1.0, 0.9, 0.8, 0.6, 0.4]):
            mem.record_turn(self._make_turn(f"EX-{i}", dignity=d))
        assert mem.dignity_trend == "falling"

    def test_max_turns_cap(self):
        mem = ConversationMemory(max_turns=5)
        for i in range(10):
            mem.record_turn(self._make_turn(f"EX-{i}"))
        assert mem.turn_count == 5

    def test_snapshot_returns_dataclass(self):
        mem = ConversationMemory()
        mem.record_turn(self._make_turn("EX-1", "grief", ["children"]))
        snap = mem.snapshot()
        assert isinstance(snap, ConversationSnapshot)

    def test_to_dict_full(self):
        mem = ConversationMemory()
        mem.record_turn(self._make_turn("EX-1", "grief", ["children"], 0.8, 1.0, ["P#2135"]))
        d = mem.to_dict()
        assert len(d["turns"]) == 1
        assert d["turns"][0]["exchange_id"] == "EX-1"
        assert d["turns"][0]["register"] == "grief"
        assert d["turns"][0]["themes"] == ["children"]
        assert d["turns"][0]["confidence"] == 0.8
        assert d["turns"][0]["dignity_score"] == 1.0
        assert d["turns"][0]["canon_sources"] == ["P#2135"]
        assert "snapshot" in d


class TestWitnessRecordMetadata:
    """Test that WitnessRecord.to_dict() includes metadata."""

    def test_metadata_survives_to_dict(self):
        from WEAVER.witness_network import WitnessNetwork
        wn = WitnessNetwork()
        meta = {
            "dignity": {"D": 1.0, "A": 0.9, "L": 0.8, "M": 0.7},
            "intelligence": {"register": "grief", "themes": ["children"]},
            "conversation": {"dominant_register": "grief", "turn_count": 3},
        }
        record = wn.witness("exchange", "EX-001: D=1.0", "organism", metadata=meta)
        d = record.to_dict()
        assert "metadata" in d
        assert d["metadata"]["dignity"]["D"] == 1.0
        assert d["metadata"]["intelligence"]["register"] == "grief"
        assert d["metadata"]["conversation"]["dominant_register"] == "grief"

    def test_empty_metadata_serializes(self):
        from WEAVER.witness_network import WitnessNetwork
        wn = WitnessNetwork()
        record = wn.witness("exchange", "EX-001: D=1.0", "organism")
        d = record.to_dict()
        assert "metadata" in d
        assert d["metadata"] == {}

    def test_chain_still_valid_with_metadata(self):
        from WEAVER.witness_network import WitnessNetwork
        wn = WitnessNetwork()
        wn.witness("exchange", "EX-001", "organism", metadata={"a": 1})
        wn.witness("exchange", "EX-002", "organism", metadata={"b": 2})
        wn.witness("exchange", "EX-003", "organism", metadata={"c": 3})
        assert wn.verify_chain()


class TestLoadCertificateRoundTrip:
    """Test that certificates survive save/load cycle."""

    def test_load_matches_stored_keys(self):
        """to_chain_entry() uses 'dignity_snapshot', load_certificate must read it."""
        from WEAVER.witness_certificate import (
            WitnessCertificate, DignitySnapshot, Subject,
            InstitutionalContext, CoordinatesOfFailure,
            generate_certificate, save_certificate, load_certificate,
        )
        import tempfile
        import os

        snap = DignitySnapshot(A=0.0, L=0.8, M=0.7)
        cert = generate_certificate(
            dignity=snap,
            subject=Subject("donor:EX-001", "donor"),
            context=InstitutionalContext("kalaxi", "dignity_check", "EX-001", "phase_2"),
            coordinates=CoordinatesOfFailure(
                axis="A", node_id="check", rule_id="D=AxLxM",
                inputs_present=["test input"],
                missing_or_unreadable=["A"],
                machine_explanation="A was zero",
            ),
        )

        # Save and load
        with tempfile.TemporaryDirectory() as tmpdir:
            # Monkey-patch the certificate directory
            import WEAVER.witness_certificate as wc_mod
            original_dir = wc_mod.CERTIFICATE_DIR
            wc_mod.CERTIFICATE_DIR = type(original_dir)(tmpdir)
            try:
                save_certificate(cert)
                loaded = load_certificate(cert.certificate_id)
            finally:
                wc_mod.CERTIFICATE_DIR = original_dir

            assert loaded is not None
            assert loaded.certificate_id == cert.certificate_id
            assert loaded.dignity.A == 0.0
            assert loaded.dignity.L == 0.8
            assert loaded.dignity.M == 0.7
            assert loaded.coordinates.axis == "A"
            assert loaded.coordinates.machine_explanation == "A was zero"
            assert loaded.context.institution_id == "kalaxi"
            assert loaded.halt_reason_code == cert.halt_reason_code
            assert loaded.schema_version == "1.0"
            assert "witness_certificate" in loaded.tags
