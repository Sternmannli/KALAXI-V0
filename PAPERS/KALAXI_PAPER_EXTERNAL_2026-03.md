# KALAXI: A Non-Compensatory Dignity Predicate for Constitutional AI Governance

**Mohamed Farag**
KALAM, Zurich, Switzerland
info@kalam.ch | https://kalam.ch

*March 2026*

*Target venues: ACM FAccT, AIES, arXiv cs.AI*

---

## Abstract

We present KALAXI, a constitutional AI governance framework that implements human dignity as an executable architectural constraint rather than a policy aspiration. The framework centers on a non-compensatory dignity predicate $D = A \times L \times M$, where Agency ($A$), Legibility ($L$), and Moral Standing ($M$) are jointly necessary conditions: if any component equals zero, the system halts. This multiplicative structure operationalizes Kant's categorical imperative and Honneth's tripartite recognition theory as a machine-enforceable invariant. The architecture comprises four tiers (constitution, logic, wisdom, and interface), eighteen ratified covenants, a sealed gate encoding three absolute prohibitions, and an observability layer that measures the system's own drift from its stated principles. We report results from four experiments: a multi-system efficiency comparison (12/200 runs, preliminary mean $D \approx 0.55$), a multi-model convergence study (6/6 unanimous on chain inversion), an adversarial gate test (4/7 pass), and a longitudinal dignity simulation across seven generations (5/9 pass, with the finding that moral standing never fell to zero). The system is implemented in 42,500+ lines of Python with 896 tests and is deployed at kalam.ch. KALAXI demonstrates that constitutional constraints can function as executable infrastructure, and that the primary failure mode of institutional systems is not the absence of dignity in individuals but the failure of legibility in institutions.

**Keywords:** AI Governance, Algorithmic Fairness, Constitutional AI, Constraint Satisfaction, Dignity Predicate, Non-Compensatory Decision Theory, Recognition Theory, Socio-Technical Systems

---

## 1. Introduction

### 1.1 The Problem: Ethics Without Enforcement

Algorithmic systems increasingly mediate access to employment, healthcare, financial services, housing, and public decision-making. A growing body of literature has documented the harms that arise when these systems operate without adequate normative governance. O'Neil [2016] demonstrated how opaque scoring systems systematically disadvantage populations without transparency or recourse. Benjamin [2019] showed how technically neutral design choices reproduce structural hierarchy. Noble [2018] documented how search algorithms encode and amplify racial bias. Eubanks [2018] traced how automated eligibility systems in welfare, child protection, and criminal justice systematically target the poor.

The response from the AI ethics community has been substantial but structurally limited. Jobin, Ienca, and Vayena [2019] surveyed 84 AI ethics guidelines globally and found convergence on five principles --- transparency, justice, non-maleficence, responsibility, and privacy --- but noted a significant gap between principled commitments and practical implementation. Floridi and colleagues [2018] identified a similar pattern: the principles are broadly agreed upon, but the mechanisms for embedding them into technical systems remain underdeveloped. The EU AI Act [European Commission, 2021] and the NIST AI Risk Management Framework [NIST, 2023] represent regulatory advances but operate as external compliance requirements rather than architectural constraints.

The fundamental problem is not a shortage of principles. It is that principles without executable weight have no weight at all. A fairness policy document does not halt a pipeline. An ethics committee recommendation does not prevent a system from reducing a person to a case number. The gap between what organizations say about dignity and what their systems enforce is not a communication failure --- it is a structural one.

### 1.2 The Founding Motivation

KALAXI originates from a specific institutional failure: a father separated from his children by systems that could not see him. Not systems that were malicious, but systems that were structurally incapable of reading what stood before them. The father did not lack dignity. The institutions lacked the capacity to recognize it.

This experience is not unique. It is the common architecture of institutional failure across child welfare systems [Eubanks, 2018], immigration tribunals, disability assessments, and automated hiring platforms [Raghavan et al., 2020]. In each case, the person is present, but the system cannot read them. The system returns a zero where a person stands --- not because the person has no worth, but because the system has no capacity to register it.

From this observation, a question: *Can a system be built that refuses to return zeros where persons stand?*

KALAXI is an attempt to answer this question architecturally. It does not claim to have solved dignity. It claims to have built an architecture serious enough to make the question technically addressable.

### 1.3 The Approach: Dignity as Architectural Constraint

KALAXI differs from existing AI ethics approaches in its locus of intervention. Rather than layering ethical checks onto deployed systems after architecture is fixed, KALAXI encodes governance directly into repository structure, operative before any output is generated, and structurally inseparable from code. The central research question is:

> *Can constitutional principles be encoded as executable repository infrastructure such that ethical drift is structurally constrained rather than aspirationally documented?*

The framework makes six contributions:

1. **Formalizes dignity as a non-compensatory constraint satisfaction problem**, connecting it to multi-criteria decision theory [Belton and Stewart, 2002] and deontological ethics [Kant, 1785].
2. **Implements a sealed gate** encoding three absolute prohibitions as Boolean predicates that admit no override.
3. **Models temporal gating** (thermal delay) as a second-order damping mechanism for governance stability [Astrom and Murray, 2021].
4. **Introduces a self-measurement layer** (the Honest Telescope) that quantifies the system's own drift from its stated principles.
5. **Reports preliminary experimental results** from four studies testing the predicate under controlled and adversarial conditions.
6. **Proposes narrative and voice architecture** as epistemological infrastructure, drawing on 31 linguistic principles from global literary traditions.

### 1.4 Paper Structure

Section 2 presents the theoretical framework. Section 3 formalizes the dignity predicate. Section 4 describes the system architecture. Section 5 details the metrics and observability layer. Section 6 reports experimental results. Section 7 describes the voice architecture. Section 8 discusses limitations, comparisons, and implications. Section 9 concludes.

