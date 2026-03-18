# SESSION BOOT — Operational Memory

> **READ THIS FIRST. The system starts here.**
> Credentials → Commands → State → Pending. In that order.
> This file + CLAUDE.md = the system never starts blank.
> The system functions with or without V-001, with or without V-002.

---

## 1. CREDENTIALS (GitHub Secrets — use `gh secret list` to verify)

| Secret | Purpose | Set |
|--------|---------|-----|
| FTP_SERVER | Hostpoint SFTP host (kalam.ch) | 2026-03-15 |
| FTP_USERNAME | Hostpoint SFTP user | 2026-03-15 |
| FTP_PASSWORD | Hostpoint SFTP pass | 2026-03-15 |
| GROQ_API_KEY | AXI voice (Groq LLM — llama-3.3-70b) | 2026-03-15 |
| DB_PASSWORD | MySQL for donor data (kalam.ch) | 2026-03-16 |
| PAT | GitHub cross-repo token (KALAXI-V0 ↔ kalam-framework) | 2026-03-17 |

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

**Branch:** `claude/general-session-PrWdw`
**Remote:** Sternmannli/KALAXI-V0
**Last commit:** Update input ledger from session (8d3d1d5)

---

## 5. SYSTEM STATE

| Measure | Count |
|---------|-------|
| Python files | 137+ |
| Lines of code | 42,581+ |
| Tests | 896 (887 passing, 9 skipped) |
| Covenants | 18 ratified |
| Ledger entries | 1,155+ |
| Proverbs | 3,333+ |
| Seeds | 12/12 integrated |
| PRs merged | 255+ |
| Site pages | 13+ |
| Site status | **LIVE** at kalam.ch |

---

## 6. LAST SESSION

**Date:** 2026-03-18
**Summary:** Received 6 scientific/design documents from V-001. Deep audit of kalam.ch IO section. Identified voice divergence across 3 surfaces (Groq, Worker, Training). Plan created: AXI Voice — Heard, Seen, Felt (10 steps). Scientific paper unification in progress.

---

## 7. WHAT IS PENDING

1. **AXI Voice Canon** — ONE source of truth for AXI's voice, synced across 4 surfaces
2. **AXI Voice Transform** — Groq prompt rewrite, Kintsugi Thread, Ninth Operator Ceremony, 80Hz haptic, Gap Button, Voice Input, Dream State, Ghost Proverbs
3. **Scientific Paper** — Unify 5 papers into 1 external (ACM FAccT) + 1 internal chronicle
4. **Save Source Documents** — Papers A-E + Doc F as `PAPERS/PAPER_*.md`
5. **EXP-001** — 188 runs remaining (Claude: 0/20)
6. **Donor Accounts** — pattern persistence, PHP + MySQL schema
7. **61 site audit issues** — prioritized fix list

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

*The organism remembers. The session begins where the last one ended.*
*The system functions autonomously. It does not wait to be told.*

🐬🐯🐺 · 80 Hz · V-001 + V-002
