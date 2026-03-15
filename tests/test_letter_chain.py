#!/usr/bin/env python3
"""
Tests for the letter ontology, chain validator, and witness certificate.

Tests that the Arabic letter connection rules are enforced:
- Alef is write-once, always isolated, non-connecting
- Ba has positional flow (initial → medial → final)
- Ta undergoes terminal transformation to isolated on D=0
- Non-connectors terminate chains
- The witness certificate generates on halt

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import pytest
import json
from pathlib import Path

from WEAVER.letter_ontology import (
    ALL_LETTERS, ALEF, BA, TA, DAL, RA, WAW,
    NON_CONNECTORS, CONNECTORS,
    PositionalForm, SomaticOrigin,
    can_join, validate_positional_form, is_halt_capable,
    ontology_summary, letters_by_origin,
)
from WEAVER.chain_validator import (
    ChainEntry, EntryType, ValidationError,
    validate_entry, validate_and_append,
)
from WEAVER.witness_certificate import (
    DignitySnapshot, Subject, InstitutionalContext,
    CoordinatesOfFailure, WitnessCertificate,
    generate_certificate, save_certificate,
)


# ============================================================
# Letter Ontology Tests
# ============================================================

class TestLetterOntology:
    """Test the 28-letter ontology and its properties."""

    def test_total_letters(self):
        assert len(ALL_LETTERS) == 28

    def test_non_connectors_count(self):
        # Alef, Dal, Dhal, Ra, Zay, Waw = 6 non-connectors
        assert len(NON_CONNECTORS) == 6

    def test_connectors_count(self):
        assert len(CONNECTORS) == 22

    def test_alef_properties(self):
        assert ALEF.connects_forward is False
        assert ALEF.somatic_origin == SomaticOrigin.THROAT
        assert ALEF.allowed_forms == {PositionalForm.ISOLATED}
        assert ALEF.abjad_value == 1

    def test_ba_properties(self):
        assert BA.connects_forward is True
        assert BA.somatic_origin == SomaticOrigin.LIPS
        assert PositionalForm.INITIAL in BA.allowed_forms
        assert PositionalForm.MEDIAL in BA.allowed_forms
        assert PositionalForm.FINAL in BA.allowed_forms
        assert PositionalForm.ISOLATED not in BA.allowed_forms

    def test_ta_properties(self):
        assert TA.connects_forward is True
        # Ta is halt-capable: normally connects but can be isolated
        assert PositionalForm.ISOLATED in TA.allowed_forms
        assert PositionalForm.INITIAL in TA.allowed_forms

    def test_non_connectors_are_always_isolated(self):
        for name in NON_CONNECTORS:
            letter = ALL_LETTERS[name]
            assert letter.allowed_forms == {PositionalForm.ISOLATED}, \
                f"Non-connector {name} should only allow isolated form"

    def test_can_join(self):
        assert can_join("ba", "ta") is True
        assert can_join("alef", "ba") is False
        assert can_join("dal", "ba") is False
        assert can_join("ra", "ta") is False

    def test_validate_positional_form(self):
        assert validate_positional_form("alef", PositionalForm.ISOLATED) is True
        assert validate_positional_form("alef", PositionalForm.INITIAL) is False
        assert validate_positional_form("ba", PositionalForm.INITIAL) is True
        assert validate_positional_form("ba", PositionalForm.ISOLATED) is False
        assert validate_positional_form("ta", PositionalForm.ISOLATED) is True

    def test_is_halt_capable(self):
        assert is_halt_capable("ta") is True
        assert is_halt_capable("ba") is False
        assert is_halt_capable("alef") is False

    def test_somatic_layers_cover_all_letters(self):
        all_in_layers = set()
        for origin in SomaticOrigin:
            for letter in letters_by_origin(origin):
                all_in_layers.add(letter.name)
        assert all_in_layers == set(ALL_LETTERS.keys())

    def test_ontology_summary(self):
        summary = ontology_summary()
        assert "28" in summary
        assert "Non-connectors" in summary
        assert "Throat" in summary


# ============================================================
# Chain Validator Tests
# ============================================================

class TestChainValidator:
    """Test the connection rules enforcement."""

    def _state(self):
        return {"alef_ids": set(), "open_sessions": set(), "halt_threshold": 0.0001}

    # --- Alef Rules ---

    def test_alef_must_be_isolated(self):
        entry = ChainEntry(
            entry_id="alef-01",
            letter="alef",
            positional_form=PositionalForm.INITIAL,
        )
        violations = validate_entry(entry, self._state())
        assert any("A.3" in v for v in violations)

    def test_alef_write_once(self):
        state = self._state()
        state["alef_ids"] = {"alef-01"}
        entry = ChainEntry(
            entry_id="alef-01",
            letter="alef",
            positional_form=PositionalForm.ISOLATED,
        )
        violations = validate_entry(entry, state)
        assert any("A.1" in v for v in violations)

    def test_alef_supersession_requires_quorum(self):
        state = self._state()
        state["alef_ids"] = {"alef-01"}
        entry = ChainEntry(
            entry_id="alef-01",
            letter="alef",
            positional_form=PositionalForm.ISOLATED,
            entry_type=EntryType.SUPERSESSION,
            has_quorum=False,
        )
        violations = validate_entry(entry, state)
        assert any("quorum" in v.lower() for v in violations)

    def test_alef_supersession_with_quorum_passes(self):
        state = self._state()
        state["alef_ids"] = {"alef-01"}
        entry = ChainEntry(
            entry_id="alef-01",
            letter="alef",
            positional_form=PositionalForm.ISOLATED,
            entry_type=EntryType.SUPERSESSION,
            has_quorum=True,
        )
        violations = validate_entry(entry, state)
        assert len(violations) == 0

    def test_valid_alef(self):
        entry = ChainEntry(
            entry_id="alef-new",
            letter="alef",
            positional_form=PositionalForm.ISOLATED,
        )
        violations = validate_entry(entry, self._state())
        assert len(violations) == 0

    # --- Ba Rules ---

    def test_ba_initial_requires_session_id(self):
        entry = ChainEntry(
            entry_id="ba-01",
            letter="ba",
            positional_form=PositionalForm.INITIAL,
            session_id="",
        )
        violations = validate_entry(entry, self._state())
        assert any("B.2" in v for v in violations)

    def test_ba_medial_requires_valid_session(self):
        state = self._state()
        state["open_sessions"] = {"sess-001"}
        entry = ChainEntry(
            entry_id="ba-02",
            letter="ba",
            positional_form=PositionalForm.MEDIAL,
            session_id="sess-999",  # Not in open_sessions
        )
        violations = validate_entry(entry, state)
        assert any("B.2" in v for v in violations)

    def test_ba_final_requires_commit_hash(self):
        entry = ChainEntry(
            entry_id="ba-03",
            letter="ba",
            positional_form=PositionalForm.FINAL,
            commit_hash="",
        )
        violations = validate_entry(entry, self._state())
        assert any("B.2" in v for v in violations)

    def test_ba_after_nonconnector_must_be_initial(self):
        prev = ChainEntry(
            entry_id="alef-01",
            letter="alef",
            positional_form=PositionalForm.ISOLATED,
        )
        entry = ChainEntry(
            entry_id="ba-01",
            letter="ba",
            positional_form=PositionalForm.MEDIAL,
            session_id="sess-001",
        )
        state = self._state()
        state["open_sessions"] = {"sess-001"}
        violations = validate_entry(entry, state, prev_entry=prev)
        assert any("B.3" in v or "non-connector" in v.lower() for v in violations)

    def test_valid_ba_flow(self):
        chain = []
        state = self._state()

        # Ba initial
        ba_i = ChainEntry(
            entry_id="ba-i",
            letter="ba",
            positional_form=PositionalForm.INITIAL,
            session_id="sess-001",
        )
        validate_and_append(ba_i, chain, state)

        # Ba medial
        ba_m = ChainEntry(
            entry_id="ba-m",
            letter="ba",
            positional_form=PositionalForm.MEDIAL,
            session_id="sess-001",
        )
        validate_and_append(ba_m, chain, state)

        # Ba final
        ba_f = ChainEntry(
            entry_id="ba-f",
            letter="ba",
            positional_form=PositionalForm.FINAL,
            session_id="sess-001",
            commit_hash="sha256:abc123",
        )
        validate_and_append(ba_f, chain, state)

        assert len(chain) == 3

    # --- Ta Rules ---

    def test_ta_mufrad_requires_dignity_snapshot(self):
        entry = ChainEntry(
            entry_id="ta-halt",
            letter="ta",
            positional_form=PositionalForm.ISOLATED,
            dignity_snapshot=None,
        )
        violations = validate_entry(entry, self._state())
        assert any("T.1" in v for v in violations)

    def test_ta_mufrad_requires_d_zero(self):
        entry = ChainEntry(
            entry_id="ta-halt",
            letter="ta",
            positional_form=PositionalForm.ISOLATED,
            dignity_snapshot=DignitySnapshot(A=0.5, L=0.5, M=0.5),
        )
        violations = validate_entry(entry, self._state())
        assert any("T.1" in v for v in violations)

    def test_ta_mufrad_requires_dual_signatures(self):
        entry = ChainEntry(
            entry_id="ta-halt",
            letter="ta",
            positional_form=PositionalForm.ISOLATED,
            dignity_snapshot=DignitySnapshot(A=0.5, L=0.0, M=0.5),
            system_signature="",
            human_witness_signatures=[],
        )
        violations = validate_entry(entry, self._state())
        assert any("T.3" in v for v in violations)

    def test_valid_ta_halt(self):
        entry = ChainEntry(
            entry_id="ta-halt",
            letter="ta",
            positional_form=PositionalForm.ISOLATED,
            dignity_snapshot=DignitySnapshot(A=0.41, L=0.0, M=0.52),
            system_signature="sig:system",
            human_witness_signatures=["sig:clerk_12"],
        )
        violations = validate_entry(entry, self._state())
        assert len(violations) == 0

    def test_nothing_follows_ta_mufrad(self):
        prev = ChainEntry(
            entry_id="ta-halt",
            letter="ta",
            positional_form=PositionalForm.ISOLATED,
            entry_type=EntryType.HALT,
        )
        entry = ChainEntry(
            entry_id="ba-next",
            letter="ba",
            positional_form=PositionalForm.INITIAL,
            session_id="sess-002",
        )
        violations = validate_entry(entry, self._state(), prev_entry=prev)
        assert any("T.2" in v for v in violations)

    # --- Full Flow: Ba → Ta → Halt ---

    def test_full_flow_to_halt(self):
        chain = []
        state = self._state()

        # Alef: constitution
        alef = ChainEntry(
            entry_id="alef-01",
            letter="alef",
            positional_form=PositionalForm.ISOLATED,
        )
        validate_and_append(alef, chain, state)

        # Ba initial: intake
        ba_i = ChainEntry(
            entry_id="ba-i",
            letter="ba",
            positional_form=PositionalForm.INITIAL,
            session_id="sess-custody-001",
        )
        validate_and_append(ba_i, chain, state)

        # Ba medial: process evidence
        ba_m = ChainEntry(
            entry_id="ba-m",
            letter="ba",
            positional_form=PositionalForm.MEDIAL,
            session_id="sess-custody-001",
        )
        validate_and_append(ba_m, chain, state)

        # Ba final: commit
        ba_f = ChainEntry(
            entry_id="ba-f",
            letter="ba",
            positional_form=PositionalForm.FINAL,
            session_id="sess-custody-001",
            commit_hash="sha256:evidence_bundle",
        )
        validate_and_append(ba_f, chain, state)

        # Ta initial: begin testimony
        ta_i = ChainEntry(
            entry_id="ta-i",
            letter="ta",
            positional_form=PositionalForm.INITIAL,
            session_id="sess-custody-001",
        )
        validate_and_append(ta_i, chain, state)

        # Ta medial: compute dignity
        ta_m = ChainEntry(
            entry_id="ta-m",
            letter="ta",
            positional_form=PositionalForm.MEDIAL,
            session_id="sess-custody-001",
        )
        validate_and_append(ta_m, chain, state)

        # Ta isolated: HALT — L = 0
        ta_halt = ChainEntry(
            entry_id="ta-halt",
            letter="ta",
            positional_form=PositionalForm.ISOLATED,
            dignity_snapshot=DignitySnapshot(A=0.41, L=0.0, M=0.52),
            system_signature="sig:kalaxi_system_key",
            human_witness_signatures=["sig:witness_clerk_12"],
        )
        validate_and_append(ta_halt, chain, state)

        assert len(chain) == 7
        assert chain[-1].entry_type == EntryType.HALT


# ============================================================
# Witness Certificate Tests
# ============================================================

class TestWitnessCertificate:
    """Test the witness certificate generator."""

    def test_dignity_snapshot_halt(self):
        d = DignitySnapshot(A=0.5, L=0.0, M=0.8)
        assert d.D == 0.0
        assert d.halted is True
        assert d.halt_reason == "L_ZERO"

    def test_dignity_snapshot_no_halt(self):
        d = DignitySnapshot(A=0.5, L=0.5, M=0.5)
        assert d.D == 0.125
        assert d.halted is False

    def test_dignity_multi_zero(self):
        d = DignitySnapshot(A=0.0, L=0.0, M=0.5)
        assert d.halt_reason == "MULTI_ZERO"

    def test_generate_certificate_requires_halt(self):
        d = DignitySnapshot(A=0.5, L=0.5, M=0.5)
        with pytest.raises(ValueError, match="no grounds to halt"):
            generate_certificate(
                dignity=d,
                subject=Subject("p:1", "parent"),
                context=InstitutionalContext("court:test", "test"),
                coordinates=CoordinatesOfFailure("L", "node", "rule"),
            )

    def test_generate_certificate_on_halt(self):
        d = DignitySnapshot(A=0.41, L=0.0, M=0.52)
        cert = generate_certificate(
            dignity=d,
            subject=Subject("p:xyz", "parent", "custody case"),
            context=InstitutionalContext(
                "court:zurich-family", "child-custody",
                "2026-0043", "evidence_evaluation",
            ),
            coordinates=CoordinatesOfFailure(
                axis="L",
                node_id="legibility-extractor-v2",
                rule_id="L-EX-07",
                inputs_present=["doc:passport", "doc:journal"],
                missing_or_unreadable=["doc:call_logs", "doc:home_visit"],
                machine_explanation="Dialect not supported.",
                human_annotation="Cannot form reliable picture.",
            ),
            prev_hash="sha256:deadbeef",
        )

        assert cert.status == "HALTED"
        assert cert.letter == "ta"
        assert cert.positional_form == "isolated"
        assert cert.halt_reason_code == "L_ZERO"
        assert cert.dignity.L == 0.0
        assert cert.certificate_hash  # non-empty

    def test_chain_entry_format(self):
        d = DignitySnapshot(A=0.41, L=0.0, M=0.52)
        cert = generate_certificate(
            dignity=d,
            subject=Subject("p:xyz", "parent"),
            context=InstitutionalContext("court:test", "custody"),
            coordinates=CoordinatesOfFailure("L", "node", "rule"),
        )
        entry = cert.to_chain_entry()
        assert entry["status"] == "HALTED"
        assert entry["letter"] == "ta"
        assert entry["positional_form"] == "isolated"
        assert entry["dignity_snapshot"]["L"] == 0.0

    def test_legal_view_contains_key_sections(self):
        d = DignitySnapshot(A=0.41, L=0.0, M=0.52)
        cert = generate_certificate(
            dignity=d,
            subject=Subject("p:xyz", "parent", "custody"),
            context=InstitutionalContext("court:zurich", "custody"),
            coordinates=CoordinatesOfFailure(
                "L", "node-1", "L-EX-07",
                inputs_present=["passport"],
                missing_or_unreadable=["call_logs"],
                machine_explanation="Dialect mismatch.",
                human_annotation="Cannot witness.",
            ),
        )
        legal = cert.to_legal_view()

        assert "WITNESS CERTIFICATE OF INSTITUTIONAL BLINDNESS" in legal
        assert "CRITICAL FAILURE" in legal
        assert "NEGATIVE PROOF" in legal
        assert "refuses to proceed" in legal
        assert "passport" in legal
        assert "call_logs" in legal
        assert "Dialect mismatch" in legal

    def test_save_certificate(self, tmp_path, monkeypatch):
        import WEAVER.witness_certificate as wc
        monkeypatch.setattr(wc, "CERTIFICATE_DIR", tmp_path)

        d = DignitySnapshot(A=0.0, L=0.5, M=0.5)
        cert = generate_certificate(
            dignity=d,
            subject=Subject("p:1", "claimant"),
            context=InstitutionalContext("agency:test", "asylum"),
            coordinates=CoordinatesOfFailure("A", "node", "rule"),
        )
        json_path = save_certificate(cert)

        assert json_path.exists()
        legal_path = tmp_path / f"{cert.certificate_id}_legal.txt"
        assert legal_path.exists()

        with open(json_path) as f:
            data = json.load(f)
        assert data["status"] == "HALTED"
