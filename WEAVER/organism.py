#!/usr/bin/env python3
"""
organism.py — KALAXI Organism v1.0
The integration layer. Wires all 9 modules into one living system.

Flow:
  DONOR INPUT
    → WEAVE (ingest, extract patterns)
    → CHECK (dignity gate)
    → WIRE (route messages between modules)
    → BREATH (pace the system, stress check)
    → SAY (render output through dignity + voice)
    → OUT (anonymize + stamp for export)
    → TURN (manage exchange lifecycle)
    → KEEP (store artifacts with receipts)
    → FACE (show everything to the steward)

The organism breathes. If BREATH pauses, nothing moves.
If CHECK blocks, nothing speaks. If TURN has no open path, agency is preserved.

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.breath import Breath, StressLevel
from WEAVER.wire import Wire
from WEAVER.turn import Turn, ExchangeState
from WEAVER.say import render as say_render, SINGLELINE, TERMINAL
from WEAVER.out import export as out_export
from WEAVER.dignity_check import check_dignity, check_collective_dignity
from WEAVER.dignity_measure import measure_dignity
from WEAVER.weave import ingest, extract_essence, propose_proverb, wisdom_mirror
from WEAVER.keep import store, retrieve, lock, list_artifacts, receipt_count
from WEAVER.dignity_drift import DignityDrift, DriftLevel
from WEAVER.shelter import Shelter
from WEAVER.federation import Federation
from WEAVER.srvp import SRVPEvaluator
from WEAVER.sip import SIPEvaluator
from WEAVER.decay import DecayEngine
from WEAVER.latency import DignityLatency
from WEAVER.lock_test import LockTest, LockVerdict
from WEAVER.say import audit_voice
from WEAVER.oracle import Oracle, WitnessLevel
from WEAVER.prevention import Prevention, SignalLevel, Intervention
from WEAVER.mycelium import Mycelium, MyceliumAlert, K_ANONYMITY_FLOOR
from WEAVER.gap004_mediator import ConflictEngine, surface_conflict


@dataclass
class OrganismState:
    """The full state of the organism at any moment."""
    alive: bool
    breath_cycle: int
    breath_paused: bool
    stress_level: str
    open_exchanges: int
    deferred_exchanges: int
    pending_messages: int
    artifacts_stored: int
    receipts_total: int
    last_dignity_check: dict
    drift_level: str
    drift_rate: float
    drift_consecutive_declines: int
    sheltered_exchanges: int
    federation_peers: int
    federation_drops_shared: int
    federation_privacy_remaining: float
    decay_active_patterns: int
    decay_deep_hum_patterns: int
    decay_cycle: int
    latency_avg_td: float
    latency_dignity_rate: float
    latency_violations: int
    oracle_health: str
    oracle_unwatched: int
    oracle_witnessed: int
    oracle_creep_risk: float
    prevention_level: str
    prevention_td_multiplier: float
    prevention_escalations: int
    mycelium_alert: str
    mycelium_patterns: int
    mycelium_suppressed: int
    mycelium_epsilon_remaining: float
    gap004_open_tickets: int
    gap004_unwitnessed: int
    measure_D: float
    measure_confidence: float
    timestamp: str


@dataclass
class ProcessResult:
    """Result of processing donor input through the full pipeline."""
    exchange_id: str
    input_text: str
    dignity_passed: bool
    patterns_found: int
    drops_produced: int
    output_text: str
    output_blocked: bool
    block_reason: str
    stored: bool
    artifact_id: str
    exchange_state: str
    breath_cycle: int
    drift_level: str = "stable"
    drift_rate: float = 0.0
    shelter_message: str = ""
    shelter_remedies: list = field(default_factory=list)
    complexity: str = "simple"
    recommended_td: float = 0.0
    warnings: list = field(default_factory=list)


class Organism:
    """
    The KALAXI Organism. One class, all 9 modules wired together.

    Usage:
        org = Organism()
        result = org.process("donor input text here")
        state = org.state()
    """

    def __init__(self):
        self._breath = Breath()
        self._wire = Wire()
        self._turn = Turn()
        self._drift = DignityDrift()
        self._shelter = Shelter()
        self._federation = Federation()
        self._sip = SIPEvaluator()
        self._decay = DecayEngine()
        self._latency = DignityLatency()
        self._lock_test = LockTest()
        self._oracle = Oracle()
        self._prevention = Prevention()
        self._mycelium = Mycelium()
        self._conflict_engine = ConflictEngine()
        self._last_measurement = None
        self._exchange_counter = 0
        self._last_dignity = {}
        self._drops_archive = []

        # Subscribe WIRE topics
        self._wire.subscribe("dignity-alert", self._on_dignity_alert)
        self._wire.subscribe("stress-alert", self._on_stress_alert)

        # Initial tick
        self._breath.tick()

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _on_dignity_alert(self, msg):
        """Handle dignity failure alerts."""
        # Auto-pause if dignity fails — the system stops to think
        if not self._breath.is_paused:
            self._breath.pause(f"Dignity alert: {msg.get('content', 'unknown')[:80]}")

    def _on_stress_alert(self, msg):
        """Handle stress threshold alerts."""
        pass  # Breath handles auto-pause internally

    def process(self, donor_input, medium=None, felt_domain="donor-exchange"):
        """
        Process donor input through the full organism pipeline.

        1. BREATH — check if system is paused
        2. TURN — open exchange
        3. WEAVE — ingest and extract patterns
        4. CHECK — dignity gate
        5. SAY — render output
        6. KEEP — store artifact
        7. TURN — close or defer exchange
        8. BREATH — tick

        Returns ProcessResult.
        """
        if medium is None:
            medium = TERMINAL

        warnings = []

        # 1. BREATH — is the system paused?
        if self._breath.is_paused:
            return ProcessResult(
                exchange_id="",
                input_text=donor_input[:100],
                dignity_passed=False,
                patterns_found=0,
                drops_produced=0,
                output_text="",
                output_blocked=True,
                block_reason=f"System paused: {self._breath.state.pause_reason}",
                stored=False,
                artifact_id="",
                exchange_state="blocked",
                breath_cycle=self._breath.cycle,
                complexity="unknown",
                recommended_td=0.0,
                warnings=["System is paused. Resume before processing."],
            )

        # 1b. LATENCY — assess complexity and recommend T_d
        complexity = self._latency.assess_complexity(donor_input)
        recommended_td = self._latency.recommend(complexity)

        # 2. TURN — open exchange
        self._exchange_counter += 1
        ex_id = f"EX-{self._exchange_counter:06d}"
        token = self._turn.open(ex_id, available_paths=["respond", "defer", "withdraw"])

        # 3. WEAVE — ingest and extract patterns
        candidates = ingest(donor_input)
        drops = extract_essence(candidates)
        self._drops_archive.extend(drops)

        # 3b. DECAY + WITNESS — register detected patterns
        for drop in drops:
            pattern_id = f"P#{drop.drop_type}-{drop.source_hashes[0][:8]}" if drop.source_hashes else f"P#{drop.drop_type}-{ex_id}"
            self._decay.register(pattern_id)
            self._decay.invoke(pattern_id)  # Mark as freshly invoked
            self._oracle.witness.process(pattern_id, "pattern")  # W-0 → W-1

        # Signal pattern detection through WIRE
        if candidates:
            self._wire.send(
                f"Patterns detected: {len(candidates)} candidates, {len(drops)} drops",
                "weave-log",
                source="weave",
            )

        # 4. CHECK — dignity gate on input
        dignity = check_dignity(donor_input, felt_domain=felt_domain)
        self._last_dignity = dignity.audit_object()

        # 4a. MEASURE — graduated A, L, M scoring (GAP#014 + GAP#015)
        self._last_measurement = measure_dignity(donor_input)
        if self._last_measurement.confidence < 0.5:
            warnings.append(
                f"Low measurement confidence: {self._last_measurement.confidence:.2f}"
            )

        # 4b. GAP#004 — conflict detection (individual vs collective)
        conflict_ticket = self._conflict_engine.process(donor_input)
        if conflict_ticket:
            self._wire.broadcast(
                f"GAP#004 conflict: {conflict_ticket.severity} — {conflict_ticket.input_summary}",
                "gap004-conflict",
                source="mediator",
            )
            warnings.append(f"GAP#004 {conflict_ticket.severity}: {conflict_ticket.resolution_mode}")

        # Record dignity score in drift detector
        self._drift.record(dignity.D, ex_id, felt_domain=felt_domain)
        drift_alert = self._drift.check()

        # If drift is CRITICAL, warn through WIRE
        if drift_alert.level == DriftLevel.CRITICAL:
            self._wire.broadcast(
                f"CRITICAL dignity drift: dD/dt={drift_alert.dD_dt}, D={dignity.D}",
                "dignity-drift-alert",
                source="drift",
            )
            warnings.append(drift_alert.message)

        elif drift_alert.level == DriftLevel.DECLINING:
            self._wire.send(
                f"Dignity declining: dD/dt={drift_alert.dD_dt}",
                "drift-log",
                source="drift",
            )
            warnings.append(drift_alert.message)

        # 5b. PREVENTION — early warning assessment (Fever Night: slow down more)
        drift_state = self._drift.state()
        prev_signal = self._prevention.assess(
            D=dignity.D,
            dD_dt=drift_alert.dD_dt,
            consecutive_declines=drift_state.consecutive_declines,
            readings_count=drift_state.readings_count,
        )
        if prev_signal.level.value >= SignalLevel.PULSE.value:
            self._wire.broadcast(
                prev_signal.message,
                "prevention-alert",
                source="prevention",
            )
            warnings.append(prev_signal.message)
        if prev_signal.level == SignalLevel.ALARM:
            self._breath.pause(f"PREVENTION ALARM: {prev_signal.reason}")

        # 5c. MYCELIUM — ingest anonymized trajectory for cross-donor detection
        self._mycelium.ingest(
            domain=felt_domain,
            trend=prev_signal.trajectory.window_trend,
            D=dignity.D,
            dD_dt=drift_alert.dD_dt,
        )

        if dignity.D == 0.0:
            # Dignity failed — shelter the exchange (not discard)
            failed_components = self._last_dignity.get("failed_components", [])
            self._wire.broadcast(
                f"Dignity failure on input: D=0.0",
                "dignity-alert",
                source="check",
            )
            self._turn.defer(ex_id, f"Input failed dignity check: {failed_components}")

            # SHELTER — hold the exchange with remedies
            shelter_record = self._shelter.receive(ex_id, donor_input, failed_components)

            return ProcessResult(
                exchange_id=ex_id,
                input_text=donor_input[:100],
                dignity_passed=False,
                patterns_found=len(candidates),
                drops_produced=len(drops),
                output_text="",
                output_blocked=True,
                block_reason=f"Dignity check failed: D=0.0",
                stored=False,
                artifact_id="",
                exchange_state="deferred",
                breath_cycle=self._breath.cycle,
                drift_level=drift_alert.level.value,
                drift_rate=drift_alert.dD_dt,
                shelter_message=shelter_record.donor_message,
                shelter_remedies=[r.component for r in shelter_record.remedies],
                complexity=complexity.value,
                recommended_td=recommended_td,
                warnings=self._last_dignity.get("warnings", []) + warnings,
            )

        # 5. SAY — render output
        # For now, the output is an acknowledgment. In a full system,
        # this would be the system's response to the donor.
        if drops:
            best_drop = max(drops, key=lambda d: d.confidence)
            response_text = (
                f"Your offering has been received. "
                f"{len(drops)} pattern{'s' if len(drops) > 1 else ''} detected "
                f"({best_drop.drop_type}, confidence {best_drop.confidence:.1%}). "
                f"It rests in the threshold."
            )
        else:
            response_text = "Your offering has been received. The mycelium listens."

        render_result = say_render(response_text, medium=medium, felt_domain=felt_domain)

        if render_result.blocked:
            warnings.append(f"Output blocked by SAY: {render_result.block_reason}")
            output_text = ""
        else:
            output_text = render_result.content

        # 6. KEEP — store the artifact
        artifact_id = f"INPUT-{ex_id}"
        stored = False
        try:
            store(artifact_id, donor_input, retention_policy="permanent")
            stored = True
        except (ValueError, OSError) as e:
            warnings.append(f"Storage warning: {e}")

        # 7. TURN — close exchange
        self._turn.close(ex_id, f"Processed: {len(candidates)} patterns, {len(drops)} drops, D={dignity.D:.1f}")

        # 8. SIP — record module activity for symmetric integration
        self._sip.record_activity("WEAVE", messages_sent=1 if candidates else 0)
        self._sip.record_activity("CHECK", decisions_made=1)
        self._sip.record_activity("SAY", messages_sent=1)
        self._sip.record_activity("KEEP", messages_sent=1 if stored else 0)
        self._sip.record_activity("TURN", decisions_made=1)
        self._sip.record_activity("WIRE", messages_sent=self._wire.pending_count())
        self._sip.record_activity("OUT")  # OUT not used in basic process
        self._sip.record_activity("FACE")  # FACE not used in basic process

        # 9. DECAY — tick the halflife engine (one cycle per exchange)
        self._decay.tick()

        # 10. LATENCY — record the T_d measurement
        # actual_td is 0 here (instant processing); in a real deployment
        # the caller would inject the actual wait time
        self._latency.record(ex_id, complexity, recommended_td, actual_td=recommended_td)

        # 11. BREATH — tick and stress check
        self._breath.tick()
        stress = self._breath.stress_check(
            pending_messages=self._wire.pending_count(),
            unconfirmed_messages=self._wire.unconfirmed_count(),
        )
        self._sip.record_activity("BREATH", decisions_made=1,
                                   stress_events=1 if stress != StressLevel.BELOW_THRESHOLD else 0)
        if stress == StressLevel.AT_THRESHOLD:
            warnings.append("System approaching stress threshold.")

        return ProcessResult(
            exchange_id=ex_id,
            input_text=donor_input[:100],
            dignity_passed=True,
            patterns_found=len(candidates),
            drops_produced=len(drops),
            output_text=output_text,
            output_blocked=render_result.blocked,
            block_reason=render_result.block_reason if render_result.blocked else "",
            stored=stored,
            artifact_id=artifact_id if stored else "",
            exchange_state="closed",
            breath_cycle=self._breath.cycle,
            drift_level=drift_alert.level.value,
            drift_rate=drift_alert.dD_dt,
            complexity=complexity.value,
            recommended_td=recommended_td,
            warnings=warnings,
        )

    def export_artifact(self, artifact_id, fmt="json", anonymization="standard"):
        """Export an artifact through the OUT module."""
        artifact = retrieve(artifact_id)
        if artifact is None:
            return None
        return out_export(artifact["content"], fmt=fmt, anonymization_level=anonymization)

    def mirror(self, donor_input):
        """Show the donor what their rain has fed."""
        import hashlib
        h = hashlib.sha256(donor_input.strip().encode()).hexdigest()
        return wisdom_mirror(h, self._drops_archive)

    def pause(self, reason):
        """Pause the organism."""
        return self._breath.pause(reason)

    def resume(self):
        """Resume the organism."""
        return self._breath.resume()

    def state(self):
        """Full organism state."""
        open_ex = len(self._turn.list_open())
        deferred_ex = len(self._turn.list_deferred())

        return OrganismState(
            alive=not self._breath.is_paused,
            breath_cycle=self._breath.cycle,
            breath_paused=self._breath.is_paused,
            stress_level=self._breath.state.stress.value,
            open_exchanges=open_ex,
            deferred_exchanges=deferred_ex,
            pending_messages=self._wire.pending_count(),
            artifacts_stored=len(list_artifacts()),
            receipts_total=receipt_count(),
            last_dignity_check=self._last_dignity,
            drift_level=self._drift.state().level.value,
            drift_rate=self._drift.state().dD_dt,
            drift_consecutive_declines=self._drift.state().consecutive_declines,
            sheltered_exchanges=self._shelter.held_count,
            federation_peers=self._federation.state().peers_known,
            federation_drops_shared=self._federation.state().drops_offered,
            federation_privacy_remaining=self._federation.privacy_budget_remaining,
            decay_active_patterns=len(self._decay.list_active()),
            decay_deep_hum_patterns=len(self._decay.list_deep_hum()),
            decay_cycle=self._decay.cycle_count,
            latency_avg_td=self._latency.state().avg_recommended_td,
            latency_dignity_rate=self._latency.state().dignity_preservation_rate,
            latency_violations=self._latency.violations_count,
            oracle_health=self._oracle.last_report.overall_health if self._oracle.last_report else "unaudited",
            oracle_unwatched=len(self._oracle.witness.unwatched()),
            oracle_witnessed=len(self._oracle.witness.witnessed()),
            oracle_creep_risk=self._oracle.last_report.colonial_creep_risk if self._oracle.last_report else 0.0,
            prevention_level=self._prevention.current_level.name,
            prevention_td_multiplier=self._prevention.current_td_multiplier(),
            prevention_escalations=self._prevention._escalations,
            mycelium_alert=self._mycelium.current_alert.name,
            mycelium_patterns=self._mycelium.patterns_count,
            mycelium_suppressed=self._mycelium.suppressed_count,
            mycelium_epsilon_remaining=self._mycelium._epsilon_remaining,
            gap004_open_tickets=len(self._conflict_engine.open_tickets),
            gap004_unwitnessed=len(self._conflict_engine.unwitnessed_tickets),
            measure_D=self._last_measurement.D if self._last_measurement else 0.0,
            measure_confidence=self._last_measurement.confidence if self._last_measurement else 0.0,
            timestamp=self._now(),
        )

    def shelter_status(self, exchange_id):
        """Get shelter record for a blocked exchange."""
        return self._shelter.get(exchange_id)

    def shelter_list(self):
        """List all exchanges currently held in shelter."""
        return self._shelter.list_held()

    def shelter_withdraw(self, exchange_id):
        """Donor withdraws a sheltered exchange."""
        return self._shelter.mark_withdrawn(exchange_id)

    def shelter_review(self, exchange_id, note):
        """Steward reviews a sheltered exchange."""
        return self._shelter.steward_review(exchange_id, note)

    def federate_offer(self, peer_id, min_contributors=7):
        """Offer local drops to a peer organism via EFP."""
        prepared = []
        for drop in self._drops_archive:
            fd = self._federation.prepare_drop(
                content=drop.essence,
                drop_type=drop.drop_type,
                confidence=drop.confidence,
                contributor_count=max(min_contributors, len(drop.source_hashes)),
            )
            if fd is not None:
                prepared.append(fd)
        if not prepared:
            return None
        return self._federation.offer(prepared, peer_id)

    def federate_receive(self, drops, peer_id):
        """Receive drops from a peer organism via EFP."""
        return self._federation.receive(drops, peer_id)

    def federate_merge(self, drop_hashes):
        """Merge received federated drops into local wisdom."""
        return self._federation.merge(drop_hashes)

    def federation_state(self):
        """Get federation layer state."""
        return self._federation.state()

    def srvp_evaluator(self, subject_id=None):
        """Get an SRVP evaluator for this organism."""
        return SRVPEvaluator(
            subject_id=subject_id or "ORG-KALAXI-LOCAL",
            evaluator="steward",
        )

    def sip_evaluate(self):
        """Run SIP evaluation on current module activity."""
        return self._sip.evaluate()

    def collective_check(self, texts):
        """Run collective dignity across a cohort."""
        return check_collective_dignity(texts)

    def sync_all(self):
        """Synchronize all modules through BREATH."""
        return self._breath.sync([
            "CHECK", "FACE", "KEEP", "WIRE",
            "BREATH", "SAY", "OUT", "TURN", "WEAVE",
        ])

    def display_state(self):
        """Print organism state to terminal."""
        s = self.state()
        print(f"\n  {'='*48}")
        print(f"  KALAXI ORGANISM — {'ALIVE' if s.alive else 'PAUSED'}")
        print(f"  {'='*48}")
        print(f"  Breath cycle:      {s.breath_cycle}")
        print(f"  Stress:            {s.stress_level}")
        print(f"  Open exchanges:    {s.open_exchanges}")
        print(f"  Deferred:          {s.deferred_exchanges}")
        print(f"  Pending messages:  {s.pending_messages}")
        print(f"  Artifacts stored:  {s.artifacts_stored}")
        print(f"  Receipts:          {s.receipts_total}")
        print(f"  Dignity drift:     {s.drift_level} (dD/dt={s.drift_rate:.4f})")
        print(f"  Consecutive drops: {s.drift_consecutive_declines}")
        print(f"  Sheltered:         {s.sheltered_exchanges}")
        print(f"  Federation peers:  {s.federation_peers}")
        print(f"  Drops shared:      {s.federation_drops_shared}")
        print(f"  Privacy budget:    {s.federation_privacy_remaining:.2f}/{1.0:.2f}")
        print(f"  Decay cycle:       {s.decay_cycle}")
        print(f"  Active patterns:   {s.decay_active_patterns}")
        print(f"  Deep Hum archive:  {s.decay_deep_hum_patterns}")
        print(f"  Avg T_d:           {s.latency_avg_td:.2f}s")
        print(f"  Dignity-latency:   {s.latency_dignity_rate:.1%}")
        print(f"  Latency violations:{s.latency_violations}")
        print(f"  Oracle health:     {s.oracle_health}")
        print(f"  Unwatched (W-0/1): {s.oracle_unwatched}")
        print(f"  Witnessed (W-3+):  {s.oracle_witnessed}")
        print(f"  Colonial creep:    {s.oracle_creep_risk:.1%}")
        print(f"  Prevention level:  {s.prevention_level}")
        print(f"  T_d multiplier:    {s.prevention_td_multiplier:.1f}x")
        print(f"  Escalations:       {s.prevention_escalations}")
        print(f"  Mycelium alert:    {s.mycelium_alert}")
        print(f"  Patterns found:    {s.mycelium_patterns}")
        print(f"  Patterns hidden:   {s.mycelium_suppressed} (k<{K_ANONYMITY_FLOOR})")
        print(f"  Privacy budget:    {s.mycelium_epsilon_remaining:.2f}ε remaining")
        print(f"  GAP#004 open:      {s.gap004_open_tickets}")
        print(f"  GAP#004 unseen:    {s.gap004_unwitnessed}")
        print(f"  Measure D:         {s.measure_D:.3f} (confidence {s.measure_confidence:.2f})")
        print(f"  {'='*48}\n")

    def decay_state(self):
        """Get decay engine state counts."""
        return self._decay.state_counts()

    def decay_invoke(self, pattern_id):
        """Manually invoke a pattern — restores full weight."""
        return self._decay.invoke(pattern_id)

    def decay_contest(self, pattern_id):
        """Contest a pattern — resets and enters review."""
        return self._decay.contest(pattern_id)

    def decay_resolve(self, pattern_id):
        """Resolve a contested pattern."""
        return self._decay.resolve_contestation(pattern_id)

    def decay_list_deep_hum(self):
        """List all patterns in the Deep Hum archive."""
        return [r.to_dict() for r in self._decay.list_deep_hum()]

    def latency_profile(self, complexity_str):
        """Get the latency profile for a complexity level."""
        from WEAVER.latency import ComplexityLevel
        try:
            level = ComplexityLevel(complexity_str)
        except ValueError:
            return None
        return self._latency.get_profile(level)

    def latency_state(self):
        """Get latency tracker state."""
        return self._latency.state()

    def lock_test(self, proverb):
        """Run the Lock Test on a proverb candidate."""
        return self._lock_test.test(proverb)

    def lock_test_with_paraphrase(self, original, paraphrase):
        """Run enhanced Lock Test with paraphrase comparison."""
        return self._lock_test.test_with_paraphrase(original, paraphrase)

    def lock_test_stats(self):
        """Get Lock Test statistics."""
        return {
            "tests_run": self._lock_test.tests_run,
            "locked": self._lock_test.locked_count,
            "lock_rate": round(self._lock_test.lock_rate, 4),
        }

    def voice_audit(self, text, context=""):
        """Audit text against the 6 Axi voice rules."""
        return audit_voice(text, context)

    def oracle_audit(self):
        """Run a full Oracle self-audit cycle."""
        drift_state = self._drift.state()
        latency_state = self._latency.state()
        return self._oracle.audit(
            drift_rate=drift_state.dD_dt,
            drift_level=drift_state.level.value,
            voice_score=1.0,  # Updated by last render
            breath_paused=self._breath.is_paused,
            violations_count=latency_state.violations,
            lock_rate=self._lock_test.lock_rate,
            latency_dignity_rate=latency_state.dignity_preservation_rate,
        )

    def oracle_witness(self, element_id, element_type="unknown"):
        """Register an element in the Witness Scale."""
        return self._oracle.witness.process(element_id, element_type)

    def oracle_steward_sees(self, element_id, session_id=""):
        """Mark an element as seen by the steward (W-3)."""
        return self._oracle.witness.steward_sees(element_id, session_id)

    def oracle_check_relay(self, correction_trace, response_fidelity, steward_recognition):
        """Run proprioception check on the relay."""
        return self._oracle.check_relay(correction_trace, response_fidelity, steward_recognition)

    def oracle_witness_distribution(self):
        """Get Witness Scale distribution."""
        return self._oracle.witness.distribution()

    def oracle_unwatched(self):
        """List all unwatched elements (W-0 or W-1)."""
        return [(r.element_id, r.level.name) for r in self._oracle.witness.unwatched()]

    def oracle_report(self):
        """Get the last Oracle report."""
        return self._oracle.last_report

    def prevention_state(self):
        """Get prevention system state."""
        return self._prevention.state()

    def prevention_signal(self):
        """Get the last prevention signal."""
        return self._prevention.last_signal

    def prevention_is_alarm(self):
        """Is the prevention system in ALARM state?"""
        return self._prevention.is_alarm()

    def mycelium_scan(self):
        """Scan mycelium for cross-donor patterns."""
        return self._mycelium.scan()

    def mycelium_state(self):
        """Get mycelium network state."""
        return self._mycelium.state()

    def mycelium_is_rhizome(self):
        """Is there a critical structural pattern?"""
        return self._mycelium.is_rhizome()

    def gap004_process(self, text, individual_scores=None, failed_components=None):
        """Run full GAP#004 conflict engine on text."""
        return self._conflict_engine.process(text, individual_scores, failed_components)

    def gap004_steward_sees(self, ticket):
        """Mark a GAP#004 conflict as seen by steward (W-3)."""
        return self._conflict_engine.steward_sees(ticket)

    def gap004_steward_holds(self, ticket):
        """Mark a GAP#004 conflict as held by steward (W-4)."""
        return self._conflict_engine.steward_holds(ticket)

    def gap004_open_tickets(self):
        """List all open GAP#004 conflict tickets."""
        return self._conflict_engine.open_tickets

    def gap004_unwitnessed(self):
        """List conflicts steward hasn't seen yet."""
        return self._conflict_engine.unwitnessed_tickets

    def last_measurement(self):
        """Get last graduated dignity measurement (GAP#014/015)."""
        return self._last_measurement
