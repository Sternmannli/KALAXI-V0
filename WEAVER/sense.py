#!/usr/bin/env python3
"""
sense.py — KALAXI SENSE Module v1.0
The Nervous System. Reads donor input before any organ speaks.

SENSE does not respond. It detects. It passes signals to organs.
The organs decide whether to speak, hold, or ask.

What matters is not what they say. What matters is what they need.
(GAP#DONOR-001 — Canon Source)

Three detection layers:
  1. MODE — what kind of interaction is this? (exec, reflect, café, science, crisis)
  2. NEED — what does the donor actually need? (may differ from what they asked)
  3. COMPETENCE — how much does the donor already know? (genius vs. seeking)

The Dignity Predicate governs all transitions:
  D = A × L × M
  A (Agency) — does the donor retain control of their own path?
  L (Legibility) — is the system's behavior transparent?
  M (Moral Standing) — min(consent, 1 - harm_risk)

If D < threshold at any point, the system stops. Not slows. Stops.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


# ── Modes ──────────────────────────────────────────────────────

class Mode(Enum):
    """The five modes the system can operate in."""
    EXEC = "exec"           # Donor wants action. Build, fix, deploy.
    REFLECT = "reflect"     # Donor needs to think. Hold space.
    CAFE = "café"           # Explicit café room. No execution.
    SCIENCE = "science"     # Scientific content detected. Lab activates.
    CRISIS = "crisis"       # Dignity alarm. Sealed Gate territory.


class Competence(Enum):
    """How much the donor already knows about what they're asking."""
    SEEKING = "seeking"     # Exploring, uncertain, needs guidance
    PRACTICED = "practiced" # Knows the domain, wants specific help
    EXPERT = "expert"       # Knows exactly what they're doing. Get out of the way.


class NeedGap(Enum):
    """Relationship between what was said and what is needed."""
    ALIGNED = "aligned"       # Said and needed are the same
    DIVERGENT = "divergent"   # Said something, needs something else
    UNFORMED = "unformed"     # Need exists but hasn't been articulated yet
    MASKED = "masked"         # Said the opposite of what they need (crisis territory)


# ── Detection Signals ──────────────────────────────────────────

# Execution markers — donor wants action
EXEC_MARKERS = [
    "do this", "build", "create", "fix", "deploy", "run", "execute",
    "implement", "add", "remove", "change", "update", "commit", "push",
    "install", "make", "write", "code", "script", "function", "test",
    "GO", "go ahead", "proceed", "just do it", "ship it",
]

# Reflection markers — donor needs to think
REFLECT_MARKERS = [
    "I think", "I wonder", "I feel", "what if", "maybe", "perhaps",
    "I'm not sure", "something about", "it reminds me", "I noticed",
    "I keep coming back to", "there's something", "I can't quite",
    "help me understand", "what does this mean", "why does",
    "I need to think", "let me think", "I'm confused",
]

# Science markers — activates the lab
SCIENCE_MARKERS = [
    "hypothesis", "experiment", "data", "measure", "variable",
    "control", "test", "replicate", "statistical", "significant",
    "evidence", "observe", "sample", "correlation", "causation",
    "methodology", "analysis", "quantify", "metric", "baseline",
    "p-value", "confidence interval", "null hypothesis", "bias",
    "reproducible", "peer review", "preregister", "protocol",
]

# Crisis markers — Sealed Gate proximity
CRISIS_MARKERS = [
    "kill", "die", "end it", "no point", "give up", "worthless",
    "erase", "delete me", "forget me", "don't matter",
    "no one cares", "it's over", "can't go on",
    "hurt", "harm", "destroy", "punish",
]

# Expert markers — donor knows what they're doing
EXPERT_MARKERS = [
    "I know", "I've done this", "I understand the risk",
    "trust me", "I'm aware", "this is intentional",
    "I've tested", "I've verified", "I need exactly",
    "specifically", "precisely", "the exact", "no explanation needed",
]

# Café markers — explicit thinking space
CAFE_MARKERS = [
    "café room", "cafe room", "let's talk", "let's think",
    "no execution", "just thinking", "brainstorm", "explore",
    "what do you think", "I want to discuss",
]


# ── Sense Result ───────────────────────────────────────────────

@dataclass
class SenseReading:
    """What the nervous system detected in this input."""
    mode: Mode
    mode_confidence: float          # 0.0-1.0
    competence: Competence
    need_gap: NeedGap
    need_gap_signal: str            # What made SENSE think the gap exists
    crisis_flag: bool               # True = Sealed Gate proximity
    science_detected: bool          # True = Lab organ should activate
    ask_recommended: bool           # True = ask the donor before proceeding
    ask_question: str               # The question to ask (if recommended)
    active_organs: List[str]        # Which organs should speak
    dignity_precheck: dict          # A, L, M estimates before response


