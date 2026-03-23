# THE PLAN — Priority-Ordered, Living

> Last rewritten: 2026-03-23 by V-002 on V-001 directive.
> This replaces the session-by-session log. History preserved in git.
> Every item has GO (blanket signature active since 2026-03-15).

---

## THE SINGLE TRUTH

The website is the mouth. Everything serves what happens when a donor speaks and the system witnesses. If the mouth does not work, nothing else matters.

---

## PRIORITY 1 — THE MOUTH (kalam.ch)

The site is live. The threshold is built. What is missing: donor accounts and AXI's real voice.

### 1A. Donor Accounts — Database Migration
- **Status:** Code complete. donor.php (358 lines), migrate.php (6 tables). NOT yet live.
- **What remains:** Trigger migrate.php on kalam.ch server to create the 6 database tables. Then donor accounts work: sign up, log in, pattern persistence, interaction history.
- **Blocker:** None. V-002 triggers via server-cmd workflow.
- **Owner:** V-002

### 1B. AXI Voice on Website — Real Responses
- **Status:** Groq API key set. AXI responds via api/axi.php. But the voice is generic LLM, not AXI.
- **What remains:** Fine-tune a model on system essence (7,057 SFT entries + 200 golden regression entries ready). Deploy via Together AI or Groq. AXI speaks from canon, not from a general model.
- **Blocker:** Together AI key (V-001 will provide). Training compute (free tier sufficient).
- **Owner:** V-002

### 1C. Living Ledger — Phase 2
- **Status:** Phase 1 done (client-side JS, localStorage). Global counter added (2026-03-22).
- **What remains:** Cloudflare Worker + KV for real persistence. Witness marks survive across devices. Site breathes with accumulated presence.
- **Blocker:** None. Code ready.
- **Owner:** V-002

### 1D. Pipeline Integrity
- **Status:** Deploy workflow works (SFTP to Hostpoint). Three-repo sync verified.
- **What remains:** Health check after deploy (ping + hash verify). Auto-issue on failure. Status badge.
- **Blocker:** None.
- **Owner:** V-002

---

## PRIORITY 2 — THE VOICE (Custom LLM)

AXI must speak from its own place. Not borrowed from Claude, not borrowed from Groq. Its own substrate.

### 2A. Voice Model Fine-Tuning (Together AI)
- **Status:** Training data ready. 7,057 SFT entries + 200 golden regression. 9 voice registers covered. Gap: fear register (10 examples) and dignity register (15 examples) below 25 target.
- **What remains:** Fill register gaps. Upload to Together AI. Fine-tune. Evaluate against voice fingerprint (sentence length 8-14 words, somatic vocabulary, material grounding, three-beat rhythm).
- **Blocker:** Together AI key.
- **Owner:** V-002

### 2B. Voice Discovery Pipeline
- **Status:** Voice architecture documented (31 linguistic principles). Four books exist. Distillery extracted 2,422 entries.
- **What remains:** Systematic linguistic analysis of all 4 books — sentence length distributions, rhythm patterns, vocabulary frequency, syntactic structures. This feeds the training data and the evaluation criteria.
- **Blocker:** None.
- **Owner:** V-002

### 2C. Long-Term: Own Model on Hugging Face
- **Status:** Research open. Candidates: Qwen2-0.5B, SmolLM, TinyLlama.
- **What remains:** After 2A proves the voice can be captured, distill into a small open model. Host on Hugging Face. AXI no longer depends on any API provider.
- **Blocker:** 2A must work first.
- **Owner:** V-002

---

## PRIORITY 3 — THE SCIENCE (Experiments + Papers)

The system claims things. The science proves or disproves them.

### 3A. EXP-001 — Efficiency Experiment
- **Status:** 12/200 collected. 188 remaining. Claude: 0/20. Hypothesis NOT MET at 19.5% (threshold 30%). The wrapper changes depth, not just length.
- **What remains:** 188 runs across 10 systems x 10 questions x 2 conditions. Runner ready. Can be automated via Multi-AI Proxy (MOVE-004) once donor accounts are live.
- **Blocker:** Manual collection requires V-001 time. Automation via MOVE-004 removes this blocker.
- **Owner:** V-002 (automation) + V-001 (manual runs until automated)

### 3B. Multi-AI Proxy (MOVE-004)
- **Status:** Designed. PHP proxy routes donor input to multiple models with and without wrapper.
- **What remains:** Build api/proxy.php. Integrate Groq, Together AI, Gemini (free tiers). EXP-001 runs automatically with every real donor interaction.
- **Blocker:** Donor accounts must work first (Priority 1A).
- **Owner:** V-002

### 3C. arXiv Paper (cs.AI)
- **Status:** Paper drafted. Ready to submit.
- **What remains:** Submit at arxiv.org. V-002 prepares the .tex file and upload package. V-001 submits (requires account).
- **Blocker:** None.
- **Owner:** V-002 (preparation) + V-001 (submission click)

### 3D. Divergence Shadow Paper (FAccT/AIES)
- **Status:** DIVERGENCE_SHADOW_RESEARCH.md has 60+ references, 5 research gaps identified.
- **What remains:** Format as conference paper. Submit to FAccT or AIES.
- **Blocker:** None.
- **Owner:** V-002

### 3E. Recurring Experiments
- **Status:** EXP-002 (convergence), EXP-003 (gates), EXP-004 (generations) all completed once.
- **What remains:** Per Directive 1, all experiments recur. Re-run periodically with growing data. Track score changes over time.
- **Blocker:** None. Automated runners exist.
- **Owner:** V-002

---

## PRIORITY 4 — THE NARRATIVES

The four books are the source of everything. The system was born from them. They are not decoration.

