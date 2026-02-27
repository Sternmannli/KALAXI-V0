# 📋 KALAXI PROJECT TRACKER

**Last updated:** 2026-02-28

---

## 🟢 IMMEDIATE (Next Actions)

| Pri | Task | Status | Notes / Command |
|-----|------|--------|-----------------|
| **P0** | **Update master context** with today's intentions | ☐ Not started | `cd ~/Desktop/Kalaxi/CONTEXT && python3 update_context.py` |
| **P0** | **Append anomaly harvest** to `THRESHOLD.md` | ☐ Not started | `cat ANOMALY_HARVEST/THRESHOLD_ADDITIONS.md >> THRESHOLD.md` |
| **P0** | **Commit and push** after each change | ☐ Not started | `git add ... && git commit -m "..." && git push` |
| **P0** | **Run cross‑anomaly compressor** on new clusters | ☐ Not started | `python3 WEAVER/proverb_compressor.py` |
| **P0** | **Update mirror.md** before any ratification session | ☐ Not started | Required before `tend.py --review`. Last entry: 2026-02-26. |

---

## 🟡 MEDIUM‑TERM (Next Few Sessions)

| Pri | Task | Status | Notes |
|-----|------|--------|-------|
| **P1** | **Create new public GitHub repo** (sanitized version) | ☐ Not started | Name idea: `Kalaxi-Concept` |
| **P1** | **Populate seed readiness calendar** | ☐ Not started | Create `MANIFEST/seed_calendar.md` |
| **P1** | **Review future seeds (12) and make decisions** | ☐ Not started | See `FUTURE/` folder |
| **P1** | **Complete arXiv submission** | ☐ Not started | Waiting for endorsement |
| **P1** | **Update red feathers ledger** after each act of witnessing | ☐ Ongoing | Current: 6 entries |
| **P1** | **Process any new anomalies from donors** | ☐ Not started | Check for [RETURN] signals |
| **P1** | **Implement [RETURN] signal mechanism** (Future Seed 03) | ☐ Not started | See `FUTURE/seed_03_return_signal.md` |
| **P1** | **Formalize steward council** (Future Seed 02) | ☐ Not started | See `FUTURE/seed_02_steward_council.md` |

---

## 🔮 LONG‑TERM VISIONS / FUTURE SEEDS (Require Your Approval)

| Pri | Task | Status | Decision Needed |
|-----|------|--------|-----------------|
| **P2** | **Dignity Predicate v2.0 – Adoption** | ☐ Not started | Adopt as proposed? Adopt with modifications? Postpone? |
| **P2** | **Restoration Registry – Governance & Implementation** | ☐ Not started | Accept the three‑part ownership model? Refine further? Hold? |
| **P2** | **Origin Knot – Private Reflection File** | ☐ Not started | Add `CANON/origin_knot.md` now? Later? Never? |
| **P2** | **Penguin Pulse Visualization** (Future Seed 12) | ☐ Not started | See `FUTURE/seed_12_penguin_pulse.md` |
| **P2** | **Second Convergence** (Future Seed 01) | ☐ Not started | Awaiting donor recognition |
| **P2** | Other Future Seeds (04–11) | ☐ Not started | See `FUTURE/` folder |

---

## 🗓️ DEADLINES & CALENDAR

| Date (2026) | Item | Action Required |
|-------------|------|-----------------|
| **March 1** | Unknown deadline (Mohamed mentioned) | Investigate: What is due? Prepare accordingly. |
| **March 4** | Seeds added Feb 26 become ready (7‑day) | Review seeds in THRESHOLD.md |
| **March 11** | Humour seeds become ready (14‑day) | Review in THRESHOLD.md |
| **March 26** | 30‑day covenant amendments become ready | Check for pending changes |
| **April 26** | 90‑day constitutional changes become ready | None yet, but monitor |
| **Ongoing** | Seeds from anomaly harvest become ready | Staggered readiness starting 7 days from addition |

---

## 📅 SEED READINESS CALENDAR (To Be Populated)

After appending the harvest, create `MANIFEST/seed_calendar.md`:

| Seed ID | Date Added | Delay (days) | Ready Date | Status | Action |
|---------|------------|--------------|------------|--------|--------|
| ANOM#PHYSICS-FERMI-001 | 2026-02-28 | 7 | 2026-03-07 | Pending | – |

---

## 🧩 FUTURE SEEDS – DECISION STATUS (from `FUTURE/` folder)

| Seed | Title | Decisions Made? | Notes |
|------|-------|-----------------|-------|
| 01 | Second Convergence | ☐ No | Awaiting donor recognition |
| 02 | Steward Council | ☐ No | Formalize roles? |
| 03 | [RETURN] Signal | ☐ No | Mechanism for donor response |
| 04–11 | (Other seeds) | ☐ No | See `FUTURE/` for details |
| 12 | Penguin Pulse | ☐ No | Visualisation |

---

## 🪞 MIRROR RITUAL REMINDER

- Last mirror entry: **2026-02-26 01:15**
- Next tending session requires a new entry in `STEWARD/mirror.md` (timestamp within 24h).

---

## 🔴 RED FEATHER LEDGER

- Current count: **6** (see `MANIFEST/red_feathers.md`)
- After each ratification, compost, convergence, or significant act: add one line.

---

## 📄 ARXIV PAPER STATUS

- File: `PAPERS/Kalaxi_arXiv_GO4_Source.tex`
- Endorsement requested for **cs.OH**.
- Status: **Pending**.
- Next: Check every few days.

---

## 🌐 PUBLIC REPO PREPARATION

- **Goal:** New repo `Kalaxi-Concept` with sanitized content.
- **Include:** `FOUNDATIONS/` (conceptual), `CANON/FIRST-SIGHT.md`, `INVITATION.md`, `ANOMALY_HARVEST/` (titles only), `FUTURE/` (as ideas), website files, README.
- **Exclude:** `WEAVER/`, `STEWARD/`, `MANIFEST/receipts/`, `THRESHOLD.md`, `ABSURDITY_QUEUE.md`, `CONVERGENCE/`.

---

## 📌 HOW TO USE THIS TRACKER

- **Start of session:** Open this file, review what's next.
- **End of session:** Update checkboxes, add notes, change "Last updated".
- **Commit changes** to GitHub after each session.
- **Sync with master context:** After updating tracker, run `update_context.py` to reflect top priorities.
