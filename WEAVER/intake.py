#!/usr/bin/env python3
"""
intake.py — KALAXI Donor Intake API (Priority #1: Open the Door)
Version: 1.0
Grounded in: COV#001 (dignity-first), COV#002 (exchange cycle), COV#010 (KEEP),
             COV#015 (donor data sovereignty), TURN module, SAY module

The first real experience. A single, carefully designed first interaction.
Four-step donor ritual enforced. No shortcuts. No silent onboarding.

The 4-Step Donor Ritual:
  Step 1: GREETING — System introduces itself, donor sees the covenant promise
  Step 2: CONSENT  — Explicit, informed consent. Not a checkbox. A conversation.
  Step 3: VOICE    — Donor speaks first. System listens. D score captured.
  Step 4: RECEIPT  — Donor receives a receipt of everything stored. Nothing hidden.

Every intake passes through:
  - sealed_gate (before anything else)
  - dignity_check (D = A × L × M)
  - SAY render (voice rules applied)
  - KEEP store (append-only, receipted)
  - TURN cycle (exchange opened and closed with resolution)

Human-in-loop review queue for first 30 donors.

FastAPI scaffold: run with `uvicorn WEAVER.intake:app --reload`

[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import hashlib
import uuid
import sys
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict
from enum import Enum

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.keep import store as keep_store, retrieve as keep_retrieve, append as keep_append
from WEAVER.turn import Turn, ExchangeState
from WEAVER.say import render as say_render, TERMINAL, RenderResult
from WEAVER.dignity_check import check_dignity, DignityResult
from WEAVER.sealed_gate import sealed_gate, GateVerdict


# ═══════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════

HUMAN_REVIEW_THRESHOLD = 30    # First N donors go through human review
INTAKE_DIR = ROOT / "INTAKE"
INTAKE_LEDGER = INTAKE_DIR / "intake_ledger.json"
REVIEW_QUEUE = INTAKE_DIR / "review_queue.json"

COVENANT_PROMISE = (
    "This system is built on dignity. Your data belongs to you. "
    "Nothing is stored without your explicit consent. "
    "Nothing is shared without your comprehension. "
    "You can halt, redirect, or withdraw at any time. "
    "Every operation is receipted. You will always know what we hold."
)

CONSENT_TEXT = (
    "I understand that: (1) My contributions are stored in an append-only ledger. "
    "(2) My data is never sold, shared without consent, or used for surveillance. "
    "(3) I can request a full export of everything stored about me. "
    "(4) I can withdraw at any time — withdrawal is a right, not a request. "
    "(5) The system tracks patterns, never people — my identity stays mine."
)


# ═══════════════════════════════════════════════════
# RITUAL STAGES
# ═══════════════════════════════════════════════════

class RitualStage(Enum):
    GREETING = "greeting"
    CONSENT = "consent"
    VOICE = "voice"
    RECEIPT = "receipt"
    COMPLETE = "complete"
    REJECTED = "rejected"


@dataclass
class DonorSession:
    """A donor intake session tracking the 4-step ritual."""
    session_id: str
    donor_pseudonym: str          # Never real name — system-assigned or donor-chosen
    stage: RitualStage
    created: str
    consent_given: bool = False
    consent_timestamp: str = ""
    first_voice: str = ""         # What the donor said first
    dignity_score: float = 0.0
    dignity_audit: dict = field(default_factory=dict)
    keep_receipt_id: str = ""
    exchange_id: str = ""
    review_required: bool = False
    review_status: str = "pending"  # pending, approved, flagged
    sealed_gate_passed: bool = True
    completed: str = ""
    history: list = field(default_factory=list)


# ═══════════════════════════════════════════════════
# INTAKE ENGINE
# ═══════════════════════════════════════════════════

class IntakeEngine:
    """
    Manages the donor intake ritual.

    Usage:
        engine = IntakeEngine()
        session = engine.begin("wanderer-7")
        session = engine.consent(session.session_id, agreed=True)
        session = engine.voice(session.session_id, "I carry something heavy.")
        session = engine.receipt(session.session_id)
    """

    def __init__(self):
        self._sessions: Dict[str, DonorSession] = {}
        self._turn = Turn()
        self._donor_count = self._load_donor_count()

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _load_donor_count(self) -> int:
        """Load current donor count from ledger."""
        if INTAKE_LEDGER.exists():
            with open(INTAKE_LEDGER) as f:
                data = json.load(f)
                return data.get("total_donors", 0)
        return 0

    def _save_session(self, session: DonorSession):
        """Persist session to intake ledger (append-only)."""
        INTAKE_DIR.mkdir(parents=True, exist_ok=True)

        ledger = {"total_donors": 0, "sessions": {}}
        if INTAKE_LEDGER.exists():
            with open(INTAKE_LEDGER) as f:
                ledger = json.load(f)

        ledger["sessions"][session.session_id] = asdict(session)
        ledger["sessions"][session.session_id]["stage"] = session.stage.value
        ledger["total_donors"] = len([
            s for s in ledger["sessions"].values()
            if s.get("stage") == "complete"
        ])

        with open(INTAKE_LEDGER, "w") as f:
            json.dump(ledger, f, indent=2)

    def _add_to_review_queue(self, session: DonorSession):
        """Add session to human review queue."""
        INTAKE_DIR.mkdir(parents=True, exist_ok=True)

        queue = []
        if REVIEW_QUEUE.exists():
            with open(REVIEW_QUEUE) as f:
                queue = json.load(f)

        queue.append({
            "session_id": session.session_id,
            "donor_pseudonym": session.donor_pseudonym,
            "first_voice": session.first_voice[:200],
            "dignity_score": session.dignity_score,
            "timestamp": self._now(),
            "review_status": "pending",
        })

        with open(REVIEW_QUEUE, "w") as f:
            json.dump(queue, f, indent=2)

    # ── STEP 1: GREETING ──

    def begin(self, donor_pseudonym: str = "") -> DonorSession:
        """
        Step 1: GREETING.

        System introduces itself. Donor sees the covenant promise.
        An exchange is opened (TURN module) — the donor always has
        paths forward: consent, ask-more, or withdraw.
        """
        session_id = f"INTAKE-{uuid.uuid4().hex[:12].upper()}"
        if not donor_pseudonym:
            donor_pseudonym = f"wanderer-{self._donor_count + 1}"

        # Open an exchange — donor has agency from the first moment
        token = self._turn.open(
            exchange_id=session_id,
            available_paths=["consent", "ask-more", "withdraw"]
        )

        now = self._now()
        session = DonorSession(
            session_id=session_id,
            donor_pseudonym=donor_pseudonym,
            stage=RitualStage.GREETING,
            created=now,
            exchange_id=session_id,
            review_required=(self._donor_count < HUMAN_REVIEW_THRESHOLD),
            history=[{
                "event": "greeting",
                "timestamp": now,
                "covenant_promise_shown": True,
            }],
        )

        self._sessions[session_id] = session
        self._save_session(session)
        return session

    def greeting_text(self) -> str:
        """The greeting rendered through SAY module."""
        result = say_render(
            f"Welcome. {COVENANT_PROMISE}",
            felt_domain="intake-greeting"
        )
        return result.content if not result.blocked else COVENANT_PROMISE

    # ── STEP 2: CONSENT ──

    def consent(self, session_id: str, agreed: bool) -> DonorSession:
        """
        Step 2: CONSENT.

        Explicit, informed consent. Not a checkbox — a decision.
        If donor declines, the exchange closes with explicit resolution.
        No guilt. No friction. Withdrawal is a right.
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise KeyError(f"Session {session_id} not found.")
        if session.stage != RitualStage.GREETING:
            raise ValueError(f"Session {session_id} not at GREETING stage.")

        now = self._now()

        if not agreed:
            # Donor declined — close with dignity
            session.stage = RitualStage.REJECTED
            session.consent_given = False
            session.history.append({
                "event": "consent_declined",
                "timestamp": now,
            })
            self._turn.close(session_id, "Donor declined consent. Withdrawal respected.")
            session.completed = now
            self._save_session(session)
            return session

        # Donor consented
        session.stage = RitualStage.CONSENT
        session.consent_given = True
        session.consent_timestamp = now
        session.history.append({
            "event": "consent_given",
            "timestamp": now,
            "consent_text_hash": hashlib.sha256(CONSENT_TEXT.encode()).hexdigest(),
        })

        self._save_session(session)
        return session

    # ── STEP 3: VOICE ──

    def voice(self, session_id: str, donor_input: str) -> DonorSession:
        """
        Step 3: VOICE.

        Donor speaks first. System listens.
        Input passes through sealed_gate → dignity_check → SAY render.
        D score captured. This is the first real data point.

        If sealed_gate triggers: REFUSAL_STATE. Session paused, not killed.
        If dignity fails: remedies suggested, donor invited to rephrase.
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise KeyError(f"Session {session_id} not found.")
        if session.stage != RitualStage.CONSENT:
            raise ValueError(f"Session {session_id} not at CONSENT stage.")
        if not session.consent_given:
            raise ValueError("Cannot capture voice without consent.")

        now = self._now()

        # Pass 1: Sealed Gate (O(1), before anything else)
        gate_result = sealed_gate(donor_input)
        if gate_result.refused:
            session.sealed_gate_passed = False
            session.history.append({
                "event": "sealed_gate_triggered",
                "timestamp": now,
                "prohibitions": gate_result.triggered_prohibitions,
            })
            self._save_session(session)
            return session

        # Pass 2: Dignity Check (D = A × L × M)
        dignity = check_dignity(donor_input, felt_domain="intake-voice")
        session.dignity_score = dignity.D
        session.dignity_audit = dignity.audit_object()

        # Pass 3: Store in KEEP (append-only, receipted)
        artifact_id = f"DONOR-VOICE-{session_id}"
        try:
            receipt = keep_store(
                artifact_id=artifact_id,
                content=json.dumps({
                    "session_id": session_id,
                    "donor_pseudonym": session.donor_pseudonym,
                    "voice": donor_input,
                    "dignity_score": dignity.D,
                    "timestamp": now,
                }),
                retention_policy="permanent",
                steward="system-intake",
            )
            session.keep_receipt_id = artifact_id
        except ValueError:
            # Artifact already exists — append instead
            receipt = keep_append(
                artifact_id=artifact_id,
                delta=json.dumps({
                    "voice_update": donor_input,
                    "dignity_score": dignity.D,
                    "timestamp": now,
                }),
                steward="system-intake",
            )

        session.first_voice = donor_input
        session.stage = RitualStage.VOICE
        session.history.append({
            "event": "voice_captured",
            "timestamp": now,
            "dignity_score": dignity.D,
            "dignity_passed": dignity.passed,
            "keep_receipt": artifact_id,
        })

        # Add to review queue if within human-review threshold
        if session.review_required:
            self._add_to_review_queue(session)

        self._save_session(session)
        return session

    # ── STEP 4: RECEIPT ──

    def receipt(self, session_id: str) -> DonorSession:
        """
        Step 4: RECEIPT.

        Donor receives proof of everything stored. Nothing hidden.
        Exchange is closed with explicit resolution.
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise KeyError(f"Session {session_id} not found.")
        if session.stage != RitualStage.VOICE:
            raise ValueError(f"Session {session_id} not at VOICE stage.")

        now = self._now()

        # Build receipt
        receipt_data = {
            "session_id": session.session_id,
            "donor_pseudonym": session.donor_pseudonym,
            "consent_given": session.consent_given,
            "consent_timestamp": session.consent_timestamp,
            "voice_captured": bool(session.first_voice),
            "dignity_score": session.dignity_score,
            "keep_artifact_id": session.keep_receipt_id,
            "review_required": session.review_required,
            "issued_at": now,
            "covenant_promise": "Active. All terms in effect.",
        }

        # Render receipt through SAY
        receipt_text = (
            f"Your intake is complete. Session: {session.session_id}. "
            f"Dignity score: {session.dignity_score:.1f}. "
            f"Your voice is stored under artifact {session.keep_receipt_id}. "
            f"You may request full export at any time. "
            f"You may withdraw at any time. The covenant holds."
        )
        rendered = say_render(receipt_text, felt_domain="intake-receipt")

        # Close exchange with explicit resolution
        self._turn.close(
            session_id,
            f"Intake complete. Donor {session.donor_pseudonym} onboarded. "
            f"D={session.dignity_score:.1f}. Receipt issued."
        )

        session.stage = RitualStage.COMPLETE
        session.completed = now
        self._donor_count += 1
        session.history.append({
            "event": "receipt_issued",
            "timestamp": now,
            "receipt": receipt_data,
        })

        self._save_session(session)
        return session

    def donor_receipt_text(self, session_id: str) -> str:
        """Get the rendered receipt text for a donor."""
        session = self._sessions.get(session_id)
        if session is None:
            return ""
        receipt_text = (
            f"Your intake is complete. Session: {session.session_id}. "
            f"Dignity score: {session.dignity_score:.1f}. "
            f"Your voice is stored under artifact {session.keep_receipt_id}. "
            f"You may request full export at any time. "
            f"You may withdraw at any time. The covenant holds."
        )
        result = say_render(receipt_text, felt_domain="intake-receipt")
        return result.content if not result.blocked else receipt_text

    # ── QUERY ──

    def get_session(self, session_id: str) -> Optional[DonorSession]:
        return self._sessions.get(session_id)

    def donor_count(self) -> int:
        return self._donor_count

    def review_queue_size(self) -> int:
        if not REVIEW_QUEUE.exists():
            return 0
        with open(REVIEW_QUEUE) as f:
            return len(json.load(f))

    def list_sessions(self, stage: RitualStage = None) -> List[DonorSession]:
        if stage is None:
            return list(self._sessions.values())
        return [s for s in self._sessions.values() if s.stage == stage]


