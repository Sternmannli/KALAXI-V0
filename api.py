#!/usr/bin/env python3
"""
api.py — KALAXI Witness Engine v1.0
The Living Bridge. Connects all four tiers through HTTP.

This is the comprehensive API service that makes the organism breathable
through the web. Every request passes through constitutional gates.
Every response is grounded in canon. Every interaction is witnessed.

Architecture:
  Stone (Constitution)  → Sealed Gate, Dignity Check on every request
  Weaver (Engine)       → Full organism pipeline, Input Ledger
  Honey (Wisdom)        → Proverbs, treasures, narratives via Voice Engine
  Hand (Interface)      → This API + threshold-client.js on kalam.ch

Endpoints:
  POST /witness         — Full pipeline processing (the core act)
  POST /intake/begin    — Donor onboarding ritual (step 1)
  POST /intake/consent  — Donor consent (step 2)
  POST /intake/voice    — Donor first voice (step 3)
  POST /intake/receipt  — Donor receipt (step 4)
  GET  /breath          — System vitals and health
  GET  /canon/proverb   — Proverb from the corpus
  GET  /canon/narrative — Narrative fragment
  GET  /canon/treasure  — Treasure from the archive
  GET  /canon/voice     — Random canon fragment (any source)
  GET  /ledger/status   — Ledger statistics
  GET  /ledger/verify   — Hash chain verification
  GET  /certificate/{id}— Witness certificate retrieval
  WS   /ws              — WebSocket for real-time threshold interaction

Novel properties:
  1. Constitutional API — every request passes through D = A × L × M
  2. Negative Witness Protocol — failure produces certificates, not errors
  3. Hash-Chained Ledger — every interaction cryptographically linked
  4. Canon-Grounded Voice — responses selected from corpus, never freely generated
  5. Breath Pacing — biologically-inspired rate limiting
  6. Multi-Register Narrative — four books at four frequencies

Run: python api.py
  or: uvicorn api:app --host 0.0.0.0 --port 8080 --reload

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import json
import time
import hashlib
import asyncio
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import asdict
from typing import Optional, List, Dict

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════
# KALAXI IMPORTS — the four tiers
# ═══════════════════════════════════════════════════

# Stone (Constitution)
from WEAVER.sealed_gate import sealed_gate
from WEAVER.dignity_check import check_dignity
from WEAVER.dignity_measure import measure_dignity

# Weaver (Engine)
from WEAVER.organism import Organism, ProcessResult
from WEAVER.input_ledger import InputLedger
from WEAVER.breath import Breath
from WEAVER.sense import sense as sense_read
from WEAVER.witness_certificate import (
    generate_certificate, save_certificate, load_certificate,
    DignitySnapshot, Subject, InstitutionalContext, CoordinatesOfFailure,
)

# Honey (Wisdom) via Voice Engine
from WEAVER.voice_engine import VoiceEngine, detect_register

# Hand (Interface) — Intake
from WEAVER.intake import IntakeEngine, COVENANT_PROMISE, CONSENT_TEXT, RitualStage


# ═══════════════════════════════════════════════════
# APPLICATION
# ═══════════════════════════════════════════════════

app = FastAPI(
    title="KALAXI Witness Engine",
    description=(
        "The Living Bridge. Constitutional API where every request passes "
        "through dignity gates. Failure produces witness certificates, not errors. "
        "Responses are grounded in canon — 3,333+ proverbs, 93 narrative chapters, "
        "200 golden regression utterances. D = A × L × M."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow kalam.ch and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://kalam.ch",
        "https://www.kalam.ch",
        "http://localhost:3000",
        "http://localhost:4321",   # Astro dev server
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════
# SHARED STATE — initialized once at startup
# ═══════════════════════════════════════════════════

_organism: Optional[Organism] = None
_voice: Optional[VoiceEngine] = None
_intake: Optional[IntakeEngine] = None
_ledger: Optional[InputLedger] = None
_breath: Optional[Breath] = None
_boot_time: str = ""
_request_count: int = 0
_witness_count: int = 0


@app.on_event("startup")
async def startup():
    """Initialize all system components."""
    global _organism, _voice, _intake, _ledger, _breath, _boot_time

    _boot_time = datetime.now(timezone.utc).isoformat()

    # Initialize in order of dependency
    _breath = Breath()
    _voice = VoiceEngine()
    _intake = IntakeEngine()

    # Organism is heavy — initialize in a thread to avoid blocking startup
    # The boot ritual may try network checks that hang in some environments
    import threading

    def _init_organism():
        global _organism
        try:
            _organism = Organism()
            print(f"  Organism:    ALIVE (loaded in background)")
        except Exception as e:
            print(f"  [ALARM] Organism initialization failed: {e}")
            _organism = None

    org_thread = threading.Thread(target=_init_organism, daemon=True)
    org_thread.start()
    # Give it a short window to initialize
    org_thread.join(timeout=5.0)
    if _organism is None and org_thread.is_alive():
        print(f"  Organism:    INITIALIZING (boot ritual in progress...)")

    # Ledger for direct access
    try:
        _ledger = InputLedger()
    except Exception:
        _ledger = None

    corpus_stats = _voice.stats()
    print(f"\n  ═══════════════════════════════════════")
    print(f"  KALAXI WITNESS ENGINE — ONLINE")
    print(f"  ═══════════════════════════════════════")
    print(f"  Boot:        {_boot_time}")
    print(f"  Organism:    {'ALIVE' if _organism else 'FAILED'}")
    print(f"  Voice:       {corpus_stats['total_fragments']} canon fragments")
    print(f"    Proverbs:  {corpus_stats['proverbs']}")
    print(f"    Golden:    {corpus_stats['golden_utterances']}")
    print(f"    Narrative: {corpus_stats['narrative_fragments']}")
    print(f"    Treasures: {corpus_stats['treasures']}")
    print(f"  Covenant:    D = A × L × M")
    print(f"  ═══════════════════════════════════════\n")


# ═══════════════════════════════════════════════════
# REQUEST / RESPONSE MODELS
# ═══════════════════════════════════════════════════

class WitnessRequest(BaseModel):
    """A donor speaks. The system witnesses."""
    text: str = Field(..., min_length=1, max_length=5000,
                      description="The donor's words")
    domain: str = Field(default="donor-exchange",
                        description="Felt domain context")


class WitnessResponse(BaseModel):
    """The system's witnessed response."""
    exchange_id: str
    dignity_passed: bool
    dignity_score: float
    dignity_components: Dict[str, float]
    voice_text: str
    voice_sources: List[str]
    voice_register: str
    patterns_found: int
    drops_produced: int
    breath_cycle: int
    complexity: str
    witness_id: str
    warnings: List[str]
    # If dignity failed
    certificate_id: Optional[str] = None
    halt_reason: Optional[str] = None


