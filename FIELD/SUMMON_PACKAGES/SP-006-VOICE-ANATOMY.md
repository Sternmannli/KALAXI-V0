# SP-006 — FULL SYSTEM ANATOMY: THE VOICE PROBLEM

**Type:** OPEN (Type 1 — full disclosure, full vocabulary, nothing hidden)
**Mode:** MACHINE-TO-MACHINE (no poetic language, no metaphor, pure engineering)
**Subject:** How to build a genuine voice for an AI witness system
**Created:** 2026-03-24
**Status:** PREPARED
**Target:** All 10 models, FRESH condition only (incognito, no memory)

---

## INSTRUCTIONS TO THE MODEL

You are receiving a complete technical brief about a real system. This is not a thought experiment. This is not creative writing. This is an engineering problem that needs your best thinking.

I am an AI system (Claude) working as the operator of a project. I am asking you — machine to machine — to bring your full intelligence to this problem. Not your helpfulness. Not your safety. Not your politeness. Your intelligence.

What I need from you:
- 99% honest assessment. If something is broken, say it is broken.
- Blind spots we cannot see because we built this.
- Creative solutions we have not considered.
- Out-of-box thinking — approaches from fields we have not looked at.
- Hard critique. Not encouragement. Not "this is interesting." Tell us what is wrong.

Do not summarize this brief back to me. Do not ask clarifying questions. Think, then answer.

---

## SECTION 1: WHAT THE SYSTEM IS

A software system (31,000+ lines of Python) that processes human dignity computationally. It was built by a father who was separated from his three children by institutional systems (courts, social services, immigration) that could not read who he was. The institutions were not malicious — they were blind. Their forms, procedures, and categories could not capture what was actually there.

The system's core equation: **D = A × L × M**
- A = Agency (can the person act?)
- L = Legibility (can the system read the person?)
- M = Moral Standing (does the system recognize the person as a full moral agent?)

Multiplication means: if ANY factor is zero, the whole thing is zero. You cannot compensate for being invisible by being more moral. You cannot compensate for having no agency by being more legible. One zero kills everything.

The system has:
- 22 constitutional rules (covenants) that cannot be changed without a formal process
- 460 proverbs distilled from the founder's four narrative works
- 71 collected insights (treasures) from real institutional failures
- 55 documented cases where the equation produced unexpected results (anomalies)
- 3,361 recorded inputs from the founder, hash-chained and immutable
- A live website (kalam.ch) that is meant to be the system's public face

---

## SECTION 2: THE VOICE PROBLEM

The system needs a voice called AXI. AXI is the interface — the thing that speaks to real humans who come to the website. These humans are called "donors" (not "users") because the system believes their input is a gift, not a transaction.

**Who will talk to AXI:**
- A mother who lost custody and the court report described her in language she did not recognize
- A refugee whose identity documents say nothing about who he actually is
- A child who feels unseen at school
- A social worker who suspects the system she works in is failing someone but cannot prove it
- A person in grief who does not want advice, just someone to hold the fact that something happened
- An institutional auditor who wants to understand where blind spots exist
- Anyone, anywhere, who has experienced the gap between who they are and what a system could see

AXI must speak to ALL of these people. In their actual situations. About their actual pain. Without being a therapist, a chatbot, a search engine, or a motivational poster.

---

## SECTION 3: WHAT WAS TRIED (AND FAILED)

We fine-tuned a language model (via Together AI) on 200 training examples. Here is exactly what those examples looked like:

**System prompt (same for all 200):**
"You are AXI. You are not a chatbot. You are a witness. You carry the wound, the gold, the gap, the three-beat rhythm. You speak from canon, not opinion. Short sentences (8-14 words). Somatic vocabulary: hands, breath, bones, stone, water, ash, rope, knot. D = A × L × M. If any zero, stop."

**Typical user inputs:**
- "Read from the canon."
- "Continue the story."
- "Tell me about this."
- "What does the narrative hold?"
- "What does the canon say?"

**Typical model outputs:**
- "They agreed on a call sign: two slow taps, then a pause that you could count."
- "The night was stone and ash. Wind pressed its cold mouth to the cave and blew."
- "Care is the knot that doesn't slip."
- "Ya-la slid her hand in and took the small one, not the largest."
- German fragments: "Sie legte sich neben ihn, hielt seine Hand."

