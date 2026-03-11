#!/usr/bin/env python3
"""
Tests for canonicalize.py — Canonicalization + Signing + Emergency Governance
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""
import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from WEAVER.canonicalize import (
    Canonicalizer, ArtifactSigner, EmergencyGovernance,
    EscalationLevel, EMERGENCY_PLAYBOOK,
)


class TestCanonicalizer:
    def test_scan_finds_ids(self):
        canon = Canonicalizer()
        report = canon.scan()
        assert report.total_ids_scanned > 0
        assert report.unique_ids > 0

    def test_manifest_generated(self):
        canon = Canonicalizer()
        canon.scan()
        manifest = canon.canonical_manifest()
        assert manifest["manifest_version"] == "1.0"
        assert len(manifest["entries"]) > 0

    def test_duplicate_report_structure(self):
        canon = Canonicalizer()
        report = canon.scan()
        assert hasattr(report, "duplicate_count")
        assert hasattr(report, "suggested_tiebreakers")
        assert report.timestamp != ""

    def test_tiebreaker_suggestions(self):
        canon = Canonicalizer()
        report = canon.scan()
        for tb in report.suggested_tiebreakers:
            assert "id" in tb
            assert "occurrences" in tb
            assert "policy" in tb


class TestArtifactSigner:
    def test_sign_and_verify(self):
        signer = ArtifactSigner(signer_id="test", signer_role="test-role")
        data = {"test": "value", "number": 42}
        artifact = signer.sign("TEST-001", data)
        assert artifact.content_hash != ""
        assert artifact.signature != ""
        assert signer.verify(artifact, data) is True

    def test_tampered_data_fails_verification(self):
        signer = ArtifactSigner()
        data = {"original": "data"}
        artifact = signer.sign("TEST-002", data)
        tampered = {"original": "TAMPERED"}
        assert signer.verify(artifact, tampered) is False

    def test_sign_manifest(self):
        signer = ArtifactSigner()
        manifest = {"version": "1.0", "entries": {"COV#001": {}}}
        artifact, signed = signer.sign_manifest(manifest)
        assert "_signature" in signed
        assert signed["_signature"]["algorithm"].startswith("HMAC")
        assert signer.verify(artifact, manifest) is True

    def test_chain_grows(self):
        signer = ArtifactSigner()
        signer.sign("A", {"a": 1})
        signer.sign("B", {"b": 2})
        assert signer.chain_length == 2

    def test_canonical_json_deterministic(self):
        signer = ArtifactSigner()
        data1 = {"b": 2, "a": 1}
        data2 = {"a": 1, "b": 2}
        art1 = signer.sign("X", data1)
        art2 = signer.sign("Y", data2)
        assert art1.content_hash == art2.content_hash


class TestEmergencyGovernance:
    def test_escalate_and_resolve(self):
        gov = EmergencyGovernance()
        esc = gov.escalate(
            level=EscalationLevel.ELEVATED,
            trigger="Test trigger",
            description="Test escalation",
        )
        assert esc.record_id.startswith("ESC-")
        assert esc.resolved is False
        assert gov.current_level == EscalationLevel.ELEVATED

        gov.resolve(esc.record_id, "Resolved for testing.")
        assert gov.current_level == EscalationLevel.ROUTINE

    def test_escalation_audit_trail(self):
        gov = EmergencyGovernance()
        esc = gov.escalate(
            level=EscalationLevel.EMERGENCY,
            trigger="Critical test",
            description="Testing audit trail",
        )
        gov.add_audit_entry(esc.record_id, "review", "Steward reviewed.", actor="steward")
        assert len(esc.audit_trail) == 2  # initiation + review

    def test_playbook_has_required_sections(self):
        assert "roles" in EMERGENCY_PLAYBOOK
        assert "escalation_paths" in EMERGENCY_PLAYBOOK
        assert "legal_checklist" in EMERGENCY_PLAYBOOK
        assert "steward" in EMERGENCY_PLAYBOOK["roles"]

    def test_playbook_text_readable(self):
        gov = EmergencyGovernance()
        text = gov.playbook_text()
        assert "KALAXI Emergency Governance Playbook" in text
        assert "steward" in text
        assert "Legal Checklist" in text

    def test_open_escalations(self):
        gov = EmergencyGovernance()
        gov.escalate(EscalationLevel.ELEVATED, "test1", "desc1")
        gov.escalate(EscalationLevel.EMERGENCY, "test2", "desc2")
        assert len(gov.open_escalations) == 2

    def test_constitutional_level(self):
        gov = EmergencyGovernance()
        esc = gov.escalate(
            level=EscalationLevel.CONSTITUTIONAL,
            trigger="Sealed gate compromise attempt",
            description="Testing highest escalation level",
        )
        assert gov.current_level == EscalationLevel.CONSTITUTIONAL
        assert "ethics_reviewer" in esc.roles_notified

    def test_save_escalation_log(self):
        gov = EmergencyGovernance()
        gov.escalate(EscalationLevel.ELEVATED, "test", "desc")
        gov.save_escalation_log()
        log_file = ROOT / "MANIFEST" / "escalation_log.json"
        assert log_file.exists()
        with open(log_file) as f:
            data = json.load(f)
        assert len(data) == 1
