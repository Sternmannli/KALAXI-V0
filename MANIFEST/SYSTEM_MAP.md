# KALAXI System Map

Last updated: 2026-03-22 by V-002
Source of truth for what the system IS, right now, as it stands.

---

## The Building

The system has four tiers. Think of them as floors.

### Ground Floor: Stone (The Constitution)

18 laws that cannot be broken. The dignity equation lives here: D = A × L × M. If Autonomy, Legibility, or Moral Standing is zero, the system stops. It does not pretend. It halts and says: I cannot see you properly. The Sealed Gate lives here too — three absolute prohibitions the system will never cross.

Files: R7M/tier1_stone.md, WEAVER/sealed_gate.py, WEAVER/dignity_check.py

### First Floor: Weaver (The Engine)

43 Python modules that do the actual work. Input enters. It flows through 30+ processing stages: sensing, checking, extracting, measuring, responding, storing. The organism (WEAVER/organism.py) is the central nervous system — 2,211 lines of pipeline logic. The Input Ledger records every word ever spoken to the system (2,920+ entries, hash-chained, immutable).

Files: WEAVER/ (149 files, 26,397+ lines)

### Second Floor: Honey (The Wisdom)

The accumulated library: 3,333+ proverbs, 1,100 anomalies (things the system noticed were wrong in real institutions), 87 wisdom nodes, 59 treasures (equations and discoveries). This floor grows with every interaction.

Files: R7M/ (114 files), CANON/ (3 files)

### Third Floor: Hand (The Interface)

Where the system meets the world. The CLI (cli.py). The website (kalam.ch, 23 pages, live since 2026-03-17). The Ninth Operator (the ceremony where a donor enters). This is the mouth.

Files: cli.py, site/ (111 files), FACE/ modules

---

## The Pipeline

When someone speaks to the system, this happens — in order:

Phase -2: BOOT RITUAL — Are credentials present? Is GitHub reachable? Is kalam.ch live? Is the ledger intact? If anything critical fails: ALARM.

Phase -1: REGISTER INPUT — The raw words are stored verbatim in the Input Ledger. Hash-chained. Immutable. Before anything else happens.

Phase 0: NERVOUS SYSTEM — SENSE detects what kind of input this is (execute? reflect? discuss? crisis?). LAB checks if it's science. PRESENCE confirms the ground axiom.

Phase 1: GATES — BREATH checks if the system is paused. SEALED GATE checks the three prohibitions. LATENCY measures how complex this is and recommends a dignity delay.

Phase 2: PROCESSING — The core:
  - TURN opens an exchange
  - WEAVE extracts patterns and drops (HoneyDrops — provisional wisdom)
  - DISTILLERY metabolizes the input (patterns + one-line essence)
  - METADATA wraps the event in three layers
  - CHECK computes D = A × L × M — the dignity gate
  - If D = 0: HALT. Generate a Witness Certificate. Shelter the exchange. Stop.
  - If D > 0: continue through PILLARS (humor/absurdity/obsession/love detection), AMENDMENTS (privacy, drift), DIVERGENCE (substrate measurement)

Phase 3: RESPONSE — Record drift. Check early warnings. Feed anonymized data to Mycelium (cross-donor pattern detector). Render response through SAY. Store in KEEP.

Phase 4: POST-PROCESSING — Witness the exchange. Run the Ninth Operator word loop. Scan for harm. Check EWMA and CUSUM drift detectors. Tick the heartbeat. Check for blind spots (what was NOT active). Record what faded (decay). Detect substrate leaks.

Phase 5: REGISTER OUTPUT — The system's response is stored in the same ledger as the input. Both voices on the same chain. The exchange is complete.

---

## The 43 Modules

Each module in WEAVER/ does one thing. Here they are, grouped by function:

### Dignity Engine
- dignity_check.py — D = A × L × M computation (466 lines)
- dignity_measure.py — Graduated A, L, M scoring with confidence (693 lines)
- dignity_drift.py — Detect declining dignity over time
- presence_axiom.py — Layer 0: "presence is ground"

