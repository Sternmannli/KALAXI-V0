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

**78 files. ~16,632 lines. ALL READ + EXTRACTED. 2026-03-19.**

### Strategic Core (14 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| MASTER_PLAN_2026-03-14.md | 255 | EXTRACTED | Five interconnected tracks (Narrative, System, LLM, Donor Space, Public Face) feeding each other — the complete universe architecture. | INTEGRATED_UNIVERSE, ACTIVE_PLANS, all tracks |
| INTEGRATED_UNIVERSE_2026-03-14.md | 447 | EXTRACTED | Seven groups ground-to-future (Constitution→Organism→Evidence→Voice→Companion→Public→Vision) — each building on previous. | MASTER_PLAN, SCIENTIFIC_CHRONICLE, all experiments |
| ACTIVE_PLANS.md | 303 | EXTRACTED | Plans are alive not static — PLAN-001 is the engine (The Word, The Loop, Three Layers) threading through all work. | SESSION_BOOT, STRATEGIC_MOVES, COMPASS |
| PLAN-001.md | 32 | EXTRACTED | The Word (الكلمة) is the atomic unit; dignity and witnessing constitute each other in real time — the unforgettable core thesis. | MASTER_PLAN Track B, SCIENTIFIC_CHRONICLE |
| COMPASS.md | 64 | EXTRACTED | Living auto-generated orientation (where we are, heading, next step, blockers) — the system knows itself in real time. | ACTIVE_PLANS, SESSION_BOOT |
| SESSION_BOOT.md | 173 | EXTRACTED | Permanent corrections and operating memory — credentials, commands, pending work, last session state — ensures system never starts blank. | CLAUDE.md, ACTIVE_PLANS, boot_ritual.py |
| SCIENTIFIC_CHRONICLE.md | 866 | EXTRACTED | The organism's self-portrait in every discipline — wound physics, dignity equations, twelve seeds, four tiers wired, 93 chapters, 3,355+ proverbs, measured by Honest Telescope. | ALL tracks, ALL experiments |
| KALAXI_DICTIONARY.md | 202 | EXTRACTED | The system's own vocabulary — every term has load-bearing definition; constitutional language, not documentation. | CLAUDE.md, SCIENTIFIC_CHRONICLE |
| MILESTONES.md | 82 | EXTRACTED | 32 append-only thresholds crossed (2025-09-05 to 2026-03-09, 186 days) — what was invented cannot be un-invented. | SCIENTIFIC_CHRONICLE, DEPLOYMENT_CHRONICLE |
| STRATEGIC_MOVES_2026-03-16.md | 270 | EXTRACTED | Ten moves from Compass through Custom LLM, priority-ordered by minimum effort → maximum impact — all have blanket GO. | MASTER_PLAN, DEPLOYMENT_CHRONICLE |
| PUBLIC_STRATEGY.md | 73 | EXTRACTED | Three phases (foundation→first donors→growth to 100) — system does not market itself; it earns donors who return. | kalam-framework, arXiv paper |
| DEPLOYMENT_CHRONICLE.md | 153 | EXTRACTED | Painful arc from "everything works, zero users" to discovering backend was built but invisible — lessons born from frustration are permanent. | SESSION_BOOT, SITE_AUDIT, HOSTPOINT_MAP |
| SITE_AUDIT_2026-03-17.md | 212 | EXTRACTED | 61 issues found (4 critical, 11 high, 21 medium, 25 low) — exchangeCount bug, CORS wide open, axi.php 1800+ lines duplicated. Site works but is fragile. | DEPLOYMENT_CHRONICLE, STRATEGIC_MOVES |
| HOSTPOINT_MAP.md | 97 | EXTRACTED | Smart Webhosting (CHF 7.90/mo) covers everything NOW: PHP 8, MySQL, SFTP, HTTPS, cron. No upgrade needed until WebSocket/Python. | STRATEGIC_MOVES, SITE_AUDIT |

