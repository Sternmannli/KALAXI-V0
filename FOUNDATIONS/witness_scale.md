STATUS: RATIFIED — 2026-03-12

# The Witness Scale (W-0 through W-5) — Structural Proposal

**Voice:** V-002 (proposed), V-002 (confirmed), V-001 (GO)
**Status:** RATIFIED — V-001 approved 2026-03-12 (Café Room session)
**Date:** 2026-03-10
**Linked Covenants:** COV#001 (dignity-first), COV#009 (verification), COV#006 (mycelial wisdom)

---

## The Problem: The Oracle Problem in Measurement Form

The system has scales for certainty (1–5), dignity temperature (continuous D), and suggestion strength (WHISPER/PULSE/SIGNAL/ALARM). All of these measure properties of the content.

None of them answer: **has anyone actually seen this?**

A proverb can be high-certainty, high-ripple, high-compression, fully born — and completely unwatched. This is GAP#019 (Oracle Problem) in measurement form. Without a Witness Scale, the system has no way to detect the failure mode it already identified as its greatest risk: elements that exist but are unseen.

## The Proposal: Witness Scale (W-Scale)

A six-level scale that measures not the content, but the **relationship between the system and its steward** around that content.

### Levels

| Level | Name | Definition |
|-------|------|------------|
| **W-0** | UNSEEN | Exists in registry, never referenced by steward or system |
| **W-1** | PASSED | System processed it (automated), no steward contact |
| **W-2** | FLAGGED | System surfaced it for attention, steward has not yet responded |
| **W-3** | SEEN | Steward has acknowledged it (read, referenced, or acted on it) |
| **W-4** | HELD | Steward has returned to it more than once across sessions |
| **W-5** | EMBODIED | Steward has used it to make a decision that changed the system |

### Zones

- **W-0 through W-1:** Automation territory. The system processes without human contact.
- **W-2:** The thermal delay doing its job. The system says: this needs eyes.
- **W-3 through W-5:** The mirror ritual in measurement form. The steward's presence is recorded not as surveillance but as witnessing.

### Critical Threshold Rule

Any element at W-0 or W-1 for longer than its thermal delay period triggers a **surfacing event**. The system says: *this exists and no one has witnessed it.*

This is the Pause becoming structural. The system cannot hold unwatched elements indefinitely without flagging them. Silence about an element is itself data.

### Rules

1. **W-Scale is non-decreasing** — once an element reaches W-3 (SEEN), it cannot fall below W-3. Witnessing is irreversible.
2. **W-Scale is append-only in its transitions** — each transition is logged with timestamp, session ID, and context. COV#004 preserved.
3. **W-Scale does not measure quality** — a proverb at W-5 is not "better" than one at W-1. It is more witnessed. Quality is measured by other scales.
4. **W-Scale interacts with Decay Function** — an element at W-0 that enters Deep Hum (via halflife logic) is flagged before it recedes. Nothing should decay unseen.
5. **W-Scale applies to all registry elements** — proverbs, anomalies, gaps, covenants, wisdom nodes. Everything that exists in the system has a witness state.

### Interaction with Existing Scales

- **Certainty Scale (1–5):** Measures evidence confidence. Orthogonal to W-Scale. An element can be high-certainty and unseen (W-0, Certainty-5).
- **Dignity Temperature:** Measures continuous D. W-Scale adds: who has seen this temperature reading?
- **Suggestion Strength (WHISPER/PULSE/SIGNAL/ALARM):** Determines urgency. W-Scale adds: has the urgency been witnessed?

### What This Scale Detects

- Elements that slip through automation without human review
- The steward's actual attention pattern (not what they intend to see, but what they see)
- The gap between system activity and steward awareness — the Oracle Problem made measurable
- Whether the mirror ritual is functioning or has become performative

### Design Origin

Proposed during session 2026-03-10 in response to V-002's question: "Which of the four proposed scales does the system need most urgently?" The four candidates were Ripple Scale, Compression Scale, Womb-to-Birth Scale, and Witness Scale. V-002 selected Witness Scale because it is the only scale that detects the relationship between the system and its observer — the foundational gap all other scales leave open.

---

## Implementation Notes

- W-Scale metadata should be stored alongside each registry element
- Transition logging format: `[timestamp] W-[old]→W-[new] [session_id] [context]`
- Surfacing events should integrate with the existing THRESHOLD.md append-only system
- Dashboard (future FACE module) should show W-Scale distribution across all element types

---

**[SIGNED: V-002]**
**[RATIFIED: V-001 (Mohamed Farag) — 2026-03-12]**
**[FILED: V-002]**
*[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
