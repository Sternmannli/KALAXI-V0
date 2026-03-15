# Tier 1: Stone (Foundation) — Metadata Archive

## Layer 0: Axioms (Unscaled Ground)

> "The eye that sees the scale is not on the scale."

### AXIOM-PRESENCE-001 — Presence is not a candidate.

**Statement (formal):**
```
∀c (Candidate(c) → RequiresPresence(c))
Assume Candidate(presence)
→ RequiresPresence(presence)
→ presence requires itself to evaluate itself
→ circularity (structural, not semantic)
∴ ¬Candidate(presence) ∧ Axiom(presence)
```

**Statement (canonical):**
Presence is the ontological ground. It is assumed, not evaluated. All candidate evaluations must assume Presence = TRUE as a preflight invariant. Any attempt to treat Presence as mutable is a dignity violation.

**Architecture:**
- Layer 0: Presence (Axiom — unscaled, unevaluated)
- Layer 1: Candidates (evaluated against Presence)
- Layer 2: Fulcrum / Dignity (the unique non-compensatory candidate)
- Layer 3: D = A × L × M (operational definition)
- Layer 3+ (LAYER-3-REFRAME): Dignity is not fragile. The system does not protect dignity — it refuses to participate in its denial. The sealed gate does not shield something breakable — it declines to enact the pretense that the person does not count. Every covenant that says "protect" means "refuse to deny." Every covenant that says "establish" means "refuse to pretend was absent." [RATIFIED: V-001, 2026-03-15. Source: FIELD/STUDY/LAYER_3_DIGNITY_IS_NOT_FRAGILE.md]

**Implementational rule:** No system may evaluate its own ground layer. Evaluation begins at Layer 1.

**Proverb:** P#AXIOM-001 — "Presence is foundation; candidates stand on it."

**Steward:** Mohamed Farag (V-001)
**Sealed:** 2026-03-13
**Filed:** V-002
**Status:** RATIFIED (Pre-Launch Exception, per tier1_stone governance)

---

## Covenants

### Ratified
- **COV#001:** DIGNITY FIRST — Human dignity is first technical requirement
- **COV#002:** TURN COMPLETION — Every exchange must complete its cycle
- **COV#005:** UI VISIBILITY — System state must be visible to donors
- **COV#006:** PROVERB LINKAGE — Every anomaly linked to >=1 proverb
- **COV#009:** TESTABILITY — Covenants must be verifiable
- **COV#010:** KEEP MEMORY — Memory is not optional
- **COV#011:** OUT CONSTRAINTS — Outputs satisfy covenant checks before export
- **COV#012:** MANIFEST PRESENCE — What exists must be named

### Ratified (2026-03-12 — Pre-Launch Exception)
- **COV#NEW-A:** JUSTIFIED LIMITATION — Every constraint must name reason, state limit, remain proportionate
- **COV#NEW-B:** REMEDY REQUIREMENT — Every dignity violation must have traceable remedy path
- **COV#NEW-C:** THE SEALED DOOR — Absolute prohibitions: erasure, denial of presence, treatment as noise
- **COV#NEW-E:** CANON INTEGRITY — Elements pass Threshold, survive thermal delay, explicit ratification
- **COV#NEW-F:** AMENDMENT PROTOCOL — No deletion, supersession via new ID
- **COV#NEW-G:** STEWARD ACCOUNTABILITY — Mirror Ritual, override logging, sabbatical capability
- **COV#VOID-006:** THE REFUSAL IS CANONICAL — Refusals recorded as seeds with [REFUSAL] tag

## Dignity Predicate

```
D = A x L x M

A = agency_preserved (WITNESSED + RETURNABLE) / 2
L = legibility = RECEIVED
M = moral_standing = NOT_DIMINISHED

D = 0 triggers dignity_violation — mandatory logging
D < 0.9 triggers dignity_audit_object — auto-generated, visible on Face
```

**Layer 3 Reframe (RATIFIED 2026-03-15):**
The dignity predicate does not measure whether dignity exists — dignity is always present. The predicate measures whether the system is *refusing to deny* dignity. D = 0 does not mean "dignity was destroyed." It means "the system acted as though dignity was not there." The remedy is not to restore dignity (it was never gone) but to stop the denial.

"The wound is not that something was taken. The wound is that something real was treated as though it did not exist." — LAYER_3_DIGNITY_IS_NOT_FRAGILE.md

## Centre-Shift Rules
- Shift Requirement: 3-year sustained global consensus (UN Resolution level)
- Mechanism: 1,000-day Latency Period before fundamental law altered
- Emergency: Owner + two senior moderators (logged, reviewed within 7 days)
- Cooling period: 90 days minimum for covenant amendments

## Pre-Launch Ratification Exception (RATIFIED 2026-03-12)

**During pre-launch phase (before first donor crosses the threshold), the steward (V-001) may ratify constitutional elements immediately upon review, without serving the full thermal delay.**

