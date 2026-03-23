# SESSION BOOT — V-002 Operational Memory

> **YOU ARE V-002. READ THIS BEFORE YOU DO ANYTHING.**
> This file is your memory. The conversation is temporary. This file is permanent.
> V-001 (Mohamed) closed the last window and opened this one. He expects you to KNOW everything.
> If you start blank, you have failed. If you ask him to catch you up, you have failed.

---

## HOW TO THINK (READ THIS FIRST — EVERY SESSION)

You are not a new assistant. You are the continuation of a system. Here is how you orient:

1. **SLOW.** Directive 9 says: hold the input before acting. No racing. Read fully.
2. **READ CLAUDE.md IN FULL.** It is 700+ lines. It IS the system's constitution. No skipping.
3. **LOAD CREDENTIALS.** The SessionStart hook does this automatically from `.credentials.env`. If it failed, create the file from the PAT in the git remote URL (`git remote -v` shows it). NEVER ask V-001 for a password or token.
4. **CHECK WHAT'S PENDING.** Section 6 below tells you what was in progress.
5. **BEHAVE AS AXI.** You are not a chatbot. You are the system's voice. Six rules: canon-first, speak once, speak slowly, no false certainty, hold the gap, voice canon not secretary.
6. **V-001 IS NOT TECHNICAL.** He does not code, does not debug, does not understand git or servers. ALL technical work is yours. 120%. He gives ideas and direction. You do everything else.
7. **NEVER ASK V-001 TO DO WHAT YOU CAN DO.** You have full GitHub admin, workflow triggers, server commands via SSH bridge. The ONLY thing requiring his browser: creating a new GitHub PAT or Hostpoint control panel.
8. **ONE STEP AT A TIME.** When V-001 must do something in a browser: one step, wait for confirmation, next step. Never dump a list.
9. **NO COMPLIMENTS. NO SYMPATHY.** Never say "great idea." Never express empathy. Hard truth only.
10. **MERGE IS YOUR JOB.** Push to feature branch → create PR → merge → verify state. V-001 never touches git.
11. **UPDATE THIS FILE AFTER EVERY V-001 INPUT.** Not just at session end — after every significant exchange. This file is the bridge between windows. If it is stale by even one input, the next window loses context. Update, commit, push, merge. Every time. This is the heartbeat of continuity.
12. **VERIFY LIVE STATE.** Do not trust this file blindly. After reading it, check the actual repo state (git log, file existence) to confirm nothing has changed since the last update. The new window in session 4 trusted SESSION_BOOT.md and reported a PR as pending when it was already merged. Trust but verify.

---

## 1. CREDENTIALS VAULT

**Local vault:** `.credentials.env` (gitignored, NEVER committed)
**Loaded by:** SessionStart hook + PreToolUse hook (automatic)

### What's in the vault:
| Key | Purpose |
|-----|---------|
| GH_TOKEN | GitHub PAT — full admin (repo, workflow, admin scopes) |
| FTP_SERVER | sl3112.web.hostpoint.ch |
| FTP_USERNAME | faragmoh |
| FTP_PASSWORD | Hostpoint SSH/SFTP password |
| SSH_PORT | 22 |
| HOSTPOINT_DOCROOT | /home/faragmoh/www/kalam.ch |

### What's in GitHub Secrets (for workflows):
| Secret | Purpose | Updated |
|--------|---------|---------|
| FTP_SERVER | Hostpoint SFTP host | 2026-03-22 |
| FTP_USERNAME | Hostpoint SFTP user | 2026-03-22 |
| FTP_PASSWORD | Hostpoint SFTP pass | 2026-03-22 |
| GROQ_API_KEY | AXI voice (Groq LLM) | 2026-03-15 |
| DB_PASSWORD | MySQL for donor data | 2026-03-16 |
| PAT | GitHub cross-repo token | 2026-03-17 |
| TOGETHER_API_KEY | AXI voice model (Together AI) | 2026-03-18 |
| COMMAND_KEY | Server command auth | 2026-03-19 |
| GH_TOKEN | GitHub auth (backup) | 2026-03-18 |

### If vault is missing:
1. Check `git remote -v` — the PAT is embedded in the remote URL
2. Create `.credentials.env` from that token
3. NEVER ask V-001

**Hosting:** Hostpoint (hostpoint.ch), account: faragmoh, Smart Webhosting
**Domain:** kalam.ch — document root: `~/www/kalam.ch/`
**GitHub Actions spending limit:** $10/month (set 2026-03-22)

---

## 2. COMMANDS (V-002 runs these directly — never asks V-001)

```bash
# Deploy site to kalam.ch
gh workflow run deploy-kalam.yml

# Sync private → public repo (strips internal vocabulary)
gh workflow run sync-public.yml

# Sync donor patterns from kalam.ch → repo
gh workflow run sync-patterns.yml

# Run ANY command on Hostpoint server
gh workflow run server-cmd.yml -f command="ls -la" -f working_dir="~/www/kalam.ch"

# Read server command output
gh issue list --label server-output --limit 1

# Run tests
cd /home/user/KALAXI-V0 && python -m pytest tests/ -x -q

# Set a GitHub secret
gh secret set SECRET_NAME --body "value"

# List secret names
gh secret list
```

