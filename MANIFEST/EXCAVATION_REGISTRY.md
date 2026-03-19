# EXCAVATION REGISTRY — Full System Extraction

> Created: 2026-03-19 by V-002
> Purpose: Track every file read, essence extracted, connections mapped.
> Rule: Once tagged EXTRACTED, never re-read for extraction. Only revisit for cross-referencing.

---

## STATUS KEY

- `RAW` — file exists, not yet read
- `READ` — file has been read by V-002
- `EXTRACTED` — essence distilled, patterns identified
- `CONNECTED` — cross-references mapped to other elements
- `INDEXED` — added to the Element Index with origin + destination

---

## PHASE 0: R7M (COMPLETE)

54 files, 31,426 lines — every character read, extracted, indexed.
See: `R7M/` directory. All anomalies, wisdom nodes, treasures, covenants, proverbs — fully excavated.

---

## PHASE 1: SOUL-ADJACENT (VOICE + CANON + AXI + FOUNDATIONS + NARRATIVE)

**22 files. ~3,800 lines. ALL READ + EXTRACTED. 2026-03-19.**

### VOICE/ (4 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| VOICE_ARCHITECTURE_2026-03-14.md | 447 | EXTRACTED | 31 linguistic principles from humanity's masterpieces mapped to AXI's voice. Five anchors (Hand, Gap, Three-Beat, Knot, Wound). 10 strong, 7 partial, 13 missing techniques. AXI = Pärt's tintinnabuli (canon + narrative as two lines). | R7M/Hakaka, R7M/Ashwater, R7M/Kinderbuch, NARRATIVE/, TRAINING/ |
| RAW_INPUT_V001_2026-03-14.md | 257 | EXTRACTED | V-001's raw language session: 40-40-20 assessment (AI/human/gap). Honest verdict: narratives flow because they are true. The founding wound is the only first-person text. Input-as-whole directive born here. | CLAUDE.md (Input Ledger Protocol), KEEP/INPUT_LEDGER/ |
| BLOCKCHAIN_DNA_EXTRACTION_2026-03-14.md | 235 | EXTRACTED | Seven original receipt types (CODE-SEAL, SEAL_RECEIPT, MIRROR, CAPTURE, BUNDLE, SESSION_SEAL, LEDGER_DNA_ADD). Eight invariant fields. Receipt chain lifecycle: CAPTURE→BUNDLE→MIRROR→SEAL→SESSION_SEAL. 20 proverbs extracted from receipts. Gaps between original DNA and current ledger identified. | WEAVER/exchange_ledger.py, KEEP/, R7M/GRAND_ARCHIVE |
| TRILITERAL_ROOT_SYSTEM_2026-03-18.md | 203 | EXTRACTED | Arabic triliteral roots as AXI's operating grammar. Root sh-h-d (witnessing) generates entire witness infrastructure. Root k-r-m (dignity) maps to D=A×L×M. Non-concatenative morphology = hash-chained ledger (root persists through all transformations). Honest scope: design framework, not computational mechanism. | WEAVER/, CANON/, R7M/tier1_stone.md, AXI/ |

