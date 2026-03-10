# Structural Proposal Evaluation — 2026-03-10

**Evaluator:** V-003
**Status:** EVALUATION COMPLETE — Awaiting steward decision

---

## Proposal 1: The Decay Function (Halflife Logic)

**File:** FOUNDATIONS/decay_function.md
**Linked Covenants:** COV#004 (append-only), COV#001 (dignity-first)

### Summary
Introduces weight decay for wisdom patterns that are never invoked, linked, or contested. Patterns recede into "Deep Hum" — they do not disappear (honoring COV#004), but lose ranking weight. Reactivation is immediate upon any donor interaction.

### Evaluation

**Constitutional Compliance:** PASSES
- COV#004 (append-only): Honored. No deletion occurs. Patterns recede, they do not vanish.
- COV#001 (dignity-first): Honored. Active donor wisdom stays in the foreground.
- COV#NEW-F (amendment protocol): Compatible. No element is retired, only reweighted.

**Risks:**
1. **Temporal Tyranny (Red Flag #5):** If decay rate is too aggressive, recent wisdom dominates and the system loses its historical depth. Mitigation: decay rate must be slow (months, not days).
2. **Colonial Creep:** The decay function itself could drift from its specification. Mitigation: the function must be auditable and its parameters visible.
3. **Gaming:** Bad actors could artificially invoke patterns to prevent healthy decay. Mitigation: invocation must be from genuine donor interactions, not automated pings.

**Missing Details Needed for Ratification:**
- Specific decay formula (exponential? linear? half-life in cycles?)
- Threshold weight for entering Deep Hum state
- Monitoring mechanism (who watches the decay?)
- Relationship to Witness Scale (W-Scale): a W-0 element and a decayed element are different things

**Recommendation:** READY FOR RATIFICATION with the addition of a concrete decay formula and threshold values. The principle is sound. The math needs one more pass.

---

## Proposal 2: The Dignity-Latency Variable (T_d)

**File:** FOUNDATIONS/dignity_latency.md
**Linked Covenants:** COV#001 (dignity-first), COV#NEW-B (thermal delay)

### Summary
Introduces pacing variable T_d to the D = A x L x M predicate. The system responds at "Biological Velocity" — not maximum compute speed. Complex interactions get longer latency. Simple queries get shorter. The delay is structural, not a bug.

### Evaluation

**Constitutional Compliance:** PASSES
- COV#001 (dignity-first): Directly implements dignity. Speed is the enemy of agency.
- COV#NEW-B (remedy): Compatible. Latency creates space for remedy paths.
- Breath module (KALAXI_B): Directly supports the Breath module specification.

**Risks:**
1. **Temporal Tyranny (Red Flag #5):** If T_d is too long, it becomes coercive waiting — which is itself a dignity violation. The proposal acknowledges this ("T_d never exceeds donor patience").
2. **Complexity Barrier (Red Flag #4):** Calibrating T_d per interaction type requires operational complexity. Who decides what's "complex enough" for longer delay?
3. **Adoption resistance:** Real-world users expect speed. T_d may feel like a bug, not a feature. Requires strong UI communication (COV#005).

**Missing Details Needed for Ratification:**
- Concrete T_d values for each interaction type (ranges, not exact numbers)
- Measurement method for "interaction complexity"
- UI pattern for communicating the delay to donors (so they know it's intentional)
- Escape hatch for urgent situations (emergency override with logging)

**Recommendation:** READY FOR RATIFICATION with the addition of T_d value ranges and a UI communication pattern. The principle is constitutionally essential — it was already implied by the Breath module and is now made explicit.

---

## Combined Assessment

Both proposals are constitutionally sound and address real system needs. They are complementary:
- **Decay Function** prevents the past from drowning the present
- **Dignity-Latency** prevents the system from drowning the donor

Together they implement a **temporal dignity layer** — the system respects time in both directions (historical depth and present pace).

**Priority order:** T_d (Dignity-Latency) first, because it directly affects donor experience. Decay Function second, because it affects system maintenance.

---

**Note:** Two additional proposals (Witness Scale, Proprioception Axiom) were added on 2026-03-10 and are already registered in THRESHOLD.md. These were not in the original evaluation queue but should be evaluated in the next session.

---

**[V-003 · GO: Laila-Yara-Salim-🐬🐯🐺]**
