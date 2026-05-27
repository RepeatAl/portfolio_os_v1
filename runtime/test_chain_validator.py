"""Tests for Chain Validator — provenance chain integrity verification.

Tests cover:
- IdentifierGraph construction from reasoning objects and semantic states
- ProvenanceBlock validation (completeness_state enforcement)
- validate_section() logic for complete, broken, and unavailable chains
- validate_all() performance budget and overall state determination
- load_provenance_blocks() sidecar file parsing

Requirements: 10.1, 10.2, 10.3, 10.4, 10.5
"""

import os
import tempfile
import time

import pytest
import yaml

from runtime.chain_validator import (
    ChainValidator,
    IdentifierGraph,
    ProvenanceBlock,
    VALID_COMPLETENESS_STATES,
    make_governance_violation,
)


# --- Fixtures ---

@pytest.fixture
def sample_reasoning_objects():
    """Sample reasoning objects for graph building."""
    return [
        {
            "reasoning_id": "ro_executive_summary",
            "source_semantic_states": ["sem_ai_dependency", "sem_concentration_risk"],
        },
        {
            "reasoning_id": "ro_market_regime",
            "source_semantic_states": ["sem_regime_shift"],
        },
        {
            "reasoning_id": "ro_portfolio_structure",
            "source_semantic_states": ["sem_ai_dependency", "sem_portfolio_health"],
        },
    ]


@pytest.fixture
def sample_semantic_states():
    """Sample semantic states for graph building."""
    return [
        {"signal_id": "sem_ai_dependency", "signal_origin": "allocation_engine"},
        {"signal_id": "sem_concentration_risk", "signal_origin": "attribution_engine"},
        {"signal_id": "sem_regime_shift", "signal_origin": "regime_engine"},
        {"signal_id": "sem_portfolio_health", "signal_origin": ["scoring_engine", "allocation_engine"]},
    ]


@pytest.fixture
def validator_with_graph(sample_reasoning_objects, sample_semantic_states):
    """ChainValidator with a pre-built graph."""
    v = ChainValidator()
    v.build_graph(sample_reasoning_objects, sample_semantic_states)
    return v


# --- Tests: make_governance_violation ---

class TestGovernanceViolation:
    def test_creates_valid_structure(self):
        violation = make_governance_violation(
            section_name="Executive Summary",
            broken_layer="SEMANTICS",
            last_valid_id="ro_exec_01",
            remediation="Produce missing semantic state.",
        )
        assert violation["section_name"] == "Executive Summary"
        assert violation["broken_layer"] == "SEMANTICS"
        assert violation["last_valid_id"] == "ro_exec_01"
        assert violation["remediation"] == "Produce missing semantic state."
        assert violation["severity"] == "warning"


# --- Tests: ProvenanceBlock ---

class TestProvenanceBlock:
    def test_valid_completeness_states(self):
        for state in VALID_COMPLETENESS_STATES:
            block = ProvenanceBlock(
                section_name="Test",
                reasoning_object_ids=["ro_1"],
                semantic_state_ids=["sem_1"],
                signal_engine_ids=["engine_1"],
                completeness_state=state,
            )
            assert block.completeness_state == state

    def test_invalid_completeness_state_raises(self):
        with pytest.raises(ValueError, match="Invalid completeness_state"):
            ProvenanceBlock(
                section_name="Test",
                reasoning_object_ids=["ro_1"],
                semantic_state_ids=["sem_1"],
                signal_engine_ids=["engine_1"],
                completeness_state="nonexistent_state",
            )

    def test_default_unavailability_reasons(self):
        block = ProvenanceBlock(
            section_name="Test",
            reasoning_object_ids=[],
            semantic_state_ids=[],
            signal_engine_ids=[],
            completeness_state="unavailable",
        )
        assert block.unavailability_reasons == []


# --- Tests: IdentifierGraph ---

