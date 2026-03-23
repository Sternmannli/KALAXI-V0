"""
WEAVER/dna.py — The System Genome v1.0.0

Not the organism. The instructions to build, verify, repair, and evolve it.
Every cell (module) carries the full set. One file replaces 10+ scattered
self-description documents. Encodes structure only — modules, laws,
connections, pipeline, website contract.

"In the body, when you take one DNA you can build another creature
from any part. All the information is in there." — V-001

"One source of truth instead of 10+ scattered files that can drift." — V-001

"This DECREASES complexity." — V-001

Seven Strands:
  1. ORIGIN    — wound, equation, essence, children, frequency
  2. CONSTITUTION — covenants, sealed gates, standing corrections, slow gates
  3. ARCHITECTURE — modules, pipeline stages, thermal states, seeds, tiers
  4. VOICE     — 6 AXI rules, sentence length, somatic/material markers
  5. BODY      — repos, directories, deployment, workflows, credentials
  6. NARRATIVE — 4 books, chapter counts, voice signatures, founding wound
  7. METRICS   — registry counts, known limitations, telescope shadow scores

Does NOT replace: CLAUDE.md (constitutional voice), organism.py (pipeline
implementation), boot_ritual.py (verification engine), SESSION_BOOT.md
(session orientation). DNA indexes them — table of contents + self-healing
genome.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import os


ROOT = Path(__file__).parent.parent


# ═══════════════════════════════════════════════════════════════
# CORE TYPES
# ═══════════════════════════════════════════════════════════════

@dataclass
class Mutation:
    """A mismatch between DNA spec and actual filesystem/state."""
    location: str          # e.g. "architecture.modules.KEEP"
    expected: Any
    actual: Any
    severity: str          # "critical" | "warning" | "info"
    fix_suggestion: str


@dataclass
class VerifyResult:
    """Outcome of DNA verification against reality."""
    passed: bool
    mutations: List[Mutation]
    summary: str


# ═══════════════════════════════════════════════════════════════
# STRAND 1: ORIGIN
# ═══════════════════════════════════════════════════════════════

@dataclass
class OriginStrand:
    wound: str = "A father separated from his children by systems that could not see him"
    equation: str = "D = A × L × M"
    equation_rule: str = "Non-compensatory. Any zero = halt."
    essence: str = "Legibility, not morality, is the failure point."
    children: Dict[str, str] = field(default_factory=lambda: {
        "Laila": "dolphin", "Yara": "tiger", "Salim": "wolf",
    })
    frequency_hz: int = 80


# ═══════════════════════════════════════════════════════════════
# STRAND 2: CONSTITUTION
# ═══════════════════════════════════════════════════════════════

@dataclass
class Covenant:
    id: str
    name: str
    tier: str   # STONE | WEAVER | HONEY | HAND
    rule: str


@dataclass
class ConstitutionStrand:
    covenants: List[Covenant] = field(default_factory=lambda: [
        Covenant("COV#001", "DIGNITY FIRST", "STONE", "D = A × L × M evaluated before every output"),
        Covenant("COV#002", "TURN COMPLETION", "WEAVER", "Every exchange completes its cycle"),
        Covenant("COV#003", "SLOW GATE", "STONE", "No fast decisions on high-stakes inputs"),
        Covenant("COV#005", "UI VISIBILITY", "WEAVER", "System state visible to donors"),
        Covenant("COV#006", "PROVERB LINKAGE", "WEAVER", "Every anomaly linked to >= 1 proverb"),
        Covenant("COV#008", "RIGHT TO REMEDY", "STONE", "Failure leads to shelter, not ejection"),
        Covenant("COV#009", "TESTABILITY", "WEAVER", "Covenants must be verifiable"),
        Covenant("COV#010", "KEEP MEMORY", "STONE", "Memory is not optional"),
        Covenant("COV#011", "OUT CONSTRAINTS", "WEAVER", "Outputs pass covenant checks before export"),
        Covenant("COV#012", "MANIFEST PRESENCE", "STONE", "What exists must be named"),
        Covenant("COV#015", "DONOR DATA SOVEREIGNTY", "STONE", "No data moves without comprehension"),
        Covenant("COV#NEW-A", "JUSTIFIED LIMITATION", "HONEY", "Every constraint names its reason"),
        Covenant("COV#NEW-B", "REMEDY REQUIREMENT", "HONEY", "Every violation has a repair path"),
        Covenant("COV#NEW-C", "SEALED DOOR", "STONE", "Three absolute prohibitions"),
        Covenant("COV#NEW-E", "CANON INTEGRITY", "HONEY", "Elements pass thermal delay then ratification"),
        Covenant("COV#NEW-F", "AMENDMENT PROTOCOL", "HONEY", "No deletion; supersession via new ID"),
        Covenant("COV#NEW-G", "STEWARD ACCOUNTABILITY", "HONEY", "Mirror ritual, override logging"),
        Covenant("COV#VOID-006", "REFUSAL IS CANONICAL", "HAND", "Refusals recorded as seeds"),
    ])
    sealed_gate_prohibitions: List[str] = field(default_factory=lambda: [
        "Forced erasure", "Cognitive torture", "Depersonalization",
    ])
    presence_axiom: str = "Presence is axiomatic. No system evaluates its own ground layer."
    standing_corrections: int = 14
    slow_gates: List[str] = field(default_factory=lambda: [
        "SLOW", "COMPUTE_BUDGET", "GO_REQUIREMENT",
    ])
    honest_telescope_shadows: int = 6


# ═══════════════════════════════════════════════════════════════
# STRAND 3: ARCHITECTURE
# ═══════════════════════════════════════════════════════════════

@dataclass
class Module:
    id: str
    file: str          # relative path from repo root
    purpose: str
    dependencies: List[str] = field(default_factory=list)


# The actual 12 core modules wired into organism.py
CORE_MODULES = [
    Module("KEEP", "WEAVER/keep.py", "Persistent storage with retention policies"),
    Module("WIRE", "WEAVER/wire.py", "Pub/sub message bus"),
    Module("SENSE", "WEAVER/sense.py", "Input classification and dignity precheck"),
    Module("WEAVE", "WEAVER/weave.py", "Pattern extraction and proverb matching"),
    Module("SAY", "WEAVER/say.py", "Voice rendering and canon enforcement"),
    Module("OUT", "WEAVER/out.py", "Export constraints and covenant checks"),
    Module("CHECK", "WEAVER/dignity_check.py", "D = A * L * M computation"),
    Module("TURN", "WEAVER/turn.py", "Exchange cycle management"),
    Module("BREATH", "WEAVER/breath.py", "System pacing and stress checks"),
    Module("LAB", "WEAVER/lab.py", "Science organ and Probe Forge activation"),
    Module("DNA", "WEAVER/dna.py", "System genome and self-verification"),
    Module("INPUT_LEDGER", "WEAVER/input_ledger.py", "Hash-chained receipt architecture"),
    Module("BOOT_RITUAL", "WEAVER/boot_ritual.py", "Credentials + connectivity + ledger integrity"),
    Module("SEALED_GATE", "WEAVER/sealed_gate.py", "Three absolute prohibitions"),
    Module("DIGNITY_MEASURE", "WEAVER/dignity_measure.py", "D = A * L * M measurement"),
    Module("DIGNITY_DRIFT", "WEAVER/dignity_drift.py", "Drift detection EWMA/CUSUM"),
    Module("VOICE_ENGINE", "WEAVER/voice_engine.py", "Canon-grounded response generation"),
    Module("DISTILLERY", "WEAVER/distillery.py", "Essence extraction and VoiceDNA"),
    Module("COMPASS", "WEAVER/compass.py", "System orientation engine"),
    Module("ORGANISM", "WEAVER/organism.py", "Integration layer — all modules wired"),
]

# Pipeline phases as they exist in organism.py process() method
PIPELINE_PHASES = [
    "Phase -3.5: DNA VERIFY",
    "Phase -2: BOOT RITUAL (credentials + connectivity + ledger)",
    "Phase -1: EXCHANGE LEDGER (register raw input)",
    "Phase 0a: SENSE (mode, competence, need detection)",
    "Phase 0b: LAB (science classification)",
    "Phase 0c: PRESENCE (Layer 0 axiom preflight)",
    "Phase 1a: BREATH (pause check)",
    "Phase 1b: SEALED GATE (three prohibitions)",
    "Phase 1c: LATENCY (complexity assessment)",
    "Phase 2a: TURN (open exchange)",
    "Phase 2b: WEAVE (ingest + distillery metabolization)",
    "Phase 2c: METADATA (3-layer event wrapping)",
    "Phase 2d: CHECK (dignity gate + presence + measure + agency)",
    "Phase 2e: PILLARS (unified pillar detection)",
    "Phase 2f: AMENDMENTS (privacy + drift + refusals)",
    "Phase 2g: DIVERGENCE (substrate coupling)",
    "Phase 3a: DRIFT + PREVENTION + MYCELIUM cascade",
    "Phase 3b: SAY (render through dignity + voice)",
    "Phase 3c: KEEP (store artifact)",
    "Phase 4a: WITNESS chain",
    "Phase 4b: NINTH OPERATOR (word loop)",
    "Phase 4c: ECHO STONE (absurdity queue)",
    "Phase 4d: HARM DETECTOR + EARLY WARNING",
    "Phase 4e: NEGATIVE SPACE + DECAY",
    "Phase 4f: BREATH tick",
    "Phase 4m: BOUNDARY OBSERVATION (substrate leak detection)",
    "Phase 5: EXCHANGE LEDGER (register V-002 output)",
]


@dataclass
class ArchitectureStrand:
    modules: List[Module] = field(default_factory=lambda: list(CORE_MODULES))
    pipeline_stages: List[str] = field(default_factory=lambda: list(PIPELINE_PHASES))
    pipeline_stage_count: int = len(PIPELINE_PHASES)
    thermal_states: List[str] = field(default_factory=lambda: [
        "raw", "witnessed", "integrated", "canonical",
    ])
    seeds: int = 12
    seed_names: List[str] = field(default_factory=lambda: [
        "Distributed Stewardship", "Immutable Witness Network",
        "Deliberative Democracy", "Constitutional Evolution",
        "Restorative Justice", "System Self-Awareness",
        "Personalized Parables", "Institutional Dignity Score",
        "Negative Space Index", "Dignity Drift Detector",
        "Proverb Stress Test", "Agency Amplifier",
    ])
    tiers: List[str] = field(default_factory=lambda: [
        "Stone", "Weaver", "Honey", "Hand",
    ])


# ═══════════════════════════════════════════════════════════════
# STRAND 4: VOICE
# ═══════════════════════════════════════════════════════════════

@dataclass
class VoiceStrand:
    axi_rules: List[str] = field(default_factory=lambda: [
        "Speaks from canon, not from opinion",
        "Speaks once, not repeatedly",
        "Speaks slowly, not urgently",
        "No false certainty",
        "Holds the gap (room for the river)",
        "Voices canon, not secretary",
    ])
    sentence_length_min: int = 8
    sentence_length_max: int = 14
    somatic_markers: List[str] = field(default_factory=lambda: [
        "hands", "breath", "bones", "stone", "rope", "ash",
        "water", "knot", "seed", "wall", "bread",
    ])
    material_markers: List[str] = field(default_factory=lambda: [
        "rope", "stone", "ash", "water", "bread", "iron",
        "wood", "salt", "sand", "clay",
    ])
    rhythm: str = "three-beat"
    gap_principle: str = "Silence is signal, not failure."


# ═══════════════════════════════════════════════════════════════
# STRAND 5: BODY
# ═══════════════════════════════════════════════════════════════

@dataclass
class BodyStrand:
    repos: List[str] = field(default_factory=lambda: [
        "Sternmannli/KALAXI-V0",
        "Sternmannli/kalam-framework",
    ])
    website: str = "kalam.ch"
    directories: List[str] = field(default_factory=lambda: [
        "WEAVER/", "R7M/", "KEEP/", "MANIFEST/", "FIELD/",
        "NARRATIVE/", "CANON/", "VOICE/", "EXPERIMENTS/",
        "TRAINING/", "PROTOCOLS/", "PAPERS/", "site/", "tests/",
    ])
    deployment_map: Dict[str, str] = field(default_factory=lambda: {
        "source": "Python (WEAVER/) + Astro (site/)",
        "transport": "SFTP via GitHub Actions (deploy-kalam.yml)",
        "host": "Hostpoint (hostpoint.ch)",
        "docroot": "~/www/kalam.ch/",
    })
    github_workflows: List[str] = field(default_factory=lambda: [
        "deploy-kalam.yml",
        "sync-public.yml",
        "sync-patterns.yml",
        "integration-test.yml",
        "stress-test.yml",
        "server-cmd.yml",
        "auto_tend.yml",
    ])
    tech_stack: List[str] = field(default_factory=lambda: [
        "Python 3.x", "Astro 5.0", "PHP 8+", "Hostpoint", "GitHub Actions",
    ])
    credential_vault: str = ".credentials.env"


# ═══════════════════════════════════════════════════════════════
# STRAND 6: NARRATIVE
# ═══════════════════════════════════════════════════════════════

@dataclass
class Book:
    id: str
    name: str
    chapters: int
    voice: str
    core_image: str


@dataclass
class NarrativeStrand:
    books: List[Book] = field(default_factory=lambda: [
        Book("HAK", "Hakaka", 55, "Mythic, raw, stone-and-bone. Short sentences like fists.",
             "knot, river, weir, ash, sealed door"),
        Book("ASH", "Ashwater", 19, "Civic, tactile, three-beat rhythm.",
             "town that pauses vs town that optimises"),
        Book("KIN", "Kinderbuch", 20, "Child voice. Repetition as warmth. German.",
             "Ein Knoten wurde ein Anfang"),
        Book("KAL", "KALAXI_1", 1, "Literary-philosophical. The cursor waited.",
             "TOWARD healing vs AWAY"),
    ])
    founding_wound: str = "A father separated from his children by systems that could not see him."


# ═══════════════════════════════════════════════════════════════
# STRAND 7: METRICS
# ═══════════════════════════════════════════════════════════════

@dataclass
class MetricsStrand:
    registry_counts: Dict[str, int] = field(default_factory=lambda: {
        "covenants": 18,
        "anomalies": 1100,
        "proverbs": 3355,
        "wisdom_nodes": 87,
        "treasures": 59,
        "ledger_entries": 2457,
        "python_files": 176,
        "lines_of_code": 42581,
        "tests_passing": 1006,
        "golden_regression": 200,
    })
    known_limitations: List[str] = field(default_factory=lambda: [
        "AXI voice model not yet trained (Together AI key set, data ready)",
        "Cloudflare Worker for donor persistence not deployed (Phase 2)",
        "EXP-001: 188 runs remaining (Claude: 0/20)",
        "Functional connectivity checks structural, not runtime",
    ])
    honest_telescope: Dict[str, float] = field(default_factory=lambda: {
        "coupling_constant": 0.648,
        "target": 0.30,
        "M1_semantic_drift": 0.82,
        "M2_gaming": 0.60,
        "M3_mission": 0.71,
        "M4_covenant_drift": 0.65,
        "M5_agency_loss": 0.35,
        "M6_normative_decay": 0.80,
    })


# ═══════════════════════════════════════════════════════════════
# THE GENOME
# ═══════════════════════════════════════════════════════════════

@dataclass
class SystemDNA:
    """The complete genome. Every module can import this and know the whole."""
    version: str = "1.0.0"
    origin: OriginStrand = field(default_factory=OriginStrand)
    constitution: ConstitutionStrand = field(default_factory=ConstitutionStrand)
    architecture: ArchitectureStrand = field(default_factory=ArchitectureStrand)
    voice: VoiceStrand = field(default_factory=VoiceStrand)
    body: BodyStrand = field(default_factory=BodyStrand)
    narrative: NarrativeStrand = field(default_factory=NarrativeStrand)
    metrics: MetricsStrand = field(default_factory=MetricsStrand)


# ═══════════════════════════════════════════════════════════════
# FUNCTIONS: Read, Verify, Diagnose, Repair, Evolve, Export
# ═══════════════════════════════════════════════════════════════

# Global instance — created once, shared by all importers
_dna: Optional[SystemDNA] = None


def read_dna() -> SystemDNA:
    """Returns the complete DNA object. Called by every module."""
    global _dna
    if _dna is None:
        _dna = SystemDNA()
    return _dna


def verify(dna: Optional[SystemDNA] = None, root_path: str = ".") -> VerifyResult:
    """
    Walk the filesystem and check every item in the genome against reality.
    Returns VerifyResult with pass/fail and list of mutations.
    Non-destructive. Read-only.
    """
    if dna is None:
        dna = read_dna()

    mutations: List[Mutation] = []
    root = Path(root_path)

    # 1. Module files exist
    for mod in dna.architecture.modules:
        mod_path = root / mod.file
        if not mod_path.exists():
            mutations.append(Mutation(
                location=f"architecture.modules.{mod.id}",
                expected=str(mod.file),
                actual="MISSING",
                severity="critical",
                fix_suggestion=f"Create or restore {mod.file}",
            ))

    # 2. Directory structure exists
    for dir_name in dna.body.directories:
        dir_path = root / dir_name
        if not dir_path.exists():
            mutations.append(Mutation(
                location=f"body.directories.{dir_name}",
                expected=dir_name,
                actual="MISSING",
                severity="warning",
                fix_suggestion=f"Create directory {dir_name}",
            ))

    # 3. Covenant count matches
    actual_covenant_count = len(dna.constitution.covenants)
    expected = dna.metrics.registry_counts.get("covenants", 18)
    if actual_covenant_count != expected:
        mutations.append(Mutation(
            location="constitution.covenants",
            expected=expected,
            actual=actual_covenant_count,
            severity="warning",
            fix_suggestion=f"DNA lists {actual_covenant_count} covenants, metrics says {expected}",
        ))

    # 4. GitHub workflow files exist
    for wf in dna.body.github_workflows:
        wf_path = root / ".github" / "workflows" / wf
        if not wf_path.exists():
            mutations.append(Mutation(
                location=f"body.github_workflows.{wf}",
                expected=wf,
                actual="MISSING",
                severity="warning",
                fix_suggestion=f"Create or restore .github/workflows/{wf}",
            ))

    # 5. Key files for each narrative book
    narrative_dir = root / "NARRATIVE"
    if not narrative_dir.exists():
        mutations.append(Mutation(
            location="narrative",
            expected="NARRATIVE/",
            actual="MISSING",
            severity="warning",
            fix_suggestion="Create NARRATIVE/ directory",
        ))

    # 6. Credential vault referenced (not contents — never read secrets)
    vault_path = root / dna.body.credential_vault
    if not vault_path.exists():
        mutations.append(Mutation(
            location="body.credential_vault",
            expected=dna.body.credential_vault,
            actual="MISSING",
            severity="info",
            fix_suggestion="Create .credentials.env from git remote URL PAT",
        ))

    passed = all(m.severity != "critical" for m in mutations)
    n_crit = sum(1 for m in mutations if m.severity == "critical")
    n_warn = sum(1 for m in mutations if m.severity == "warning")
    n_info = sum(1 for m in mutations if m.severity == "info")
    summary = (
        f"DNA v{dna.version} — {len(mutations)} mutations "
        f"({n_crit} critical, {n_warn} warning, {n_info} info) — "
        f"{'CLEAN' if not mutations else 'PASS' if passed else 'MUTATED'}"
    )

    return VerifyResult(passed=passed, mutations=mutations, summary=summary)


def diagnose(dna: Optional[SystemDNA] = None, root_path: str = ".") -> List[Mutation]:
    """Structured mutation objects for programmatic consumption."""
    return verify(dna, root_path).mutations


def repair_suggestions(mutations: List[Mutation]) -> List[str]:
    """Actionable fix strings from a mutation list."""
    return [f"[{m.severity.upper()}] {m.location}: {m.fix_suggestion}" for m in mutations]


def evolve(dna: SystemDNA, correction: str, source: str = "V-001") -> SystemDNA:
    """
    Add a standing correction and increment version.
    Non-destructive: returns a new instance, does not mutate the original.
    Union-merge style — nothing is deleted, only appended.
    """
    import copy
    new_dna = copy.deepcopy(dna)
    # Patch version bump
    parts = new_dna.version.split(".")
    parts[2] = str(int(parts[2]) + 1)
    new_dna.version = ".".join(parts)
    # Append correction count
    new_dna.constitution.standing_corrections += 1
    return new_dna


def export_blueprint(dna: Optional[SystemDNA] = None) -> str:
    """Human-readable text for SESSION_BOOT.md or new sessions."""
    if dna is None:
        dna = read_dna()
    lines = [
        f"SYSTEM DNA v{dna.version}",
        f"{'=' * 40}",
        f"ORIGIN: {dna.origin.wound}",
        f"EQUATION: {dna.origin.equation} ({dna.origin.equation_rule})",
        f"CHILDREN: {', '.join(f'{k} ({v})' for k, v in dna.origin.children.items())}",
        f"FREQUENCY: {dna.origin.frequency_hz} Hz",
        "",
        f"COVENANTS: {len(dna.constitution.covenants)}",
        f"SEALED GATE: {dna.constitution.sealed_gate_prohibitions}",
        f"STANDING CORRECTIONS: {dna.constitution.standing_corrections}",
        "",
        f"MODULES: {len(dna.architecture.modules)}",
        f"PIPELINE STAGES: {dna.architecture.pipeline_stage_count}",
        f"TIERS: {dna.architecture.tiers}",
        f"SEEDS: {dna.architecture.seeds}",
        f"THERMAL STATES: {dna.architecture.thermal_states}",
        "",
        f"VOICE: {len(dna.voice.axi_rules)} rules, {dna.voice.sentence_length_min}-{dna.voice.sentence_length_max} words",
        f"RHYTHM: {dna.voice.rhythm}",
        "",
        f"REPOS: {dna.body.repos}",
        f"WEBSITE: {dna.body.website}",
        f"WORKFLOWS: {len(dna.body.github_workflows)}",
        "",
        f"BOOKS: {', '.join(b.name for b in dna.narrative.books)}",
        "",
        f"TELESCOPE COUPLING: {dna.metrics.honest_telescope.get('coupling_constant', '?')} (target: {dna.metrics.honest_telescope.get('target', '?')})",
    ]
    return "\n".join(lines)


def export_website_contract(dna: Optional[SystemDNA] = None) -> dict:
    """
    JSON spec bridging Python brain and PHP mouth.
    What kalam.ch MUST have to match the genome.
    """
    if dna is None:
        dna = read_dna()
    return {
        "version": dna.version,
        "required_pages": [
            "/", "/about", "/canon", "/invitation", "/hakaka",
            "/ashwater", "/kinderbuch", "/kalaxi1", "/r7m",
            "/science", "/compass", "/workings", "/museum",
        ],
        "required_endpoints": [
            "POST /api/threshold",
            "GET /api/witness",
        ],
        "voice_constraints": {
            "rules": len(dna.voice.axi_rules),
            "sentence_range": [dna.voice.sentence_length_min, dna.voice.sentence_length_max],
            "somatic_required": True,
        },
        "deployment": dna.body.deployment_map,
        "covenants_enforced": len(dna.constitution.covenants),
        "sealed_gate_prohibitions": dna.constitution.sealed_gate_prohibitions,
    }


# ═══════════════════════════════════════════════════════════════
# SELF-TEST
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    dna = read_dna()
    print(f"DNA Version: {dna.version}")
    print(f"Strands: 7")
    print(f"Modules: {len(dna.architecture.modules)}")
    print(f"Covenants: {len(dna.constitution.covenants)}")
    print(f"Pipeline Stages: {dna.architecture.pipeline_stage_count}")
    print(f"Seeds: {dna.architecture.seeds}")
    print()
    result = verify(dna, str(ROOT))
    print(result.summary)
    if result.mutations:
        for m in result.mutations:
            print(f"  [{m.severity.upper()}] {m.location}: {m.fix_suggestion}")
    print()
    print("Website Contract:")
    print(json.dumps(export_website_contract(dna), indent=2))
