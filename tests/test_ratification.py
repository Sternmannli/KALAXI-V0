#!/usr/bin/env python3
"""
test_ratification.py — Tests for the KALAXI Ratification Engine
Covers: lifecycle transitions, thermal delays, sign-offs, signatures,
        pre-launch exception, supersession, persistence, bootstrap, CLI.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import sys
import pytest
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.ratification import (
    RatificationEngine, RatificationError,
    ElementState, ElementType, SignOff,
    RatificationElement, THERMAL_DELAYS, SIGNOFF_REQUIREMENTS,
    ratification_summary, ratification_commit,
    get_engine,
)
from WEAVER.canonicalize import ArtifactSigner


# ═══════════════════════════════════════════════════
# LIFECYCLE TESTS
# ═══════════════════════════════════════════════════

class TestLifecycle:
    """Test the three-state lifecycle: COMMITTED → PROVISIONAL → RATIFIED."""

    def setup_method(self):
        self.engine = RatificationEngine(pre_launch=True)

    def test_commit_creates_committed_element(self):
        elem = self.engine.commit("COV#TEST-001", ElementType.COVENANT,
                                  "Test Covenant", "A test")
        assert elem.state == ElementState.COMMITTED
        assert elem.element_id == "COV#TEST-001"
        assert elem.element_type == ElementType.COVENANT
        assert elem.name == "Test Covenant"

    def test_duplicate_commit_raises(self):
        self.engine.commit("COV#DUP", ElementType.COVENANT, "Dup", "test")
        with pytest.raises(RatificationError, match="already registered"):
            self.engine.commit("COV#DUP", ElementType.COVENANT, "Dup2", "test2")

    def test_offer_to_threshold(self):
        self.engine.commit("P#TEST-001", ElementType.PROVERB, "Test Proverb", "A test")
        elem = self.engine.offer_to_threshold("P#TEST-001")
        assert elem.state == ElementState.PROVISIONAL
        assert elem.provisional_at is not None
        assert elem.thermal_delay_expires is not None

    def test_offer_non_committed_raises(self):
        self.engine.commit("P#TEST-002", ElementType.PROVERB, "Test", "test")
        self.engine.offer_to_threshold("P#TEST-002")
        with pytest.raises(RatificationError, match="not COMMITTED"):
            self.engine.offer_to_threshold("P#TEST-002")

    def test_full_lifecycle_proverb(self):
        """Proverb: commit → offer → sign (steward) → ratify."""
        self.engine.commit("P#LC-001", ElementType.PROVERB, "Lifecycle Proverb", "test")
        self.engine.offer_to_threshold("P#LC-001")
        self.engine.sign_off("P#LC-001", "steward", "V-001", "Mohamed Farag")
        elem, signed = self.engine.ratify("P#LC-001")
        assert elem.state == ElementState.RATIFIED
        assert elem.ratified_at is not None
        assert signed.signature

    def test_full_lifecycle_covenant(self):
        """Covenant: commit → offer → sign (owner + ethics) → ratify."""
        self.engine.commit("COV#LC-001", ElementType.COVENANT, "Lifecycle Covenant", "test")
        self.engine.offer_to_threshold("COV#LC-001")
        self.engine.sign_off("COV#LC-001", "canonical_owner", "V-001", "Mohamed Farag")
        self.engine.sign_off("COV#LC-001", "ethics_reviewer", "V-002", "Claude")
        elem, signed = self.engine.ratify("COV#LC-001")
        assert elem.state == ElementState.RATIFIED
        assert len(elem.sign_offs) == 2

    def test_ratify_without_signoffs_raises(self):
        self.engine.commit("COV#NOSIGN", ElementType.COVENANT, "No Sign", "test")
        self.engine.offer_to_threshold("COV#NOSIGN")
        with pytest.raises(RatificationError, match="missing sign-offs"):
            self.engine.ratify("COV#NOSIGN")

    def test_ratify_non_provisional_raises(self):
        self.engine.commit("P#NOTPROV", ElementType.PROVERB, "Not Prov", "test")
        with pytest.raises(RatificationError, match="not PROVISIONAL"):
            self.engine.ratify("P#NOTPROV")


# ═══════════════════════════════════════════════════
# SIGN-OFF TESTS
# ═══════════════════════════════════════════════════

class TestSignOff:
    """Test sign-off recording and validation."""

    def setup_method(self):
        self.engine = RatificationEngine(pre_launch=True)
        self.engine.commit("COV#SIGN-001", ElementType.COVENANT, "Sign Test", "test")
        self.engine.offer_to_threshold("COV#SIGN-001")

    def test_valid_signoff(self):
        elem = self.engine.sign_off("COV#SIGN-001", "canonical_owner", "V-001", "Mohamed")
        assert len(elem.sign_offs) == 1
        assert elem.sign_offs[0].role == "canonical_owner"

    def test_duplicate_role_signoff_raises(self):
        self.engine.sign_off("COV#SIGN-001", "canonical_owner", "V-001", "Mohamed")
        with pytest.raises(RatificationError, match="already signed"):
            self.engine.sign_off("COV#SIGN-001", "canonical_owner", "V-001", "Mohamed")

    def test_invalid_role_raises(self):
        with pytest.raises(RatificationError, match="not required"):
            self.engine.sign_off("COV#SIGN-001", "random_role", "V-003", "Nobody")

    def test_signoff_on_committed_raises(self):
        self.engine.commit("P#COMMITTED", ElementType.PROVERB, "C", "test")
        with pytest.raises(RatificationError, match="PROVISIONAL"):
            self.engine.sign_off("P#COMMITTED", "steward", "V-001", "Mohamed")


# ═══════════════════════════════════════════════════
# THERMAL DELAY TESTS
# ═══════════════════════════════════════════════════

class TestThermalDelay:
    """Test thermal delay enforcement."""

    def test_prelaunch_bypasses_thermal_delay(self):
        engine = RatificationEngine(pre_launch=True)
        engine.commit("COV#THERMAL-001", ElementType.COVENANT, "Thermal Test", "test")
        elem = engine.offer_to_threshold("COV#THERMAL-001")
        # Pre-launch: thermal expires immediately
        assert elem.thermal_delay_expires == elem.provisional_at

    def test_postlaunch_enforces_thermal_delay(self):
        engine = RatificationEngine(pre_launch=False)
        engine.commit("COV#THERMAL-002", ElementType.COVENANT, "Thermal Test", "test")
        elem = engine.offer_to_threshold("COV#THERMAL-002")
        # 90-day delay for covenants
        offered = datetime.fromisoformat(elem.provisional_at)
        expires = datetime.fromisoformat(elem.thermal_delay_expires)
        assert (expires - offered).days == 90

    def test_postlaunch_ratify_before_expiry_raises(self):
        engine = RatificationEngine(pre_launch=False)
        engine.commit("COV#EARLY", ElementType.COVENANT, "Early", "test")
        engine.offer_to_threshold("COV#EARLY")
        engine.sign_off("COV#EARLY", "canonical_owner", "V-001", "Mohamed")
        engine.sign_off("COV#EARLY", "ethics_reviewer", "V-002", "Claude")
        with pytest.raises(RatificationError, match="thermal delay not expired"):
            engine.ratify("COV#EARLY")

    def test_patch_has_zero_delay(self):
        engine = RatificationEngine(pre_launch=False)
        engine.commit("PATCH#001", ElementType.PATCH, "Fix", "test")
        elem = engine.offer_to_threshold("PATCH#001")
        assert elem.thermal_delay_days == 0

    def test_seed_has_seven_day_delay(self):
        assert THERMAL_DELAYS[ElementType.SEED] == 7

    def test_covenant_has_ninety_day_delay(self):
        assert THERMAL_DELAYS[ElementType.COVENANT] == 90

    def test_centre_shift_has_thousand_day_delay(self):
        assert THERMAL_DELAYS[ElementType.CENTRE_SHIFT] == 1000


# ═══════════════════════════════════════════════════
# SIGNATURE TESTS
# ═══════════════════════════════════════════════════

class TestSignature:
    """Test cryptographic signing at ratification."""

    def setup_method(self):
        self.signer = ArtifactSigner(signer_id="V-002", signer_role="steward-system")
        self.engine = RatificationEngine(signer=self.signer, pre_launch=True)

    def test_ratification_produces_signature(self):
        self.engine.commit("P#SIG-001", ElementType.PROVERB, "Sig Test", "test")
        self.engine.offer_to_threshold("P#SIG-001")
        self.engine.sign_off("P#SIG-001", "steward", "V-001", "Mohamed")
        elem, signed = self.engine.ratify("P#SIG-001")
        assert elem.signature is not None
        assert elem.content_hash is not None
        assert len(elem.signature) > 10

    def test_signature_verification(self):
        self.engine.commit("P#VER-001", ElementType.PROVERB, "Verify Test", "test")
        self.engine.offer_to_threshold("P#VER-001")
        self.engine.sign_off("P#VER-001", "steward", "V-001", "Mohamed")
        self.engine.ratify("P#VER-001")
        assert self.engine.verify("P#VER-001") is True

    def test_unratified_verify_returns_false(self):
        self.engine.commit("P#UNRAT", ElementType.PROVERB, "Unrat", "test")
        self.engine.offer_to_threshold("P#UNRAT")
        assert self.engine.verify("P#UNRAT") is False


# ═══════════════════════════════════════════════════
# SUPERSESSION TESTS (COV#NEW-F)
# ═══════════════════════════════════════════════════

class TestSupersession:
    """No deletion — only supersession via new ID."""

    def setup_method(self):
        self.engine = RatificationEngine(pre_launch=True)

    def test_supersede_marks_old_element(self):
        self.engine.commit("COV#OLD", ElementType.COVENANT, "Old", "test")
        self.engine.commit("COV#NEW", ElementType.COVENANT, "New", "test")
        old = self.engine.supersede("COV#OLD", "COV#NEW")
        assert old.superseded_by == "COV#NEW"

    def test_supersede_self_raises(self):
        self.engine.commit("COV#SELF", ElementType.COVENANT, "Self", "test")
        with pytest.raises(RatificationError, match="Cannot supersede"):
            self.engine.supersede("COV#SELF", "COV#SELF")

    def test_supersede_nonexistent_new_raises(self):
        self.engine.commit("COV#EXISTS", ElementType.COVENANT, "Exists", "test")
        with pytest.raises(RatificationError, match="not registered"):
            self.engine.supersede("COV#EXISTS", "COV#GHOST")


# ═══════════════════════════════════════════════════
# FAST PATH TESTS
# ═══════════════════════════════════════════════════

class TestFastPath:
    """Test ratify_immediate (pre-launch fast path)."""

    def test_ratify_immediate(self):
        engine = RatificationEngine(pre_launch=True)
        elem, signed = engine.ratify_immediate(
            "P#FAST-001", ElementType.PROVERB, "Fast Proverb", "Quick test"
        )
        assert elem.state == ElementState.RATIFIED
        assert elem.pre_launch_exception is True
        assert signed.signature

    def test_ratify_immediate_covenant(self):
        engine = RatificationEngine(pre_launch=True)
        elem, signed = engine.ratify_immediate(
            "COV#FAST-001", ElementType.COVENANT, "Fast Covenant", "Quick test"
        )
        assert elem.state == ElementState.RATIFIED
        assert len(elem.sign_offs) == 2  # canonical_owner + ethics_reviewer

    def test_ratify_immediate_postlaunch_raises(self):
        engine = RatificationEngine(pre_launch=False)
        with pytest.raises(RatificationError, match="only valid during pre-launch"):
            engine.ratify_immediate("P#FAIL", ElementType.PROVERB, "Fail", "test")


# ═══════════════════════════════════════════════════
# QUERY TESTS
# ═══════════════════════════════════════════════════

class TestQueries:
    """Test query methods."""

    def setup_method(self):
        self.engine = RatificationEngine(pre_launch=True)
        # Create elements in various states
        self.engine.commit("P#Q1", ElementType.PROVERB, "Q1", "test")
        self.engine.commit("P#Q2", ElementType.PROVERB, "Q2", "test")
        self.engine.offer_to_threshold("P#Q2")
        self.engine.commit("P#Q3", ElementType.PROVERB, "Q3", "test")
        self.engine.offer_to_threshold("P#Q3")
        self.engine.sign_off("P#Q3", "steward", "V-001", "Mohamed")
        self.engine.ratify("P#Q3")

    def test_committed_query(self):
        assert len(self.engine.committed()) == 1
        assert self.engine.committed()[0].element_id == "P#Q1"

    def test_provisional_query(self):
        assert len(self.engine.provisional()) == 1
        assert self.engine.provisional()[0].element_id == "P#Q2"

    def test_ratified_query(self):
        assert len(self.engine.ratified()) == 1
        assert self.engine.ratified()[0].element_id == "P#Q3"

    def test_awaiting_signoff(self):
        awaiting = self.engine.awaiting_signoff()
        assert len(awaiting) == 1
        assert awaiting[0].element_id == "P#Q2"

    def test_ready_to_ratify(self):
        # P#Q2 is provisional but has no sign-offs → not ready
        # P#Q3 is already ratified → not in ready list
        assert len(self.engine.ready_to_ratify()) == 0

    def test_summary(self):
        s = self.engine.summary()
        assert s["total_elements"] == 3
        assert s["committed"] == 1
        assert s["provisional"] == 1
        assert s["ratified"] == 1


# ═══════════════════════════════════════════════════
# PERSISTENCE TESTS
# ═══════════════════════════════════════════════════

class TestPersistence:
    """Test save/load."""

    def test_save_and_load(self, tmp_path):
        persist = tmp_path / "registry.json"
        engine1 = RatificationEngine(pre_launch=True, persist_path=persist)
        engine1.ratify_immediate("P#PERSIST-001", ElementType.PROVERB, "Persist", "test")
        engine1.save()

        engine2 = RatificationEngine(pre_launch=True, persist_path=persist)
        loaded = engine2.load()
        assert loaded == 1
        elem = engine2.get("P#PERSIST-001")
        assert elem is not None
        assert elem.state == ElementState.RATIFIED
        assert elem.signature is not None

    def test_load_nonexistent_returns_zero(self, tmp_path):
        engine = RatificationEngine(persist_path=tmp_path / "nope.json")
        assert engine.load() == 0


# ═══════════════════════════════════════════════════
# BOOTSTRAP TESTS
# ═══════════════════════════════════════════════════

class TestBootstrap:
    """Test bootstrapping from existing ratification_log.md."""

    def test_bootstrap_from_log(self):
        engine = RatificationEngine(pre_launch=True)
        count = engine.bootstrap_from_log()
        # Should load the existing ratified elements from ratification_log.md
        assert count > 0
        # Check founding covenants
        cov001 = engine.get("COV#001")
        assert cov001 is not None
        assert cov001.state == ElementState.RATIFIED

    def test_bootstrap_loads_proverbs(self):
        engine = RatificationEngine(pre_launch=True)
        engine.bootstrap_from_log()
        p = engine.get("P#EMERGE-2134")
        assert p is not None
        assert p.state == ElementState.RATIFIED

    def test_bootstrap_no_double_load(self):
        engine = RatificationEngine(pre_launch=True)
        c1 = engine.bootstrap_from_log()
        c2 = engine.bootstrap_from_log()
        assert c2 == 0  # Second call should load nothing new


# ═══════════════════════════════════════════════════
# TYPE INFERENCE TESTS
# ═══════════════════════════════════════════════════

class TestTypeInference:
    """Test element type inference from ID."""

    def test_covenant(self):
        assert RatificationEngine._type_from_id("COV#001") == ElementType.COVENANT

    def test_proverb(self):
        assert RatificationEngine._type_from_id("P#2135") == ElementType.PROVERB

    def test_structural(self):
        assert RatificationEngine._type_from_id("STRUCT#TD-001") == ElementType.STRUCTURAL

    def test_axiom(self):
        assert RatificationEngine._type_from_id("AXIOM#PROP-001") == ElementType.AXIOM

    def test_treasure(self):
        assert RatificationEngine._type_from_id("T#01") == ElementType.TREASURE

    def test_go_signal(self):
        assert RatificationEngine._type_from_id("GO#EXP-001") == ElementType.GO_SIGNAL

    def test_oath(self):
        assert RatificationEngine._type_from_id("OATH::SOVEREIGN-AXIS") == ElementType.OATH


# ═══════════════════════════════════════════════════
# ELEMENT SERIALIZATION TESTS
# ═══════════════════════════════════════════════════

class TestSerialization:
    """Test to_dict serialization."""

    def test_to_dict_contains_all_fields(self):
        engine = RatificationEngine(pre_launch=True)
        elem, _ = engine.ratify_immediate("P#SER-001", ElementType.PROVERB, "Ser", "test")
        d = elem.to_dict()
        assert d["element_id"] == "P#SER-001"
        assert d["state"] == "ratified"
        assert d["element_type"] == "proverb"
        assert d["signature"] is not None
        assert d["content_hash"] is not None
        assert len(d["sign_offs"]) > 0
        assert len(d["changelog"]) > 0


# ═══════════════════════════════════════════════════
# MODULE API TESTS
# ═══════════════════════════════════════════════════

class TestModuleAPI:
    """Test the module-level API functions."""

    def test_ratification_summary(self):
        import WEAVER.ratification as mod
        mod._ENGINE = None  # Reset singleton
        s = ratification_summary()
        assert "total_elements" in s
        assert "pre_launch_active" in s

    def test_ratification_commit(self):
        import WEAVER.ratification as mod
        mod._ENGINE = None
        d = ratification_commit("P#API-001", "proverb", "API Test", "test")
        assert d["state"] == "committed"


# ═══════════════════════════════════════════════════
# CHANGELOG TESTS
# ═══════════════════════════════════════════════════

class TestChangelog:
    """Test append-only changelog."""

    def test_changelog_grows(self):
        engine = RatificationEngine(pre_launch=True)
        engine.commit("P#CL-001", ElementType.PROVERB, "CL", "test")
        assert len(engine._changelog) == 1
        engine.offer_to_threshold("P#CL-001")
        assert len(engine._changelog) == 2
        engine.sign_off("P#CL-001", "steward", "V-001", "Mohamed")
        assert len(engine._changelog) == 3
        engine.ratify("P#CL-001")
        assert len(engine._changelog) == 4

    def test_element_changelog(self):
        engine = RatificationEngine(pre_launch=True)
        elem, _ = engine.ratify_immediate("P#ECL-001", ElementType.PROVERB, "ECL", "test")
        # Should have: COMMITTED, PROVISIONAL, SIGN-OFF(steward), RATIFIED
        assert len(elem.changelog) >= 4
        assert "COMMITTED" in elem.changelog[0]
        assert "RATIFIED" in elem.changelog[-1]


# ═══════════════════════════════════════════════════
# SIGNOFF REQUIREMENTS TABLE TESTS
# ═══════════════════════════════════════════════════

class TestRequirementsTable:
    """Verify the requirements table matches tier1_stone.md."""

    def test_covenant_requires_owner_and_ethics(self):
        req = SIGNOFF_REQUIREMENTS[ElementType.COVENANT]
        assert "canonical_owner" in req
        assert "ethics_reviewer" in req

    def test_proverb_requires_steward_only(self):
        req = SIGNOFF_REQUIREMENTS[ElementType.PROVERB]
        assert req == ["steward"]

    def test_centre_shift_requires_four_signers(self):
        req = SIGNOFF_REQUIREMENTS[ElementType.CENTRE_SHIFT]
        assert len(req) == 4
        assert "senior_moderator_1" in req
        assert "senior_moderator_2" in req


# ═══════════════════════════════════════════════════
# ORGANISM INTEGRATION TEST
# ═══════════════════════════════════════════════════

class TestOrganismIntegration:
    """Test that the ratification engine integrates with the Organism."""

    def test_organism_has_ratification(self):
        from WEAVER.organism import Organism
        org = Organism()
        assert hasattr(org, '_ratification')
        assert isinstance(org._ratification, RatificationEngine)

    def test_organism_state_includes_ratification(self):
        from WEAVER.organism import Organism
        org = Organism()
        s = org.state()
        assert hasattr(s, 'ratification_total')
        assert hasattr(s, 'ratification_ratified')
        assert s.ratification_total >= 0

    def test_organism_report_includes_ratification(self):
        from WEAVER.organism import Organism
        org = Organism()
        report = org.full_report()
        assert "ratification" in report
        assert "total_elements" in report["ratification"]
