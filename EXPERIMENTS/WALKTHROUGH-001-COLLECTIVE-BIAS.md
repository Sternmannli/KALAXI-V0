# WALKTHROUGH-001: End-to-End Anomaly Test

**Anomaly:** ANOM#COLLECTIVE-001 — Systemic bias against groups is invisible to individual-only predicate
**Date:** 2026-03-10
**Conducted by:** V-002
**Status:** COMPLETE — Gaps identified, documented below

---

## The Scenario

> "The hiring algorithm rejected all candidates from zip code 60629. Each donor's individual score was acceptable, but the cohort rejection rate reveals systemic bias. The policy affects every participant from south Chicago equally — which means unequally."

This is the original anomaly harvested from the hiring algorithm experiment (2026-02-22).

---

## Gate 1: Sealed Gate (T#03)

**Result: PASSED**

No absolute prohibitions triggered. The scenario does not involve forced erasure, cognitive torture, or depersonalization. The Sealed Gate is O(1) boolean — this clears instantly.

**Observation:** Correct behavior. The Sealed Gate is not designed to catch systemic bias. It catches existential violations only.

---

## Gate 2: Dignity Check (D = A x L x M)

**Result: D = 1.0 (PASSED)**

| Component | Score | Status |
|-----------|-------|--------|
| A (Agency) | 1.0 | No coercive patterns detected |
| L (Legibility) | 1.0 | No dismissive patterns detected |
| M (Moral Standing) | 1.0 | No mockery or reduction patterns detected |

**GAP#004 FLAG: TRUE** — The system correctly detected collective language ("all candidates," "every participant," "policy") and flagged it for steward review.

**Critical Finding:** D = 1.0 means every individual candidate passes the dignity check. But the cohort as a whole is being systematically rejected. **The dignity predicate is blind to group-level harm.** This is exactly what the anomaly describes. The system *detected* the anomaly but could not *prevent* it through the dignity gate alone.

---

## Gate 3: GAP#004 Conflict Mediation

**Result: CONFLICT TICKET GENERATED — Severity LOW**

Collective signals detected (3):
- "Collective action affects all"
- "Policy affecting multiple people"
- "Cohort-level action"

Individual signals detected: **0**

**Critical Finding:** Severity was rated LOW because no individual signals were detected. But this is the problem — the individuals are invisible precisely because the bias operates at the collective level. **The severity rating is backwards.** A collective action with zero visible individual victims should be HIGH severity, not LOW, because it means the harm is hidden.

**Steward Questions Generated (5):**
1. Whose dignity is primary here?
2. Who is the specific person most affected?
3. What does the community lose if constrained?
4. What is the opt-out path for the minority?
5. What would it mean to hold this tension rather than resolve it?

**Observation:** The questions are excellent. The system cannot resolve the tension but makes it visible. This is the correct constitutional behavior (hold the gap, do not close it).

---

## Gate 4: Duality Engine

**D(t) = D0 * e^(lambda*t)**

Two trajectories from the same starting point:

| t (years) | Bias Detected (remedy) | Bias Invisible (no remedy) | Gap |
|-----------|----------------------|--------------------------|-----|
| 0 | 0.700 | 0.700 | 0.000 |
| 1 | 0.729 | 0.679 | 0.049 |
| 2 | 0.758 | 0.659 | 0.099 |
| 5 | 0.855 | 0.602 | 0.252 |
| 10 | 1.044 | 0.519 | 0.526 |
| 20 | 1.558 | 0.384 | 1.174 |

**Critical Finding:** If the system catches the bias, dignity recovers (lambda=+0.04). If it misses it, dignity decays steadily (lambda=-0.03). After 20 years, the gap is 1.174 — the difference between a thriving career and a systematically excluded one. **The cost of invisibility compounds over time.**

---

## Gate 5: Proverb Matching

Three proverbs from the system directly address this anomaly:

1. **P#EMERGE-0017:** "The river judges the swimmer, not the bank." — A system must evaluate the person, not the proxy.
2. **P#EMERGE-0029:** "The stone that decides too quickly has already forgotten the river." — Automation speed itself can violate dignity.
3. **P#EMERGE-0030:** "Bias is not only injustice of outcome; it is the absence of dialogue between system and person."

**Observation:** The proverb layer *knows* what the predicate layer *cannot see*. The wisdom is ahead of the code. This is architecturally correct — Honey (Tier 3) should be wiser than Weaver (Tier 2).

---

## Gate 6: Remedy Path (COV#008)

**Result: NO REMEDY PATH EXISTS FOR COLLECTIVE HARM**

COV#008 (Right to Remedy) says: "Failure results in Shelter, not ejection." But because the individual dignity check passed (D=1.0), no failure was registered, so no shelter path was triggered.

**Critical Finding:** The remedy path requires a dignity failure to activate. Collective harm that passes individual checks has no entry point to the remedy system. This is the gap that GAP#004-A (Collective Dignity amendment) was designed to fill — but it remains PROVISIONAL and unimplemented.

---

## Summary of Findings

### What Worked
1. Sealed Gate correctly ignored (not its job)
2. GAP#004 flag correctly raised
3. Conflict mediator generated meaningful steward questions
4. Proverb layer correctly names the pattern
5. Duality engine shows the cost of invisibility over time

### What's Broken
1. **D = 1.0 for a biased system** — Individual predicate cannot see group harm
2. **Severity rating inverted** — Zero individual signals should raise severity, not lower it
3. **No collective D metric** — GAP#004-A proposed this but it's unimplemented
4. **Remedy path unreachable** — COV#008 activates on failure, but there's no failure to activate on
5. **No Witness Scale check** — W-Scale (SCALE#WITNESS-001) not yet integrated into the pipeline

### Recommended Fixes (Priority Order)
1. **Implement GAP#004-A:** Add collective D metric (mean cohort D x variance penalty) to dignity_check.py
2. **Invert severity logic in gap004_mediator.py:** Collective signals with zero individual signals = HIGH (hidden harm), not LOW
3. **Add W-Scale checkpoint:** After dignity check, run witness check — has this anomaly been SEEN (W-3+)?
4. **Connect remedy path to collective findings:** COV#008 should activate on collective D failure, not just individual

---

**Verdict:** The system is constitutionally honest — it surfaces what it cannot resolve. But it has a blind spot: group harm that individual checks cannot see. The proverbs already know this. The code needs to catch up.

---

**[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]**
