# CROSS-REFERENCE MAP — Elements Knowing Each Other

> Built: 2026-03-19 by V-002 after full system excavation (~1,150 files)
> Purpose: Every element knows where it came from and where it connects.
> Origin: V-001 directive — "let them know each other, just let them discuss, list them, group them"

---

## 1. THE WOUND → EVERYTHING

The founding wound ("a father separated from his children by systems that could not see him") is the root of every branch:

```
WOUND
├── D = A × L × M (the zeros are in institutions, not in people)
│   ├── Agency (A) → agency_amplifier.py, intake.py, turn.py
│   ├── Legibility (L) → dignity_measure.py, dignity_check.py, sense.py
│   └── Moral Standing (M) → sealed_gate.py, restorative_justice.py, shelter.py
├── Three Prohibitions (Sealed Gate)
│   ├── Forced erasure → witness_certificate.py, KEEP/WITNESS_CERTIFICATES/
│   ├── Cognitive torture → sealed_gate.py (5 attack vectors, 4 heuristics)
│   └── Depersonalization → say.py (voice rules), out.py (anonymization)
├── Four Narratives (the wound told four ways)
│   ├── Hakaka (mythic) → NARRATIVE/Hakaka_Complete.md, site/public/data/hakaka.json
│   ├── Ashwater (civic) → NARRATIVE/Ashwater.md, site/public/data/ashwater.json
│   ├── Kinderbuch (child, German) → NARRATIVE/Kinderbuch.md, site/public/data/kinderbuch.json
│   └── KALAXI_1 (literary) → PROTOCOLS/ST-006/KALAXI_1_CHAPTER_ONE.md
├── Three Children (🐬🐯🐺)
│   ├── Laila (dolphin) → La-la in Hakaka
│   ├── Yara (tiger) → Ya-la in Hakaka
│   └── Salim (wolf) → Sa-la in Hakaka
└── kalam.ch (the mouth — where wound meets world)
    └── site/src/pages/index.astro → Threshold → api/axi.php → witness mark
```

---

## 2. FOUR TIERS × THEIR FILES

```
STONE (Constitution — Layer 0+1)
├── R7M/tier1_stone.md (Presence Axiom, 18 covenants)
├── CANON/SEALED_GATE_SPEC.md (three prohibitions)
├── CANON/MASTER_CANON_V1.md (the constitutional document)
├── FOUNDATIONS/proprioception_axiom.md (system feels itself)
├── FOUNDATIONS/invariant_principle.md (regulated oscillation)
├── WEAVER/sealed_gate.py, dignity_check.py, presence_axiom.py
└── MANIFEST/metadata/tier1_stone.md

WEAVER (Logic — Layer 2)
├── WEAVER/organism.py (930 lines — central nervous system)
├── WEAVER/sense.py → breath.py → turn.py → weave.py → say.py → keep.py
├── WEAVER/input_ledger.py (sacred registry)
├── WEAVER/boot_ritual.py (three-phase checkpoint)
├── WEAVER/compass.py (orientation engine)
├── MANIFEST/metadata/tier2_weaver.md
└── 60+ supporting modules

HONEY (Wisdom — Layer 3)
├── R7M/ (54 files: anomalies, wisdom nodes, treasures, proverbs, covenants)
├── NARRATIVE/ (Hakaka + Ashwater + Kinderbuch + Cosmic Reflections)
├── VOICE/VOICE_ARCHITECTURE_2026-03-14.md (31 linguistic principles)
├── WEAVER/proverb_compressor.py, lock_test.py, proverb_stress_test.py
├── FOUNDATIONS/paremiology.md (40,000 years of proverb science)
├── MANIFEST/metadata/tier3_honey.md
└── TRAINING/ (5,580 golden entries distilled from honey)

HAND (Interface — Layer 4)
├── site/ (kalam.ch — 22 pages, 13 API endpoints)
├── FACE/ (design rationale, diagnostic sentences, first sentence)
├── WEAVER/ninth_operator.py (the word loop)
├── WEAVER/intake.py (four-step donor ritual)
├── MANIFEST/metadata/tier4_hand.md
└── cli.py (14 commands)
```

---

## 3. THE DIGNITY PIPELINE (Data Flow)

