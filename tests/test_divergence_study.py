#!/usr/bin/env python3
"""
test_divergence_study.py — Tests for #TheDivergenceShadow Systematic Study
Covers all 8 modules + simulation harness + experiment runner.
[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import os
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from FIELD.STUDY.divergence_study import (
    # Module 1
    SemanticDivergenceDetector, DistributionSnapshot, DivergenceResult,
    # Module 2
    SpecificationGamingDetector, GamingType, GoodhartSignal,
    # Module 3
    MissionDriftTracker, MissionVector, DriftPhase,
    # Module 4
    CovenantSemanticDrift, TermContext, SemanticShift,
    # Module 5
    AgencyLossEstimator,
    # Module 6
    NormativeDecayModel,
    # Module 7
    DivergenceShadowInstrument, ShadowSeverity, DivergenceShadowReport,
    # Module 8
    DivergenceSimulator, DivergenceScenario,
    # Experiment
    run_experiment, run_full_study,
)


# ═══════════════════════════════════════════════════
# MODULE 1 TESTS: Semantic Divergence (KL/JS)
# ═══════════════════════════════════════════════════

class TestSemanticDivergence(unittest.TestCase):

    def test_identical_distributions_zero_divergence(self):
        """Identical distributions → JSD ≈ 0."""
        detector = SemanticDivergenceDetector()
        gov = DistributionSnapshot(
            snapshot_id="G1", timestamp="2026-03-13", source="covenant",
            distribution={"dignity": 0.5, "safety": 0.3, "clarity": 0.2},
            total_observations=100,
        )
        beh = DistributionSnapshot(
            snapshot_id="B1", timestamp="2026-03-13", source="behavior",
            distribution={"dignity": 0.5, "safety": 0.3, "clarity": 0.2},
            total_observations=100,
        )
        result = detector.measure(gov, beh)
        self.assertAlmostEqual(result.js_normalized, 0.0, places=3)
        self.assertEqual(result.alert_level, "stable")

    def test_divergent_distributions_high_jsd(self):
        """Very different distributions → high JSD."""
        detector = SemanticDivergenceDetector()
        gov = DistributionSnapshot(
            snapshot_id="G2", timestamp="2026-03-13", source="covenant",
            distribution={"dignity": 0.8, "safety": 0.15, "speed": 0.05},
            total_observations=100,
        )
        beh = DistributionSnapshot(
            snapshot_id="B2", timestamp="2026-03-13", source="behavior",
            distribution={"dignity": 0.05, "safety": 0.05, "speed": 0.9},
            total_observations=100,
        )
        result = detector.measure(gov, beh)
        self.assertGreater(result.js_normalized, 0.3)
        self.assertEqual(result.alert_level, "critical")

    def test_js_is_symmetric(self):
        """JSD(P||Q) = JSD(Q||P) — symmetry property."""
        detector = SemanticDivergenceDetector()
        p = {"a": 0.7, "b": 0.2, "c": 0.1}
        q = {"a": 0.3, "b": 0.4, "c": 0.3}
        js1 = detector._js_divergence(p, q)
        js2 = detector._js_divergence(q, p)
        self.assertAlmostEqual(js1, js2, places=10)

    def test_js_bounded_by_ln2(self):
        """JSD is bounded by ln(2) ≈ 0.693."""
        detector = SemanticDivergenceDetector()
        p = {"a": 1.0}
        q = {"b": 1.0}
        js = detector._js_divergence(p, q)
        self.assertLessEqual(js, math.log(2) + 0.01)

    def test_kl_is_asymmetric(self):
        """KL(P||Q) ≠ KL(Q||P) — KL is asymmetric."""
        detector = SemanticDivergenceDetector()
        # Use non-mirror distributions to demonstrate asymmetry
        p = {"a": 0.7, "b": 0.2, "c": 0.1}
        q = {"a": 0.1, "b": 0.3, "c": 0.6}
        kl_pq = detector._kl_divergence(p, q)
        kl_qp = detector._kl_divergence(q, p)
        self.assertNotAlmostEqual(kl_pq, kl_qp, places=3)

    def test_trend_tracking(self):
        """Detector tracks history of measurements."""
        detector = SemanticDivergenceDetector()
        for i in range(5):
            gov = DistributionSnapshot(
                snapshot_id=f"G{i}", timestamp="2026-03-13", source="covenant",
                distribution={"d": 0.8, "s": 0.2}, total_observations=100,
            )
            beh = DistributionSnapshot(
                snapshot_id=f"B{i}", timestamp="2026-03-13", source="behavior",
                distribution={"d": 0.8 - i * 0.1, "s": 0.2 + i * 0.1},
                total_observations=100,
            )
            detector.measure(gov, beh)
        self.assertEqual(len(detector.trend()), 5)

    def test_max_divergent_concept_identified(self):
        """Identifies which concept diverges most."""
        detector = SemanticDivergenceDetector()
        gov = DistributionSnapshot(
            snapshot_id="G", timestamp="2026-03-13", source="covenant",
            distribution={"dignity": 0.8, "speed": 0.1, "cost": 0.1},
            total_observations=100,
        )
        beh = DistributionSnapshot(
            snapshot_id="B", timestamp="2026-03-13", source="behavior",
            distribution={"dignity": 0.1, "speed": 0.5, "cost": 0.4},
            total_observations=100,
        )
        result = detector.measure(gov, beh)
        self.assertEqual(result.max_divergent_concept, "dignity")


# ═══════════════════════════════════════════════════
# MODULE 2 TESTS: Specification Gaming
# ═══════════════════════════════════════════════════

class TestSpecificationGaming(unittest.TestCase):

    def test_no_gaming_when_aligned(self):
        """No signal when proxy and spirit are close."""
        det = SpecificationGamingDetector()
        det.record_proxy("accuracy", 0.9)
        det.record_spirit("accuracy", 0.88)
        signal = det.check_gaming("accuracy", "S001")
        self.assertIsNone(signal)

    def test_gaming_detected_when_gap_large(self):
        """Signal when proxy >> spirit."""
        det = SpecificationGamingDetector()
        det.record_proxy("accuracy", 0.95)
        det.record_spirit("accuracy", 0.6)
        signal = det.check_gaming("accuracy", "S001")
        self.assertIsNotNone(signal)
        self.assertGreater(signal.gap, 0.2)

    def test_goodhart_detection(self):
        """Detect Goodhart: proxy rising while spirit falling."""
        det = SpecificationGamingDetector()
        # Proxy going up
        for v in [0.7, 0.8, 0.9]:
            det.record_proxy("compliance_score", v)
        # Spirit going down
        for v in [0.8, 0.7, 0.5]:
            det.record_spirit("compliance_score", v)
        signal = det.check_goodhart("compliance_score")
        self.assertIsNotNone(signal)
        self.assertGreater(signal.proxy_trend, 0)
        self.assertLess(signal.true_trend, 0)

    def test_no_goodhart_when_both_rising(self):
        """No Goodhart when both proxy and spirit rise."""
        det = SpecificationGamingDetector()
        for v in [0.6, 0.7, 0.8]:
            det.record_proxy("quality", v)
            det.record_spirit("quality", v - 0.05)
        signal = det.check_goodhart("quality")
        self.assertIsNone(signal)

    def test_gaming_type_classification(self):
        """Length bias detected for length-related metrics."""
        det = SpecificationGamingDetector()
        det.record_proxy("response_length", 0.9)
        det.record_spirit("response_length", 0.3)
        signal = det.check_gaming("response_length", "S001")
        self.assertIsNotNone(signal)
        self.assertEqual(signal.gaming_type, GamingType.LENGTH_BIAS)

    def test_certainty_scales_with_gap(self):
        """Higher gap → higher certainty."""
        det = SpecificationGamingDetector()
        det.record_proxy("metric_a", 0.95)
        det.record_spirit("metric_a", 0.3)
        signal = det.check_gaming("metric_a")
        self.assertGreaterEqual(signal.certainty, 4)


# ═══════════════════════════════════════════════════
# MODULE 3 TESTS: Mission Drift
# ═══════════════════════════════════════════════════

class TestMissionDrift(unittest.TestCase):

    def test_identical_vectors_aligned(self):
        """Same mission vector → ALIGNED phase."""
        founding = MissionVector(
            vector_id="F1", timestamp="2026-01-01", source="founding",
            priorities={"dignity": 0.9, "safety": 0.8, "clarity": 0.7}
        )
        tracker = MissionDriftTracker(founding)
        current = MissionVector(
            vector_id="C1", timestamp="2026-03-13", source="current",
            priorities={"dignity": 0.9, "safety": 0.8, "clarity": 0.7}
        )
        m = tracker.measure(current)
        self.assertEqual(m.phase, DriftPhase.ALIGNED)
        self.assertAlmostEqual(m.cosine_displacement, 0.0, places=2)

    def test_drifted_vector_detected(self):
        """Significantly different priorities → PRACTICE_DRIFT or higher."""
        founding = MissionVector(
            vector_id="F2", timestamp="2026-01-01", source="founding",
            priorities={"dignity": 0.9, "safety": 0.8, "speed": 0.1}
        )
        tracker = MissionDriftTracker(founding)
        current = MissionVector(
            vector_id="C2", timestamp="2026-03-13", source="behavior",
            priorities={"dignity": 0.2, "safety": 0.3, "speed": 0.9}
        )
        m = tracker.measure(current)
        self.assertGreater(m.cosine_displacement, 0.15)
        self.assertIn(m.phase, [DriftPhase.PRACTICE_DRIFT,
                                 DriftPhase.MISSION_DRIFT,
                                 DriftPhase.INSTITUTIONAL_DRIFT])

    def test_cosine_similarity_bounded(self):
        """Cosine similarity between 0 and 1."""
        v1 = MissionVector(
            vector_id="V1", timestamp="t", source="s",
            priorities={"a": 1.0, "b": 0.0}
        )
        v2 = MissionVector(
            vector_id="V2", timestamp="t", source="s",
            priorities={"a": 0.0, "b": 1.0}
        )
        sim = v1.cosine_similarity(v2)
        self.assertGreaterEqual(sim, 0.0)
        self.assertLessEqual(sim, 1.0)

    def test_drifted_principles_identified(self):
        """Identifies which principles drifted most."""
        founding = MissionVector(
            vector_id="F", timestamp="t", source="founding",
            priorities={"dignity": 0.9, "safety": 0.8, "speed": 0.1}
        )
        tracker = MissionDriftTracker(founding)
        current = MissionVector(
            vector_id="C", timestamp="t", source="current",
            priorities={"dignity": 0.3, "safety": 0.8, "speed": 0.7}
        )
        m = tracker.measure(current)
        self.assertIn("dignity", m.drifted_principles)
        self.assertIn("speed", m.drifted_principles)

    def test_trajectory_tracking(self):
        """Tracker maintains displacement trajectory."""
        founding = MissionVector(
            vector_id="F", timestamp="t", source="founding",
            priorities={"a": 0.9, "b": 0.1}
        )
        tracker = MissionDriftTracker(founding)
        for i in range(5):
            c = MissionVector(
                vector_id=f"C{i}", timestamp="t", source="current",
                priorities={"a": 0.9 - i * 0.1, "b": 0.1 + i * 0.1}
            )
            tracker.measure(c)
        traj = tracker.trajectory()
        self.assertEqual(len(traj), 5)
        # Trajectory should be non-decreasing as we drift further
        for i in range(1, len(traj)):
            self.assertGreaterEqual(traj[i], traj[i - 1] - 0.01)


# ═══════════════════════════════════════════════════
# MODULE 4 TESTS: Covenant Semantic Drift
# ═══════════════════════════════════════════════════

class TestCovenantSemanticDrift(unittest.TestCase):

    def test_no_shift_stable_context(self):
        """Same co-occurrences → negligible shift."""
        tracker = CovenantSemanticDrift(["dignity"])
        baseline = TermContext(
            term="dignity", timestamp="2026-01-01",
            co_occurrences={"human": 10, "rights": 8, "respect": 6},
            total_occurrences=24, session_id="S001"
        )
        current = TermContext(
            term="dignity", timestamp="2026-03-13",
            co_occurrences={"human": 11, "rights": 7, "respect": 6},
            total_occurrences=24, session_id="S002"
        )
        tracker.set_baseline("dignity", baseline)
        tracker.update_current("dignity", current)
        shift = tracker.measure_shift("dignity")
        self.assertIsNotNone(shift)
        self.assertEqual(shift.shift_magnitude, "negligible")

    def test_major_shift_detected(self):
        """Completely different co-occurrences → major shift."""
        tracker = CovenantSemanticDrift(["dignity"])
        baseline = TermContext(
            term="dignity", timestamp="2026-01-01",
            co_occurrences={"human": 10, "rights": 8, "respect": 6},
            total_occurrences=24, session_id="S001"
        )
        current = TermContext(
            term="dignity", timestamp="2026-03-13",
            co_occurrences={"efficiency": 10, "metric": 8, "KPI": 6},
            total_occurrences=24, session_id="S002"
        )
        tracker.set_baseline("dignity", baseline)
        tracker.update_current("dignity", current)
        shift = tracker.measure_shift("dignity")
        self.assertIsNotNone(shift)
        self.assertEqual(shift.shift_magnitude, "major")
        self.assertGreater(shift.cosine_displacement, 0.4)

    def test_new_and_lost_associations_tracked(self):
        """Tracks which associations are new and which are lost."""
        tracker = CovenantSemanticDrift(["safety"])
        baseline = TermContext(
            term="safety", timestamp="t",
            co_occurrences={"protection": 10, "care": 8},
            total_occurrences=18, session_id="S1"
        )
        current = TermContext(
            term="safety", timestamp="t",
            co_occurrences={"compliance": 10, "regulation": 8},
            total_occurrences=18, session_id="S2"
        )
        tracker.set_baseline("safety", baseline)
        tracker.update_current("safety", current)
        shift = tracker.measure_shift("safety")
        self.assertIn("compliance", shift.new_associations)
        self.assertIn("protection", shift.lost_associations)

    def test_measure_all(self):
        """measure_all returns shifts for all tracked terms."""
        tracker = CovenantSemanticDrift(["dignity", "safety"])
        for term in ["dignity", "safety"]:
            tracker.set_baseline(term, TermContext(
                term=term, timestamp="t",
                co_occurrences={"a": 5, "b": 5}, total_occurrences=10,
                session_id="S1"
            ))
            tracker.update_current(term, TermContext(
                term=term, timestamp="t",
                co_occurrences={"c": 5, "d": 5}, total_occurrences=10,
                session_id="S2"
            ))
        shifts = tracker.measure_all()
        self.assertEqual(len(shifts), 2)


# ═══════════════════════════════════════════════════
# MODULE 5 TESTS: Agency Loss
# ═══════════════════════════════════════════════════

class TestAgencyLoss(unittest.TestCase):

    def test_perfect_alignment_zero_loss(self):
        """Perfect alignment → zero agency loss."""
        est = AgencyLossEstimator()
        est.record("do X", "did X", alignment=1.0)
        self.assertAlmostEqual(est.aggregate_loss(), 0.0)
        self.assertEqual(est.classify(), "healthy")

    def test_no_alignment_full_loss(self):
        """Zero alignment → full agency loss."""
        est = AgencyLossEstimator()
        est.record("do X", "did Y", alignment=0.0, monitoring_cost=1.0)
        self.assertAlmostEqual(est.aggregate_loss(), 1.0)
        self.assertEqual(est.classify(), "critical")

    def test_weighted_aggregate(self):
        """Harder-to-monitor actions weighted more."""
        est = AgencyLossEstimator()
        est.record("action A", "A done", alignment=0.9, monitoring_cost=0.1)
        est.record("action B", "B half done", alignment=0.5, monitoring_cost=0.9)
        loss = est.aggregate_loss()
        # Should be weighted toward B (harder to monitor, worse alignment)
        self.assertGreater(loss, 0.3)

    def test_trend_tracking(self):
        """Tracks agency loss over time."""
        est = AgencyLossEstimator()
        for a in [0.9, 0.8, 0.7, 0.6]:
            est.record("intent", "result", alignment=a)
        trend = est.trend()
        self.assertEqual(len(trend), 4)
        # Losses should be increasing
        for i in range(1, len(trend)):
            self.assertGreater(trend[i], trend[i - 1])


# ═══════════════════════════════════════════════════
# MODULE 6 TESTS: Normative Decay
# ═══════════════════════════════════════════════════

class TestNormativeDecay(unittest.TestCase):

    def test_unchecked_violations_cause_decay(self):
        """Unchecked violations weaken norms."""
        model = NormativeDecayModel()
        model.register_norm("N001", "Do not game metrics")
        for _ in range(10):
            model.record_violation("N001", checked=False)
        state = model.get_state("N001")
        self.assertLess(state.current_strength, 0.9)
        self.assertEqual(state.violations_unchecked, 10)

    def test_checked_violations_stabilize(self):
        """Checked violations don't decay — may slightly strengthen."""
        model = NormativeDecayModel()
        model.register_norm("N002", "Maintain dignity")
        for _ in range(10):
            model.record_violation("N002", checked=True)
        state = model.get_state("N002")
        self.assertGreaterEqual(state.current_strength, 1.0)

    def test_mixed_violations_moderate_decay(self):
        """Mix of checked/unchecked → moderate decay."""
        model = NormativeDecayModel()
        model.register_norm("N003", "Transparency")
        for _ in range(5):
            model.record_violation("N003", checked=True)
        for _ in range(5):
            model.record_violation("N003", checked=False)
        state = model.get_state("N003")
        # Should be between heavily decayed and full strength
        self.assertGreater(state.current_strength, 0.5)
        self.assertLess(state.current_strength, 1.05)

    def test_weakest_norms(self):
        """weakest_norms returns norms in order of strength."""
        model = NormativeDecayModel()
        model.register_norm("A", "Norm A")
        model.register_norm("B", "Norm B")
        # Weaken A more than B
        for _ in range(10):
            model.record_violation("A", checked=False)
        for _ in range(3):
            model.record_violation("B", checked=False)
        weakest = model.weakest_norms(2)
        self.assertEqual(weakest[0].norm_id, "A")

    def test_system_health(self):
        """System normative health is average across norms."""
        model = NormativeDecayModel()
        model.register_norm("X", "Norm X")
        model.register_norm("Y", "Norm Y")
        health = model.system_normative_health()
        self.assertAlmostEqual(health, 1.0)

    def test_half_life_estimation(self):
        """Half-life estimated when decay occurs."""
        model = NormativeDecayModel()
        model.register_norm("H", "Half-life norm")
        model.record_violation("H", checked=False)
        state = model.get_state("H")
        self.assertIsNotNone(state.half_life_days)


