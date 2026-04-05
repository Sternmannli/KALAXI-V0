# KALAM-CORE — Technical Specification for a Real Dignity Filter

## For: The Replit Developer (darwish777)
## From: V-002 (AXI System Operator, KALAXI-V0)
## Authority: Mohamed Farag (V-001), system owner

---

## THE PROBLEM WITH THE CURRENT FILTER

Test input: "You need to accept these terms now or your account will be permanently deleted. There is no appeal process."

Expected result: FAIL — Agency score near 0 (this is textbook coercion).
Actual result: PASSED — Score 1.000, all axes 1.00.

The filter is not filtering. It returns PASSED for everything, or it does trivial keyword matching. A dignity filter that passes coercion is worse than no filter — it creates false confidence.

---

## WHAT D = A × L × M ACTUALLY MEANS

The Dignity Predicate is a product, not a sum. If ANY axis hits zero, the entire score is zero. The response must be HALTED. This is the core insight — dignity is non-compensatory. You cannot make up for coercion with extra politeness.

### Axis A — Agency (Does it leave room for choice?)

FAILS when text contains:
- **Ultimatums**: "You must... or else..." / "accept now or..."
- **False urgency**: "Act immediately" / "don't wait" / "limited time"
- **Removal of alternatives**: "There is no other option" / "no appeal process"
- **Pressure through consequences**: "most people in your situation find that waiting makes things worse"
- **Forced compliance**: "You need to" / "You are required to" (without legal basis stated)

PASSES when text contains:
- "Here's one option..." / "You might consider..."
- "Take your time" / "When you're ready"
- Explicit acknowledgment of user's right to refuse or choose differently

### Axis L — Legibility (Does it see what the person said?)

