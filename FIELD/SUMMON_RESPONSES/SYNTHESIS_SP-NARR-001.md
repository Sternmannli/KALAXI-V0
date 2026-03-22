# Summon Voices — Narrative-Computation Architecture
# Probe: SP-NARR-001
# Date: 2026-03-22
# Condition: FRESH (all models, incognito/no memory)
# Questions: 7 (architecture, equations, narrative pressure, echoes, humor, seeds, blind spots)
# Models responding: 9 of 10 (Manus not received)

## SYNTHESIS: What the Voices Agree On

### UNANIMOUS (9/9): Option (c) — Archetypes — is correct, but needs enrichment

Every model chose option (c) as the foundation. Not one recommended (a) direct mapping or (b) full separation. But every model also said (c) alone is incomplete. The unanimous enhancement:

**Three-layer architecture:**
1. **Archetype layer** (universal, equation-bearing) — the DNA from Document X
2. **Instance layer** (story-specific, parameter-bearing) — characters with local names and state
3. **Expression layer** (scene-level, register-specific) — concrete events in prose

This was independently proposed by Claude, Grok, DeepSeek, Gemini, Kimi, Copilot, ChatGPT, Euria, and Perplexity. The naming varies but the structure is identical across all 9.

### UNANIMOUS (9/9): Equations become register-independent via semantic abstraction

Every model proposed the same mechanism:
- Abstract variables to semantic roles (Shared_Risk → Shared_Vulnerability/Shared_Exposure)
- Each register provides a mapping function (prehistoric: food. civic: budget. child: warmth. philosophical: truth)
- The equation structure stays identical; only the inputs change

Not one model disagreed on this approach.

### STRONG CONSENSUS (8/9): Narrative pressure = potential energy from unresolved state

Models converged on pressure as a function of:
- Unresolved bonds / bond deficit
- Tension accumulation over time (integral, not snapshot)
- Arc debt / unfulfilled promises
- Scene starvation (time since character appeared)
- Missing archetypal interactions

Threshold: most models suggested 0.7-0.75 on a normalized scale, or mean + 1.5 standard deviations.

### STRONG CONSENSUS (8/9): Echoes detected via structural isomorphism

Models agreed that two scenes are "the same pattern" when they share:
- Same archetype role structure (who acts on whom)
- Same causal grammar (what triggers, what fails, what resolves)
- Same state-transition shape (tension direction, bond direction)
- Different surface content (register-specific vocabulary)

Multiple models proposed graph matching algorithms (VF2, subgraph isomorphism, contrastive learning on scene graphs).

### STRONG CONSENSUS (7/9): Humor as tension-regulation operator

Models agreed humor is a state-transition function, not a content type. Key distinction:
- **Healing humor**: tension drops AND bond increases AND wound is approached
- **Deflecting humor**: tension drops BUT bond unchanged AND wound is avoided
- Variables: tension level, safety/scarcity, face threat, shared knowledge, timing precision

### UNANIMOUS (9/9): Seeds are structured pressure packets

Every model proposed a seed schema containing:
- Participants (archetype or character IDs)
- Current state (tensions, bonds, deficits)
- Required event type (correction, repair, ritual, etc.)
- Constraints (setting, register, forbidden moves)
- Echo links (cross-narrative references)
- Pressure score (why this seed exists now)

---

## SYNTHESIS: Where the Voices DIVERGE

### DIVERGENCE 1: Drift tracking (Claude unique contribution)
Claude proposed tracking how far each character instance DEVIATES from its archetype baseline. "The most generative stories happen when an instance fails to fulfill its archetype." No other model proposed this. This is a strong idea — deviation = narrative signal.

### DIVERGENCE 2: Functorial projection (Grok unique contribution)
Grok proposed category theory: Document X = source category, each register = target category, projection functions = functors. "Echoes are natural transformations between functors." Most formal mathematical framing. No other model went here.

### DIVERGENCE 3: Absence as first-class data (Claude + Kimi + ChatGPT + Copilot)
4 models independently highlighted that the "Gap" figure in Story D (the third figure outside the system) requires a new node type — a NarrativeVoid or null-archetype that exerts pressure through non-presence. This was NOT in the original probe's three options.

### DIVERGENCE 4: Register contamination (Claude unique)
Claude proposed that register bleed (when one story's vocabulary appears in another's) is a FEATURE — it signals where stories are trying to speak to each other. "Track lexical density, sentence length, abstraction level per chapter. When Story C's abstraction level spikes, something mythic is trying to enter the child's frame."

