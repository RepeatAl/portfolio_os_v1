"""Runtime State Model — Multi-dimensional runtime state vocabulary.

Provides shared runtime state vocabulary for all governance-aware components.
States belong to orthogonal integrity dimensions, NOT a single linear severity
ladder. This enables precise failure classification where INVALID (structurally
unusable artifact) and INCONSISTENT (contradictory runtime truth) represent
different failure modes, not comparable severities.

Design Decision (Hardening 1): Multi-dimensional state model with orthogonal
integrity dimensions prevents incorrect linear severity assumptions.
"""

from enum import StrEnum


class RuntimeState(StrEnum):
    """Canonical runtime states for all governance-aware components.

    Each state represents a specific failure mode or health condition.
    States are NOT linearly ordered — they belong to orthogonal integrity
    dimensions defined in STATE_DIMENSIONS.
    """

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    INVALID = "invalid"
    INCONSISTENT = "inconsistent"
    COLLAPSED = "collapsed"
    DETERMINISTIC_FAILURE = "deterministic_failure"
    CANONICAL_BREAK = "canonical_break"


class IntegrityDimension(StrEnum):
    """Orthogonal integrity dimensions for runtime state classification.

    Each dimension represents an independent axis of system health:
    - DATA_AVAILABILITY: healthy → degraded → unavailable → collapsed
    - STRUCTURAL_VALIDITY: healthy → invalid
    - RUNTIME_CONSISTENCY: healthy → inconsistent
    - REPLAY_INTEGRITY: healthy → deterministic_failure
    - CHAIN_INTEGRITY: healthy → canonical_break
    """

    DATA_AVAILABILITY = "data_availability"
    STRUCTURAL_VALIDITY = "structural_validity"
    RUNTIME_CONSISTENCY = "runtime_consistency"
    REPLAY_INTEGRITY = "replay_integrity"
    CHAIN_INTEGRITY = "chain_integrity"


# States grouped by dimension. A state may indicate failure in one dimension
# while others remain healthy. HEALTHY affects no dimensions.
STATE_DIMENSIONS: dict[RuntimeState, list[IntegrityDimension]] = {
    RuntimeState.HEALTHY: [],
    RuntimeState.DEGRADED: [IntegrityDimension.DATA_AVAILABILITY],
    RuntimeState.UNAVAILABLE: [IntegrityDimension.DATA_AVAILABILITY],
    RuntimeState.COLLAPSED: [IntegrityDimension.DATA_AVAILABILITY],
    RuntimeState.INVALID: [IntegrityDimension.STRUCTURAL_VALIDITY],
    RuntimeState.INCONSISTENT: [IntegrityDimension.RUNTIME_CONSISTENCY],
    RuntimeState.DETERMINISTIC_FAILURE: [IntegrityDimension.REPLAY_INTEGRITY],
    RuntimeState.CANONICAL_BREAK: [IntegrityDimension.CHAIN_INTEGRITY],
}


def aggregate_pipeline_state(component_states: list[RuntimeState]) -> RuntimeState:
    """Aggregate component states into pipeline state.

    Uses worst-state-per-dimension logic, then selects the most impactful
    overall state. CANONICAL_BREAK and DETERMINISTIC_FAILURE are treated as
    equally critical (both represent integrity compromise in their respective
    dimensions).

    Priority order (highest to lowest impact):
    1. CANONICAL_BREAK / DETERMINISTIC_FAILURE (chain or replay integrity)
    2. COLLAPSED (complete data availability loss)
    3. INCONSISTENT (runtime consistency failure)
    4. INVALID (structural validity failure)
    5. UNAVAILABLE (partial data availability loss)
    6. DEGRADED (minor data availability reduction)
    7. HEALTHY (no dimension compromised)

    Args:
        component_states: List of RuntimeState values from individual components.
            Empty list returns HEALTHY.

    Returns:
        The aggregated RuntimeState representing the worst overall pipeline health.
    """
    if not component_states:
        return RuntimeState.HEALTHY

    if RuntimeState.CANONICAL_BREAK in component_states or RuntimeState.DETERMINISTIC_FAILURE in component_states:
        if RuntimeState.CANONICAL_BREAK in component_states:
            return RuntimeState.CANONICAL_BREAK
        return RuntimeState.DETERMINISTIC_FAILURE

    if RuntimeState.COLLAPSED in component_states:
        return RuntimeState.COLLAPSED

    if RuntimeState.INCONSISTENT in component_states:
        return RuntimeState.INCONSISTENT

    if RuntimeState.INVALID in component_states:
        return RuntimeState.INVALID

    if RuntimeState.UNAVAILABLE in component_states:
        return RuntimeState.UNAVAILABLE

    if RuntimeState.DEGRADED in component_states:
        return RuntimeState.DEGRADED

    return RuntimeState.HEALTHY