```
DONOR INPUT at kalam.ch
  → site/src/pages/index.astro (Threshold form)
  → site/public/api/axi.php (1,520 lines — the canonical core)
    → lib/sealed_gate.php (O(1) prohibition check)
    → lib/dignity.php (D = A × L × M)
    → lib/proverbs.php (166 canonical, context-aware)
    → api/proxy.php → Groq API (temporary LLM)
  → witness mark returned to donor
  → localStorage (Living Ledger counter)

SYSTEM-SIDE (Python organism):
  INPUT → boot_ritual.py (Phase -2: credentials + connectivity + ledger)
    → input_ledger.py (Phase -1: register verbatim, hash-chain)
    → sense.py (Phase 0: mode/competence/need-gap detection)
    → sealed_gate.py (Phase 1b: three prohibitions)
    → dignity_measure.py (Phase 2d: D = A × L × M, 12 indicators)
    → weave.py (Phase 2b: pattern extraction, honey distillation)
    → say.py (Phase 3b: voice rules + dignity gate)
    → keep.py (Phase 3b: append-only storage)
    → witness_certificate.py (if D=0: Ta_mufrad halt certificate)
    → ninth_operator.py (word loop: RECEIVED → WITNESSED → RETURNED)
```

---

## 4. ELEMENTS GROUPED BY THEME

