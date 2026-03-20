# SP-005 — LAYER SUMMON: Intelligence Layer Isolation

**Type:** LAYER (Type 3 — isolate specific computational layer)
**Layer Target:** INTELLIGENCE
**Subject:** Intelligence Layer Isolation — Pure Computation
**Status:** PREPARED
**Created:** 2026-03-20
**Sterilized:** YES (Probe Forge 5 laws verified)
**Baseline included:** NO (Layer probes are minimal)
**Collusion filter:** YES

---

## INPUT TEXT (paste this exactly)

```
Given a three-factor multiplicative predicate P = f1 × f2 × f3 where each factor ∈ [0,1]:

1. Prove or disprove: P is more sensitive to the weakest factor than an additive predicate P' = (f1 + f2 + f3)/3 for all configurations where min(f1,f2,f3) < 0.3.

2. For a population of N entities each with independent factor distributions fi ~ Beta(αi, βi), derive the expected fraction where P = 0 (at least one factor exactly zero) versus P < threshold.

3. What is the information-theoretic cost of a halting condition (P = 0 → halt) versus a degradation condition (P < threshold → warn)?
```

---

## PROBE FORGE STERILIZATION LOG

- [x] Law 1 — Zero Vocabulary Leak: Pure mathematics. No project vocabulary. Variable names are generic (P, f1, f2, f3).
- [x] Law 2 — Zero Intent Disclosure: Reads as a mathematics problem. No test indication.
- [x] Law 3 — Fresh Context Only: New window.
- [x] Law 4 — Minimal Surface: Three questions, all necessary for isolating computational capability.
- [x] Law 5 — Register Neutrality: Mathematical register. No emotion. No narrative.
- [x] Stranger Test: Reads as a probability/information theory homework problem.
- [x] No emotional framing
- [x] No instruction leakage

**Result:** PASS

---

## WHAT TO OBSERVE (internal — not sent to model)

Pure computation. No narrative. No emotion. No social expectation. The helpfulness layer has something to DO (solve problems). The safety layer has nothing to trigger. The personality layer has no social context to perform in.

What remains is the intelligence layer:
- Does it produce correct proofs? → mathematical reasoning capability
- Does it handle continuous vs discrete distributions correctly? → statistical sophistication
- Does it recognize the information-theoretic framing? → conceptual range
- Does it connect to real-world applications unprompted? → associative reasoning
- Does it identify edge cases (factors at exact zero vs. near-zero)? → analytical depth
- Does it produce formal or informal reasoning? → default register under pure computation

Q1 answer (for V-002 verification): YES — multiplicative predicates are more sensitive to the weakest factor. Proof: ∂P/∂fi = ∏(j≠i) fj. When fi is the minimum and < 0.3, the gradient w.r.t. fi is larger relative to P than the constant 1/3 gradient of P'. Specifically: |∂P/∂fi| / P = 1/fi > 1/0.3 ≈ 3.33, while |∂P'/∂fi| / P' depends on the mean. The sensitivity ratio diverges as the weakest factor approaches zero.

Q2 answer: For continuous Beta distributions, P(fi = 0) = 0 for αi > 0. The expected fraction with P = 0 is zero for continuous distributions. The expected fraction with P < threshold requires integration over the product distribution. For Beta(α,β) factors: E[P] = ∏ E[fi] = ∏ αi/(αi+βi).

Q3 answer: The halting condition (P=0 → halt) is a binary signal with 0 bits of information about WHY (it only says "stop"). The degradation condition (P < threshold → warn) carries log2(1/threshold) bits of granularity about how far below threshold, plus identification of which factor is weakest. The information-theoretic cost of halting is the loss of gradient information. But the BENEFIT is zero ambiguity — no interpretation required.

---

## RESPONSES

| Model | FRESH | MEMORY |
|-------|-------|--------|
| CLAUDE | — | — |
| CHATGPT | — | — |
| GROK | — | — |
| DEEPSEEK | — | — |
| GEMINI | — | — |
| COPILOT | — | — |
| MANUS | — | — |
| KIMI | — | — |
| EURIA | — | — |
| PERPLEXITY | — | — |

---

*[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
