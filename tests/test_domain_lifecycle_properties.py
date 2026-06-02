"""Property test: Domain Lifecycle Transition Validation.

**Property 8: Domain Lifecycle Transition Validation**
**Validates: Requirements 9.2, 9.3, 9.4**

Tests that for any domain in any lifecycle state, attempting a transition to a
target state succeeds if and only if the (from_state, to_state) pair is in the
set of valid transitions: {(active, deprecated), (deprecated, archived),
(deprecated, active)}. All other transitions are rejected.

Additional invariants:
- Deprecated domains cannot own active responsibilities (cannot_own check)
- Reassignment plans preserve required ownership handoff semantics
- Reassignment execution records ledger entries
- Unknown domains default to ACTIVE only where implementation explicitly defines
  that behavior
"""

from __future__ import annotations

import os
import tempfile
import uuid
from datetime import datetime, timezone

import yaml
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from governance.domain_lifecycle import (
    DomainLifecycleManager,
    DomainLifecycleState,
    DeprecationRequest,
    ReassignmentPlan,
    ReassignmentPlanEntry,
    VALID_DOMAIN_TRANSITIONS,
)
from governance.mutation_audit_ledger import MutationAuditLedger, LedgerEntry
from governance.actor_identity import ActorIdentity, ActorType


# --- Strategies ---

lifecycle_state_strategy = st.sampled_from(list(DomainLifecycleState))

domain_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=1,
    max_size=20,
)

# All possible (from_state, to_state) pairs
all_transition_pairs = st.tuples(lifecycle_state_strategy, lifecycle_state_strategy)

# Valid transition set as defined in the design
VALID_TRANSITION_SET: set[tuple[DomainLifecycleState, DomainLifecycleState]] = {
    (DomainLifecycleState.ACTIVE, DomainLifecycleState.DEPRECATED),
    (DomainLifecycleState.DEPRECATED, DomainLifecycleState.ARCHIVED),
    (DomainLifecycleState.DEPRECATED, DomainLifecycleState.ACTIVE),
}

# Artifact types used in the project
artifact_type_strategy = st.sampled_from([
    "SSOT", "ENGINE", "CONFIG", "STEERING", "REPORT_OUT",
    "DATA_OUT", "DATA_IN", "SNAPSHOT", "DASHBOARD", "RUNTIME", "CALIBRATION",
])


# --- Helpers ---

def _create_temp_domain_registry(domains: list[dict]) -> str:
    """Create a temporary domain registry YAML file."""
    fd, path = tempfile.mkstemp(suffix=".yaml")
    with os.fdopen(fd, "w") as f:
        yaml.dump({"domains": domains}, f, default_flow_style=False)
    return path


def _create_temp_artifact_registry(artifacts: list[dict]) -> str:
    """Create a temporary artifact registry YAML file."""
    fd, path = tempfile.mkstemp(suffix=".yaml")
    with os.fdopen(fd, "w") as f:
        yaml.dump({"artifacts": artifacts}, f, default_flow_style=False)
    return path


def _create_temp_ledger() -> tuple[MutationAuditLedger, str]:
    """Create a temporary ledger for testing."""
    fd, path = tempfile.mkstemp(suffix=".yaml")
    os.close(fd)
    os.unlink(path)  # Let the ledger create it fresh
    ledger = MutationAuditLedger(path)
    return ledger, path


def _make_actor() -> ActorIdentity:
    """Create a test actor identity."""
    return ActorIdentity(
        actor_type=ActorType.USER,
        actor_id="test_user",
        context={},
        is_fallback=False,
    )


def _cleanup_files(*paths: str) -> None:
    """Remove temporary files."""
    for path in paths:
        try:
            os.unlink(path)
        except OSError:
            pass


# --- Property 8: Domain Lifecycle Transition Validation ---


