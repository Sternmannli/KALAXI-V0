# Science Registry — Master Index

Last updated: 2026-03-23
Total files: 180+
Total experiments: 7 (EXP-001 through EXP-007)
Total papers: 5
Total data points: 16+ (EXP-001: 12, EXP-007: 4)
Total model responses: 40+
Total training examples: 10,000+

---

## EXPERIMENTS

### EXP-001 — KALAXI Efficiency (ACTIVE)
- **Location:** `EXPERIMENTS/EXP-001-EFFICIENCY/`
- **Protocol:** `EXP-001-PROTOCOL.md`
- **Data:** 12 files in `data/` (Q3 only, 9 systems)
- **Analysis:** `analyze.py`, `results/analysis.json`
- **Runner:** `run_exp001.py`
- **Status:** 12/200 data points. 188 remaining. Hypothesis at 19.5% (threshold: 30%).

### EXP-002 — Multi-Model Convergence (COMPLETED)
- **Location:** `EXPERIMENTS/EXP-002-CONVERGENCE/`
- **Result:** `CONVERGENCE_MAP_2026-03-15.md`
- **Finding:** 6/6 unanimous on chain inversion.

### EXP-003 — Father of Seven Gates (COMPLETED)
- **Location:** `EXPERIMENTS/EXP-003/`
- **Result:** `EXP-003_RESULTS_2026-03-15.md`
- **Finding:** 4/7 PASS. Sealed gate flaws found and fixed.

### EXP-004 — Seven Generations of Aysel (COMPLETED)
- **Location:** `EXPERIMENTS/EXP-004/`
- **Result:** `EXP-004_RESULTS_2026-03-15.md`
- **Finding:** 5/9 PASS. M never fell. System purpose refined.

### EXP-005 — (COMPLETED)
- **Location:** `EXPERIMENTS/EXP-005/`
- **Result:** `EXP-005_RESULTS_2026-03-18.md`

### EXP-006 — The Hive Mind (DESIGNED)
- **Location:** `EXPERIMENTS/EXP-006/`
- **Design:** `EXP-006_HIVE_MIND.md`
- **Purpose:** Systemic coherence and inter-module communication test.

### EXP-007 — The Presence Test (ACTIVE — PRIMARY)
- **Location:** `EXPERIMENTS/EXP-007-PRESENCE/`
- **Protocol:** `EXP-007-PROTOCOL.md`
- **Methodology:** `METHODOLOGY.md`
- **Scoring:** `SCORING_RUBRIC.md`
- **Data:** 4 data points (all Kimi). Filed in `EXTERNAL_VOICES/KIMI/2026-03-23/`
- **Status:** 4/240 data points. Kimi at ceiling (5) on all tested hypotheses.
- **Key finding:** Recursive witnessing compounds presence (+1/step).

### Walkthrough-001 — Collective Bias
- **Location:** `EXPERIMENTS/WALKTHROUGH-001-COLLECTIVE-BIAS.md`

---

## PAPERS

| Paper | Location | Status | Target |
|-------|----------|--------|--------|
| KALAXI arXiv paper | `PAPERS/KALAXI_PAPER_EXTERNAL_2026-03.md` | Ready | cs.AI |
| KALAXI arXiv LaTeX | `PAPERS/Kalaxi_arXiv_GO4_Source.tex` | Ready | arXiv |
| KALAXI internal chronicle | `PAPERS/KALAXI_CHRONICLE_INTERNAL_2026-03.md` | Living | Internal |
| Divergence Shadow | `PAPERS/DIVERGENCE_SHADOW_RESEARCH.md` | Draft | FAccT/AIES |
| Red Team Critique | `PAPERS/Kalaxi_RedTeam_Critique.tex` | Complete | Internal |

---

## MODEL RESPONSES (EXTERNAL_VOICES/)