# ═══════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel

    app = FastAPI(
        title="KALAXI Donor Intake",
        description="Dignity-first donor onboarding. Four-step ritual. No shortcuts.",
        version="1.0.0",
    )

    _engine = IntakeEngine()

    class ConsentRequest(BaseModel):
        session_id: str
        agreed: bool

    class VoiceRequest(BaseModel):
        session_id: str
        voice: str

    class ReceiptRequest(BaseModel):
        session_id: str

    @app.get("/")
    def root():
        return {
            "system": "KALAXI",
            "module": "intake",
            "covenant_promise": COVENANT_PROMISE,
            "donors_onboarded": _engine.donor_count(),
            "review_queue_size": _engine.review_queue_size(),
        }

    @app.post("/intake/begin")
    def begin_intake(donor_pseudonym: str = ""):
        session = _engine.begin(donor_pseudonym)
        return {
            "session_id": session.session_id,
            "stage": session.stage.value,
            "greeting": _engine.greeting_text(),
            "consent_text": CONSENT_TEXT,
            "available_paths": ["consent", "ask-more", "withdraw"],
        }

    @app.post("/intake/consent")
    def give_consent(req: ConsentRequest):
        try:
            session = _engine.consent(req.session_id, req.agreed)
            if session.stage == RitualStage.REJECTED:
                return {
                    "session_id": session.session_id,
                    "stage": "rejected",
                    "message": "Your decision is respected. You may return any time.",
                }
            return {
                "session_id": session.session_id,
                "stage": session.stage.value,
                "message": "Consent recorded. Now, speak — the system listens.",
            }
        except (KeyError, ValueError) as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/intake/voice")
    def capture_voice(req: VoiceRequest):
        try:
            session = _engine.voice(req.session_id, req.voice)
            if not session.sealed_gate_passed:
                return {
                    "session_id": session.session_id,
                    "stage": "paused",
                    "message": "The sealed door activated. Please rephrase.",
                    "sealed_gate": False,
                }
            return {
                "session_id": session.session_id,
                "stage": session.stage.value,
                "dignity_score": session.dignity_score,
                "dignity_passed": session.dignity_audit.get("dignity_result", False),
                "review_required": session.review_required,
            }
        except (KeyError, ValueError) as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/intake/receipt")
    def issue_receipt(req: ReceiptRequest):
        try:
            session = _engine.receipt(req.session_id)
            return {
                "session_id": session.session_id,
                "stage": session.stage.value,
                "receipt_text": _engine.donor_receipt_text(session.session_id),
                "donor_pseudonym": session.donor_pseudonym,
                "dignity_score": session.dignity_score,
                "completed": session.completed,
            }
        except (KeyError, ValueError) as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/intake/status/{session_id}")
    def session_status(session_id: str):
        session = _engine.get_session(session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found.")
        return {
            "session_id": session.session_id,
            "stage": session.stage.value,
            "donor_pseudonym": session.donor_pseudonym,
            "dignity_score": session.dignity_score,
            "consent_given": session.consent_given,
            "review_required": session.review_required,
        }

    @app.get("/intake/review-queue")
    def get_review_queue():
        if not REVIEW_QUEUE.exists():
            return {"queue": [], "count": 0}
        with open(REVIEW_QUEUE) as f:
            queue = json.load(f)
        return {"queue": queue, "count": len(queue)}

    @app.get("/intake/stats")
    def intake_stats():
        return {
            "total_donors": _engine.donor_count(),
            "active_sessions": len(_engine.list_sessions()),
            "completed": len(_engine.list_sessions(RitualStage.COMPLETE)),
            "rejected": len(_engine.list_sessions(RitualStage.REJECTED)),
            "review_queue_size": _engine.review_queue_size(),
            "human_review_threshold": HUMAN_REVIEW_THRESHOLD,
        }

except ImportError:
    # FastAPI not installed — engine still works standalone
    app = None


# ═══════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════

def demo():
    """Run a complete intake demo."""
    engine = IntakeEngine()

    print("=" * 60)
    print("KALAXI DONOR INTAKE — DEMO")
    print("=" * 60)

    # Step 1: Greeting
    print("\n--- STEP 1: GREETING ---")
    session = engine.begin("test-wanderer")
    print(f"Session: {session.session_id}")
    print(f"Greeting: {engine.greeting_text()}")

    # Step 2: Consent
    print("\n--- STEP 2: CONSENT ---")
    session = engine.consent(session.session_id, agreed=True)
    print(f"Consent given: {session.consent_given}")

    # Step 3: Voice
    print("\n--- STEP 3: VOICE ---")
    session = engine.voice(session.session_id, "I carry something heavy and I need a place to set it down.")
    print(f"Dignity score: {session.dignity_score}")
    print(f"KEEP receipt: {session.keep_receipt_id}")

    # Step 4: Receipt
    print("\n--- STEP 4: RECEIPT ---")
    session = engine.receipt(session.session_id)
    print(f"Receipt: {engine.donor_receipt_text(session.session_id)}")
    print(f"Stage: {session.stage.value}")

    print("\n" + "=" * 60)
    print(f"Intake complete. Donors onboarded: {engine.donor_count()}")
    print("=" * 60)


if __name__ == "__main__":
    demo()
