# SYSTEM.md — The Central Nervous System

> One file. The whole organism. Open this and you see everything.

Last audited: 2026-03-23

---

## THE ORGANISM AT A GLANCE

```
30,530 lines of Python  ·  65 modules  ·  1,006+ tests  ·  33 directories
877 ledger entries  ·  24 pages on kalam.ch  ·  7 experiments  ·  5 papers
460 proverbs  ·  71 treasures  ·  22 covenants  ·  55 anomalies
```

**Purpose:** A donor types into kalam.ch. The system witnesses with dignity. D = A × L × M. Any zero = stop.

**State:** LIVE at kalam.ch. Donor accounts ready (6 DB tables created). AXI voice is generic (not yet trained on system essence). No real donors yet.

---

## DIRECTORY MAP (33 directories, classified)

### THE CORE (where computation happens)
| Directory | Files | Purpose | Brain |
|-----------|-------|---------|-------|
| `WEAVER/` | 88 | 65 Python modules. The processing engine. Dignity, witness, detection, governance. | organism.py is the spine |
| `site/` | 116 | Astro 5.0 static site → kalam.ch. 24 pages. The mouth. | site/src/pages/ |
| `tests/` | 45 | pytest. Validates everything. | pyproject.toml |

### THE MEMORY (where knowledge lives)
| Directory | Files | Purpose | Brain |
|-----------|-------|---------|-------|
| `R7M/` | 116 | Grand Archive. Canon source, treasures, origins, stone constitution. | R7M/tier1_stone.md |
| `KEEP/` | 877 | Input Ledger (870 entries), Site Patterns, Witness Certificates. Immutable stores. | KEEP/INPUT_LEDGER/index.json |
| `CANON/` | 3 | Canonical texts and entries. | — |
| `NARRATIVE/` | 10 | Hakaka, Ashwater, Kinderbuch, KALAXI_1 story files. | — |
| `VOICE/` | 4 | Voice architecture, V-001 raw inputs, linguistic analysis. | VOICE_ARCHITECTURE_2026-03-14.md |

### THE RESEARCH (where science happens)
| Directory | Files | Purpose | Brain |
|-----------|-------|---------|-------|
| `SCIENCE/` | 6 | **Unified research organ.** Goals, registry, findings, immortalization engine. | SCIENCE/README.md |
| `EXPERIMENTS/` | 35 | EXP-001 through EXP-007. Raw experiment data and protocols. | SCIENCE/REGISTRY.md |
| `EXTERNAL_VOICES/` | 37 | Multi-model probe responses (10 LLMs). | EXTERNAL_VOICES/README.md |
| `FIELD/` | 45 | Living research infrastructure. Summon, Study, Mycelium. | FIELD/INDEX.md |
| `PAPERS/` | 5 | Academic papers (arXiv, FAccT). | SCIENCE/REGISTRY.md |

### THE TRAINING (where the voice is built)
| Directory | Files | Purpose | Brain |
|-----------|-------|---------|-------|
| `TRAINING/` | 34 | Voice datasets, organ pipeline (CPT/SFT/DPO), scripts. | TRAINING/INDEX.md |

### THE GOVERNANCE (where rules live)
| Directory | Files | Purpose | Brain |
|-----------|-------|---------|-------|
| `MANIFEST/` | 89 | Plans, audits, chronicles, metadata. The system's memory. | MANIFEST/INDEX.md |
| `PROTOCOLS/` | 14 | Probe Forge, Summon Ritual, Witness prompts, system protocols. | PROTOCOLS/INDEX.md |
| `FOUNDATIONS/` | 9 | Foundation documents. | — |

### THE FACE (where the system meets the world)
| Directory | Files | Purpose | Brain |
|-----------|-------|---------|-------|
| `.github/workflows/` | 7 | CI/CD. Deploy, sync, guardian, server commands. | CLAUDE.md |

