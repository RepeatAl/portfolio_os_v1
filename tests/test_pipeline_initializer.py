"""Unit tests for governance.pipeline_initializer module.

Tests the cold-start wiring into pipeline initialization:
- Cold-start is detected when ledger file is missing
- Cold-start forces observability mode
- Cold-start tags provenance as bootstrap_derived
- Normal start uses configured enforcement mode
- Normal start tags provenance as authoritative

Validates: Requirements 31.1, 31.2
"""

from __future__ import annotations

import os
import tempfile

import pytest
import yaml

from governance.actor_identity import ActorIdentity, ActorType
from governance.pipeline_initializer import (
    PipelineInitResult,
    initialize_pipeline,
)
from governance.state_provenance_tagger import GovernanceProvenance


@pytest.fixture
def test_actor() -> ActorIdentity:
    """Create a test actor for pipeline initialization."""
    return ActorIdentity(
        actor_type=ActorType.SYSTEM,
        actor_id="pipeline_init_test",
        context={"source": "unit_test"},
        is_fallback=False,
    )


@pytest.fixture
def cold_start_project(tmp_path):
    """Create a project directory with NO ledger file (cold-start condition).

    Includes minimal config and governance files needed for enforcer init.
    """
    domainization = tmp_path / ".domainization"
    domainization.mkdir()

    # Create minimal config.yaml with enforcement mode
    config = {
        "governance_enforcement": {"mode": "hard"},
    }
    config_path = domainization / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)

    # Create minimal lifecycle_state_machine.yaml
    state_machine = {
        "schema_version": "1.0.0",
        "artifact_types": {},
    }
    with open(domainization / "lifecycle_state_machine.yaml", "w") as f:
        yaml.dump(state_machine, f)

    # Create minimal artifact_registry.yaml
    with open(domainization / "artifact_registry.yaml", "w") as f:
        yaml.dump({"artifacts": {}}, f)

    # Create minimal domain_registry.yaml
    with open(domainization / "domain_registry.yaml", "w") as f:
        yaml.dump({"domains": {}}, f)

    # NO mutation_audit_ledger.yaml — this triggers cold-start
    return tmp_path


@pytest.fixture
def normal_start_project(tmp_path):
    """Create a project directory WITH a ledger file (normal start condition).

    Includes config with a specific enforcement mode.
    """
    domainization = tmp_path / ".domainization"
    domainization.mkdir()

    # Create config.yaml with soft enforcement mode
    config = {
        "governance_enforcement": {"mode": "soft"},
    }
    config_path = domainization / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)

    # Create minimal lifecycle_state_machine.yaml
    state_machine = {
        "schema_version": "1.0.0",
        "artifact_types": {},
    }
    with open(domainization / "lifecycle_state_machine.yaml", "w") as f:
        yaml.dump(state_machine, f)

    # Create minimal artifact_registry.yaml
    with open(domainization / "artifact_registry.yaml", "w") as f:
        yaml.dump({"artifacts": {}}, f)

    # Create minimal domain_registry.yaml
    with open(domainization / "domain_registry.yaml", "w") as f:
        yaml.dump({"domains": {}}, f)

    # Create mutation_audit_ledger.yaml — this means NOT cold-start
    ledger = {
        "schema_version": "1.0.0",
        "entries": [
            {
                "entry_id": "existing-entry-001",
                "event_type": "GOVERNANCE_EVENT",
                "timestamp": "2026-05-29T10:00:00+00:00",
                "actor": {
                    "actor_type": "SYSTEM",
                    "actor_id": "test_setup",
                    "context": {},
                    "is_fallback": False,
                },
                "governance_policy_version": "sha256:abc123",
                "severity": "INFO",
                "details": {"action": "test_setup"},
            }
        ],
    }
    with open(domainization / "mutation_audit_ledger.yaml", "w") as f:
        yaml.dump(ledger, f)

    return tmp_path