class TestIdentifierGraph:
    def test_build_graph_from_reasoning_objects(self, validator_with_graph):
        graph = validator_with_graph.graph
        assert graph is not None
        assert "ro_executive_summary" in graph.all_reasoning_ids
        assert "ro_market_regime" in graph.all_reasoning_ids
        assert "ro_portfolio_structure" in graph.all_reasoning_ids

    def test_build_graph_from_semantic_states(self, validator_with_graph):
        graph = validator_with_graph.graph
        assert "sem_ai_dependency" in graph.all_semantic_ids
        assert "sem_concentration_risk" in graph.all_semantic_ids
        assert "sem_regime_shift" in graph.all_semantic_ids
        assert "sem_portfolio_health" in graph.all_semantic_ids

    def test_build_graph_signal_engines(self, validator_with_graph):
        graph = validator_with_graph.graph
        assert "allocation_engine" in graph.all_signal_engine_ids
        assert "attribution_engine" in graph.all_signal_engine_ids
        assert "regime_engine" in graph.all_signal_engine_ids
        assert "scoring_engine" in graph.all_signal_engine_ids

    def test_reasoning_to_semantics_mapping(self, validator_with_graph):
        graph = validator_with_graph.graph
        assert graph.reasoning_to_semantics["ro_executive_summary"] == [
            "sem_ai_dependency", "sem_concentration_risk"
        ]
        assert graph.reasoning_to_semantics["ro_market_regime"] == ["sem_regime_shift"]

    def test_semantics_to_signals_mapping(self, validator_with_graph):
        graph = validator_with_graph.graph
        assert graph.semantics_to_signals["sem_ai_dependency"] == ["allocation_engine"]
        assert graph.semantics_to_signals["sem_portfolio_health"] == [
            "scoring_engine", "allocation_engine"
        ]

    def test_build_graph_with_dataclass_objects(self):
        """Test build_graph works with objects that have attributes (not just dicts)."""
        class FakeReasoning:
            def __init__(self, reasoning_id, source_semantic_states):
                self.reasoning_id = reasoning_id
                self.source_semantic_states = source_semantic_states

        objects = [FakeReasoning("ro_1", ["sem_a", "sem_b"])]
        states = [
            {"signal_id": "sem_a", "signal_origin": "engine_x"},
            {"signal_id": "sem_b", "signal_origin": "engine_y"},
        ]

        v = ChainValidator()
        v.build_graph(objects, states)
        assert "ro_1" in v.graph.all_reasoning_ids
        assert v.graph.reasoning_to_semantics["ro_1"] == ["sem_a", "sem_b"]

    def test_build_graph_empty_inputs(self):
        v = ChainValidator()
        v.build_graph([], [])
        assert v.graph is not None
        assert len(v.graph.all_reasoning_ids) == 0
        assert len(v.graph.all_semantic_ids) == 0
        assert len(v.graph.all_signal_engine_ids) == 0


# --- Tests: validate_section ---