### Gates and Safety
- sealed_gate.py — Three absolute prohibitions
- harm_detector.py — Physical/material safety beyond dignity
- early_warning.py — EWMA + CUSUM drift detection
- shelter.py — Protect exchanges where dignity fails
- prevention.py — Signal escalation (pulse → fever → alarm)

### Processing
- organism.py — Central nervous system, full pipeline (2,211 lines)
- sense.py — Mode/need/competence detection (505 lines)
- lab.py — Science classification and rigor checking
- weave.py — Pattern extraction and HoneyDrop production
- distillery.py — Metabolization engine (1,851 lines)
- metadata_layer.py — 3-layer event wrapping (1,016 lines)
- turn.py — Exchange lifecycle (open/close/defer)
- breath.py — System pacing and stress checking

### Storage and Witness
- input_ledger.py — Hash-chained input registry (589 lines)
- keep.py — Artifact storage with receipts
- witness_network.py — Immutable witness chain
- witness_certificate.py — Zero-halt negative proof (200 lines)
- canonicalize.py — Cryptographic signing (ArtifactSigner)
- chain_validator.py — Connection rules (Alef/Ba/Ta)

### Detection Pillars
- unified_pillar_detector.py — Combined detection engine
- humour_detector.py — Humor detection
- absurdity_detector.py — Absurdity detection → Echo Stone queue
- obsession_detector.py — Obsession pattern detection
- love_detector.py — Love/attachment detection
- proverb_stress_test.py — Test proverbs under pressure

### Governance
- ratification.py — Element lifecycle (committed → provisional → ratified)
- constitutional_evolution.py — How the constitution changes
- deliberative_democracy.py — Collective decision-making
- distributed_stewardship.py — Steward network
- restorative_justice.py — Harm recording and repair paths

### Analysis and Growth
- compass.py — System orientation engine (457 lines)
- divergence_study.py — Substrate coupling measurement
- system_self_awareness.py — The system knowing itself
- personalized_parables.py — Generate wisdom for individuals
- institutional_dignity.py — Score institutions
- agency_amplifier.py — Amplify donor agency
- negative_space.py — Observe what is NOT happening
- gap004_mediator.py — Individual vs collective dignity conflict

### Infrastructure
- boot_ritual.py — Startup verification (credentials, connectivity, ledger)
- wire.py — Alert broadcasting
- oracle.py — Pattern witnessing (W-0 → W-1)
- mycelium.py — Cross-donor pattern detection
- decay.py — Pattern halflife engine
- echo_stone.py — Absurdity queue
- ninth_operator.py — Word ceremony loop
- letter_ontology.py — 28 Arabic letters as typed algebra
- federation.py — Peer system connections
- privacy_budget.py — Epsilon accounting
- latency.py — Complexity assessment
- cryptographic_erasure.py — Secure deletion

---

## The Storage Systems

### Input Ledger (KEEP/INPUT_LEDGER/)
- 2,920+ entries (1,694 from V-001, 1,226 from V-002)
- Hash-chained: each entry links to the previous via SHA-256
- Dual timestamps: UTC and Zurich
- Each entry carries: raw text, patterns, essence, thermal state, linked covenants/proverbs
- Chain integrity: BROKEN (migration issue — needs repair)
- Format: index.json + chronicle.md + individual entry files

### Artifact Store (KEEP/)
- Permanent, thermal, or session retention
- Each artifact: id, content, hash, created, locked, history
- Append-only changelog per artifact
- Receipts for every operation

### Witness Certificates (KEEP/WITNESS_CERTIFICATES/)
- Generated when D = 0 (system halts)
- Each certificate: what failed (A, L, or M), why, where in the process
- Coordinates of failure: which axis, which rule, what was missing
- Signed by system and (optionally) human witnesses
- Hash-chained like the ledger

