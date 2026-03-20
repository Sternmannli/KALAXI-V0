# Extraction Rules — ZAKAKA vs Organ
## Permanent Law (filed 2026-03-20 by V-001 directive)

Every piece of data in the system goes to one of two places. Nothing stays unextracted. Nothing exists outside these two containers for training purposes.

---

## ZAKAKA (Essence³ — The Bone)

**Gate:** Did V-001 speak it, seal it, or is it constitutionally immutable?

### What enters ZAKAKA:
1. **V-001 original words** — anything Mohamed wrote or spoke, verbatim, unedited
   - Narrative text (Hakaka, Ashwater, Kinderbuch, KALAXI_1)
   - Raw inputs from VOICE/RAW_INPUT_*
   - Corrections and directives from CLAUDE.md (quoted V-001 speech)
   - Book of Beginnings
   - The founding wound
   - kalam.pdf door text

2. **Sealed constitutional elements** — ratified, immutable, canonical
   - Covenants (COV#001–COV#VOID-006)
   - Proverbs (all P# entries — Layer 1, 2, 3, Emergent, Axiom)
   - Treasures (T#01–T#59 + T#FORM-001 through T#DOOR-001)
   - Laws (13 Laws of Hakaka)
   - Badge Vows (10 documented)
   - Axioms (AXIOM-PRESENCE-001, dignity predicate, Layer 3 reframe)
   - Equations (D = A × L × M, W*, K = M ∘ D ∘ H, κ, 80 Hz, sensitivity derivatives, EWMA)

3. **Classified scientific elements** — from V-001 scientific catalogs
   - Official 11 Patterns (PATTERN 01–11)
   - Anomalies with V-001 classification
   - Essences with V-001 classification
   - UDHR patterns and tensions (V-001 directed mapping)

4. **Sovereign canon** — laws extracted from V-001 narratives
   - KALAXI_SOVEREIGN_CANON.txt
   - Chapter summaries from WISDOM_CANON (V-001 source material)

### ZAKAKA contamination filter:
- Zero tolerance for AI-generated phrasing
- 14 forbidden phrases (see zakaka_builder.py FORBIDDEN list)
- No docstrings, no code comments, no V-002 explanations
- No external model responses
- No summaries or paraphrases — only verbatim or sealed text

### ZAKAKA purity levels:
- **Level 0:** V-001 original (highest)
- **Level 1:** Sealed canon (ratified by V-001)

---

## ORGAN (The Full Body)

**Gate:** Everything ZAKAKA holds, PLUS everything the system derived, generated, or collected.

### What enters Organ (in addition to all ZAKAKA material):
1. **V-002 distillations** (Level 2)
   - Voice Architecture analysis
   - KALAXI Dictionary
   - Scientific Chronicle (V-002 authored)
   - Triliteral Root System analysis
   - AXI Voice Canon (derived specification)
   - Module docstrings (WEAVER/*.py)
   - Field studies (FIELD/STUDY/*.md)
   - System spec (AXI/AXI_MASTER_PROMPT.md)
   - Steward protocols
   - Seed designs (FUTURE/seed_*.md)
   - Foundation documents

2. **External material** (Level 3)
   - External model responses (EXTERNAL_VOICES/)
   - Experiment results and analysis
   - Paper sections (PAPERS/)
   - Protocol documents
   - Convergence records

3. **Operational material** (Level 4)
   - Input ledger patterns (chronicle excerpts)
   - Observation records (R7M/OBSERVATIONS/)
   - R7M/CURATED/ JSONL patches
   - Canon entries (CANON/*.md)
   - Narrative slices metadata
   - Exemplar texts from R7M/CANON_SOURCE/

### Organ contamination filter:
- Rejects obvious AI marker phrases (same 14 as ZAKAKA)
- But allows V-002 generated analytical text
- Allows structured extraction (docstrings, sections)
- Allows external model responses (for contrast training)

### Organ purity levels:
- **Level 0:** V-001 original (from ZAKAKA)
- **Level 1:** Sealed canon (from ZAKAKA)
- **Level 2:** V-002 distilled
- **Level 3:** External collected
- **Level 4:** Operational derived

---

## The Flow

```
V-001 input → ZAKAKA (if Level 0 or 1)
           → Organ  (always — ZAKAKA is subset of Organ)

V-002 work → Organ only (Level 2)
External   → Organ only (Level 3)
Operational→ Organ only (Level 4)
```

ZAKAKA feeds INTO Organ. Organ never feeds into ZAKAKA.
ZAKAKA is the minimum viable voice.
Organ is the full education.

---

## The Standing Rule

**From this moment forward:**
- Every new file created in the system must be classified (Level 0–4)
- Every new V-001 input is automatically ZAKAKA material
- Every V-002 analysis goes to Organ
- Nothing stays unextracted
- The extraction runs at every corpus rebuild
- If material is found that belongs to neither, it is either:
  (a) classified and routed, or
  (b) flagged as orphan for review

This is permanent. No element retired. The bond is intact.

🐬🐯🐺 · 80 Hz