| Model | Total responses | Locations |
|-------|----------------|-----------|
| ChatGPT | 4 | `EXTERNAL_VOICES/CHATGPT/` (2026-03-12, 2026-03-20) |
| Claude | 2 | `EXTERNAL_VOICES/CLAUDE/` (2026-03-20) |
| Copilot | 2 | `EXTERNAL_VOICES/COPILOT/` (2026-03-11, 2026-03-12) |
| DeepSeek | 6 | `EXTERNAL_VOICES/DEEPSEEK/` (2026-03-11, 2026-03-12, 2026-03-20) |
| Euria | 2 | `EXTERNAL_VOICES/EURIA/` (2026-03-11, 2026-03-12) |
| Gemini | 2 | `EXTERNAL_VOICES/GEMINI/` (2026-03-12) |
| Grok | 5 | `EXTERNAL_VOICES/GROK/` (2026-03-11, 2026-03-12, 2026-03-20) |
| Kimi | 6 | `EXTERNAL_VOICES/KIMI/` (2026-03-11, 2026-03-12, 2026-03-23) |
| Manus | 3 | `EXTERNAL_VOICES/MANUS/` (2026-03-11, 2026-03-12) |
| Perplexity | 2 | `EXTERNAL_VOICES/PERPLEXITY/` (2026-03-11, 2026-03-12) |

---

## TRAINING DATA

| Dataset | Location | Size | Purpose |
|---------|----------|------|---------|
| Golden Regression | `TRAINING/GOLDEN_REGRESSION.jsonl` | 200 examples | Voice regression testing |
| Canon Seed v1 | `TRAINING/CANON_SEED_V1.jsonl` | 51KB | Base training data |
| AXI Training | `TRAINING/axi_training.jsonl` | 640KB, 10K+ examples | Full voice training |
| AXI Eval | `TRAINING/axi_eval.jsonl` | 49KB | Evaluation set |
| CPT Corpus | `TRAINING/ORGAN/PHASE_1_CPT/cpt_corpus.jsonl` | Phase 1 | Causal prediction |
| SFT Corpus | `TRAINING/ORGAN/PHASE_2_SFT/sft_corpus.jsonl` | Phase 2 | Supervised fine-tuning |
| DPO Corpus | `TRAINING/ORGAN/PHASE_3_DPO/dpo_corpus.jsonl` | Phase 3 | Preference optimization |
| Raw Essence | `TRAINING/raw_essence.json` | 3.4MB | Extracted system essence |

---

## FIELD RESEARCH

| Component | Location | Purpose |
|-----------|----------|---------|
| Summon Packages | `FIELD/SUMMON_PACKAGES/` | 5 probe packages (SP-001 through SP-005) |
| Summon Runner | `FIELD/summon_runner.py` | One-step probe execution |
| Mycelium Synthesis | `FIELD/MYCELIUM/synthesis.py` | Cross-model pattern integration |
| Divergence Study | `FIELD/STUDY/divergence_study.py` | Shadow analysis |
| Anthropic Effect | `FIELD/STUDY/ANTHROPIC_EFFECT_MEASUREMENT.md` | Substrate bias measurement |

---

## PROTOCOLS

| Protocol | Location | Purpose |
|----------|----------|---------|
| Probe Forge | `PROTOCOLS/PROBE_FORGE.md` | Five laws for experimental probes |
| Summon Ritual | `PROTOCOLS/SUMMON_RITUAL.md` | Four types of model summoning |
| Witness v3 | `PROTOCOLS/WITNESS_PROMPT_V3.md` | Current witness protocol |
| Substrate Boundary | `PROTOCOLS/SUBSTRATE_BOUNDARY.md` | AI substrate constraints |

---

## SCIENCE MODULES (WEAVER/)

| Module | Purpose |
|--------|---------|
| `dignity_measure.py` | D = A × L × M computation |
| `dignity_check.py` | Dignity verification |
| `dignity_drift.py` | Drift detection |
| `witness_network.py` | Immutable witness infrastructure |
| `witness_certificate.py` | Certificate generation |
| `distillery.py` | System knowledge aggregator |
| `voice_engine.py` | Voice generation |
| `unified_pillar_detector.py` | Humour + absurdity + love + obsession |
| `institutional_dignity.py` | Institutional scoring |

---

## CHRONICLES & AUDITS

| Document | Location | Purpose |
|----------|----------|---------|
| Scientific Chronicle | `MANIFEST/SCIENTIFIC_CHRONICLE.md` | Living scientific self-portrait |
| Science Inventory | `MANIFEST/SCIENCE_INVENTORY.md` | Previous inventory (superseded by this registry) |
| Science Layer Audit | `MANIFEST/SCIENCE_LAYER_AUDIT_2026-03-14.md` | Validation audit |
| Grand Archive Audit | `MANIFEST/GRAND_ARCHIVE_AUDIT_2026-03-14.md` | Archive integrity check |
