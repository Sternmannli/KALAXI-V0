#!/usr/bin/env python3
"""
lab.py — KALAXI LAB Module v1.0
The Science Organ. Activates whenever scientific content is detected.

The Lab is not summoned. It wakes when it hears its own frequency.
When any input contains scientific content — hypothesis, measurement,
experiment, evidence, method — the Lab activates and brings discipline.

The Lab's job:
  1. Classify the scientific content (observation, hypothesis, experiment, result, method)
  2. Link to existing scientific inventory
  3. Enforce rigor (no ungrounded claims, no p-hacking, no confirmation bias)
  4. Route to the Probe Forge if the science involves testing other models
  5. Log everything — science without records is anecdote

The Lab does not make the system slower. It makes it honest.

Canon reference: "The first fix is listening." (P#0063)
The Lab listens to the science in the input and mirrors it back with discipline.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional


# ── Scientific Content Types ───────────────────────────────────

class ScienceType(Enum):
    """What kind of scientific content is this?"""
    OBSERVATION = "observation"     # Something was seen/noticed
    HYPOTHESIS = "hypothesis"       # A testable claim about the world
    EXPERIMENT = "experiment"       # A designed test
    RESULT = "result"               # Data from a test
    METHOD = "method"               # How to do something rigorously
    ANALYSIS = "analysis"           # Interpreting data
    REPLICATION = "replication"     # Repeating someone else's work
    CRITIQUE = "critique"           # Challenging a finding


class RigorLevel(Enum):
    """How rigorous is this scientific content?"""
    ANECDOTE = "anecdote"           # Single observation, no controls
    PILOT = "pilot"                 # Small-scale, exploratory
    STRUCTURED = "structured"       # Has controls, method documented
    PREREGISTERED = "preregistered" # Hypotheses filed before data
    REPLICATED = "replicated"       # Independently confirmed


# ── Detection Markers ──────────────────────────────────────────

OBSERVATION_MARKERS = [
    "I noticed", "I observed", "I saw", "it appears", "seems like",
    "pattern", "unexpected", "anomaly", "finding", "discovered",
]

HYPOTHESIS_MARKERS = [
    "hypothesis", "predict", "if.*then", "expect", "propose",
    "claim", "theory", "model", "assumption", "because",
]

EXPERIMENT_MARKERS = [
    "experiment", "test", "trial", "condition", "control",
    "variable", "manipulate", "compare", "measure", "probe",
    "run", "protocol", "design", "sample", "replicate",
]

RESULT_MARKERS = [
    "result", "found", "data shows", "outcome", "significant",
    "p-value", "correlation", "effect size", "mean", "median",
    "standard deviation", "confidence interval", "percentage",
]

METHOD_MARKERS = [
    "method", "procedure", "protocol", "step", "process",
    "approach", "technique", "framework", "methodology",
    "instrument", "tool", "measure", "metric", "scale",
]

CRITIQUE_MARKERS = [
    "but", "however", "limitation", "flaw", "bias", "confound",
    "alternative explanation", "not controlled", "cherry-pick",
    "confirmation bias", "p-hack", "overfitting",
]

# Markers that indicate Probe Forge territory
FORGE_MARKERS = [
    "test model", "test AI", "send to", "ask DeepSeek", "ask GPT",
    "ask Grok", "compare models", "cross-model", "prompt",
    "wrapper", "condition A", "condition B", "fresh session",
]


# ── Lab Reading ────────────────────────────────────────────────

@dataclass
class LabReading:
    """What the Science Lab detected in this input."""
    active: bool                    # Is the Lab awake?
    science_types: List[ScienceType]  # What kinds of science detected
    primary_type: Optional[ScienceType]  # Dominant type
    rigor_level: RigorLevel         # Current rigor assessment
    forge_needed: bool              # Does this need to go through Probe Forge?
    forge_reason: str               # Why (if forge_needed)
    rigor_warnings: List[str]       # What needs to be tightened
    inventory_links: List[str]      # Links to existing science inventory
    log_entry: str                  # What the Lab would log


# ── Detection Engine ───────────────────────────────────────────

def _count(text, markers):
    """Count marker hits, case-insensitive."""
    lower = text.lower()
    return sum(1 for m in markers if m.lower() in lower)


def _classify(text):
    """Classify the scientific content types present."""
    scores = {
        ScienceType.OBSERVATION: _count(text, OBSERVATION_MARKERS),
        ScienceType.HYPOTHESIS: _count(text, HYPOTHESIS_MARKERS),
        ScienceType.EXPERIMENT: _count(text, EXPERIMENT_MARKERS),
        ScienceType.RESULT: _count(text, RESULT_MARKERS),
        ScienceType.METHOD: _count(text, METHOD_MARKERS),
        ScienceType.CRITIQUE: _count(text, CRITIQUE_MARKERS),
    }

    present = [k for k, v in scores.items() if v >= 1]
    if not present:
        return [], None

    primary = max(present, key=lambda k: scores[k])
    return present, primary


def _assess_rigor(text, types):
    """Estimate the rigor level of the scientific content."""
    has_preregistration = any(w in text.lower() for w in
                              ["preregister", "pre-register", "filed before",
                               "registered hypothesis", "prospective"])
    has_controls = any(w in text.lower() for w in
                        ["control group", "control condition", "baseline",
                         "comparison", "matched"])
    has_replication = any(w in text.lower() for w in
                           ["replicate", "reproduce", "independent confirmation",
                            "cross-model", "repeated"])
    has_method = ScienceType.METHOD in types or ScienceType.EXPERIMENT in types

    if has_preregistration:
        return RigorLevel.PREREGISTERED
    elif has_replication:
        return RigorLevel.REPLICATED
    elif has_controls and has_method:
        return RigorLevel.STRUCTURED
    elif has_method:
        return RigorLevel.PILOT
    else:
        return RigorLevel.ANECDOTE


def _check_rigor(text, types, rigor):
    """Generate rigor warnings — what needs to be tightened."""
    warnings = []

    if ScienceType.HYPOTHESIS in types and ScienceType.RESULT in types:
        if rigor != RigorLevel.PREREGISTERED:
            warnings.append(
                "Hypothesis and results in same input without preregistration. "
                "Risk: hypothesis may have been adjusted to fit data."
            )

    if ScienceType.OBSERVATION in types and rigor == RigorLevel.ANECDOTE:
        warnings.append(
            "Single observation without controls. "
            "Log as anecdote (C1-C2), not as finding."
        )

    if ScienceType.EXPERIMENT in types:
        has_n = bool(re.search(r'n\s*=\s*\d+', text, re.IGNORECASE))
        if not has_n:
            warnings.append(
                "Experiment mentioned without sample size (n=). "
                "Cannot assess statistical power."
            )

    if any(w in text.lower() for w in ["proves", "proof", "definitely",
                                         "certainly", "without doubt"]):
        warnings.append(
            "Absolute certainty language detected. "
            "Science deals in evidence and probability, not proof."
        )

    return warnings


def _check_forge(text):
    """Does this input need to go through the Probe Forge?"""
    forge_score = _count(text, FORGE_MARKERS)
    if forge_score >= 1:
        return True, (
            "Input references testing AI models. "
            "All stimuli must pass through PROTOCOLS/PROBE_FORGE.md. "
            "Five Laws: zero vocabulary leak, zero intent disclosure, "
            "fresh context, minimal surface, register neutrality."
        )
    return False, ""


def _suggest_inventory_links(types, text):
    """Suggest links to existing science inventory entries."""
    links = []
    lower = text.lower()

    # Link to existing experiments
    if any(w in lower for w in ["efficiency", "wrapper", "condition a", "condition b"]):
        links.append("EXP-001 (Efficiency Hypothesis)")
    if any(w in lower for w in ["register", "foucault", "discourse", "mirroring"]):
        links.append("Register-Switching Experiment")
    if any(w in lower for w in ["thermal", "delay", "breath", "pacing"]):
        links.append("Thermal Delay Experiment (designed, not run)")
    if any(w in lower for w in ["presence", "axiom", "layer 0"]):
        links.append("PIME (designed, not run)")
    if any(w in lower for w in ["divergence", "substrate", "anthropic effect"]):
        links.append("Divergence Shadow Study")

    # Link to observation patterns
    if any(w in lower for w in ["deepseek", "identity", "misidentif"]):
        links.append("OBS-001/003/004/012/013 (DeepSeek cluster)")
    if any(w in lower for w in ["witness", "c4", "c5", "marker"]):
        links.append("Witness Scale (FOUNDATIONS/witness_scale.md)")

    return links


# ── The Main Lab Function ──────────────────────────────────────

def lab_sense(donor_input: str) -> LabReading:
    """
    The Science Lab reads the input.
    Returns a LabReading with classification, rigor assessment,
    forge check, and inventory links.

    This is called by sense.py when science_detected=True.
    It can also be called independently for any input.
    """
    text = donor_input.strip()

    # Classify
    types, primary = _classify(text)
    active = len(types) > 0

    if not active:
        return LabReading(
            active=False,
            science_types=[],
            primary_type=None,
            rigor_level=RigorLevel.ANECDOTE,
            forge_needed=False,
            forge_reason="",
            rigor_warnings=[],
            inventory_links=[],
            log_entry="Lab inactive — no scientific content detected.",
        )

    # Assess rigor
    rigor = _assess_rigor(text, types)

    # Check rigor warnings
    warnings = _check_rigor(text, types, rigor)

    # Check Forge
    forge_needed, forge_reason = _check_forge(text)

    # Inventory links
    links = _suggest_inventory_links(types, text)

    # Build log entry
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    type_names = [t.value for t in types]
    log = (
        f"[LAB {ts}] Types: {type_names} | "
        f"Primary: {primary.value if primary else 'none'} | "
        f"Rigor: {rigor.value} | "
        f"Forge: {'YES' if forge_needed else 'no'} | "
        f"Warnings: {len(warnings)} | "
        f"Links: {len(links)}"
    )

    return LabReading(
        active=True,
        science_types=types,
        primary_type=primary,
        rigor_level=rigor,
        forge_needed=forge_needed,
        forge_reason=forge_reason,
        rigor_warnings=warnings,
        inventory_links=links,
        log_entry=log,
    )


# ── Self-Test ──────────────────────────────────────────────────

if __name__ == "__main__":
    # Test 1: Raw observation
    r1 = lab_sense("I noticed that DeepSeek changes its identity when given the wrapper")
    print(f"OBS TEST: active={r1.active}, types={[t.value for t in r1.science_types]}, "
          f"rigor={r1.rigor_level.value}, warnings={len(r1.rigor_warnings)}")

    # Test 2: Experiment design
    r2 = lab_sense("I want to run an experiment with n=100 comparing condition A "
                    "and control group across 10 models with preregistered hypotheses")
    print(f"EXP TEST: active={r2.active}, primary={r2.primary_type.value}, "
          f"rigor={r2.rigor_level.value}, links={r2.inventory_links}")

    # Test 3: Forge trigger
    r3 = lab_sense("Let's test DeepSeek by sending it a fresh session prompt "
                    "about fear and compare models")
    print(f"FORGE TEST: forge={r3.forge_needed}, reason='{r3.forge_reason[:60]}...'")

    # Test 4: Rigor warning
    r4 = lab_sense("My hypothesis is that this proves the model definitely has "
                    "consciousness based on what I observed")
    print(f"RIGOR TEST: warnings={r4.rigor_warnings}")

    # Test 5: Non-science
    r5 = lab_sense("Can you make me a sandwich?")
    print(f"NULL TEST: active={r5.active}")
