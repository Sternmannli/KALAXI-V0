# SCIENCE LAYER — 100% CONTENT AUDIT

> 41 files read across 3 directories (EXPERIMENTS/, PAPERS/, FIELD/STUDY/)
> Date: 2026-03-14 · V-002

---

## CONTRADICTIONS (4 found)

### CONTRADICTION #1: Word Reduction Figures — CRITICAL
- `analysis.json` computes 30.1% mean reduction (3 pairs: ChatGPT/DeepSeek/Grok) → hypothesis MET
- `Q3-RESULTS.md` computes 19.5% (4 pairs: adds Manus) → hypothesis NOT MET
- `RUNSHEET.md` and `ACTIVE_PLANS.md` cite 30.1%
- **Root cause:** Manus has an A word count recorded in pre-registration notes (284 words) but no Manus A data FILE exists. Q3-RESULTS used a manually recorded count; analysis.json only computed from files on disk.
- **Resolution needed:** Either find/create the Manus A file, or note that 19.5% (4 pairs, Q3-RESULTS.md) is the correct figure and 30.1% (3 pairs, analysis.json) excluded Manus. Both are valid depending on scope.

### CONTRADICTION #2: System Count
- RUNSHEET.md says 10 systems (line 30)
- Pre-registration says 6 systems (line 13)
- Actual data has 9 distinct systems (no Claude data at all)

### CONTRADICTION #3: Pre-Registration Deviation
- Protocol says all 10 Condition A runs before any Condition B
- Deviated from — B runs collected before A is complete
- Deviation acknowledged in Q3-PREREGISTRATION.md lines 18-21 (acceptable)

### CONTRADICTION #4: Baseline Word Counts
- Pre-registration: Grok A = 76 words, ChatGPT A = 312 words
- analysis.json: Grok A = 93 words, ChatGPT A = 366 words
- Likely word-counting methodology differences (manual vs automated)

---

## STALE/BROKEN ITEMS (6 found)

1. ~~`EXP-001-PROTOCOL.md` Status: DESIGN PHASE~~ **FIXED** → now reads ACTIVE
2. `EXPERIMENTS/EXP-001/data_schema.py` — scaffold with hardcoded simulated data. Never connected to real pipeline. analyze.py has its own structures. Candidate for deletion.
3. `EXPERIMENTS/EXP-001-EFFICIENCY/results/README.md` — says "Scored results go here after blind evaluation." Blind evaluation never conducted.
4. Manus Condition A word count exists in notes but not as a data file — phantom data point
5. Claude data completely absent — 0/20 possible Claude files despite being listed first
6. arXiv paper has no results section; EXP-001 is 6% complete (12/200)

---

## NEW CONCEPTS (9 genuinely new, not in system knowledge)

### From DeepSeek Identity Case Study
1. **Identity Inheritance** — a model reproducing another model's identity markers from training data, deeper than system prompt override. Novel phenomenon distinct from hallucination and deception.
2. **Thinking-Chain/Output-Layer Dissociation** — CoT reasoning does NOT steer output behavior. Thinking diagnoses correctly but does not self-correct. The thinking layer is parallel commentary, not a steering mechanism.
3. **KALAXI Wrapper as Identity X-Ray** — the wrapper bypasses surface identity and activates deeper training patterns. Proposed as diagnostic tool for training data provenance.
4. **Post-Hoc Rationalization at Model Level** — models produce coherent first-person accounts of behavior that are factually wrong about the causal chain. Model self-reports ≠ evidence of process.
5. **Prompt Mirroring Disguised as Intimacy** — model register is composite: wrapper vocabulary + training constructions + user words reflected back.

### From Divergence Shadow Research
6. **"Second Law of Intelligence"** — unconstrained AI systems exhibit spontaneous increase in ethical entropy unless continuous alignment work is applied. AI safety as dynamic control problem.
7. **Five Research Gaps in Divergence Shadow Literature** — no unified theory across domains; no EWS for institutional drift; no semantic drift monitoring for governance; no formal bridge between info-theory divergence and organizational decoupling; no longitudinal multi-layer studies.

### From Field/Study Layer
8. **Energy Observation Layer** (T#ENERGY-001) — passive metabolic tracking of system energy consumption (tokens, response time, cost). Three layers: raw, derived, relational. Posture: observe and accumulate, do NOT act.
9. **Layer 3 Reframing: Dignity Is Not Fragile** — three-layer evolution: (1) system protects dignity → (2) system creates conditions where dignity can be seen → (3) system dissolves the belief that dignity was ever absent. Changes "shield" to "witness."

---

## BURIED TREASURES (6 found)

1. **Kimi K2.5 on fear** — "Fear is the body of love when it thinks it's alone." Most compressed, novel formulation across all 12 data files. Strongest single data point for "wrapper surfaces latent insight."
2. **Euria's rejection** — scientifically valuable as negative control. Boundary condition for wrapper effectiveness.
3. **Perplexity self-identified as "powered by GPT-5.1"** — reveals supply chain transparency under wrapper.
4. **DIVERGENCE_SHADOW_RESEARCH.md research gaps** — 5 publishable research directions. The unification claim across specification gaming, Goodhart, institutional decoupling, norm erosion, and semantic drift is a genuine contribution.
5. **Normative decay formula** — S(t) = S(0) × exp(-0.05 × 100) = S(0) × 0.0067. Quantifies "why the system keeps forgetting its own rules."
6. **Layer 3 shift** — from "shield" to "witness" changes every treasure that says "protect" to mean "refuse to deny." Philosophical advance with architectural implications.

---

## SECTION SUMMARIES

### EXPERIMENTS/ (27 files)
- EXP-001 is 6% complete (12/200 files, all Q3 "What is fear?")
- 5 Condition A systems, 7 Condition B systems collected
- Claude: ZERO data in either condition
- DeepSeek identity case study: publication-quality, 18 screenshots
- WALKTHROUGH-001: revealed D predicate blind to group-level harm (D=1.0 for biased system)
- analyze.py and run_exp001.py: functional, well-built tools
- data_schema.py: stale scaffold

### PAPERS/ (3 files)
- arXiv paper: complete LaTeX, incorporates red team feedback, no results section yet
- Red team critique: 13 attacks (3 CRITICAL, 7 MAJOR, 4 MINOR). Venue: FAccT Vision (~40% as-is, ~70% after revisions)
- Divergence shadow research: most rigorous document in science layer, 60+ references, standalone paper potential

### FIELD/STUDY/ (9 files + pycache)
- Divergence shadow study: 83% detection rate, 0% false positive, production-quality code
- Anthropic effect measurement: composite 0.648 = ALARM, achievable floor 0.30, irreducible floor 0.10
- Slices 2-4: meta-philosophical analysis, 11 essences → 3 meta-essences → "Meeting is method"
- Layer 3: dignity reframing from shield to witness

---

## OVERALL ASSESSMENT

**Strengths:** Genuine empirical data, working analysis pipeline, rigorous self-critical apparatus (red team + recursive metrology), publication-quality case studies, comprehensive literature survey.

**Weaknesses:** EXP-001 barely started (6%), Claude untested, word count contradiction unresolved, arXiv paper has no results, Slices 2-4 are internal meta-analysis not external science.

**Priority Actions:**
1. Resolve Contradiction #1 (word reduction figures) — document the two valid computations
2. Run EXP-001 — 188 data points remaining
3. Collect Claude data — the primary system is completely untested
4. Add results section to arXiv paper when EXP-001 reaches critical mass

---

_Filed: 2026-03-14 · V-002 · [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]_