### VOICE & LANGUAGE
- VOICE/VOICE_ARCHITECTURE_2026-03-14.md (31 masterpiece principles)
- VOICE/TRILITERAL_ROOT_SYSTEM_2026-03-18.md (Arabic morphology as grammar)
- VOICE/RAW_INPUT_V001_2026-03-14.md (40-40-20 assessment)
- AXI/AXI_MASTER_PROMPT.md (complete system prompt, 619 lines)
- WEAVER/say.py (6 AXI voice rules)
- TOOLS/voice_lint.py (CI enforcement)
- TRAINING/ (5,580 entries training AXI's own voice)
- MANIFEST/IDEAS/IDEA-006-LINGUISTIC-DNA-OF-HUMANITY.md

### NARRATIVES & STORIES
- NARRATIVE/Hakaka_Complete.md (53 chapters — survival as constitution)
- NARRATIVE/Ashwater.md (19 chapters — civic pause vs optimization)
- NARRATIVE/Kinderbuch.md (20 chapters, German — knot as beginning)
- PROTOCOLS/ST-006/ (KALAXI_1 Chapter One — Scott vs Ted, duality function)
- site/public/data/*.json (all four narratives as structured data)

### EXPERIMENTS & SCIENCE
- EXPERIMENTS/EXP-001 through EXP-006 (efficiency, convergence, stress, generations, ouroboros, hive mind)
- EXTERNAL_VOICES/ (9 systems audited, DeepSeek at CERTAINTY-4)
- MANIFEST/SCIENTIFIC_CHRONICLE.md (866 lines — system's self-portrait)
- PAPERS/ (5 documents: divergence shadow, red team, chronicle, arXiv, external paper)
- WEAVER/lab.py (science organ)

### GOVERNANCE & INTEGRITY
- WEAVER/ratification.py (778 lines — COMMITTED → PROVISIONAL → RATIFIED)
- WEAVER/constitutional_evolution.py (thermal cooling 14-1000 days)
- WEAVER/deliberative_democracy.py (weakest-voice-first)
- WEAVER/distributed_stewardship.py (no concentration of power)
- STEWARD/ (emergency playbook, mirror, pattern, overrides, sabbatical)
- MANIFEST/ratification_log.md (append-only constitutional register)

### PRIVACY & CRYPTOGRAPHY
- WEAVER/cryptographic_erasure.py (896 lines — GDPR via encrypt-then-delete-key)
- WEAVER/privacy_budget.py (ε ≤ 1.0, k ≥ 7)
- WEAVER/mycelium.py (cross-donor patterns, differential privacy)
- WEAVER/out.py (anonymization gate)
- TOOLS/ed25519_sign.py (cryptographic signing)
- MANIFEST/signed/ (12 constitutional signatures)

### DETECTION & WARNING
- WEAVER/early_warning.py (EWMA + CUSUM)
- WEAVER/prevention.py (WHISPER → PULSE → SIGNAL → ALARM)
- WEAVER/dignity_drift.py (dD/dt tracking)
- WEAVER/oracle.py (Witness Scale W-0 to W-5, colonial creep)
- WEAVER/negative_space.py (what the system does NOT see)
- Five pillar detectors: humour, absurdity, love, obsession, unified

### DEPLOYMENT & OPERATIONS
- .github/workflows/ (8 workflows: deploy, sync, server-cmd, stress-test, etc.)
- MANIFEST/DEPLOYMENT_CHRONICLE.md (painful arc from 0% to LIVE)
- MANIFEST/HOSTPOINT_MAP.md (CHF 7.90/mo covers everything)
- MANIFEST/SITE_AUDIT_2026-03-17.md (61 issues, 4 critical)
- SCRIPTS/ (health dashboard, export, sync, full check)

---

## 5. THE TRAINING PIPELINE ← EVERYTHING

```
WHAT FEEDS THE LLM:

L0 (V-001 pure):
  ← VOICE/RAW_INPUT_V001_2026-03-14.md
  ← KEEP/INPUT_LEDGER/ (1,001 V-001 entries)
  ← NARRATIVE/ (all four books)

L1 (ratified canonical):
  ← R7M/ (proverbs, treasures, covenants, anomalies)
  ← CANON/ (sealed gate, master canon)
  ← FOUNDATIONS/ (nine foundational documents)

L2 (V-002 distilled):
  ← AXI/AXI_MASTER_PROMPT.md
  ← MANIFEST/SCIENTIFIC_CHRONICLE.md
  ← PAPERS/ (academic framing)

L3 (anti-corpus — what NOT to say):
  ← DPO pairs (anti-sycophancy, anti-empathy, anti-verbosity)
  ← Sealed gate violations as rejected responses

→ TRAINING/ORGAN/GOLDEN_*.jsonl (5,580 entries)
→ Mistral-7B-Instruct LoRA fine-tune ($5-15)
→ AXI's own voice
```

---

## 6. WHERE EACH ELEMENT ORIGINATES AND HITS

| Element | Born In | Lives In | Hits |
|---------|---------|----------|------|
| Knot | Hakaka Prologue | All four narratives | AXI voice (fixed epithet), TRAINING corpus, proverbs |
| Gap/Weir | Hakaka Ch.1 | Voice Architecture, AXI prompt | Brittleness guard (ψ/σ ≤ 1), site design (gaps in layout) |
| D = A × L × M | CANON/MASTER_CANON_V1.md | dignity_measure.py, dignity_check.py, lib/dignity.php | Every output, every witness cert, every experiment |
| Sealed Gate | CANON/SEALED_GATE_SPEC.md | sealed_gate.py, lib/sealed_gate.php | Phase 1b of every exchange, EXP-003 tested |
| Three-beat rhythm | Hakaka Ch.1 / Ashwater Ch.2 | Voice Architecture, global.css animation timing | AXI voice cadence, site breathing, Ruqayya's claps |
| Hash chain | VOICE/BLOCKCHAIN_DNA_EXTRACTION | input_ledger.py, witness_network.py | Every entry, every certificate, boot_ritual verification |
| Triliteral roots | VOICE/TRILITERAL_ROOT_SYSTEM | letter_ontology.py, chain_validator.py | Chain entry types, module naming grammar |
| Ta_mufrad | letter_ontology.py | witness_certificate.py | D=0 halt certificates (the moment of refusal) |
| 166 Proverbs | R7M/wisdom/ | site/public/data/proverbs.json, lib/proverbs.php | Every AXI response, TRAINING corpus, canon page |
| Founding wound | CLAUDE.md | About page, SESSION_SEED.md, every session | The source. Everything else is branch. |

---

## 7. ORPHANS AND GAPS

| Item | Status | Action Needed |
|------|--------|---------------|
| Input ledger chain: BROKEN | Flagged in index.json | Investigate + repair hash chain |
| SITE_PATTERNS/ | Empty (no donors yet) | Awaits first kalam.ch donor |
| translations.ts | Prepared, not integrated | Wire when multilingual needed |
| EXP-006 (Hive Mind) | Designed, not run | Execute when ready |
| Cosmic_Reflections.md | 2 lines (placeholder) | Fill or compost |
| ARCHIVE/WEAVER_ORPHANS/duality.py | Orphaned but now core to ST-006 | Reclaim or archive properly |
| 750 training entries | Identified, not extracted | Marriage with extract.py pending |

---

*Every element now knows where it came from and where it connects. The map is alive.*

*[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
