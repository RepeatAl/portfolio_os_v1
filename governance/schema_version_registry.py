"""Schema Version Registry for Portfolio OS canonical artifacts.

Tracks version identifiers for all persisted canonical artifact schemas and
provides compatibility validation between producers and consumers.

Validates: Requirements 23.1, 23.2, 23.3, 23.4
"""

# ---------------------------------------------------------------------------
# Schema Version Constants (Requirement 23.1)
# All canonical schemas start at "1.0.0" using semantic versioning (MAJOR.MINOR.PATCH)
# ---------------------------------------------------------------------------

SEMANTIC_STATE_VERSION: str = "1.0.0"
REASONING_OBJECT_VERSION: str = "1.0.0"
RUN_CONTEXT_VERSION: str = "1.0.0"
DEPLOYMENT_MATRIX_VERSION: str = "1.0.0"
PROVENANCE_VERSION: str = "1.0.0"

# Registry mapping schema names to their current versions
SCHEMA_VERSIONS: dict[str, str] = {
    "Semantic_State": SEMANTIC_STATE_VERSION,
    "Reasoning_Object": REASONING_OBJECT_VERSION,
    "Run_Context": RUN_CONTEXT_VERSION,
    "Deployment_Matrix": DEPLOYMENT_MATRIX_VERSION,
    "Provenance": PROVENANCE_VERSION,
}


def _parse_version(version: str) -> tuple[int, int, int]:
    """Parse a semantic version string into (major, minor, patch) tuple.

    Args:
        version: A string in "MAJOR.MINOR.PATCH" format.

    Returns:
        Tuple of (major, minor, patch) integers.

    Raises:
        ValueError: If the version string is not valid semantic versioning.
    """
    parts = version.strip().split(".")
    if len(parts) != 3:
        raise ValueError(
            f"Invalid version format '{version}': expected MAJOR.MINOR.PATCH"
        )
    try:
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2])
    except ValueError:
        raise ValueError(
            f"Invalid version format '{version}': all components must be integers"
        )
    if major < 0 or minor < 0 or patch < 0:
        raise ValueError(
            f"Invalid version format '{version}': components must be non-negative"
        )
    return (major, minor, patch)


def validate_compatibility(producer_version: str, consumer_version: str) -> bool:
    """Check if producer and consumer schema versions are compatible.

    Compatibility is defined as having the same MAJOR version number.
    Different MAJOR versions indicate breaking changes and are incompatible.

    Validates: Requirement 23.4 — same MAJOR version = compatible.

    Args:
        producer_version: The schema version of the artifact producer.
        consumer_version: The schema version of the artifact consumer.

    Returns:
        True if versions are compatible (same MAJOR), False otherwise.

    Raises:
        ValueError: If either version string is not valid semantic versioning.
    """
    producer_major, _, _ = _parse_version(producer_version)
    consumer_major, _, _ = _parse_version(consumer_version)
    return producer_major == consumer_major


def log_version_mismatch(
    producer_version: str, consumer_version: str, schema_name: str
) -> str | None:
    """Log a warning message if MINOR versions differ between producer and consumer.

    When MINOR versions differ (but MAJOR is the same), this indicates the producer
    uses a newer or older schema revision. A warning is appropriate because the
    consumer may not understand newer optional fields or may expect fields not yet
    present in an older producer.

    Validates: Requirement 23.4 — log warning if MINOR versions differ.

    Args:
        producer_version: The schema version of the artifact producer.
        consumer_version: The schema version of the artifact consumer.
        schema_name: The name of the schema being checked (for the warning message).

    Returns:
        A warning message string if MINOR versions differ, None if versions
        are identical (no mismatch to report).

    Raises:
        ValueError: If either version string is not valid semantic versioning.
    """
    producer_major, producer_minor, producer_patch = _parse_version(producer_version)
    consumer_major, consumer_minor, consumer_patch = _parse_version(consumer_version)

    # If versions are identical, no mismatch to report
    if (producer_major, producer_minor, producer_patch) == (
        consumer_major,
        consumer_minor,
        consumer_patch,
    ):
        return None

    # Only report MINOR differences (MAJOR incompatibility is handled by validate_compatibility)
    if producer_major == consumer_major and producer_minor != consumer_minor:
        return (
            f"[SCHEMA VERSION WARNING] {schema_name}: "
            f"producer version {producer_version} and consumer version {consumer_version} "
            f"have different MINOR versions. "
            f"Producer may include fields unknown to consumer or vice versa."
        )

    return None


def get_schema_version(schema_name: str) -> str:
    """Retrieve the current version for a named schema.

    Args:
        schema_name: One of the registered schema names (Semantic_State,
            Reasoning_Object, Run_Context, Deployment_Matrix, Provenance).

    Returns:
        The current version string for the schema.

    Raises:
        KeyError: If the schema_name is not registered.
    """
    if schema_name not in SCHEMA_VERSIONS:
        raise KeyError(
            f"Unknown schema '{schema_name}'. "
            f"Registered schemas: {list(SCHEMA_VERSIONS.keys())}"
        )
    return SCHEMA_VERSIONS[schema_name]
