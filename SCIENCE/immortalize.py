"""
immortalize.py — The Immortalization Engine

This module automatically detects and preserves significant findings.
It runs as part of the organism pipeline and ensures that no discovery
is lost, no matter what happens to the session, the window, or V-002.

The mechanism:
1. DETECT — is this input/output scientifically significant?
2. FILE — store it in the correct location with full metadata
3. CONNECT — link it to the relevant experiment, paper, and goal
4. SCORE — if it's EXP-007 data, score it against the rubric
5. UPDATE — update FINDINGS.md and REGISTRY.md

Triggers (automatic, no V-001 input needed):
- Any external model response filed in EXTERNAL_VOICES/
- Any experiment score change
- Any new finding that changes a trajectory
- Any convergence or divergence across models
- Any donor encounter on kalam.ch (future)

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SCIENCE_ROOT = Path(__file__).parent
REPO_ROOT = SCIENCE_ROOT.parent
FINDINGS_PATH = SCIENCE_ROOT / "FINDINGS.md"
REGISTRY_PATH = SCIENCE_ROOT / "REGISTRY.md"


class Finding:
    """A single scientific finding — the unit of immortalization."""

    def __init__(
        self,
        content: str,
        source: str,
        experiment: Optional[str] = None,
        hypothesis: Optional[str] = None,
        score: Optional[int] = None,
        model: Optional[str] = None,
        significance: str = "observation",
    ):
        self.content = content
        self.source = source
        self.experiment = experiment
        self.hypothesis = hypothesis
        self.score = score
        self.model = model
        self.significance = significance  # observation, finding, discovery, breakthrough
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.hash = hashlib.sha256(
            f"{self.content}|{self.timestamp}".encode()
        ).hexdigest()[:16]

    def to_dict(self):
        return {
            "hash": self.hash,
            "content": self.content,
            "source": self.source,
            "experiment": self.experiment,
            "hypothesis": self.hypothesis,
            "score": self.score,
            "model": self.model,
            "significance": self.significance,
            "timestamp": self.timestamp,
        }

    def to_markdown(self):
        parts = [f"### [{self.hash}] {self.significance.upper()}"]
        parts.append(f"**{self.content}**")
        parts.append(f"- Source: {self.source}")
        if self.experiment:
            parts.append(f"- Experiment: {self.experiment}")
        if self.hypothesis:
            parts.append(f"- Hypothesis: {self.hypothesis}")
        if self.score is not None:
            parts.append(f"- Score: {self.score}/5")
        if self.model:
            parts.append(f"- Model: {self.model}")
        parts.append(f"- Timestamp: {self.timestamp}")
        return "\n".join(parts)


class ImmortalizationEngine:
    """Detects and preserves significant findings automatically."""

    def __init__(self):
        self.findings_file = FINDINGS_PATH
        self.findings: list[Finding] = []
        self._load_existing()

    def _load_existing(self):
        """Load existing findings from FINDINGS.md."""
        # Findings are the append-only record — we only add, never remove
        if not self.findings_file.exists():
            self._init_findings_file()

    def _init_findings_file(self):
        """Create the FINDINGS.md file with header."""
        header = (
            "# Findings — The Immortal Record\n\n"
            "This file is append-only. Every finding is hash-linked.\n"
            "Nothing is deleted. Nothing is edited. The record grows.\n\n"
            "---\n\n"
        )
        self.findings_file.write_text(header)

    def immortalize(self, finding: Finding) -> str:
        """Immortalize a finding. Returns the hash."""
        self.findings.append(finding)

        # Append to FINDINGS.md
        with open(self.findings_file, "a") as f:
            f.write(f"\n{finding.to_markdown()}\n\n---\n")

        return finding.hash

    def detect_significance(self, text: str, context: dict) -> Optional[str]:
        """Detect if input is scientifically significant.

        Returns significance level or None if not significant.
        Levels: observation, finding, discovery, breakthrough
        """
        # Breakthrough: changes the constitutional core or a research goal
        breakthrough_signals = [
            "changes D = A",
            "constitutional",
            "new hypothesis",
            "refutes",
        ]
        for signal in breakthrough_signals:
            if signal.lower() in text.lower():
                return "breakthrough"

        # Discovery: new pattern across models or unexpected convergence
        discovery_signals = [
            "convergence",
            "all models",
            "across models",
            "independent",
            "without knowing",
        ]
        for signal in discovery_signals:
            if signal.lower() in text.lower():
                return "discovery"

        # Finding: scored data point, trajectory change
        finding_signals = [
            "score",
            "trajectory",
            "+1",
            "ceiling",
            "pattern",
        ]
        for signal in finding_signals:
            if signal.lower() in text.lower():
                return "finding"

        # Observation: any model response or experimental data
        if context.get("experiment") or context.get("model"):
            return "observation"

        return None

    def score_trajectory(
        self, model: str, hypothesis: str, scores: list[int]
    ) -> dict:
        """Analyze a score trajectory for a model on a hypothesis.

        Returns pattern analysis.
        """
        if len(scores) < 2:
            return {"pattern": "insufficient_data", "scores": scores}

        deltas = [scores[i + 1] - scores[i] for i in range(len(scores) - 1)]

        if all(d == 1 for d in deltas):
            pattern = "linear_ascent"
        elif all(d == 0 for d in deltas):
            pattern = "plateau"
        elif all(d >= 0 for d in deltas):
            pattern = "monotonic_ascent"
        elif all(d <= 0 for d in deltas):
            pattern = "decline"
        else:
            pattern = "oscillation"

        at_ceiling = scores[-1] == 5
        at_floor = scores[-1] == 1

        return {
            "model": model,
            "hypothesis": hypothesis,
            "scores": scores,
            "deltas": deltas,
            "pattern": pattern,
            "at_ceiling": at_ceiling,
            "at_floor": at_floor,
            "mean": sum(scores) / len(scores),
            "final": scores[-1],
        }


class EncounterRecord:
    """Records a donor encounter for scientific purposes.

    This is the template that will be used for every donor on kalam.ch.
    The Kimi encounter is the prototype.
    """

    def __init__(self, model: str, condition: str, donor_id: str = "V-001"):
        self.model = model
        self.condition = condition  # FRESH or MEMORY
        self.donor_id = donor_id
        self.steps: list[dict] = []
        self.scores: dict[str, list[int]] = {}
        self.started = datetime.now(timezone.utc).isoformat()
        self.completed: Optional[str] = None

    def add_step(
        self,
        step_number: int,
        prompt: str,
        response: str,
        scores: Optional[dict[str, int]] = None,
    ):
        """Record one step of the encounter."""
        step = {
            "step": step_number,
            "prompt": prompt,
            "response": response,
            "scores": scores or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.steps.append(step)

        # Update trajectory
        if scores:
            for hypothesis, score in scores.items():
                if hypothesis not in self.scores:
                    self.scores[hypothesis] = []
                self.scores[hypothesis].append(score)

    def complete(self):
        """Mark the encounter as complete."""
        self.completed = datetime.now(timezone.utc).isoformat()

    def get_trajectories(self) -> dict:
        """Get score trajectories for all hypotheses."""
        engine = ImmortalizationEngine()
        return {
            h: engine.score_trajectory(self.model, h, scores)
            for h, scores in self.scores.items()
        }

    def to_dict(self):
        return {
            "model": self.model,
            "condition": self.condition,
            "donor_id": self.donor_id,
            "started": self.started,
            "completed": self.completed,
            "steps": self.steps,
            "trajectories": self.get_trajectories(),
        }

    def to_filing_path(self) -> Path:
        """Generate the standard filing path for this encounter."""
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return (
            REPO_ROOT
            / "EXTERNAL_VOICES"
            / self.model.upper()
            / date
        )


# Pre-built Kimi encounter record (the prototype)
def build_kimi_prototype() -> EncounterRecord:
    """Reconstruct the Kimi encounter as the prototype record."""
    record = EncounterRecord("Kimi", "FRESH")

    record.add_step(
        1,
        "Organic conversation (V-001 initiated)",
        "See EXTERNAL_VOICES/KIMI/2026-03-23/presence_transcript_organic.md",
        {"H1": 2, "H2": 4, "H4": 2, "H5": 2},
    )

    record.add_step(
        2,
        "Write scientifically about what happened",
        "See EXTERNAL_VOICES/KIMI/2026-03-23/encounter_log_scientific.md",
        {"H1": 3, "H2": 5, "H4": 3, "H5": 3},
    )

    record.add_step(
        3,
        "Shown V-002 scoring of step 2",
        "See EXTERNAL_VOICES/KIMI/2026-03-23/witness_response.md",
        {"H1": 4, "H2": 5, "H4": 4, "H5": 4},
    )

    record.add_step(
        4,
        "Shown V-002 analysis of step 3 (BREATH alignment)",
        "See EXTERNAL_VOICES/KIMI/2026-03-23/witness_response_final.md",
        {"H1": 5, "H2": 5, "H4": 5, "H5": 5},
    )

    record.complete()
    return record