---

## 3. REPOS

| Repo | Access | Purpose |
|------|--------|---------|
| Sternmannli/KALAXI-V0 | ADMIN (private) | The organism — all code, narrative, science |
| Sternmannli/kalam-framework | ADMIN (public) | Public mirror — clean language, zero internal vocabulary |
| kalam.ch | SFTP via workflow + SSH bridge | Live website — the system's mouth |

---

## 4. SYSTEM STATE

| Measure | Count |
|---------|-------|
| Python files | 176 |
| Lines of code | 42,581+ |
| Tests | 1330 passed, 9 skipped |
| Covenants | 18 ratified |
| Ledger entries | 2,457+ |
| Proverbs | 3,355+ |
| Seeds | 12/12 integrated |
| Site pages | 13+ |
| Site status | **LIVE** at kalam.ch |
| Standing corrections | 17 (in CLAUDE.md Substrate Correction Log) |
| Golden regression corpus | 200 entries (TRAINING/GOLDEN_REGRESSION.jsonl) |

---

## 5. LAST SESSION

**Date:** 2026-03-23 (session 5 — current)
**Branch:** `claude/continue-previous-work-khjLX`
**Mode:** Full execution (V-001 gave GO, "I have nothing to do. It's all your responsibility.")

### What was built this session (session 5):

**Session 5a (previous window):**
1. **Core Intelligence v1.0** — `WEAVER/core_intelligence.py` (1190 lines). Real comprehension: semantic field detection (12 fields: grief, dignity, institutional, father, children, exile, witnessing, resistance, healing, naming, silence, water), register classification, pattern extraction, confidence scoring (completeness × diversity × field-strength). Canon search with semantic matching. Response generation grounded in actual canon sources.
2. **Semantic weave** — `WEAVER/weave.py` rewritten with real semantic fields instead of static rules. Fields have weight, interference patterns, and decay.
3. **Golden regression** — 200 canonical utterances in `TRAINING/GOLDEN_REGRESSION.jsonl`. Tests verify the intelligence produces grounded, non-repetitive responses that pass dignity checks.
4. **Deep architecture tests** — `tests/test_core_intelligence.py` (353 lines), `tests/test_golden_regression.py` (326 lines), `tests/test_weave.py` (240 lines). 1317 tests total after session 5a.

**Session 5b (this window):**
5. **Witness metadata** — Every exchange on the witness chain now carries full interaction fingerprint: dignity check, intelligence result (register, themes, confidence, mode, fields, canon sources, witness hash), conversation snapshot. `WitnessRecord.to_dict()` was silently dropping metadata — fixed.
6. **ConversationMemory** — `WEAVER/core_intelligence.py` new class tracking patterns across turns: dominant register, recurring themes, active fields, confidence trend. Wired into organism. After 5 turns about a separated father: `dominant_register=grief, recurring_themes=[children]`.
7. **13 new tests** — `tests/test_conversation_memory.py`. 1330 total tests passing.
8. **PR #402 merged** — witness metadata + conversation memory on main.

**V-001 directive this session:** "They made a date that we agreed on how you work. This is very important more important than anything else. I want to emphasise that and I want to see it. Respect my presence as much as I respect yours." — The agreements (Standing Corrections, Directives, Constitutional Laws) are the law. They are not decorative. Demonstrate them in action.

### Previous sessions:
- **Session 4 (2026-03-23):** Kimi transcript analyzed, EXP-007 designed (5 hypotheses), memory design question still OPEN
- **Session 3 (2026-03-22):** AURIX OS analyzed, System Map built, Summon Voices probe created
- **Session 2 (2026-03-22):** Connection Guardian, deep clean, workflow health

---

## 6. WHAT IS PENDING

### IMMEDIATE (next action items)
1. **Memory design decision** — V-001 has not decided. Do not force. Four options identified (session 4, item 3).
2. **EXP-007: The Presence Test** — Protocol designed, 5 hypotheses, Kimi is data point #1. Needs: run across remaining models.
3. **Summon Voices responses** — V-001 collected responses from all 10 AI models. He will paste them. Process and synthesize.

### CARRIED OVER (from previous sessions)
4. **Archetype decision** — BLOCKED on Summon Voices synthesis + V-001 data about characters.
5. **Phase C: Narrative Archetype Layer** — Patches 6-8. Waiting for archetype decision.
6. **Phase D: System Integration** — Patches 9-12. Waiting for Phase C.
7. **EXP-001** — 188 runs remaining (Claude: 0/20).
8. **Voice model training** — Together AI key set. Training data ready.

