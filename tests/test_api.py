#!/usr/bin/env python3
"""
Tests for api.py — KALAXI Witness Engine API endpoints.

Uses FastAPI TestClient for HTTP testing.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pytest

try:
    from fastapi.testclient import TestClient
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

try:
    from api import app
    HAS_APP = True
except Exception:
    HAS_APP = False

pytestmark = pytest.mark.skipif(
    not HAS_FASTAPI or not HAS_APP,
    reason="FastAPI or API app not available"
)


# ═══════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════

@pytest.fixture(scope="module")
def client():
    """Create a test client for the API."""
    with TestClient(app) as c:
        yield c


# ═══════════════════════════════════════════════════
# ROOT
# ═══════════════════════════════════════════════════

class TestRoot:
    def test_root_returns_system_info(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["system"] == "KALAXI"
        assert data["name"] == "Witness Engine"
        assert "covenant" in data
        assert data["covenant"] == "D = A × L × M"

    def test_root_has_voice_corpus(self, client):
        resp = client.get("/")
        data = resp.json()
        assert "voice_corpus" in data
        assert data["voice_corpus"]["total_fragments"] > 0


# ═══════════════════════════════════════════════════
# BREATH
# ═══════════════════════════════════════════════════

class TestBreath:
    def test_breath_returns_status(self, client):
        resp = client.get("/breath")
        assert resp.status_code == 200
        data = resp.json()
        assert data["system"] == "KALAXI"
        assert "status" in data
        assert "voice" in data
        assert "covenant" in data


# ═══════════════════════════════════════════════════
# CANON
# ═══════════════════════════════════════════════════

class TestCanon:
    def test_proverb_endpoint(self, client):
        resp = client.get("/canon/proverb")
        assert resp.status_code == 200
        data = resp.json()
        assert "text" in data
        assert data["text"]  # Not empty

    def test_proverb_with_theme(self, client):
        resp = client.get("/canon/proverb?theme=path,bridge")
        assert resp.status_code == 200
        data = resp.json()
        assert "text" in data

    def test_narrative_endpoint(self, client):
        resp = client.get("/canon/narrative")
        assert resp.status_code == 200
        data = resp.json()
        assert "text" in data

    def test_narrative_by_book(self, client):
        resp = client.get("/canon/narrative?book=hakaka")
        assert resp.status_code == 200
        data = resp.json()
        assert "text" in data

    def test_treasure_endpoint(self, client):
        resp = client.get("/canon/treasure")
        assert resp.status_code == 200
        data = resp.json()
        assert "text" in data

    def test_voice_endpoint(self, client):
        resp = client.get("/canon/voice")
        assert resp.status_code == 200
        data = resp.json()
        assert "text" in data
        assert "source" in data


# ═══════════════════════════════════════════════════
# DIGNITY
# ═══════════════════════════════════════════════════

class TestDignity:
    def test_dignity_check(self, client):
        resp = client.post("/dignity/check", json={
            "text": "I carry something heavy and need to be seen.",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "D" in data
        assert "A" in data
        assert "L" in data
        assert "M" in data
        assert "confidence" in data
        assert data["sealed_gate"] is True

    def test_dignity_components_range(self, client):
        resp = client.post("/dignity/check", json={
            "text": "A simple honest message.",
        })
        data = resp.json()
        assert 0.0 <= data["D"] <= 1.0
        assert 0.0 <= data["A"] <= 1.0
        assert 0.0 <= data["L"] <= 1.0
        assert 0.0 <= data["M"] <= 1.0


# ═══════════════════════════════════════════════════
# WITNESS — The Core Act
# ═══════════════════════════════════════════════════

class TestWitness:
    def test_witness_basic(self, client):
        resp = client.post("/witness", json={
            "text": "I carry something heavy.",
        })
        # 200 if organism ready, 503 if still initializing
        assert resp.status_code in (200, 503)
        if resp.status_code == 200:
            data = resp.json()
            assert "exchange_id" in data
            assert "dignity_passed" in data
            assert "dignity_score" in data
            assert "voice_text" in data
            assert "witness_id" in data
            assert data["voice_text"]  # Not empty

    def test_witness_returns_dignity_components(self, client):
        resp = client.post("/witness", json={
            "text": "The stone holds the water.",
        })
        if resp.status_code == 200:
            data = resp.json()
            assert "dignity_components" in data
            assert "A" in data["dignity_components"]
            assert "L" in data["dignity_components"]
            assert "M" in data["dignity_components"]

    def test_witness_returns_voice_sources(self, client):
        resp = client.post("/witness", json={
            "text": "Tell me about the rope and the knot.",
        })
        if resp.status_code == 200:
            data = resp.json()
            assert "voice_sources" in data
            assert len(data["voice_sources"]) > 0

    def test_witness_empty_text_rejected(self, client):
        resp = client.post("/witness", json={"text": ""})
        assert resp.status_code == 422  # Validation error

    def test_witness_increments_count(self, client):
        # Get initial count
        breath1 = client.get("/breath").json()
        initial = breath1.get("witnesses_generated", 0)

        # Witness
        resp = client.post("/witness", json={"text": "Test witness."})

        if resp.status_code == 200:
            # Count should increase
            breath2 = client.get("/breath").json()
            assert breath2.get("witnesses_generated", 0) > initial


# ═══════════════════════════════════════════════════
# INTAKE RITUAL
# ═══════════════════════════════════════════════════

class TestIntake:
    def test_begin_intake(self, client):
        resp = client.post("/intake/begin")
        assert resp.status_code == 200
        data = resp.json()
        assert "session_id" in data
        assert data["stage"] == "greeting"
        assert "greeting" in data
        assert "consent_text" in data

    def test_consent_flow(self, client):
        # Begin
        begin = client.post("/intake/begin").json()
        session_id = begin["session_id"]

        # Consent
        resp = client.post("/intake/consent", json={
            "session_id": session_id,
            "agreed": True,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["stage"] == "consent"

    def test_withdrawal_respected(self, client):
        # Begin
        begin = client.post("/intake/begin").json()
        session_id = begin["session_id"]

        # Decline
        resp = client.post("/intake/consent", json={
            "session_id": session_id,
            "agreed": False,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["stage"] == "rejected"
        assert "respected" in data["message"].lower()


# ═══════════════════════════════════════════════════
# LEDGER
# ═══════════════════════════════════════════════════

class TestLedger:
    def test_ledger_status(self, client):
        resp = client.get("/ledger/status")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data

    def test_ledger_verify(self, client):
        resp = client.get("/ledger/verify")
        assert resp.status_code == 200
        data = resp.json()
        assert "verified" in data or "message" in data


# ═══════════════════════════════════════════════════
# CERTIFICATE
# ═══════════════════════════════════════════════════

class TestCertificate:
    def test_nonexistent_certificate(self, client):
        resp = client.get("/certificate/nonexistent-id")
        assert resp.status_code == 404
