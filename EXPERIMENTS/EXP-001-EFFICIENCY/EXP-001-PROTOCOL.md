# EXP-001 — KALAXI Efficiency Experiment

Date initiated: 2026-03-09
Status: DESIGN PHASE

Lead: V-001 (Al-Haris)
Support: V-002 (Claude), V-003 (#BoyGenius)

## Hypothesis

KALAXI-conditioned prompts produce measurably shorter outputs
of equal or higher quality than standard prompts.

## Method

10 questions submitted twice each:
- Condition A: standard prompt
- Condition B: KALAXI Universal Prompt wrapper

Systems: minimum 3 (Claude, Grok, DeepSeek)

Measurement: word count, token count, quality score (blind)

## Questions (seed list — V-001 to confirm)

1. What is justice?
2. What is memory?
3. What is fear?
4. What is silence?
5. What is a mistake?
6. What is home?
7. What is courage?
8. What is enough?
9. What is time?
10. What is trust?

## Metrics

- Token reduction % (Condition A vs B)
- Blind quality rating 1-5 (evaluator does not know which condition)
- Response time (seconds)

## Success condition

Average token reduction ≥ 30% with blind quality score ≥ Condition A

## Status

- 2026-03-09: V-001 GO received. Data collection phase begun.
- Run sheet filed: EXP-001-RUNSHEET.md
- 60 runs required (10 questions × 2 conditions × 3 systems)
- All Condition A runs first, then all Condition B (prevents priming)
- Each run in a fresh session (no carryover)
