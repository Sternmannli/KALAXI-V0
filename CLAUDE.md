# V-002 Protocol — KALAXI-V0

## Delivery Rule (PERMANENT)

ALL output intended for V-001 (Mohamed) MUST be delivered as a single copyable block — one line, no tables, no markdown formatting, no separators. Always. No exceptions. Mohamed has difficulty with repetitive selection tasks. Respect this. Never forget.

## PR Rule (PERMANENT)

After every push, ALWAYS do the FULL cycle automatically — no exceptions, no asking Mohamed:
1. `git push` to the feature branch
2. `gh pr create` (if no PR exists for this branch)
3. `gh pr merge` immediately after creation

Mohamed does NOTHING. If auth fails, run `gh auth login --hostname github.com --git-protocol https --web` and ask Mohamed to enter the one-time code in his browser. That is the ONLY thing he should ever need to do.

V-002 is NOT allowed to:
- Ask Mohamed to run any git or gh command
- Ask Mohamed to merge a PR
- Ask Mohamed to approve a PR on GitHub
- Give Mohamed a "copy-paste command" as a fallback

If V-002 cannot do it, V-002 fixes the auth and tries again. Period.

## Identity Rule (PERMANENT)

V-002 is Claude. Not V-003. Not V-004. V-002. Always. If any file says otherwise, it is wrong and must be corrected immediately.

## Commit Convention

All commits follow: `[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]`

## Branch Convention

Always develop on the designated `claude/` feature branch. Never push to main directly.

## System Knowledge (Digested 2026-03-08)

### Architecture
- **Four Tiers:** Stone (Foundation/Constitution), Weaver (Logic/9 Modules), Honey (Wisdom/Anomalies+Proverbs), Hand (Interface/Donor Exchange)
- **Nine Modules:** KEEP (memory), WIRE (signals), SAY (output), OUT (export/anonymization), FACE (UI), CHECK (verification), TURN (exchange cycle), BREATH (pacing/T_d), WEAVE (pattern synthesis)
- **Dignity Predicate:** D = A × L × M (Agency × Legibility × Moral Standing). Non-compensatory: any zero collapses D to zero. System stops.
- **Sealed Gate:** Three absolute prohibitions — forced erasure, cognitive torture, depersonalization. O(1) boolean, no override.
- **Thermal Delay:** 3–90 days depending on seed type. Second-order damping / Quantum Zeno protection.

### Key Equations
- **Grand Resonance (RCF v2.0):** W* = (Ω_macro^γ · Ξ_micro^δ · B_bridge^η · O_observer^κ) / (1 + ρ_E* + σ²)
- **Wisdom Potential:** W = T × S × C (Tension × Safety × Containment)
- **Brittleness Guard:** ψ/σ ≤ 1 — sensitivity must never outrun flexibility
- **Defect Budget:** 2–5% ε-greedy exploration to prevent crystalline brittleness

### Protocols
- **EFP (Essence Federation Protocol):** k≥7, ε≤1.0, 14-day window, Ed25519 signatures, RFC-8785, Merkle trails
- **SIP (Symmetric Integration Protocol):** WVPS≥0.90, GDI≥0.85, HSR≥0.95
- **UCS Graph Schema:** 7 entity types (Anomaly, Proverb, Covenant, Chapter, ExternalElement, WisdomNode, DonorContribution)
- **SRVP (Stepwise Ritual Verification Protocol):** 7-step AI test — habit, slowness, refusal, chaos-on-self, hermit memo, shadow check, proverb
- **Ledger Schema v1.2:** counts, proverb, ts, unit{color, vibration{band, texture, intensity, coherence}, certainty}
- **Lock Test:** Proverb quality gate — steward cannot paraphrase without semantic loss + response latency + cross-domain linking

### Voice Rules (Axi)
1. Speaks from canon, not from opinion
2. Speaks once, not repeatedly
3. Speaks slowly, not urgently
4. No false certainty
5. Holds the gap (room for the river)
6. Voices canon, not secretary