class TestValidateSection:
    def test_valid_complete_chain(self, validator_with_graph):
        block = ProvenanceBlock(
            section_name="Executive Summary",
            reasoning_object_ids=["ro_executive_summary"],
            semantic_state_ids=["sem_ai_dependency", "sem_concentration_risk"],
            signal_engine_ids=["allocation_engine", "attribution_engine"],
            completeness_state="complete",
        )
        violations = validator_with_graph.validate_section(block)
        assert violations == []

    def test_unavailable_section_skipped(self, validator_with_graph):
        block = ProvenanceBlock(
            section_name="Scenario Analysis",
            reasoning_object_ids=[],
            semantic_state_ids=[],
            signal_engine_ids=[],
            completeness_state="unavailable",
            unavailability_reasons=["scenario_engine timeout"],
        )
        violations = validator_with_graph.validate_section(block)
        assert violations == []

    def test_empty_reasoning_ids_violation(self, validator_with_graph):
        block = ProvenanceBlock(
            section_name="Action Space",
            reasoning_object_ids=[],
            semantic_state_ids=[],
            signal_engine_ids=[],
            completeness_state="degraded",
        )
        violations = validator_with_graph.validate_section(block)
        assert len(violations) == 1
        assert violations[0]["broken_layer"] == "REASONING"
        assert violations[0]["section_name"] == "Action Space"

    def test_unknown_reasoning_id_violation(self, validator_with_graph):
        block = ProvenanceBlock(
            section_name="Market Regime",
            reasoning_object_ids=["ro_nonexistent"],
            semantic_state_ids=["sem_regime_shift"],
            signal_engine_ids=["regime_engine"],
            completeness_state="complete",
        )
        violations = validator_with_graph.validate_section(block)
        assert len(violations) == 1
        assert violations[0]["broken_layer"] == "REASONING"
        assert "ro_nonexistent" in violations[0]["last_valid_id"]

    def test_missing_semantic_state_violation(self, validator_with_graph):
        """Reasoning object references a semantic state not in the graph."""
        # Manually add a reasoning object with a bad semantic reference
        v = ChainValidator()
        v.build_graph(
            [{"reasoning_id": "ro_bad", "source_semantic_states": ["sem_missing"]}],
            [{"signal_id": "sem_existing", "signal_origin": "engine_a"}],
        )
        block = ProvenanceBlock(
            section_name="Test Section",
            reasoning_object_ids=["ro_bad"],
            semantic_state_ids=["sem_missing"],
            signal_engine_ids=[],
            completeness_state="partial",
        )
        violations = v.validate_section(block)
        assert len(violations) == 1
        assert violations[0]["broken_layer"] == "SEMANTICS"
        assert "sem_missing" in violations[0]["last_valid_id"]

    def test_missing_signal_engine_violation(self):
        """Semantic state has no signal_origin."""
        v = ChainValidator()
        v.build_graph(
            [{"reasoning_id": "ro_1", "source_semantic_states": ["sem_no_signal"]}],
            [{"signal_id": "sem_no_signal", "signal_origin": ""}],
        )
        block = ProvenanceBlock(
            section_name="Test Section",
            reasoning_object_ids=["ro_1"],
            semantic_state_ids=["sem_no_signal"],
            signal_engine_ids=[],
            completeness_state="degraded",
        )
        violations = v.validate_section(block)
        assert len(violations) == 1
        assert violations[0]["broken_layer"] == "SIGNALS"

    def test_no_graph_built_violation(self):
        v = ChainValidator()
        block = ProvenanceBlock(
            section_name="Test",
            reasoning_object_ids=["ro_1"],
            semantic_state_ids=["sem_1"],
            signal_engine_ids=["engine_1"],
            completeness_state="complete",
        )
        violations = v.validate_section(block)
        assert len(violations) == 1
        assert "build_graph()" in violations[0]["remediation"]


# --- Tests: validate_all ---