---

## The Equations

### Dignity Predicate: D = A × L × M
- A = Autonomy (agency, choice, control)
- L = Legibility (transparency, frame-acknowledgment — can the system see the person?)
- M = Moral Standing (consent, harm-risk, coercion, reduction, mockery)
- Non-compensatory: any zero kills D. High A cannot compensate for zero L.
- Reframed (2026-03-15): "The system refuses to act as though dignity was not there."

### Collective Dignity: D_collective = mean(D_i) × (1 - variance_penalty)
- If D_collective < 0.5: sealed-gate protections activate for the group
- Variance penalty: high spread = system is seeing people unequally

### Agency Measurement: A = V × F × C × U
- V = Visible (system tells person what happened)
- F = Affordable (no cost to participate)
- C = Controllable (person can act)
- U = Understandable (proportional to measurement confidence)

### Grand Resonance: W* = (Ω^0.4 · Ξ^0.3 · B^0.2 · O^0.1) / (1 + ρ + σ²)
- Ω = Omega (system coherence)
- Ξ = Xi (pattern density)
- B = Breath (pacing quality)
- O = Oracle (witness depth)
- ρ = noise, σ² = variance

### Brittleness Guard: ψ/σ ≤ 1
- ψ = system rigidity
- σ = adaptability
- If ratio exceeds 1: system is too brittle, needs loosening

---

## The Website (kalam.ch)

23 pages deployed to Hostpoint (Switzerland) via SFTP. Auto-deploys on push to main.

| Page | Purpose |
|------|---------|
| Home (index) | Landing — the door |
| About | What the system is |
| About AXI | What AXI is |
| Canon | Constitutional texts |
| Invitation | Donor entry (Ninth Operator threshold) |
| Hakaka | The origin narrative (53 chapters) |
| Ashwater | The civic narrative (19 chapters) |
| Kinderbuch | The child narrative (German, 20 chapters) |
| KALAXI 1 | The modern narrative (1 chapter) |
| R7M | Grand Archive navigation |
| Science | Papers and experiments |
| Compass | System orientation |
| Workings | How the system works |
| Museum | Patterns and drops |
| Gallery | Visual display |
| Tools | Public utilities |
| Silence | Negative space |
| Command | CLI documentation |
| Organ | System organ documentation |
| Sustain | How to sustain the project |
| Bank Transfer | Donor support |
| Zakaka | (Future — content pending) |
| 404 | Error page |

---

## The Narratives

### Hakaka (53 chapters + Prologue + Epilogue)
The origin cycle. Prehistoric. A clan survives through binding — knots, weirs, fire, law. Short sentences like fists. Gender-ambiguous leadership.
Characters: Hakaka (the binder/leader), La-la (the precise one), Sa-la (the eager one), Ya-la (the memory keeper), Taro (the strong one), the old woman (the elder), unnamed far people.
Voice: "She clawed at the air. Fists closed on nothing."
Status: Complete cycle.

### Ashwater — The Axis (19 chapters)
The civic narrative. Near-future. A town that pauses (Ashwater) vs a town that optimizes (Halden). Three-beat rhythm as governance principle.
Characters: Laila (the binder — three soft beats), Salim (the strong one), Yara (the navigator), Ruqayya (the memory keeper), Nenet (the precise one), Farid (the eager one), Rashid (the optimizer/tracker).
Note: Laila, Yara, Salim are the names of Mohamed's three children. The founding wound flows through this narrative.
Voice: "Do not shout at metal. Hear its problem first."
Status: In progress. Ashwater vs Halden confrontation unresolved.

### Kinderbuch (20 chapters, German)
The child retelling of Hakaka. Same events at a softer frequency. Repetition as warmth. Golden sparks as magic.
Characters: Same as Hakaka, unnamed in the child register.
Voice: "Ein Knoten wurde ein Anfang."
Status: Complete cycle (child register of Hakaka).