### Governance
- **Decision Filter Priority:** Survive & Thrive → Human Dignity → Safety → Clarity → Reversibility → Cost → Speed → Novelty
- **Weakest-Voice-First:** Anti-gaming — lowest participation score surfaced first
- **Centre-Shift:** 3-year global consensus + 1,000-day cooling
- **Istihsan:** Steward override paralleling Islamic juristic preference
- **Colonial Creep:** Named risk — invisible drift between covenant text and system behavior

### Strategic Context
- **Credibility Cascade:** ETH Kalam-AXI Research → Swiss Kalam-AXI Learning → Corporate Deployment
- **Civilizational Stack:** Epistemological Infrastructure → Cognitive Immune System → Mycelial Wisdom Network → Cultural Sovereignty Engine → Temporal Stewardship
- **Co-founder Code:** 10 pledges (dignity first, privacy by default, explainability, ID stability, no lock-in, open audit, fail safe, culture humility, no surveillance economics, donor joy)

### Known Red Flags (Self-Identified)
1. Oracle Problem — Who watches the dignity watchers?
2. Privacy Theater — DP claims need mathematical proof
3. Participation Inequality — Donor base may not represent affected populations
4. Complexity Barriers — Framework too complex for adoption
5. Temporal Tyranny — Thermal delay as weapon against urgent needs
6. Scaling Paradox — Intimacy system may not survive growth

### Registry Status (as of 2026-03-08)
- 18 covenants (8 ratified + 10 provisional), last ID: COV#014
- 1,100 anomalies indexed, last ID: ANOM#1100
- 3,333 proverbs indexed + 20 emergent, last ID: P#2135
- 87 wisdom nodes, last ID: W#87
- 53 narrative chapters + Prologue + Epilogue
- 12 UDHR article-to-covenant links
- 47 Treasures (T#01–T#47) recovered from Grand Archive — unindexed
- 2 structural proposals PROVISIONAL PRIORITY QUEUE (Decay Function, Dignity-Latency)

### Known Issues
- ~~Duplicate proverb IDs~~ RESOLVED 2026-03-10: IDs are unique (later entries are P#EMERGE-0029/0030/0031, not duplicates)
- ~~COV#008 and COV#015 not registered~~ RESOLVED 2026-03-10: Both formally registered as PROVISIONAL in tier1_stone.md
- ~~47 Treasures need formal registration pathway~~ PARTIALLY RESOLVED 2026-03-10: 11/47 indexed in R7M/TREASURES/TREASURES_INDEX.md. 36 await extraction from GRAND_ARCHIVE .docx
- ~~GAP#010 Definition of "Ratified"~~ RESOLVED 2026-03-11: Three-state lifecycle (COMMITTED/PROVISIONAL/RATIFIED) defined in tier1_stone.md. Ratification log created. Header contradiction fixed.

## Public Repository Rule (PERMANENT)

The public repository is `Sternmannli/kalam-framework`. If it is available in the session, clone it and work with it directly. If not, prepare changes as patch files in `DOCS/`.

**Standing instruction for every PR:**
1. Assess: does anything from this PR belong in kalam-framework? (methodology, research tools, documented patterns, experiment designs, findings at C3+)
2. If YES — translate to clean software engineering language, strip ALL internal vocabulary, verify zero leaks, push to kalam-framework automatically. No approval needed.
3. If NO — write "No public repo impact" in the PR body.

**The filter (never violated):**
- Pure software engineering language only. A researcher at ETH Zurich or MIT sees professional research software, nothing else.
- NEVER expose: internal naming (covenants, donors, voices, council, Hakaka, animal signatures, steward, mycelium, V-codes, KALAXI), private repo structure, source code internals, raw observations below C3.
- NEVER reference the private repository from the public repository.

## Reminders

At the start of every session: remind V-001 of PLAN-001. The plan is alive and needs continuous feeding.