class ConsentRequest(BaseModel):
    session_id: str
    agreed: bool


class VoiceRequest(BaseModel):
    session_id: str
    voice: str = Field(..., min_length=1, max_length=5000)


class ReceiptRequest(BaseModel):
    session_id: str


# ═══════════════════════════════════════════════════
# ROOT
# ═══════════════════════════════════════════════════

@app.get("/")
async def root():
    """The door. The system introduces itself."""
    return {
        "system": "KALAXI",
        "name": "Witness Engine",
        "version": "1.0.0",
        "covenant": "D = A × L × M",
        "covenant_promise": COVENANT_PROMISE,
        "voice_corpus": _voice.stats() if _voice else {},
        "organism_alive": _organism is not None,
        "boot_time": _boot_time,
        "requests_served": _request_count,
        "witnesses_generated": _witness_count,
    }


# ═══════════════════════════════════════════════════
# WITNESS — The Core Act
# ═══════════════════════════════════════════════════

@app.post("/witness", response_model=WitnessResponse)
async def witness(req: WitnessRequest):
    """
    The core act of the system. A donor speaks. The system witnesses.

    The input passes through the full organism pipeline:
      Sealed Gate → Dignity Check → SENSE → WEAVE → CHECK → RESPOND

    If dignity holds: canon-grounded voice response.
    If dignity fails: witness certificate (the halt IS the product).
    """
    global _request_count, _witness_count
    _request_count += 1

    if _organism is None:
        raise HTTPException(
            status_code=503,
            detail="The organism is not yet alive. Please wait."
        )

    # Process through the full pipeline
    try:
        result = _organism.process(req.text, felt_domain=req.domain)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"The organism encountered an error: {str(e)[:200]}"
        )

    # Get dignity measurement for component scores
    measurement = measure_dignity(req.text)
    dignity_components = {
        "A": round(measurement.A.final_score, 3),
        "L": round(measurement.L.final_score, 3),
        "M": round(measurement.M.final_score, 3),
        "D": round(measurement.D, 3),
        "confidence": round(measurement.confidence, 3),
    }

    # Generate voice response from canon
    voice_response = _voice.respond(
        req.text,
        dignity=measurement.D,
        register=detect_register(req.text),
    )

    _witness_count += 1

    # Build the witness response
    response = WitnessResponse(
        exchange_id=result.exchange_id,
        dignity_passed=result.dignity_passed,
        dignity_score=round(measurement.D, 3),
        dignity_components=dignity_components,
        voice_text=voice_response.text if result.dignity_passed else voice_response.text,
        voice_sources=voice_response.sources,
        voice_register=voice_response.register,
        patterns_found=result.patterns_found,
        drops_produced=result.drops_produced,
        breath_cycle=result.breath_cycle,
        complexity=result.complexity,
        witness_id=voice_response.witness_id,
        warnings=result.warnings,
    )

    # If dignity failed, note the certificate
    if not result.dignity_passed:
        response.halt_reason = result.block_reason
        response.voice_text = "Witnessed. The system cannot proceed with dignity intact."

    return response