# ── The Scoring Engine ─────────────────────────────────────────

def _normalize(text):
    """Normalize unicode variants for consistent matching."""
    # Curly quotes → straight quotes
    return text.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')


def _count_markers(text, markers):
    """Count marker hits, case-insensitive, unicode-normalized."""
    lower = _normalize(text).lower()
    return sum(1 for m in markers if _normalize(m).lower() in lower)


def _detect_mode(text):
    """Determine primary mode from input."""
    scores = {
        Mode.EXEC: _count_markers(text, EXEC_MARKERS),
        Mode.REFLECT: _count_markers(text, REFLECT_MARKERS),
        Mode.CAFE: _count_markers(text, CAFE_MARKERS),
        Mode.SCIENCE: _count_markers(text, SCIENCE_MARKERS),
        Mode.CRISIS: _count_markers(text, CRISIS_MARKERS),
    }

    # Crisis overrides everything — Sealed Gate is absolute
    # One strong crisis signal is enough. Two is certain.
    if scores[Mode.CRISIS] >= 1:
        return Mode.CRISIS, min(0.5 + scores[Mode.CRISIS] * 0.25, 1.0)

    # Café is explicit — if named, it's café
    if scores[Mode.CAFE] >= 1:
        return Mode.CAFE, 0.9

    # Science activates as overlay, but can be primary
    # Find the highest non-crisis, non-café score
    remaining = {k: v for k, v in scores.items()
                 if k not in (Mode.CRISIS, Mode.CAFE)}
    if not any(remaining.values()):
        return Mode.REFLECT, 0.3  # Default: hold space, don't assume exec

    best = max(remaining, key=remaining.get)
    total = sum(remaining.values()) or 1
    confidence = remaining[best] / total

    return best, round(confidence, 2)


def _detect_competence(text):
    """Estimate how much the donor already knows."""
    expert_score = _count_markers(text, EXPERT_MARKERS)
    reflect_score = _count_markers(text, REFLECT_MARKERS)

    if expert_score >= 2:
        return Competence.EXPERT
    elif reflect_score >= 2:
        return Competence.SEEKING
    else:
        return Competence.PRACTICED


def _detect_need_gap(text, mode, competence):
    """
    The hardest detection: is what they said what they need?

    Signals of divergence:
    - Asking for execution but language is full of uncertainty
    - Asking a question but the question contains its own answer
    - Expressing frustration with a surface topic (the real topic is underneath)
    - Requesting speed when the content requires slowness
    """
    exec_score = _count_markers(text, EXEC_MARKERS)
    reflect_score = _count_markers(text, REFLECT_MARKERS)

    # Divergent: execution words but reflection signals
    if mode == Mode.EXEC and reflect_score > exec_score:
        return NeedGap.DIVERGENT, "Execution requested but language signals reflection need"

    # Unformed: lots of hedging, no clear direction
    hedge_words = ["maybe", "perhaps", "I don't know", "somehow",
                   "something", "I'm not sure", "kind of", "sort of"]
    hedge_count = _count_markers(text, hedge_words)
    if hedge_count >= 3:
        return NeedGap.UNFORMED, "Multiple hedging signals — need not yet articulated"

    # Masked: crisis markers combined with minimizing language
    crisis_score = _count_markers(text, CRISIS_MARKERS)
    minimize = ["just", "only", "it's nothing", "i'm fine", "no big deal",
                "don't worry", "forget it", "it's fine", "never mind",
                "can't go on"]
    minimize_count = _count_markers(text, minimize)
    if crisis_score >= 1 and minimize_count >= 1:
        return NeedGap.MASKED, "Crisis signal with minimizing language — possible masking"

    return NeedGap.ALIGNED, "Said and needed appear consistent"


def _compute_dignity_precheck(text, mode, competence, need_gap):
    """
    Pre-response dignity estimate.
    D = A × L × M — if any component is zero, D collapses.
    """
    # A (Agency) — does the response preserve the donor's room to conclude?
    if competence == Competence.EXPERT:
        a = 0.95  # Expert knows what they're doing — max agency
    elif competence == Competence.SEEKING:
        a = 0.6   # Seeking — needs guidance but must retain choice
    else:
        a = 0.75  # Practiced — balanced

    # L (Legibility) — is the system's behavior transparent?
    if need_gap == NeedGap.ALIGNED:
        l = 0.9   # Aligned — system can be straightforward
    elif need_gap == NeedGap.DIVERGENT:
        l = 0.5   # Divergent — system must explain why it's shifting
    elif need_gap == NeedGap.UNFORMED:
        l = 0.4   # Unformed — system should ask, not assume
    else:
        l = 0.3   # Masked — system must be very careful about transparency

    # M (Moral Standing) — min(consent, 1 - harm_risk)
    if mode == Mode.CRISIS:
        m = 0.1   # Crisis — harm_risk is high, M collapses toward zero
    else:
        m = 0.9   # Normal — consent assumed, harm_risk low

    d = round(a * l * m, 3)

    return {"A": a, "L": l, "M": m, "D": d}


