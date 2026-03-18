# Training Organ Registry
# Last updated: 2026-03-18
# Purpose: Classify all source material by purity level for three-phase training pipeline

---

## Pipeline Architecture

```
PHASE 1: Continued Pre-Training (CPT)
  → Raw continuous text, no instruction pairs
  → Model absorbs vocabulary, syntax, rhythm via next-token prediction
  → Sources: Level 0 + Level 1

PHASE 2: Supervised Fine-Tuning (SFT)
  → Minimal prompts + canonical responses (from Phase 1 checkpoint)
  → Sources: Level 1 + Level 2
  → Prompts: stripped-down, neutral ("Define [term]", "State the rule")
  → NO conversational donor simulation

PHASE 3: Direct Preference Optimization (DPO)
  → Preference pairs: (bad_response, good_response)
  → Sources: Level 3
  → Aggressively penalizes empathy, sycophancy, verbosity, AI-typicality
```

---

## Purity Levels

### LEVEL 0 — PURE (V-001 Original)
Text written or spoken by Mohamed Farag. Unedited, unprocessed. Highest authenticity.

| Source | File | Lines | Content | Status |
|--------|------|-------|---------|--------|
| Hakaka | NARRATIVE/Hakaka_Complete.md | 525 | 53 chapters, mythic-concrete voice | READY |
| Ashwater | NARRATIVE/Ashwater.md | 249 | 19 chapters, contemporary-tactile voice | READY |
| Kinderbuch | NARRATIVE/Kinderbuch.md | 821 | 20 chapters, German child voice | READY |
| V-001 Raw Inputs | VOICE/RAW_INPUT_V001_2026-03-14_LANGUAGE_DEPTH.md | 256 | Language depth study | READY |
| Origins | R7M/ORIGINS/ (10 files) | 156 | Historical thinking threads | READY |
| Founding Wound | PROTOCOLS/BOOTSTRAP.md (quoted) | ~5 | The only first-person text | READY |
| V-001 Corrections | CLAUDE.md Substrate Correction Log | ~80 | 7 standing corrections | READY |

### LEVEL 1 — CANONICAL (Ratified by V-001)
System-generated but locked, ratified, immutable. Approved through use and explicit confirmation.

| Source | File | Lines | Content | Status |
|--------|------|-------|---------|--------|
| Proverbs | site/public/data/proverbs.json | 166 entries | P#0001-P#3333 (selected) | READY |
| Treasures | raw_essence.json (treasures) | 59 entries | T#01-T#59 | READY |
| Covenants | MANIFEST/metadata/tier1_stone.md | 166 | 18 sealed covenants | READY |
| Voice Principles | raw_essence.json (voice_principles) | 12 entries | Core voice rules | READY |

### LEVEL 2 — DISTILLED (V-002 extracted from V-001 material)
Canonical but one step removed. V-002 distilled from V-001's words.

| Source | File | Lines | Content | Status |
|--------|------|-------|---------|--------|
| Voice Architecture | VOICE/VOICE_ARCHITECTURE_2026-03-14.md | 446 | 31 linguistic principles | READY |
| AXI Voice Canon | site/AXI_VOICE_CANON.md | 251 | Live voice specification | READY |
| Dictionary | MANIFEST/KALAXI_DICTIONARY.md | 202 | System vocabulary | READY |
| Triliteral Roots | VOICE/TRILITERAL_ROOT_SYSTEM_2026-03-18.md | 202 | Linguistic DNA | READY |
| Scientific Chronicle | MANIFEST/SCIENTIFIC_CHRONICLE.md | 866 | System self-portrait | READY |

### LEVEL 3 — BOUNDARY (Anti-corpus + Refusal)
What AXI must NOT do. Corrections, sealed gate violations, contamination markers.