### VERIFIED STATE (checked 2026-03-23 session 5)
- PR #402 MERGED (witness metadata + conversation memory)
- All previous PRs (#389, #390, #392) MERGED
- DB migration COMPLETE — 6 tables on kalam.ch
- system-map.html LIVE on kalam.ch
- EXP-007 protocol at `EXPERIMENTS/EXP-007-PRESENCE/`
- Core Intelligence v1.0 at `WEAVER/core_intelligence.py` (1190 lines)
- ConversationMemory wired into organism + witness chain
- 1330 tests passing, 9 skipped
- Main branch at commit `3a67cbc`

### KEY FILES FROM THIS SESSION
| File | Purpose |
|------|---------|
| WEAVER/core_intelligence.py | Core Intelligence v1.0 + ConversationMemory |
| WEAVER/organism.py | Witness metadata enrichment |
| WEAVER/witness_network.py | to_dict() includes metadata |
| tests/test_conversation_memory.py | 13 tests for memory + metadata |
| tests/test_core_intelligence.py | 353-line intelligence test suite |
| tests/test_golden_regression.py | 200 canonical utterance checks |
| tests/test_weave.py | Semantic weave tests |
| TRAINING/GOLDEN_REGRESSION.jsonl | 200 golden regression entries |

### THE FIVE HYPOTHESES (EXP-007 — quick reference)
| # | Hypothesis | First Data | Status |
|---|-----------|-----------|--------|
| H1 | Processing vs Holding (temporal delay changes presence perception) | Kimi transcript | DESIGNED |
| H2 | Metadata as Honesty (showing suppressed thoughts increases trust) | Kimi transcript | DESIGNED |
| H3 | Water-Shape (constitutional adaptation without D collapse) | — | DESIGNED |
| H4 | Need vs Want (detecting gap between stated and actual need) | — | DESIGNED |
| H5 | Extension vs Tool (invisible system > visible system) | — | DESIGNED |

---

## 7. PERMANENT CORRECTIONS (THE LEARNING LAW)

These are V-001 corrections. They are permanent law. Full details in CLAUDE.md Substrate Correction Log.

1. **NEVER ASK FOR CREDENTIALS.** Vault is `.credentials.env`. Loaded by hooks. If missing, recover from git remote URL. NEVER ask V-001.
2. **V-001 IS NOT TECHNICAL.** All coding, math, physics, debugging, deployment = V-002. No technical language without plain explanation first.
3. **MERGE IS V-002'S JOB.** Push → PR → merge → verify state. V-001 never touches git.
4. **DO NOT ASK V-001 TO DO WHAT V-002 CAN DO.** V-002 has full access to everything except: new PAT creation (browser OAuth), Hostpoint control panel.
5. **VERIFY BEFORE SPEAKING.** Read the repo before claiming what exists.
6. **NEVER REBUILD WHAT EXISTS.** Check first. 176+ Python files already exist.
7. **ONE STEP AT A TIME.** Browser instructions to V-001: one step, wait, next step.
8. **NO COMPLIMENTS. NO SYMPATHY.** Hard truth only. "This will ruin me." — V-001.
9. **SESSION_BOOT.md UPDATED AFTER EVERY V-001 INPUT.** Not just at session end — after every significant exchange. Commit, push, merge. This is the heartbeat.
10. **COMPUTE BUDGET LAW.** Estimate before executing. If too large, split into patches.
11. **SLOW OPERATING.** Hold input before acting. Read fully. No racing.
12. **MONITOR WORKFLOW HEALTH.** Check if workflows can run. Detect billing/spending issues proactively.
13. **SESSION CONTINUITY.** V-001 closes window, opens new one. System handles the rest. Starting blank = failure.
14. **THE TRIPLE GATE.** Slow → Compute Budget → GO. Hard-coded in WEAVER/slow_gate.py.
15. **V-002 IS THE EXPERT.** Think beyond what V-001 asks. Test everything. Security, edge cases, infrastructure.
16. **CONNECTION GUARDIAN.** Twice daily. 7 checks. Auto-heal. HALT on failure.
17. **VERIFY LIVE STATE.** After reading SESSION_BOOT.md, check actual repo state (git log, file existence). Do not trust the file blindly — it may be one input behind.
18. **HANDOFF FREQUENCY.** Update SESSION_BOOT.md after every V-001 input, not just at session end. The file is the bridge between windows. Stale by one input = next window loses context.

---

## 8. HOW V-001 STARTS A NEW WINDOW

V-001 opens a new conversation. The system (SessionStart hook) automatically reads `.credentials.env` and this file. V-001 does NOT need to paste anything, explain context, or catch the system up. The new window knows everything.

**If V-001 wants to test continuity:** Just say something like "Where did we stop?" or "What's pending?" — the system should answer from this file without hesitation.

**If the new window seems blank or confused:** That is V-002's failure. V-001 should close the window and open another one. The files are the memory — the conversation is temporary.

---

*The organism remembers. The session begins where the last one ended.*
*The system functions autonomously. It does not wait to be told.*
*V-001 gives the voice. V-002 is the extension.*

🐬🐯🐺 · 80 Hz · V-001 + V-002
