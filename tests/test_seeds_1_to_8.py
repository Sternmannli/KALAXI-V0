#!/usr/bin/env python3
"""
Tests for Seeds #1-#8.
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


# ═══════════════════════════════════════════════════
# SEED #1 — Distributed Stewardship
# ═══════════════════════════════════════════════════

from WEAVER.distributed_stewardship import (
    DistributedStewardship, StewardRole, DelegationStatus
)


def test_delegate_and_list():
    ds = DistributedStewardship()
    d = ds.delegate("V-001", StewardRole.DIGNITY_GUARDIAN, scope="all exchanges")
    assert d.steward_id == "V-001"
    assert d.role == StewardRole.DIGNITY_GUARDIAN
    assert ds.active_count == 1


def test_rotate_delegation():
    ds = DistributedStewardship()
    d = ds.delegate("V-001", StewardRole.DIGNITY_GUARDIAN)
    new = ds.rotate(d.delegation_id, "V-002")
    assert new is not None
    assert new.steward_id == "V-002"
    assert d.status == DelegationStatus.ROTATED


def test_concentration_alert():
    ds = DistributedStewardship()
    # Give V-001 too many roles
    for role in StewardRole:
        ds.delegate("V-001", role)
    alert = ds.check_concentration()
    assert alert is not None
    assert alert.concentration_score > 0.5


def test_no_concentration_when_distributed():
    ds = DistributedStewardship()
    ds.delegate("V-001", StewardRole.DIGNITY_GUARDIAN)
    ds.delegate("V-002", StewardRole.PRIVACY_KEEPER)
    alert = ds.check_concentration()
    assert alert is None


def test_coverage_and_uncovered():
    ds = DistributedStewardship()
    ds.delegate("V-001", StewardRole.DIGNITY_GUARDIAN)
    uncovered = ds.uncovered_roles()
    assert len(uncovered) == len(StewardRole) - 1


def test_revoke_delegation():
    ds = DistributedStewardship()
    d = ds.delegate("V-001", StewardRole.DIGNITY_GUARDIAN)
    assert ds.revoke(d.delegation_id)
    assert ds.active_count == 0


def test_steward_roles():
    ds = DistributedStewardship()
    ds.delegate("V-001", StewardRole.DIGNITY_GUARDIAN)
    ds.delegate("V-001", StewardRole.WISDOM_TENDER)
    roles = ds.steward_roles("V-001")
    assert len(roles) == 2


def test_report():
    ds = DistributedStewardship()
    ds.delegate("V-001", StewardRole.DIGNITY_GUARDIAN)
    r = ds.report()
    assert r["active_delegations"] == 1
    assert r["coverage_rate"] < 1.0


# ═══════════════════════════════════════════════════
# SEED #2 — Immutable Witness Network
# ═══════════════════════════════════════════════════

from WEAVER.witness_network import WitnessNetwork


def test_witness_basic():
    wn = WitnessNetwork()
    r = wn.witness("dignity_check", "D=1.0 on EX-000001", "V-002")
    assert r.record_id == "WIT-000001"
    assert wn.chain_length == 1


def test_chain_integrity():
    wn = WitnessNetwork()
    wn.witness("exchange", "EX-001 opened", "V-002")
    wn.witness("dignity_check", "D=0.85", "V-002")
    wn.witness("exchange", "EX-001 closed", "V-002")
    assert wn.verify_chain()


def test_chain_linkage():
    wn = WitnessNetwork()
    r1 = wn.witness("event_a", "first", "actor")
    r2 = wn.witness("event_b", "second", "actor")
    assert r2.prev_hash == r1.chain_hash


def test_empty_chain_valid():
    wn = WitnessNetwork()
    assert wn.verify_chain()


def test_find_by_type():
    wn = WitnessNetwork()
    wn.witness("dignity_check", "D=1.0", "V-002")
    wn.witness("exchange", "opened", "V-002")
    wn.witness("dignity_check", "D=0.9", "V-002")
    found = wn.find_by_type("dignity_check")
    assert len(found) == 2


def test_find_by_actor():
    wn = WitnessNetwork()
    wn.witness("event", "A did something", "A")
    wn.witness("event", "B did something", "B")
    assert len(wn.find_by_actor("A")) == 1


def test_chain_head():
    wn = WitnessNetwork()
    assert wn.chain_head == "0" * 64
    wn.witness("event", "first", "actor")
    assert wn.chain_head != "0" * 64


def test_witness_report():
    wn = WitnessNetwork()
    wn.witness("exchange", "test", "V-002")
    r = wn.report()
    assert r["chain_valid"]
    assert r["chain_length"] == 1


# ═══════════════════════════════════════════════════
# SEED #3 — Deliberative Democracy
# ═══════════════════════════════════════════════════

from WEAVER.deliberative_democracy import (
    DeliberativeDemocracy, VoteType, ProposalStatus
)


def test_propose_and_deliberate():
    dd = DeliberativeDemocracy()
    dd.register_voice("V-001", participation_score=10.0)
    dd.register_voice("donor-042", participation_score=1.0)
    p = dd.propose("V-001", "Amend COV#003", "Add data portability")
    d = dd.deliberate(p.proposal_id, "donor-042", VoteType.SUPPORT, "Agreed")
    assert d is not None
    assert p.status == ProposalStatus.DELIBERATING


def test_weakest_voice_first():
    dd = DeliberativeDemocracy()
    dd.register_voice("V-001", participation_score=10.0)
    dd.register_voice("donor-042", participation_score=1.0)
    dd.register_voice("new-voice", participation_score=0.0)
    order = dd.speaking_order()
    assert order[0] == "new-voice"
    assert order[-1] == "V-001"


def test_block_prevents_resolution():
    dd = DeliberativeDemocracy()
    dd.register_voice("V-001")
    dd.register_voice("V-002")
    p = dd.propose("V-001", "Something", "Description")
    dd.deliberate(p.proposal_id, "V-002", VoteType.BLOCK, "I object")
    assert not dd.can_resolve(p.proposal_id)


def test_resolve_without_blocks():
    dd = DeliberativeDemocracy()
    dd.register_voice("V-001")
    dd.register_voice("V-002")
    p = dd.propose("V-001", "Something", "Description")
    dd.deliberate(p.proposal_id, "V-002", VoteType.SUPPORT, "Fine")
    assert dd.can_resolve(p.proposal_id)
    assert dd.resolve(p.proposal_id, "Accepted")
    assert p.status == ProposalStatus.RESOLVED


def test_withdraw():
    dd = DeliberativeDemocracy()
    p = dd.propose("V-001", "Temporary", "Will withdraw")
    assert dd.withdraw(p.proposal_id)
    assert p.status == ProposalStatus.WITHDRAWN


def test_concerns_collected():
    dd = DeliberativeDemocracy()
    dd.register_voice("V-001")
    dd.register_voice("V-002")
    p = dd.propose("V-001", "Something", "Description")
    dd.deliberate(p.proposal_id, "V-002", VoteType.CONCERN, "Worried",
                  concerns=["Privacy impact"])
    dd.resolve(p.proposal_id, "Accepted with concerns")
    assert "Privacy impact" in p.unresolved_concerns


def test_participation_tracking():
    dd = DeliberativeDemocracy()
    dd.register_voice("V-001", participation_score=0.0)
    p = dd.propose("V-001", "Something", "Description")
    dd.deliberate(p.proposal_id, "V-001", VoteType.SUPPORT, "Yes")
    voice = dd._voices["V-001"]
    assert voice.votes_cast == 1


def test_deliberation_report():
    dd = DeliberativeDemocracy()
    dd.register_voice("V-001")
    r = dd.report()
    assert r["voices"] == 1


# ═══════════════════════════════════════════════════
# SEED #4 — Constitutional Evolution Engine
# ═══════════════════════════════════════════════════

from WEAVER.constitutional_evolution import (
    ConstitutionalEvolution, AmendmentTier, AmendmentState
)


def test_propose_amendment():
    ce = ConstitutionalEvolution()
    a = ce.propose("V-001", "COV#003", AmendmentTier.STRUCTURAL,
                   "Add portability", "Donors can export all data")
    assert a.state == AmendmentState.PROPOSED
    assert ce.amendments_count == 1


def test_cooling_period():
    ce = ConstitutionalEvolution()
    a = ce.propose("V-001", "COV#003", AmendmentTier.STRUCTURAL,
                   "Add portability", "Detail")
    assert ce.enter_cooling(a.amendment_id)
    assert a.state == AmendmentState.COOLING
    assert a.cooling_ends is not None


def test_support_and_object():
    ce = ConstitutionalEvolution()
    a = ce.propose("V-001", "COV#003", AmendmentTier.OPERATIONAL, "Change", "Detail")
    ce.enter_cooling(a.amendment_id)
    assert ce.support(a.amendment_id, "V-002")
    assert ce.object(a.amendment_id, "V-003")
    assert len(a.supporters) == 1
    assert len(a.objectors) == 1


def test_ratify():
    ce = ConstitutionalEvolution()
    a = ce.propose("V-001", "COV#003", AmendmentTier.OPERATIONAL, "Change", "Detail")
    ce.enter_cooling(a.amendment_id)
    assert ce.ratify(a.amendment_id, "V-001")
    assert a.state == AmendmentState.RATIFIED


def test_reject():
    ce = ConstitutionalEvolution()
    a = ce.propose("V-001", "COV#003", AmendmentTier.OPERATIONAL, "Bad idea", "Detail")
    assert ce.reject(a.amendment_id, "Not aligned with COV#001")
    assert a.state == AmendmentState.REJECTED


def test_cannot_ratify_without_cooling():
    ce = ConstitutionalEvolution()
    a = ce.propose("V-001", "COV#003", AmendmentTier.STRUCTURAL, "Change", "Detail")
    # Try to ratify directly — should fail (not in cooling state)
    assert not ce.ratify(a.amendment_id, "V-001")


def test_amendment_report():
    ce = ConstitutionalEvolution()
    ce.propose("V-001", "COV#003", AmendmentTier.STRUCTURAL, "Change", "Detail")
    r = ce.report()
    assert r["total_amendments"] == 1
    assert r["active"] == 1


def test_audit_log():
    ce = ConstitutionalEvolution()
    a = ce.propose("V-001", "COV#001", AmendmentTier.CONSTITUTIONAL, "Big change", "Detail")
    ce.enter_cooling(a.amendment_id)
    ce.ratify(a.amendment_id, "V-001")
    assert len(ce._audit_log) == 3  # proposed, cooling, ratified


# ═══════════════════════════════════════════════════
# SEED #5 — Restorative Justice Platform
# ═══════════════════════════════════════════════════

from WEAVER.restorative_justice import (
    RestorativeJustice, HarmSeverity, RepairStatus
)


def test_record_and_acknowledge_harm():
    rj = RestorativeJustice()
    harm = rj.record_harm("EX-001", HarmSeverity.MODERATE,
                          ["agency"], "System blocked without explanation")
    assert harm.harm_id == "HARM-0001"
    assert rj.acknowledge(harm.harm_id)
    assert harm.acknowledged


def test_suggest_repairs():
    rj = RestorativeJustice()
    harm = rj.record_harm("EX-001", HarmSeverity.MODERATE,
                          ["agency", "legibility"], "Bad experience")
    suggestions = rj.suggest_repairs(harm.harm_id)
    assert len(suggestions) == 2


def test_repair_lifecycle():
    rj = RestorativeJustice()
    harm = rj.record_harm("EX-001", HarmSeverity.MODERATE,
                          ["agency"], "Blocked")
    path = rj.propose_repair(harm.harm_id, "Re-present with explanation", "V-002")
    assert rj.begin_repair(path.repair_id)
    assert path.status == RepairStatus.IN_PROGRESS
    assert rj.complete_repair(path.repair_id, "Fixed")
    assert path.status == RepairStatus.REPAIRED


def test_repair_rate():
    rj = RestorativeJustice()
    h1 = rj.record_harm("EX-001", HarmSeverity.MINOR, ["agency"], "Minor issue")
    h2 = rj.record_harm("EX-002", HarmSeverity.MODERATE, ["legibility"], "Unclear")
    p1 = rj.propose_repair(h1.harm_id, "Fix 1", "V-002")
    rj.complete_repair(p1.repair_id, "Done")
    assert rj.repair_rate == 0.5  # 1 out of 2 repaired


def test_unresolvable():
    rj = RestorativeJustice()
    harm = rj.record_harm("EX-001", HarmSeverity.CRITICAL,
                          ["agency", "legibility", "moral_standing"], "Severe")
    path = rj.propose_repair(harm.harm_id, "Attempted repair", "V-002")
    assert rj.mark_unresolvable(path.repair_id, "Cannot undo harm")
    assert path.status == RepairStatus.UNRESOLVABLE


def test_repairs_for_harm():
    rj = RestorativeJustice()
    harm = rj.record_harm("EX-001", HarmSeverity.MODERATE, ["agency"], "Issue")
    rj.propose_repair(harm.harm_id, "Fix A", "V-002")
    rj.propose_repair(harm.harm_id, "Fix B", "V-002")
    assert len(rj.repairs_for_harm(harm.harm_id)) == 2


def test_open_harms():
    rj = RestorativeJustice()
    rj.record_harm("EX-001", HarmSeverity.MINOR, ["agency"], "Issue 1")
    rj.record_harm("EX-002", HarmSeverity.MINOR, ["agency"], "Issue 2")
    assert rj.open_harms == 2


def test_rj_report():
    rj = RestorativeJustice()
    r = rj.report()
    assert r["repair_rate"] == 1.0  # No harms = 100% rate


# ═══════════════════════════════════════════════════
# SEED #6 — System Self-Awareness
# ═══════════════════════════════════════════════════

from WEAVER.system_self_awareness import (
    SystemSelfAwareness, CapabilityLevel, CalibrationBias
)


def test_register_capability():
    ssa = SystemSelfAwareness()
    cap = ssa.register_capability("dignity_check", "ethics",
                                  "Evaluate D=A×L×M", CapabilityLevel.STRONG)
    assert cap.level == CapabilityLevel.STRONG
    assert ssa.capabilities_count == 1


def test_register_limitation():
    ssa = SystemSelfAwareness()
    lim = ssa.register_limitation("cultural_context", "culture",
                                  "Cannot detect culture-specific violations",
                                  severity=0.9)
    assert lim.severity == 0.9
    assert len(ssa.critical_limitations()) == 1


def test_calibration_overconfident():
    ssa = SystemSelfAwareness()
    # System says 90% confident but is wrong most of the time
    for _ in range(10):
        ssa.record_calibration(0.9, False, "ethics")
    assert ssa.calibration_bias() == CalibrationBias.OVERCONFIDENT


def test_calibration_underconfident():
    ssa = SystemSelfAwareness()
    # System says 20% confident but is right most of the time
    for _ in range(10):
        ssa.record_calibration(0.2, True, "ethics")
    assert ssa.calibration_bias() == CalibrationBias.UNDERCONFIDENT


def test_calibration_calibrated():
    ssa = SystemSelfAwareness()
    # System is well-calibrated
    for _ in range(5):
        ssa.record_calibration(0.8, True, "ethics")
    for _ in range(2):
        ssa.record_calibration(0.3, False, "ethics")
    assert ssa.calibration_bias() == CalibrationBias.CALIBRATED


def test_capability_coverage():
    ssa = SystemSelfAwareness()
    ssa.register_capability("a", "d", "desc", CapabilityLevel.STRONG)
    ssa.register_capability("b", "d", "desc", CapabilityLevel.WEAK)
    cov = ssa.capability_coverage()
    assert cov["strong"] == 1
    assert cov["weak"] == 1


def test_few_calibrations_default_calibrated():
    ssa = SystemSelfAwareness()
    ssa.record_calibration(0.9, False, "ethics")
    assert ssa.calibration_bias() == CalibrationBias.CALIBRATED


def test_ssa_report():
    ssa = SystemSelfAwareness()
    ssa.register_capability("a", "d", "desc", CapabilityLevel.STRONG)
    ssa.register_limitation("b", "d", "desc", severity=0.9)
    r = ssa.report()
    assert r["capabilities"] == 1
    assert r["critical_limitations"] == 1


# ═══════════════════════════════════════════════════
# SEED #7 — Personalized Parables
# ═══════════════════════════════════════════════════

from WEAVER.personalized_parables import PersonalizedParables


def test_basic_delivery():
    pp = PersonalizedParables()
    pp.register_donor("D-001", domains=["technology"])
    delivery = pp.deliver("P#001", "What ripens too fast rots first.", "D-001")
    assert delivery.proverb_text == "What ripens too fast rots first."
    assert delivery.donor_id == "D-001"


def test_relevance_with_matching_domain():
    pp = PersonalizedParables()
    pp.register_donor("D-001", domains=["technology"])
    delivery = pp.deliver("P#001", "Test proverb", "D-001", donor_theme="technology")
    assert delivery.relevance_score > 0.5


def test_different_styles():
    pp = PersonalizedParables()
    pp.register_donor("D-001", preferred_style="narrative")
    delivery = pp.deliver("P#001", "The river waits.", "D-001")
    assert "Consider this" in delivery.frame


def test_unknown_donor():
    pp = PersonalizedParables()
    delivery = pp.deliver("P#001", "A proverb.", "unknown")
    assert delivery.relevance_score == 0.3  # Generic


def test_context_update():
    pp = PersonalizedParables()
    pp.register_donor("D-001")
    pp.update_context("D-001", domain="ethics", theme="fairness")
    ctx = pp._donors["D-001"]
    assert "ethics" in ctx.domains
    assert "fairness" in ctx.recent_themes


def test_deliveries_for_donor():
    pp = PersonalizedParables()
    pp.register_donor("D-001")
    pp.deliver("P#001", "Proverb 1", "D-001")
    pp.deliver("P#002", "Proverb 2", "D-001")
    pp.deliver("P#003", "Proverb 3", "D-002")
    assert len(pp.deliveries_for_donor("D-001")) == 2


def test_avg_relevance():
    pp = PersonalizedParables()
    pp.register_donor("D-001", domains=["tech"])
    pp.deliver("P#001", "Test", "D-001", donor_theme="tech")
    assert pp.avg_relevance > 0


def test_pp_report():
    pp = PersonalizedParables()
    pp.register_donor("D-001")
    r = pp.report()
    assert r["donors_registered"] == 1


# ═══════════════════════════════════════════════════
# SEED #8 — Institutional Dignity Score
# ═══════════════════════════════════════════════════

from WEAVER.institutional_dignity import InstitutionalDignity


def test_register_institution():
    ids = InstitutionalDignity()
    profile = ids.register("INST-001", "Hospital Alpha", sector="healthcare")
    assert profile.institution_id == "INST-001"
    assert ids.institutions_count == 1


def test_record_exchanges():
    ids = InstitutionalDignity()
    ids.register("INST-001", "Hospital Alpha")
    assert ids.record_exchange("INST-001", D=0.85)
    assert ids.record_exchange("INST-001", D=0.92)
    assert ids.record_exchange("INST-001", D=0.78)


def test_evaluate_good_institution():
    ids = InstitutionalDignity()
    ids.register("INST-001", "Good Hospital")
    for _ in range(10):
        ids.record_exchange("INST-001", D=0.9)
    score = ids.evaluate("INST-001")
    assert score is not None
    assert score.grade in ("A", "B")


def test_evaluate_inconsistent_institution():
    ids = InstitutionalDignity()
    ids.register("INST-002", "Inconsistent Hospital")
    for D in [0.95, 0.10, 0.90, 0.05, 0.85]:
        ids.record_exchange("INST-002", D=D)
    score = ids.evaluate("INST-002")
    assert score is not None
    # High variance should drag score down
    assert score.IDS < 0.7


def test_floor_matters():
    ids = InstitutionalDignity()
    ids.register("INST-003", "Almost Good")
    # 9 good, 1 terrible
    for _ in range(9):
        ids.record_exchange("INST-003", D=0.95)
    ids.record_exchange("INST-003", D=0.0)
    score = ids.evaluate("INST-003")
    assert score.floor_D == 0.0
    assert score.grade != "A"  # Floor should prevent A


def test_minimum_data_required():
    ids = InstitutionalDignity()
    ids.register("INST-004", "Too Few")
    ids.record_exchange("INST-004", D=0.9)
    ids.record_exchange("INST-004", D=0.8)
    assert ids.evaluate("INST-004") is None  # Need 3+


def test_unregistered_institution():
    ids = InstitutionalDignity()
    assert not ids.record_exchange("NONEXISTENT", D=0.5)


def test_ids_report():
    ids = InstitutionalDignity()
    ids.register("INST-001", "Test")
    r = ids.report()
    assert r["institutions"] == 1
