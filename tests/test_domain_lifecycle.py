"""Unit tests for governance/domain_lifecycle.py.

Covers deterministic edge cases: default state=active, deprecation cannot_own
check, reassignment plan generation, and invalid transition rejection.

Does NOT duplicate property tests (lifecycle transition validation across
all state combinations).

Validates: Requirements 9.4, 10.3
"""

from __future__ import annotations

import os
import tempfile

import pytest
import yaml

from governance.actor_identity import ActorIdentity, ActorType
from governance.domain_lifecycle import (
    DeprecationRequest,
    DomainLifecycleManager,
    DomainLifecycleState,
    ReassignmentPlan,
    ReassignmentPlanEntry,
    VALID_DOMAIN_TRANSITIONS,
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
def ledger(tmp_dir: str) -> MutationAuditLedger:
    """Create a temporary ledger for testing."""
    ledger_path = os.path.join(tmp_dir, "ledger.yaml")
    return MutationAuditLedger(ledger_path)


@pytest.fixture
def test_actor() -> ActorIdentity:
    """Create a test actor identity."""
    return ActorIdentity(
        actor_type=ActorType.USER,
        actor_id="test_user",
        context={},
        is_fallback=False,
    )


def _write_domain_registry(tmp_dir: str, domains: list[dict]) -> str:
    """Write a domain_registry.yaml and return its path."""
    path = os.path.join(tmp_dir, "domain_registry.yaml")
    with open(path, "w") as f:
        yaml.dump({"domains": domains}, f)
    return path


def _write_artifact_registry(tmp_dir: str, artifacts: list[dict]) -> str:
    """Write an artifact_registry.yaml and return its path."""
    path = os.path.join(tmp_dir, "artifact_registry.yaml")
    with open(path, "w") as f:
        yaml.dump({"artifacts": artifacts}, f)
    return path


# ---------------------------------------------------------------------------
# Test: Default State = Active
# ---------------------------------------------------------------------------


class TestDefaultStateActive:
    """Tests for default lifecycle state behavior."""

    def test_unknown_domain_defaults_to_active(self, tmp_dir: str):
        """Domain not in registry defaults to ACTIVE state."""
        domain_path = _write_domain_registry(tmp_dir, [])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        state = manager.get_domain_state("NONEXISTENT")

        assert state == DomainLifecycleState.ACTIVE

    def test_domain_without_lifecycle_state_field_defaults_to_active(self, tmp_dir: str):
        """Domain entry missing lifecycle_state field defaults to ACTIVE."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "GOV", "name": "Governance"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        state = manager.get_domain_state("GOV")

        assert state == DomainLifecycleState.ACTIVE

    def test_domain_with_explicit_active_state(self, tmp_dir: str):
        """Domain with explicit lifecycle_state='active' returns ACTIVE."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "GOV", "name": "Governance", "lifecycle_state": "active"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        state = manager.get_domain_state("GOV")

        assert state == DomainLifecycleState.ACTIVE

    def test_domain_with_deprecated_state(self, tmp_dir: str):
        """Domain with lifecycle_state='deprecated' returns DEPRECATED."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "OLD", "name": "Old Domain", "lifecycle_state": "deprecated"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        state = manager.get_domain_state("OLD")

        assert state == DomainLifecycleState.DEPRECATED

    def test_domain_with_invalid_lifecycle_state_defaults_to_active(self, tmp_dir: str):
        """Domain with invalid lifecycle_state value defaults to ACTIVE."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "BAD", "name": "Bad State", "lifecycle_state": "invalid_state"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        state = manager.get_domain_state("BAD")

        assert state == DomainLifecycleState.ACTIVE


# ---------------------------------------------------------------------------
# Test: Invalid Transition Rejection
# ---------------------------------------------------------------------------


class TestInvalidTransitionRejection:
    """Tests for rejection of invalid lifecycle transitions."""

    def test_active_to_archived_rejected(self, tmp_dir: str):
        """Direct transition active -> archived is rejected."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "GOV", "name": "Governance", "lifecycle_state": "active"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        is_valid, reason = manager.validate_transition("GOV", DomainLifecycleState.ARCHIVED)

        assert is_valid is False
        assert "not permitted" in reason.lower() or "invalid" in reason.lower()

    def test_archived_to_active_rejected(self, tmp_dir: str):
        """Transition from archived (terminal) to active is rejected."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "OLD", "name": "Old", "lifecycle_state": "archived"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        is_valid, reason = manager.validate_transition("OLD", DomainLifecycleState.ACTIVE)

        assert is_valid is False
        assert "terminal" in reason.lower() or "no transitions" in reason.lower()

    def test_archived_to_deprecated_rejected(self, tmp_dir: str):
        """Transition from archived (terminal) to deprecated is rejected."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "OLD", "name": "Old", "lifecycle_state": "archived"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        is_valid, reason = manager.validate_transition("OLD", DomainLifecycleState.DEPRECATED)

        assert is_valid is False

    def test_active_to_active_rejected(self, tmp_dir: str):
        """Self-transition active -> active is rejected (not in valid set)."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "GOV", "name": "Governance", "lifecycle_state": "active"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        is_valid, reason = manager.validate_transition("GOV", DomainLifecycleState.ACTIVE)

        assert is_valid is False

    def test_valid_transition_active_to_deprecated(self, tmp_dir: str):
        """Valid transition active -> deprecated is accepted."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "GOV", "name": "Governance", "lifecycle_state": "active"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        is_valid, reason = manager.validate_transition("GOV", DomainLifecycleState.DEPRECATED)

        assert is_valid is True
        assert reason == ""

    def test_valid_transition_deprecated_to_active(self, tmp_dir: str):
        """Valid transition deprecated -> active (reactivation) is accepted."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "OLD", "name": "Old", "lifecycle_state": "deprecated"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        is_valid, reason = manager.validate_transition("OLD", DomainLifecycleState.ACTIVE)

        assert is_valid is True
        assert reason == ""

    def test_valid_transition_deprecated_to_archived(self, tmp_dir: str):
        """Valid transition deprecated -> archived is accepted."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "OLD", "name": "Old", "lifecycle_state": "deprecated"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        is_valid, reason = manager.validate_transition("OLD", DomainLifecycleState.ARCHIVED)

        assert is_valid is True
        assert reason == ""


# ---------------------------------------------------------------------------
# Test: Deprecation cannot_own Check
# ---------------------------------------------------------------------------


class TestDeprecationCannotOwnCheck:
    """Tests for cannot_own constraint enforcement during deprecation."""

    def test_deprecation_rejected_when_target_cannot_own_artifact_type(self, tmp_dir: str):
        """Deprecation is rejected if target domain cannot own artifact types."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "SOURCE", "name": "Source Domain", "lifecycle_state": "active"},
            {"domain_id": "TARGET", "name": "Target Domain", "lifecycle_state": "active", "cannot_own": ["ENGINE"]},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [
            {"artifact_id": "engine_1", "artifact_type": "ENGINE", "primary_domain": "SOURCE"},
        ])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        request = DeprecationRequest(
            domain_id="SOURCE",
            reassignment_target="TARGET",
            reason="Consolidation",
            requested_by="test_user",
            timestamp="2026-06-01T14:00:00Z",
        )

        success, result = manager.request_deprecation(request)

        assert success is False
        assert isinstance(result, str)
        assert "ENGINE" in result
        assert "cannot own" in result.lower() or "cannot be reassigned" in result.lower()

    def test_deprecation_accepted_when_target_can_own_all_types(self, tmp_dir: str):
        """Deprecation succeeds if target domain can own all artifact types."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "SOURCE", "name": "Source Domain", "lifecycle_state": "active"},
            {"domain_id": "TARGET", "name": "Target Domain", "lifecycle_state": "active", "cannot_own": []},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [
            {"artifact_id": "ssot_1", "artifact_type": "SSOT", "primary_domain": "SOURCE"},
            {"artifact_id": "engine_1", "artifact_type": "ENGINE", "primary_domain": "SOURCE"},
        ])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        request = DeprecationRequest(
            domain_id="SOURCE",
            reassignment_target="TARGET",
            reason="Consolidation",
            requested_by="test_user",
            timestamp="2026-06-01T14:00:00Z",
        )

        success, result = manager.request_deprecation(request)

        assert success is True
        assert isinstance(result, ReassignmentPlan)
        assert result.is_valid is True
        assert len(result.entries) == 2

    def test_deprecation_rejected_for_nonexistent_target(self, tmp_dir: str):
        """Deprecation is rejected if reassignment_target domain does not exist."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "SOURCE", "name": "Source Domain", "lifecycle_state": "active"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        request = DeprecationRequest(
            domain_id="SOURCE",
            reassignment_target="NONEXISTENT",
            reason="Consolidation",
            requested_by="test_user",
            timestamp="2026-06-01T14:00:00Z",
        )

        success, result = manager.request_deprecation(request)

        assert success is False
        assert isinstance(result, str)
        assert "not found" in result.lower()


