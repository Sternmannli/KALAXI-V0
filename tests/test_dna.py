"""
tests/test_dna.py — Verification suite for the System Genome.

[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from WEAVER.dna import (
    read_dna, verify, diagnose, repair_suggestions, evolve,
    export_blueprint, export_website_contract,
    SystemDNA, Mutation, VerifyResult,
)


# ── Read ──

def test_dna_loads():
    dna = read_dna()
    assert isinstance(dna, SystemDNA)
    assert dna.version == "1.0.0"


def test_dna_seven_strands():
    dna = read_dna()
    assert dna.origin is not None
    assert dna.constitution is not None
    assert dna.architecture is not None
    assert dna.voice is not None
    assert dna.body is not None
    assert dna.narrative is not None
    assert dna.metrics is not None


# ── Origin ──

def test_origin_wound():
    dna = read_dna()
    assert "father" in dna.origin.wound.lower()
    assert "children" in dna.origin.wound.lower()


def test_origin_equation():
    dna = read_dna()
    assert "D" in dna.origin.equation
    assert "A" in dna.origin.equation
    assert "L" in dna.origin.equation
    assert "M" in dna.origin.equation


def test_origin_children():
    dna = read_dna()
    assert "Laila" in dna.origin.children
    assert "Yara" in dna.origin.children
    assert "Salim" in dna.origin.children


def test_origin_frequency():
    dna = read_dna()
    assert dna.origin.frequency_hz == 80


# ── Constitution ──

def test_covenants_count():
    dna = read_dna()
    assert len(dna.constitution.covenants) == 18


def test_sealed_gate_three():
    dna = read_dna()
    assert len(dna.constitution.sealed_gate_prohibitions) == 3


def test_slow_gates():
    dna = read_dna()
    assert len(dna.constitution.slow_gates) == 3


# ── Architecture ──

def test_modules_defined():
    dna = read_dna()
    assert len(dna.architecture.modules) >= 12


def test_pipeline_stages():
    dna = read_dna()
    assert dna.architecture.pipeline_stage_count > 0
    assert len(dna.architecture.pipeline_stages) == dna.architecture.pipeline_stage_count


def test_thermal_states():
    dna = read_dna()
    assert dna.architecture.thermal_states == ["raw", "witnessed", "integrated", "canonical"]


def test_four_tiers():
    dna = read_dna()
    assert dna.architecture.tiers == ["Stone", "Weaver", "Honey", "Hand"]


def test_twelve_seeds():
    dna = read_dna()
    assert dna.architecture.seeds == 12
    assert len(dna.architecture.seed_names) == 12


# ── Voice ──

def test_six_axi_rules():
    dna = read_dna()
    assert len(dna.voice.axi_rules) == 6


def test_sentence_length_range():
    dna = read_dna()
    assert dna.voice.sentence_length_min == 8
    assert dna.voice.sentence_length_max == 14


# ── Body ──

def test_repos():
    dna = read_dna()
    assert len(dna.body.repos) >= 2


def test_website():
    dna = read_dna()
    assert dna.body.website == "kalam.ch"


def test_workflows_count():
    dna = read_dna()
    assert len(dna.body.github_workflows) == 7


# ── Narrative ──

def test_four_books():
    dna = read_dna()
    assert len(dna.narrative.books) == 4
    names = [b.name for b in dna.narrative.books]
    assert "Hakaka" in names
    assert "Ashwater" in names
    assert "Kinderbuch" in names
    assert "KALAXI_1" in names


def test_founding_wound():
    dna = read_dna()
    assert dna.narrative.founding_wound == dna.origin.wound + "."


# ── Metrics ──

def test_registry_counts():
    dna = read_dna()
    assert dna.metrics.registry_counts["covenants"] == 18
    assert dna.metrics.registry_counts["proverbs"] >= 3000


def test_honest_telescope():
    dna = read_dna()
    assert "coupling_constant" in dna.metrics.honest_telescope
    assert "target" in dna.metrics.honest_telescope


# ── Verify ──

def test_verify_runs():
    result = verify(root_path=str(ROOT))
    assert isinstance(result, VerifyResult)
    assert isinstance(result.passed, bool)
    assert isinstance(result.mutations, list)


def test_verify_passes_on_clean():
    result = verify(root_path=str(ROOT))
    assert result.passed is True, f"Failed: {result.summary}"


def test_verify_summary_format():
    result = verify(root_path=str(ROOT))
    assert "DNA v1.0.0" in result.summary


# ── Diagnose ──

def test_diagnose_returns_list():
    mutations = diagnose(root_path=str(ROOT))
    assert isinstance(mutations, list)


# ── Repair Suggestions ──

def test_repair_suggestions():
    mutations = [
        Mutation("test.loc", "expected", "actual", "warning", "fix this"),
    ]
    suggestions = repair_suggestions(mutations)
    assert len(suggestions) == 1
    assert "fix this" in suggestions[0]


# ── Evolve ──

def test_evolve_increments_version():
    dna = read_dna()
    original_version = dna.version
    new_dna = evolve(dna, "Test correction")
    assert new_dna.version != original_version
    parts = new_dna.version.split(".")
    assert int(parts[2]) == int(original_version.split(".")[2]) + 1


def test_evolve_nondestructive():
    dna = read_dna()
    original_corrections = dna.constitution.standing_corrections
    new_dna = evolve(dna, "Test correction")
    assert new_dna.constitution.standing_corrections == original_corrections + 1
    # Original unchanged (deepcopy)
    assert dna.constitution.standing_corrections == original_corrections


# ── Export ──

def test_export_blueprint():
    bp = export_blueprint()
    assert "DNA v1.0.0" in bp
    assert "ORIGIN" in bp
    assert "EQUATION" in bp
    assert "MODULES" in bp


def test_export_website_contract():
    contract = export_website_contract()
    assert isinstance(contract, dict)
    assert "version" in contract
    assert "required_pages" in contract
    assert "required_endpoints" in contract
    assert "voice_constraints" in contract
    assert "deployment" in contract
    # Must be valid JSON
    json.dumps(contract)


def test_export_website_contract_pages():
    contract = export_website_contract()
    pages = contract["required_pages"]
    assert "/" in pages
    assert "/about" in pages
    assert "/canon" in pages
