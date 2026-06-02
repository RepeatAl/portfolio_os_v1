"""Unit tests for governance/influence_graph.py.

Covers deterministic edge cases: valid/invalid YAML loading, missing fields,
missing file, and module exclusion on missing declaration.

Does NOT duplicate property tests (round-trip, cycle detection completeness,
directionality enforcement across generated inputs).

Validates: Requirements 1.2, 1.3
"""

from __future__ import annotations

import os
import tempfile

import pytest
import yaml

from governance.influence_graph import (
    CycleDetectionResult,
    DirectionalityViolation,
    GovernanceInfluenceGraph,
    InfluenceDirection,
    ModuleDependencyDeclaration,
)
from governance.mutation_audit_ledger import MutationAuditLedger


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_dir():
    """Provide a temporary directory for test YAML files."""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def valid_declarations_yaml(tmp_dir: str) -> str:
    """Create a valid governance_influence_declarations.yaml."""
    path = os.path.join(tmp_dir, "governance_influence_declarations.yaml")
    data = {
        "schema_version": "1.0.0",
        "modules": [
            {
                "module_id": "module_a",
                "read_dependencies": [],
                "write_dependencies": ["module_b"],
                "influence_direction": "upstream",
            },
            {
                "module_id": "module_b",
                "read_dependencies": ["module_a"],
                "write_dependencies": [],
                "influence_direction": "downstream",
            },
        ],
    }
    with open(path, "w") as f:
        yaml.dump(data, f)
    return path


@pytest.fixture
def ledger(tmp_dir: str) -> MutationAuditLedger:
    """Create a temporary ledger for testing."""
    ledger_path = os.path.join(tmp_dir, "ledger.yaml")
    return MutationAuditLedger(ledger_path)


# ---------------------------------------------------------------------------
# Test: Valid YAML Loading
# ---------------------------------------------------------------------------


class TestValidYAMLLoading:
    """Tests for successful loading of well-formed declarations."""

    def test_load_valid_declarations(self, valid_declarations_yaml: str):
        """Valid YAML with correct schema loads all module declarations."""
        graph = GovernanceInfluenceGraph(valid_declarations_yaml)
        declarations = graph.load_declarations()

        assert len(declarations) == 2
        assert declarations[0].module_id == "module_a"
        assert declarations[0].influence_direction == InfluenceDirection.UPSTREAM
        assert declarations[0].write_dependencies == ("module_b",)
        assert declarations[1].module_id == "module_b"
        assert declarations[1].influence_direction == InfluenceDirection.DOWNSTREAM

    def test_validate_at_init_with_valid_acyclic_graph(
        self, valid_declarations_yaml: str, ledger: MutationAuditLedger
    ):
        """validate_at_init succeeds for a valid acyclic graph without violations."""
        graph = GovernanceInfluenceGraph(valid_declarations_yaml, ledger=ledger)
        is_valid, errors = graph.validate_at_init()

        assert is_valid is True
        assert errors == []


# ---------------------------------------------------------------------------
# Test: Invalid YAML Loading
# ---------------------------------------------------------------------------


