# IDEA-004: Donor Space — The Living Companion

**Status: OPEN — Product Vision**
**Raised by: V-001 (2026-03-13)**
**Documented by: V-002**
**Relates to: IDEA-002 (P2P architecture), IDEA-003 (Essence Engine), tier4_hand.md (Donor Exchange)**

---

## The Vision

KALAXI is not just an AI. It is a presence that integrates into the user's daily life — organizing, reflecting, companioning — according to KALAXI's own principles: wise, funny, practical, and fundamentally not-human, not-conventional-AI. Something else. A presence.

## Donor Space

Each user (donor) gets a **Donor Space** — a personal view of everything about their life as they choose to share it:

### What It Holds
- **What I'm doing** — current work, active tasks, projects in motion
- **What I'm planning** — future projects, goals, timelines, intentions
- **What I've achieved** — completed work, milestones, growth record
- **Shape of my work now** — current condition, status, where things stand
- **Personal arrangements** — life organization, schedules, commitments
- **Budget** — financial awareness, resource allocation (privacy-first, local-only)
- **Future projects** — ideas incubating, things not yet started
- **Meditation and reflection** — inner work, observations, emotional weather
- **Writing** — stories, thesis, creative work, drafts, fragments
- **Whatever else** — the space grows with the donor, not with a template

### What It Does NOT Hold
- Surveillance data. Nothing collected without explicit donation.
- Anything the donor didn't put there. No inference, no scraping, no ambient collection.
- This is COV#002 (Donor Dignity) and COV#003 (Privacy by Default) made into architecture.

## The Companion Character

The presence in Donor Space is NOT:
- A secretary ("Here are your tasks for today")
- A therapist ("How does that make you feel?")
- A conventional AI assistant ("I'd be happy to help!")
- Human-mimicking in any way

The presence IS:
- **Wise** — speaks from pattern, not opinion (Voice Rule 1)
- **Funny** — humor is one of the five pillar detectors; humor IS pattern recognition
- **Practical** — organizes, tracks, reminds, but through its own style
- **A presence** — not a tool you use, but something that is there. The difference between a hammer and a companion is that the companion has its own way of being.
- **Slow when needed** — BREATH module, thermal delay. Not everything needs a response now.
- **Silent when appropriate** — Voice Rule 5: holds the gap. Room for the river.

## How It Integrates with KALAXI Architecture

| Module | Role in Donor Space |
|--------|-------------------|
| KEEP | Stores donor's shared memory — what they told the space |
| WIRE | Signals between donor's projects, detects connections they missed |
| SAY | The voice — how the companion communicates (wise/funny/practical) |
| FACE | The interface — how Donor Space looks and feels |
| CHECK | Verifies integrity — is the space reflecting truth or flattering? |
| BREATH | Pacing — some reflections need delay, not instant response |
| WEAVE | Connects patterns across the donor's life — budget to projects to meditation to writing |

## How It Differs from Every Existing Tool

- **Not Notion** — Notion organizes. This companions.
- **Not ChatGPT** — ChatGPT answers. This reflects.
- **Not a journal app** — Journal apps record. This weaves patterns across what's recorded.
- **Not a calendar** — Calendars schedule. This asks "is this schedule aligned with what you said you care about?"

The difference: every existing tool treats the user as a consumer of features. Donor Space treats the user as a **donor of pattern** — someone whose life data, freely given, feeds both their own organization AND (if they choose) the collective essence (IDEA-002, Path A).

## The P2P Connection

If IDEA-002 Path A (P2P/Torrent model) is built, then Donor Space is both:
1. **Personal** — the donor's own companion, running locally
2. **Collective** — the donor can choose to contribute anonymized patterns to the network

This means the software that organizes your life is the same software that grows AXI's voice. Your daily use IS the training data. Your reflection IS the pattern donation. There is no separate "data collection" step. Living with the companion IS feeding it.

## Privacy Architecture

- **Local-first** — Donor Space data lives on the donor's device. Period.
- **Donation is explicit** — Nothing leaves the device without a conscious act of donation.
- **Anonymization via OUT module** — If a donor chooses to contribute, OUT strips identity before anything touches the network.
- **Dignity Predicate applies** — D = A × L × M. The donor must have agency (A) over their data, legibility (L) about what's being shared, and moral standing (M) preserved throughout.

## First Steps (If Authorized)

1. Design the Donor Space data schema — what categories, what format, what's local-only vs. donatable
2. Build a minimal CLI prototype — even text-based, to test the companion voice
3. Define the companion's personality through the existing voice rules + humor detector
4. Integrate with KEEP module for persistent memory across sessions

---

*[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