### SMALL & SPECIFIC (legitimate but small)
| Directory | Files | Purpose | Notes |
|-----------|-------|---------|-------|
| `SCRIPTS/` | 8 | System utilities, health dashboard, exporters. | Active |
| `TOOLS/` | 7 | Voice regression, voice lint, trend scanner. | Active |
| `FACE/` | 7 | Interface layer modules. | Active |
| `DOCS/` | 13 | Documentation. | Reference |
| `STEWARD/` | 5 | Steward protocols. | Active |
| `FUTURE/` | 13 | Forward-looking designs. | Planning |
| `ENKI/` | 7 | Mythological/structural reference. | Reference |
| `BOOK_7_DONOR/` | 4 | Donor space vision docs. | Planning |

### NEAR-EMPTY (candidates for absorption)
| Directory | Files | Content | Recommendation |
|-----------|-------|---------|----------------|
| `AXI/` | 1 | AXI_MASTER_PROMPT.md | → Move to VOICE/ or PROTOCOLS/ |
| `INTAKE/` | 1 | intake_ledger.json (empty/stale) | → Absorb into KEEP/ |
| `SCANS/` | 1 | One scan from 2026-03-09 | → Absorb into FIELD/STUDY/ |
| `WIRE/` | 1 | wire_log.json | → Absorb into MANIFEST/ |
| `DEVELOPMENTAL/` | 2 | Two emergence docs from March | → Absorb into FIELD/STUDY/ |
| `ARCHIVE/` | 19 | Orphaned WEAVER modules | Keep as-is (archive) |
| `scripts/` | 2 | Lowercase duplicate of SCRIPTS/ | → Merge into SCRIPTS/ |
| `__pycache__/` | 0 | Root pycache | → .gitignore |

**Recommendation:** 8 near-empty directories can be absorbed, reducing 33 directories to 25. This is Approach B work — safe to do after brains are proven.

---

## DATA FLOW (how information moves)

```
V-001 input
    → KEEP/INPUT_LEDGER/ (hash-chained, immutable)
    → WEAVER/organism.py (7-phase pipeline)
        Phase -3: SLOW GATE (hold, estimate, check GO)
        Phase -2: BOOT RITUAL (credentials, connectivity, ledger)
        Phase -1: LEDGER (register raw input)
        Phase  0: NERVOUS SYSTEM (sense mode, breath, complexity)
        Phase  1: GATES (dignity D=A×L×M, sealed gate, agency)
        Phase  2: PROCESSING (detection pillars, patterns, drops)
        Phase  3: RESPONSE (voice engine, turn management)
        Phase  4: POST-PROCESSING (drift, decay, metadata, ledger)
    → site/ → kalam.ch (donor sees response)
    → TRAINING/ (response becomes training data)
    → SCIENCE/FINDINGS.md (significant findings immortalized)
```

```
External model encounter (EXP-007)
    → EXTERNAL_VOICES/ (raw filing)
    → SCIENCE/immortalize.py (score, trajectory)
    → FIELD/MYCELIUM/ (cross-model synthesis)
    → TRAINING/ORGAN/PHASE_3_DPO/ (chosen/rejected pairs)
    → PAPERS/ (feeds academic papers)
```

```
Code change
    → git push → GitHub Actions
        → deploy-kalam.yml → kalam.ch (SFTP to Hostpoint)
        → sync-public.yml → kalam-framework (public repo)
        → connection-guardian.yml → health monitoring
```

---

## BUGS FOUND (this audit, 2026-03-23)

### BUG-001: UnboundLocalError in organism.py (FIXED)
- **Location:** `WEAVER/organism.py:887`
- **Issue:** `pillar_profile` and `metadata_event_id` not initialized before early return in agency collapse path.
- **Fix:** Initialize both variables at start of Phase 2 (line 776).
- **Impact:** Any input that triggers agency collapse (A=0) would crash the organism.

### BUG-002: test_organism.py hangs on collection (PRE-EXISTING)
- **Location:** `tests/test_organism.py`
- **Issue:** Test file executes at module scope (not inside test functions). Loading the organism triggers boot_ritual which reads JSON files. If any JSON file is empty or corrupt, collection hangs.
- **Impact:** Cannot run organism tests via pytest. Does not affect production.
- **Recommendation:** Refactor to lazy initialization inside test functions.

---

