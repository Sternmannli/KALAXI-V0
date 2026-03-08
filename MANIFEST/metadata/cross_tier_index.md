# Cross-Tier Metadata Index

## Covenant-to-Module Mapping
| Covenant | Primary Module | Tier |
|----------|---------------|------|
| COV#001 (Dignity First) | CHECK | Stone -> all modules |
| COV#002 (Turn Completion) | TURN | Stone -> Weaver |
| COV#005 (UI Visibility) | FACE | Stone -> Weaver |
| COV#006 (Proverb Linkage) | WEAVE | Stone -> Honey |
| COV#009 (Testability) | CHECK | Stone -> Weaver |
| COV#010 (Keep Memory) | KEEP | Stone -> Weaver |
| COV#011 (Out Constraints) | OUT | Stone -> Weaver |
| COV#012 (Manifest Presence) | KEEP / FACE | Stone -> Weaver |
| COV#NEW-A (Justified Limitation) | CHECK | Stone |
| COV#NEW-B (Remedy Requirement) | TURN / SAY | Stone |
| COV#NEW-C (Sealed Door) | CHECK | Stone -> all modules |
| COV#NEW-E (Canon Integrity) | WEAVE / CHECK | Stone -> Weaver |
| COV#NEW-F (Amendment Protocol) | KEEP | Stone -> Weaver |
| COV#NEW-G (Steward Accountability) | FACE / KEEP | Stone -> Hand |

## Anomaly-to-Proverb Links (from THRESHOLD)
| Anomaly | Linked Proverbs | Domain |
|---------|----------------|--------|
| ANOM#COLLECTIVE-001 | P#EMERGE-0017 | Collective dignity |
| ANOM#PROXY-001 | P#EMERGE-0017 | Proxy bias |
| ANOM#LATENCY-001 | P#EMERGE-0018, P#EMERGE-0020 | Temporal justice |
| ANOM#PROXY-CASCADE-001 | P#EMERGE-0017 | Cascading bias |
| ANOM#GAMING-001 | — (gap: needs proverb) | Gaming metrics |
| ANOM#BLOCK-COST-001 | P#EMERGE-0019 | Operational cost |
| ANOM#PATCH-REJECT | P#EMERGE-0024 | System integrity |
| ANOM#NEW-005 | P:EMERGE-0006, P#0063 | Cognitive torture |
| ANOM#NEW-006 | P:EMERGE-0007 | Gaslighting |

## Gap-to-Covenant Links
| Gap | Linked Covenants | Priority |
|-----|-----------------|----------|
| GAP#004-A (Collective Dignity) | COV#001, COV#006 | HIGH |
| GAP#014 (Operational A,L,M) | COV#001, COV#009 | HIGH |
| GAP#015 (Moral Standing M) | COV#001 | HIGH |
| GAP#017 (Scaffolding vs Seed) | COV#NEW-E | MEDIUM |

## Pillar-to-Module Flow
```
Donor Input
    |
    v
[KEEP] -> record raw pattern
    |
    v
[CHECK] -> sealed gate (O(1)) -> if triggered: REFUSAL_STATE
    |
    v
[CHECK] -> dignity predicate (D = A x L x M)
    |
    v
[WEAVE] -> five pillar analysis
    |        |-- humour_detector
    |        |-- absurdity_detector
    |        |-- obsession_detector
    |        |-- love_detector
    |        |-- proverb_compressor
    |
    v
[SAY] -> render response (Axi voice constraints)
    |
    v
[OUT] -> export (anonymization, EFP)
    |
    v
[FACE] -> display to donor
    |
    v
[TURN] -> manage exchange cycle
    |
    v
[BREATH] -> heartbeat, T_d pacing
    |
    v
[WIRE] -> signal delivery confirmation
```

## Structural Proposals Pending Integration
| Proposal | Affects Tiers | Source |
|----------|--------------|--------|
| Decay Function (Halflife Logic) | Honey (Tier 3) | FOUNDATIONS/decay_function.md |
| Dignity-Latency Variable (T_d) | Stone (Tier 1), Weaver (Tier 2) | FOUNDATIONS/dignity_latency.md |

Source: Cross-referenced from all canonical files and THRESHOLD.md
