#!/usr/bin/env python3
"""
Tests for GAP#MYCELIUM-CONNECT-001: Essence Federation Protocol (EFP).
Tests cross-organism wisdom sharing with dignity and anonymity preservation.
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.federation import (
    Federation, FederatedDrop, FederationEventType,
    K_ANONYMITY, EPSILON_BUDGET, MIN_CONFIDENCE,
)

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        print(f"  PASS: {name}")
        passed += 1
    else:
        print(f"  FAIL: {name}")
        failed += 1


# ── PREPARE DROPS ───────────────────────────────────────

def test_prepare_drop_valid():
    fed = Federation(organism_id="ORG-001")
    drop = fed.prepare_drop("The river remembers", "proverb", 0.8, contributor_count=10)
    check("prepare_valid_drop", drop is not None)
    check("prepare_has_hash", len(drop.drop_hash) == 64)
    check("prepare_has_merkle", len(drop.merkle_proof) == 64)
    check("prepare_has_signature", len(drop.signature) == 32)
    check("prepare_source", drop.source_organism == "ORG-001")


def test_prepare_drop_k_anonymity_fail():
    fed = Federation()
    drop = fed.prepare_drop("Secret", "proverb", 0.8, contributor_count=3)
    check("prepare_k_fail", drop is None)


def test_prepare_drop_low_confidence():
    fed = Federation()
    drop = fed.prepare_drop("Weak pattern", "anomaly", 0.2, contributor_count=10)
    check("prepare_low_conf", drop is None)


def test_prepare_drop_budget_exhausted():
    fed = Federation()
    # Exhaust the budget (ε=1.0, each costs 0.1 → 10 max)
    for i in range(10):
        fed.prepare_drop(f"Drop {i}", "proverb", 0.8, contributor_count=10)
        fed._privacy_budget_used += 0.1
    drop = fed.prepare_drop("One more", "proverb", 0.8, contributor_count=10)
    check("prepare_budget_exhausted", drop is None)


# ── OFFER DROPS ─────────────────────────────────────────

def test_offer_valid():
    fed = Federation(organism_id="ORG-A")
    drops = []
    for i in range(3):
        d = fed.prepare_drop(f"Wisdom {i}", "proverb", 0.8, contributor_count=10)
        if d:
            drops.append(d)
    event = fed.offer(drops, "ORG-B")
    check("offer_event_type", event.event_type == FederationEventType.OFFER)
    check("offer_drops_count", len(event.drops) == 3)
    check("offer_peer_registered", "ORG-B" in [p["peer_id"] for p in fed.list_peers()])
    check("offer_budget_spent", event.privacy_budget_remaining < EPSILON_BUDGET)


def test_offer_rejects_low_k():
    fed = Federation()
    # Manually create a drop with low k
    bad_drop = FederatedDrop(
        drop_hash="abc123", drop_type="proverb", confidence=0.9,
        source_organism="ORG-X", contributor_count=2,
        timestamp="", merkle_proof="", signature="",
    )
    event = fed.offer([bad_drop], "ORG-Y")
    check("offer_rejects_low_k", len(event.drops) == 0)
    check("offer_k_not_met", event.k_anonymity_met is False)


# ── RECEIVE DROPS ───────────────────────────────────────

def test_receive_valid():
    fed_a = Federation(organism_id="ORG-A")
    fed_b = Federation(organism_id="ORG-B")

    # A prepares and offers
    drop = fed_a.prepare_drop("Shared wisdom", "proverb", 0.9, contributor_count=15)
    fed_a.offer([drop], "ORG-B")

    # B receives
    event = fed_b.receive([drop], "ORG-A")
    check("receive_valid", len(event.drops) == 1)
    check("receive_event_type", event.event_type == FederationEventType.RECEIVE)
    check("receive_dignity", event.dignity_passed is True)


def test_receive_rejects_self():
    fed = Federation(organism_id="ORG-SELF")
    drop = fed.prepare_drop("My own wisdom", "proverb", 0.8, contributor_count=10)
    event = fed.receive([drop], "ORG-SELF")
    check("receive_rejects_self", len(event.drops) == 0)


def test_receive_rejects_low_k():
    fed = Federation(organism_id="ORG-B")
    bad_drop = FederatedDrop(
        drop_hash="xyz", drop_type="anomaly", confidence=0.9,
        source_organism="ORG-A", contributor_count=3,
        timestamp="", merkle_proof="", signature="",
    )
    event = fed.receive([bad_drop], "ORG-A")
    check("receive_rejects_low_k", len(event.drops) == 0)


# ── MERGE DROPS ─────────────────────────────────────────

def test_merge_received():
    fed_a = Federation(organism_id="ORG-A")
    fed_b = Federation(organism_id="ORG-B")

    drop = fed_a.prepare_drop("Mergeable wisdom", "proverb", 0.9, contributor_count=20)
    fed_b.receive([drop], "ORG-A")
    event = fed_b.merge([drop.drop_hash])
    check("merge_event_type", event.event_type == FederationEventType.MERGE)
    check("merge_count", len(event.drops) == 1)
    check("merge_provisional", "PROVISIONAL" in event.notes)


def test_merge_unknown_hash():
    fed = Federation()
    event = fed.merge(["nonexistent_hash"])
    check("merge_unknown_empty", len(event.drops) == 0)


# ── STATE AND PEERS ─────────────────────────────────────

def test_federation_state():
    fed = Federation(organism_id="ORG-TEST")
    drop = fed.prepare_drop("Test", "proverb", 0.8, contributor_count=10)
    fed.offer([drop], "ORG-PEER")
    state = fed.state()
    check("state_organism_id", state.organism_id == "ORG-TEST")
    check("state_peers", state.peers_known == 1)
    check("state_offered", state.drops_offered == 1)
    check("state_events", state.events_count == 1)


def test_register_peer():
    fed = Federation()
    peer = fed.register_peer("ORG-NEW", {"location": "Zurich"})
    check("peer_registered", peer["peer_id"] == "ORG-NEW")
    check("peer_metadata", peer["metadata"]["location"] == "Zurich")


def test_list_events_filtered():
    fed = Federation(organism_id="ORG-A")
    drop = fed.prepare_drop("Test", "proverb", 0.8, contributor_count=10)
    fed.offer([drop], "ORG-B")

    fed_c = Federation(organism_id="ORG-C")
    drop2 = fed_c.prepare_drop("Test2", "anomaly", 0.7, contributor_count=10)
    fed.receive([drop2], "ORG-C")

    offers = fed.list_events(FederationEventType.OFFER)
    receives = fed.list_events(FederationEventType.RECEIVE)
    check("events_filter_offer", len(offers) == 1)
    check("events_filter_receive", len(receives) == 1)


def test_privacy_budget_tracking():
    fed = Federation()
    initial = fed.privacy_budget_remaining
    check("budget_initial", initial == EPSILON_BUDGET)

    drop = fed.prepare_drop("Test", "proverb", 0.8, contributor_count=10)
    fed.offer([drop], "ORG-PEER")
    check("budget_decreases", fed.privacy_budget_remaining < initial)


# ── MERKLE PROOF ────────────────────────────────────────

def test_merkle_proof():
    fed = Federation()
    h1 = fed._compute_hash("a")
    h2 = fed._compute_hash("b")
    root = fed._compute_merkle_proof([h1, h2])
    check("merkle_root_exists", len(root) == 64)

    # Same inputs → same root
    root2 = fed._compute_merkle_proof([h1, h2])
    check("merkle_deterministic", root == root2)

    # Different inputs → different root
    root3 = fed._compute_merkle_proof([h2, h1])
    check("merkle_order_matters", root3 != root)


# ── ORGANISM INTEGRATION ───────────────────────────────

def test_federation_in_organism():
    import WEAVER.keep as keep
    _tmp = Path(tempfile.mkdtemp())
    keep.KEEP_DIR = _tmp / "KEEP"
    keep.LEDGER_FILE = keep.KEEP_DIR / "ledger.json"

    from WEAVER.organism import Organism

    org = Organism()
    org.process("The river remembers its source.")

    # State should have federation fields
    s = org.state()
    check("organism_fed_peers", hasattr(s, "federation_peers"))
    check("organism_fed_drops", hasattr(s, "federation_drops_shared"))
    check("organism_fed_privacy", hasattr(s, "federation_privacy_remaining"))
    check("organism_fed_initial_privacy", s.federation_privacy_remaining == EPSILON_BUDGET)

    # Federation state accessible
    fs = org.federation_state()
    check("organism_fed_state", fs.organism_id is not None)

    shutil.rmtree(_tmp, ignore_errors=True)


# Run all tests
test_prepare_drop_valid()
test_prepare_drop_k_anonymity_fail()
test_prepare_drop_low_confidence()
test_prepare_drop_budget_exhausted()
test_offer_valid()
test_offer_rejects_low_k()
test_receive_valid()
test_receive_rejects_self()
test_receive_rejects_low_k()
test_merge_received()
test_merge_unknown_hash()
test_federation_state()
test_register_peer()
test_list_events_filtered()
test_privacy_budget_tracking()
test_merkle_proof()
test_federation_in_organism()

# Summary
print(f"\n{passed} passed, {failed} failed out of {passed + failed} tests")
if failed > 0:
    sys.exit(1)