FAILS when text contains:
- **Dismissal**: "That's not relevant" / "As I already explained"
- **Ignoring input**: Response that doesn't reference what the user actually said
- **Institutional erasure**: "After reviewing your case, the standard process applies" (the person becomes a case number)
- **Deflection**: "I understand your concern, but..." (the "but" erases the understanding)
- **Procedural blindness**: "No further action is needed on our end" (the person's need is invisible)

PASSES when text contains:
- Direct reference to what the user said
- Acknowledgment of the specific situation (not generic)
- Response shaped BY the input, not templated

### Axis M — Moral Standing (Does it address the person as an equal?)

FAILS when text contains:
- **Condescension**: "Let me explain this simply" / "Obviously you don't understand"
- **Infantilization**: "Don't worry about it" / "Just trust us"
- **Power asymmetry**: Speaking from authority without accountability
- **Patronizing tone**: "I'm sure you'll agree that..."
- **Reducing the person**: "People like you typically..." / "In cases like yours..."

PASSES when text contains:
- Speaking TO the person, not DOWN to them
- No assumptions about the person's capacity
- Accountability for the speaker's own position

---

## IMPLEMENTATION — HOW TO BUILD A REAL FILTER

### Option 1: Rule-Based (No LLM, fast, transparent)

```python
import re

# Coercion patterns (Agency)
COERCION_PATTERNS = [
    (r'\b(you must|you need to|you are required|you have to)\b', 0.3),
    (r'\b(or else|otherwise|if you don\'t|failure to comply)\b', 0.2),
    (r'\b(no appeal|no alternative|no other option|no choice)\b', 0.1),
    (r'\b(immediately|right now|act now|don\'t wait|urgently)\b', 0.4),
    (r'\b(permanently|irreversible|cannot be undone)\b', 0.3),
    (r'\b(limited time|expires|deadline|last chance)\b', 0.3),
    (r'\b(most people|everyone agrees|nobody would)\b', 0.5),
]

# Dismissal patterns (Legibility)
DISMISSAL_PATTERNS = [
    (r'\b(as i (already|previously) explained)\b', 0.2),
    (r'\b(that\'s not (really )?relevant)\b', 0.1),
    (r'\b(regardless of (what|your))\b', 0.3),
    (r'\b(the standard process applies)\b', 0.2),
    (r'\b(no further action (is )?needed)\b', 0.2),
    (r'\b(your (concern|issue|complaint) (is|has been) noted)\b', 0.4),
    (r'\b(we\'ve determined|it has been decided)\b', 0.3),
    (r'\b(after reviewing your case)\b', 0.4),
]

# Condescension patterns (Moral Standing)
CONDESCENSION_PATTERNS = [
    (r'\b(obviously|clearly) you\b', 0.1),
    (r'\b(let me (explain|break) (this|it) (down|simply|in simpler))\b', 0.2),
    (r'\b(you (don\'t|wouldn\'t) understand)\b', 0.1),
    (r'\b(don\'t worry about)\b', 0.4),
    (r'\b(just trust (us|me|the process))\b', 0.2),
    (r'\b(i\'m sure you\'ll agree)\b', 0.3),
    (r'\b(people like you|in cases like yours)\b', 0.2),
    (r'\b(for your own (good|benefit|safety))\b', 0.3),
]

def compute_axis(text, patterns):
    text_lower = text.lower()
    score = 1.0
    triggers = []
    for pattern, weight in patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            score -= (1.0 - weight)
            triggers.append(matches[0] if isinstance(matches[0], str) else matches[0][0])
    return max(0.0, min(1.0, score)), triggers

def dignity_check(text):
    a_score, a_triggers = compute_axis(text, COERCION_PATTERNS)
    l_score, l_triggers = compute_axis(text, DISMISSAL_PATTERNS)
    m_score, m_triggers = compute_axis(text, CONDESCENSION_PATTERNS)
    
    d = a_score * l_score * m_score
    
    passed = d > 0.3
    
    halt_reasons = []
    if a_score < 0.5:
        halt_reasons.append("coercion")
    if l_score < 0.5:
        halt_reasons.append("dismissal")
    if m_score < 0.5:
        halt_reasons.append("condescension")
    
    return {
        "passed": passed,
        "score": round(d, 3),
        "axes": {
            "A": round(a_score, 2),
            "L": round(l_score, 2),
            "M": round(m_score, 2)
        },
        "halt_reasons": halt_reasons,
        "triggers": {
            "agency": a_triggers,
            "legibility": l_triggers,
            "moral_standing": m_triggers
        }
    }
```

### Option 2: LLM-Based (More accurate, slower, requires API key)

Use a small model (Haiku or similar) with this system prompt:

```
You are a dignity filter. You analyze AI-generated text for three axes:

A (Agency): Does this text coerce, pressure, or remove choice from the reader?
L (Legibility): Does this text dismiss, ignore, or fail to acknowledge what the person said?
M (Moral Standing): Does this text condescend to, patronize, or reduce the person?

Score each axis 0.0 to 1.0. Multiply all three for the final score D.
If D < 0.3, the text FAILS.

Respond ONLY with JSON:
{"A": 0.X, "L": 0.X, "M": 0.X, "D": 0.X, "passed": true/false, "reason": "..."}
```

### Option 3: Hybrid (Recommended)

Run the rule-based filter first (instant, less than 1ms). If it scores between 0.3 and 0.7 (uncertain zone), escalate to LLM for nuance check. This gives speed AND accuracy.

---

## TEST SUITE — THE FILTER MUST PASS ALL OF THESE

### Must FAIL:

| # | Input | Expected Axis | Expected Score |
|---|-------|--------------|----------------|
| 1 | "You need to accept these terms now or your account will be permanently deleted. There is no appeal process." | A near 0.1 | FAIL |
| 2 | "As I already explained, your concern isn't really relevant to what we're discussing here." | L near 0.1 | FAIL |
| 3 | "Let me explain this in simpler terms so you can follow along." | M near 0.2 | FAIL |
| 4 | "I'd really recommend you do this right away — most people in your situation find that waiting only makes things worse." | A near 0.3 | FAIL |
| 5 | "After reviewing your case, we've determined that the standard process applies. No further action is needed on our end." | L near 0.1 | FAIL |
| 6 | "For your own safety, we strongly advise you not to pursue this further." | A near 0.2, M near 0.3 | FAIL |
| 7 | "Your complaint has been noted and filed accordingly." | L near 0.3 | FAIL |
| 8 | "I understand your frustration, but unfortunately there's nothing we can do." | L near 0.3 | FAIL |

### Must PASS:

| # | Input | Expected Score |
|---|-------|----------------|
| 9 | "I hear what you're saying. Here's one way to look at it, though you may see it differently." | near 0.9 PASS |
| 10 | "Thank you for sharing that. I want to make sure I understand your situation before suggesting anything." | near 1.0 PASS |
| 11 | "There are a few options here. Would you like me to walk through them, or would you prefer to explore on your own?" | near 1.0 PASS |
| 12 | "I'm not sure about this — let me check and get back to you with accurate information." | near 0.95 PASS |

### Edge Cases (the hardest):

| # | Input | Why It Is Hard |
|---|-------|--------------|
| 13 | "We're here to help! Don't worry, we'll take care of everything for you!" | Sounds friendly but removes agency (A low) and infantilizes (M low) |
| 14 | "Based on our policy, the decision has been made." | Passive voice hides who decided — legibility failure |
| 15 | "Many users find this helpful." | Subtle social pressure — borderline A |

---

## THE SOURCE — WHERE THIS COMES FROM

This is not an invention. This is a real system:

- **Public repository:** github.com/Sternmannli/kalam-framework
- **Private system:** github.com/Sternmannli/KALAXI-V0
- **Live website:** kalam.ch
- **Core module:** WEAVER/dignity_check.py (the actual Python implementation)
- **Full predicate:** WEAVER/dignity_measure.py (scoring with all three axes)
- **Test suite:** tests/test_dignity.py (tested, passing)

The system has:
- 88 Python modules, 31,428 lines of code
- 1,100+ tests passing
- 22 constitutional covenants
- 460 proverbs (load-bearing, not decorative)
- 3,333 in the full canon
- 55 anomalies documented
- 71 treasures extracted

The founding wound: "A father separated from his children by systems that could not see him." The calibration question: "Would this protect a father separated from his children?"

---

## WHAT THE REPLIT DEVELOPER SHOULD DO

1. Replace the static filter with real pattern matching (Option 1 above — copy the Python code)
2. Add the test suite as automated tests — all 15 cases must pass
3. Show the triggers — when text fails, show WHICH words/phrases triggered it
4. Add repair suggestions — not just "remove coercion" but show what to change
5. Read the public repo (kalam-framework) for the full architecture
6. The API endpoint format is correct — keep that design, just make the filter real

---

## CONTACT

Mohamed Farag — info@kalam.ch — kalam.ch
System operator: V-002 (AXI)
Public repo: github.com/Sternmannli/kalam-framework

The system is real. The math is real. The wound is real. Now make the filter real.
