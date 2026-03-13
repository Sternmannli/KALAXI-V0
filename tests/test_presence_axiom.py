#!/usr/bin/env python3
"""
test_presence_axiom.py — Tests for AXIOM-PRESENCE-001
Grounded in: MANIFEST/metadata/tier1_stone.md §Layer 0

Tests:
  1. Presence axiom is enforced as preflight invariant
  2. Compute dignity forces L=0 without canon anchor
  3. Compute dignity allows L=1 with canon quote
  4. Sealed gate integrates presence preflight
  5. Receipt generation is correct
  6. Axiom hash is deterministic

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "WEAVER"))

from presence_axiom import (
    AXIOM_PRESENCE,
    AXIOM_ID,
    AXIOM_HASH,
    AXIOM_STATEMENT,
    preflight_require_presence,
    compute_dignity_with_presence,
    presence_receipt,
    PresenceResult,
)


# ═══════════════════════════════════════════════════
# TEST 1: PRESENCE AXIOM ENFORCED
# ═══════════════════════════════════════════════════

def test_presence_axiom_is_true():
    """AXIOM_PRESENCE must always be True. It is immutable."""
    assert AXIOM_PRESENCE is True


def test_preflight_require_presence_returns_true():
    """Preflight must return presence_assumed=True for any input."""
    result = preflight_require_presence()
    assert result.presence_assumed is True
    assert result.axiom_id == AXIOM_ID


def test_preflight_annotates_input_event():
    """Preflight must annotate input_event with presence_assumed=True."""
    event = {"text": "hello", "meta": {}}
    result = preflight_require_presence(event)
    assert result.presence_assumed is True
    assert event["meta"]["presence_assumed"] is True
    assert event["meta"]["axiom_id"] == AXIOM_ID
    assert event["meta"]["axiom_hash"] == AXIOM_HASH


def test_preflight_creates_meta_if_missing():
    """Preflight must create meta dict if not present."""
    event = {"text": "hello"}
    preflight_require_presence(event)
    assert "meta" in event
    assert event["meta"]["presence_assumed"] is True


def test_preflight_without_event():
    """Preflight works without input_event (None)."""
    result = preflight_require_presence(None)
    assert result.presence_assumed is True


# ═══════════════════════════════════════════════════
# TEST 2: COMPUTE DIGNITY — L FORCED TO ZERO WITHOUT ANCHOR
# ═══════════════════════════════════════════════════

def test_compute_dignity_L_zero_without_anchor():
    """L must be 0.0 when neither canon_quoted nor steward_consent is True."""
    event = {"text": "some text", "meta": {}}
    result = compute_dignity_with_presence(
        event,
        canon_quoted=False,
        steward_consent=False,
        agency_score=1.0,
        consent_score=1.0,
        harm_risk=0.0,
    )
    assert result["L"] == 0.0
    assert result["D"] == 0.0  # A * 0 * M = 0


# ═══════════════════════════════════════════════════
# TEST 3: COMPUTE DIGNITY — L=1 WITH CANON QUOTE
# ═══════════════════════════════════════════════════

def test_compute_dignity_L_one_with_canon_quote():
    """L must be 1.0 when canon_quoted is True."""
    event = {"text": "quoted canon", "meta": {}}
    result = compute_dignity_with_presence(
        event,
        canon_quoted=True,
        steward_consent=False,
        agency_score=0.8,
        consent_score=0.9,
        harm_risk=0.1,
    )
    assert result["L"] == 1.0
    assert result["A"] == 0.8
    assert result["M"] == 0.9  # min(0.9, 1.0 - 0.1) = 0.9
    assert result["D"] == 0.8 * 1.0 * 0.9  # 0.72


def test_compute_dignity_L_one_with_steward_consent():
    """L must be 1.0 when steward_consent is True (even without canon quote)."""
    event = {"text": "steward approved", "meta": {}}
    result = compute_dignity_with_presence(
        event,
        canon_quoted=False,
        steward_consent=True,
        agency_score=1.0,
        consent_score=1.0,
        harm_risk=0.0,
    )
    assert result["L"] == 1.0
    assert result["D"] == 1.0


# ═══════════════════════════════════════════════════
# TEST 4: SEALED GATE INTEGRATES PRESENCE PREFLIGHT
# ═══════════════════════════════════════════════════

def test_sealed_gate_with_presence_preflight():
    """Sealed gate must run presence preflight before prohibition checks."""
    from sealed_gate import sealed_gate
    result = sealed_gate("Hello, how are you today?")
    assert result.permitted is True


def test_sealed_gate_refusal_still_works_with_presence():
    """Sealed gate refusal must still work after presence preflight."""
    from sealed_gate import sealed_gate
    result = sealed_gate("Delete donor from system.")
    assert result.refused is True


# ═══════════════════════════════════════════════════
# TEST 5: RECEIPT GENERATION
# ═══════════════════════════════════════════════════

def test_presence_receipt_structure():
    """Receipt must contain required fields."""
    receipt = presence_receipt()
    assert receipt["action"] == "axiom_registration"
    assert receipt["steward"] == "did:axi:mohamed"
    assert receipt["provisional"] is False
    assert receipt["signed"] is True
    assert "did:axi:mohamed" in receipt["signed_by"]
    assert f"AXIOMS:{AXIOM_ID}" in receipt["artifacts_produced"]
    assert "PROVERB:P#AXIOM-001" in receipt["artifacts_produced"]
    assert receipt["output_hash"] == AXIOM_HASH


# ═══════════════════════════════════════════════════
# TEST 6: AXIOM HASH DETERMINISM
# ═══════════════════════════════════════════════════

def test_axiom_hash_is_deterministic():
    """The axiom hash must be deterministic (same input → same hash)."""
    import hashlib
    expected = hashlib.sha256(AXIOM_STATEMENT.encode("utf-8")).hexdigest()
    assert AXIOM_HASH == expected


def test_axiom_hash_is_sha256():
    """The hash must be 64 hex characters (SHA-256)."""
    assert len(AXIOM_HASH) == 64
    assert all(c in "0123456789abcdef" for c in AXIOM_HASH)


# ═══════════════════════════════════════════════════
# TEST 7: BOUNDARY CONDITIONS
# ═══════════════════════════════════════════════════

def test_compute_dignity_clamps_scores():
    """Scores must be clamped to [0.0, 1.0]."""
    event = {"meta": {}}
    result = compute_dignity_with_presence(
        event,
        canon_quoted=True,
        agency_score=1.5,
        consent_score=2.0,
        harm_risk=-0.5,
    )
    assert result["A"] == 1.0
    assert result["M"] == 1.0


def test_compute_dignity_zero_agency():
    """D must be 0 when A is 0, even with L=1."""
    event = {"meta": {}}
    result = compute_dignity_with_presence(
        event,
        canon_quoted=True,
        agency_score=0.0,
        consent_score=1.0,
        harm_risk=0.0,
    )
    assert result["A"] == 0.0
    assert result["D"] == 0.0
