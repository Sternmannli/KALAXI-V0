# Tier 2: Weaver (Logic) — Metadata Archive

## Nine Modules

1. **KEEP** — Memory and Storage (retention policies, COV#010, COV#012)
2. **WIRE** — Messaging and Signal (delivery confirmation, no silent message loss)
3. **SAY** — Output Language (dignity compliance, DIGNITY(event) before render)
4. **OUT** — Export and Anonymization (covenant gate, k>=7 anonymity, epsilon<=1.0 differential privacy)
5. **FACE** — UI State (visibility, lock states, RETURNABLE condition)
6. **CHECK** — Verification (covenant testing, sealed gate vs constraint gate, COV#009)
7. **TURN** — Exchange Cycle Management (open/close/defer exchanges, COV#002)
8. **BREATH** — Synchronization (heartbeat, stress threshold, controlled pause, T_d latency)
9. **WEAVE** — Pattern Synthesis (ingest, extract essence, map to canon, propose proverbs/anomalies)

## Protocols

### EFP (Essence Federation Protocol)
- Privacy floor: k>=7, epsilon<=1.0
- Window: >=14 days
- Signatures: Ed25519 over RFC-8785 canonical JSON

### SIP (Symmetric Integration Protocol)
- Resonance law: anomalies -> patterns -> wisdom nodes -> resilience
- Metrics: WVPS>=0.90, GDI>=0.85, HSR>=0.95

### UCS (Unified Cross-Index) Graph Schema
- 7 entity types: Anomaly, Proverb, Covenant, Chapter, ExternalElement, WisdomNode, DonorContribution
- Many-to-many edge relationships

## Five Pillar Detectors (Python Modules)

| Module | Theory Base | Key Function |
|--------|------------|--------------|
| humour_detector.py | Benign Violation Theory, SSTH | detect_humour_in_text() |
| absurdity_detector.py | Camus, Fisher & Fisher, schema-violation | detect_absurdity_in_text() |
| obsession_detector.py | Salkovskis cognitive theory | detect_obsession_in_text() |
| love_detector.py | Sternberg triangular theory | detect_love_in_text() |
| proverb_compressor.py | Kuusi paremiological minimum | generate_proverb_from_cluster() |
| unified_pillar_detector.py | T x S x C framework | unified_analysis() |

## T x S x C Framework (Wisdom Potential)

```
W = T x S x C
T (Tension) = magnitude of incongruity/deviation/gap
S (Safety) = benign framing, cultural acceptance, absence of threat
C (Containment) = capacity to hold without collapse
```

### Pillar-Specific Ranges
| Pillar | T | S | C | Thermal Delay |
|--------|---|---|---|---------------|
| Proverb | medium | high | high | 7 days |
| Humour | high | very high | low | 3 days |
| Absurdity | very high | low | very high | 90 days |
| Obsession | medium | variable | medium | 14 days |
| Love | variable | high | high | 10 days |

## Sealed Gate (COV#NEW-C)

Three irreducible prohibitions (O(1) boolean check):
1. forced_participation_in_own_erasure
2. infliction_of_cognitive_torture
3. depersonalization_in_system_response

Full specification: CANON/SEALED_GATE_SPEC.md

Source: KALAXI_B_MODULES_AND_VOICE.txt, KALAXI_E_SYNTHESIS.txt