class TestInvalidYAMLLoading:
    """Tests for malformed or structurally invalid YAML files."""

    def test_missing_modules_key(self, tmp_dir: str):
        """YAML without 'modules' key raises ValueError."""
        path = os.path.join(tmp_dir, "bad.yaml")
        with open(path, "w") as f:
            yaml.dump({"schema_version": "1.0.0", "not_modules": []}, f)

        graph = GovernanceInfluenceGraph(path)
        with pytest.raises(ValueError, match="missing 'modules' key"):
            graph.load_declarations()

    def test_invalid_influence_direction_skipped(self, tmp_dir: str):
        """Module with invalid influence_direction is skipped during loading."""
        path = os.path.join(tmp_dir, "bad_direction.yaml")
        data = {
            "schema_version": "1.0.0",
            "modules": [
                {
                    "module_id": "good_module",
                    "read_dependencies": [],
                    "write_dependencies": [],
                    "influence_direction": "upstream",
                },
                {
                    "module_id": "bad_module",
                    "read_dependencies": [],
                    "write_dependencies": [],
                    "influence_direction": "invalid_direction",
                },
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        graph = GovernanceInfluenceGraph(path)
        declarations = graph.load_declarations()

        # Only the valid module should be loaded
        assert len(declarations) == 1
        assert declarations[0].module_id == "good_module"

    def test_module_missing_module_id_skipped(self, tmp_dir: str):
        """Module entry missing 'module_id' is skipped."""
        path = os.path.join(tmp_dir, "no_id.yaml")
        data = {
            "schema_version": "1.0.0",
            "modules": [
                {
                    "read_dependencies": [],
                    "write_dependencies": [],
                    "influence_direction": "upstream",
                },
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        graph = GovernanceInfluenceGraph(path)
        declarations = graph.load_declarations()

        assert len(declarations) == 0


# ---------------------------------------------------------------------------
# Test: Missing File
# ---------------------------------------------------------------------------


class TestMissingFile:
    """Tests for behavior when the declarations file does not exist."""

    def test_load_declarations_file_not_found(self, tmp_dir: str):
        """Loading from a non-existent file raises FileNotFoundError."""
        path = os.path.join(tmp_dir, "nonexistent.yaml")
        graph = GovernanceInfluenceGraph(path)

        with pytest.raises(FileNotFoundError):
            graph.load_declarations()

    def test_validate_at_init_file_not_found(
        self, tmp_dir: str, ledger: MutationAuditLedger
    ):
        """validate_at_init returns failure when file is missing."""
        path = os.path.join(tmp_dir, "nonexistent.yaml")
        graph = GovernanceInfluenceGraph(path, ledger=ledger)

        is_valid, errors = graph.validate_at_init()

        assert is_valid is False
        assert len(errors) == 1
        assert "not found" in errors[0].lower() or "not found" in errors[0]


# ---------------------------------------------------------------------------
# Test: Module Exclusion on Missing Declaration
# ---------------------------------------------------------------------------


class TestModuleExclusion:
    """Tests for module exclusion when declarations are missing or invalid."""

    def test_empty_modules_list_fails_validation(self, tmp_dir: str):
        """An empty modules list causes validate_at_init to fail."""
        path = os.path.join(tmp_dir, "empty.yaml")
        data = {"schema_version": "1.0.0", "modules": []}
        with open(path, "w") as f:
            yaml.dump(data, f)

        graph = GovernanceInfluenceGraph(path)
        is_valid, errors = graph.validate_at_init()

        assert is_valid is False
        assert any("no valid module" in e.lower() for e in errors)

    def test_validate_declaration_rejects_empty_module_id(self):
        """validate_declaration returns False for empty module_id."""
        decl = ModuleDependencyDeclaration(
            module_id="",
            read_dependencies=(),
            write_dependencies=(),
            influence_direction=InfluenceDirection.UPSTREAM,
        )
        graph = GovernanceInfluenceGraph.__new__(GovernanceInfluenceGraph)
        assert graph.validate_declaration(decl) is False

    def test_validate_declaration_accepts_valid_declaration(self):
        """validate_declaration returns True for a well-formed declaration."""
        decl = ModuleDependencyDeclaration(
            module_id="valid_module",
            read_dependencies=("dep_a",),
            write_dependencies=("dep_b",),
            influence_direction=InfluenceDirection.DOWNSTREAM,
        )
        graph = GovernanceInfluenceGraph.__new__(GovernanceInfluenceGraph)
        assert graph.validate_declaration(decl) is True


# ---------------------------------------------------------------------------
# Test: Cycle Detection (deterministic cases)
# ---------------------------------------------------------------------------


class TestCycleDetectionDeterministic:
    """Deterministic cycle detection tests for known graph structures."""

    def test_direct_cycle_detected(self, tmp_dir: str, ledger: MutationAuditLedger):
        """A direct cycle (A writes B, B writes A) is detected."""
        path = os.path.join(tmp_dir, "cycle.yaml")
        data = {
            "schema_version": "1.0.0",
            "modules": [
                {
                    "module_id": "a",
                    "read_dependencies": [],
                    "write_dependencies": ["b"],
                    "influence_direction": "upstream",
                },
                {
                    "module_id": "b",
                    "read_dependencies": [],
                    "write_dependencies": ["a"],
                    "influence_direction": "upstream",
                },
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        graph = GovernanceInfluenceGraph(path, ledger=ledger)
        graph.load_declarations()
        graph.build_graph()
        result = graph.detect_cycles()

        assert result.has_cycle is True
        assert len(result.cycle_path) >= 2

    def test_no_cycle_in_linear_graph(self, tmp_dir: str):
        """A linear graph (A->B->C) has no cycle."""
        path = os.path.join(tmp_dir, "linear.yaml")
        data = {
            "schema_version": "1.0.0",
            "modules": [
                {
                    "module_id": "a",
                    "read_dependencies": [],
                    "write_dependencies": ["b"],
                    "influence_direction": "upstream",
                },
                {
                    "module_id": "b",
                    "read_dependencies": [],
                    "write_dependencies": ["c"],
                    "influence_direction": "upstream",
                },
                {
                    "module_id": "c",
                    "read_dependencies": [],
                    "write_dependencies": [],
                    "influence_direction": "upstream",
                },
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        graph = GovernanceInfluenceGraph(path)
        graph.load_declarations()
        graph.build_graph()
        result = graph.detect_cycles()

        assert result.has_cycle is False
        assert result.cycle_path == []


# ---------------------------------------------------------------------------
# Test: Directionality Enforcement (deterministic cases)
# ---------------------------------------------------------------------------


class TestDirectionalityEnforcementDeterministic:
    """Deterministic directionality enforcement tests."""

    def test_downstream_writing_upstream_produces_violation(
        self, tmp_dir: str, ledger: MutationAuditLedger
    ):
        """A downstream module writing to an upstream module is a violation."""
        path = os.path.join(tmp_dir, "violation.yaml")
        data = {
            "schema_version": "1.0.0",
            "modules": [
                {
                    "module_id": "upstream_mod",
                    "read_dependencies": [],
                    "write_dependencies": [],
                    "influence_direction": "upstream",
                },
                {
                    "module_id": "downstream_mod",
                    "read_dependencies": [],
                    "write_dependencies": ["upstream_mod"],
                    "influence_direction": "downstream",
                },
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        graph = GovernanceInfluenceGraph(path, ledger=ledger)
        graph.load_declarations()
        graph.build_graph()
        violations = graph.enforce_directionality()

        assert len(violations) == 1
        assert violations[0].violating_module == "downstream_mod"
        assert violations[0].target_module == "upstream_mod"

    def test_upstream_writing_downstream_no_violation(self, tmp_dir: str):
        """An upstream module writing to a downstream module is NOT a violation."""
        path = os.path.join(tmp_dir, "no_violation.yaml")
        data = {
            "schema_version": "1.0.0",
            "modules": [
                {
                    "module_id": "upstream_mod",
                    "read_dependencies": [],
                    "write_dependencies": ["downstream_mod"],
                    "influence_direction": "upstream",
                },
                {
                    "module_id": "downstream_mod",
                    "read_dependencies": [],
                    "write_dependencies": [],
                    "influence_direction": "downstream",
                },
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        graph = GovernanceInfluenceGraph(path)
        graph.load_declarations()
        graph.build_graph()
        violations = graph.enforce_directionality()

        assert violations == []
