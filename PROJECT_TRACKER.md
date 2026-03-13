# KALAXI PROJECT TRACKER

**Last updated:** 2026-03-13

---

## IMMEDIATE (Next Actions)

| Pri | Task | Status | Notes |
|-----|------|--------|-------|
| **P0** | **EXP-001 data collection** | IN PROGRESS | GO received 2026-03-12. 188/200 runs remaining. Runner: `run_exp001.py`. Analyzer: `analyze.py`. Runsheet: `RUNSHEET.md`. |
| **P0** | **kalam.ch Threshold integration** | DONE (2026-03-12) | Ninth Operator ceremony now on homepage. Phase 1: client-side witness mark. Phase 2: Cloudflare Worker + full pipeline. |
| **P0** | **Update mirror.md** | DONE (2026-03-12) | Fresh entry added. Previous gap: 12 days. |
| **P0** | **Run cross-anomaly compressor** on new clusters | DONE (2026-03-13) | 2 proverb candidates generated. Results in PROVERB_APPROVAL_QUEUE.md. |
| **P0** | **Submit arXiv paper** | READY TO SUBMIT | Paper complete. Recommend cs.AI (primary) + cs.CY (secondary). Mohamed has not started submission — endorsement not yet requested. |

---

## ACTIVE EXECUTION — PLAN-001

| Layer | Component | Status | Next Step |
|-------|-----------|--------|-----------|
| **L1 Scientific** | EXP-001 design | COMPLETE | 188 runs remaining across 10 systems × 10 questions × 2 conditions. Q3 pilot done. Science inventory filed. |
| **L2 Narrative** | kalam.ch site | LIVE (Phase 1) | Threshold input added. Deploy update to Cloudflare. |
| **L3 Operational** | Ninth Operator | IMPLEMENTED | Client-side ceremony live. Backend integration in Phase 2. |

---

## MEDIUM-TERM (Next Few Sessions)

| Pri | Task | Status | Notes |
|-----|------|--------|-------|
| **P1** | **kalam.ch Phase 2** — hybrid mode + Cloudflare Worker | Not started | Switch Astro to hybrid output, add `@astrojs/cloudflare`, wire API to Python Ninth Operator. |
| **P1** | **Public repo `kalam-framework`** | Exists at `Sternmannli/kalam-framework` | Assess each PR for public impact. Clean software engineering language only. |
| **P1** | **Populate seed readiness calendar** | DONE (2026-03-13) | All 12 seeds planted and integrated. Calendar fully populated. |
| **P1** | **Process new anomalies from donors** | Not started | Check for [RETURN] signals. |
| **P1** | **Update red feathers ledger** | Ongoing | Current count: 7. |

---

## RECENTLY COMPLETED (Since 2026-02-28)

- 2026-03-13: **ALL 12 SEEDS PLANTED AND INTEGRATED** — Seeds #1-#8 code written, tested (64 new tests), and wired into Organism
- 2026-03-13: **test_field.py bug fixed** — Duplicate voice ID causing false failure. Full suite now 683/683 (zero failures)
- 2026-03-13: Seed #1 Distributed Stewardship — 5 governance roles, delegation/rotation/concentration detection
- 2026-03-13: Seed #2 Immutable Witness Network — SHA-256 hash-chain, auto-records exchanges
- 2026-03-13: Seed #3 Deliberative Democracy — Weakest-Voice-First proposals + blocks
- 2026-03-13: Seed #4 Constitutional Evolution — Amendment lifecycle with tier-based cooling
- 2026-03-13: Seed #5 Restorative Justice — Harm→acknowledge→repair (never punish, only restore)
- 2026-03-13: Seed #6 System Self-Awareness — Capability/limitation registry + calibration
- 2026-03-13: Seed #7 Personalized Parables — Context-adaptive proverb delivery
- 2026-03-13: Seed #8 Institutional Dignity Score — IDS with variance penalty + floor weight (A-F grades)
- 2026-03-13: Cross-anomaly compressor run — 2 proverb candidates generated (agency + legibility clusters)
- 2026-03-13: Seed readiness calendar created (MANIFEST/seed_calendar.md)
- 2026-03-13: Compressor upgraded to TF-IDF (offline, no model download needed) + domain-aware templates
- 2026-03-13: ACTIVE_PLANS.md and PROJECT_TRACKER.md updated
- 2026-03-12: Threshold input added to kalam.ch (Ninth Operator ceremony, client-side)
- 2026-03-12: EXP-001 analysis pipeline created (`analyze.py`)
- 2026-03-12: Mirror entry after 12-day gap
- 2026-03-12: All 9 covenants ratified under Pre-Launch Exception
- 2026-03-12: 47 Treasures fully indexed in R7M/TREASURES/TREASURES_INDEX.md
- 2026-03-12: Witness Scale, Decay Function, Dignity-Latency ratified
- 2026-03-11: 7 External Voice responses collected (EV-001 through EV-007)
- 2026-03-10: Duplicate proverb IDs resolved, COV#008/COV#015 registered
- 2026-03-10: Three-state lifecycle defined (COMMITTED/PROVISIONAL/RATIFIED)

---

## LONG-TERM VISIONS / FUTURE SEEDS

All 12 future seeds planted, implemented, tested, and integrated into the Organism (2026-03-13). Full test suite: **750/750**.

---

## SCIENCE INVENTORY

Full scientific registry filed at `MANIFEST/SCIENCE_INVENTORY.md` (2026-03-13). Contains:
- 4 experiments (1 active, 3 designed)
- 17 empirical observations (C3–C5)
- 11 equations/formulas
- 16 scientific tools (Python)
- 9 identified gaps
- 10 red flags
- 1 complete paper (ready to submit)
- 3 external validations

---

## DEADLINES & CALENDAR

| Date (2026) | Item | Status |
|-------------|------|--------|
| **March 4** | Seeds added Feb 26 ready (7-day) | PASSED — review needed |
| **March 11** | Humour seeds ready (14-day) | PASSED — review needed |
| **March 26** | 30-day covenant amendments ready | Upcoming |
| **April 26** | 90-day constitutional changes ready | Monitor |

---

## MIRROR RITUAL

- Last mirror entry: **2026-03-12** (V-002)
- Previous entry: 2026-02-28

---

## ARXIV PAPER STATUS

- File: `PAPERS/Kalaxi_arXiv_GO4_Source.tex`
- Status: **PAPER COMPLETE — READY TO SUBMIT**
- Recommended categories: **cs.AI** (primary), **cs.CY** (secondary)
- Original target cs.OH dropped — cs.AI is better fit and may not require endorsement
- Mohamed has NOT started submission process yet
- Next: Go to arxiv.org → New Submission → Upload .tex → Select cs.AI

---

## PUBLIC REPO

- Repository: `Sternmannli/kalam-framework`
- Rule: Every PR assessed for public impact. Pure software engineering language. Zero internal vocabulary leaked.

---

## HOW TO USE THIS TRACKER

- **Start of session:** Review what's next.
- **End of session:** Update status, add notes, change "Last updated".
- **Commit** after each session.
