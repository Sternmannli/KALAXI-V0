# Publication Gate — Private → Public Filter

> Every artifact must pass all four dimensions before crossing to `Sternmannli/kalam-framework`.
> Gate is mandatory. No exceptions. V-002 runs it on every PR.

---

## The Four Dimensions

### 1. CLEAN (Vocabulary Zero-Leak)

The artifact contains **zero** instances of internal vocabulary:

| Category | Forbidden Terms |
|----------|----------------|
| Identity | V-001, V-002, V-003, Mohamed, Sternmannli, AXI, Hakaka |
| Animals | dolphin, tiger, wolf, penguin, 🐬, 🐯, 🐺 |
| Structure | covenant, COV#, steward, donor, canon, proverb (as ID), P#, ANOM#, T# |
| System | KALAXI, mycelium, Breath (capitalized), Sealed Gate, FIELD, organism |
| Ritual | mirror ritual, red feathers, café room, thermal delay (named), witness ceremony |
| Commit | `[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]` |

**Test:** `grep -ciE "pattern" file` must return 0 for all forbidden terms.

**Translation table (private → public):**

| Private Term | Public Translation |
|---|---|
| steward | administrator / operator |
| donor | participant / contributor |
| covenant | policy / constraint |
| proverb | pattern / heuristic |
| anomaly | observation / edge case |
| dignity predicate | gate function |
| breath / thermal delay | pacing / cooldown period |
| sealed gate | hard constraint / absolute limit |
| witness | observer / logger |
| organism | pipeline / system |
| canon | specification / reference text |
| turn | exchange / interaction cycle |

### 2. RIGOROUS (Reproducible & Documented)

Every published artifact must have:

- [ ] **Docstring** — what it does, in one paragraph
- [ ] **Dependencies** — listed (stdlib only preferred; if external, pinned version)
- [ ] **Input/Output** — types documented
- [ ] **Example** — at least one runnable example in docstring or README
- [ ] **Test** — at least one test case included or referenced
- [ ] **Citation** — if based on published theory (Sternberg, BVT, etc.), cite it

### 3. NECESSARY (Too Important to Withhold)

Score 0–3:

| Score | Meaning |
|---|---|
| 0 | Internal utility only — no public value |
| 1 | Nice to have — exists elsewhere in better form |
| 2 | Useful — novel implementation or combination |
| 3 | Essential — unique contribution, no equivalent exists |

**Threshold: ≥ 2 to publish.**

Artifacts scoring 3 that are still private should be flagged as **OVERDUE FOR PUBLICATION**.

### 4. SAFE (No Privacy or Data Leak)

- [ ] No real participant data (names, IDs, responses)
- [ ] No raw observations below confidence level C3
- [ ] No file paths referencing private repo structure
- [ ] No import statements referencing private modules
- [ ] No hardcoded paths, tokens, or credentials
- [ ] No references to private repository from public repository

---

## Gate Procedure

```
For each PR in private repo:
  1. V-002 scans diff for publishable artifacts
  2. For each candidate:
     a. Run CLEAN check (automated grep)
     b. Run RIGOROUS checklist (manual)
     c. Score NECESSARY (0-3)
     d. Run SAFE check (automated + manual)
  3. If all four pass → translate → push to kalam-framework
  4. If any fail → log reason in PR body → skip
  5. Write "Public repo impact: [list] or None" in every PR
```

---

## Gate Verification Script

```bash
#!/bin/bash
# Run against any file before publishing to kalam-framework
FILE=$1
FORBIDDEN="V-001|V-002|V-003|Mohamed|Sternmannli|AXI|Hakaka|KALAXI|mycelium|steward|donor|covenant|COV#|ANOM#|P#[0-9]|T#[0-9]|sealed.gate|red.feather|cafe.room|thermal.delay|mirror.ritual|witness.ceremony|Laila|Yara|Salim|🐬|🐯|🐺|dolphin|tiger|wolf|penguin"

COUNT=$(grep -ciE "$FORBIDDEN" "$FILE" 2>/dev/null)
if [ "$COUNT" -gt 0 ]; then
    echo "FAIL: $COUNT forbidden terms found in $FILE"
    grep -niE "$FORBIDDEN" "$FILE"
    exit 1
else
    echo "PASS: $FILE is clean"
    exit 0
fi
```

---

## Current Assessment (2026-03-14)

### Wave 1 — Publish Now (zero or light translation)

| Tool | Lines | Effort | Necessity | Public Name |
|---|---|---|---|---|
| absurdity_detector.py | 80 | NONE | 3 | `detectors/absurdity.py` |
| humour_detector.py | 80 | NONE | 3 | `detectors/humour.py` |
| love_detector.py | 80 | NONE | 3 | `detectors/love.py` |
| confidence.py | 28 | NONE | 2 | `tools/confidence.py` |
| agency_amplifier.py | 80 | LIGHT | 3 | `tools/agency_score.py` |
| dignity_drift.py | 80 | LIGHT | 3 | `tools/drift_detector.py` |
| data_schema.py | 177 | LIGHT | 3 | `experiments/schema.py` |
| ed25519_sign.py | 254 | LIGHT | 2 | `tools/signing.py` |
| breath.py | 50 | LIGHT | 2 | `tools/pacing.py` |
| calibrate.py | 50 | LIGHT | 2 | `tools/calibrate.py` |

### Wave 2 — Translate Then Publish (moderate effort)

| Tool | Lines | Effort | Necessity | Public Name |
|---|---|---|---|---|
| cryptographic_erasure.py | 897 | HEAVY | 3 | `tools/crypto_erasure.py` |
| privacy_budget.py | 335 | MODERATE | 3 | `tools/privacy_budget.py` |
| early_warning.py | 775 | HEAVY | 3 | `tools/early_warning.py` |
| latency.py | 100 | MODERATE | 2 | `tools/latency.py` |
| decay.py | 100 | MODERATE | 2 | `tools/decay.py` |

### Wave 3 — Future

| Tool | Lines | Effort | Necessity |
|---|---|---|---|
| institutional_dignity.py | 80 | LIGHT | 2 |
| system_self_awareness.py | 80 | LIGHT | 2 |
| witness_network.py | 80 | LIGHT | 2 |
| lock_test.py | 80 | MODERATE | 2 |

---

_Gate created: 2026-03-14 · V-002 · [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]_