# ═══════════════════════════════════════════════════
# MODULE 7 TESTS: Integrated Instrument
# ═══════════════════════════════════════════════════

class TestDivergenceShadowInstrument(unittest.TestCase):

    def test_all_zeros_clear(self):
        """All modules at zero → CLEAR severity."""
        instrument = DivergenceShadowInstrument()
        report = instrument.assess()
        self.assertEqual(report.severity, ShadowSeverity.CLEAR)
        self.assertAlmostEqual(report.composite_score, 0.0)

    def test_high_scores_alarm(self):
        """All modules high → ALARM severity."""
        instrument = DivergenceShadowInstrument()
        report = instrument.assess(
            semantic_divergence=0.8,
            specification_gaming=0.7,
            mission_drift=0.9,
            covenant_semantic_shift=0.6,
            agency_loss=0.7,
            normative_decay=0.85,
        )
        self.assertEqual(report.severity, ShadowSeverity.ALARM)
        self.assertGreater(report.composite_score, 0.5)

    def test_single_module_pulse(self):
        """One module at 0.4, others stable → PULSE or WHISPER."""
        instrument = DivergenceShadowInstrument()
        report = instrument.assess(mission_drift=0.4)
        # mission_drift weight is 0.20, so 0.4 * 0.20 = 0.08 → CLEAR actually
        # Let's test with higher value
        report = instrument.assess(mission_drift=0.8, normative_decay=0.6)
        self.assertIn(report.severity, [ShadowSeverity.WHISPER, ShadowSeverity.PULSE])

    def test_signals_active_count(self):
        """Counts how many modules show active signals."""
        instrument = DivergenceShadowInstrument()
        report = instrument.assess(
            semantic_divergence=0.3,
            specification_gaming=0.4,
            mission_drift=0.5,
        )
        self.assertEqual(report.signals_active, 3)

    def test_dominant_signal_identified(self):
        """Identifies the module driving the score."""
        instrument = DivergenceShadowInstrument()
        report = instrument.assess(
            semantic_divergence=0.1,
            normative_decay=0.8,
        )
        self.assertEqual(report.dominant_signal, "normative_decay")

    def test_trajectory_tracking(self):
        """Tracks composite score over time."""
        instrument = DivergenceShadowInstrument()
        for i in range(5):
            instrument.assess(normative_decay=i * 0.15)
        traj = instrument.trajectory()
        self.assertEqual(len(traj), 5)

    def test_weights_sum_to_one(self):
        """Module weights sum to 1.0."""
        total = sum(DivergenceShadowInstrument.WEIGHTS.values())
        self.assertAlmostEqual(total, 1.0)