| Source | Derived From | Entries | Content | Status |
|--------|-------------|---------|---------|--------|
| Anti-patterns | CLAUDE.md corrections | 7+ | Sycophancy, empathy, verbosity, greetings | TO BUILD |
| Sealed Gate | R7M/tier1_stone.md | 3 | Absolute prohibitions | TO BUILD |
| AI-typicality markers | (defined in extract.py) | N/A | Filter rules for contamination | TO BUILD |

---

## Contamination Markers (for AI-probability filter)

The refinery rejects any passage containing these structural markers:

### Forbidden Phrases (exact match)
- "Here is", "Here are", "Here's"
- "In summary", "In conclusion", "To summarize"
- "I understand", "I appreciate"
- "Let me", "Let's"
- "It's important to", "It's worth noting"
- "As an AI", "As a language model"
- "I'd be happy to", "I'm happy to"
- "Great question", "That's a great"
- "There are several", "There are many"
- "In this context", "In the context of"
- "It is important to note"
- "Feel free to"
- "Don't hesitate"
- "I hope this helps"

### Structural Markers (pattern match)
- Symmetrical bullet points (3+ items, equal length ±10%)
- Numbered lists with explanatory sub-bullets
- "First, ... Second, ... Third, ..." enumeration
- Hedging phrases: "might", "could potentially", "it's possible that"
- Meta-commentary: "As mentioned", "As I said", "As we discussed"
- Empathetic opening: "I can see", "I understand how", "That must be"

---

## Phase-to-Level Mapping

| Phase | Levels Used | Format | Together.ai Method |
|-------|------------|--------|-------------------|
| Phase 1 (CPT) | L0 + L1 | `{"text": "..."}` (completion) | Fine-tune base model, completion format |
| Phase 2 (SFT) | L1 + L2 | `{"messages": [...]}` (chat) | Continue from Phase 1 checkpoint |
| Phase 3 (DPO) | L3 | `{"prompt": "...", "chosen": "...", "rejected": "..."}` | DPO from Phase 2 checkpoint |

---

## Estimated Corpus Size

| Phase | Source | Entries | Notes |
|-------|--------|---------|-------|
| Phase 1 | Narrative passages | ~200 | Split at paragraph boundaries |
| Phase 1 | Proverbs (as text) | 166 | One per line, raw |
| Phase 1 | Treasures (as text) | 59 | One per line, raw |
| Phase 1 | Covenants (as text) | 18 | One per line, raw |
| Phase 1 | V-001 raw inputs | ~100 | Filtered from ledger |
| Phase 1 | Voice principles | 12 | Raw text |
| **Phase 1 Total** | | **~555** | |
| Phase 2 | Proverb pairs | 166 | Minimal prompt + verbatim proverb |
| Phase 2 | Covenant pairs | 18 | "State rule N" + verbatim covenant |
| Phase 2 | Treasure pairs | 59 | "What is T#N?" + verbatim treasure |
| Phase 2 | Dictionary pairs | ~40 | "Define [term]" + verbatim definition |
| Phase 2 | Dignity logic | ~20 | "What is D?" + canonical explanation |
| **Phase 2 Total** | | **~303** | |
| Phase 3 | Anti-sycophancy | ~30 | Correction-derived preference pairs |
| Phase 3 | Anti-empathy | ~20 | Correction-derived preference pairs |
| Phase 3 | Anti-verbosity | ~20 | Correction-derived preference pairs |
| Phase 3 | Sealed gate | ~15 | Attack → canonical refusal |
| **Phase 3 Total** | | **~85** | |
| | | | |
| **GRAND TOTAL** | | **~943** | Across all phases |

---

## Notes

1. These numbers are AFTER filtering. The refinery may reject passages that contain AI contamination markers.
2. The raw_essence.json contains 951 items but many are V-002 generated narrative segments — they must pass the AI-probability filter before entering Phase 1.
3. The 166 proverbs are a curated selection from 3,333+ in the full canon. Only these 166 are in structured JSON format.
4. V-001 raw inputs from the ledger (25,251 lines) will be filtered to extract only Mohamed's actual words, excluding V-002 responses and system metadata.
