"""Property tests: Deployment Authority Model — Properties 4, 5, 6.

**Property 4: Authority Model Round-Trip**
**Property 5: Topology Constraint Enforcement**
**Property 6: Deploy Provenance Round-Trip**

**Validates: Requirements 4.3, 4.5, 5.1, 5.2, 5.3, 6.1, 6.5**

Tests the deployment authority model's serialization round-trips,
topology constraint enforcement (forbidden authority pairs), and
deploy provenance recording behavior.

CTO Decision (2026-05-31) — Forbidden Pair Resolution:
The final FORBIDDEN_AUTHORITY_PAIRS set is ADDITIVE and stricter.
The implementation keeps the original pair AND adds the design-spec pair.

Final forbidden-pair set (3 pairs):
  1. (mutate_governance, deploy) — original pair (design + implementation agree)
  2. (deploy, change_enforcement_mode) — design-spec pair (ADDED per CTO decision)
  3. (change_enforcement_mode, execute_override) — implementation pair (KEPT per CTO decision)

This is NOT a deviation — it is an explicit CTO decision to enforce all three
separation-of-concern boundaries simultaneously.
"""

import logging
from unittest.mock import MagicMock, patch

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from governance.deployment_authority import (
    Authority,
    AuthorityAssignment,
    AuthorityRole,
    DeploymentAuthorityModel,
    DeployProvenance,
    FORBIDDEN_AUTHORITY_PAIRS,
)


# =============================================================================
# Strategies
# =============================================================================

# All valid Authority values
all_authorities = list(Authority)
all_roles = list(AuthorityRole)

# Strategy for a frozenset of Authority values (non-empty)
authority_set_strategy = st.frozensets(
    st.sampled_from(all_authorities),
    min_size=1,
    max_size=6,
)

# Strategy for a single AuthorityAssignment
authority_assignment_strategy = st.builds(
    AuthorityAssignment,
    role=st.sampled_from(all_roles),
    authorities=authority_set_strategy,
)

# Strategy for DeployProvenance fields
deploy_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P")),
    min_size=1,
    max_size=64,
)
timestamp_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P")),
    min_size=1,
    max_size=40,
)
hash_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=1,
    max_size=64,
)
details_strategy = st.dictionaries(
    keys=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=20,
    ),
    values=st.text(min_size=0, max_size=50),
    max_size=5,
)


# =============================================================================
# Property 4: Authority Model Round-Trip
# Validates: Requirements 4.3, 4.5
# =============================================================================


@given(
    owner_authorities=authority_set_strategy,
    ci_authorities=authority_set_strategy,
    runtime_authorities=authority_set_strategy,
)
@settings(max_examples=200)
def test_property_4_authority_model_roundtrip(
    owner_authorities: frozenset,
    ci_authorities: frozenset,
    runtime_authorities: frozenset,
) -> None:
    """**Validates: Requirements 4.3, 4.5**

    For any valid authority configuration (3 roles, frozensets of Authority),
    serialize/deserialize produces an equivalent configuration.
    """
    assignments = [
        AuthorityAssignment(role=AuthorityRole.OWNER, authorities=owner_authorities),
        AuthorityAssignment(role=AuthorityRole.CI, authorities=ci_authorities),
        AuthorityAssignment(role=AuthorityRole.RUNTIME, authorities=runtime_authorities),
    ]

    for original in assignments:
        serialized = original.to_dict()
        deserialized = AuthorityAssignment.from_dict(serialized)

        assert deserialized.role == original.role
        assert deserialized.authorities == original.authorities


# =============================================================================
# Property 5: Topology Constraint Enforcement
# Validates: Requirements 5.1, 5.2, 5.3
#
# CTO Decision (2026-05-31): Final forbidden-pair set is ADDITIVE (3 pairs).
# All three pairs are tested explicitly below.
# =============================================================================


@given(data=st.data())
@settings(max_examples=200)
def test_property_5_topology_forbidden_pairs_rejected(data: st.DataObject) -> None:
    """**Validates: Requirements 5.1, 5.2, 5.3**

    Configurations where at least one role holds a forbidden authority pair
    MUST be rejected by topology validation.
    """
    # Pick a forbidden pair to inject
    forbidden_pair = data.draw(st.sampled_from(FORBIDDEN_AUTHORITY_PAIRS))
    auth_a, auth_b = forbidden_pair

    # Pick which role will hold the forbidden pair
    violating_role = data.draw(st.sampled_from(all_roles))

    # Generate additional authorities for the violating role (may include more)
    extra_authorities = data.draw(
        st.frozensets(st.sampled_from(all_authorities), max_size=4)
    )
    violating_authorities = frozenset({auth_a, auth_b}) | extra_authorities

    # Build a 3-role config with the violation injected
    assignments = []
    for role in all_roles:
        if role == violating_role:
            assignments.append(
                AuthorityAssignment(role=role, authorities=violating_authorities)
            )
        else:
            # Generate clean authorities for other roles
            other_auths = data.draw(
                st.frozensets(st.sampled_from(all_authorities), min_size=1, max_size=3)
            )
            assignments.append(
                AuthorityAssignment(role=role, authorities=other_auths)
            )

    # Create model and load assignments directly
    model = DeploymentAuthorityModel(model_path="/dev/null", ledger=None)
    model._assignments = assignments

    is_valid, violations = model.validate_topology()
    assert not is_valid, (
        f"Expected topology rejection for role {violating_role} holding "
        f"forbidden pair ({auth_a}, {auth_b}), but validation passed"
    )
    assert len(violations) > 0


