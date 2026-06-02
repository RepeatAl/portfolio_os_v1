"""Canonical Boundary — Classify artifacts as canonical or transient.

Enforces the boundary between canonical artifacts (subject to full governance
enforcement) and transient artifacts (exempt from canonical governance).

Validates: Requirements 16.1, 16.2, 16.3, 16.4, 16.5
"""

# ---------------------------------------------------------------------------
# Canonical Artifacts (Requirement 16.2)
# Subject to full atomic semantic integrity, determinism, and provenance.
# ---------------------------------------------------------------------------

CANONICAL_ARTIFACTS: frozenset[str] = frozenset({
    "semantic_state_snapshot",
    "reasoning_object",
    "daily_report",
    "deployment_matrix",
    "run_context",
    "provenance_metadata",
})

# ---------------------------------------------------------------------------
# Transient Artifacts (Requirement 16.3)
# Exempt from full governance enforcement. Must not cross runtime boundaries.
# ---------------------------------------------------------------------------

TRANSIENT_ARTIFACTS: frozenset[str] = frozenset({
    "orchestration_buffer",
    "in_memory_transform",
    "pre_validation_staging",
    "intermediate_draft_reasoning",
})


def classify(artifact_name: str) -> str:
    """Classify an artifact as 'canonical' or 'transient'.

    Every runtime artifact must belong to exactly one category
    (Requirement 16.1).

    Args:
        artifact_name: The name/type of the artifact to classify.

    Returns:
        "canonical" if the artifact is in CANONICAL_ARTIFACTS,
        "transient" if the artifact is in TRANSIENT_ARTIFACTS.

    Raises:
        ValueError: If the artifact_name is not recognized in either set.
    """
    if artifact_name in CANONICAL_ARTIFACTS:
        return "canonical"
    if artifact_name in TRANSIENT_ARTIFACTS:
        return "transient"
    raise ValueError(
        f"Unknown artifact '{artifact_name}'. "
        f"Must be one of canonical: {sorted(CANONICAL_ARTIFACTS)} "
        f"or transient: {sorted(TRANSIENT_ARTIFACTS)}"
    )


def enforce_boundary(
    artifact_name: str,
    is_persisted: bool = False,
    is_passed_downstream: bool = False,
) -> str:
    """Enforce the canonical/transient boundary with promotion logic.

    If a transient artifact is persisted or passed to a downstream engine,
    it is promoted to canonical status (Requirement 16.5). Canonical artifacts
    always remain canonical regardless of flags.

    Args:
        artifact_name: The name/type of the artifact.
        is_persisted: Whether the artifact has been or will be persisted to disk.
        is_passed_downstream: Whether the artifact is passed to a downstream
            engine as input.

    Returns:
        "canonical" if the artifact is canonical or was promoted,
        "transient" if the artifact remains transient.

    Raises:
        ValueError: If the artifact_name is not recognized in either set.
    """
    current = classify(artifact_name)

    if current == "transient" and (is_persisted or is_passed_downstream):
        # Promotion: transient artifact crossed a boundary (Requirement 16.5)
        return "canonical"

    return current