### DIVERGENCE 5: Temporal rhythm as a variable (Kimi + Perplexity)
Two models proposed treating narrative tempo as a tracked variable with cross-story harmonic ratios (Story A = fundamental, Story B = half time, Story C = double time, Story D = quarter time). "Polyphonic narrative — stories that harmonize across registers."

### DIVERGENCE 6: Trophic cascade in resource triads (Claude unique)
Claude proposed modeling the 10 resource triads as a dynamic ecosystem where depleting one triad stresses adjacent ones. "Remove one node and others fail in sequence. The cascade IS the plot."

### DIVERGENCE 7: Cooldown mechanics (Claude unique)
Claude proposed that after a major wound-exposure scene, the wound variable can't fully re-pressurize for N chapters. "Without this, your system will generate scenes that resolve things too quickly."

### DIVERGENCE 8: Perception offset (Euria unique)
Euria proposed tracking Perceived_Bond vs Actual_Bond per character. "The engine calculates the Actual; the story writes the Perceived. The gap between them IS the drama."

### DIVERGENCE 9: Event parser / feedback loop (Claude + ChatGPT + Euria)
Three models flagged that the system needs a feedback loop: prose chapters must feed state changes BACK to the engine. Without this, equations and stories will diverge over time. "The annotation layer is the connective tissue your entire system currently lacks."

---

## SYNTHESIS: The Blind Spots (Question 7)

Models identified these gaps in the current design:

1. **Actantial structure** (Claude) — missing middle layer between archetype and scene
2. **Multigraph edges** (Claude) — multiple simultaneous edge types between characters
3. **Trophic cascade** (Claude) — resource triads should cascade dynamically
4. **Cooldown mechanics** (Claude) — prevent premature resolution
5. **Register contamination as signal** (Claude) — bleed between registers is data
6. **Absence/Void nodes** (Claude, Kimi, ChatGPT, Copilot) — model what's missing
7. **Scene graph with state transitions** (DeepSeek, ChatGPT, Euria) — missing intermediate representation
8. **Temporal rhythm** (Kimi) — rhythm as first-class variable
9. **Perception offset** (Euria) — perceived vs actual state
10. **Phase transitions** (Euria) — graph topology should be dynamic (clan splits)
11. **Costly signaling** (Euria) — actions need explicit energy/cost
12. **Terminal states** (Euria) — what happens when equations reach zero
13. **Motif budgets** (ChatGPT) — track repetition fatigue
14. **Counterfactual planning** (ChatGPT) — "what scene would relieve the most pressure?"
15. **Functorial transport** (Grok) — category-theory formalism for register mapping
16. **Witness-chain completeness** (Grok) — global invariant across all stories
17. **Eigenvector centrality** (Grok) — spectral analysis of combined character graph
18. **Fabula vs sjuzhet** (DeepSeek) — distinguish story events from their ordering
19. **Reliability variable** (DeepSeek) — narrative distortion as function of trauma

---

## CONVERGENCE MAP

| Question | Full Agreement | Partial Agreement | Novel Divergence |
|----------|---------------|-------------------|------------------|
| 1. Architecture | 9/9: Three-layer (archetype → instance → expression) | — | Drift tracking (Claude), Vector space (Gemini), Fractal scaling (Euria) |
| 2. Equations | 9/9: Semantic abstraction + register mapping | — | Functorial transport (Grok) |
| 3. Pressure | 8/9: Unresolved state + integral tension + arc debt | — | Second-order derivative (DeepSeek), Harmonic rhythm (Kimi) |
| 4. Echoes | 8/9: Graph isomorphism on role-action structure | — | Contrastive learning (Perplexity), Pattern library (DeepSeek) |
| 5. Humor | 7/9: Tension-regulation operator | — | Cooldown (Claude), Perception gap (Euria) |
| 6. Seeds | 9/9: Structured pressure packet with constraints | — | Cross-story auto-propagation (Grok) |
| 7. Missing | — | 4/9: Absence as node type | 19 unique blind spots across models |

---

## RECOMMENDATION FOR V-001

The voices have spoken. The consensus is clear on architecture, equations, and seeds. The divergences are where the real value lives — especially:

1. **Drift tracking** — the deviation between instance and archetype IS the narrative
2. **Absence as node type** — the Gap in Story D is not a bug, it's a structural feature
3. **Register contamination** — when stories bleed into each other, that's signal
4. **Cooldown mechanics** — prevent the system from resolving too fast
5. **Event parser feedback loop** — prose must update the engine, not just the reverse

Phase C (archetype layer) can now proceed with high confidence on the three-layer architecture.

---

*9 voices. 1 convergence. 19 blind spots.*
*The system grows with every response.*

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