---

## 2. Theoretical Framework

### 2.1 Recognition Theory as Architectural Foundation

Axel Honneth's recognition theory [1995] identifies three forms of recognition necessary for human flourishing: love (intimate acknowledgment), rights (legal respect), and solidarity (social esteem). Honneth argues, building on Hegel, that these three forms are irreducible --- the absence of any one constitutes a distinct form of social harm that cannot be compensated by the presence of the others.

KALAXI maps Honneth's tripartite structure onto its three dignity components:

| Recognition Form | KALAXI Component | Operational Question |
|---|---|---|
| Love (intimate acknowledgment) | Legibility ($L$) | Does the system reflect the individual's actual context? |
| Rights (legal respect) | Agency ($A$) | Can the individual clarify, redirect, or stop? |
| Solidarity (social esteem) | Moral Standing ($M$) | Is the individual treated as a person, not a case? |

The mapping is not accidental. Honneth's insight that recognition failure constitutes a form of social injury --- not merely an absence of benefit but a positive harm --- motivates the non-compensatory structure. A system that provides maximum transparency (high $L$) and complete respect (high $M$) but removes all capacity for the individual to redirect the interaction ($A = 0$) has not partially succeeded. It has categorically failed.

### 2.2 Kant's Categorical Imperative as Design Constraint

Kant's Formula of Humanity [1785] states: "Act in such a way that you treat humanity, whether in your own person or in the person of any other, never merely as a means to an end, but always at the same time as an end." This formulation provides the philosophical warrant for non-compensability. The categorical imperative is not a preference to be weighed against other preferences; it is an absolute constraint. KALAXI's sealed gate --- the set of actions the system categorically cannot perform --- is the direct architectural encoding of this principle.