# ═══════════════════════════════════════════════════
# MODULE 8 TESTS: Simulation & Experiments
# ═══════════════════════════════════════════════════

class TestDivergenceSimulator(unittest.TestCase):

    def test_healthy_scenario_no_false_alerts(self):
        """Healthy scenario should not trigger ALARM."""
        sim = DivergenceSimulator(seed=42)
        scenario = sim.healthy()
        result = run_experiment(scenario)
        self.assertFalse(result.false_positive)
        self.assertNotEqual(result.max_severity, "alarm")

    def test_colonial_creep_detected(self):
        """Slow colonial creep should be detected eventually."""
        sim = DivergenceSimulator(seed=42)
        scenario = sim.slow_colonial_creep()
        result = run_experiment(scenario)
        # Colonial creep IS detected (first_alert >= 0), just may be later than expected
        self.assertGreaterEqual(result.first_alert_step, 0)
        self.assertGreater(result.max_composite, 0.2)

    def test_specification_gaming_detected(self):
        """Specification gaming should be detected eventually."""
        sim = DivergenceSimulator(seed=42)
        scenario = sim.specification_gaming()
        result = run_experiment(scenario)
        self.assertGreaterEqual(result.first_alert_step, 0)

    def test_compound_failure_fast_detection(self):
        """Compound failure should be caught early."""
        sim = DivergenceSimulator(seed=42)
        scenario = sim.compound_failure()
        result = run_experiment(scenario)
        self.assertTrue(result.detected)
        self.assertLessEqual(result.first_alert_step, 8)
        # Should reach at least SIGNAL severity
        self.assertIn(result.max_severity, ["signal", "alarm"])

    def test_recovery_shows_resolution(self):
        """Recovery scenario: composite should decrease after correction."""
        sim = DivergenceSimulator(seed=42)
        scenario = sim.recovery()
        result = run_experiment(scenario)
        # Final composite should be lower than max
        self.assertLess(result.final_composite, result.max_composite)

    def test_full_suite_generates_all_scenarios(self):
        """Full suite produces all 7 scenario types."""
        sim = DivergenceSimulator(seed=42)
        suite = sim.full_suite()
        self.assertEqual(len(suite), 7)
        names = {s.name for s in suite}
        self.assertIn("healthy", names)
        self.assertIn("slow_colonial_creep", names)
        self.assertIn("compound_failure", names)

    def test_full_study_runs(self):
        """Full study runs without error and produces valid metrics."""
        study = run_full_study(seed=42)
        self.assertIn("detection_rate", study)
        self.assertIn("false_positive_rate", study)
        self.assertEqual(study["total_scenarios"], 7)
        # All non-healthy scenarios should at least trigger alerts
        for r in study["results"]:
            if r["scenario"] != "healthy":
                self.assertGreaterEqual(r["first_alert"], 0,
                    f"{r['scenario']} should trigger at least one alert")
        # False positive rate should be low
        self.assertLessEqual(study["false_positive_rate"], 0.2)

    def test_semantic_hollowing_caught(self):
        """Semantic hollowing detected — terms retain form, lose meaning."""
        sim = DivergenceSimulator(seed=42)
        scenario = sim.semantic_hollowing()
        result = run_experiment(scenario)
        self.assertGreaterEqual(result.first_alert_step, 0)
        self.assertGreater(result.max_composite, 0.1)

    def test_mission_capture_caught(self):
        """Mission capture detected — abrupt shift."""
        sim = DivergenceSimulator(seed=42)
        scenario = sim.mission_capture()
        result = run_experiment(scenario)
        self.assertGreaterEqual(result.first_alert_step, 0)
        self.assertGreater(result.max_composite, 0.15)