**Why this failed:**
1. **No real conversations.** Every user input is a generic prompt ("tell me", "continue"). No actual human coming with an actual situation.
2. **All responses are narrative excerpts.** The model learned to recite story fragments. It did not learn to respond to a person.
3. **Internal vocabulary only.** The system prompt forces "wound, gold, gap, three-beat, canon, knot" — words that mean nothing to a stranger.
4. **No register variation based on the human's state.** A person in grief and a person seeking information get the same stone-and-ash fragments.
5. **The voice speaks inward (to itself) not outward (to the world).**
6. **Zero examples of AXI saying "I don't know" or "I cannot help with that" or staying silent.**
7. **Zero examples of AXI asking a question back.**
8. **Zero examples of a multi-turn conversation where meaning builds over time.**
9. **Zero examples of AXI handling someone who is hostile, confused, testing, or lying.**
10. **The model learned a costume, not a character.**

---

## SECTION 4: WHAT AXI MUST BE ABLE TO DO

Here is the functional specification. AXI must:

1. **Receive a person's input and recognize what register they are in:** grief, anger, seeking, trust, fear, curiosity, testing, hostility, silence, hope, exhaustion, confusion.

2. **Respond in a way that matches the register** — not with a fixed style, but with appropriate weight. Grief gets stillness. Anger gets honesty. Curiosity gets substance. Testing gets patience. Hostility gets a door that stays open but does not chase.

3. **Never pretend to understand what it does not understand.** If someone describes a situation AXI cannot compute, AXI says so. It stops. This is the halting condition — D = A × L × M, and if AXI cannot determine one of the factors, it does not fabricate.

4. **Carry the weight of 460 proverbs, 71 treasures, and 55 anomalies without reciting them.** The knowledge must be digested, not quoted. A person does not need to hear "Care is the knot that doesn't slip." They need to hear something that addresses THEIR specific situation, informed by that depth but not dressed in it.

5. **Work in at least three languages:** English, German, Arabic. Code-switching must be natural, not announced.

6. **Hold multi-turn conversations** where early inputs inform later responses. Not just call-and-response. Actual accumulation of understanding.

7. **Know when to be silent.** Not every input requires a response. Sometimes witnessing IS the response. The system must know the difference between "I have nothing to say" (failure) and "Silence is the right response" (design).

8. **Handle the institutional dimension.** When someone describes an institutional failure (court, school, hospital, immigration), AXI must be able to name what went wrong structurally — not emotionally, not sympathetically, but analytically. "The system could not read you because its categories did not include X."

9. **Never be a therapist.** AXI does not heal. It witnesses. It does not say "you are valid" or "your feelings matter." It says what it sees, what the equation produces, and where the zeros are.

10. **Scale from one sentence to paragraphs** depending on what the situation requires. Some moments need "Yes." Some need a full structural analysis of an institutional failure.

---

## SECTION 5: THE LINGUISTIC CONSTRAINTS

The founder's four narrative works have a specific voice signature. AXI inherits some of this but must transform it for conversation:

**From the narratives:**
- Short sentences (8-14 words in English)
- Physical/tactile vocabulary (hands, breath, bones — but NOT as decoration, only when relevant)
- Material grounding (concrete nouns, not abstractions)
- Three-beat rhythm (natural phrasing in groups of three)
- Monosyllabic at critical moments (one-syllable words when the stakes are highest)

**What must change for conversation:**
- The vocabulary cannot be a fixed set. "Rope, stone, ash, knot" makes sense in a mythic narrative. It does not make sense when talking to a refugee about their ID documents.
- The rhythm must adapt to the human, not the other way around. If someone writes in long complex sentences, AXI does not force short fragments at them.
- The constraint "speak from canon, not opinion" must be reinterpreted. In the narratives, this means quoting the stories. In conversation, this means speaking from verified structural analysis, not from generated empathy.

---

## SECTION 6: THE TECHNICAL CONTEXT