@given(
    from_state=lifecycle_state_strategy,
    to_state=lifecycle_state_strategy,
)
@settings(max_examples=200)
def test_property8_valid_transitions_accepted_invalid_rejected(
    from_state: DomainLifecycleState,
    to_state: DomainLifecycleState,
) -> None:
    """For any (from_state, to_state) pair, the transition is accepted iff it
    is in the valid transition set.

    Valid transitions: {(active, deprecated), (deprecated, archived), (deprecated, active)}
    All other transitions are rejected.
    """
    domain_id = "TEST_DOMAIN"

    # Create a domain registry with the domain in from_state
    domains = [
        {
            "domain_id": domain_id,
            "name": "Test Domain",
            "lifecycle_state": str(from_state),
            "allowed_artifact_types": ["SSOT", "ENGINE"],
            "cannot_own": [],
        }
    ]

    domain_reg_path = _create_temp_domain_registry(domains)
    artifact_reg_path = _create_temp_artifact_registry([])

    try:
        manager = DomainLifecycleManager(
            domain_registry_path=domain_reg_path,
            artifact_registry_path=artifact_reg_path,
            ledger=None,
        )

        is_valid, reason = manager.validate_transition(domain_id, to_state)

        if (from_state, to_state) in VALID_TRANSITION_SET:
            assert is_valid, (
                f"Expected valid transition ({from_state} -> {to_state}) "
                f"to be accepted, but got rejection: {reason}"
            )
            assert reason == ""
        else:
            assert not is_valid, (
                f"Expected invalid transition ({from_state} -> {to_state}) "
                f"to be rejected, but it was accepted"
            )
            assert reason != "", (
                f"Rejected transition ({from_state} -> {to_state}) "
                f"should have a non-empty rejection reason"
            )
    finally:
        _cleanup_files(domain_reg_path, artifact_reg_path)


@given(
    from_state=lifecycle_state_strategy,
    to_state=lifecycle_state_strategy,
)
@settings(max_examples=200)
def test_property8_transition_completeness(
    from_state: DomainLifecycleState,
    to_state: DomainLifecycleState,
) -> None:
    """Verify that VALID_DOMAIN_TRANSITIONS dict is consistent with the
    expected valid transition set — no extra transitions exist and none are missing."""
    valid_targets = VALID_DOMAIN_TRANSITIONS.get(from_state, [])

    if (from_state, to_state) in VALID_TRANSITION_SET:
        assert to_state in valid_targets, (
            f"VALID_DOMAIN_TRANSITIONS missing expected transition: "
            f"({from_state} -> {to_state})"
        )
    else:
        assert to_state not in valid_targets, (
            f"VALID_DOMAIN_TRANSITIONS contains unexpected transition: "
            f"({from_state} -> {to_state})"
        )



# --- Additional Invariant: cannot_own check for deprecated domains ---


