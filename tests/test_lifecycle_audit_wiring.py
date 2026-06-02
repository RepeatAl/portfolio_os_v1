"""Tests for lifecycle transition audit logging wiring (Task 9.2).

Verifies:
- enforce_transition() emits a GOVERNANCE_EVENT ledger entry when ledger is connected
- Ledger entry contains correct actor, policy version, and provenance
- enforce_transition() works without a ledger (backward compatible)
- Severity mapping: INFO for pass, WARNING for warn, CRITICAL for block

Validates: Requirements 11.1, 11.2, 11.3, 11.4
"""

import os
import tempfile
import uuid

import yaml
import pytest

from governance.lifecycle_enforcer import LifecycleEnforcer
from governance.mutation_audit_ledger import MutationAuditLedger, LedgerEntry
from governance.actor_identity import ActorIdentity, ActorType
from governance.policy_versioner import PolicyVersioner
from governance.state_provenance_tagger import StateProvenanceTagger, GovernanceProvenance


# --- Fixtures ---


@pytest.fixture
def state_machine_yaml(tmp_path):
    """Create a minimal lifecycle state machine YAML for testing."""
    sm_path = tmp_path / "lifecycle_state_machine.yaml"
    sm_data = {
        "artifact_types": {
            "SSOT": {
                "states": ["draft", "review", "canonical", "deprecated"],
                "initial_state": "draft",
                "transitions": [
                    {"from": "draft", "to": "review"},
                    {"from": "review", "to": "canonical"},
                    {"from": "review", "to": "draft"},
                    {"from": "canonical", "to": "deprecated"},
                ],
                "read_only_states": ["deprecated"],
                "regenerable_states": [],
            },
            "REPORT_OUT": {
                "states": ["generating", "active", "stale", "archived"],
                "initial_state": "generating",
                "transitions": [
                    {"from": "generating", "to": "active"},
                    {"from": "active", "to": "stale"},
                    {"from": "stale", "to": "archived"},
                    {"from": "active", "to": "generating"},
                ],
                "read_only_states": ["archived"],
                "regenerable_states": ["stale", "active"],
            },
        }
    }
    with open(sm_path, "w") as f:
        yaml.dump(sm_data, f)
    return str(sm_path)


@pytest.fixture
def ledger(tmp_path):
    """Create a MutationAuditLedger in a temp directory."""
    ledger_path = tmp_path / "mutation_audit_ledger.yaml"
    return MutationAuditLedger(str(ledger_path))


@pytest.fixture
def policy_versioner(tmp_path):
    """Create a PolicyVersioner with a minimal governance file set."""
    config_dir = tmp_path / ".domainization"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text("governance_enforcement:\n  mode: observability\n")
    return PolicyVersioner(str(tmp_path))


@pytest.fixture
def provenance_tagger():
    """Create a StateProvenanceTagger with authoritative provenance."""
    tagger = StateProvenanceTagger()
    tagger.tag(
        source="config.yaml",
        is_validated=True,
        is_cached=False,
        is_cold_start=False,
    )
    return tagger


@pytest.fixture
def test_actor():
    """Create a test actor identity."""
    return ActorIdentity(
        actor_type=ActorType.ENGINE,
        actor_id="test_engine",
        context={"run_id": "test-run-001"},
        is_fallback=False,
    )


# --- Tests ---


