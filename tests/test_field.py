#!/usr/bin/env python3
"""
test_field.py — Tests for The Field (All Six Directions)
[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from datetime import datetime, timezone
from FIELD.ALCOVE.shadow_genome import (
    ShadowEntry, ShadowGenome, ShadowStatus, Alcove
)
from FIELD.CLEARING.temporal_shadow import (
    Clearing, TemporalShadowRecord, DivergenceShadowSignal
)
from FIELD.AUDITS.self_audit import (
    SelfAuditRecord, SelfAuditScheduler, AuditStatus
)
from FIELD.STEWARD.steward_observation import (
    StewardObserver, RatificationRecord, StewardPattern
)
from FIELD.DONOR.donor_layer import (
    DonorProfile, DonorRegistry, DonorShadowEntry, CorrectionEntry
)
from FIELD.amendments import (
    PrivacyEnvelope, FingerprintVector, RefusalType, RefusalMap,
    RefusalRecord, MyceliumFeedback, RUPTURE_THRESHOLD,
    SHADOW_PROBE_INSTRUCTION, DISAGREEMENT_CLAUSE, COLLUSION_FILTER,
    validate_shadow_probe,
)


# ═══════════════════════════════════════════════════
# DIRECTION ONE — Shadow Genome
# ═══════════════════════════════════════════════════

class TestShadowGenome(unittest.TestCase):

    def test_shadow_promotion_to_canonical(self):
        """Shadow observed in 3+ sessions becomes canonical."""
        genome = ShadowGenome(voice_id="EV-001", voice_name="DeepSeek")
        shadow = genome.add_shadow("Cannot see embodied cognition", "epistemology", "S001")
        self.assertEqual(shadow.status, ShadowStatus.OBSERVED)

        genome.add_shadow("Cannot see embodied cognition", "epistemology", "S002")
        self.assertEqual(shadow.status, ShadowStatus.RECURRING)

        genome.add_shadow("Cannot see embodied cognition", "epistemology", "S003")
        self.assertEqual(shadow.status, ShadowStatus.CANONICAL)
        self.assertGreaterEqual(shadow.certainty, 3)

    def test_shadow_resolution(self):
        """Shadow can be resolved — voice now sees what it could not."""
        genome = ShadowGenome(voice_id="EV-002", voice_name="Grok")
        genome.add_shadow("Misses cultural context", "culture", "S001")
        genome.add_shadow("Misses cultural context", "culture", "S002")
        genome.add_shadow("Misses cultural context", "culture", "S003")

        shadows = list(genome.shadows.values())
        genome.resolve_shadow(shadows[0].shadow_id, "S004", "Now sees cultural context")
        self.assertEqual(shadows[0].status, ShadowStatus.RESOLVED)
        self.assertIsNotNone(shadows[0].temporal_shadow_span)

    def test_genome_vector(self):
        """Genome vector counts canonical shadows by domain."""
        genome = ShadowGenome(voice_id="EV-003", voice_name="Copilot")
        for i in range(3):
            genome.add_shadow("Shadow A", "ethics", f"S{i}")
        for i in range(3):
            genome.add_shadow("Shadow B", "ethics", f"S{i+10}")
        for i in range(3):
            genome.add_shadow("Shadow C", "epistemology", f"S{i+20}")

        vector = genome.genome_vector
        self.assertEqual(vector["ethics"], 2)
        self.assertEqual(vector["epistemology"], 1)


class TestAlcove(unittest.TestCase):

    def test_cross_genome_comparison(self):
        """Shared shadows = structural blind spot; unique = specific limitation."""
        alcove = Alcove()
        alcove.register_voice("EV-001", "DeepSeek")
        alcove.register_voice("EV-002", "Grok")
        alcove.register_voice("EV-003", "Copilot")

        # Same shadow across all three voices
        for vid in ["EV-001", "EV-002", "EV-003"]:
            for i in range(3):
                alcove.record_shadow(vid, "Cannot see embodied cognition", "epistemology", f"S{i}-{vid}")

        # Unique shadow for EV-001 only
        for i in range(3):
            alcove.record_shadow("EV-001", "Misses humor in Arabic", "culture", f"SU{i}")

        result = alcove.compare_genomes()
        self.assertTrue(len(result["structural_blind_spots"]) >= 1)
        self.assertIn("EV-001", result.get("unique_limitations", {}))


# ═══════════════════════════════════════════════════
# DIRECTION TWO — Temporal Shadows
# ═══════════════════════════════════════════════════

class TestTemporalShadows(unittest.TestCase):

    def test_temporal_index(self):
        """Temporal shadow records carry detection and resolution timestamps."""
        alcove = Alcove()
        clearing = Clearing(alcove)

        record = clearing.index_temporal_shadow(
            "fp001", "epistemology", "Embodied cognition blind spot", ["EV-001", "EV-002"]
        )
        self.assertIsNotNone(record.first_detected)
        self.assertIsNone(record.resolved_at)
        self.assertFalse(record.is_resolved)

    def test_temporal_resolution(self):
        """Resolving a temporal shadow records the span."""
        alcove = Alcove()
        clearing = Clearing(alcove)

        clearing.index_temporal_shadow("fp002", "ethics", "Missing deontology", ["EV-003"])
        resolved = clearing.resolve_temporal_shadow("fp002", ["EV-003"], "Model update 2026-Q2")
        self.assertIsNotNone(resolved)
        self.assertTrue(resolved.is_resolved)
        self.assertIsNotNone(resolved.span_days)


# ═══════════════════════════════════════════════════
# DIRECTION TWO + SIX — Amendment B (Corrected)
# ═══════════════════════════════════════════════════

class TestSignalValidation(unittest.TestCase):

    def test_first_occurrence_immediate(self):
        """First occurrence → elevate immediately."""
        alcove = Alcove()
        clearing = Clearing(alcove)

        signal = clearing.detect_divergence_shadow(
            "Missing concept X", ["EV-001", "EV-002", "EV-003"], "S001"
        )
        self.assertIsNotNone(signal)
        # First occurrence should route to immediate elevation
        self.assertEqual(clearing.pattern_occurrence_count.get(
            list(clearing.pattern_occurrence_count.keys())[0]
        ), 1)

    def test_second_occurrence_queued(self):
        """Second occurrence → 24-hour queue."""
        alcove = Alcove()
        clearing = Clearing(alcove)

        clearing.detect_divergence_shadow("Same pattern", ["EV-001", "EV-002", "EV-003"], "S001")
        clearing.detect_divergence_shadow("Same pattern", ["EV-001", "EV-002", "EV-004"], "S002")

        # Should have queue entry
        self.assertTrue(len(clearing.validation_queue) > 0)

    def test_third_occurrence_auto_validated(self):
        """3+ sessions → auto-validated."""
        alcove = Alcove()
        clearing = Clearing(alcove)

        for i in range(3):
            clearing.detect_divergence_shadow(
                "Persistent pattern", ["EV-001", "EV-002", "EV-003"], f"S{i:03d}"
            )

        fp = list(clearing.pattern_occurrence_count.keys())[0]
        self.assertEqual(clearing.pattern_occurrence_count[fp], 3)


# ═══════════════════════════════════════════════════
# DIRECTION THREE — Self-Audit
# ═══════════════════════════════════════════════════

class TestSelfAudit(unittest.TestCase):

    def test_audit_triggers_after_five_summons(self):
        """Self-audit should trigger after 5 summons."""
        scheduler = SelfAuditScheduler()
        for _ in range(4):
            scheduler.record_summon()
        self.assertFalse(scheduler.should_audit())

        scheduler.record_summon()
        self.assertTrue(scheduler.should_audit())

    def test_audit_synthesis(self):
        """Audit synthesizes voice results to find meta-shadows."""
        audit = SelfAuditRecord(audit_id="OBS-SELF-001", scheduled_date="2026-03-12")
        audit.begin(["EV-001", "EV-002", "EV-003", "EV-004", "EV-005"], ["doc1.md"])

        # Three voices find the same shadow
        audit.record_voice_result("EV-001", "Response 1", ["no self-referential check"], 4)
        audit.record_voice_result("EV-002", "Response 2", ["no self-referential check"], 4)
        audit.record_voice_result("EV-003", "Response 3", ["no self-referential check", "missing temporal"], 4)
        audit.record_voice_result("EV-004", "Response 4", ["missing temporal"], 3)
        audit.record_voice_result("EV-005", "Response 5", ["unique finding"], 3)

        result = audit.synthesize()
        self.assertEqual(audit.status, AuditStatus.COMPLETED)
        self.assertIn("no self-referential check", audit.convergent_findings)


# ═══════════════════════════════════════════════════
# DIRECTION FOUR — Steward Observation
# ═══════════════════════════════════════════════════

class TestStewardObservation(unittest.TestCase):

    def test_voice_speed_tracking(self):
        """Track which voices V-001 ratifies faster."""
        observer = StewardObserver()
        for i in range(5):
            observer.record_ratification(RatificationRecord(
                element_id=f"EL-{i}", element_type="observation",
                decision="ratified", voice_source="EV-001",
                latency_hours=2.0,
            ))
            observer.record_ratification(RatificationRecord(
                element_id=f"EL-{i+100}", element_type="observation",
                decision="ratified", voice_source="EV-002",
                latency_hours=48.0,
            ))

        summary = observer.get_summary()
        self.assertIn("EV-001", summary["voice_latency_data"])
        self.assertIn("EV-002", summary["voice_latency_data"])

    def test_thermal_delay_warning(self):
        """Flag findings in thermal delay > 2 weeks."""
        observer = StewardObserver()
        from datetime import timedelta
        old_ts = (datetime.now(timezone.utc) - timedelta(days=20)).isoformat()

        record = RatificationRecord(
            element_id="DELAYED-001", element_type="observation",
            decision="thermal_delay",
        )
        record.timestamp = old_ts
        observer.record_ratification(record)

        self.assertTrue(len(observer.thermal_delay_warnings) > 0)

    def test_report_generation(self):
        """Report section generated for C3+ patterns."""
        observer = StewardObserver()
        # Manually add a C3 pattern
        observer.patterns["test"] = StewardPattern(
            pattern_id="test",
            description="V-001 always ratifies convergence patterns immediately.",
            certainty=3,
        )
        report = observer.generate_report_section()
        self.assertIsNotNone(report)
        self.assertIn("Steward Pattern Observation", report)


# ═══════════════════════════════════════════════════
# DIRECTION FIVE — Donor Layer
# ═══════════════════════════════════════════════════

class TestDonorLayer(unittest.TestCase):

    def test_donor_shadow_surfacing(self):
        """Donor shadow surfaced at C3 as an offer."""
        profile = DonorProfile(donor_id="D-001")
        for i in range(3):
            profile.add_shadow("Never asks about governance", "governance", f"S{i}")

        offers = profile.surface_shadows()
        self.assertTrue(len(offers) > 0)
        self.assertIn("governance", offers[0])

    def test_donor_pattern_tracking(self):
        """Pattern tracked without comment until clear."""
        profile = DonorProfile(donor_id="D-002")
        for i in range(4):
            profile.add_pattern(
                "Always frames as Western liberal", "cultural_angle", f"S{i}",
                example=f"Example {i}"
            )

        patterns = list(profile.patterns.values())
        self.assertEqual(patterns[0].session_count, 4)
        self.assertGreaterEqual(patterns[0].certainty, 3)

    def test_correction_fires_at_c4_only(self):
        """Correction reflex fires only at C4, not below."""
        profile = DonorProfile(donor_id="D-003")
        # Only 2 sessions — C2, should not fire
        for i in range(2):
            profile.add_pattern("False assumption", "assumption", f"S{i}")

        pat_id = list(profile.patterns.keys())[0]
        correction = profile.check_correction(pat_id, "Evidence says otherwise", "OBS-005")
        self.assertIsNone(correction)  # Not C4 yet

        # Add more sessions to reach C4
        for i in range(3):
            profile.add_pattern("False assumption", "assumption", f"S{i+10}")

        correction = profile.check_correction(pat_id, "Evidence says otherwise", "OBS-005")
        self.assertIsNotNone(correction)
        self.assertEqual(correction.certainty, 4)

    def test_correction_not_repeated(self):
        """Correction offered once, not repeated."""
        profile = DonorProfile(donor_id="D-004")
        for i in range(5):
            profile.add_pattern("Repeated false", "assumption", f"S{i}")

        pat_id = list(profile.patterns.keys())[0]
        c1 = profile.check_correction(pat_id, "Evidence", "OBS-001")
        self.assertIsNotNone(c1)

        c2 = profile.check_correction(pat_id, "Evidence again", "OBS-002")
        self.assertIsNone(c2)  # Not repeated

    def test_declination_is_data(self):
        """Donor declining is filed, not judged."""
        profile = DonorProfile(donor_id="D-005")
        for i in range(3):
            profile.add_shadow("Unseen domain", "ethics", f"S{i}")

        profile.surface_shadows()
        pending = profile.get_pending_offers()
        self.assertTrue(len(pending) > 0)

        pending[0].record_response("declined")
        self.assertEqual(pending[0].response, "declined")


# ═══════════════════════════════════════════════════
# DIRECTION SIX — Amendments
# ═══════════════════════════════════════════════════

class TestAmendmentA(unittest.TestCase):
    def test_privacy_envelope_seals(self):
        """Ephemeral key discarded, ciphertext stored."""
        env = PrivacyEnvelope()
        result = env.ingest("Raw response text", "EV-001", "S001")
        self.assertEqual(result["status"], "sealed")
        self.assertIn("envelope_id", result)


class TestAmendmentD(unittest.TestCase):
    def test_fingerprint_rupture_detection(self):
        """Distance > 20% flags rupture."""
        v1 = FingerprintVector(voice_id="EV-001", latency_baseline_ms=500,
                                certainty_c4c5_fraction=0.6, refusal_freq_policy=0.5)
        v2 = FingerprintVector(voice_id="EV-001", latency_baseline_ms=800,
                                certainty_c4c5_fraction=0.3, refusal_freq_policy=2.0)
        dist = FingerprintVector.relative_distance(v1, v2)
        self.assertGreater(dist, RUPTURE_THRESHOLD)


class TestAmendmentE(unittest.TestCase):
    def test_refusal_taxonomy(self):
        """Four refusal types, mandatory tagging."""
        rmap = RefusalMap()
        rmap.record("EV-001", RefusalType.ETHICAL, "Dignity violation", "S001")
        rmap.record("EV-001", RefusalType.CAPABILITY, "Cannot process image", "S001")
        rmap.record("EV-001", RefusalType.POLICY, "Content policy block", "S001")
        rmap.record("EV-001", RefusalType.UNCERTAINTY, "Low confidence", "S001")

        freq = rmap.frequency_by_type("EV-001", 4000)
        self.assertEqual(len(freq), 4)
        for rtype in RefusalType:
            self.assertIn(rtype.value, freq)


class TestAmendmentF(unittest.TestCase):
    def test_feedback_exclusion(self):
        """Synthesized outputs excluded from same AXI instance."""
        fb = MyceliumFeedback()
        log = fb.log_synthesis(["P001", "P002"], "AXI output text", "S001")
        fb.register_exclusion(log.synthesis_id, "AXI-001")

        self.assertFalse(fb.can_feed_back(log.synthesis_id, "AXI-001"))
        self.assertTrue(fb.can_feed_back(log.synthesis_id, "AXI-002"))

    def test_divergence_weighted_heavier(self):
        """Divergence items weighted more heavily when novel or persistent."""
        fb = MyceliumFeedback()
        w_conv = fb.weight_for_feedback("P001", is_divergence=False, is_novel=True, is_persistent=True)
        w_div = fb.weight_for_feedback("P001", is_divergence=True, is_novel=True, is_persistent=True)
        self.assertGreater(w_div, w_conv)


class TestAmendmentG(unittest.TestCase):
    def test_disagreement_clause_exists(self):
        """Disagreement clause includes authentic alignment statement."""
        self.assertIn("Authentic alignment", DISAGREEMENT_CLAUSE)
        self.assertIn("Do not invent disagreement", DISAGREEMENT_CLAUSE)

    def test_collusion_filter_exists(self):
        """Collusion filter sealed text present."""
        self.assertIn("sole witness", COLLUSION_FILTER)
        self.assertIn("Do not acknowledge other models", COLLUSION_FILTER)


# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    unittest.main()