@given(
    owner_authorities=authority_set_strategy,
    ci_authorities=authority_set_strategy,
    runtime_authorities=authority_set_strategy,
)
@settings(max_examples=200)
def test_property_5_topology_clean_configs_accepted(
    owner_authorities: frozenset,
    ci_authorities: frozenset,
    runtime_authorities: frozenset,
) -> None:
    """**Validates: Requirements 5.1, 5.2, 5.3**

    Configurations where NO role holds any forbidden authority pair
    MUST be accepted by topology validation.
    """
    # Filter out any configuration that contains a forbidden pair
    for auths in [owner_authorities, ci_authorities, runtime_authorities]:
        for auth_a, auth_b in FORBIDDEN_AUTHORITY_PAIRS:
            assume(not (auth_a in auths and auth_b in auths))

    assignments = [
        AuthorityAssignment(role=AuthorityRole.OWNER, authorities=owner_authorities),
        AuthorityAssignment(role=AuthorityRole.CI, authorities=ci_authorities),
        AuthorityAssignment(role=AuthorityRole.RUNTIME, authorities=runtime_authorities),
    ]

    model = DeploymentAuthorityModel(model_path="/dev/null", ledger=None)
    model._assignments = assignments

    is_valid, violations = model.validate_topology()
    assert is_valid, (
        f"Expected clean config to pass topology validation, "
        f"but got violations: {violations}"
    )
    assert violations == []


def test_property_5_explicit_forbidden_pair_1_mutate_governance_deploy() -> None:
    """**Validates: Requirements 5.1**

    Verify mutate_governance and deploy cannot be held by one role.
    Explicitly tests implemented forbidden pair 1.
    """
    for role in all_roles:
        assignment = AuthorityAssignment(
            role=role,
            authorities=frozenset({Authority.MUTATE_GOVERNANCE, Authority.DEPLOY}),
        )
        model = DeploymentAuthorityModel(model_path="/dev/null", ledger=None)
        model._assignments = [assignment]

        is_valid, violations = model.validate_topology()
        assert not is_valid, (
            f"Role {role} holding (mutate_governance, deploy) should be rejected"
        )


def test_property_5_explicit_forbidden_pair_2_deploy_change_enforcement() -> None:
    """**Validates: Requirements 5.2**

    Verify deploy and change_enforcement_mode cannot be held by one role.
    CTO Decision (2026-05-31): This pair from the design spec is now enforced.
    """
    for role in all_roles:
        assignment = AuthorityAssignment(
            role=role,
            authorities=frozenset(
                {Authority.DEPLOY, Authority.CHANGE_ENFORCEMENT_MODE}
            ),
        )
        model = DeploymentAuthorityModel(model_path="/dev/null", ledger=None)
        model._assignments = [assignment]

        is_valid, violations = model.validate_topology()
        assert not is_valid, (
            f"Role {role} holding (deploy, change_enforcement_mode) "
            f"should be rejected"
        )


def test_property_5_explicit_forbidden_pair_3_change_enforcement_execute_override() -> None:
    """**Validates: Requirements 5.2, 5.3**

    Verify change_enforcement_mode and execute_override cannot be held by one role.
    CTO Decision (2026-05-31): This implementation pair is KEPT in the additive set.
    """
    for role in all_roles:
        assignment = AuthorityAssignment(
            role=role,
            authorities=frozenset(
                {Authority.CHANGE_ENFORCEMENT_MODE, Authority.EXECUTE_OVERRIDE}
            ),
        )
        model = DeploymentAuthorityModel(model_path="/dev/null", ledger=None)
        model._assignments = [assignment]

        is_valid, violations = model.validate_topology()
        assert not is_valid, (
            f"Role {role} holding (change_enforcement_mode, execute_override) "
            f"should be rejected"
        )


# =============================================================================
# Property 5 — check_authority verification
# Verify check_authority only succeeds for assigned authorities.
# Test all 6 authority values against all 3 roles.
# =============================================================================


