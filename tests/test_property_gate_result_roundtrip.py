"""Property test: GateResult Round-Trip Serialization.

**Property 1: GateResult Round-Trip Serialization**
**Validates: Requirements 5.6, 26.4**

Tests that for any valid GateResult (valid statuses: pass/fail/timeout/skip,
valid enforcement_actions: block/warn/info, arbitrary duration_ms, details
lists, timestamps, policy versions, provenance strings), to_dict() then
from_dict() produces an equivalent object.

Also tests GateSummary round-trip serialization.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from governance.gate_framework import (
    GateResult,
    GateSummary,
    VALID_STATUSES,
    VALID_ENFORCEMENT_ACTIONS,
    VALID_AGGREGATE_STATES,
)


# Strategies for GateResult fields
status_strategy = st.sampled_from(sorted(VALID_STATUSES))
enforcement_action_strategy = st.sampled_from(sorted(VALID_ENFORCEMENT_ACTIONS))
duration_ms_strategy = st.floats(min_value=0.0, max_value=120000.0, allow_nan=False, allow_infinity=False)
gate_name_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P")),
    min_size=1,
    max_size=80,
)
details_strategy = st.lists(
    st.text(min_size=0, max_size=200),
    max_size=10,
)
timestamp_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P")),
    min_size=1,
    max_size=40,
)
policy_version_strategy = st.text(min_size=0, max_size=80)
provenance_strategy = st.text(min_size=0, max_size=40)


@given(
    gate_name=gate_name_strategy,
    status=status_strategy,
    enforcement_action=enforcement_action_strategy,
    duration_ms=duration_ms_strategy,
    details=details_strategy,
    timestamp=timestamp_strategy,
    policy_version=policy_version_strategy,
    provenance=provenance_strategy,
)
@settings(max_examples=100)
def test_gate_result_roundtrip_serialization(
    gate_name: str,
    status: str,
    enforcement_action: str,
    duration_ms: float,
    details: list[str],
    timestamp: str,
    policy_version: str,
    provenance: str,
) -> None:
    """For any valid GateResult, to_dict() then from_dict() produces an equivalent object."""
    original = GateResult(
        gate_name=gate_name,
        status=status,
        enforcement_action=enforcement_action,
        duration_ms=duration_ms,
        details=details,
        timestamp=timestamp,
        governance_policy_version=policy_version,
        governance_state_provenance=provenance,
    )

    serialized = original.to_dict()
    deserialized = GateResult.from_dict(serialized)

    assert deserialized.gate_name == original.gate_name
    assert deserialized.status == original.status
    assert deserialized.enforcement_action == original.enforcement_action
    assert deserialized.duration_ms == original.duration_ms
    assert deserialized.details == original.details
    assert deserialized.timestamp == original.timestamp
    assert deserialized.governance_policy_version == original.governance_policy_version
    assert deserialized.governance_state_provenance == original.governance_state_provenance


# Strategies for GateSummary fields
aggregate_state_strategy = st.sampled_from(sorted(VALID_AGGREGATE_STATES))
int_strategy = st.integers(min_value=0, max_value=1000)
sha_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=0,
    max_size=64,
)
branch_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P")),
    min_size=0,
    max_size=50,
)
overhead_strategy = st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)


@given(
    total_gates=int_strategy,
    passed=int_strategy,
    failed=int_strategy,
    blocked=int_strategy,
    timed_out=int_strategy,
    total_duration_ms=duration_ms_strategy,
    aggregate_state=aggregate_state_strategy,
    git_sha=sha_strategy,
    branch=branch_strategy,
    runtime_integrity_hash=sha_strategy,
    governance_overhead_percent=overhead_strategy,
)
@settings(max_examples=100)
def test_gate_summary_roundtrip_serialization(
    total_gates: int,
    passed: int,
    failed: int,
    blocked: int,
    timed_out: int,
    total_duration_ms: float,
    aggregate_state: str,
    git_sha: str,
    branch: str,
    runtime_integrity_hash: str,
    governance_overhead_percent: float,
) -> None:
    """For any valid GateSummary, to_dict() then from_dict() produces an equivalent object."""
    original = GateSummary(
        total_gates=total_gates,
        passed=passed,
        failed=failed,
        blocked=blocked,
        timed_out=timed_out,
        total_duration_ms=total_duration_ms,
        aggregate_state=aggregate_state,
        git_sha=git_sha,
        branch=branch,
        runtime_integrity_hash=runtime_integrity_hash,
        governance_overhead_percent=governance_overhead_percent,
    )

    serialized = original.to_dict()
    deserialized = GateSummary.from_dict(serialized)

    assert deserialized.total_gates == original.total_gates
    assert deserialized.passed == original.passed
    assert deserialized.failed == original.failed
    assert deserialized.blocked == original.blocked
    assert deserialized.timed_out == original.timed_out
    assert deserialized.total_duration_ms == original.total_duration_ms
    assert deserialized.aggregate_state == original.aggregate_state
    assert deserialized.git_sha == original.git_sha
    assert deserialized.branch == original.branch
    assert deserialized.runtime_integrity_hash == original.runtime_integrity_hash
    assert deserialized.governance_overhead_percent == original.governance_overhead_percent