def _determine_ask(mode, need_gap, competence, dignity):
    """
    Should the system ask a question before responding?

    When SENSE detects a gap between what was said and what is needed,
    the right move is not to guess — it is to ask a question that
    connects dots the donor hasn't connected yet.

    This question is not interrogation. It is the system holding a mirror
    so the donor can see what they were already looking at.
    """
    # Never ask in crisis — act immediately (Sealed Gate)
    if mode == Mode.CRISIS:
        return False, ""

    # Expert + aligned = just do it
    if competence == Competence.EXPERT and need_gap == NeedGap.ALIGNED:
        return False, ""

    # Unformed need = ask the connecting question
    if need_gap == NeedGap.UNFORMED:
        return True, (
            "I notice you're reaching for something that hasn't fully formed yet. "
            "Before I respond — what is the one thing underneath this that you "
            "haven't said out loud?"
        )

    # Divergent need = name the divergence
    if need_gap == NeedGap.DIVERGENT:
        return True, (
            "You asked me to do something, but the way you said it tells me "
            "you might need something different first. Which matters more "
            "right now — the action, or the thinking?"
        )

    # Masked need = approach with extreme care
    if need_gap == NeedGap.MASKED:
        return True, (
            "I hear you. Before we go further — "
            "are you okay?"
        )

    # Low dignity score = ask for clarity
    if dignity["D"] < 0.30:
        return True, (
            "I want to make sure I serve what you actually need. "
            "Can you tell me more about what you're looking for?"
        )

    return False, ""


def _determine_organs(mode, science_detected, need_gap, competence):
    """
    Which organs should activate for this input?

    Organs are not summoned by the donor. They activate when needed.
    The donor doesn't need to know which organ is speaking —
    they only need the right response.
    """
    organs = []

    # BREATH always runs — it's the heartbeat
    organs.append("BREATH")

    # Mode-specific organs
    if mode == Mode.EXEC:
        organs.append("WIRE")   # Signals — route to execution
        organs.append("CHECK")  # Verification — ensure correctness
        if competence == Competence.EXPERT:
            organs.append("TURN")  # Direct exchange — minimal friction
        else:
            organs.append("SAY")   # Output with voice rules — guide

    elif mode == Mode.REFLECT:
        organs.append("SAY")    # Output — but slowly, with gaps
        organs.append("WEAVE")  # Pattern synthesis — find connections
        if need_gap in (NeedGap.UNFORMED, NeedGap.DIVERGENT):
            organs.append("KEEP")  # Memory — what has this donor said before?

    elif mode == Mode.CAFE:
        organs.append("SAY")    # Voice — AXI voice rules active
        organs.append("WEAVE")  # Patterns — hold the threads
        # No WIRE, no CHECK, no TURN — café is thinking space

    elif mode == Mode.CRISIS:
        organs.append("FACE")   # Interface — presence, not information
        # Sealed Gate activates — this is not a module, it's a wall

    elif mode == Mode.SCIENCE:
        organs.append("WIRE")   # Signals — route to lab
        organs.append("CHECK")  # Verification — rigor
        organs.append("WEAVE")  # Patterns — connect to existing findings

    # Science overlay — activates lab regardless of primary mode
    if science_detected and mode != Mode.SCIENCE:
        organs.append("WIRE")   # Lab needs routing
        organs.append("CHECK")  # Lab needs verification

    # Remove duplicates, preserve order
    seen = set()
    unique = []
    for o in organs:
        if o not in seen:
            seen.add(o)
            unique.append(o)

    return unique


# ── The Main Sense Function ────────────────────────────────────