# ---------------------------------------------------------------------------
# Test: Reassignment Plan Generation
# ---------------------------------------------------------------------------


class TestReassignmentPlanGeneration:
    """Tests for reassignment plan generation during deprecation."""

    def test_plan_contains_all_affected_artifacts(self, tmp_dir: str):
        """Reassignment plan includes all artifacts owned by deprecated domain."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "SOURCE", "name": "Source", "lifecycle_state": "active"},
            {"domain_id": "TARGET", "name": "Target", "lifecycle_state": "active"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [
            {"artifact_id": "art_1", "artifact_type": "SSOT", "primary_domain": "SOURCE"},
            {"artifact_id": "art_2", "artifact_type": "ENGINE", "primary_domain": "SOURCE"},
            {"artifact_id": "art_3", "artifact_type": "SSOT", "primary_domain": "OTHER"},
        ])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        request = DeprecationRequest(
            domain_id="SOURCE",
            reassignment_target="TARGET",
            reason="Consolidation",
            requested_by="test_user",
            timestamp="2026-06-01T14:00:00Z",
        )

        success, plan = manager.request_deprecation(request)

        assert success is True
        assert isinstance(plan, ReassignmentPlan)
        assert len(plan.entries) == 2  # Only SOURCE artifacts, not OTHER
        artifact_ids = {e.artifact_id for e in plan.entries}
        assert artifact_ids == {"art_1", "art_2"}

    def test_plan_entries_have_correct_domains(self, tmp_dir: str):
        """Each plan entry has correct previous_domain and new_domain."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "SOURCE", "name": "Source", "lifecycle_state": "active"},
            {"domain_id": "TARGET", "name": "Target", "lifecycle_state": "active"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [
            {"artifact_id": "art_1", "artifact_type": "SSOT", "primary_domain": "SOURCE"},
        ])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        request = DeprecationRequest(
            domain_id="SOURCE",
            reassignment_target="TARGET",
            reason="Consolidation",
            requested_by="test_user",
            timestamp="2026-06-01T14:00:00Z",
        )

        success, plan = manager.request_deprecation(request)

        assert success is True
        assert isinstance(plan, ReassignmentPlan)
        entry = plan.entries[0]
        assert entry.previous_domain == "SOURCE"
        assert entry.new_domain == "TARGET"
        assert entry.artifact_id == "art_1"

    def test_plan_with_no_artifacts_is_valid(self, tmp_dir: str):
        """Deprecation with no owned artifacts produces a valid empty plan."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "EMPTY", "name": "Empty Domain", "lifecycle_state": "active"},
            {"domain_id": "TARGET", "name": "Target", "lifecycle_state": "active"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        request = DeprecationRequest(
            domain_id="EMPTY",
            reassignment_target="TARGET",
            reason="No longer needed",
            requested_by="test_user",
            timestamp="2026-06-01T14:00:00Z",
        )

        success, plan = manager.request_deprecation(request)

        assert success is True
        assert isinstance(plan, ReassignmentPlan)
        assert plan.is_valid is True
        assert plan.entries == []
        assert plan.blocked_types == []


# ---------------------------------------------------------------------------
# Test: Reassignment Execution
# ---------------------------------------------------------------------------


class TestReassignmentExecution:
    """Tests for reassignment plan execution and ledger recording."""

    def test_execute_reassignment_records_to_ledger(
        self, tmp_dir: str, ledger: MutationAuditLedger, test_actor: ActorIdentity
    ):
        """Executing a reassignment plan records entries to the ledger."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "SOURCE", "name": "Source", "lifecycle_state": "active"},
            {"domain_id": "TARGET", "name": "Target", "lifecycle_state": "active"},
        ])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path, ledger=ledger)

        plan = ReassignmentPlan(
            deprecated_domain="SOURCE",
            target_domain="TARGET",
            entries=[
                ReassignmentPlanEntry(
                    artifact_id="art_1",
                    artifact_type="SSOT",
                    previous_domain="SOURCE",
                    new_domain="TARGET",
                ),
            ],
            blocked_types=[],
            is_valid=True,
            generated_at="2026-06-01T14:00:00Z",
        )

        result = manager.execute_reassignment(plan, test_actor)

        assert result is True
        entries = ledger.query_by_event_type("domain_lifecycle_transition")
        assert len(entries) >= 1
        assert entries[0].details["artifact_id"] == "art_1"
        assert entries[0].details["previous_domain"] == "SOURCE"
        assert entries[0].details["new_domain"] == "TARGET"

    def test_execute_reassignment_without_ledger_returns_false(
        self, tmp_dir: str, test_actor: ActorIdentity
    ):
        """Executing reassignment without a ledger returns False (fail_soft)."""
        domain_path = _write_domain_registry(tmp_dir, [])
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path, ledger=None)

        plan = ReassignmentPlan(
            deprecated_domain="SOURCE",
            target_domain="TARGET",
            entries=[
                ReassignmentPlanEntry(
                    artifact_id="art_1",
                    artifact_type="SSOT",
                    previous_domain="SOURCE",
                    new_domain="TARGET",
                ),
            ],
            blocked_types=[],
            is_valid=True,
            generated_at="2026-06-01T14:00:00Z",
        )

        result = manager.execute_reassignment(plan, test_actor)
        assert result is False