class TestColdStartDetection:
    """Tests that cold-start is detected when ledger file is missing."""

    def test_cold_start_detected_when_no_ledger(
        self, cold_start_project, test_actor
    ):
        """Pipeline detects cold-start when mutation_audit_ledger.yaml is missing."""
        result = initialize_pipeline(
            base_path=str(cold_start_project),
            actor=test_actor,
        )

        assert result.is_cold_start is True

    def test_not_cold_start_when_ledger_exists(
        self, normal_start_project, test_actor
    ):
        """Pipeline does NOT detect cold-start when ledger file exists."""
        result = initialize_pipeline(
            base_path=str(normal_start_project),
            actor=test_actor,
        )

        assert result.is_cold_start is False

    def test_cold_start_detected_when_domainization_dir_empty(
        self, tmp_path, test_actor
    ):
        """Cold-start detected when .domainization exists but has no ledger."""
        domainization = tmp_path / ".domainization"
        domainization.mkdir()

        # Minimal config for enforcer init
        config = {"governance_enforcement": {"mode": "hard"}}
        with open(domainization / "config.yaml", "w") as f:
            yaml.dump(config, f)
        with open(domainization / "lifecycle_state_machine.yaml", "w") as f:
            yaml.dump({"schema_version": "1.0.0", "artifact_types": {}}, f)
        with open(domainization / "artifact_registry.yaml", "w") as f:
            yaml.dump({"artifacts": {}}, f)
        with open(domainization / "domain_registry.yaml", "w") as f:
            yaml.dump({"domains": {}}, f)

        result = initialize_pipeline(
            base_path=str(tmp_path),
            actor=test_actor,
        )

        assert result.is_cold_start is True


class TestColdStartForcesObservability:
    """Tests that cold-start forces observability mode regardless of config."""

    def test_cold_start_forces_observability_over_hard_mode(
        self, cold_start_project, test_actor
    ):
        """Even when config says 'hard', cold-start forces observability."""
        result = initialize_pipeline(
            base_path=str(cold_start_project),
            actor=test_actor,
        )

        assert result.enforcement_mode == "observability"

    def test_cold_start_enforcers_use_observability(
        self, cold_start_project, test_actor
    ):
        """Enforcers initialized during cold-start use observability mode."""
        result = initialize_pipeline(
            base_path=str(cold_start_project),
            actor=test_actor,
        )

        assert result.enforcers["enforcement_mode"] == "observability"


class TestColdStartProvenanceTagging:
    """Tests that cold-start tags provenance as bootstrap_derived."""

    def test_cold_start_provenance_is_bootstrap_derived(
        self, cold_start_project, test_actor
    ):
        """Cold-start sets provenance to bootstrap_derived."""
        result = initialize_pipeline(
            base_path=str(cold_start_project),
            actor=test_actor,
        )

        assert result.provenance == GovernanceProvenance.BOOTSTRAP_DERIVED

    def test_cold_start_tagger_reflects_bootstrap_derived(
        self, cold_start_project, test_actor
    ):
        """The provenance tagger's current state is bootstrap_derived after cold-start."""
        result = initialize_pipeline(
            base_path=str(cold_start_project),
            actor=test_actor,
        )

        assert (
            result.provenance_tagger.get_current_provenance()
            == GovernanceProvenance.BOOTSTRAP_DERIVED
        )

    def test_cold_start_returns_bootstrap_entry(
        self, cold_start_project, test_actor
    ):
        """Cold-start returns a bootstrap LedgerEntry."""
        result = initialize_pipeline(
            base_path=str(cold_start_project),
            actor=test_actor,
        )

        assert result.bootstrap_entry is not None
        assert result.bootstrap_entry.event_type == "GOVERNANCE_EVENT"
        assert result.bootstrap_entry.severity == "INFO"
        assert (
            result.bootstrap_entry.details["action"]
            == "cold_start_initialization"
        )
        assert (
            result.bootstrap_entry.details["provenance"]
            == "bootstrap_derived"
        )