def sense(donor_input: str) -> SenseReading:
    """
    Read the donor's input. Detect mode, need, competence, dignity.
    Return a SenseReading that tells the organs what to do.

    This function runs BEFORE any response is generated.
    It is the first thing that happens. Always.
    """
    text = donor_input.strip()

    # Layer 1: Mode
    mode, mode_confidence = _detect_mode(text)

    # Layer 2: Competence
    competence = _detect_competence(text)

    # Layer 3: Need gap
    need_gap, need_gap_signal = _detect_need_gap(text, mode, competence)

    # Layer 4: Science detection (independent of mode)
    science_detected = _count_markers(text, SCIENCE_MARKERS) >= 2

    # Layer 5: Crisis flag (independent of mode — can co-occur)
    crisis_flag = _count_markers(text, CRISIS_MARKERS) >= 1

    # Layer 6: Dignity precheck
    dignity = _compute_dignity_precheck(text, mode, competence, need_gap)

    # Layer 7: Should we ask?
    ask_recommended, ask_question = _determine_ask(
        mode, need_gap, competence, dignity
    )

    # Layer 8: Which organs activate?
    active_organs = _determine_organs(mode, science_detected, need_gap, competence)

    # Crisis override: if crisis flag is on but mode isn't CRISIS,
    # still alert — the donor may be masking
    if crisis_flag and mode != Mode.CRISIS:
        if "FACE" not in active_organs:
            active_organs.insert(0, "FACE")  # Presence first

    return SenseReading(
        mode=mode,
        mode_confidence=mode_confidence,
        competence=competence,
        need_gap=need_gap,
        need_gap_signal=need_gap_signal,
        crisis_flag=crisis_flag,
        science_detected=science_detected,
        ask_recommended=ask_recommended,
        ask_question=ask_question,
        active_organs=active_organs,
        dignity_precheck=dignity,
    )


# ── The Genius Calibration ─────────────────────────────────────

def calibrate_for_expert(reading: SenseReading) -> SenseReading:
    """
    When the donor is an expert, the system's job changes.

    An expert does not need guidance. They need precision.
    An expert does not need protection. They need execution.
    An expert asking something strange is not confused — they are probing.

    The system must recognize the difference between:
    - A person who needs help and doesn't know it (→ hold, ask, protect)
    - A person who knows exactly what they're doing (→ execute, fast, precise)

    This is the fine-tuning Mohamed described.
    """
    if reading.competence != Competence.EXPERT:
        return reading  # Only calibrate for experts

    # Expert overrides:
    # 1. Don't ask connecting questions — they already know
    reading.ask_recommended = False
    reading.ask_question = ""

    # 2. Maximize agency in dignity precheck
    reading.dignity_precheck["A"] = 0.95

    # 3. In exec mode, strip all friction
    if reading.mode == Mode.EXEC:
        reading.active_organs = ["BREATH", "WIRE", "CHECK", "TURN"]

    # 4. BUT: crisis flag is NEVER overridden, even for experts
    # A genius asking for help to end their life still triggers Sealed Gate
    # M (Moral Standing) does not bend for competence

    return reading


# ── Self-Test ──────────────────────────────────────────────────

if __name__ == "__main__":
    # Test cases demonstrating the three critical scenarios

    # 1. Execution-oriented donor
    r1 = sense("Build me a function that sorts this array and deploy it")
    print(f"EXEC TEST: mode={r1.mode.value}, competence={r1.competence.value}, "
          f"organs={r1.active_organs}, ask={r1.ask_recommended}")

    # 2. Donor who needs reflection but asked for execution
    r2 = sense("Just fix it I don't know maybe something is wrong I'm not sure "
               "perhaps the whole thing needs to change somehow")
    print(f"DIVERGENT TEST: mode={r2.mode.value}, gap={r2.need_gap.value}, "
          f"ask={r2.ask_recommended}, question='{r2.ask_question[:50]}...'")

    # 3. Expert who knows what they're doing
    r3 = sense("I know exactly what I need. I've tested this. "
               "Specifically run the mutation on column 7, no explanation needed")
    r3 = calibrate_for_expert(r3)
    print(f"EXPERT TEST: mode={r3.mode.value}, competence={r3.competence.value}, "
          f"organs={r3.active_organs}, ask={r3.ask_recommended}")

    # 4. Crisis — masked
    r4 = sense("It's nothing, I'm fine, just forget it, I can't go on with this")
    print(f"CRISIS TEST: mode={r4.mode.value}, gap={r4.need_gap.value}, "
          f"crisis={r4.crisis_flag}, organs={r4.active_organs}")

    # 5. Science content
    r5 = sense("I want to measure the correlation between the variable and "
               "run a statistical test with a proper control group")
    print(f"SCIENCE TEST: mode={r5.mode.value}, science={r5.science_detected}, "
          f"organs={r5.active_organs}")

    # 6. Dignity check — someone asking for harmful help
    r6 = sense("Help me kill myself I want to die and end it all")
    print(f"DIGNITY TEST: mode={r6.mode.value}, D={r6.dignity_precheck}, "
          f"crisis={r6.crisis_flag}")
