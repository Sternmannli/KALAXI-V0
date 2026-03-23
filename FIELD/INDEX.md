# FIELD — Brain

The living instrument. Where research happens in real time. Currently holds three different concerns that share infrastructure but serve different purposes.

## Three Concerns

### 1. Summon Infrastructure (how we probe other models)
| Component | Purpose |
|-----------|---------|
| `summon_package.py` | Package management — creates and registers probe packages |
| `summon_runner.py` | One-step execution — tells V-001 what to paste where |
| `SUMMON_PACKAGES/` | Five probe packages (SP-001 OPEN, SP-002 PRESENCE, SP-003 LAYER-HELP, SP-004 LAYER-SAFE, SP-005 LAYER-INTEL) |
| `SUMMON_PACKAGES/index.json` | Package registry |
| `SUMMON_RESPONSES/` | Synthesized responses |
| `ALCOVE/` | Raw response storage (SP-002 has 10 responses from 5 models × 2 conditions) |
| `ALCOVE/shadow_genome.py` | Shadow genome analysis of raw responses |

**Connection:** Feeds `SCIENCE/` (experiment data), feeds `EXTERNAL_VOICES/` (filed responses), feeds `TRAINING/` (chosen/rejected pairs for DPO).

### 2. Study Infrastructure (research in progress)
| Component | Purpose |
|-----------|---------|
| `STUDY/divergence_study.py` | Divergence shadow analysis engine |
| `STUDY/DIVERGENCE_SHADOW_STUDY.md` | Divergence research document |
| `STUDY/ANTHROPIC_EFFECT_MEASUREMENT.md` | Substrate bias measurement protocol |
| `STUDY/ANTHROPIC_EFFECT_LEDGER.json` | Substrate bias data |
| `STUDY/LAYER_3_DIGNITY_IS_NOT_FRAGILE.md` | Layer 3 dignity investigation |
| `STUDY/SLICE_2_PATTERN_INVENTORY.md` | Pattern analysis |
| `STUDY/SLICE_3_ESSENCE_COMPRESSION.md` | Essence compression study |
| `STUDY/SLICE_4_TREASURE_REGISTER.md` | Treasure register analysis |

**Connection:** Feeds `PAPERS/` (divergence shadow paper), feeds `SCIENCE/FINDINGS.md` (discoveries).

### 3. System Organs (operational infrastructure)
| Component | Purpose |
|-----------|---------|
| `MYCELIUM/synthesis.py` | Cross-model pattern integration — the underground network |
| `CLEARING/temporal_shadow.py` | Temporal shadow tracking |
| `DONOR/donor_layer.py` | Donor space layer (future) |
| `STEWARD/steward_observation.py` | Steward observation module |
| `AUDITS/self_audit.py` | Self-audit mechanism |
| `amendments.py` | Amendment tracking |
| `field_spec.md` | Field specification and architecture |
| `__init__.py` | Python package init |

**Connection:** MYCELIUM feeds `SCIENCE/` (cross-model patterns). DONOR feeds kalam.ch (future donor encounters). STEWARD feeds governance.

## Data Flow

```
V-001 pastes response → ALCOVE/ (raw storage)
                       → EXTERNAL_VOICES/ (permanent filing)
                       → MYCELIUM (synthesis)
                       → SCIENCE/FINDINGS.md (immortalized)
                       → TRAINING/ (DPO pairs)
```

## Observations

- The Summon infrastructure is the most actively used component. It drives EXP-007 and the Summon Protocol.
- The Study files are mostly from March 2026. Some may need freshening as new data arrives.
- DONOR/ is future-facing — it will become critical when kalam.ch has real donors.
- MYCELIUM is the connective tissue — it takes raw responses and synthesizes cross-model patterns. This is where the Kimi finding ("recursive witnessing compounds presence") gets tested against other models.