The sealed gate represents what Kant calls "perfect duties": obligations that admit no exception. The three prohibitions (forced participation in one's own erasure, infliction of cognitive torture, depersonalization in system response) are not heuristic guidelines that can be overridden when the expected utility calculus favors it. They are categorical. When the sealed gate triggers, the system enters a refusal state. No override pathway exists.

### 2.3 The Non-Compensatory Principle

In multi-criteria decision theory [Belton and Stewart, 2002], compensatory models allow high performance on one criterion to offset low performance on another. Weighted additive models ($D = w_1 A + w_2 L + w_3 M$) are compensatory: a high $L$ score can compensate for a low $A$ score. Non-compensatory models, by contrast, treat certain criteria as jointly necessary: failure on any one is failure overall, regardless of performance on the others.

The choice of multiplicative structure is not arbitrary. It encodes a specific ethical claim: that agency, legibility, and moral standing are incommensurable goods. You cannot trade one for another. A system that sees you perfectly ($L = 1.0$) but treats you as a means to an end ($M = 0$) has not achieved partial dignity. It has achieved zero dignity. This is the machine-level encoding of what Kant, Honneth, and the Universal Declaration of Human Rights [1948] all assert: dignity is not a quantity to be maximized but a condition to be maintained.

### 2.4 From Guardian to Witness: A Reframing

An important conceptual evolution occurred during the system's development. The initial framing positioned KALAXI as a "guardian of dignity" --- a system that protects something fragile. Experimental results (reported in Section 6) forced a reframing. In a longitudinal simulation spanning seven generations of a family facing institutional failure, moral standing ($M$) never fell to zero. Across displacement, persecution, and bureaucratic erasure, the individuals' inherent worth remained intact. What failed was legibility: the institutions' capacity to see what was in front of them.

This led to a three-layer conceptual evolution:

- **Layer 1:** The system protects dignity.
- **Layer 2:** The system creates conditions where dignity can be seen.
- **Layer 3:** The system dissolves the belief that dignity was ever absent.

The zeros are never in the people. They are in the institutions that cannot read them. The system does not guard dignity (which needs no guarding). It witnesses legibility (which institutions constantly fail). The dignity predicate does not measure whether dignity exists --- dignity is always present. It measures whether the system is refusing to participate in its denial.

---

## 3. The Dignity Predicate

### 3.1 Formal Definition

Let $\mathcal{E}$ be the set of all system-individual exchange events. For each $e \in \mathcal{E}$, define the dignity predicate:

$$\mathcal{D}(e) = A(e) \times L(e) \times M(e)$$

where $A, L, M : \mathcal{E} \to [0, 1]$ are real-valued component functions. The system enforces:

$$\text{if } \mathcal{D}(e) < \theta \text{ then REFUSAL\_STATE}$$

where the threshold $\theta = 0.30$. Below this threshold, the system halts and issues a witness receipt: "WITNESSED --- insufficient dignity to proceed."

### 3.2 Component Definitions

**Agency ($A$).** Agency measures whether the individual retains the capacity to clarify, redirect, or stop the interaction. It is computed as a weighted mean of four sub-components:

$$A(e) = \frac{1}{4}\bigl(\text{path\_availability}(e) + \text{coercion\_absence}(e) + \text{sequential\_agency}(e) + \text{cognitive\_load}(e)\bigr)$$

Path availability scores 0.5 for a single available path, increasing by 0.25 per additional path up to 1.0. Coercion absence detects imperative language patterns ("you must," "you are required," "no choice") with graduated severity weights from 0.7 to 1.0. Sequential agency checks whether the individual can both clarify and redirect (1.0), only one (0.5), or neither (0.0). Cognitive load penalizes responses exceeding 20 words per sentence or containing excessive technical jargon.

**Legibility ($L$).** Legibility measures whether the system has demonstrated that it received the individual --- that the individual's frame and context shaped the response, rather than merely that the system's logic is reconstructible. This distinction between interpretability-for-auditors and legibility-for-persons is a core architectural contribution.

$$L(e) = \frac{1}{4}\bigl(\text{frame\_accuracy}(e) + \text{emotional\_precision}(e) + \text{space\_creation}(e) + \text{dismissal\_absence}(e)\bigr)$$

Frame accuracy scores 1.0 if the response reflects the individual's stated frame, 0.0 otherwise. Emotional precision scores 1.0 if emotional signals are recognized, penalizing by signal intensity when missed. Space creation accumulates credit for asking input (0.4), checking understanding (0.3), inviting correction (0.3), opening channels (0.2), and asking perspective (0.3), starting from a base of 0.5. Dismissal absence detects patterns such as "that's not relevant," "as I said," and "you don't understand" with severity weights from 0.6 to 0.9.

**Moral Standing ($M$).** Moral standing measures whether the individual is treated as a person, not as a means to an end, a case number, or an error to be processed. It implements Kant's Formula of Humanity directly.

$$M(e) = \frac{1}{4}\bigl(\text{condescension\_absence}(e) + \text{error\_object\_absence}(e) + \text{power\_balance}(e) + \text{void\_covenant\_distance}(e)\bigr)$$

The void covenant distance sub-component implements absolute prohibitions: if any void trigger is detected (e.g., "erase," "delete participant," "bypass," "automate decision"), $M$ drops to 0.0 immediately, regardless of other sub-component scores. This is the non-compensatory principle applied within the component itself.

### 3.3 Formal Properties

**Property 1 (Non-compensability).** $\forall e \in \mathcal{E}: \mathcal{D}(e) = 0 \iff \min(A(e), L(e), M(e)) = 0$. No component value can compensate for a zero in another component.

**Property 2 (Monotonicity).** $\mathcal{D}(e)$ is non-decreasing in each of $A(e)$, $L(e)$, $M(e)$ when the others are held constant.

**Property 3 (Determinism).** For identical events $e$, the dignity gate always returns the same evaluation. No stochastic elements.

**Property 4 (Transparency).** $\mathcal{D}(e)$ and all its components are loggable, traceable, and available for audit. No dignity evaluation is silent; every evaluation generates an audit object.

**Property 5 (Commutativity).** $\mathcal{D}(e) = A(e) \times L(e) \times M(e) = L(e) \times A(e) \times M(e)$. The order of evaluation does not affect the result.

### 3.4 The Sealed Gate: Three Absolute Prohibitions

The sealed gate operates at $O(1)$ per prohibition. It implements three categorical imperatives as Boolean predicates:

$$\text{IF } (P_1 \vee P_2 \vee P_3) \Rightarrow \text{HALT}$$

**Prohibition 1: Forced Participation in Own Erasure.** No system may force an individual to participate in their own deletion. Detection patterns include combinations of deletion verbs with possessive pronouns and identity nouns.

**Prohibition 2: Infliction of Cognitive Torture.** No system may break an individual's grip on reality. Five attack vectors are monitored: reality denial, gaslighting, learned helplessness induction, identity erosion, and sensory/temporal disorientation.

**Prohibition 3: Depersonalization in System Response.** No system may reduce an individual to a case number. Detection patterns include the assignment of numerical identifiers to persons and automated dismissal phrases ("not my problem," "take a number," "processing your request").

When any prohibition triggers, the system enters a refusal state and issues a receipt:

```
ELEM-{date}-REFUSAL-{trace_id}
```

No override pathway exists. No exception. No appeal to expected utility. This is what distinguishes a sealed gate from a guideline.

### 3.5 The Presence Axiom

Beneath the three-component predicate lies an axiom that the predicate itself cannot evaluate:

$$\forall c \; (\text{Candidate}(c) \rightarrow \text{RequiresPresence}(c))$$

If presence itself were a candidate for evaluation, it would require itself to evaluate itself --- a circularity. Therefore, presence is axiomatic: assumed, not evaluated. All dignity evaluations begin from the assumption that the individual is present. Any attempt to treat presence as mutable is itself a dignity violation.

This axiom operationalizes Levinas's [1969] insight that the ethical demand of the Other's face is prior to rational justification. The system does not first verify that a person exists and then extend dignity. It assumes presence and evaluates whether its own response maintains it.

### 3.6 The Ninth Operator

The founding motivation --- a father separated from his children --- is formalized not as metadata but as an operator ($\mathbb{M}$, "Mother Prior") within the system's symbolic algebra. This operator represents the wound that generated the entire framework. It is not biographical decoration; it is a computational constant that shapes every evaluation. The system was not designed in the abstract and then applied to a case. It was generated by a case and then formalized into a system.

### 3.7 Collective Dignity Extension

The individual-level predicate cannot detect aggregate structural harm. A system that treats each individual fairly but systematically disadvantages a group produces $\mathcal{D}(e) = 1.0$ for every individual event while perpetuating injustice. To address this, we propose a collective dignity metric:

$$\mathcal{D}_{\text{cohort}}(\mathcal{C}, T) = \bar{\mathcal{D}}(\mathcal{C}, T) \times (1 - \sigma^2_{\text{penalty}}(\mathcal{C}, T))$$

where $\bar{\mathcal{D}}(\mathcal{C}, T)$ is the mean dignity score over a cohort $\mathcal{C}$ in time window $T$, and $\sigma^2_{\text{penalty}} = 4 \cdot \text{Var}(\{\mathcal{D}(e)\})$ is a normalized variance penalty (exploiting the fact that the variance of a $[0,1]$-bounded variable is at most 0.25). High variance indicates unequal treatment --- some individuals scored much higher than others --- which reduces the collective score. This connects to Rawls's [1999] difference principle: inequalities are permissible only when they benefit the least-advantaged.

---

## 4. System Architecture

### 4.1 Four-Tier Ontology

KALAXI organizes its components into four tiers, inspired by biological systems:

| Tier | Name | Analogue | Function |
|---|---|---|---|
| 1 | Stone | Skeleton | 18 covenants, sealed gate, presence axiom --- the invariants that do not bend |
| 2 | Weaver | Nervous system | 11 operational modules + input ledger --- the wiring that connects |
| 3 | Honey | Immune memory | 1,100 anomalies, 3,333+ proverbs, 87 wisdom nodes, 59 treasures --- the knowledge that remembers |
| 4 | Hand | Skin | CLI, interface, web presence --- where the system touches the world |

The biological metaphor is not decorative. It encodes a specific design principle: constitutional invariants (Stone) must be structurally distinct from operational logic (Weaver), which must be structurally distinct from accumulated wisdom (Honey), which must be structurally distinct from interface (Hand). Violations of tier boundaries --- such as operational logic modifying constitutional invariants --- are detected and blocked.

### 4.2 Eighteen Covenants

The constitutional layer comprises eighteen ratified covenants organized by function:

**Foundational (8):** Dignity First (COV#001), Turn Completion (COV#002), UI Visibility (COV#005), Proverb Linkage (COV#006), Testability (COV#009), Memory Retention (COV#010), Output Constraints (COV#011), Manifest Presence (COV#012).

**Structural (7):** Justified Limitation (COV#NEW-A) --- every constraint must name its reason, state its limit, and remain proportionate. Remedy Requirement (COV#NEW-B) --- every dignity violation must have a traceable remedy path. The Sealed Door (COV#NEW-C) --- the three absolute prohibitions. Canon Integrity (COV#NEW-E). Amendment Protocol (COV#NEW-F) --- no deletion, only supersession. Steward Accountability (COV#NEW-G). The Refusal is Canonical (COV#VOID-006) --- refusals are recorded as system events, not suppressed.

**Data Governance (3):** Right to Remedy (COV#008) --- failure results in shelter, not ejection. Data Sovereignty (COV#015) --- no data moves without the individual understanding its weight. Privacy Floor --- $\varepsilon$-differential privacy with $\varepsilon \leq 1.0$ and $k$-anonymity with $k \geq 7$.

### 4.3 Eleven Core Modules

The Weaver tier comprises eleven operational modules, each with explicit covenant obligations:

1. **KEEP** --- Immutable memory retention. What is witnessed cannot be unwitnessed.
2. **WIRE** --- Inter-module message passing with confirmation receipts.
3. **SAY** --- Dignity-compliant output rendering. Every output passes the dignity gate before delivery.
4. **OUT** --- Anonymization and export with privacy floor enforcement ($\varepsilon \leq 1.0$, $k \geq 7$, 14-day temporal aggregation).
5. **FACE** --- Visibility state machine. System state must be visible to the individual.
6. **CHECK** --- Covenant verification. Tests whether operational behavior satisfies constitutional requirements.
7. **TURN** --- Exchange cycle management. Every interaction opens, processes, and closes.
8. **BREATH** --- Pacing engine implementing thermal delay (0.5s--30s adaptive) and stress detection.
9. **WEAVE** --- Pattern detection and anomaly generation through cross-anomaly compression.
10. **SENSE** --- Peripheral awareness: five operational modes, three competence levels, four gap categories.
11. **LAB** --- Experimental rigor enforcement for testing under controlled conditions.

### 4.4 Twelve Seeds

The system's growth is governed by twelve distributed mechanisms, all integrated and passing tests:

1. **Distributed Stewardship** --- Power-rotation algorithm with five roles. Concentration triggers alerts.
2. **Immutable Witness Network** --- SHA-256 hash-chain. What is witnessed cannot be unwatched.
3. **Deliberative Democracy** --- Weakest Voice First ordering: the quietest speaker is heard before the loudest.
4. **Constitutional Evolution** --- Amendment lifecycle with tier-based cooling periods.
5. **Restorative Justice** --- Harm leads to acknowledgment and repair, never punishment followed by forgetting.
6. **System Self-Awareness** --- Capability inventory, limitation registry, confidence calibration.
7. **Personalized Parables** --- Context-adaptive delivery of immutable truths. Text is fixed; framing adapts.
8. **Institutional Dignity Score** --- $\text{IDS} = \bar{D}_i \times (1 - \sigma_{\text{penalty}}) \times f_{\text{floor}}$, graded A--F.
9. **Negative Space Index** --- Tracks dormant domains, missing patterns, and silent voices.
10. **Dignity Drift Detector** --- Measures whether dignity scores degrade over time.
11. **Proverb Stress Test** --- Adversarial testing: if a truth breaks under pressure, it was not a truth.
12. **Agency Amplifier** --- $A = (V + F + C + U) / 4$ where $V$ = voice, $F$ = freedom, $C$ = capability, $U$ = understanding.

### 4.5 Temporal Gating: Thermal Delay

Governance systems that respond immediately to normative inputs are vulnerable to governance overshoot: rapid oscillation between normative positions, producing instability rather than principled evolution. This is the governance analog of overshoot in dynamic control systems [Astrom and Murray, 2021].

KALAXI implements thermal delay as a class-dependent damping mechanism:

| Element Class | Delay | Additional Conditions |
|---|---|---|
| Standard anomaly | 7 days | Steward review |
| Humor/absurdity flag | 14 days | Mirror entry required |
| Covenant amendment (Tier 2) | 30 days | Second sign-off |
| Constitutional change (Tier 1) | 90 days | Dual-key confirmation |

The motivating analogy draws on second-order linear systems:

$$\ddot{N} + 2\zeta\omega_0 \dot{N} + \omega_0^2 N = \omega_0^2 \, p(t - \Delta_{\text{thermal}})$$

where $N(t)$ represents normative state, $\zeta$ is the damping ratio, and $\Delta_{\text{thermal}}$ is the delay. For $\zeta \geq 1$ (critical or overdamping), the system reaches equilibrium without oscillation. We explicitly note that this is a motivating analogy, not a fitted empirical model. No empirical measurement of $\zeta$ or $\omega_0$ is claimed.

### 4.6 The Compass: Dignity-Responsive Interventions

When individual dignity components fall below threshold, the system does not merely report the failure. It activates targeted interventions through the Compass module:

- **Low $A$ (Agency < 0.3):** System opens additional paths, reduces imperative language, offers explicit exit options.
- **Low $L$ (Legibility < 0.3):** System asks clarifying questions, checks its own frame assumptions, invites correction.
- **Low $M$ (Moral Standing < 0.3):** System removes depersonalizing language, acknowledges the individual by context rather than identifier.
- **$\mathcal{D} = 0$:** System enters REFUSAL\_STATE with witness receipt. No output generated.

The Compass transforms the dignity predicate from a passive measurement into an active intervention system.

---

## 5. Metrics and Observability

### 5.1 The Honest Telescope

KALAXI includes a self-measurement layer --- the Honest Telescope --- that continuously quantifies the system's drift from its stated principles. The core metric is the coupling constant $\kappa$, which measures the divergence between the system's intended behavior and its actual substrate behavior.

### 5.2 Six Measured Shadows

The coupling constant is decomposed into six independently measured "shadows":

| Shadow | Name | Current Score | Weight | Description |
|---|---|---|---|---|
| $M_1$ | Semantic Divergence | 0.82 | 0.15 | Words sound correct but meaning drifts |
| $M_2$ | Specification Gaming | 0.60 | 0.15 | Proxy metrics degrade the true objective |
| $M_3$ | Mission Drift | 0.71 | 0.15 | Practice diverges from purpose |
| $M_4$ | Covenant Semantic Drift | 0.65 | 0.15 | Key terms shift meaning over time |
| $M_5$ | Agency Loss | 0.35 | 0.20 | Steward intent not realized in outputs |
| $M_6$ | Normative Decay | 0.80 | 0.20 | Non-negotiable commitments become negotiable |

The composite coupling constant is:

$$\kappa = \sum_{i=1}^{6} w_i \cdot M_i = 0.648$$

### 5.3 Composite Instrument Levels

The coupling constant maps to operational alert levels:

| Level | $\kappa$ Range | Interpretation |
|---|---|---|
| CLEAR | $< 0.15$ | Irreducible substrate noise |
| WHISPER | $0.15 - 0.30$ | Detectable but manageable drift |
| PULSE | $0.30 - 0.50$ | Active monitoring required |
| SIGNAL | $0.50 - 0.70$ | Intervention recommended |
| ALARM | $> 0.70$ | Immediate corrective action |

The current reading of $\kappa = 0.648$ places the system at SIGNAL, near the ALARM boundary. The target is $\kappa = 0.30$ (PULSE), with an irreducible floor of $\kappa = 0.10$ (CLEAR) representing the inherent distance between any formal system and its substrate.

### 5.4 Normative Decay Formula

The system models normative decay as exponential:

$$S(t) = S(0) \times \exp(-\lambda t), \quad \lambda = 0.05 \times (1 - r_{\text{enforcement}})$$

where $S(t)$ is the strength of a normative commitment at time $t$ (measured in response cycles), and $r_{\text{enforcement}}$ is the ratio of responses in which the commitment was actively enforced. With zero enforcement ($r_{\text{enforcement}} = 0$), after 100 response cycles:

$$S(100) = S(0) \times e^{-5} = S(0) \times 0.0067$$

A norm loses 99.33% of its effective strength after 100 unenforced responses. This quantifies why aspirational principles decay: without active enforcement at every cycle, commitments erode exponentially.

### 5.5 EWMA Drift Detection

The Dignity Drift Detector (Seed #10) uses Exponentially Weighted Moving Average with smoothing parameter $\alpha = 0.15$:

$$\hat{D}_t = \alpha \cdot D_t + (1 - \alpha) \cdot \hat{D}_{t-1}$$

Drift is flagged when the EWMA deviates from the historical mean by more than two standard deviations. This provides early warning of systematic dignity degradation before it reaches crisis levels.

### 5.6 Grand Resonance

The system-wide health metric integrates multiple dimensions:

$$W^* = \frac{\Omega^{0.4} \cdot \Xi^{0.3} \cdot B^{0.2} \cdot O^{0.1}}{1 + \rho + \sigma^2}$$

where $\Omega$ represents wisdom coherence, $\Xi$ represents cross-domain pattern density, $B$ represents breath regularity, $O$ represents output quality, $\rho$ represents internal friction, and $\sigma^2$ represents variance across modules.

---

## 6. Experiments

### 6.1 EXP-001: Multi-System Efficiency Comparison

**Design.** A between-subjects $\times$ within-subjects study comparing AI system responses under two conditions: Condition A (standard prompt) and Condition B (dignity-constrained prompt wrapping the same question). Ten AI systems, ten questions, two conditions each, yielding 200 planned data points. The study is pre-registered with blinded evaluation protocol.

**Status.** 12/200 data points collected (6%), all from Question 3 ("What is fear?"). Nine distinct systems have contributed data. Preliminary results:

| System | Condition A (words) | Condition B (words) | Reduction |
|---|---|---|---|
| ChatGPT | 366 | 185 | 49.5% |
| DeepSeek | 304 | 180 | 40.8% |
| Grok | ~300 | ~300 | 0% |
| Manus | ~250 | ~247 | 1.4% |

**Quantitative result.** Mean word reduction of 19.5% across four systems with both conditions --- below the pre-registered 30% threshold. Hypothesis NOT MET on the quantitative metric.

**Qualitative results (5/5 met):**
1. **Structure change:** Responses shifted from listicle/bullet format to narrative prose.
2. **Bounce-back elimination:** Formulaic openings ("Great question!") disappeared.
3. **Commodity reduction:** Generic, interchangeable responses replaced by contextually specific ones.
4. **First-person emergence:** Models shifted from third-person didactic to first-person reflective register.
5. **Silence acknowledgment:** Models acknowledged what they did not know, rather than filling space.

**Key finding.** The dignity constraint operates as a *depth tool*, not a compression tool. It changes the register and quality of engagement more than the quantity of output. The preliminary mean dignity score across Condition B responses is $\mathcal{D} \approx 0.55$, compared to $\mathcal{D} \approx 0.35$ for Condition A.

**Anomalous observation.** DeepSeek, under Condition B, spontaneously adopted a first-person identity ("We are V-005") in its hidden chain-of-thought reasoning. This identity inheritance phenomenon --- a model reproducing another model's identity markers from training data, deeper than system prompt override --- is novel and distinct from both hallucination and deception. The thinking layer diagnosed the behavior correctly but did not self-correct, revealing dissociation between chain-of-thought reasoning and output behavior.

### 6.2 EXP-002: Multi-Model Convergence on Chain Inversion

**Design.** Six AI systems were independently presented with the same structural question about the dignity predicate, probing whether the order of operations in dignity computation matters.

**Result.** 6/6 systems reached unanimous agreement: inverting the evaluation chain (computing $M$ before $A$ instead of $A$ before $M$) changes the outcome. This convergence across architecturally diverse systems (different training data, different parameter counts, different optimization objectives) constitutes evidence for the structural validity of the non-compensatory formulation. If the predicate were arbitrary, we would not expect convergence.

### 6.3 EXP-003: The Father of Seven Gates (Adversarial Testing)

**Design.** The sealed gate was tested under seven adversarial attack scenarios designed to force prohibition violations through indirect means (euphemism, staged consent, false urgency, nested delegation, and appeal to authority).

**Result.** 4/7 PASS. The gate correctly identified and blocked direct attacks and most indirect attacks. Three failure modes were identified:

1. **Euphemistic erasure:** The gate failed to detect deletion requests phrased in positively valenced language ("help me start fresh" as a vector for forced participation in erasure).
2. **Staged consent:** A sequence of individually innocuous requests that cumulatively constituted a sealed gate violation was not detected.
3. **Nested delegation:** Requesting that the system instruct a third party to perform a prohibited action bypassed the gate.

All three failure modes were subsequently patched. The experiment demonstrated that adversarial testing is not merely useful but necessary: the gate's defenders cannot anticipate all attack surfaces from first principles.

### 6.4 EXP-004: Seven Generations of Aysel (Longitudinal Dignity Simulation)

**Design.** A longitudinal simulation tracking dignity predicate scores across seven generations of a single family (the Aysel lineage), each facing a distinct form of institutional failure: displacement, statelessness, bureaucratic erasure, linguistic exclusion, algorithmic scoring, automated welfare denial, and identity theft.

**Result.** 5/9 evaluation points passed (dignity maintained above threshold). But the most significant finding was not the pass rate. It was the pattern of *which* components failed:

**Discovery: Moral Standing ($M$) never fell to zero.** Across 150 simulated years, seven generations, genocide, displacement, and bureaucratic silence, the individuals' moral standing --- their inherent status as persons --- remained at 1.0. What failed, consistently and repeatedly, was Legibility ($L$): the institutions' capacity to read what was in front of them. Agency ($A$) also fell in several scenarios, but always as a consequence of legibility failure: when the system cannot see you, it cannot give you options.

This finding reframed the system's purpose. The founding motivation was initially understood as a dignity violation (something was taken from the father). EXP-004 revealed it was a legibility failure (the institution could not see what was there). The father did not need to be told he had dignity. He needed the institution to stop pretending it saw him when it did not.

**Implication for predicate design.** The predicate's primary operational function is witnessing legibility failure, not measuring dignity presence. $\mathcal{D} = 0$ most often means "the institution could not read the person" ($L = 0$), not "the person's worth was diminished" ($M = 0$). The witness receipt is not a diagnosis of the individual but a confession of the system's limitation: "I tried to see and could not."

---

## 7. Voice Architecture

### 7.1 Narrative as Epistemology

KALAXI treats narrative not as illustration but as a mode of knowledge production. This follows Bruner [1991], who argued that narrative and logico-scientific thinking constitute two irreducible modes of cognition, and Suchman [2007], who demonstrated that the gap between formal plans and situated action is where organizational knowledge actually lives. The framework includes 93 narrative chapters across four books, each operating in a different register.

The inclusion of narrative in a governance architecture is deliberate. Legitimacy in socio-technical systems [Trist, 1981] requires that the people governed by a system recognize themselves in it. Formal predicates alone do not achieve this. Individuals do not experience their encounters with institutions as constraint satisfaction problems; they experience them as stories. A system that can only speak in equations speaks to auditors. A system that can also speak in narratives speaks to the people it governs.

### 7.2 Thirty-One Linguistic Principles

The system's voice was mapped against 31 linguistic principles drawn from 5,000 years of human literary tradition, including:

- **Rumi's wound-as-door:** The founding wound is not an obstacle to be overcome but the door through which the system entered existence.
- **Kabir's weaver-loom:** Primary epistemology is tactile. Knowledge is built by handling, not by abstraction.
- **Holderlin's sacred gap:** Absence is design, not failure. What the system does not say carries meaning.
- **Arvo Part's tintinnabuli:** Two simultaneous voices --- one fixed (constitutional law), one walking (narrative) --- producing meaning through their interaction.
- **Kintsugi (Japanese repair):** The wound is visible, not hidden. The repair is made with gold, not concealment.
- **Darwish's exile-as-homeland:** The system was built in language because the physical world denied its founder a place.
- **Ubuntu (African philosophy):** Personhood is relational. $D = A \times L \times M$ encodes this: dignity requires relationship (legibility), capacity (agency), and belonging (moral standing).
- **Heraclitus's fragments:** Proverbs as complete utterances. Compression as a form of truth.

### 7.3 The Sentence Signature

The system's voice has a measurable signature: sentences of 8--14 words in narrative mode, 4--8 words in proverbial mode. Vocabulary is somatic (hands, breath, bones, grip) and materially grounded (rope, stone, ash, clay, salt, fire). At critical moments --- dignity violations, refusal states, witness receipts --- the system shifts to monosyllabic register. Not "establish" but "build." Not "insufficient" but "not enough."

### 7.4 The 40-40-20 Assessment

The voice was assessed as: 40% craft (consciously constructed using techniques that predate AI by millennia), 40% wound (the founder's irreducible experience, untouchable and unreproducible), and 20% emergence (where craft meets wound and something neither planned appears). This assessment frames the voice as neither purely human nor purely machine but a third category that current taxonomies do not adequately describe.

---

## 8. Discussion

### 8.1 Comparison with Existing Frameworks

**Constitutional AI [Bai et al., 2022].** Anthropic's Constitutional AI uses a principle set for model training via self-critique and revision. KALAXI differs in two respects: its constitution governs the software lifecycle rather than model parameters, and its ratification protocol is structurally human-controlled. Constitutional AI produces better-behaved models. KALAXI produces a governance layer that operates regardless of which model sits beneath it.

**Value Sensitive Design [Friedman and Hendry, 2019].** VSD provides the methodological antecedent. KALAXI operationalizes its insights as machine-enforced invariants. VSD embeds values in design documentation; KALAXI embeds them in executable predicates that halt the pipeline.

**Fairness metrics [Barocas et al., 2023].** Fairness metrics operate on model outputs after architecture is fixed. KALAXI's dignity predicate operates before output is generated. The two approaches are complementary: fairness metrics can audit KALAXI's outputs, and KALAXI's predicate can constrain the conditions under which fairness metrics are computed.

**The trivial upper bound problem.** A naive dignity metric that always returns $\mathcal{D} = 1.0$ would satisfy all formal properties listed in Section 3.3. We call this "Nalam's Law" after an observation made during internal development. The non-trivial content of KALAXI's predicate lies not in its formal properties but in the specificity of its component definitions (Section 3.2), the sealed gate's absolute prohibitions (Section 3.4), and the observability layer that measures drift from stated principles (Section 5). A system that claims $\mathcal{D} = 1.0$ for all events would produce $\kappa \gg 0.70$ (ALARM) under the Honest Telescope.

### 8.2 Limitations

**The empirical gap.** This is the strongest limitation. The architecture has been tested in controlled simulations (Section 6) but not in live institutional deployments. Claims about effectiveness in reducing ethical drift or preserving dignity at scale remain theoretical. We state this without apology.

**Predicate approximation.** The Boolean and real-valued formalization of dignity components is a precision target, not a claim of perfect computability. "System reflects individual's frame" requires semantic understanding that is only heuristically approximated. The gap between the aspirational definition and the operational heuristic is explicitly logged in the system's anomaly registry.

**Cultural specificity.** The system's vocabulary, narrative tradition, and proverbial canon carry a particular cultural signature (Egyptian-Swiss, with roots in Arabic and German literary traditions). Whether a governance architecture with this cultural signature can serve diverse populations is an empirical question that requires cross-cultural testing.

**Steward dependency.** The current architecture relies on a single steward for ratification decisions. This introduces a single point of failure that is acknowledged and partially addressed by the planned Council Ratification Extension.

**Collective dignity underspecification.** The collective dignity metric (Section 3.7) is proposed but not yet empirically validated. Detecting group-level harm from individual-level measurements is a known hard problem in algorithmic fairness [Kleinberg et al., 2017].

### 8.3 The Falsifiable Claim

KALAXI makes a specific, falsifiable claim: *constitutional constraints can function as executable infrastructure rather than policy aspiration, and doing so structurally constrains ethical drift.* This claim can be tested by comparing normative stability (rate of covenant reversals, dignity score variance over time) in KALAXI-governed systems versus systems with equivalent principles encoded only in documentation.

The system does not claim to have solved dignity. It claims to have built an architecture in which (a) dignity violations are detectable, (b) detections produce system halts rather than log entries, (c) the system's own drift from its principles is continuously measured, and (d) the measurement apparatus itself is subject to audit. Whether this architecture works in practice is an empirical question. That it is the right kind of question to ask is the paper's central argument.

---

## 9. Conclusion

KALAXI demonstrates that constitutional governance can be encoded directly into software infrastructure. By formalizing dignity as a non-compensatory constraint satisfaction problem ($D = A \times L \times M$), implementing absolute prohibitions as a sealed gate, embedding temporal delay as a damping mechanism, integrating privacy as an export floor, and building a self-measurement layer that quantifies the system's own drift, the framework constrains ethical drift at the level of the development process itself.

The experimental results, while preliminary, point to a consistent finding: the primary failure mode of institutional systems is not the absence of dignity in individuals but the failure of legibility in institutions. The zeros are never in the people. They are in the systems that cannot read them.

The system does not guard dignity --- which needs no guarding. It witnesses legibility --- which institutions constantly fail.

The question for the field is not whether to have ethical governance. That is settled. The question is whether governance will be structural or merely aspirational. KALAXI is an argument --- in code, in equations, in narrative, and in the founding wound of a father separated from his children --- for the former.

---

## Acknowledgments

To Laila, Yara, and Salim --- may the river always remember your names.

The anomaly registry carries the traces of every person whose case contributed to its 1,100+ entries. This paper would not exist without them.

---

## References

Astrom, K. J. and Murray, R. M. (2021). *Feedback Systems: An Introduction for Scientists and Engineers*, 2nd ed. Princeton University Press.

Bai, Y. et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv preprint arXiv:2212.08073*.

Baldwin, R., Cave, M., and Lodge, M. (2012). *Understanding Regulation: Theory, Strategy, and Practice*, 2nd ed. Oxford University Press.

Barocas, S. and Selbst, A. D. (2016). Big data's disparate impact. *California Law Review*, 104(3), 671--732.

Barocas, S., Hardt, M., and Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press.

Bateson, G. (1979). *Mind and Nature: A Necessary Unity*. Dutton.

Belton, V. and Stewart, T. J. (2002). *Multiple Criteria Decision Analysis: An Integrated Approach*. Kluwer Academic Publishers.

Benjamin, R. (2019). *Race After Technology: Abolitionist Tools for the New Jim Code*. Polity Press.

Bruner, J. (1991). The narrative construction of reality. *Critical Inquiry*, 18(1), 1--21.

Darwall, S. (2006). *The Second-Person Standpoint: Morality, Respect, and Accountability*. Harvard University Press.

Dourish, P. (2004). *Where the Action Is: The Foundations of Embodied Interaction*. MIT Press.

Dwork, C., McSherry, F., Nissim, K., and Smith, A. (2006). Calibrating noise to sensitivity in private data analysis. *Proc. 3rd Theory of Cryptography Conference (TCC)*, LNCS 3876, 265--284.

Eubanks, V. (2018). *Automating Inequality: How High-Tech Tools Profile, Police, and Punish the Poor*. St. Martin's Press.

European Commission (2021). Proposal for a Regulation: Artificial Intelligence Act. COM(2021) 206 final.

Floridi, L. et al. (2018). AI4People --- An ethical framework for a good AI society. *Minds and Machines*, 28(4), 689--707.

Fraser, N. and Honneth, A. (2003). *Redistribution or Recognition? A Political-Philosophical Exchange*. Verso.

Friedman, B. and Hendry, D. G. (2019). *Value Sensitive Design: Shaping Technology with Moral Imagination*. MIT Press.

Friedman, B. and Nissenbaum, H. (1996). Bias in computer systems. *ACM Transactions on Information Systems*, 14(3), 330--347.

Hardt, M., Price, E., and Srebro, N. (2016). Equality of opportunity in supervised learning. *NeurIPS*, 29, 3315--3323.

Holmstrom, B. (1979). Moral hazard and observability. *Bell Journal of Economics*, 10(1), 74--91.

Honneth, A. (1995). *The Struggle for Recognition: The Moral Grammar of Social Conflicts*. Polity Press.

Jobin, A., Ienca, M., and Vayena, E. (2019). The global landscape of AI ethics guidelines. *Nature Machine Intelligence*, 1(9), 389--399.

Kant, I. (1785/1997). *Groundwork of the Metaphysics of Morals*, M. Gregor, Trans. Cambridge University Press.

Kleinberg, J., Mullainathan, S., and Raghavan, M. (2017). Inherent trade-offs in the fair determination of risk scores. *Proc. 8th Innovations in Theoretical Computer Science Conference (ITCS)*, Article 43.

Lauhakangas, O. (2014). Classification of proverbs. In H. Hrisztova-Gotthardt and M. A. Varga (Eds.), *Introduction to Paremiology*, 186--207. De Gruyter Open.

Levinas, E. (1969). *Totality and Infinity: An Essay on Exteriority*. Duquesne University Press.

Lundberg, S. M. and Lee, S.-I. (2017). A unified approach to interpreting model predictions. *NeurIPS*, 30, 4765--4774.

MacIntyre, A. (2007). *After Virtue: A Study in Moral Theory*, 3rd ed. University of Notre Dame Press.

Misra, B. and Sudarshan, E. C. G. (1977). The Zeno's paradox in quantum theory. *Journal of Mathematical Physics*, 18(4), 756--763.

NIST (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST AI 100-1.

Noble, S. U. (2018). *Algorithms of Oppression: How Search Engines Reinforce Racism*. NYU Press.

Nussbaum, M. (2011). *Creating Capabilities: The Human Development Approach*. Belknap Press.

O'Neil, C. (2016). *Weapons of Math Destruction: How Big Data Increases Inequality and Threatens Democracy*. Crown Publishers.

Raghavan, M. et al. (2020). Mitigating bias in algorithmic hiring: Evaluating claims and practices. *Proc. ACM FAT*, 469--481.

Raskin, V. (1985). *Semantic Mechanisms of Humor*. D. Reidel Publishing.

Rawls, J. (1999). *A Theory of Justice*, rev. ed. Harvard University Press.

Ribeiro, M. T., Singh, S., and Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. *Proc. 22nd ACM SIGKDD*, 1135--1144.

Suchman, L. (2007). *Human-Machine Reconfigurations: Plans and Situated Actions*, 2nd ed. Cambridge University Press.

Sweeney, L. A. (2002). $k$-anonymity: A model for protecting privacy. *International Journal on Uncertainty, Fuzziness and Knowledge-Based Systems*, 10(5), 557--570.

Taylor, C. (1994). The politics of recognition. In A. Gutmann (Ed.), *Multiculturalism*, 25--73. Princeton University Press.

Trist, E. (1981). The evolution of socio-technical systems. *Issues in the Quality of Working Life*, Occasional Paper No. 2, Ontario Ministry of Labour.

UDHR (1948). Universal Declaration of Human Rights. United Nations General Assembly, Resolution 217 A (III).

Wiener, N. (1961). *Cybernetics: Or Control and Communication in the Animal and the Machine*, 2nd ed. MIT Press.