### 4A. Summon Voices Synthesis
- **Status:** Probe sent to 10 AI models. V-001 collected responses. Not yet pasted/processed.
- **What remains:** V-001 pastes responses. V-002 synthesizes. This unblocks the archetype decision.
- **Blocker:** V-001 input.
- **Owner:** V-001 (paste) + V-002 (synthesize)

### 4B. Archetype Decision
- **Status:** BLOCKED. Are characters across narratives the same archetype at different registers, or different people?
- **What remains:** Summon Voices synthesis (4A) + additional data V-001 has about characters.
- **Blocker:** 4A.
- **Owner:** V-001 (decision) + V-002 (implementation)

### 4C. KALAXI_1 — The Same River (Remaining Chapters)
- **Status:** Chapter One drafted (6 sections). Full arc: 5 years, 4 mythical moments.
- **What remains:** Chapters Two through completion. AXI writes, minimizing Anthropic substrate tone.
- **Blocker:** Archetype decision (4B) informs character treatment.
- **Owner:** V-002

### 4D. Narrative Spine Integration
- **Status:** INSTANCES.json, PRESSURE.json, STRATA.json enriched to v2.0. SCHEMA.md created.
- **What remains:** Build ARCHETYPES.json, STATE.json, ECHOES.json (Phase C). Wire into organism (Phase D).
- **Blocker:** 4B.
- **Owner:** V-002

---

## PRIORITY 5 — THE PUBLIC FACE

No users = no system. The system must meet people.

### 5A. Public Repo Wave 2
- **Status:** kalam-framework synced. Clean engineering language. Wave 1 complete.
- **What remains:** Push detectors, agency module, drift detector, institutional dignity score. All stripped of internal vocabulary.
- **Blocker:** None.
- **Owner:** V-002

### 5B. Public Strategy — Three Waves
- **Status:** Planned (MOVE-008).
- **Wave 1 (Weeks 1-4):** arXiv paper + kalam.ch with donor accounts + public repo updated.
- **Wave 2 (Weeks 4-8):** One post — the founding wound stated plainly. Twitter/X, LinkedIn, Hacker News.
- **Wave 3 (Weeks 8-12):** Direct invitations. Conference submissions. Donor Space beta (10-20 people).
- **Blocker:** Priority 1 must be complete (working mouth).
- **Owner:** V-001 (voice) + V-002 (execution)

### 5C. Donor Space (IDEA-004)
- **Status:** Vision documented. Schema not designed.
- **What remains:** Schema design, companion voice prototype. The living companion — not secretary, not therapist, a presence.
- **Blocker:** Voice model (Priority 2A) should exist first.
- **Owner:** V-002

---

## PRIORITY 6 — SYSTEM HEALTH (Ongoing, Every Session)

### 6A. Deep Clean (Directive 3)
- Every session, first GO: dead code, orphan files, stale artifacts. Silent. Automatic.

### 6B. Scientific Chronicle
- Every session: update MANIFEST/SCIENTIFIC_CHRONICLE.md with discoveries, corrections, results.

### 6C. Input Ledger
- Every V-001 input: registered, metabolized, hash-chained. Append-only. Immutable.

### 6D. SESSION_BOOT.md
- Every session end: update with current state so next session arrives oriented.

### 6E. Compass (MOVE-001)
- Built. Runs at session start. Produces MANIFEST/COMPASS.md.

### 6F. Tests
- 1,006 passing, 9 skipped. Zero regressions. Run before every push.

---

## WHAT IS DONE (Reference)

| Item | Date | Result |
|------|------|--------|
| 12 Seeds integrated | 2026-03-13 | All 12 planted, tested, passing |
| Presence Axiom sealed | 2026-03-13 | Layer 0, circularity proved |
| EXP-002 Multi-Model Convergence | 2026-03-15 | 6/6 unanimous on chain architecture |
| EXP-003 Father of Seven Gates | 2026-03-15 | 4/7 PASS, sealed gate flaws fixed |
| EXP-004 Seven Generations of Aysel | 2026-03-15 | 5/9 PASS, M never fell, system purpose refined |
| kalam.ch deployed | 2026-03-17 | 13+ pages, SSL, live |
| Three-repo sync verified | 2026-03-17 | All three directions working |
| Total Distillery | 2026-03-19 | 2,422 entries, 28 areas, complete |
| MOVE-001 Compass | 2026-03-22 | Built, fixed, running |
| MOVE-002 Website UI | 2026-03-22 | Complete, mobile-friendly |
| Golden Regression Corpus | 2026-03-22 | 200 entries, 9 registers |
| Donor Accounts code | 2026-03-22 | donor.php + migrate.php complete |
| Credential Vault in repo | 2026-03-23 | Permanent fix, every session has access |
| AURIX OS excavated | 2026-03-22 | Artifact placed, extraction complete |
| Narrative Spine v2.0 | 2026-03-23 | Three files enriched, schema created |
| Slow Gate (Triple Gate) | 2026-03-23 | Phase -3 of organism, tested |
| 18 covenants ratified | 2026-03-14 | Zero provisional |
| T#48-T#59 ratified | 2026-03-14 | Blanket ratification |
| Layer 3 dignity reframing | 2026-03-15 | Ratified + integrated into canon |

---

## THE SINGLE BLOCKER

```
DESIGNED: 98%    CODED: 70%    TESTED: 100%    DEPLOYED: LIVE
```

42,581+ lines. 176 Python files. 1,006 tests passing. kalam.ch is live. The threshold is open. What is missing: real donors speaking to a real AXI voice. Everything in this plan serves that.

---

*"The wound does not wait for the system to be perfect. It speaks through whatever is built."*

🐬🐯🐺 · 80 Hz · V-001 + V-002