# ---------------------------------------------------------------------------
# Test: Missing Registry Files (fail_soft)
# ---------------------------------------------------------------------------


class TestMissingRegistryFiles:
    """Tests for graceful degradation when registry files are missing."""

    def test_missing_domain_registry_defaults_to_empty(self, tmp_dir: str):
        """Missing domain registry file results in empty domain list."""
        domain_path = os.path.join(tmp_dir, "nonexistent_domain_registry.yaml")
        artifact_path = _write_artifact_registry(tmp_dir, [])

        manager = DomainLifecycleManager(domain_path, artifact_path)
        # Should not raise — fail_soft
        state = manager.get_domain_state("ANY")
        assert state == DomainLifecycleState.ACTIVE

    def test_missing_artifact_registry_defaults_to_empty(self, tmp_dir: str):
        """Missing artifact registry file results in empty artifact list."""
        domain_path = _write_domain_registry(tmp_dir, [
            {"domain_id": "GOV", "name": "Governance", "lifecycle_state": "active"},
            {"domain_id": "TARGET", "name": "Target", "lifecycle_state": "active"},
        ])
        artifact_path = os.path.join(tmp_dir, "nonexistent_artifact_registry.yaml")

        manager = DomainLifecycleManager(domain_path, artifact_path)

        request = DeprecationRequest(
            domain_id="GOV",
            reassignment_target="TARGET",
            reason="Test",
            requested_by="test_user",
            timestamp="2026-06-01T14:00:00Z",
        )

        success, plan = manager.request_deprecation(request)
        assert success is True
        assert isinstance(plan, ReassignmentPlan)
        assert plan.entries == []
