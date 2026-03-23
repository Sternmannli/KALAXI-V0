# Narrative Spine — Controlled Vocabularies

## Transition Types

Used in `PRESSURE.json` field `desired_transition`. Describes what kind of scene change is needed.

| Value | Meaning |
|-------|---------|
| `confrontation_into_repair` | Open conflict must be acknowledged and restored |
| `failure_into_insight` | A mistake must produce understanding |
| `distance_into_contact` | Separated parties must meet |
| `silence_into_witness` | Something unspoken must be seen |
| `scarcity_into_coordination` | Lack must produce cooperation |
| `conflict_into_pause` | Escalation must be interrupted by deliberate stillness |
| `absence_into_recognition` | What is missing must be acknowledged |
| `pressure_into_release` | Accumulated tension must discharge safely |
| `confusion_into_precision` | Ambiguity must sharpen into clarity |
| `stasis_into_movement` | A stuck situation must shift |

## Pressure Modes

Used in `PRESSURE.json` field `pressure_mode`. Describes what kind of response the narrative demands.

| Value | Meaning |
|-------|---------|
| `continuation` | The story needs more — another scene, another chapter |
| `repair` | Harm has been done; restoration is needed |
| `witness` | Something must be seen, not fixed |
| `silence` | The right response is to hold, not act |
| `interruption` | The current trajectory must be broken |
| `echo` | A pattern from another story wants to repeat here |

## Instance Status

Used in `INSTANCES.json` field `status`.

| Value | Meaning |
|-------|---------|
| `present` | Active in the narrative, scenes exist |
| `latent` | Exists but underdeveloped, few or no dedicated scenes |
| `void` | Structural absence — exerts pressure through non-presence |

## Wound Status

Used in `INSTANCES.json` field `current_state.wounds.status`.

| Value | Meaning |
|-------|---------|
| `open` | Active, unresolved |
| `healing` | Being processed, partially resolved |
| `resolved` | Addressed in prose, no longer generating pressure |
| `integrated` | Wound became part of the character's strength |
| `structural` | Cannot be resolved — it IS the architecture |

## Strata Coupling Relationships

Used in `STRATA.json` field `coupling[].relationship`.

Free-text descriptions. Common patterns:
- "co-determine survival" (COHESION ↔ PROVISION)
- "adversarial" (CONCEALMENT ↔ PERCEPTION)
- "inversely related" (SIGNAL ↔ CONCEALMENT)
- "enables" (NAVIGATION → MOVEMENT)
- "precedes" (PERCEPTION → REPAIR)
- "regulates" (RELEASE → HIERARCHY)
- "strengthens" (RELEASE → COHESION)
- "consumes" (SHELTER → PROVISION)

## Pressure Breakdown Components

Used in `PRESSURE.json` field `breakdown`. All values 0.0–1.0.

| Field | Meaning |
|-------|---------|
| `unresolved_bonds` | Characters with open relational gaps |
| `tension_integral` | Accumulated tension without release |
| `arc_debt` | Promises, foreshadowing not yet paid |
| `scene_starvation` | Characters absent too long |
| `missing_strata` | Behavioral laws not yet expressed in this story |
| `echo_potential` | Patterns resolved elsewhere wanting repetition here |