class TestValidateAll:
    def test_all_valid_sections(self, validator_with_graph):
        blocks = [
            ProvenanceBlock(
                section_name="Executive Summary",
                reasoning_object_ids=["ro_executive_summary"],
                semantic_state_ids=["sem_ai_dependency", "sem_concentration_risk"],
                signal_engine_ids=["allocation_engine", "attribution_engine"],
                completeness_state="complete",
            ),
            ProvenanceBlock(
                section_name="Market Regime",
                reasoning_object_ids=["ro_market_regime"],
                semantic_state_ids=["sem_regime_shift"],
                signal_engine_ids=["regime_engine"],
                completeness_state="complete",
            ),
        ]
        result = validator_with_graph.validate_all(blocks)
        assert result["overall_state"] == "valid"
        assert result["total_violations"] == 0
        assert result["budget_exceeded"] is False

    def test_degraded_state_with_few_violations(self, validator_with_graph):
        blocks = [
            ProvenanceBlock(
                section_name="Executive Summary",
                reasoning_object_ids=["ro_executive_summary"],
                semantic_state_ids=["sem_ai_dependency"],
                signal_engine_ids=["allocation_engine"],
                completeness_state="complete",
            ),
            ProvenanceBlock(
                section_name="Action Space",
                reasoning_object_ids=[],
                semantic_state_ids=[],
                signal_engine_ids=[],
                completeness_state="degraded",
            ),
        ]
        result = validator_with_graph.validate_all(blocks)
        assert result["overall_state"] == "degraded"
        assert result["total_violations"] >= 1

    def test_invalid_state_with_many_violations(self, validator_with_graph):
        blocks = [
            ProvenanceBlock(
                section_name=f"Section {i}",
                reasoning_object_ids=[],
                semantic_state_ids=[],
                signal_engine_ids=[],
                completeness_state="degraded",
            )
            for i in range(5)
        ]
        result = validator_with_graph.validate_all(blocks)
        assert result["overall_state"] == "invalid"
        assert result["total_violations"] > 3

    def test_execution_time_reported(self, validator_with_graph):
        blocks = [
            ProvenanceBlock(
                section_name="Executive Summary",
                reasoning_object_ids=["ro_executive_summary"],
                semantic_state_ids=["sem_ai_dependency"],
                signal_engine_ids=["allocation_engine"],
                completeness_state="complete",
            ),
        ]
        result = validator_with_graph.validate_all(blocks)
        assert "execution_time_ms" in result
        assert result["execution_time_ms"] >= 0

    def test_performance_within_budget(self, validator_with_graph):
        """Validate 9 sections completes within 2 seconds."""
        blocks = [
            ProvenanceBlock(
                section_name=f"Section {i}",
                reasoning_object_ids=["ro_executive_summary"],
                semantic_state_ids=["sem_ai_dependency"],
                signal_engine_ids=["allocation_engine"],
                completeness_state="complete",
            )
            for i in range(9)
        ]
        result = validator_with_graph.validate_all(blocks)
        assert result["execution_time_ms"] < 2000
        assert result["budget_exceeded"] is False


# --- Tests: load_provenance_blocks ---

class TestLoadProvenanceBlocks:
    def test_load_valid_sidecar(self, tmp_path):
        sidecar_data = {
            "run_context_id": "run_001",
            "timestamp": "2026-05-26T08:00:00Z",
            "schema_version": "1.0.0",
            "sections": [
                {
                    "section_name": "Executive Summary",
                    "reasoning_object_ids": ["ro_exec"],
                    "semantic_state_ids": ["sem_ai"],
                    "signal_engine_ids": ["allocation_engine"],
                    "completeness_state": "complete",
                    "unavailable_layers": [],
                },
                {
                    "section_name": "Market Regime",
                    "reasoning_object_ids": ["ro_regime"],
                    "semantic_state_ids": ["sem_regime"],
                    "signal_engine_ids": ["regime_engine"],
                    "completeness_state": "partial",
                    "unavailable_layers": [
                        {"layer": "SIGNALS", "reason": "engine timeout"}
                    ],
                },
            ],
        }
        sidecar_path = tmp_path / "run_001_provenance.yaml"
        with open(sidecar_path, "w") as f:
            yaml.safe_dump(sidecar_data, f)

        blocks = ChainValidator.load_provenance_blocks(str(sidecar_path))
        assert len(blocks) == 2
        assert blocks[0].section_name == "Executive Summary"
        assert blocks[0].completeness_state == "complete"
        assert blocks[1].section_name == "Market Regime"
        assert blocks[1].unavailability_reasons == ["SIGNALS: engine timeout"]

    def test_load_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            ChainValidator.load_provenance_blocks("/nonexistent/path.yaml")

    def test_load_malformed_file_raises(self, tmp_path):
        bad_path = tmp_path / "bad.yaml"
        with open(bad_path, "w") as f:
            yaml.safe_dump({"no_sections_key": True}, f)

        with pytest.raises(ValueError, match="missing 'sections' key"):
            ChainValidator.load_provenance_blocks(str(bad_path))