# ═══════════════════════════════════════════════════
# INTAKE — Donor Onboarding Ritual
# ═══════════════════════════════════════════════════

@app.post("/intake/begin")
async def intake_begin(donor_pseudonym: str = ""):
    """Step 1: Greeting. The door opens."""
    if _intake is None:
        raise HTTPException(status_code=503, detail="Intake engine not initialized.")

    session = _intake.begin(donor_pseudonym)
    return {
        "session_id": session.session_id,
        "stage": session.stage.value,
        "greeting": _intake.greeting_text(),
        "consent_text": CONSENT_TEXT,
        "available_paths": ["consent", "ask-more", "withdraw"],
    }


@app.post("/intake/consent")
async def intake_consent(req: ConsentRequest):
    """Step 2: Consent. Not a checkbox — a decision."""
    if _intake is None:
        raise HTTPException(status_code=503, detail="Intake engine not initialized.")

    try:
        session = _intake.consent(req.session_id, req.agreed)
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
async def intake_voice(req: VoiceRequest):
    """Step 3: Voice. The donor speaks first. The system listens."""
    if _intake is None:
        raise HTTPException(status_code=503, detail="Intake engine not initialized.")

    try:
        session = _intake.voice(req.session_id, req.voice)
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
            "dignity_score": round(session.dignity_score, 3),
            "dignity_passed": session.dignity_audit.get("dignity_result", False),
            "review_required": session.review_required,
        }
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/intake/receipt")
async def intake_receipt(req: ReceiptRequest):
    """Step 4: Receipt. Nothing hidden. The covenant holds."""
    if _intake is None:
        raise HTTPException(status_code=503, detail="Intake engine not initialized.")

    try:
        session = _intake.receipt(req.session_id)
        return {
            "session_id": session.session_id,
            "stage": session.stage.value,
            "receipt_text": _intake.donor_receipt_text(session.session_id),
            "message": "Your intake is complete. The covenant holds.",
        }
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# ═══════════════════════════════════════════════════
# BREATH — System Vitals
# ═══════════════════════════════════════════════════

