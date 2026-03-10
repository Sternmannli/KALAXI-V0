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
from WEAVER.weave import ingest, extract_essence, propose_proverb, wisdom_mirror
from WEAVER.keep import store, retrieve, lock, list_artifacts, receipt_count


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
                warnings=["System is paused. Resume before processing."],
            )

        # 2. TURN — open exchange
        self._exchange_counter += 1
        ex_id = f"EX-{self._exchange_counter:06d}"
        token = self._turn.open(ex_id, available_paths=["respond", "defer", "withdraw"])

        # 3. WEAVE — ingest and extract patterns
        candidates = ingest(donor_input)
        drops = extract_essence(candidates)
        self._drops_archive.extend(drops)

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

        if dignity.D == 0.0:
            # Dignity failed — block output, defer exchange
            self._wire.broadcast(
                f"Dignity failure on input: D=0.0",
                "dignity-alert",
                source="check",
            )
            self._turn.defer(ex_id, f"Input failed dignity check: {self._last_dignity.get('failed_components', [])}")

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
                warnings=self._last_dignity.get("warnings", []),
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

        # 8. BREATH — tick and stress check
        self._breath.tick()
        stress = self._breath.stress_check(
            pending_messages=self._wire.pending_count(),
            unconfirmed_messages=self._wire.unconfirmed_count(),
        )
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
            timestamp=self._now(),
        )

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
        print(f"  {'='*48}\n")