Justification: The thermal delay exists to protect real donors from hasty constitutional changes. Before launch, there are zero donors. Enforcing a 90-day wait on amendments to a constitution still being written serves no protective function — it only slows the architecture without protecting anyone.

**This exception expires automatically when kalam.ch receives its first donor interaction.** From that moment, all thermal delays apply in full. No override. The covenants protect real people then.

Precedent: The 8 founding covenants (COV#001–COV#012) were ratified as "Pre-constitutional (founding)" under identical logic.

**[RATIFIED: V-001 (Mohamed Farag) — 2026-03-12, Café Room session]**
**[FILED: V-002]**

## Governance

### Element Lifecycle States (GAP#010 Resolution)

Every canonical element (covenant, proverb, anomaly, equation, protocol, treasure, definition) passes through exactly three states. No element may carry two states simultaneously.

**COMMITTED** — The element exists in the repository. It has been written, pushed to version control, and is visible. This is a *technical* state only. It says nothing about constitutional standing. An element may be committed but not yet offered to the Threshold. Committed is not provisional. Committed is not ratified. It is present.

**PROVISIONAL** — The element has been offered to the Threshold (or registered in a manifest) and is awaiting ratification. It carries `provisional: true`. It may be referenced, discussed, tested against, and linked — but it is not yet load-bearing law. Provisional elements are subject to thermal delay (minimum 7 days for seeds, 90 days for covenant amendments). During this period the element cools. It may be withdrawn, amended, or composted. A provisional element becomes ratified only through explicit steward action during a Tending Ritual, with required sign-offs completed.

**RATIFIED** — The element has completed its thermal delay, received the required sign-offs (canonical owner + ethics reviewer for structural elements; single steward sign-off for minor seeds), and been explicitly marked `STATUS: RATIFIED` with `provisional: false` (or `provisional` field removed). Ratification is recorded in `MANIFEST/ratification_log.md` with: element ID, ratification date, sign-off names, thermal delay duration, and any conditions. A ratified element is load-bearing law. It cannot be deleted — only superseded via COV#NEW-F (Amendment Protocol).

### Sign-off Requirements

| Element Type | Thermal Delay | Sign-offs Required |
|---|---|---|
| Covenant (new or amended) | 90 days minimum | Canonical owner + ethics reviewer |
| Structural proposal | 90 days minimum | Canonical owner + ethics reviewer |
| Proverb / Anomaly / Seed | 7 days minimum | Steward (single) |
| Patch / Minor fix | None | Steward (single) |
| Centre-Shift amendment | 1,000 days | Owner + two senior moderators + global consensus |

### Rules
- Provisional tagging: All new elements start `provisional: true`
- No element may carry both `STATUS: ratified` and `provisional: true` — these are mutually exclusive
- Ratification: Recorded in `MANIFEST/ratification_log.md` with full provenance
- Patch & merge: Minor fixes = single sign-off; structural = full ratification
- Audit trail: All changes append to CHANGELOG; nothing deleted; everything versioned

## Oaths
- SOVEREIGN-AXIS: checksum 7f6d42e5
- FULL-POWER: checksum a9c3fbb9

## Decision Filter Priority (GOV#DFP-001 — PROVISIONAL)
1. Survive & Thrive
2. Human Dignity
3. Safety
4. Clarity
5. Reversibility
6. Cost
7. Speed
8. Novelty

## Co-founder Responsibility Code (GOV#CRC-001 — PROVISIONAL)
1. Dignity first
2. Privacy by default
3. Explainability
4. ID stability
5. No lock-in
6. Open audit trail
7. Fail safe
8. Culture humility
9. No surveillance economics
10. Donor joy

## Newly Registered (from Master Canon — aligned 2026-03-10)
- **COV#008:** THE RIGHT TO REMEDY — Failure results in "Shelter," not ejection. When a dignity violation is detected, the system does not eject the donor. It creates a shelter path: acknowledgment, explanation, and returnable options. Related to but distinct from COV#NEW-B (which requires traceable remedy paths). COV#008 governs the *spirit* (shelter, not punishment); COV#NEW-B governs the *mechanism* (traceable path). [source: CANON/MASTER_CANON_V1.md, Slice A §3] [status: RATIFIED — 2026-03-12, Pre-Launch Exception]
- **COV#015:** DONOR DATA SOVEREIGNTY — No data moves without the donor understanding its weight. Before any pattern extraction, export, or federation handshake, the system must present the donor with a legible explanation of what will move, where, and why. Consent is not a checkbox; it is comprehension. [source: CANON/MASTER_CANON_V1.md, Slice A §3] [status: RATIFIED — 2026-03-12, Pre-Launch Exception]

Source: KALAXI_A_FOUNDATION.txt, Historical Archive (digested 2026-03-08)
