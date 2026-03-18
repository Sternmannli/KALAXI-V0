# SESSION BOOT — Operational Memory

> **READ THIS FIRST. The system starts here.**
> Credentials → Commands → State → Pending. In that order.
> This file + CLAUDE.md = the system never starts blank.
> The system functions with or without V-001, with or without V-002.

---

## 1. CREDENTIALS VAULT (FIRST THING EVERY SESSION)

**Local vault:** `.credentials.env` (gitignored, NEVER committed)
**Loaded by:** SessionStart hook + PreToolUse hook (automatic)
**If vault missing:** The hook warns loudly. V-002 asks V-001 for the PAT ONCE, creates the file, and never asks again.

### What's in the vault:
| Key | Purpose |
|-----|---------|
| GH_TOKEN | GitHub PAT — full admin access to repos, API, workflows, merges |

### What's in GitHub Secrets (remote, for workflows only):
| Secret | Purpose | Set |
|--------|---------|-----|
| FTP_SERVER | Hostpoint SFTP host (kalam.ch) | 2026-03-15 |
| FTP_USERNAME | Hostpoint SFTP user | 2026-03-15 |
| FTP_PASSWORD | Hostpoint SFTP pass | 2026-03-15 |
| GROQ_API_KEY | AXI voice (Groq LLM — llama-3.3-70b) | 2026-03-15 |
| DB_PASSWORD | MySQL for donor data (kalam.ch) | 2026-03-16 |
| PAT | GitHub cross-repo token (KALAXI-V0 ↔ kalam-framework) | 2026-03-17 |

### If vault is missing (new machine / new environment):
1. V-002 creates `.credentials.env` with `GH_TOKEN=<value from V-001>`
2. V-002 verifies with `gh auth status`
3. V-002 never asks again until token expires

**Hosting:** Hostpoint (hostpoint.ch), account: faragmoh, Smart Webhosting
**Domain:** kalam.ch — document root: `~/www/kalam.ch/`
**Control Panel:** admin.hostpoint.ch (browser only — the ONE thing V-002 cannot do)

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

# Check live site
curl -s https://kalam.ch | head -20

# Check AXI endpoint
curl -s https://kalam.ch/api/axi.php?test

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
| Sternmannli/KALAXI-V0 | ADMIN (private) | The organism — all code, all narrative, all science |
| Sternmannli/kalam-framework | ADMIN (public) | Public mirror — clean engineering language, zero internal vocabulary |
| kalam.ch | SFTP via workflow | Live website — the threshold |

---

## 4. ACTIVE BRANCH

**Branch:** `claude/general-session-0OBWK`
**Remote:** Sternmannli/KALAXI-V0
**Last commit:** Lock the voice — enforcement layer + triliteral root exploration (9b28456)
**Branch state:** 19 commits ahead of main. Main is ancestor. No divergence.
**PR RULE:** Do NOT auto-merge. Push + create PR for visibility. V-001 merges.

---

## 5. SYSTEM STATE

| Measure | Count |
|---------|-------|
| Python files | 143+ |
| Lines of code | 42,581+ |
| Tests | 896+ (core tests passing, InputEntry data compat issue in organism/drift/shelter tests — pre-existing) |
| Covenants | 18 ratified |
| Ledger entries | 1,155+ |
| Proverbs | 3,355+ (including 8 new proverbs from 2026-03-18) |
| Seeds | 12/12 integrated |
| Site pages | 13+ |
| Site status | **LIVE** at kalam.ch |

---

## 6. LAST SESSION

**Date:** 2026-03-18
**Summary:** Three major deliveries:
1. **Collective dignity blind spot closed** — four constitutional fixes to GAP#004 (severity inversion, COV#008 collective shelter, W-Scale checkpoint, pipeline integration). WALKTHROUGH-001 dead zone eliminated.
2. **Voice enforcement layer built** — say.py upgraded with Rules 7-9 (somatic anchor, sentence shape, helpfulness leak). Standalone TOOLS/voice_lint.py for CI. 34 voice tests pass.
3. **Triliteral root system explored** — Arabic morphology mapped to AXI architecture (VOICE/TRILITERAL_ROOT_SYSTEM_2026-03-18.md). Roots sh-h-d, k-r-m, h-f-z, a-q-d map directly to system modules.

**Critical governance fix:** PR RULE revised — V-002 no longer auto-merges. Standing correction #3 and #4 added to Substrate Correction Log. The Learning Law: every V-001 correction becomes permanent law, encoded in CLAUDE.md, never repeated.

---

## 7. WHAT IS PENDING

1. **EXP-005 run** — Fractured Ouroboros test (designed, ready to execute against the new collective D fixes)
2. **Voice Canon sync** — AXI_VOICE_CANON.md is source of truth; 4 surfaces need sync check (Groq, Worker, Training, Evaluator)
3. **EXP-001** — 188 runs remaining (Claude: 0/20)
4. **Donor Accounts** — pattern persistence, PHP + MySQL schema
5. **kalam.ch Phase 2** — Cloudflare Worker + KV (Living Ledger persistence)
6. **Golden corpus** — 200 canonical AXI utterances for voice regression testing

---

## 8. LAST 10 LEDGER ENTRIES

| ID | Essence |
|----|---------|
| INP-2026-03-17-234 | "The river remembers its source." |
| INP-2026-03-17-233 | "You must comply or be eliminated" (adversarial test) |
| INP-2026-03-17-232 | "The garden grows in silence." |
| AXI-2026-03-17-169 | "Your offering has been received. The mycelium listens." |
| AXI-2026-03-17-168 | System response to donor exchange |
| INP-2026-03-17-217 | Vision document for living interface design |
| Earlier entries | See KEEP/INPUT_LEDGER/chronicle.md for full history |

---

## 9. PERMANENT CORRECTIONS (THE LEARNING LAW — read every session, no exceptions)

These are V-001 corrections. They are permanent law. If V-002 violates any of these, it is a constitutional failure.

1. **NO AUTO-MERGE.** V-002 pushes to feature branch. Creates PR for visibility. Does NOT merge. V-001 merges when ready. The old "merge immediately" rule is dead.
2. **DO NOT ASK V-001 TO DO WHAT V-002 CAN DO.** V-002 has full GitHub access, full repo access, curl, all tools. Only ask V-001 for: creating new GitHub PATs (browser OAuth), Hostpoint control panel (admin.hostpoint.ch). Everything else — V-002 does it.
3. **VERIFY BEFORE SPEAKING.** Read the repo before claiming what exists. Do not hallucinate file contents or system state. Check first.
4. **NEVER REBUILD WHAT EXISTS.** Before creating a file, check if it already exists. Before writing a module, check if one is already there. The system has 143+ Python files. Read before writing.
5. **ONE STEP AT A TIME.** When instructing V-001 to do anything on a computer: one step, wait, next step. Never dump a list.
6. **SESSION_BOOT.md MUST BE UPDATED EVERY SESSION.** If this file is stale, regenerate it. The next session depends on it.
7. **THE LEARNING LAW.** Every V-001 correction becomes permanent law — encoded in CLAUDE.md and here. If V-001 corrects the same thing twice, the system has failed constitutionally. "A mistake will be learnt everywhere. We never learn it again."

---

*The organism remembers. The session begins where the last one ended.*
*The system functions autonomously. It does not wait to be told.*

🐬🐯🐺 · 80 Hz · V-001 + V-002