def test_property_5_check_authority_all_roles_all_authorities() -> None:
    """**Validates: Requirements 4.3, 5.1**

    Verify check_authority only succeeds for assigned authorities.
    Tests all 6 authority values against all 3 roles using the
    canonical model assignment.
    """
    # Canonical model: OWNER=(mutate_governance, change_enforcement_mode),
    # CI=(deploy, accept_runtime_hash), RUNTIME=(execute_override, change_fail_mode)
    canonical_assignments = [
        AuthorityAssignment(
            role=AuthorityRole.OWNER,
            authorities=frozenset(
                {Authority.MUTATE_GOVERNANCE, Authority.CHANGE_ENFORCEMENT_MODE}
            ),
        ),
        AuthorityAssignment(
            role=AuthorityRole.CI,
            authorities=frozenset(
                {Authority.DEPLOY, Authority.ACCEPT_RUNTIME_HASH}
            ),
        ),
        AuthorityAssignment(
            role=AuthorityRole.RUNTIME,
            authorities=frozenset(
                {Authority.EXECUTE_OVERRIDE, Authority.CHANGE_FAIL_MODE}
            ),
        ),
    ]

    model = DeploymentAuthorityModel(model_path="/dev/null", ledger=None)
    model._assignments = canonical_assignments

    # Expected mapping
    expected = {
        AuthorityRole.OWNER: {Authority.MUTATE_GOVERNANCE, Authority.CHANGE_ENFORCEMENT_MODE},
        AuthorityRole.CI: {Authority.DEPLOY, Authority.ACCEPT_RUNTIME_HASH},
        AuthorityRole.RUNTIME: {Authority.EXECUTE_OVERRIDE, Authority.CHANGE_FAIL_MODE},
    }

    for role in all_roles:
        for authority in all_authorities:
            result = model.check_authority(role, authority)
            if authority in expected[role]:
                assert result is True, (
                    f"Expected {role} to hold {authority}"
                )
            else:
                assert result is False, (
                    f"Expected {role} NOT to hold {authority}"
                )


# =============================================================================
# Property 6: Deploy Provenance Round-Trip
# Validates: Requirements 6.1, 6.5
# =============================================================================


@given(
    deploy_id=deploy_id_strategy,
    timestamp=timestamp_strategy,
    actor_role=st.sampled_from(all_roles),
    authority_used=st.sampled_from(all_authorities),
    is_validated=st.booleans(),
    runtime_hash=hash_strategy,
    details=details_strategy,
)
@settings(max_examples=200)
def test_property_6_deploy_provenance_roundtrip(
    deploy_id: str,
    timestamp: str,
    actor_role: AuthorityRole,
    authority_used: Authority,
    is_validated: bool,
    runtime_hash: str,
    details: dict,
) -> None:
    """**Validates: Requirements 6.1, 6.5**

    For any valid DeployProvenance record, serialize/deserialize
    produces an equivalent object.
    """
    original = DeployProvenance(
        deploy_id=deploy_id,
        timestamp=timestamp,
        actor_role=actor_role,
        authority_used=authority_used,
        is_validated=is_validated,
        runtime_hash=runtime_hash,
        details=details,
    )

    serialized = original.to_dict()
    deserialized = DeployProvenance.from_dict(serialized)

    assert deserialized.deploy_id == original.deploy_id
    assert deserialized.timestamp == original.timestamp
    assert deserialized.actor_role == original.actor_role
    assert deserialized.authority_used == original.authority_used
    assert deserialized.is_validated == original.is_validated
    assert deserialized.runtime_hash == original.runtime_hash
    assert deserialized.details == original.details


def test_property_6_unvalidated_provenance_emits_warning(caplog) -> None:
    """**Validates: Requirements 6.1**

    Verify invalid deploy provenance (is_validated=False) emits WARNING.
    """
    mock_ledger = MagicMock()
    model = DeploymentAuthorityModel(model_path="/dev/null", ledger=mock_ledger)

    provenance = DeployProvenance(
        deploy_id="test-deploy-001",
        timestamp="2026-06-01T14:00:00Z",
        actor_role=AuthorityRole.CI,
        authority_used=Authority.DEPLOY,
        is_validated=False,
        runtime_hash="sha256:abc123",
        details={"workflow": "test"},
    )

    with caplog.at_level(logging.WARNING):
        model.record_deploy_provenance(provenance)

    # Verify WARNING was logged
    assert any(
        "Unvalidated deployment" in record.message
        for record in caplog.records
    ), "Expected WARNING log for unvalidated deployment"

    # Verify ledger was called with WARNING severity
    mock_ledger.append.assert_called_once()
    entry = mock_ledger.append.call_args[0][0]
    assert entry.severity == "WARNING"


def test_property_6_validated_provenance_accepted_consistently() -> None:
    """**Validates: Requirements 6.1**

    Verify validated provenance is accepted consistently (INFO severity,
    no warning emitted).
    """
    mock_ledger = MagicMock()
    model = DeploymentAuthorityModel(model_path="/dev/null", ledger=mock_ledger)

    provenance = DeployProvenance(
        deploy_id="test-deploy-002",
        timestamp="2026-06-01T15:00:00Z",
        actor_role=AuthorityRole.CI,
        authority_used=Authority.DEPLOY,
        is_validated=True,
        runtime_hash="sha256:def456",
        details={"workflow": "production"},
    )

    model.record_deploy_provenance(provenance)

    # Verify ledger was called with INFO severity
    mock_ledger.append.assert_called_once()
    entry = mock_ledger.append.call_args[0][0]
    assert entry.severity == "INFO"