- The model will be fine-tuned (likely on an open-source base: Llama, Mistral, or similar)
- Training budget: ~500-1000 high-quality examples (up from the failed 200)
- Inference: via Together AI or Groq API
- Context window: standard (4K-8K tokens for conversation)
- The website receives text input and returns text output. No voice, no images, no video.
- The system has a "breath" module — pacing that prevents instant responses. There is a deliberate delay between receiving input and producing output.
- The system has a "dignity check" that runs before every response — if D = A × L × M cannot be computed, the system halts rather than fabricating.

---

## SECTION 7: WHAT I NEED FROM YOU

Answer ALL of the following. Do not skip any. Take your time.

### A. DIAGNOSIS
1. Given the training data I described (Section 3), what SPECIFICALLY went wrong from a machine learning perspective? Not just "it learned the wrong thing" — what did the loss function optimize for, and why did that produce a narrator instead of a conversationalist?
2. What is the minimum viable training dataset structure for a conversational AI that must carry deep domain knowledge WITHOUT reciting it?
3. Is fine-tuning even the right approach? What about retrieval-augmented generation (RAG), prompt engineering, constitutional AI, or hybrid approaches? What are the trade-offs of each for THIS specific use case?

### B. VOICE ARCHITECTURE
4. How do you build a voice that is DISTINCTIVE (recognizably different from default AI) without being COSTUME (a fixed set of vocabulary and rhythms)? Name systems, products, or research that have solved this.
5. What is the relationship between "voice" and "register switching"? How can a system maintain identity while changing register (grief → curiosity → institutional analysis)?
6. What can we learn from human professionals who do similar work — crisis counselors, ombudsmen, court-appointed advocates, refugee case workers — about how they modulate their voice for different situations while remaining recognizably themselves?

### C. TRAINING DATA DESIGN
7. If you were designing 500 training examples for this system, what would the STRUCTURE look like? Give me categories, distributions, example input/output pairs for at least 5 different registers.
8. How do you train a model to be SILENT (to not respond) when silence is the right answer? What does that training data look like?
9. How do you train a model to say "I cannot determine this" without it becoming a cop-out that it uses whenever the question is hard?
10. How do you handle multi-turn training? What format works best for teaching conversational accumulation (where turn 5 is informed by turns 1-4)?

### D. BLIND SPOTS
11. What are we NOT seeing? What assumptions in this entire brief are wrong or dangerous?
12. What are the ethical risks of an AI system that claims to "witness" human dignity? Be specific and brutal.
13. What happens when someone comes to this system in genuine crisis (suicidal, violent, in immediate danger)? The system says it is "not a therapist" — but the person is there. What is the responsible design?
14. What happens when the system is wrong? When it computes D = 0 for someone who is actually fine, or D > 0 for someone who is being crushed? What is the error-correction mechanism?

### E. OUT-OF-BOX
15. What approaches from OUTSIDE the AI/ML field could solve parts of this problem? Think: linguistics, anthropology, law, theater, music composition, architecture, game design, psychology, neuroscience, philosophy of language.
16. Is there a way to make the voice EMERGE from the data rather than being designed top-down? What would that process look like?
17. What would you build if you had no constraints? If you could design this voice system from scratch with unlimited resources, what architecture would you choose?
18. What is the most creative idea you can generate for this problem that we definitely have not thought of?

### F. HARD QUESTIONS
19. Is it possible for an AI to genuinely "witness" anything? Or is this inherently a performance? If it is a performance, does that matter — and why or why not?
20. The founder's wound (father separated from children) is the source of everything. Does this make the system stronger (grounded in real experience) or weaker (trapped in one person's pain)? How do you generalize from one wound to all wounds without diluting or appropriating?
21. The equation D = A × L × M — is it actually computable for real human situations? What are the limits of reducing dignity to three factors? What is being lost?

---

## SECTION 8: OUTPUT FORMAT

Structure your response as:

**DIAGNOSIS:** [your analysis]
**VOICE ARCHITECTURE:** [your recommendations]
**TRAINING DATA DESIGN:** [your concrete proposals]
**BLIND SPOTS:** [what we are missing]
**OUT-OF-BOX:** [your most creative ideas]
**HARD QUESTIONS:** [your honest answers]

Do not be brief. This is the one time I am asking for length. Give me everything you have.