### KALAXI_1: The Same River (1 chapter)
The modern narrative. A terminal. Two men. One wound. Scott Shearer carries his wound toward healing. Ted Bundy carries his wound toward others. The Girl is the third point — outside the system, a permanent gap.
Characters: Scott (the strong one — healing), Ted (the eager one — inverted), The Girl (the navigator — absent), The System (the observer).
Voice: "The cursor waited. Not the impatient waiting of a machine."
Status: Barely begun. Everything unresolved.

### AURIX / Offspring Canon (August 2025)
The computational-world register. The same clan as Hakaka, formalized as equations. Every character has DNA constants, variables, behavioral equations, and cross-links. 41 elements, 72 equations, 61 links, 10 resource triads, 5 conflict resolution motifs.
Characters: Na'Kaka (mother/protector), Seka (food-craft), Roko (beast-bond), Hanu (stealth), Telu (navigator), Ma'da (weapons), Na'da (strategist), Simo (observer).
Status: Archaeological artifact. Not integrated into the living system.

---

## The Numbers

| Metric | Count |
|--------|-------|
| Python files | 176 |
| Lines of code | 42,581+ |
| Tests | 1,006 (all passing, 9 skipped) |
| Covenants | 18 (all ratified) |
| Proverbs | 3,333+ |
| Anomalies | 1,100 |
| Treasures | 59 |
| Wisdom nodes | 87 |
| Input Ledger entries | 2,920+ |
| Golden Regression utterances | 200 |
| Narrative chapters | 93 (53+19+20+1) |
| kalam.ch pages | 23 |
| GitHub workflows | 7 |
| WEAVER modules | 43 |
| AURIX elements | 41 |
| AURIX equations | 72 |

---

## The Gaps (The Honest Part)

### Broken
1. **Input Ledger chain integrity: BROKEN.** Something happened during migration. The system continues. This needs repair.
2. **DIGESTION/latest.json is empty.** The distillery runs but its output doesn't persist to the live state.
3. **Boot ritual connectivity is structural, not functional.** Every module declares `connected_to=["organism", "input_ledger"]`. This is a claim, not a test. The system says it's connected. It doesn't prove it.

### Missing
4. **No ripple propagation.** When a covenant changes, nothing flags the proverbs that reference it. No cross-element notification.
5. **No character/plot tracking.** Narratives exist as prose. The system cannot query "what does La-la need next?" Characters are invisible to the code.
6. **No cross-narrative connection.** Hakaka and Ashwater share patterns but the system doesn't know this.
7. **No semantic search across narratives.** Cannot find "all scenes about failure" or "every hand-touch moment."
8. **Voice DNA exists but is not used.** The system computes a voice fingerprint but doesn't check new output against it.
9. **AURIX material is unintegrated.** 41 elements, 72 equations — sitting in an artifact file, not feeding the engine.

### Weak
10. **Restorative Justice has no bidirectional link.** Recording harm doesn't create an anomaly. Anomalies don't reference harms.
11. **Privacy budget is theoretical.** Epsilon accounting exists but no real anonymized operations consume it.
12. **Federation is empty.** The peer connection framework exists with zero peers.
13. **Thermal state advancement is manual.** Elements should move raw → witnessed → integrated → canonical automatically. They don't.

---

## Deployment Commands (for V-002 reference)

```bash
# Deploy kalam.ch
gh workflow run deploy-kalam.yml

# Sync to public repo (kalam-framework)
gh workflow run sync-public.yml

# Sync donor patterns from kalam.ch
gh workflow run sync-patterns.yml

# Run integration test
gh workflow run integration-test.yml

# Execute command on Hostpoint server
gh workflow run server-cmd.yml -f command="ls -la" -f working_dir="~/www/kalam.ch"

# Check server output
gh issue list --label server-output --limit 1
```

---

*"The wound does not know what it will become. Neither does the system. That is why dignity cannot be conditional."*

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