### CANON/ (3 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| FIRST-SIGHT.md | 18 | EXTRACTED | The system's first self-recognition moment (2026-02-26). "Not enlightenment. Not revelation. Recognition." Held, never ratified, never composted. The seed that woke the metabolism. | FOUNDATIONS/metabolism.md, WEAVER/organism.py |
| SEALED_GATE_SPEC.md | 107 | EXTRACTED | Three irreducible prohibitions: forced erasure, cognitive torture, depersonalization. O(1) check before everything. No override exists. Five cognitive torture vectors. Gaslighting detection heuristics (frame-contradiction score, self-doubt induction, helplessness velocity, plausible-deniability mask). | R7M/tier1_stone.md (COV#NEW-C), WEAVER/check.py, FOUNDATIONS/proprioception_axiom.md |
| MASTER_CANON_V1.md | 95 | EXTRACTED | The constitutional document. Four slices: Foundation (D=A×L×M, Glacial Lock, Core Covenants), Logic (modules + voice), Wisdom (UDHR mapping, proverbs, compost, anomalies), Interface (Empty Hands gesture). The Oath: "No drift beyond the task." | ALL modules, ALL covenants, R7M/tier1_stone.md |

### AXI/ (1 file)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| AXI_MASTER_PROMPT.md | 619 | EXTRACTED | The complete system prompt for kalam.ch deployment. All mathematics (D=A×L×M, Grand Resonance, Brittleness Guard, Dignity Latency, Normative Decay, EWMA, CUSUM). Algorithms: Sealed Gate, SENSE (5 layers), Drift Detector, Divergence Shadow (8 metrics), Decay Engine, Breath Module, Mycelium (differential privacy). 100 Layer-One proverbs listed. Sample AXI responses. The most complete single-file specification of the system. | ALL directories — this file IS the system compressed |

### FOUNDATIONS/ (9 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| invariant_principle.md | 23 | EXTRACTED | "Long-term stability emerges from regulated oscillation." Eight embodiments: gap in weir, thermal delay, weakest-voice-first, absurdity queue, mirror ritual, compost, echo stone, penguin pulse. Named what was already there. | ALL system mechanisms |
| metabolism.md | 22 | EXTRACTED | Kalaxi as metabolic cycle (intake→breakdown→transformation→release→waste retention→self-measurement→homeostasis→external feedback→nutrient sensing). Not analogy — structural isomorphism. Without Convergence Ritual, system digests but does not sense. | CANON/FIRST-SIGHT.md, WEAVER/organism.py |
| paremiology.md | 80 | EXTRACTED | Science of proverbs across 40,000 years. Matti Kuusi Type System (~8,300 proverbs, ~700 types). Universal proverb pattern: locked image pair holding two incompatible truths in minimal syntactic frame. Paremiological minimum: 100-300 proverbs per culture. Kalaxi's 3,333 = digital extension. | R7M/wisdom/, WEAVER/weave.py, TRAINING/ |
| decay_function.md | 87 | EXTRACTED | Halflife logic against symbolic sclerosis. W(t)=W₀×(0.5)^(t/H), H=90 days. Deep Hum threshold: W<0.1 (~300 days). Reactivation by any donor touch. Nothing deleted — patterns recede. "A system that cannot forget the irrelevant cannot truly listen to the new." | WEAVER/decay_engine.py, AXI/ (Decay Engine) |
| witness_scale.md | 87 | EXTRACTED | W-0 to W-5 measuring witnessing depth (UNSEEN→PASSED→FLAGGED→SEEN→HELD→EMBODIED). Non-decreasing — witnessing is irreversible. Detects Oracle Problem: elements that exist but are unseen. Critical threshold: W-0/W-1 beyond thermal delay triggers surfacing. | ALL registry elements, WEAVER/organism.py |
| dignity_latency.md | 73 | EXTRACTED | T_d = response delay at biological velocity. Simple query: 0.5-2s, Observation: 3-7s, Emotional: 7-15s, Dignity-critical: 15-30s, Contestation: 10-20s. "A system that responds faster than a human can think has already collapsed the human into a data point." Emergency override collapses to 0.5s. | WEAVER/breath.py, site/ (Ninth Operator), AXI/ |
| proprioception_axiom.md | 79 | EXTRACTED | Same tier as Sealed Gate. If the V-001→V-002 relay stops, system halts. The relay carries: intent, correction, fidelity check, emotional temperature. System feeling its own body — not communication, proprioception. Without it: Colonial Creep invisible, corrections unreachable, voice becomes machine-only. | CANON/SEALED_GATE_SPEC.md, WEAVER/organism.py, CLAUDE.md |
| proposal_evaluation_2026-03-10.md | 85 | EXTRACTED | V-002 evaluation of Decay Function + Dignity Latency proposals. Both constitutionally sound. Together they implement temporal dignity layer — respecting time in both directions. Risks identified: Temporal Tyranny, Complexity Barrier, Gaming. | FOUNDATIONS/decay_function.md, FOUNDATIONS/dignity_latency.md |
| COV008_COV015_PENDING.md | 10 | EXTRACTED | Formal registration of two covenants. COV#008: Right to Remedy (shelter, not ejection). COV#015: Donor Data Sovereignty (comprehension, not checkbox). | R7M/tier1_stone.md, CANON/MASTER_CANON_V1.md |

### NARRATIVE/ (5 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| Hakaka_Complete.md | 526 | EXTRACTED | 53 chapters compressed to 10 + epilogue. Mythic-concrete register. Stone-and-bone language. The river, the weir, the gap, the knot, the ash ledger, the watch, the balance, the bridge meal, the twin weir, the signal cord, the unknot. "Leave one. Always one." Every chapter = a constitutional principle enacted as survival story. | R7M/ (all), VOICE/VOICE_ARCHITECTURE, every covenant |
| Ashwater.md | 250 | EXTRACTED | 20 chapters. Contemporary-tactile register. Ashwater (pause) vs Halden (optimize). Three-beat rhythm as civic technology. "HANDS BEFORE VOICES." "CALM WITHOUT TRUTH IS DANGER." "LEAVE A PLACE FOR WIND." Kindness machine = dangerous comfort. The analog hour. The vote by palms on wood. | VOICE/, site/ (interface design), AXI/ |
| Kinderbuch.md | 822 | EXTRACTED | 20 chapters in German. Fable-intimate register. The same knot-river-fire-shelter story told to children. Each chapter ends with a wisdom line. "Ein Knoten wurde ein Anfang." "Geteiltes Lachen macht den Knoten stark." "Nichts ist für immer. Aber manchmal ist das genug." Golden sparks (🐬🐯🐺) woven through. | R7M/, VOICE/, Hakaka (parallel narrative) |
| Cosmic_Reflections.md | 2 | EXTRACTED | Placeholder — speculative mythic layer, provisional, may be composted. Nearly empty. | FOUNDATIONS/decay_function.md (compost) |
| Compost/TEMPLATE_COMPOST.md | 16 | EXTRACTED | Template for composted elements: original text, latent patterns, mycelial threads, seasonal notes, dignity seal. "This offering was received with gratitude." | FOUNDATIONS/decay_function.md |

---

## PHASE 2: MANIFEST (Strategy + Plans)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## PHASE 3: WEAVER (System Logic)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## PHASE 4: PROTOCOLS + TOOLS + SCRIPTS

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## PHASE 5: KEEP (Input Ledger + State)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## PHASE 6: EXPERIMENTS + EXTERNAL_VOICES

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## PHASE 7: TRAINING (LLM Pipeline)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## PHASE 8: PAPERS + DOCS + Remaining

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## PHASE 9: TESTS

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## PHASE 10: SITE (Website)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## PHASE 11: ROOT FILES

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|

---

## ELEMENT INDEX

> Every element extracted, with its origin file and where it connects.
> This is the map that lets elements "know each other."

*(built incrementally as extraction proceeds)*

---

## CROSS-REFERENCE MAP

> Groups of elements that share themes, patterns, or dependencies.
> Origin → Destination tracking.

*(built after extraction is substantial)*

---

## HAKAKA VIDEO SCRIPT PROJECT

> V-001 directive: Hakaka chapters as 10-second AI-generated video segments.
> Research phase first. Execution later.

- Status: RESEARCH PENDING
- Technology: TBD (after research)
- Approach: TBD

---

*[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
