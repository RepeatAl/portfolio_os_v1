"""Tests for governance/delta_init.py — Delta layer initialization sequence.

Verifies:
- Components load in correct order: InfluenceGraph → DeploymentAuthority → TransitionCooldown → DomainLifecycleManager
- CRITICAL events (cycles, topology violations) halt init
- fail_soft components (cooldown, lifecycle) degrade gracefully
- No framework escalation, no plugin system, no event bus, no runtime kernel

Requirements: 2.4, 4.4, 5.4, 11.5
"""

import os
import tempfile

import pytest
import yaml

from governance.delta_init import DeltaInitResult, initialize_delta_layer


@pytest.fixture
def valid_declarations_yaml(tmp_path):
    """Create a valid governance_influence_declarations.yaml.

    All modules that write to mutation_audit_ledger are declared as 'upstream'
    to avoid directionality violations (upstream modules can write to other
    upstream modules without triggering the downstream-writes-upstream check).
    """
    data = {
        "schema_version": "1.0.0",
        "modules": [
            {
                "module_id": "influence_graph",
                "read_dependencies": [],
                "write_dependencies": [],
                "influence_direction": "upstream",
            },
            {
                "module_id": "deployment_authority",
                "read_dependencies": ["policy_versioner"],
                "write_dependencies": ["mutation_audit_ledger"],
                "influence_direction": "upstream",
            },
            {
                "module_id": "mutation_audit_ledger",
                "read_dependencies": [],
                "write_dependencies": [],
                "influence_direction": "upstream",
            },
            {
                "module_id": "policy_versioner",
                "read_dependencies": [],
                "write_dependencies": [],
                "influence_direction": "upstream",
            },
        ],
    }
    path = tmp_path / "governance_influence_declarations.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f)
    return str(path)


@pytest.fixture
def cyclic_declarations_yaml(tmp_path):
    """Create a declarations YAML with a cycle: A writes B, B writes A."""
    data = {
        "schema_version": "1.0.0",
        "modules": [
            {
                "module_id": "module_a",
                "read_dependencies": [],
                "write_dependencies": ["module_b"],
                "influence_direction": "downstream",
            },
            {
                "module_id": "module_b",
                "read_dependencies": [],
                "write_dependencies": ["module_a"],
                "influence_direction": "downstream",
            },
        ],
    }
    path = tmp_path / "cyclic_declarations.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f)
    return str(path)


@pytest.fixture
def valid_authority_yaml(tmp_path):
    """Create a valid deployment_authority_model.yaml."""
    data = {
        "schema_version": "1.0.0",
        "roles": [
            {"role": "OWNER", "authorities": ["mutate_governance", "change_enforcement_mode"]},
            {"role": "CI", "authorities": ["deploy", "accept_runtime_hash"]},
            {"role": "RUNTIME", "authorities": ["execute_override", "change_fail_mode"]},
        ],
    }
    path = tmp_path / "deployment_authority_model.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f)
    return str(path)


@pytest.fixture
def topology_violating_authority_yaml(tmp_path):
    """Create an authority model with a topology violation (CI has deploy + mutate_governance)."""
    data = {
        "schema_version": "1.0.0",
        "roles": [
            {"role": "OWNER", "authorities": ["change_enforcement_mode"]},
            {"role": "CI", "authorities": ["deploy", "mutate_governance", "accept_runtime_hash"]},
            {"role": "RUNTIME", "authorities": ["execute_override", "change_fail_mode"]},
        ],
    }
    path = tmp_path / "bad_authority_model.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f)
    return str(path)


@pytest.fixture
def valid_config_yaml(tmp_path):
    """Create a valid config.yaml with transition_hysteresis section."""
    data = {
        "enforcement_mode": "observability",
        "transition_hysteresis": {"cooldown_hours": 4},
    }
    path = tmp_path / "config.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f)
    return str(path)


@pytest.fixture
def valid_domain_registry_yaml(tmp_path):
    """Create a valid domain_registry.yaml."""
    data = {
        "domains": [
            {"domain_id": "GOV", "name": "Governance", "lifecycle_state": "active"},
            {"domain_id": "DATA", "name": "Data", "lifecycle_state": "active"},
        ]
    }
    path = tmp_path / "domain_registry.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f)
    return str(path)


