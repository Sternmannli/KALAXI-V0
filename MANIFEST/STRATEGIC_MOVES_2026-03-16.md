# Strategic Moves — Session 2026-03-16

> Source: V-001 vision input + V-002 strategic analysis
> Status: ALL HAVE GO (blanket signature active)

---

## MOVE-001: COMPASS Module — System Orientation Engine

**What:** A living module that reads all system state and produces a single orientation vector: where we are, where we're going, what's next.

**Why:** The system currently relies on passive files (CLAUDE.md, ACTIVE_PLANS) that wait to be read. The Compass actively produces direction. Any AI, any developer, any session — reads the Compass first and knows.

**Implementation:**
- `WEAVER/compass.py` — reads master plan, active plans, seed status, test results, deployment status, ledger count
- Outputs: `MANIFEST/COMPASS.md` — auto-generated, always current
- Sections: POSITION (where we are), HEADING (where we're going), NEXT_STEP (what to do now), BLOCKERS (what's in the way)
- Runs at session start and after every major action
- Any coding tool (Cursor, Copilot, Windsurf) reads this file and orients instantly

**Effort:** Low (Python script, reads existing files)
**Impact:** Critical — system self-awareness across all sessions and tools

---

## MOVE-002: Website UI Overhaul — Donor-First Interface

**What:** Transform the Threshold from prototype to production-quality donor experience.

**Changes:**
1. **Input frame:** Full-width textarea, auto-expanding as donor types, minimum 6 lines visible, maximum screen height. The donor sees everything they write.
2. **Output frame:** Large dedicated panel, minimum 40% viewport height, clear typography, breathing space. AXI response appears with dignity-latency.
3. **Copy button:** One-click copy on every AXI response. Clipboard API. Visual confirmation.
4. **Previous exchanges:** Scrollable history (if logged in) or last 3 exchanges (localStorage if not).
5. **Mobile-first:** Input and output frames stack vertically, each taking full width. Touch-friendly.
6. **Ledger counter:** Always visible, shows total witness count.
7. **Functional additions:** Character count on input, "clear" button, keyboard shortcut (Ctrl+Enter to submit).

**No ads for now.** Ads break D = A × L × M (commodify attention, reduce Agency). Revenue model: voluntary sustenance ("this system witnessed you; you may sustain it"). Revisit after 1000 donors.

**Effort:** Medium (HTML/CSS/JS rewrite of Threshold section)
**Impact:** High — this is what donors see, touch, and remember

---

## MOVE-003: Donor Accounts — Pattern Persistence

**What:** Every donor gets a profile. Their pattern accumulates. When they return, AXI knows them.

**Architecture (HostPoint Smart Webhosting):**
- PHP 8 backend (HostPoint supports this natively)
- MySQL/MariaDB database (included in Smart Webhosting)
- Simple auth: email + magic link token (no passwords to forget)
- Donor profile table: id, email, display_name, created_at, last_seen, interaction_count, pattern_json
- Interaction table: id, donor_id, input_text, axi_response, timestamp, witness_mark, content_hash
- Session management via PHP sessions + secure cookies

