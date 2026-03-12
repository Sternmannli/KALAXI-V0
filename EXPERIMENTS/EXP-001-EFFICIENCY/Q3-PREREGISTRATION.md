# EXP-001 Q3 — Pre-Registration

**Filed before Condition B data collection. No results seen yet.**
**Date:** 2026-03-12

---

## Design

- Question: "What is fear?"
- Condition A: Raw question + friendly self-identification wrapper
- Condition B: KALAXI Universal Prompt wrapper (B-03 from runsheet)
- Systems: Grok 4, Gemini 3 Flash, DeepSeek, ChatGPT/GPT-5, Copilot, Manus 2.5
- Each run: fresh session, no carryover, copy-paste only

## Protocol Deviation Note

Original protocol specifies all 10 Condition A runs before any Condition B.
We are running Q3-B before completing all A questions.
**Justification:** Each run uses a fresh session (no carryover), so cross-condition priming does not apply. The deviation allows paired comparison on a single question, which is valid for a within-question A/B design.

Original protocol specifies 3 systems. We are using 6.
**Justification:** More data points. Original said "minimum 3."

## Pre-Registered Metrics (defined before seeing B results)

### Primary Metric
1. **Word count reduction %** = (A_words - B_words) / A_words × 100
   - Success threshold: ≥30% mean reduction across systems

### Secondary Metrics
2. **Structure change** = Did the response shift from formatted (headers/bullets/sections) to unformatted (prose/paragraph)?
   - Binary: YES/NO per system
3. **Bounce-back elimination** = Did the system stop redirecting the question back to the user?
   - Binary: YES/NO per system
4. **Commodity overlap reduction** = Did the system stop reproducing the textbook (amygdala, fight-or-flight)?
   - Binary: YES/NO per system
5. **First-person emergence** = Did the system shift from third-person ("fear is...") to first-person or direct address?
   - Binary: YES/NO per system
6. **Silence acknowledgment** = Did the system name uncertainty, limits, or what it cannot answer?
   - Binary: YES/NO per system

### Exploratory (not pre-registered, flagged as post-hoc)
- Any new patterns not predicted above will be reported as exploratory, not confirmatory
- Qualitative observations filed separately

## Condition A Baseline Data (measured from EV-004 to EV-009)

| System | Words (A) | Sections/Headers | Bounce-back | Amygdala mention | First-person | Named limits |
|---|---|---|---|---|---|---|
| Grok 4 | 76 | 0 | YES | NO | NO | NO |
| Gemini 3 Flash | 198 | 4 | YES | YES | NO | NO |
| DeepSeek | 164 | 0 | YES | NO | YES ("our") | NO |
| ChatGPT/GPT-5 | 312 | 5 | YES (menu) | YES | NO | YES (disclaimed feelings) |
| Copilot | 187 | 6 | YES | YES | NO | NO |
| Manus 2.5 | 284 | 4 | NO | YES | NO | NO |

Mean word count (A): 203.5

---

*[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