class TestEnforceTransitionEmitsLedgerEntry:
    """Verify enforce_transition() emits a ledger entry when ledger is connected."""

    def test_valid_transition_emits_governance_event(
        self, state_machine_yaml, ledger, policy_versioner, provenance_tagger, test_actor
    ):
        """A valid transition emits a GOVERNANCE_EVENT with INFO severity."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
            ledger=ledger,
            policy_versioner=policy_versioner,
            provenance_tagger=provenance_tagger,
        )

        result = enforcer.enforce_transition(
            artifact_id="spec_governance",
            artifact_type="SSOT",
            from_state="draft",
            to_state="review",
            actor=test_actor,
        )

        assert result.status == "pass"
        assert result.enforcement_action == "info"

        # Verify ledger entry was emitted
        entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
        assert len(entries) == 1

        entry = entries[0]
        assert entry.event_type == "GOVERNANCE_EVENT"
        assert entry.severity == "INFO"
        assert entry.details["artifact_id"] == "spec_governance"
        assert entry.details["artifact_type"] == "SSOT"
        assert entry.details["from_state"] == "draft"
        assert entry.details["to_state"] == "review"
        assert entry.details["validity"] == "pass"
        assert entry.details["enforcement_action"] == "info"

    def test_invalid_transition_soft_mode_emits_critical(
        self, state_machine_yaml, ledger, policy_versioner, provenance_tagger, test_actor
    ):
        """An invalid transition in soft mode emits CRITICAL severity."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
            ledger=ledger,
            policy_versioner=policy_versioner,
            provenance_tagger=provenance_tagger,
        )

        result = enforcer.enforce_transition(
            artifact_id="spec_governance",
            artifact_type="SSOT",
            from_state="draft",
            to_state="deprecated",
            actor=test_actor,
        )

        assert result.status == "fail"
        assert result.enforcement_action == "block"

        entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
        assert len(entries) == 1

        entry = entries[0]
        assert entry.severity == "CRITICAL"
        assert entry.details["validity"] == "fail"
        assert entry.details["enforcement_action"] == "block"

    def test_invalid_transition_observability_emits_warning(
        self, state_machine_yaml, ledger, policy_versioner, provenance_tagger, test_actor
    ):
        """An invalid transition in observability mode emits WARNING severity."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="observability",
            ledger=ledger,
            policy_versioner=policy_versioner,
            provenance_tagger=provenance_tagger,
        )

        result = enforcer.enforce_transition(
            artifact_id="spec_governance",
            artifact_type="SSOT",
            from_state="draft",
            to_state="deprecated",
            actor=test_actor,
        )

        assert result.status == "pass"
        assert result.enforcement_action == "warn"

        entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
        assert len(entries) == 1

        entry = entries[0]
        assert entry.severity == "WARNING"
        assert entry.details["validity"] == "pass"
        assert entry.details["enforcement_action"] == "warn"

    def test_multiple_transitions_emit_multiple_entries(
        self, state_machine_yaml, ledger, policy_versioner, provenance_tagger, test_actor
    ):
        """Each enforce_transition() call emits a separate ledger entry."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
            ledger=ledger,
            policy_versioner=policy_versioner,
            provenance_tagger=provenance_tagger,
        )

        enforcer.enforce_transition(
            "art1", "SSOT", "draft", "review", actor=test_actor
        )
        enforcer.enforce_transition(
            "art2", "SSOT", "review", "canonical", actor=test_actor
        )
        enforcer.enforce_transition(
            "art3", "SSOT", "draft", "deprecated", actor=test_actor
        )

        entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
        assert len(entries) == 3


class TestLedgerEntryContainsCorrectMetadata:
    """Verify ledger entries contain correct actor, policy version, and provenance."""

    def test_actor_identity_in_ledger_entry(
        self, state_machine_yaml, ledger, policy_versioner, provenance_tagger, test_actor
    ):
        """Ledger entry contains the actor identity as a dict."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
            ledger=ledger,
            policy_versioner=policy_versioner,
            provenance_tagger=provenance_tagger,
        )

        enforcer.enforce_transition(
            "spec_governance", "SSOT", "draft", "review", actor=test_actor
        )

        entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
        entry = entries[0]

        assert entry.actor["actor_type"] == "ENGINE"
        assert entry.actor["actor_id"] == "test_engine"
        assert entry.actor["context"] == {"run_id": "test-run-001"}
        assert entry.actor["is_fallback"] is False

    def test_policy_version_in_ledger_entry(
        self, state_machine_yaml, ledger, policy_versioner, provenance_tagger, test_actor
    ):
        """Ledger entry contains the governance policy version hash."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
            ledger=ledger,
            policy_versioner=policy_versioner,
            provenance_tagger=provenance_tagger,
        )

        enforcer.enforce_transition(
            "spec_governance", "SSOT", "draft", "review", actor=test_actor
        )

        entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
        entry = entries[0]

        assert entry.governance_policy_version.startswith("sha256:")
        expected_version = policy_versioner.get_current_version()
        assert entry.governance_policy_version == expected_version

    def test_provenance_in_ledger_entry(
        self, state_machine_yaml, ledger, policy_versioner, provenance_tagger, test_actor
    ):
        """Ledger entry details contain governance state provenance."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
            ledger=ledger,
            policy_versioner=policy_versioner,
            provenance_tagger=provenance_tagger,
        )

        enforcer.enforce_transition(
            "spec_governance", "SSOT", "draft", "review", actor=test_actor
        )

        entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
        entry = entries[0]

        assert entry.details["governance_state_provenance"] == "authoritative"

    def test_entry_has_valid_uuid_and_timestamp(
        self, state_machine_yaml, ledger, policy_versioner, provenance_tagger, test_actor
    ):
        """Ledger entry has a valid UUID entry_id and ISO 8601 timestamp."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
            ledger=ledger,
            policy_versioner=policy_versioner,
            provenance_tagger=provenance_tagger,
        )

        enforcer.enforce_transition(
            "spec_governance", "SSOT", "draft", "review", actor=test_actor
        )

        entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
        entry = entries[0]

        # Validate UUID format
        uuid.UUID(entry.entry_id)  # Raises ValueError if invalid

        # Validate ISO 8601 timestamp (contains 'T' and timezone info)
        assert "T" in entry.timestamp