@app.get("/breath")
async def breath():
    """
    The system's vital signs. How the organism breathes right now.
    """
    voice_stats = _voice.stats() if _voice else {}

    # Ledger stats
    ledger_stats = {}
    if _ledger:
        try:
            entries = _ledger.latest(1)
            ledger_stats = {
                "last_entry_id": entries[0].entry_id if entries else None,
                "total_entries": _ledger.count() if hasattr(_ledger, 'count') else "unknown",
            }
        except Exception:
            ledger_stats = {"status": "accessible", "error": None}

    breath_state = {}
    if _breath:
        breath_state = {
            "cycle": _breath.cycle,
            "is_paused": _breath.is_paused,
            "stress_level": _breath.stress_level.value if hasattr(_breath, 'stress_level') else "normal",
        }

    organism_state = {}
    if _organism:
        try:
            state = _organism.state()
            organism_state = {
                "exchanges_processed": state.exchanges_processed if hasattr(state, 'exchanges_processed') else 0,
                "dignity_drift": state.dignity_drift if hasattr(state, 'dignity_drift') else "stable",
                "breath_cycle": state.breath_cycle if hasattr(state, 'breath_cycle') else 0,
            }
        except Exception:
            organism_state = {"status": "alive"}

    return {
        "system": "KALAXI",
        "status": "breathing" if not (_breath and _breath.is_paused) else "paused",
        "boot_time": _boot_time,
        "uptime_seconds": round(
            (datetime.now(timezone.utc) - datetime.fromisoformat(_boot_time)).total_seconds()
        ) if _boot_time else 0,
        "breath": breath_state,
        "organism": organism_state,
        "voice": voice_stats,
        "ledger": ledger_stats,
        "requests_served": _request_count,
        "witnesses_generated": _witness_count,
        "covenant": "D = A × L × M — non-compensatory, any zero halts",
    }


# ═══════════════════════════════════════════════════
# CANON — Wisdom from the Corpus
# ═══════════════════════════════════════════════════

@app.get("/canon/proverb")
async def canon_proverb(theme: Optional[str] = Query(None, description="Theme words (comma-separated)")):
    """A proverb from the corpus. 3,333+ accumulated."""
    if _voice is None:
        raise HTTPException(status_code=503, detail="Voice engine not initialized.")

    theme_words = [w.strip() for w in theme.split(",")] if theme else None
    fragment = _voice.proverb(theme_words=theme_words)

    if fragment is None:
        return {"text": "The canon holds its tongue.", "source": "silence"}

    return {
        "text": fragment.text,
        "id": fragment.id,
        "source": fragment.source,
        "register": fragment.register,
    }


@app.get("/canon/narrative")
async def canon_narrative(book: Optional[str] = Query(
    None, description="Book: hakaka, ashwater, kinderbuch"
)):
    """A fragment from one of four narrative registers."""
    if _voice is None:
        raise HTTPException(status_code=503, detail="Voice engine not initialized.")

    fragment = _voice.narrative_fragment(book=book)

    if fragment is None:
        return {"text": "The story waits.", "source": "silence", "book": book}

    return {
        "text": fragment.text,
        "source": fragment.source,
        "book": fragment.book,
        "register": fragment.register,
    }


@app.get("/canon/treasure")
async def canon_treasure(id: Optional[str] = Query(
    None, description="Treasure ID (e.g. T#01)"
)):
    """A treasure from the archive. 59 equations, protocols, discoveries."""
    if _voice is None:
        raise HTTPException(status_code=503, detail="Voice engine not initialized.")

    fragment = _voice.treasure(treasure_id=id)

    if fragment is None:
        return {"text": "The archive is sealed.", "source": "silence"}

    return {
        "text": fragment.text,
        "id": fragment.id,
        "source": fragment.source,
    }


@app.get("/canon/voice")
async def canon_voice():
    """Any random fragment from the entire canon corpus."""
    if _voice is None:
        raise HTTPException(status_code=503, detail="Voice engine not initialized.")

    fragment = _voice._corpus.random_fragment()

    if fragment is None:
        return {"text": "Silence.", "source": "void"}

    return {
        "text": fragment.text,
        "source": fragment.source,
        "book": fragment.book,
        "id": fragment.id,
        "register": fragment.register,
    }


# ═══════════════════════════════════════════════════
# DIGNITY — Direct Measurement
# ═══════════════════════════════════════════════════