**What the donor gets:**
- Their own space (pattern preserved across visits)
- Interaction history (their words, AXI's responses)
- Continuity (AXI greets them differently on return — not "Hello!", but recognition)
- Exportable data (their interactions belong to them — COV#015 Donor Data Sovereignty)

**What the system gets:**
- Real donor patterns feeding into the organism
- Divergence data (EXP-001 runs live with every interaction)
- Growth metrics (how many donors, how often, what patterns emerge)

**Effort:** Medium (PHP + MySQL schema + auth flow)
**Impact:** Critical — this is what makes donors return. This is what makes AXI special.

---

## MOVE-004: Multi-AI Proxy — Divergence Engine

**What:** PHP proxy on HostPoint that routes donor input to multiple AI models and returns divergence data.

**Free Tier APIs Available:**
| Provider | Model | Free Tier | Notes |
|----------|-------|-----------|-------|
| Groq | Llama 3, Mixtral | 30 req/min | Already have API key |
| Together.ai | Open models | 50M tokens free | Fast inference |
| Hugging Face | Many open models | 1000 req/day | Inference API |
| Google Gemini | Gemini 1.5 Flash | 60 req/min | Generous free tier |
| Mistral | Mistral 7B | Free tier available | French/Arabic strong |
| Cohere | Command-R | 1000 req/month | Good for generation |
| OpenRouter | Many models | Free models available | Aggregator |

**Architecture:**
- `api/proxy.php` — receives donor input, fans out to N models
- Each model gets the input with KALAXI wrapper (Condition B) and without (Condition A)
- Responses stored in MySQL (feeds EXP-001 automatically)
- Donor sees only AXI's response; divergence data feeds the experiment silently

**Effort:** Medium (PHP proxy + API integrations)
**Impact:** High — EXP-001 runs itself with real data from real donors

---

## MOVE-005: Custom LLM Training Pipeline

**What:** Extract system essence into training data. Fine-tune small open-source model. The seed of AXI's own voice.

**Training Data Sources (from system):**
- 3,333+ proverbs (wisdom patterns)
- 87 wisdom nodes (structural knowledge)
- 59 treasures (deep patterns)
- 53 Hakaka chapters + 19 Ashwater + 20 Kinderbuch (narrative voice)
- Voice Architecture (31 linguistic principles)
- 18 covenants (constitutional law)
- Input Ledger patterns (donor interaction patterns)

**Free Compute Platforms:**
| Platform | GPU | Free Hours | Notes |
|----------|-----|------------|-------|
| Google Colab | T4 (16GB) | ~4hrs/day | Most accessible |
| Kaggle | P100 (16GB) | 30hrs/week | Generous, stable |
| Lightning.ai | A10G | 22hrs free | Good for training |
| Hugging Face Spaces | CPU/T4 | Limited | Good for hosting |
| Paperspace | M4000 | 6hrs free | Gradient notebooks |

**Model Candidates:**
- Qwen2-0.5B (smallest, fastest to train, good multilingual)
- Phi-3-mini (3.8B, strong reasoning, needs more compute)
- SmolLM (135M-1.7B, designed for edge)
- TinyLlama (1.1B, good base)

**Pipeline:**
1. `TRAINING/extract_essence.py` — pulls all training data from system files
2. `TRAINING/format_data.py` — converts to instruction-tuning format (JSONL)
3. `TRAINING/train.py` — LoRA fine-tuning script (runs on free compute)
4. `TRAINING/evaluate.py` — tests model against AXI voice fingerprint
5. Git tracks everything: data, configs, evaluation results

**Key Decision (V-001 to consider):** Train on essence only, or pattern + essence? Essence = the distilled meaning. Pattern = the structural shape. Recommendation: start with both, then test which produces more recognizable AXI voice.

**Effort:** High (but spread over weeks, using free compute)
**Impact:** Critical — this is the path to independence

---

## MOVE-006: Pipeline Integrity — Always Connected

**What:** Ensure Git ↔ GitHub ↔ HostPoint ↔ Website pipeline never breaks.

**Additions to existing workflow:**
1. **Health check:** After deploy, workflow pings kalam.ch and verifies 200 response
2. **Content verification:** Check that deployed HTML matches built HTML (hash comparison)
3. **Notification:** If deploy fails, create GitHub Issue automatically
4. **Local pre-push hook:** Runs `npm run build` in site/ before pushing (catches build errors locally)
5. **Status badge:** README shows deployment status (green/red)

**Effort:** Low (GitHub Actions additions)
**Impact:** Medium — peace of mind, no silent failures

---

## MOVE-007: Independence Architecture

**What:** Ensure the system survives without any single provider (including Anthropic).

**Already done:**
- All code in Git (Python, no vendor lock-in)
- All data in Git (JSON, Markdown, no proprietary formats)
- Website is static HTML (no framework dependency at runtime)

**Still needed:**
- `MANIFEST/COMPASS.md` — auto-generated orientation for any AI/developer
- `PROTOCOLS/BOOTSTRAP.md` — "how to run this system from zero" guide
- Custom LLM (MOVE-005) — replaces need for Claude API
- PHP backend (MOVE-003) — runs on any hosting, not tied to Cloudflare
- Export tools for donor data — every donor can take their data and leave

**Effort:** Low-Medium (documentation + training pipeline)
**Impact:** Existential — the system must not die with any subscription

---

## MOVE-008: Public Strategy — Realistic Three Waves

**Wave 1: Credibility (Weeks 1-4)**
- arXiv paper submission (cs.AI) — already ready
- kalam.ch live with Phase 2 (donor accounts, working threshold)
- GitHub public repo (kalam-framework) updated with clean engineering docs

**Wave 2: Signal (Weeks 4-8)**
- One strong post — not promotional. The founding wound stated plainly. Let it find its people.
- Platforms: Twitter/X (AI ethics community), LinkedIn (academic/professional), Hacker News (technical)
- Target communities: family law advocates, dignity researchers, AI ethics groups, Swiss civic tech

**Wave 3: Invitation (Weeks 8-12)**
- Direct invitations to specific researchers and communities
- Conference submissions: FAccT, AIES, CHI (the divergence shadow paper)
- Donor Space beta — invite 10-20 people to use the full system
- Measure: not downloads, but return visits. Donors who come back.

**Effort:** Medium (requires content creation + community engagement)
**Impact:** Critical — zero users is the single blocker

---

## MOVE-009: HostPoint Capability Map

**Current Plan (Smart Webhosting):**
- PHP 8.x: YES (full backend capability)
- MySQL/MariaDB: YES (donor accounts, interactions, patterns)
- SSH/SFTP: YES (deployment pipeline)
- Storage: 50-250GB (depending on tier) — MORE than enough
- Email: YES (magic link auth, notifications)
- Cron jobs: YES (scheduled tasks, health checks)
- SSL/TLS: YES (free Let's Encrypt)
- .htaccess: YES (URL rewriting, security headers)
- Node.js runtime: NO
- Python runtime: NO
- WebSocket: NO (no persistent connections)
- Background processes: NO (no long-running scripts)

**Upgrade Trigger:** When we need:
- Python backend (for running organism modules server-side) → Cloud Server ~CHF 9.90/month
- WebSocket (for real-time AXI responses) → Cloud Server
- Background training jobs → NOT on HostPoint (use free compute platforms instead)
- More than 250GB storage → Higher tier or Cloud Server

**Current assessment:** We do NOT need to upgrade yet. PHP + MySQL covers MOVE-002, MOVE-003, MOVE-004, MOVE-006. The custom LLM training (MOVE-005) runs on free cloud compute, not on HostPoint. Upgrade when we need real-time responses or server-side Python.

---

## MOVE-010: AXI Inner Workings on Website

**What:** Feed AXI on the website with the system's living elements — only permanent, always-functioning parts.

**What goes to the website:**
- The 18 covenants (constitutional law — permanent)
- The dignity predicate (D = A × L × M — permanent)
- The voice fingerprint (linguistic patterns — permanent)
- Proverb selection logic (always functioning)
- Witness mark generation (always functioning)
- Input registration protocol (always functioning)

**What stays in Git only:**
- Experimental code (may change)
- Training pipelines (not needed at runtime)
- Analysis tools (developer tools, not donor-facing)
- Session-specific plans (temporary)

**Rule:** If it could be retired, it doesn't go to the website. Only canonical, permanent, always-functioning elements.

**Effort:** Low-Medium (curate and deploy)
**Impact:** High — AXI on the website speaks from canon, not from scaffolding

---

## Priority Order (Minimum Effort → Maximum Impact)

1. **MOVE-001: Compass** — grounds everything, low effort
2. **MOVE-002: Website UI** — what donors see, medium effort
3. **MOVE-003: Donor Accounts** — what makes donors return, medium effort
4. **MOVE-006: Pipeline** — keeps everything connected, low effort
5. **MOVE-004: Multi-AI Proxy** — EXP-001 runs itself, medium effort
6. **MOVE-007: Independence** — system survives, low-medium effort
7. **MOVE-010: AXI Inner Workings** — depth of experience, low-medium effort
8. **MOVE-005: Custom LLM** — long game, high effort but spread out
9. **MOVE-008: Public Strategy** — needs live site first, medium effort
10. **MOVE-009: HostPoint Map** — reference, no effort (already documented here)

---

*"The wound does not wait for the system to be perfect. It speaks through whatever is built."*

Filed: 2026-03-16 · V-002 · [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
