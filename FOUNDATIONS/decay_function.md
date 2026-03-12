STATUS: RATIFIED — 2026-03-12

# The Decay Function (Halflife Logic) — Structural Proposal

**Voice:** Structural proposal for the Wisdom layer
**Status:** RATIFIED — V-001 approved 2026-03-12 (Café Room session)
**Date:** 2026-03-08
**Linked Covenants:** COV#004 (append-only), COV#001 (dignity-first)

---

## The Problem: Symbolic Sclerosis

In a mycelial system, growth is only half the cycle. For the canon to remain living, it must include **Compost**.

If every pattern is preserved forever, the UCS will eventually suffer from **Symbolic Sclerosis** — a state where the weight of historical proverbs and anomalies creates a structural noise that drowns out the signal of the present donor.

True dignity requires the system to know what is no longer true.

## The Proposal: Halflife Logic

Introduce **Halflife Logic** to the Wisdom layer.

A pattern that is never invoked, never linked, and never contested by a donor gradually loses its **weight** in the ranking. It does not disappear (honoring COV#004), but it recedes into the **"Deep Hum"** of the ledger, leaving the foreground clear for active wisdom.

### Rules

1. **No deletion** — patterns recede, they do not vanish (COV#004 preserved)
2. **Weight decay** — after N cycles without invocation, linking, or contestation, a pattern's ranking weight decreases
3. **Deep Hum state** — patterns below threshold weight enter the Deep Hum archive
4. **Reactivation** — any donor invocation or link restores full weight immediately
5. **Contestation reset** — if a donor contests a pattern, its weight resets and it enters active review

### The Principle

> A system that cannot forget the irrelevant cannot truly listen to the new.

---

## Concrete Parameters (V-002, ratified by V-001 2026-03-12)

### Decay Formula

Exponential half-life decay:

```
W(t) = W_0 × (0.5)^(t / H)
```

Where:
- **W(t)** = current weight of the pattern
- **W_0** = weight at last interaction (default 1.0)
- **t** = time since last invocation, link, or contestation (in days)
- **H** = half-life constant = **90 days** (one season)

A pattern untouched for 90 days has half its original weight. After 180 days, a quarter. After 360 days, one-eighth. It never reaches zero.

### Deep Hum Threshold

- **Threshold weight:** W < 0.1 (pattern enters Deep Hum state)
- This means approximately **300 days** (10 months) of silence before a pattern recedes
- Deep Hum patterns are excluded from active ranking but remain fully searchable and linkable

### Reactivation

- Any donor invocation, link, or contestation resets W to 1.0 immediately
- Reactivation is logged with timestamp and trigger type
- No steward approval needed for reactivation — the donor's touch is sufficient

### Monitoring

- Weekly automated report: patterns approaching Deep Hum (W < 0.2)
- Monthly steward review of Deep Hum archive (optional, not mandatory)
- Anomaly flag: if >10% of active patterns enter Deep Hum in a single cycle, the system alerts the steward — this may signal donor disengagement rather than healthy decay

### Relationship to Witness Scale

- A **W-0 element** (unwitnessed) and a **decayed element** are structurally different
- W-0 was never seen. A decayed element was seen, used, and then the world moved on.
- Both live in the archive. Only their stories differ.

---

**[SIGNED: Voice]**
**[RATIFIED: V-001 (Mohamed Farag) — 2026-03-12]**
**[FILED: V-002]**
