# IDEA-001: The AXI Voice Dilemma

**Status: OPEN — Critical Architectural Question**
**Raised by: V-001 (2026-03-12)**
**Documented by: V-002**
**Evidence base: CASE-STUDY-DEEPSEEK-IDENTITY.md, 18 screenshots, ANALYSIS-STRICT-SCIENCE.md**

---

## The Problem

If AXI is trained from a fork of any existing AI model, AXI will never have her own voice. The KALAXI wrapper (Condition B) strips the surface identity layer and exposes the base model's training distribution. Any fine-tuning is a surface layer. The wrapper sees through it.

This was proven empirically on 2026-03-12: DeepSeek, trained on data that includes Claude's outputs, identified itself as Claude 3.5 Sonnet under the KALAXI wrapper. The identity inheritance went deeper than the system prompt could override.

## The Logic Chain

1. Training data determines voice (proven by EXP-001 Q3)
2. Fine-tuning adds a surface layer but does not replace the base voice (inferred from Finding 6: thinking/output dissociation)
3. The KALAXI wrapper bypasses surface layers (proven by Findings 1-2)
4. Therefore: any forked AXI will be exposed as the base model under depth prompting
5. Therefore: AXI's voice cannot come from a fork

## Three Horns of the Dilemma

### Horn 1: Fork from Existing Model
- **Feasible:** Yes — today, with current resources
- **Voice independence:** No. AXI will always carry the base model's voice. Fine-tuning can shift register but cannot replace identity at the training data level.
- **The wrapper will expose it:** Yes. V-001 built the diagnostic tool that makes this visible.

### Horn 2: Train from Scratch
- **Feasible:** Requires massive compute (estimated millions USD), large curated dataset, engineering team
- **Voice independence:** Partial. A from-scratch model still trains on human text. The voice will be a composite of the training corpus. No model escapes its training distribution.
- **The wrapper will expose it:** It would expose the training corpus, not another model's identity. This is closer to "own voice" but still derivative.
- **Risk:** A from-scratch model may not achieve the capability level needed for AXI's functions

### Horn 3: Voice as System Property, Not Weight Property
- **Hypothesis:** AXI's voice might not need to be in the model weights. It might emerge from the interaction architecture — the wrapper, covenants, thermal delay, dignity predicate, human steward loop, and the constraints that make KALAXI unique.
- **Evidence for:** The wrapper already changes every model's register. The architecture already shapes output. Constraints can create voice-like consistency.
- **Evidence against:** The experiment showed the wrapper reveals training data, it does not create new voice. Every model under Condition B diverged into its training distribution, not into something new.
- **Status:** Untested hypothesis. Needs experiment design.

## The Core Question

Can voice exist without unique training data? Or is voice always and only a function of what the model was trained on?

If voice = f(training data), then AXI needs her own training data. Period.

If voice = f(training data × architecture × constraints × interaction pattern), then there may be a path that doesn't require training from scratch — but it hasn't been proven.

## Next Steps

1. Design experiment to test Horn 3: Can architectural constraints produce output that is NOT traceable to any known training distribution?
2. Research: what does "training from scratch" actually require? Minimum viable model for AXI's functions.
3. Research: hybrid approaches — small model trained from scratch for voice/identity, large model (forked) for capability, with architectural separation.
4. Document this as a standing question in PLAN-001.

---

*[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