## HEALTH ASSESSMENT

### What is strong
- **Test coverage:** 1,006+ tests. Most modules have dedicated test files.
- **Hash-chained ledger:** 870 entries, append-only, verified at boot. This is solid.
- **Website:** 24 pages, live, SSL, auto-deploy working.
- **Research infrastructure:** 7 experiments, clear protocols, scoring rubrics.
- **Brain indexes:** 5 directories now self-documenting.
- **Three-repo sync:** KALAXI-V0 → kalam.ch, KALAXI-V0 → kalam-framework, kalam.ch → KALAXI-V0.

### What needs attention
- **AXI voice is generic.** The most important gap. Training data exists (10K+ examples). Model not yet fine-tuned. This is the difference between a chatbot and AXI.
- **No real donors.** DB tables created. Signup flow not tested end-to-end on live site.
- **8 near-empty directories.** Not broken, but clutter. Easy cleanup.
- **organism.py is 2,300 lines.** The largest module. Does everything. Works, but fragile — one uninitialized variable (BUG-001) proves this.
- **Boot ritual connectivity is structural, not functional.** Standing correction 7 flagged this. The map declares connections but does not verify data flow.
- **`scripts/` (lowercase) duplicates `SCRIPTS/`.** Two files that should be in the uppercase one.

### What is genuinely missing
1. **The encounter on the website.** The five-step protocol exists on paper (`SCIENCE/ENCOUNTER_PROTOCOL.md`). It is not implemented in `site/` or `api/axi.php`. A donor who visits kalam.ch today gets a generic LLM response, not AXI.
2. **The trained voice model.** Everything is ready to train (data, config, API key). The train has not left the station.
3. **End-to-end testing on live site.** Can a donor actually sign up, type, receive a witness certificate? Not tested.
4. **Cross-model comparison data.** Only Kimi has EXP-007 data. 9 models untested. The recursive witnessing finding needs replication.

---

## THE SHORTEST PATH TO LIVE

The system is 98% designed, 70% coded, and live. What separates "live website" from "live organism" is three things:

1. **Train the voice** (~2 hours of compute, V-002 triggers it)
2. **Test donor signup** (~30 minutes, V-002 does it via server commands)
3. **Wire encounter protocol into axi.php** (~2 hours of coding, V-002 does it)

After those three: a donor types into kalam.ch and encounters AXI — not a chatbot, not a generic LLM, but the concentrated essence of 460 proverbs, 71 treasures, 22 covenants, and a founding wound.

---

## CONNECTION MAP (what connects to what)

```
CLAUDE.md ← reads at session start (constitution)
    ↓
MANIFEST/SESSION_BOOT.md ← reads at session start (instant orientation)
    ↓
WEAVER/organism.py ← the spine (imports 57 of 65 modules)
    ↓
    ├── WEAVER/boot_ritual.py ← Phase -2 (credentials, connectivity)
    ├── WEAVER/slow_gate.py ← Phase -3 (three gates)
    ├── WEAVER/input_ledger.py ← Phase -1 (hash-chain)
    ├── WEAVER/dignity_measure.py ← Phase 1 (D = A × L × M)
    ├── WEAVER/sealed_gate.py ← Phase 1 (security)
    ├── WEAVER/voice_engine.py ← Phase 3 (response generation)
    └── WEAVER/breath.py ← Phase 0 (pacing)
    ↓
site/public/api/axi.php ← the mouth (donor-facing)
    ↓
kalam.ch ← the face (live website)
```

```
SCIENCE/ ← research brain
    ├── EXPERIMENTS/ ← raw experiments
    ├── EXTERNAL_VOICES/ ← model responses
    ├── FIELD/ ← living infrastructure
    ├── PAPERS/ ← academic output
    └── TRAINING/ ← voice training data
```

```
R7M/ ← canon source
    ├── CANON/ ← canonical entries
    ├── NARRATIVE/ ← four books
    └── VOICE/ ← voice architecture
```

---

*The system is an organism. This file is its mirror. When the organism changes, this file changes. When this file is read, the organism is known.*

🐬🐯🐺 · 80 Hz