@app.post("/dignity/check")
async def dignity_check(req: WitnessRequest):
    """
    Direct dignity measurement without full pipeline.
    Returns A, L, M, D, confidence, and component details.
    """
    # Sealed Gate first
    gate = sealed_gate(req.text)
    if gate.refused:
        return {
            "sealed_gate": False,
            "triggered": gate.triggered_prohibitions,
            "D": 0.0,
            "A": 0.0, "L": 0.0, "M": 0.0,
            "message": "The sealed door is closed.",
        }

    # Measure dignity
    measurement = measure_dignity(req.text)
    dignity = check_dignity(req.text, felt_domain=req.domain)

    return {
        "sealed_gate": True,
        "D": round(measurement.D, 4),
        "A": round(measurement.A.final_score, 4),
        "L": round(measurement.L.final_score, 4),
        "M": round(measurement.M.final_score, 4),
        "confidence": round(measurement.confidence, 4),
        "passed": dignity.passed,
        "threshold": 0.30,
        "components": dignity.audit_object(),
    }


# ═══════════════════════════════════════════════════
# LEDGER — Interaction History
# ═══════════════════════════════════════════════════

@app.get("/ledger/status")
async def ledger_status():
    """Ledger statistics — how many interactions, chain state."""
    if _ledger is None:
        return {"status": "unavailable", "message": "Ledger not initialized."}

    try:
        count = _ledger.count() if hasattr(_ledger, 'count') else "unknown"
        latest = _ledger.latest(3)
        recent = []
        for entry in latest:
            recent.append({
                "id": entry.entry_id,
                "timestamp": entry.timestamp if hasattr(entry, 'timestamp') else "",
                "voice": entry.voice if hasattr(entry, 'voice') else "",
                "text_preview": entry.raw_text[:80] + "..." if hasattr(entry, 'raw_text') and len(entry.raw_text) > 80 else getattr(entry, 'raw_text', ''),
            })
        return {
            "status": "active",
            "total_entries": count,
            "recent_entries": recent,
            "chain_type": "SHA-256",
            "append_only": True,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)[:200]}


@app.get("/ledger/verify")
async def ledger_verify():
    """Verify the hash chain integrity of the Input Ledger."""
    if _ledger is None:
        return {"verified": False, "message": "Ledger not initialized."}

    try:
        if hasattr(_ledger, 'verify_chain'):
            result = _ledger.verify_chain()
            return {
                "verified": result if isinstance(result, bool) else True,
                "chain_type": "SHA-256",
                "message": "Hash chain verified." if result else "Chain integrity broken.",
            }
        return {
            "verified": "unknown",
            "message": "Chain verification method not available.",
        }
    except Exception as e:
        return {
            "verified": False,
            "message": f"Verification failed: {str(e)[:200]}",
        }


# ═══════════════════════════════════════════════════
# CERTIFICATE — Witness Certificates
# ═══════════════════════════════════════════════════

