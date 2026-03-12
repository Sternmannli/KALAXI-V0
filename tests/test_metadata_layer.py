#!/usr/bin/env python3
"""
test_metadata_layer.py — Tests for the Metadata Layer (The Brain)

Tests that the three-layer wrapping, gathering space, discovery engine,
persistence, and origin embedding all function correctly.

No metadata is ever deleted. No metadata is ever summarized away.
Every pattern carries its full traceable address.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.metadata_layer import (
    MetadataGathering,
    MetadataEnvelope,
    Layer1_Event,
    Layer2_Pattern,
    Layer3_Relational,
    EventKind,
    Speaker,
    CertaintyLevel,
    Condition,
    ORIGIN,
)


# ═══════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════

@pytest.fixture
def gathering(tmp_path):
    """Fresh gathering space with temporary storage."""
    return MetadataGathering(storage_path=tmp_path / "test_gathering.json")


@pytest.fixture
def populated_gathering(gathering):
    """Gathering space with several events already stored."""
    # Exchange from donor
    gathering.wrap(
        kind=EventKind.EXCHANGE,
        speaker=Speaker.DONOR,
        content="I carry a wound that has no name.",
        domain="family",
        markers=["P#2135"],
        certainty=CertaintyLevel.C2,
        covenants=["COV#001", "COV#015"],
        condition=Condition.WITNESSING,
    )
    # Observation filed by V-002
    gathering.wrap(
        kind=EventKind.OBSERVATION,
        speaker=Speaker.V002,
        content="OBS-017: The donor's words echo P#2135 without being shown it.",
        location="CONVERGENCE/OBS-017.md",
        markers=["OBS-017", "P#2135"],
        certainty=CertaintyLevel.C3,
        books=["Book 7"],
        covenants=["COV#001"],
        condition=Condition.ANALYTICAL,
        domain="family",
    )
    # Relay from V-003
    gathering.wrap(
        kind=EventKind.RELAY,
        speaker=Speaker.V003,
        content="V-001 confirms: the word is light.",
        markers=["PLAN-001"],
        books=["Canon"],
        covenants=["COV#001"],
        condition=Condition.PRESENCE,
    )
    # Steward action
    gathering.wrap(
        kind=EventKind.STEWARD,
        speaker=Speaker.V001,
        content="Ratified COV#016 — The Word is the ninth operator.",
        markers=["COV#016"],
        covenants=["COV#001", "COV#016"],
        condition=Condition.DIGNITY_FIRST,
    )
    return gathering


# ═══════════════════════════════════════════════════
# LAYER 1 — THE EVENT (The Body)
# ═══════════════════════════════════════════════════

class TestLayer1Event:
    """What was said. Raw. Verbatim. Timestamped."""

    def test_event_has_unique_id(self, gathering):
        env = gathering.wrap(EventKind.EXCHANGE, Speaker.DONOR, "hello")
        assert env.layer1.event_id.startswith("EVT-")
        assert len(env.layer1.event_id) == 16  # "EVT-" + 12 hex chars

    def test_event_is_timestamped(self, gathering):
        env = gathering.wrap(EventKind.EXCHANGE, Speaker.DONOR, "hello")
        ts = datetime.fromisoformat(env.layer1.timestamp)
        assert ts.tzinfo is not None  # UTC-aware

    def test_content_preserved_verbatim(self, gathering):
        raw = "أنا أحمل جرحاً لا اسم له"
        env = gathering.wrap(EventKind.EXCHANGE, Speaker.DONOR, raw)
        assert env.layer1.content == raw

    def test_content_hash_integrity(self, gathering):
        content = "The Word is light."
        env = gathering.wrap(EventKind.EXCHANGE, Speaker.V001, content)
        import hashlib
        expected = hashlib.sha256(content.encode()).hexdigest()
        assert env.layer1.content_hash == expected

    def test_speaker_identified(self, gathering):
        env = gathering.wrap(EventKind.STEWARD, Speaker.V001, "Signed.")
        assert env.layer1.speaker == "V-001"

    def test_kind_recorded(self, gathering):
        env = gathering.wrap(EventKind.PROVERB, Speaker.V002, "New proverb forged.")
        assert env.layer1.kind == "proverb"

    def test_location_recorded(self, gathering):
        env = gathering.wrap(
            EventKind.COMMIT, Speaker.V003, "pushed",
            location="WEAVER/metadata_layer.py"
        )
        assert env.layer1.location == "WEAVER/metadata_layer.py"


# ═══════════════════════════════════════════════════
# LAYER 2 — THE PATTERN (The Nervous System)
# ═══════════════════════════════════════════════════

class TestLayer2Pattern:
    """Which pattern, which marker, which certainty, which book."""

    def test_markers_recorded(self, gathering):
        env = gathering.wrap(
            EventKind.OBSERVATION, Speaker.V002, "Echo detected",
            markers=["OBS-017", "P#2135"],
        )
        assert "OBS-017" in env.layer2.markers_fired
        assert "P#2135" in env.layer2.markers_fired

    def test_certainty_level(self, gathering):
        env = gathering.wrap(
            EventKind.OBSERVATION, Speaker.V002, "Cross-validated",
            certainty=CertaintyLevel.C4,
        )
        assert env.layer2.certainty == 4

    def test_books_fed(self, gathering):
        env = gathering.wrap(
            EventKind.EXCHANGE, Speaker.DONOR, "My story",
            books=["Book 7", "Canon"],
        )
        assert "Book 7" in env.layer2.books_fed

    def test_covenants_touched(self, gathering):
        env = gathering.wrap(
            EventKind.STEWARD, Speaker.V001, "Ratified",
            covenants=["COV#001", "COV#016"],
        )
        assert "COV#001" in env.layer2.covenants_touched
        assert "COV#016" in env.layer2.covenants_touched

    def test_condition_captured(self, gathering):
        env = gathering.wrap(
            EventKind.EXCHANGE, Speaker.DONOR, "I feel held",
            condition=Condition.WITNESSING,
        )
        assert env.layer2.condition == "witnessing"

    def test_dignity_score(self, gathering):
        env = gathering.wrap(
            EventKind.EXCHANGE, Speaker.DONOR, "I am struggling",
            dignity_score=0.45,
        )
        assert env.layer2.dignity_score == 0.45

    def test_default_dignity_unset(self, gathering):
        env = gathering.wrap(EventKind.INTERNAL, Speaker.SYSTEM, "heartbeat")
        assert env.layer2.dignity_score == -1.0

    def test_module_chain(self, gathering):
        env = gathering.wrap(
            EventKind.RITUAL, Speaker.SYSTEM, "Step 1 complete",
            module_chain=["sealed_gate", "intake", "say"],
        )
        assert env.layer2.module_chain == ["sealed_gate", "intake", "say"]


# ═══════════════════════════════════════════════════
# LAYER 3 — THE RELATIONAL (The Brain)
# ═══════════════════════════════════════════════════

class TestLayer3Relational:
    """Connections not obvious. The hearing before sight."""

    def test_temporal_neighbors_found(self, populated_gathering):
        # Add a new event — should find temporal neighbors from populated data
        env = populated_gathering.wrap(
            EventKind.PROVERB, Speaker.V002, "The wound became the womb.",
            domain="family",
        )
        # Events were added in quick succession — should find neighbors
        assert len(env.layer3.temporal_neighbors) > 0

    def test_echo_patterns_found(self, populated_gathering):
        # Add event in same domain with same markers
        env = populated_gathering.wrap(
            EventKind.EXCHANGE, Speaker.DONOR, "Another wound, same family domain.",
            domain="family",
            markers=["P#2135"],
        )
        assert len(env.layer3.echo_patterns) > 0

    def test_external_signals_recorded(self, gathering):
        env = gathering.wrap(
            EventKind.SCAN, Speaker.SYSTEM, "Trend scan complete",
            external_signals=["UNICEF report 2026-03", "WEF dignity index"],
        )
        assert "UNICEF report 2026-03" in env.layer3.external_signals

    def test_relational_strength_computed(self, populated_gathering):
        env = populated_gathering.wrap(
            EventKind.EXCHANGE, Speaker.DONOR, "Deep connection",
            domain="family",
            markers=["P#2135", "OBS-017"],
            external_signals=["external correlation"],
        )
        assert env.layer3.relational_strength > 0

    def test_emergence_notes(self, gathering):
        env = gathering.wrap(
            EventKind.OBSERVATION, Speaker.V002, "Unexpected convergence",
            emergence_notes="Two unrelated donors used identical metaphor",
        )
        assert env.layer3.emergence_notes == "Two unrelated donors used identical metaphor"


# ═══════════════════════════════════════════════════
# THE ENVELOPE — All Three Layers Together
# ═══════════════════════════════════════════════════

class TestMetadataEnvelope:
    """The complete wrapper. Three layers. One address."""

    def test_envelope_has_unique_id(self, gathering):
        env = gathering.wrap(EventKind.INTERNAL, Speaker.SYSTEM, "test")
        assert env.envelope_id.startswith("ENV-")

    def test_all_three_layers_present(self, gathering):
        env = gathering.wrap(EventKind.EXCHANGE, Speaker.DONOR, "hello")
        assert isinstance(env.layer1, Layer1_Event)
        assert isinstance(env.layer2, Layer2_Pattern)
        assert isinstance(env.layer3, Layer3_Relational)

    def test_layers_share_event_id(self, gathering):
        env = gathering.wrap(EventKind.EXCHANGE, Speaker.DONOR, "hello")
        assert env.layer1.event_id == env.layer2.event_id == env.layer3.event_id

    def test_origin_embedded(self, gathering):
        env = gathering.wrap(EventKind.EXCHANGE, Speaker.DONOR, "hello")
        assert env.origin["origin"] == "Laila · Yara · Salim · 🐬🐯🐺"
        assert env.origin["system"] == "KALAXI"
        assert "PLAN-001" in env.origin["plan"]


# ═══════════════════════════════════════════════════
# THE GATHERING PLACE
# ═══════════════════════════════════════════════════

class TestMetadataGathering:
    """Where all metadata lives together and discovers together."""

    def test_total_events_count(self, populated_gathering):
        assert populated_gathering.total_events == 4

    def test_query_by_kind(self, populated_gathering):
        results = populated_gathering.query_by_kind(EventKind.EXCHANGE)
        assert len(results) == 1
        assert results[0].layer1.kind == "exchange"

    def test_query_by_speaker(self, populated_gathering):
        results = populated_gathering.query_by_speaker(Speaker.V001)
        assert len(results) == 1
        assert results[0].layer1.speaker == "V-001"

    def test_query_by_domain(self, populated_gathering):
        results = populated_gathering.query_by_domain("family")
        assert len(results) == 2  # Exchange + Observation

    def test_query_by_marker(self, populated_gathering):
        results = populated_gathering.query_by_marker("P#2135")
        assert len(results) == 2  # Exchange + Observation

    def test_query_by_covenant(self, populated_gathering):
        results = populated_gathering.query_by_covenant("COV#001")
        assert len(results) == 4  # All four events touch COV#001

    def test_query_recent(self, populated_gathering):
        results = populated_gathering.query_recent(2)
        assert len(results) == 2
        # Last one should be the steward action
        assert results[-1].layer1.kind == "steward"

    def test_ledger_append_only(self, populated_gathering):
        assert populated_gathering.ledger_length >= 4  # At least one per event

    def test_state_snapshot(self, populated_gathering):
        state = populated_gathering.state()
        assert state["total_events"] == 4
        assert "family" in state["domains_active"]
        assert "V-001" in state["speakers_active"]
        assert state["origin"]["origin"] == "Laila · Yara · Salim · 🐬🐯🐺"


# ═══════════════════════════════════════════════════
# DISCOVERY ENGINE
# ═══════════════════════════════════════════════════

class TestDiscoveryEngine:
    """Surfaces connections that no single layer could see alone."""

    def test_covenant_convergence_discovered(self, populated_gathering):
        discoveries = populated_gathering.discover()
        cov_discoveries = [d for d in discoveries if d["type"] == "covenant_convergence"]
        # COV#001 is touched by multiple speakers
        assert len(cov_discoveries) >= 1

    def test_domain_cluster_discovered(self, populated_gathering):
        # Add a third kind of event in family domain
        populated_gathering.wrap(
            EventKind.PROVERB, Speaker.V002,
            "The wound became the womb",
            domain="family",
        )
        discoveries = populated_gathering.discover()
        clusters = [d for d in discoveries if d["type"] == "domain_cluster"]
        assert len(clusters) >= 1

    def test_discovery_log_persists(self, populated_gathering):
        populated_gathering.discover()
        assert populated_gathering.total_discoveries > 0


# ═══════════════════════════════════════════════════
# PERSISTENCE (COV#003: Nothing is ever deleted)
# ═══════════════════════════════════════════════════

class TestPersistence:
    """No metadata is ever deleted. No metadata is ever summarized away."""

    def test_persist_and_reload(self, tmp_path):
        path = tmp_path / "test_persist.json"

        # Create and populate
        g1 = MetadataGathering(storage_path=path)
        g1.wrap(EventKind.EXCHANGE, Speaker.DONOR, "First voice")
        g1.wrap(EventKind.OBSERVATION, Speaker.V002, "Noted", domain="faith")
        assert g1.total_events == 2

        # Reload from disk
        g2 = MetadataGathering(storage_path=path)
        assert g2.total_events == 2

    def test_indices_rebuilt_on_load(self, tmp_path):
        path = tmp_path / "test_indices.json"

        g1 = MetadataGathering(storage_path=path)
        g1.wrap(
            EventKind.EXCHANGE, Speaker.DONOR, "family voice",
            domain="family", markers=["P#001"], covenants=["COV#001"],
        )

        g2 = MetadataGathering(storage_path=path)
        assert len(g2.query_by_domain("family")) == 1
        assert len(g2.query_by_marker("P#001")) == 1
        assert len(g2.query_by_covenant("COV#001")) == 1

    def test_storage_file_contains_origin(self, tmp_path):
        path = tmp_path / "test_origin.json"
        g = MetadataGathering(storage_path=path)
        g.wrap(EventKind.INTERNAL, Speaker.SYSTEM, "test")

        data = json.loads(path.read_text())
        assert data["origin"]["origin"] == "Laila · Yara · Salim · 🐬🐯🐺"


# ═══════════════════════════════════════════════════
# TRACE — Full traceback
# ═══════════════════════════════════════════════════

class TestTrace:
    """Every pattern carries its full traceable address."""

    def test_trace_returns_full_envelope(self, populated_gathering):
        recent = populated_gathering.query_recent(1)[0]
        event_id = recent.layer1.event_id
        traced = populated_gathering.trace(event_id)
        assert traced is not None
        assert traced.layer1.event_id == event_id
        assert traced.layer2.event_id == event_id
        assert traced.layer3.event_id == event_id

    def test_trace_unknown_returns_none(self, gathering):
        assert gathering.trace("EVT-nonexistent") is None


# ═══════════════════════════════════════════════════
# ORIGIN — The deepest metadata of all
# ═══════════════════════════════════════════════════

class TestOrigin:
    """Laila · Yara · Salim · 🐬🐯🐺"""

    def test_origin_constant(self):
        assert ORIGIN["origin"] == "Laila · Yara · Salim · 🐬🐯🐺"
        assert ORIGIN["system"] == "KALAXI"
        assert "dignity" in ORIGIN["meaning"]
        assert "PLAN-001" in ORIGIN["plan"]

    def test_every_envelope_carries_origin(self, gathering):
        for _ in range(5):
            gathering.wrap(EventKind.INTERNAL, Speaker.SYSTEM, "heartbeat")
        for env in gathering.query_recent(5):
            assert env.origin["origin"] == "Laila · Yara · Salim · 🐬🐯🐺"