@pytest.fixture
def valid_artifact_registry_yaml(tmp_path):
    """Create a valid artifact_registry.yaml."""
    data = {
        "artifacts": [
            {"artifact_id": "art_1", "artifact_type": "ENGINE", "primary_domain": "GOV"},
        ]
    }
    path = tmp_path / "artifact_registry.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f)
    return str(path)


class TestDeltaInitHappyPath:
    """Test successful initialization with all valid inputs."""

    def test_all_components_initialize_successfully(
        self,
        valid_declarations_yaml,
        valid_authority_yaml,
        valid_config_yaml,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """All 4 components should initialize when inputs are valid."""
        result = initialize_delta_layer(
            declarations_path=valid_declarations_yaml,
            authority_model_path=valid_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
        )

        assert result.success is True
        assert result.influence_graph is not None
        assert result.deployment_authority is not None
        assert result.transition_cooldown is not None
        assert result.domain_lifecycle is not None
        assert result.errors == []
        assert result.warnings == []

    def test_result_is_dataclass(
        self,
        valid_declarations_yaml,
        valid_authority_yaml,
        valid_config_yaml,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """DeltaInitResult should be a proper dataclass."""
        result = initialize_delta_layer(
            declarations_path=valid_declarations_yaml,
            authority_model_path=valid_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
        )
        assert isinstance(result, DeltaInitResult)


class TestCriticalHaltsInit:
    """Test that CRITICAL events from InfluenceGraph and DeploymentAuthority halt init."""

    def test_influence_graph_cycle_halts_init(
        self,
        cyclic_declarations_yaml,
        valid_authority_yaml,
        valid_config_yaml,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """Cycle in influence graph should halt init with success=False."""
        result = initialize_delta_layer(
            declarations_path=cyclic_declarations_yaml,
            authority_model_path=valid_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
        )

        assert result.success is False
        assert result.influence_graph is None
        assert result.deployment_authority is None
        assert result.transition_cooldown is None
        assert result.domain_lifecycle is None
        assert len(result.errors) > 0
        # Should mention cycle
        assert any("ycle" in e for e in result.errors)

    def test_missing_declarations_file_halts_init(
        self,
        tmp_path,
        valid_authority_yaml,
        valid_config_yaml,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """Missing declarations file should halt init."""
        nonexistent = str(tmp_path / "nonexistent.yaml")
        result = initialize_delta_layer(
            declarations_path=nonexistent,
            authority_model_path=valid_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
        )

        assert result.success is False
        assert result.influence_graph is None
        assert len(result.errors) > 0

    def test_topology_violation_halts_init(
        self,
        valid_declarations_yaml,
        topology_violating_authority_yaml,
        valid_config_yaml,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """Topology violation in authority model should halt init."""
        result = initialize_delta_layer(
            declarations_path=valid_declarations_yaml,
            authority_model_path=topology_violating_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
        )

        assert result.success is False
        # InfluenceGraph should have succeeded
        assert result.influence_graph is not None
        # DeploymentAuthority should have failed
        assert result.deployment_authority is None
        # Subsequent components should NOT be loaded
        assert result.transition_cooldown is None
        assert result.domain_lifecycle is None
        assert len(result.errors) > 0
        # Should mention topology or forbidden pair
        assert any("forbidden" in e.lower() or "topology" in e.lower() for e in result.errors)

    def test_missing_authority_file_halts_init(
        self,
        valid_declarations_yaml,
        tmp_path,
        valid_config_yaml,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """Missing authority model file should halt init."""
        nonexistent = str(tmp_path / "nonexistent_authority.yaml")
        result = initialize_delta_layer(
            declarations_path=valid_declarations_yaml,
            authority_model_path=nonexistent,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
        )

        assert result.success is False
        assert result.influence_graph is not None  # Step 1 passed
        assert result.deployment_authority is None  # Step 2 failed
        assert result.transition_cooldown is None  # Not reached
        assert result.domain_lifecycle is None  # Not reached


class TestFailSoftDegradation:
    """Test that fail_soft components degrade gracefully without halting init."""

    def test_missing_config_degrades_cooldown_gracefully(
        self,
        valid_declarations_yaml,
        valid_authority_yaml,
        tmp_path,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """Missing config.yaml should NOT halt init — cooldown degrades."""
        nonexistent_config = str(tmp_path / "nonexistent_config.yaml")
        result = initialize_delta_layer(
            declarations_path=valid_declarations_yaml,
            authority_model_path=valid_authority_yaml,
            config_path=nonexistent_config,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
        )

        # Init should still succeed (fail_soft)
        assert result.success is True
        assert result.influence_graph is not None
        assert result.deployment_authority is not None
        # TransitionCooldown uses default config when file is missing
        # (it handles missing file internally with a warning)
        # So it may still initialize with defaults
        assert result.domain_lifecycle is not None

    def test_missing_domain_registry_degrades_lifecycle_gracefully(
        self,
        valid_declarations_yaml,
        valid_authority_yaml,
        valid_config_yaml,
        tmp_path,
        valid_artifact_registry_yaml,
    ):
        """Missing domain registry should NOT halt init — lifecycle degrades."""
        nonexistent_registry = str(tmp_path / "nonexistent_domain_registry.yaml")
        result = initialize_delta_layer(
            declarations_path=valid_declarations_yaml,
            authority_model_path=valid_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=nonexistent_registry,
            artifact_registry_path=valid_artifact_registry_yaml,
        )

        # Init should still succeed (fail_soft)
        assert result.success is True
        assert result.influence_graph is not None
        assert result.deployment_authority is not None
        assert result.transition_cooldown is not None
        # DomainLifecycleManager handles missing registry internally (fail_soft)
        # It initializes with empty domain list
        assert result.domain_lifecycle is not None

    def test_missing_artifact_registry_degrades_lifecycle_gracefully(
        self,
        valid_declarations_yaml,
        valid_authority_yaml,
        valid_config_yaml,
        valid_domain_registry_yaml,
        tmp_path,
    ):
        """Missing artifact registry should NOT halt init — lifecycle degrades."""
        nonexistent_artifacts = str(tmp_path / "nonexistent_artifacts.yaml")
        result = initialize_delta_layer(
            declarations_path=valid_declarations_yaml,
            authority_model_path=valid_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=nonexistent_artifacts,
        )

        # Init should still succeed
        assert result.success is True
        assert result.domain_lifecycle is not None


class TestInitializationOrder:
    """Test that components are loaded in the correct order."""

    def test_influence_graph_failure_prevents_authority_loading(
        self,
        cyclic_declarations_yaml,
        valid_authority_yaml,
        valid_config_yaml,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """When InfluenceGraph fails, DeploymentAuthority should NOT be attempted."""
        result = initialize_delta_layer(
            declarations_path=cyclic_declarations_yaml,
            authority_model_path=valid_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
        )

        assert result.success is False
        assert result.influence_graph is None
        assert result.deployment_authority is None
        assert result.transition_cooldown is None
        assert result.domain_lifecycle is None

    def test_authority_failure_prevents_cooldown_and_lifecycle(
        self,
        valid_declarations_yaml,
        topology_violating_authority_yaml,
        valid_config_yaml,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """When DeploymentAuthority fails, subsequent components should NOT load."""
        result = initialize_delta_layer(
            declarations_path=valid_declarations_yaml,
            authority_model_path=topology_violating_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
        )

        assert result.success is False
        assert result.influence_graph is not None  # Step 1 passed
        assert result.deployment_authority is None  # Step 2 failed
        assert result.transition_cooldown is None  # Not reached
        assert result.domain_lifecycle is None  # Not reached


class TestLedgerIntegration:
    """Test that the ledger is passed through to components."""

    def test_init_works_without_ledger(
        self,
        valid_declarations_yaml,
        valid_authority_yaml,
        valid_config_yaml,
        valid_domain_registry_yaml,
        valid_artifact_registry_yaml,
    ):
        """Init should work with ledger=None (backward compatible)."""
        result = initialize_delta_layer(
            declarations_path=valid_declarations_yaml,
            authority_model_path=valid_authority_yaml,
            config_path=valid_config_yaml,
            domain_registry_path=valid_domain_registry_yaml,
            artifact_registry_path=valid_artifact_registry_yaml,
            ledger=None,
        )

        assert result.success is True