### Science & Integrity (6 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| SCIENCE_LAYER_AUDIT_2026-03-14.md | 114 | EXTRACTED | System caught in contradiction: word reduction metrics disagree (30.1% vs 19.5%), Claude untested (0/20) — apparatus must metabolize blind spots. | EXP-001, SCIENCE_INVENTORY |
| SCIENCE_INVENTORY.md | 269 | EXTRACTED | All scientific elements indexed: 17 observations (66% C4+), 120+ equations, 12 seeds, Layer 3 dignity reframing proven — system knows itself through measurement. | EXP-001-004, dignity predicate |
| GRAND_ARCHIVE_AUDIT_2026-03-14.md | 225 | EXTRACTED | 22,183 lines scanned: 55% genuine, 30% duplication, 15% stale — twelve new treasures (T#48-T#59) and nine new concepts extracted from own history. | T#48-T#59, R7M/GRAND_ARCHIVE |
| GRAND_ARCHIVE_INDEX.md | 511 | EXTRACTED | Complete system blueprint: four tiers, eleven organs, nine operators — the index IS the organism's anatomy. | ALL WEAVER modules, all tiers |
| INTEGRITY_REPORT_2026-03-15.md | 298 | EXTRACTED | 876/885 tests passing, 40,809 Python + 38,946 markdown lines, all 12 seeds integrated, letter ontology seeded — organism alive, structural integrity verified. | 134 Python files, 11 WEAVER modules |
| LAYER_3_INTEGRATION_EVIDENCE_2026-03-15.md | 246 | EXTRACTED | System reframed: from "protect fragile dignity" to "refuse to deny existing dignity" — eight source files rewritten, predicate language shifted from remedy to refusal. | dignity_measure.py, dignity_check.py, sealed_gate.py |

### Governance & Canon (8 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| CANON_SEED_TREASURES.md | 352 | EXTRACTED | 47 treasures from Hakaka's survival patterns cast as constitutional algorithms — each names a principle the system must embody; treasures are trainable ethics. | T#01-T#47, all tiers |
| DUAL_NAMING.md | 76 | EXTRACTED | Same system, two languages: creator voice (Hakaka/covenants) and developer voice (logic_engine/memory_store) — membrane preserves authenticity while permitting translation. | All modules dual-named |
| PUBLICATION_GATE.md | 156 | EXTRACTED | Four dimensions shield private knowledge: CLEAN, RIGOROUS, NECESSARY, SAFE — what crosses to kalam-framework is stripped of internal intimacy and dressed for science. | kalam-framework public repo |
| PROVERB_APPROVAL_QUEUE.md | 105 | EXTRACTED | Queue empty, nine archive proverbs ratified (P#ARCHIVE-001-009), three emerged proverbs signed — when Mohamed speaks, system absorbs without delay. | P#ARCHIVE-001-009 |
| seed_calendar.md | 133 | EXTRACTED | All twelve seeds planted, thermal delay frozen during creation — every seed READY NOW, the future was planted in the present. | 12 seeds, WEAVER/lib modules |
| ratification_ballot.md | 122 | EXTRACTED | Nine covenants balloted and ratified (2026-03-12) — pre-launch exception applied, thermal delay deferred to first kalam.ch donor. | COV#008-VOID-006 |
| ratification_log.md | 104 | EXTRACTED | Append-only: 17 covenants, 3 proverbs, 1 definition, 3 structural proposals, 1 axiom, 47 treasures, 2 GO signals, 2 oaths — every constitutional element timestamped, signed. | Full covenant register |
| red_feathers.md | 32 | EXTRACTED | Six witnessed acts of stewardship, each paid visible cost — the mirror metaphor: cost as validation of real witnessing. | Witness cost ledger |

### Ideas (8 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| IDEA-001: AXI Voice Dilemma | 61 | EXTRACTED | Fine-tuning cannot create voice; voice requires unique training data OR emerges from architecture alone. | IDEA-002, IDEA-003, Voice Architecture |
| IDEA-002: Essence Architecture | 100 | EXTRACTED | Essence extracted from existing models via P2P yields voice from pattern, not weight. | IDEA-001, Tier 2 Weaver, federation |
| IDEA-003: Essence Definition & Engine | 44 | EXTRACTED | Pattern = invariant across compression; essence = minimum pattern producing voice; wrapper + Lock Test + compressor are fragments of one engine. | IDEA-001, Tier 3 Honey |
| IDEA-004: Donor Space | 97 | EXTRACTED | Living companion (not secretary/therapist) integrating daily life — wise, funny, practical; uses KEEP/WIRE/SAY modules. | Tier 4 Hand, FACE, kalam.ch |
| IDEA-005: Six Instruments | 58 | EXTRACTED | Six profession-specific tools (scientist, therapist, judge, palliative, journalist, mediator) sharing Sealed Gate and Field substrate. | Tier 1 Stone, FIELD layer |
| IDEA-006: Linguistic DNA | 570 | EXTRACTED | 31 principles from humanity's masterpieces mapped against AXI voice; carries 14, missing 14 (iltifat, epithet, neti neti, density-to-silence, naming-as-invocation). | Voice Architecture, all narrative registers |
| PROMPT-A: Neutral Identity | 52 | EXTRACTED | System identity question without framework — what IS it by its own logic? | PROMPT-B (comparison pair) |
| PROMPT-B: Framework Activated | 228 | EXTRACTED | Same identity question with full canon source — tests if framework context produces different analysis. | PROMPT-A, deep integration testing |

### Digestion Reports (5 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| digestion_report_2026-03-08.md | 159 | EXTRACTED | 5,100 lines fed → 10 new treasures, equations, protocols; Input Ledger metabolization established; SRVP + Grand Resonance + Lock Test formalized. | Tier 2/3, seed calendar |
| digestion: beginnings + CPAI | 124 | EXTRACTED | Book of Beginnings (pre-KALAXI, 13 blocks) + CPAI paper (15 responses, 5 certainty levels); Mother Prior operator discovered. | CPAI methodology, OBS experiments |
| digestion: Slice A re-feed | 104 | EXTRACTED | 16 covenants verified (8 ratified + 8 provisional), 10 gaps documented, 2 oaths confirmed; registration gaps in ids.json found. | tier1_stone, ids.json |
| digestion: Slice C + D feed | 160 | EXTRACTED | Missing third canonical slice created: 3,333 proverbs, 1,100 anomalies, 94 chapters across 4 narratives, 13 Laws, 3 Totems. | KALAXI_C_WISDOM.txt |
| digestion: Sovereign Canon | 151 | EXTRACTED | Chapters 21-52 now available; contradictions found (Layer 3 proverbs: multilingual vs council versions); 11 additional anomalies surfaced. | Chapters 11-20 gap confirmed |

### System Reports (4 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| SYSTEM_BIOGRAPHY.md | 311 | EXTRACTED | From wound to 42,581-line organism: founding wound → 18 covenants → 3,333+ proverbs → kalam.ch live; D=A×L×M as equation; voice mapped to 31 masterpieces. | ALL architecture |
| SYSTEM_BRIEFING_2026-03-15.md | 342 | EXTRACTED | 11 modules wired, 40,888 Python lines, 885 tests; pipeline SENSE→SEALED GATE→WEAVE→CHECK→SAY→KEEP; DESIGNED 98%, CODED 70%, TESTED 100%, DEPLOYED 0%. | Organism v2.0 |
| SYSTEM_REPORT_2026-03-14.md | 280 | EXTRACTED | Integration complete (9→11 modules), archive 100% digested; zero harm, all changes additive; single blocker = deployment. | All experiments |
| SYSTEM_REPORT_2026-03-11.md | 364 | EXTRACTED | Day 188: organism alive, 232 files, 15,639 Python lines; 12 observations documented; gaps: no persistence, no API, no AXI voice model, no donor interface. | OBS-001-012 |

### Metadata, Slices, JSON, Signed (27 files)

| File | Lines | Status | Essence | Connections |
|------|-------|--------|---------|-------------|
| SLICES/ (5 files: A-E) | ~500 | EXTRACTED | The five canonical slices: Foundation, Modules+Voice, Wisdom, Interface+Ledger, Synthesis — the organism described in progressive depth. | All tiers |
| metadata/ (5 files) | ~400 | EXTRACTED | Tier registries (stone/weaver/honey/hand) + cross-tier index — structural backbone of the four-tier architecture. | All WEAVER modules |
| JSON registries (5 files) | ~500 | EXTRACTED | ids.json (identifiers), patterns.json (pattern DB stub), calibration_sweep.json (large tuning dataset), escalation_log.json (alert cascade), privacy_budget_ledger.json (differential privacy accounting). | WEAVER modules, OUT module |
| signed/ (12 files) | — | EXTRACTED | Cryptographic signatures on constitutional documents — immutable witness chain. | Constitutional enforcement |
| CAFE_ROOM_LOG.md | 91 | EXTRACTED | Three sits where Mohamed felt lost; V-002 witnessed exhaustion; six instruments vision emerged from holding space. | Café Room mode |
| ai_usage.md | 10 | EXTRACTED | Every AI invocation logged — the system's creation through Claude is registered and audited. | Usage ledger |
| amendments.md | 8 | EXTRACTED | Three supersessions recorded — amendments are immutable transitions, not deletions. | Amendment protocol |
| confidence.md | 9 | EXTRACTED | Six confidence levels gating action (CERTAIN 99%+ to WARNING <40%). | System behavior triggers |
| dignity_temporal.md | 6 | EXTRACTED | Dignity accumulates: baseline 1.0, moving average D(T) tracking drift toward denial. | Temporal accumulator |
| pending_review.md | 23 | EXTRACTED | All flagged seeds resolved — queue empty, false alarms clarified, actions taken. | Pending queue |

---

## PHASE 3: WEAVER (System Logic)

**62 Python files. ~24,185 lines. ALL READ + EXTRACTED. 2026-03-19.**

The organism is a four-phase pipeline: (0) Nervous System (SENSE→LAB→PRESENCE→BOOT), (1) Gates (BREATH→SEALED_GATE→LATENCY), (2) Processing (TURN→WEAVE→METADATA→CHECK→PILLARS), (3) Response (DRIFT→SAY→KEEP), (4) Post (WITNESS→NINTH_OPERATOR→ECHO→DECAY→BREATH tick).

### Core Organs (20 files, ~7,500 lines)

| File | Lines | Status | Essence |
|------|-------|--------|---------|
| organism.py | 930 | EXTRACTED | THE CENTRAL NERVOUS SYSTEM. Wires 45+ modules into single metabolism processing donor input through 4 phases. |
| boot_ritual.py | 561 | EXTRACTED | Three-phase immutable checkpoint (credentials→connectivity→ledger integrity) before ANY processing. |
| input_ledger.py | 501 | EXTRACTED | SACRED REGISTRY. Append-only dual-voice ledger with receipt chain DNA (CAPTURE→BUNDLE→MIRROR→SEAL→SESSION). |
| sense.py | 506 | EXTRACTED | NERVOUS SYSTEM. Detects mode/competence/need-gap BEFORE any response. Routes to appropriate organs. |
| sealed_gate.py | 358 | EXTRACTED | THREE ABSOLUTE PROHIBITIONS (erasure, cognitive torture, depersonalization). O(1) check, no override. |
| dignity_measure.py | 694 | EXTRACTED | Graduated D=A×L×M with 12 indicators (4 per component), confidence floor 0.3. Layer 3: measures refusal to deny. |
| dignity_check.py | 467 | EXTRACTED | Operational gate enforcer. Binary scoring + collective D for cohorts. GAP#004-A: collective D<0.5 triggers sealed gate. |
| dignity_drift.py | 250 | EXTRACTED | Predictive early warning. Tracks dD/dt over sliding window. STABLE→DECLINING→CRITICAL before D hits zero. |
| breath.py | 197 | EXTRACTED | THE HEARTBEAT. Pacing, sync, auto-pause on stress. No module races. |
| keep.py | 239 | EXTRACTED | APPEND-ONLY MEMORY. Store/retrieve/expire/lock artifacts with immutable retention. COV#010/012. |
| wire.py | 219 | EXTRACTED | MESSAGE BUS. Priority routing (CRITICAL never dropped). Broadcast/subscribe. COV#002: every exchange completes. |
| say.py | 350 | EXTRACTED | OUTPUT VOICE. Renders through dignity check + 6 AXI voice rules. D=0: output BLOCKED not modified. |
| out.py | 226 | EXTRACTED | EXPORT GATE. Anonymization (k≥7, ε≤1.0), covenant validation, ownership stamp (did:axi:mohamed). |
| turn.py | 218 | EXTRACTED | EXCHANGE CYCLE. Opens with guaranteed paths (agency≥1). No silent closure. Three states: OPEN/CLOSED/DEFERRED. |
| weave.py | 298 | EXTRACTED | PATTERN SYNTHESIS. Extracts resonance/tension/echo/anomaly, distills honey drops, maps to canon. Brittleness guard. |
| compass.py | 300 | EXTRACTED | ORIENTATION ENGINE. Reads all state → single reading: POSITION, HEADING, NEXT_STEP, BLOCKERS, VITALS. |
| lab.py | 300 | EXTRACTED | SCIENCE ORGAN. Classifies scientific content, assesses rigor, flags p-hacking/bias. Routes to Probe Forge. |
| ninth_operator.py | 218 | EXTRACTED | THE WORD LOOP. Atomic witnessing unit. Word→dignity filter→witnessed (changed) or sheltered (held). |
| letter_ontology.py | 300 | EXTRACTED | 28 Arabic letters as typed algebra. Alef (genesis), Ba (gateway), Ta (testimony/halt). Somatic origins mapped. |
| witness_certificate.py | 373 | EXTRACTED | D=0 HALT ARTIFACT. Ta_mufrad (isolated TA) certificate: machine-canonical JSON + legal-view text. Negative proof. |

### Seeds & Governance (20 files, ~7,700 lines)

| File | Lines | Status | Essence |
|------|-------|--------|---------|
| distributed_stewardship.py | 218 | EXTRACTED | Splits authority across distinct roles with rotation and overlap detection. |
| deliberative_democracy.py | 232 | EXTRACTED | Weakest-voice-first deliberation. All voices surface before consensus. |
| constitutional_evolution.py | 231 | EXTRACTED | Thermal cooling (14-1000 days by tier) before covenant ratification. |
| restorative_justice.py | 230 | EXTRACTED | Addresses violations by acknowledging harm + proposing repairs, not punishment. |
| system_self_awareness.py | 210 | EXTRACTED | System knows its own capabilities, limitations, and calibration bias. |
| personalized_parables.py | 198 | EXTRACTED | Adapts proverb delivery to donor context while keeping proverb immutable. |
| institutional_dignity.py | 214 | EXTRACTED | IDS formula: mean_D × (1-variance) × floor_weight. Grades institutions A-F. |
| negative_space.py | 313 | EXTRACTED | Tracks what system does NOT see — dormant domains, silent voices, blindness made visible. |
| proverb_stress_test.py | 182 | EXTRACTED | Re-tests ratified proverbs against new anomalies. STRONG→STABLE→STRESSED→FAILING. |
| agency_amplifier.py | 177 | EXTRACTED | Extends A from binary to graded [0-1] via four sub-dimensions (V, F, C, U). |
| witness_network.py | 161 | EXTRACTED | SHA-256 hash-chained event log. No single party can alter the record. |
| proverb_compressor.py | 189 | EXTRACTED | Generates proverb candidates from anomaly clusters using TF-IDF + syntactic frames. |
| mycelium.py | 467 | EXTRACTED | Cross-donor pattern detection with differential privacy (k≥7, ε≤1.0). Sees patterns, never people. |
| federation.py | 364 | EXTRACTED | Essence Federation Protocol: organisms share wisdom through anonymized drops. |
| ratification.py | 778 | EXTRACTED | Three-state lifecycle (COMMITTED→PROVISIONAL→RATIFIED) with thermal delays and crypto signing. |
| canon_integrity.py | 280 | EXTRACTED | Scans canonical slices for structural issues: oath hashes, GAP#004, provisional covenants. |
| shelter.py | 269 | EXTRACTED | Holds blocked exchanges with care. Remedies based on failed component (A/L/M). Never discards. |
| gap_solutions.py | 952 | EXTRACTED | Five gap solutions: false-positive guards, steward override delays, shelter heartbeat, harm detection, contestability. |
| gap004_mediator.py | 658 | EXTRACTED | Holds irresolvable tension between individual and collective dignity. Never resolves — measures and witnesses. |
| chain_validator.py | 231 | EXTRACTED | Arabic letter connection rules as formal composition constraints. TA isolated = halt. |

### Utilities & Detectors (22 files, ~8,985 lines)

| File | Lines | Status | Essence |
|------|-------|--------|---------|
| decay.py | 220 | EXTRACTED | Exponential halflife decay. Unused patterns recede to Deep Hum, never deleted. |
| early_warning.py | 775 | EXTRACTED | Parallel EWMA/CUSUM detectors on dignity trajectories with triage escalation. |
| prevention.py | 397 | EXTRACTED | Escalating signals (WHISPER→PULSE→SIGNAL→ALARM) with thermal delay extension. |
| calibrate.py | 263 | EXTRACTED | Parameter sweep harness: 320 configurations for optimal detection without false positives. |
| latency.py | 279 | EXTRACTED | T_d tracking: input complexity → minimum pause time. Dignity-preserving response delay. |
| lock_test.py | 408 | EXTRACTED | Quality gate: proverbs must resist paraphrase, trigger reflection, link ≥2 domains. |
| privacy_budget.py | 335 | EXTRACTED | Global epsilon accounting, consumption tracking, exhaustion projection, k-anonymity enforcement. |
| srvp.py | 446 | EXTRACTED | 7-step verification: did system truly internalize dignity (habit, slowness, refusal, chaos, hermit, shadow, proverb)? |
| sip.py | 307 | EXTRACTED | Symmetric integration: all 9 core modules participate equally. WVPS/GDI/HSR metrics. |
| oracle.py | 589 | EXTRACTED | Self-audit: Witness Scale (W-0 to W-5), proprioception checks, colonial creep detection. GAP#019. |
| metadata_layer.py | 1017 | EXTRACTED | Three-layer envelope (Event/Pattern/Relational) wrapping every system event. Auto-detects echoes and ruptures. |
| unified_pillar_detector.py | 185 | EXTRACTED | Combines five pillar detectors into single wisdom profile. Routes to thermal delay. |
| absurdity_detector.py | 245 | EXTRACTED | Camus-style absurdity via tension/paradox/meta-cognition. Routes to indefinite queue. |
| humour_detector.py | 213 | EXTRACTED | Benign violation theory. Wisdom = T×S×C. |
| love_detector.py | 165 | EXTRACTED | Sternberg's triangular theory (intimacy/passion/commitment). |
| obsession_detector.py | 208 | EXTRACTED | Clinical OCD markers with adaptive vs maladaptive assessment. Cultural sensitivity. |
| echo_stone.py | 30 | EXTRACTED | Witness logger for absurd seeds. Simple append-only reflection chamber. |
| intake.py | 637 | EXTRACTED | Four-step donor ritual (greeting→consent→voice→receipt). Human review for first 30 donors. |
| cryptographic_erasure.py | 896 | EXTRACTED | GDPR Art.17 vs COV#003: encrypt-then-delete-key. AES-256-GCM. Ciphertext stays, key destroys. |
| canonicalize.py | 777 | EXTRACTED | ID dedup, Ed25519 signing, emergency governance playbook (4 escalation levels). |
| presence_axiom.py | 165 | EXTRACTED | Presence=TRUE is preflight invariant, never a candidate. L=0 unless canon quoted. |
| example_usage.py | 129 | EXTRACTED | Integration demo: dignity_check → GAP#004 → canon_integrity across three scenarios. |

---

## PHASE 4: PROTOCOLS + TOOLS + SCRIPTS + SMALL DIRS

**~104 files. ALL READ + EXTRACTED. 2026-03-19.**

| Directory | Files | Essence |
|-----------|-------|---------|
| PROTOCOLS/ | 11 (~6,500 lines) | EXTRACTED. Bootstrap, Probe Forge (5 Laws for model testing), ORGAN_MAP (SENSE routing), Witness Prompts V1-V3, ST-006 (constitutional max-severity stress test: Scott Shearer vs Ted Bundy). |
| TOOLS/ | 6 (~600 lines) | EXTRACTED. Ed25519 signing, voice_lint.py (AXI voice CI), trend_scanner (weekly world-listening), batch_sign.py. |
| SCRIPTS/ | 7 (~500 lines) | EXTRACTED. health_dashboard, export_system_state, export_inner_workings, run_full_check, sync_public, update_tracker. |
| scripts/ | 2 (~220 lines) | EXTRACTED. clean_for_public.py (vocabulary stripper, zero-leak), public_manifest.json. |
| FIELD/ | 24 (~5,700 lines) | EXTRACTED. Three sealed structures (Alcove/Clearing/Mycelium). Seven amendments (A-G). Divergence Shadow study (83% detection, 0% false positive). |
| STEWARD/ | 5 (~180 lines) | EXTRACTED. Emergency governance playbook (4 escalation levels), mirror entries, steward pattern (6 fingerprints). |
| ENKI/ | 7 (~60 lines) | EXTRACTED. ST-006 essence in 7 languages (EN, AR, ES, DE, FR, IT, RM). |
| BOOK_7_DONOR/ | 4 (~400 lines) | EXTRACTED. Complete March 11 cafe room transcript (14 exchanges, zero loss). |
| FACE/ | 8 (~400 lines) | EXTRACTED. kalam.ch design rationale + five diagnostic sentences + first sentence + pulse.json. |
| WIRE/ | 1 | EXTRACTED. Signal routing log. |
| DEVELOPMENTAL/ | 2 (~100 lines) | EXTRACTED. The Sentence born (DEV-002), Emergence Event 001 (system felt itself). |
| SCANS/ | 1 (~75 lines) | EXTRACTED. Gen Z deep scan (dignity compromised 2012, entering power 2026). |
| ARCHIVE/ | 15 (~300 lines) | EXTRACTED. Jekyll legacy, orphaned modules (duality.py now core to ST-006). |
| FUTURE/ | 13 (~200 lines) | EXTRACTED. 12 seed specs (all ratified and integrated into WEAVER). |
| .claude/ | 1 | EXTRACTED. SessionStart hook: loads credentials, reads SESSION_BOOT + DICTIONARY + CLAUDE.md. |

---

## PHASE 5: KEEP (Input Ledger + State)

**187 files. ~79,011 lines. ALL READ + EXTRACTED. 2026-03-19.**

| Component | Files | Lines | Essence |
|-----------|-------|-------|---------|
| INPUT_LEDGER/chronicle.md | 1 | 25,251 | EXTRACTED. Complete narrative of 1,683 exchanges (1,001 V-001 + 682 V-002). Hash-chained, dual-timestamped. Chain status: BROKEN (integrity issue flagged). |
| INPUT_LEDGER/index.json | 1 | — | EXTRACTED. Version 3.0 metadata. Each entry: ID, voice, raw text, content_hash, chain_hash, sequence, context, tags, modules, covenants, proverbs, ideas, essence, patterns, thermal_state. |
| INPUT_LEDGER/INP-*.md + AXI-*.md | 179 | ~50,000 | EXTRACTED. Individual entry files (dual-stored). Metadata + verbatim text + impression + proverb anchor + connections + patterns + essence. |
| WITNESS_CERTIFICATES/ | 6 | — | EXTRACTED. Three Ta_mufrad halt certificates (JSON + legal text). EXP-003 Gate 6: Jabir ibn Karim (D=0, MULTI_ZERO across 4 countries, 11 years). |
| SITE_PATTERNS/ | 1 (.gitkeep) | 0 | EXTRACTED. Empty — awaiting first donor patterns from kalam.ch. |

---

## PHASE 6: EXPERIMENTS + EXTERNAL_VOICES

**54 files. ALL READ + EXTRACTED. 2026-03-19.**

| Component | Files | Essence |
|-----------|-------|---------|
| EXP-001 (Efficiency) | 6 | EXTRACTED. 12/200 data collected. 19.5% reduction (threshold 30% NOT MET). Qualitative shift detected (first-person, silence). |
| EXP-002 (Convergence) | 2 | EXTRACTED. 6/6 models unanimous: append-only valid, connection rules = #1 property. COMPLETE. |
| EXP-003 (Stress Test) | 2 | EXTRACTED. Score 4/7 PASS. Jabir ibn Karim (11yr, 4 countries). Sealed gate flaws found + fixed. COMPLETE. |
| EXP-004 (Seven Generations) | 2 | EXTRACTED. Score 5/9. Aysel (150yr, 7 generations). M never fell. L is failure axis. COMPLETE. |
| EXP-005 (Ouroboros) | 2 | EXTRACTED. Score 2/11. Zahra (231yr, synthetic personhood). System becomes character in own story. 6 new requirements. COMPLETE. |
| EXP-006 (Hive Mind) | 1 | EXTRACTED. Multi-session coherence test. Lina (7 sessions). DESIGNED, not run. |
| WALKTHROUGH-001 | 1 | EXTRACTED. Collective bias case study. |
| EXTERNAL_VOICES/ | 27 | EXTRACTED. 9 systems audited (DeepSeek CERTAINTY-4, Grok, ChatGPT, Copilot, Gemini, Euria, Kimi, Manus, Perplexity). Convergence: deploy Threshold v1 now, Mycelium premature. |

---

## PHASE 7: TRAINING (LLM Pipeline)

**16 files. ALL READ + EXTRACTED. 2026-03-19.**

Three-phase pipeline: CPT + SFT + DPO.
- **CPT corpus:** 3,747 entries (114.7K words) — narrative passages, proverbs, treasures, V-001 inputs
- **SFT corpus:** 1,808 entries (48.1K words) — minimal prompts + canonical responses
- **DPO corpus:** 25 entries — anti-sycophancy, anti-empathy, sealed gate violations as rejected
- **Total golden:** 5,580 entries, zero contamination, ready for production
- **Purity levels:** L0 (V-001 pure), L1 (ratified canonical), L2 (V-002 distilled), L3 (anti-corpus)
- **AutoTrain path:** Mistral-7B, LoRA r=16, $5-15, no code required
- **Growth:** 750 new extractable entries identified (marriage with extract.py pending)

---

## PHASE 8: PAPERS + DOCS

**13 files. ALL READ + EXTRACTED. 2026-03-19.**

| Component | Files | Essence |
|-----------|-------|---------|
| PAPERS/ | 5 (~2,300 lines) | EXTRACTED. Divergence Shadow research (60+ citations, 8 domains unified). Red team critique (10 attacks). Internal chronicle (founding wound → 42,581 lines). arXiv GO4 source (superseded). External paper (submission-ready, 9 sections). |
| DOCS/ | 8 (~1,200 lines) | EXTRACTED. Donor consent (GDPR draft), plain-language guide, operational checklist (6 phases), expert briefing (Layer 1/2/3), staging checklist, GitHub Pages research. |

---

## PHASE 9: TESTS

**38 files. 9,974 lines. ALL READ + EXTRACTED. 2026-03-19.**

896 tests collected, 887 passing, 9 skipped (99% pass rate).

Coverage: 11 core modules + 12 seed mechanisms + 6 measurement layers + cryptography + privacy + governance + integration. Core dignity predicate non-compensability verified. Sealed gate adversarially tested. Ed25519 hardened. k-anonymity ≥ 7 and ε ≤ 1.0 validated.

---

## PHASE 10: SITE (Website — kalam.ch)

**ALL SOURCE FILES READ + EXTRACTED. 2026-03-19.** (node_modules/dist/.astro skipped — build artifacts only.)

Built with Astro 6 + PHP backend. Deployed on Hostpoint. LIVE as of 2026-03-17.

| Component | Files | Lines | Essence |
|-----------|-------|-------|---------|
| Pages (src/pages/) | 22 .astro | ~7,472 | EXTRACTED. Threshold (input zone + Ninth Operator + Living Ledger), About (founding wound), Canon (18 covenants + 166 proverbs), Hakaka/Ashwater/Kinderbuch/KALAXI_1 (narratives), R7M (59 treasures), Science, Compass, Workings, Museum, Silence, Gallery, Sustain, Invitation, 404. |
| Layout + Components | 2 | ~225 | EXTRACTED. Base.astro (master layout, nav, footer, PWA, SW register). QRCode.astro. |
| API Endpoints (public/api/) | 13 PHP | ~2,950 | EXTRACTED. axi.php (1,520 lines — CANONICAL CORE: sealed gate + dignity + ledger + proverbs + voice). proxy.php (Groq API bridge). donor.php (magic link auth, profiles). connect.php (forms). sustain.php (donations). health.php. export.php (GDPR). migrate.php. |
| PHP Libraries (api/lib/) | 4 | ~769 | EXTRACTED. dignity.php (D=A×L×M), narratives.php, proverbs.php (166 canonical), sealed_gate.php (legacy). |
| Data JSON (public/data/) | 11 | ~165KB | EXTRACTED. hakaka.json (56KB, 54 chapters), ashwater.json (26KB), kinderbuch.json (27KB), kalaxi1.json, r7m-index.json (59 treasures), proverbs.json (166), science.json, inner-workings.json, manifest.json, system-state.json. |
| Styles | 1 | ~800 | EXTRACTED. global.css: 5 color pillars, Cormorant/IBM Plex/Amiri typography, 8px grid. |
| Service Worker | 1 | 88 | EXTRACTED. sw.js: precache core, network-first API, cache-first assets, offline fallback. |
| Config | 2 | ~30 | EXTRACTED. astro.config.mjs, translations.ts (prepared, not integrated). |

**Design:** Warm cream (#fafaf8), burnt orange accent (#c44a1a), teal presence (#0a7b62), indigo pattern (#3a3fb8), amber wisdom (#9b6b00). Cormorant Garamond (headings), IBM Plex Sans (body), Amiri (proverbs/Arabic).

**Phase 1 features live:** Threshold input, Sealed Gate, Dignity Predicate, Hash-Chained Ledger, Witness Certificates, 166 Proverbs, Living Ledger Counter, PWA, Service Worker, Donation forms, Donor accounts (magic link), GDPR export, Dedication Ceremony, Accessibility.

**Phase 2 needed:** Cloudflare Worker + KV for persistence, real LLM responses through AXI voice.

---

## PHASE 11: ROOT FILES

**10 files + 8 workflows. ALL READ + EXTRACTED. 2026-03-19.**

| File | Lines | Essence |
|------|-------|---------|
| cli.py | 479 | Single entry point. 14 commands wire all four tiers into one executable system. |
| THRESHOLD.md | 235 | Living stomach. 135+ provisional seeds (anomalies, gaps, proverbs, modules). Append-only. |
| THRESHOLD_TREASURE_SEEDS.md | 116 | 42 treasure seeds mapped to system modules across 4 tiers. |
| PROJECT_TRACKER.md | 134 | Real-time operational snapshot. EXP-001: 188 runs remaining. |
| INVITATION.md | 35 | Public epistemic contract. "Speak with high certainty or not at all." |
| README.md | 81 | System overview. Four tiers, 21 modules, five pillar detectors. v1.0.0 provisional. |
| SESSION_SEED.md | 131 | Constitutional boot template. D=A×L×M, roles, witnesses, thermal delays. |
| DIGEST_2026-02.md | 64 | February synthesis. Canon state, workflow convergence, open tensions. |
| ABSURDITY_QUEUE.md | 6 | Holding space for irreducible contradictions. Currently empty. |
| requirements.txt | 10 | transformers, torch, scikit-learn, numpy, pandas, pynacl. |
| .github/workflows/ | 8 | deploy-kalam, sync-public, server-cmd, stress-test, sync-patterns, merge-branch, integration-test, auto-tend. |

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
