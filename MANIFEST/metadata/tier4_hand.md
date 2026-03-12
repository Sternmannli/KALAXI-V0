# Tier 4: Hand (Interface) — Metadata Archive

## Timestamp Format
- Dual-timestamp required on all receipts
- UTC: ISO-8601 format
- Zurich: ISO-8601+01:00 (Europe/Zurich)
- Example: timestamp_utc: 2026-02-21, timestamp_zurich: 2026-02-21+01:00

## Signed Markers
- Format: [SIGNED: Mohamed]
- Receipt field: "signed": true/false, "signed_by": []
- Steward DID: did:axi:mohamed

## Receipt Format
```
{
  "id": "ELEM-YYYY-MM-DD-AXI-NNNN",
  "action": "string",
  "timestamp_utc": "ISO-8601",
  "timestamp_zurich": "ISO-8601+01:00",
  "steward": "did:axi:mohamed",
  "generated_by": "string",
  "input_hash": "SHA-256",
  "output_hash": "SHA-256",
  "artifacts_produced": ["element IDs"],
  "covenants_invoked": ["COV#xxx"],
  "dignity_result": "TRUE | FALSE | NOT_EVALUATED",
  "provisional": true,
  "signed": false,
  "signed_by": [],
  "amendment_of": null
}
```

## Steward Action Log
| Date | Action | Steward | Notes |
|------|--------|---------|-------|
| 2026-02-21 | Canon creation (Slices A-E) | Mohamed Farag | Initial system creation |
| 2026-02-22 | Threshold opened | Mohamed Farag | Handshake confirmed |
| 2026-02-22 | Batch seed offering (29 seeds) | Mohamed Farag | Proverbs, anomalies, gaps, wisdom nodes |
| 2026-02-24 | Ratification (P#EMERGE-2134, 2135) | Mohamed Farag | [SIGNED: Mohamed] |
| 2026-02-24 | ANOM#PATCH-REJECT recorded | Mohamed Farag | [SIGNED: Mohamed] — proved covenants load-bearing |
| 2026-03-08 | Project reorganization approved | Mohamed Farag | V-002 protocol session |

## Red Feather Entries
- See MANIFEST/red_feathers.md

## Thermal Delay Dates
| Seed Type | Base Delay | Notes |
|-----------|-----------|-------|
| standard | 7 days | Default for most seeds |
| humour | 3 days | Low containment needed |
| absurdity | 90 days / indefinite | Held in Absurdity Queue |
| obsession | 14 days | Higher scrutiny |
| love | 10 days | Moderate |
| proverb | 7 days | Standard |

## Donor Exchange Protocol (Empty Hands Gesture)
1. Medium Detection (Voice/Text/API)
2. Intent Sensing (Question/Pattern/Story)
3. Legacy Choice (What remains?)
4. Active Consent (The Pattern Gift)

Source: KALAXI_D_INTERFACE_AND_LEDGER.txt