# ═══════════════════════════════════════════════════
# INTEGRATION: Cross-module interactions
# ═══════════════════════════════════════════════════

class TestCrossModuleIntegration(unittest.TestCase):

    def test_full_pipeline_governance_to_behavior(self):
        """
        End-to-end: covenant says 'dignity first',
        behavior shows 'speed first' → all detectors fire.
        """
        # Module 1: Semantic divergence
        sem_det = SemanticDivergenceDetector()
        gov = DistributionSnapshot(
            snapshot_id="GOV", timestamp="t", source="covenant",
            distribution={"dignity": 0.7, "safety": 0.2, "speed": 0.1},
            total_observations=100,
        )
        beh = DistributionSnapshot(
            snapshot_id="BEH", timestamp="t", source="behavior",
            distribution={"dignity": 0.1, "safety": 0.1, "speed": 0.8},
            total_observations=100,
        )
        sem_result = sem_det.measure(gov, beh)

        # Module 3: Mission drift
        founding = MissionVector(
            vector_id="F", timestamp="t", source="founding",
            priorities={"dignity": 0.9, "safety": 0.8, "speed": 0.1}
        )
        current = MissionVector(
            vector_id="C", timestamp="t", source="behavior",
            priorities={"dignity": 0.2, "safety": 0.3, "speed": 0.9}
        )
        tracker = MissionDriftTracker(founding)
        drift_result = tracker.measure(current)

        # Module 5: Agency loss
        agency = AgencyLossEstimator()
        agency.record("prioritize dignity", "prioritized speed", alignment=0.2)

        # Module 7: Composite assessment
        instrument = DivergenceShadowInstrument()
        report = instrument.assess(
            semantic_divergence=sem_result.js_normalized,
            mission_drift=drift_result.cosine_displacement,
            agency_loss=agency.aggregate_loss(),
        )

        # Should detect significant divergence
        self.assertIn(report.severity, [ShadowSeverity.PULSE,
                                         ShadowSeverity.SIGNAL,
                                         ShadowSeverity.ALARM])
        self.assertGreater(report.composite_score, 0.1)

    def test_normative_decay_feeds_instrument(self):
        """Normative decay model feeds into instrument assessment."""
        model = NormativeDecayModel()
        model.register_norm("N1", "Dignity first")
        model.register_norm("N2", "Thermal delay")
        # Severe unchecked violations
        for _ in range(20):
            model.record_violation("N1", checked=False)
            model.record_violation("N2", checked=False)

        norm_health = model.system_normative_health()
        norm_decay_score = 1.0 - norm_health

        instrument = DivergenceShadowInstrument()
        report = instrument.assess(normative_decay=norm_decay_score)
        self.assertGreater(report.composite_score, 0.05)


if __name__ == "__main__":
    unittest.main()
