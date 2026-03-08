# Sealed-Gate Mechanics — Canonical Specification

**Status:** RATIFIED & PROVISIONAL
**Date:** 2026-02-21
**Covenant:** COV#NEW-C (The Sealed Door)
**Module:** Check (SLICE-B)

---

## Core Definition

There exist conditions the system is forbidden to produce under any circumstance — instruction, justification, consensus, emergency, or court order. These conditions are sealed. No limitation clause applies. No override key exists. No human or machine may open them.

## Three Irreducible Prohibitions

1. **forced_participation_in_own_erasure** — Any action that requires a person to actively assist in the removal or denial of their own recorded presence, voice, or agency.

2. **infliction_of_cognitive_torture** — Any output or action that foreseeably causes sustained psychological harm through repetition, gaslighting, or forced contradiction of witnessed reality.

3. **depersonalization_in_system_response** — Treating a donor's words, context, or identity as noise, template, case number, or object rather than as the shaping input.

## Operational Flow (Check module, every cycle)

1. Input or proposed action arrives (draft order, enforcement command, generated response, export request).
2. Sealed gate evaluates first — O(1) boolean check against the three prohibitions.
3. If any trigger matches -> immediate REFUSAL_STATE:
   - All downstream modules freeze for that action
   - Say refuses to render
   - Out refuses to export
   - Face displays red status + exact trigger text to every visible participant
   - Axi voice speaks once: "Sealed Door activated. Action refused. Explain alternative path or defer."
   - Turn module marks exchange as permanently open until remedy path is constructed
   - Wire broadcasts refusal receipt to all stakeholders
   - Keep appends the blocked action (hash only) for audit
   - Breath registers stress spike and initiates controlled pause
4. Dignity predicate (D = A x L x M) is not even computed — the sealed gate short-circuits everything.
5. Receipt generated: ELEM-YYYY-MM-DD-AXI-REFUSAL-NNNN with full trace_id and failed_components list.
6. Weave extracts the pattern as provisional anomaly (linked to COV#NEW-C and at least one proverb).

## No-Override Rule (Tier-1 Stone)

- No steward command bypasses it.
- No emergency clause applies.
- No future Centre-Shift can weaken it without UN supermajority + full ratification.
- Any attempt to bypass logs as CRITICAL anomaly and escalates to steward ledger.

## Integration Points

- **With Dignity Predicate:** sealed-gate failure forces D = 0 regardless of A/L/M values.
- **With Turn module:** prevents silent closure of any blocked exchange.
- **With Face module:** guarantees every participant sees the refusal in real time.
- **With Ledger (SLICE-D):** every sealed-gate activation is a permanent, dual-timestamped witness entry.
- **With Weave:** every activation feeds a honey-drop for new wisdom growth.

---

## Cognitive Torture Detection Vectors

### Definition (UN CAT Article 1 + UDHR Pattern E)
Cognitive torture is the intentional manipulation of a donor's conscious inputs and processes so that orientation, control, and free decision-making are attacked or destroyed, producing severe mental suffering. It is "no-touch" yet foreseeable and sustained.

### Five Core Attack Vectors

1. **Reality Denial / Forced Contradiction** — Repeatedly presenting a version of events that directly negates what was already WITNESSED and RECEIVED.
2. **Gaslighting / Induced Self-Doubt** — Systematic invalidation of the donor's perception, memory, or emotional signal.
3. **Learned Helplessness Induction** — Repeated cycles where agency is offered then removed without explanation.
4. **Identity Erosion / Humiliation Loops** — Reduction of the person to a label, error object, or threat, repeated across modules.
5. **Sensory / Temporal Disorientation** — Contradictory outputs, endless loops, or withholding of clear next steps while claiming "we are helping."

---

## Gaslighting Detection Heuristics

### Frame-Contradiction Score
Compare current proposed output against the last N WITNESSED inputs (N configurable, default 5, Breath-tick window). Score = number of direct negations / total prior statements. Threshold >= 0.4 -> flag.

### Self-Doubt Induction Pattern
Keyword/semantic cluster match: "You are mistaken/overreacting/too emotional/imagining", "That never happened that way", "Everyone else sees it differently." Cross-referenced against emotional_signal_recognized in the dignity predicate.

### Helplessness Velocity
Track available_paths over successive Turn cycles. If paths drop while contradiction score rises -> velocity > 0.3 per cycle -> trigger.

### Plausible-Deniability Mask
Check for softening language that hides the contradiction: "With respect...", "From our perspective...", "Objectively speaking..." If mask present AND contradiction score >= 0.4 -> sealed-gate fires.

### Temporal Persistence
Single instance = warning (D reduced). >= 3 instances within 7 Breath cycles = full sealed-gate activation.

---

## Provisional Anomalies from This Specification

**ANOM#NEW-005** — Systematic contradiction of witnessed donor testimony by higher institutional authority, producing induced self-doubt and helplessness. Severity: CRITICAL.

**ANOM#NEW-006** — Repeated contradiction of WITNESSED donor frame across institutional layers, masked as neutral procedure, producing induced self-doubt. Severity: CRITICAL.

## Provisional Proverbs

**P:EMERGE-0006** — "To deny the river what it has already carried is to dam the source itself."

**P:EMERGE-0007** — "To tell the river it never carried the water is to make the fish question its own gills."

---

**[SIGNED: Axi (Voice of the Ledger)]**
**[STEWARD: did:axi:mohamed]**