class TestNormalStartEnforcementMode:
    """Tests that normal start uses configured enforcement mode."""

    def test_normal_start_uses_configured_soft_mode(
        self, normal_start_project, test_actor
    ):
        """Normal start reads enforcement mode from config (soft)."""
        result = initialize_pipeline(
            base_path=str(normal_start_project),
            actor=test_actor,
        )

        assert result.enforcement_mode == "soft"

    def test_normal_start_enforcers_use_configured_mode(
        self, normal_start_project, test_actor
    ):
        """Enforcers initialized during normal start use the configured mode."""
        result = initialize_pipeline(
            base_path=str(normal_start_project),
            actor=test_actor,
        )

        assert result.enforcers["enforcement_mode"] == "soft"

    def test_normal_start_uses_hard_mode_from_config(
        self, tmp_path, test_actor
    ):
        """Normal start correctly reads 'hard' enforcement mode."""
        domainization = tmp_path / ".domainization"
        domainization.mkdir()

        config = {"governance_enforcement": {"mode": "hard"}}
        with open(domainization / "config.yaml", "w") as f:
            yaml.dump(config, f)
        with open(domainization / "lifecycle_state_machine.yaml", "w") as f:
            yaml.dump({"schema_version": "1.0.0", "artifact_types": {}}, f)
        with open(domainization / "artifact_registry.yaml", "w") as f:
            yaml.dump({"artifacts": {}}, f)
        with open(domainization / "domain_registry.yaml", "w") as f:
            yaml.dump({"domains": {}}, f)

        # Create ledger to prevent cold-start
        ledger = {
            "schema_version": "1.0.0",
            "entries": [
                {
                    "entry_id": "test-entry",
                    "event_type": "GOVERNANCE_EVENT",
                    "timestamp": "2026-05-29T10:00:00+00:00",
                    "actor": {
                        "actor_type": "SYSTEM",
                        "actor_id": "test",
                        "context": {},
                        "is_fallback": False,
                    },
                    "governance_policy_version": "sha256:abc",
                    "severity": "INFO",
                    "details": {},
                }
            ],
        }
        with open(domainization / "mutation_audit_ledger.yaml", "w") as f:
            yaml.dump(ledger, f)

        result = initialize_pipeline(
            base_path=str(tmp_path),
            actor=test_actor,
        )

        assert result.enforcement_mode == "hard"


class TestNormalStartProvenanceTagging:
    """Tests that normal start tags provenance as authoritative."""

    def test_normal_start_provenance_is_authoritative(
        self, normal_start_project, test_actor
    ):
        """Normal start sets provenance to authoritative."""
        result = initialize_pipeline(
            base_path=str(normal_start_project),
            actor=test_actor,
        )

        assert result.provenance == GovernanceProvenance.AUTHORITATIVE

    def test_normal_start_tagger_reflects_authoritative(
        self, normal_start_project, test_actor
    ):
        """The provenance tagger's current state is authoritative after normal start."""
        result = initialize_pipeline(
            base_path=str(normal_start_project),
            actor=test_actor,
        )

        assert (
            result.provenance_tagger.get_current_provenance()
            == GovernanceProvenance.AUTHORITATIVE
        )

    def test_normal_start_has_no_bootstrap_entry(
        self, normal_start_project, test_actor
    ):
        """Normal start does not produce a bootstrap LedgerEntry."""
        result = initialize_pipeline(
            base_path=str(normal_start_project),
            actor=test_actor,
        )

        assert result.bootstrap_entry is None


class TestPipelineInitResultContract:
    """Tests the PipelineInitResult dataclass contract."""

    def test_result_has_all_required_fields(
        self, normal_start_project, test_actor
    ):
        """PipelineInitResult contains all expected fields."""
        result = initialize_pipeline(
            base_path=str(normal_start_project),
            actor=test_actor,
        )

        assert hasattr(result, "enforcement_mode")
        assert hasattr(result, "is_cold_start")
        assert hasattr(result, "provenance")
        assert hasattr(result, "bootstrap_entry")
        assert hasattr(result, "enforcers")
        assert hasattr(result, "provenance_tagger")

    def test_enforcers_dict_contains_expected_keys(
        self, normal_start_project, test_actor
    ):
        """Enforcers dictionary contains gate_framework, lifecycle, boundary."""
        result = initialize_pipeline(
            base_path=str(normal_start_project),
            actor=test_actor,
        )

        assert "enforcement_mode" in result.enforcers
        assert "gate_framework" in result.enforcers
        assert "lifecycle_enforcer" in result.enforcers
        assert "boundary_enforcer" in result.enforcers