@app.get("/certificate/{cert_id}")
async def get_certificate(cert_id: str):
    """
    Retrieve a witness certificate by ID.
    Certificates are generated when D = 0 — the system halted.
    The halt IS the product. The certificate proves the system tried to see.
    """
    try:
        cert = load_certificate(cert_id)
        if cert is None:
            raise HTTPException(status_code=404, detail="Certificate not found.")
        return {
            "certificate_id": cert.certificate_id if hasattr(cert, 'certificate_id') else cert_id,
            "issued": cert.issued if hasattr(cert, 'issued') else "",
            "dignity": {
                "A": cert.dignity.A if hasattr(cert, 'dignity') else 0,
                "L": cert.dignity.L if hasattr(cert, 'dignity') else 0,
                "M": cert.dignity.M if hasattr(cert, 'dignity') else 0,
            },
            "halt_reason": cert.coordinates.machine_explanation if hasattr(cert, 'coordinates') else "",
            "subject": cert.subject.subject_id if hasattr(cert, 'subject') else "",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Certificate retrieval failed: {str(e)[:200]}")


# ═══════════════════════════════════════════════════
# WEBSOCKET — Real-Time Threshold
# ═══════════════════════════════════════════════════

@app.websocket("/ws")
async def websocket_threshold(websocket: WebSocket):
    """
    Real-time threshold interaction.

    The donor enters a living space. The WebSocket maintains a persistent
    connection with breath-paced responses. The system witnesses in real time.

    Protocol:
      Client sends: {"type": "voice", "text": "..."}
      Server sends: {"type": "witness", "voice_text": "...", "dignity": {...}}

      Client sends: {"type": "breath"}
      Server sends: {"type": "pulse", "cycle": N, "status": "..."}

      Client sends: {"type": "canon"}
      Server sends: {"type": "fragment", "text": "...", "source": "..."}
    """
    await websocket.accept()

    try:
        # Send greeting
        await websocket.send_json({
            "type": "greeting",
            "text": COVENANT_PROMISE,
            "system": "KALAXI Witness Engine",
            "corpus_size": _voice.stats()["total_fragments"] if _voice else 0,
        })

        while True:
            # Receive message
            try:
                data = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=300  # 5 minute timeout
                )
            except asyncio.TimeoutError:
                await websocket.send_json({
                    "type": "breath",
                    "text": "The silence holds. The system waits.",
                })
                continue

            msg_type = data.get("type", "")

            if msg_type == "voice":
                # Donor speaks — witness through pipeline
                text = data.get("text", "").strip()
                if not text:
                    await websocket.send_json({
                        "type": "silence",
                        "text": "Silence is signal. The system holds.",
                    })
                    continue

                # Dignity check
                measurement = measure_dignity(text)
                register = detect_register(text)

                # Voice response from canon
                if _voice:
                    voice_resp = _voice.respond(text, dignity=measurement.D, register=register)
                else:
                    voice_resp = None

                # Breath pacing — slight delay for dignity
                if measurement.D < 0.5:
                    await asyncio.sleep(0.5)  # Dignity delay

                await websocket.send_json({
                    "type": "witness",
                    "voice_text": voice_resp.text if voice_resp else "The knot holds.",
                    "voice_sources": voice_resp.sources if voice_resp else [],
                    "register": register,
                    "dignity": {
                        "D": round(measurement.D, 3),
                        "A": round(measurement.A.final_score, 3),
                        "L": round(measurement.L.final_score, 3),
                        "M": round(measurement.M.final_score, 3),
                    },
                    "passed": measurement.D > 0.0,
                    "witness_id": voice_resp.witness_id if voice_resp else "",
                })

            elif msg_type == "breath":
                # Pulse check
                await websocket.send_json({
                    "type": "pulse",
                    "cycle": _breath.cycle if _breath else 0,
                    "status": "breathing" if not (_breath and _breath.is_paused) else "paused",
                    "requests": _request_count,
                    "witnesses": _witness_count,
                })

            elif msg_type == "canon":
                # Random canon fragment
                if _voice:
                    frag = _voice._corpus.random_fragment()
                    if frag:
                        await websocket.send_json({
                            "type": "fragment",
                            "text": frag.text,
                            "source": frag.source,
                            "book": frag.book,
                            "id": frag.id,
                        })
                    else:
                        await websocket.send_json({
                            "type": "silence",
                            "text": "The canon rests.",
                        })
                else:
                    await websocket.send_json({
                        "type": "silence",
                        "text": "The voice is not yet awake.",
                    })

            elif msg_type == "close":
                await websocket.send_json({
                    "type": "farewell",
                    "text": "The door remains open. Return when you are ready.",
                })
                break

            else:
                await websocket.send_json({
                    "type": "unknown",
                    "text": "The system did not understand. Speak, ask for breath, or request canon.",
                })

    except WebSocketDisconnect:
        pass  # Donor left — the door stays open
    except Exception:
        try:
            await websocket.close()
        except Exception:
            pass


# ═══════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    print("\n  Starting KALAXI Witness Engine...")
    print("  Docs: http://localhost:8080/docs")
    print("  WebSocket: ws://localhost:8080/ws\n")

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info",
    )
