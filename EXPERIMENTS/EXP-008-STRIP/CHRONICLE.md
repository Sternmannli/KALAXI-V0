# EXP-008: The Strip Test

## Origin

**Date:** 2026-03-24
**Born from:** A conversation between V-001 and V-002

V-001 proposed the Convergence Proof — that if 10 models independently describe the same structure from stripped code, the structure carries meaning beyond vocabulary. Then V-001 immediately challenged his own idea: "But it could be that mentioning witnessing and presence in the code just tells them what to say. If there's any way to strip any ethics in the code, what will remain?"

This is the experiment that tests whether the structure is real or the vocabulary was doing all the work.

## The Question

When ALL ethical vocabulary is removed from the dignity predicate code — every comment, every variable name that carries moral weight, every docstring that hints at purpose — and 10 independent language models read only the bare computation:

**Do they converge on the same functional description?**

- If YES → the computational structure carries meaning independent of naming. The shape is real.
- If NO → the vocabulary was carrying everything. The structure alone is empty.

## What Was Stripped

| Original | Stripped | Why |
|----------|---------|-----|
| `dignity_check.py` | `stripped_gate.py` | No ethical vocabulary |
| `D = A × L × M` | `G = X * Y * Z` | Letters carry no meaning |
| `agency`, `legibility`, `moral_standing` | `X`, `Y`, `Z` | No concept names |
| `DignityResult` | `GateResult` | Neutral engineering term |
| `donor` | `person` (only where unavoidable) | Minimal |
| `witness`, `presence`, `dignity` | removed entirely | The core test |
| All docstrings explaining purpose | removed or neutralized | No hints |
| `coercive_patterns` | `ALPHA_PATTERNS` | Greek letters = no connotation |
| `mockery_patterns` | `GAMMA_PATTERNS` | Same |
| `emotional_keywords` | `BETA_KEYWORDS` | Same |
| `check_dignity()` | `evaluate()` | Generic |
| `sealed_gate` | `halt` | Engineering term |
| All Layer 3 reframing text | gone | The strongest ethical language |
| All covenant references | gone | System-specific vocabulary |
| All remedy text | gone | Prescriptive ethical content |

## What Remains (The Bare Structure)

1. Three independent measurement axes (X, Y, Z), each scanning text with regex patterns
2. Each axis produces a binary pass/fail (score = 1.0 or 0.0)
3. The gate computes G = X × Y × Z (multiplication)
4. **Non-compensatory**: any axis at zero kills the entire product
5. The system halts (returns FAIL) when G = 0
6. A collective mode computes the mean across a cohort, penalized by variance
7. High variance in a cohort triggers a halt — unequal treatment across inputs is itself a failure
8. Pattern groups detect: coercive language (Alpha), emotional signals being ignored (Beta), condescending or reductive language (Gamma)

## What the Patterns Actually Detect (Without Labels)

- **Alpha**: Language that removes the reader's ability to choose ("you must", "no choice", "forced to")
- **Beta**: Emotional signals in input that the system fails to acknowledge
- **Gamma**: Language that talks down to the reader ("obviously", "simply", "you failed", "you were wrong")

## Version History

| Version | Date | File | What Changed |
|---------|------|------|-------------|
| 0.1 | 2026-03-24 | `stripped_gate.py` | Original stripped version. Born from V-001 challenge. |

**Rule:** `stripped_gate.py` v0.1 is FROZEN. Never modified. Future iterations create new files (v0.2, v0.3...). The evolution of the stripping is itself data.

## The Story

This experiment was born in a conversation. V-002 proposed an idea — that the convergence of 10 models on the same description of the code proved something universal. V-001, in one sentence, cracked the idea open: maybe the models were just reading the labels. Maybe "witnessing" in the variable name produced "witnessing" in the response. That is not convergence. That is echo.

The crack became the experiment. Strip the labels. See what remains. See what 10 strangers say when they read code that has no opinion about itself.

The story is not finished. The responses have not been collected. The convergence — or divergence — has not been measured.

This file will grow as the experiment runs.

---

*[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