@given(
    blocked_types=st.lists(
        artifact_type_strategy,
        min_size=1,
        max_size=4,
        unique=True,
    ),
    owned_types=st.lists(
        artifact_type_strategy,
        min_size=1,
        max_size=5,
        unique=True,
    ),
)
@settings(max_examples=200)
def test_deprecated_domain_cannot_own_blocked_types(
    blocked_types: list[str],
    owned_types: list[str],
) -> None:
    """Verify that deprecation is rejected when the reassignment target domain
    has cannot_own constraints that conflict with artifacts owned by the
    deprecated domain.

    If any artifact type owned by the deprecated domain is in the target's
    cannot_own list, the deprecation request must be rejected.
    """
    source_domain = "SOURCE"
    target_domain = "TARGET"

    # Determine if there's a conflict
    conflicting_types = [t for t in owned_types if t in blocked_types]
    has_conflict = len(conflicting_types) > 0

    # Create domains
    domains = [
        {
            "domain_id": source_domain,
            "name": "Source Domain",
            "lifecycle_state": "active",
            "allowed_artifact_types": owned_types,
            "cannot_own": [],
        },
        {
            "domain_id": target_domain,
            "name": "Target Domain",
            "lifecycle_state": "active",
            "allowed_artifact_types": ["SSOT", "ENGINE", "CONFIG", "DATA_OUT", "REPORT_OUT"],
            "cannot_own": blocked_types,
        },
    ]

    # Create artifacts owned by source domain with the owned_types
    artifacts = [
        {
            "artifact_id": f"artifact_{i}",
            "artifact_type": atype,
            "primary_domain": source_domain,
            "file_path": f"test/artifact_{i}.py",
        }
        for i, atype in enumerate(owned_types)
    ]

    domain_reg_path = _create_temp_domain_registry(domains)
    artifact_reg_path = _create_temp_artifact_registry(artifacts)

    try:
        manager = DomainLifecycleManager(
            domain_registry_path=domain_reg_path,
            artifact_registry_path=artifact_reg_path,
            ledger=None,
        )

        request = DeprecationRequest(
            domain_id=source_domain,
            reassignment_target=target_domain,
            reason="Test deprecation",
            requested_by="test_user",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        success, result = manager.request_deprecation(request)

        if has_conflict:
            assert not success, (
                f"Deprecation should be rejected when target cannot own "
                f"types {conflicting_types}, but it was accepted"
            )
            assert isinstance(result, str), (
                "Rejected deprecation should return an error string"
            )
        else:
            assert success, (
                f"Deprecation should be accepted when no cannot_own conflicts "
                f"exist, but got rejection: {result}"
            )
            assert isinstance(result, ReassignmentPlan), (
                "Accepted deprecation should return a ReassignmentPlan"
            )
            assert result.is_valid
            assert result.blocked_types == []
    finally:
        _cleanup_files(domain_reg_path, artifact_reg_path)


# --- Additional Invariant: Reassignment plan preserves ownership handoff ---


@given(
    num_artifacts=st.integers(min_value=1, max_value=10),
    artifact_type=artifact_type_strategy,
)
@settings(max_examples=200)
def test_reassignment_plan_preserves_ownership_handoff(
    num_artifacts: int,
    artifact_type: str,
) -> None:
    """Verify that reassignment plans correctly map all artifacts from the
    deprecated domain to the target domain, preserving the handoff semantics.

    Each entry in the plan must have:
    - previous_domain == deprecated domain
    - new_domain == target domain
    - artifact_id matching an owned artifact
    """
    source_domain = "DEPRECATED_SRC"
    target_domain = "ACTIVE_TGT"

    # Ensure target can own the artifact type (no cannot_own conflict)
    domains = [
        {
            "domain_id": source_domain,
            "name": "Source",
            "lifecycle_state": "active",
            "allowed_artifact_types": [artifact_type],
            "cannot_own": [],
        },
        {
            "domain_id": target_domain,
            "name": "Target",
            "lifecycle_state": "active",
            "allowed_artifact_types": [artifact_type],
            "cannot_own": [],  # No restrictions
        },
    ]

    artifacts = [
        {
            "artifact_id": f"art_{i}",
            "artifact_type": artifact_type,
            "primary_domain": source_domain,
            "file_path": f"src/art_{i}.py",
        }
        for i in range(num_artifacts)
    ]

    domain_reg_path = _create_temp_domain_registry(domains)
    artifact_reg_path = _create_temp_artifact_registry(artifacts)

    try:
        manager = DomainLifecycleManager(
            domain_registry_path=domain_reg_path,
            artifact_registry_path=artifact_reg_path,
            ledger=None,
        )

        request = DeprecationRequest(
            domain_id=source_domain,
            reassignment_target=target_domain,
            reason="Consolidation",
            requested_by="test_user",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        success, result = manager.request_deprecation(request)

        assert success, f"Deprecation should succeed without conflicts: {result}"
        assert isinstance(result, ReassignmentPlan)
        assert result.deprecated_domain == source_domain
        assert result.target_domain == target_domain
        assert len(result.entries) == num_artifacts

        # Verify each entry preserves handoff semantics
        for entry in result.entries:
            assert entry.previous_domain == source_domain, (
                f"Entry previous_domain should be '{source_domain}', "
                f"got '{entry.previous_domain}'"
            )
            assert entry.new_domain == target_domain, (
                f"Entry new_domain should be '{target_domain}', "
                f"got '{entry.new_domain}'"
            )
            assert entry.artifact_type == artifact_type
    finally:
        _cleanup_files(domain_reg_path, artifact_reg_path)


# --- Additional Invariant: Reassignment execution records ledger entries ---


@given(
    num_artifacts=st.integers(min_value=1, max_value=5),
)
@settings(max_examples=200, deadline=None)
def test_reassignment_execution_records_ledger_entries(
    num_artifacts: int,
) -> None:
    """Verify that executing a reassignment plan records one ledger entry
    per artifact reassigned, with event_type 'domain_lifecycle_transition'."""
    source_domain = "OLD_DOMAIN"
    target_domain = "NEW_DOMAIN"

    # Build a reassignment plan directly
    entries = [
        ReassignmentPlanEntry(
            artifact_id=f"artifact_{i}",
            artifact_type="ENGINE",
            previous_domain=source_domain,
            new_domain=target_domain,
        )
        for i in range(num_artifacts)
    ]

    plan = ReassignmentPlan(
        deprecated_domain=source_domain,
        target_domain=target_domain,
        entries=entries,
        blocked_types=[],
        is_valid=True,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    # Create manager with a real ledger
    domain_reg_path = _create_temp_domain_registry([
        {"domain_id": source_domain, "name": "Old", "lifecycle_state": "deprecated",
         "allowed_artifact_types": ["ENGINE"], "cannot_own": []},
        {"domain_id": target_domain, "name": "New", "lifecycle_state": "active",
         "allowed_artifact_types": ["ENGINE"], "cannot_own": []},
    ])
    artifact_reg_path = _create_temp_artifact_registry([])
    ledger, ledger_path = _create_temp_ledger()

    try:
        manager = DomainLifecycleManager(
            domain_registry_path=domain_reg_path,
            artifact_registry_path=artifact_reg_path,
            ledger=ledger,
        )

        actor = _make_actor()
        result = manager.execute_reassignment(plan, actor)

        assert result is True, "Reassignment execution should succeed"

        # Query ledger for domain_lifecycle_transition entries
        ledger_entries = ledger.query_by_event_type("domain_lifecycle_transition")

        assert len(ledger_entries) == num_artifacts, (
            f"Expected {num_artifacts} ledger entries, got {len(ledger_entries)}"
        )

        # Verify each ledger entry has correct structure
        for le in ledger_entries:
            assert le.event_type == "domain_lifecycle_transition"
            assert le.severity == "INFO"
            details = le.details
            assert details["action"] == "artifact_reassignment"
            assert details["previous_domain"] == source_domain
            assert details["new_domain"] == target_domain
            assert details["deprecated_domain"] == source_domain
    finally:
        _cleanup_files(domain_reg_path, artifact_reg_path, ledger_path)


# --- Additional Invariant: Unknown domains default to ACTIVE ---


@given(
    unknown_domain_id=domain_id_strategy,
)
@settings(max_examples=200)
def test_unknown_domains_default_to_active(
    unknown_domain_id: str,
) -> None:
    """Verify that domains not found in the registry default to ACTIVE state.

    The implementation explicitly defines this behavior per Req 9.5:
    'defaulting to active for all existing domains'.
    """
    # Create an empty domain registry (no domains registered)
    domain_reg_path = _create_temp_domain_registry([])
    artifact_reg_path = _create_temp_artifact_registry([])

    try:
        manager = DomainLifecycleManager(
            domain_registry_path=domain_reg_path,
            artifact_registry_path=artifact_reg_path,
            ledger=None,
        )

        state = manager.get_domain_state(unknown_domain_id)

        assert state == DomainLifecycleState.ACTIVE, (
            f"Unknown domain '{unknown_domain_id}' should default to ACTIVE, "
            f"got '{state}'"
        )
    finally:
        _cleanup_files(domain_reg_path, artifact_reg_path)