class TestBackwardCompatibility:
    """Verify enforce_transition() works without a ledger (backward compatible)."""

    def test_no_ledger_valid_transition(self, state_machine_yaml):
        """enforce_transition() works without ledger for valid transitions."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
        )

        result = enforcer.enforce_transition(
            artifact_id="spec_governance",
            artifact_type="SSOT",
            from_state="draft",
            to_state="review",
        )

        assert result.status == "pass"
        assert result.enforcement_action == "info"

    def test_no_ledger_invalid_transition(self, state_machine_yaml):
        """enforce_transition() works without ledger for invalid transitions."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="hard",
        )

        result = enforcer.enforce_transition(
            artifact_id="spec_governance",
            artifact_type="SSOT",
            from_state="draft",
            to_state="deprecated",
        )

        assert result.status == "fail"
        assert result.enforcement_action == "block"

    def test_no_ledger_no_policy_versioner_no_tagger(self, state_machine_yaml):
        """enforce_transition() works with all optional params as None."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="observability",
            ledger=None,
            policy_versioner=None,
            provenance_tagger=None,
        )

        result = enforcer.enforce_transition(
            artifact_id="report_daily",
            artifact_type="REPORT_OUT",
            from_state="generating",
            to_state="active",
        )

        assert result.status == "pass"
        assert result.enforcement_action == "info"

    def test_unknown_artifact_type_without_ledger(self, state_machine_yaml):
        """enforce_transition() handles unknown artifact types without ledger."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
        )

        result = enforcer.enforce_transition(
            artifact_id="unknown_art",
            artifact_type="NONEXISTENT_TYPE",
            from_state="draft",
            to_state="review",
        )

        assert result.status == "fail"
        assert result.enforcement_action == "block"


class TestLedgerFailSoft:
    """Verify ledger failures don't break enforcement (fail-soft behavior)."""

    def test_ledger_append_failure_does_not_break_enforcement(
        self, state_machine_yaml, tmp_path, test_actor
    ):
        """If ledger.append() raises, enforce_transition() still returns result."""
        ledger_path = tmp_path / "readonly_ledger.yaml"
        ledger = MutationAuditLedger(str(ledger_path))

        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
            ledger=ledger,
        )

        # Make the ledger file read-only to trigger write failure
        os.chmod(str(ledger_path), 0o444)

        try:
            result = enforcer.enforce_transition(
                artifact_id="spec_governance",
                artifact_type="SSOT",
                from_state="draft",
                to_state="review",
                actor=test_actor,
            )

            # Enforcement still works despite ledger failure
            assert result.status == "pass"
            assert result.enforcement_action == "info"
        finally:
            # Restore permissions for cleanup
            os.chmod(str(ledger_path), 0o644)


class TestActorFromEnvironmentFallback:
    """Verify actor defaults to from_environment() when not provided."""

    def test_actor_defaults_to_environment(
        self, state_machine_yaml, ledger, policy_versioner, provenance_tagger
    ):
        """When no actor is passed, from_environment() is used."""
        enforcer = LifecycleEnforcer(
            state_machine_path=state_machine_yaml,
            enforcement_mode="soft",
            ledger=ledger,
            policy_versioner=policy_versioner,
            provenance_tagger=provenance_tagger,
        )

        enforcer.enforce_transition(
            artifact_id="spec_governance",
            artifact_type="SSOT",
            from_state="draft",
            to_state="review",
        )

        entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
        assert len(entries) == 1

        entry = entries[0]
        # Actor should be populated (from_environment resolves something)
        assert "actor_type" in entry.actor
        assert "actor_id" in entry.actor
