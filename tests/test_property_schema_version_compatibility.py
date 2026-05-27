"""Property-based tests for Schema Version Compatibility.

**Validates: Requirements 23.2, 23.4**

Tests that same MAJOR versions are compatible, different MAJOR versions are
incompatible, MINOR differences produce warnings, identical versions produce
no warnings, and compatibility is symmetric.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from governance.schema_version_registry import log_version_mismatch, validate_compatibility


# Strategy: generate a version component (integer 0-99)
version_component = st.integers(min_value=0, max_value=99)

# Strategy: generate a full version string "MAJOR.MINOR.PATCH"
version_strategy = st.builds(
    lambda major, minor, patch: f"{major}.{minor}.{patch}",
    major=version_component,
    minor=version_component,
    patch=version_component,
)

# Strategy: generate a schema name for log_version_mismatch
schema_name_strategy = st.sampled_from(
    ["Semantic_State", "Reasoning_Object", "Run_Context", "Deployment_Matrix", "Provenance"]
)


class TestSchemaVersionCompatibilityProperties:
    """Property-based tests for schema version compatibility functions."""

    @given(
        major=version_component,
        minor_a=version_component,
        patch_a=version_component,
        minor_b=version_component,
        patch_b=version_component,
    )
    @settings(max_examples=500)
    def test_same_major_always_compatible(
        self,
        major: int,
        minor_a: int,
        patch_a: int,
        minor_b: int,
        patch_b: int,
    ) -> None:
        """Property 1: Same MAJOR version is always compatible regardless of MINOR/PATCH.

        **Validates: Requirements 23.2, 23.4**

        For any two versions sharing the same MAJOR component,
        validate_compatibility returns True.
        """
        version_a = f"{major}.{minor_a}.{patch_a}"
        version_b = f"{major}.{minor_b}.{patch_b}"

        result = validate_compatibility(version_a, version_b)

        assert result is True, (
            f"Same MAJOR versions should be compatible: "
            f"{version_a} vs {version_b} returned {result}"
        )

    @given(
        major_a=version_component,
        major_b=version_component,
        minor_a=version_component,
        patch_a=version_component,
        minor_b=version_component,
        patch_b=version_component,
    )
    @settings(max_examples=500)
    def test_different_major_always_incompatible(
        self,
        major_a: int,
        major_b: int,
        minor_a: int,
        patch_a: int,
        minor_b: int,
        patch_b: int,
    ) -> None:
        """Property 2: Different MAJOR version is always incompatible.

        **Validates: Requirements 23.2, 23.4**

        For any two versions with different MAJOR components,
        validate_compatibility returns False.
        """
        from hypothesis import assume

        assume(major_a != major_b)

        version_a = f"{major_a}.{minor_a}.{patch_a}"
        version_b = f"{major_b}.{minor_b}.{patch_b}"

        result = validate_compatibility(version_a, version_b)

        assert result is False, (
            f"Different MAJOR versions should be incompatible: "
            f"{version_a} vs {version_b} returned {result}"
        )

    @given(
        major=version_component,
        minor_a=version_component,
        minor_b=version_component,
        patch_a=version_component,
        patch_b=version_component,
        schema_name=schema_name_strategy,
    )
    @settings(max_examples=500)
    def test_minor_difference_produces_warning(
        self,
        major: int,
        minor_a: int,
        minor_b: int,
        patch_a: int,
        patch_b: int,
        schema_name: str,
    ) -> None:
        """Property 3: Different MINOR version with same MAJOR produces a warning string.

        **Validates: Requirements 23.4**

        When MAJOR versions match but MINOR versions differ,
        log_version_mismatch returns a non-None warning string.
        """
        from hypothesis import assume

        assume(minor_a != minor_b)

        version_a = f"{major}.{minor_a}.{patch_a}"
        version_b = f"{major}.{minor_b}.{patch_b}"

        result = log_version_mismatch(version_a, version_b, schema_name)

        assert result is not None, (
            f"MINOR version difference should produce warning: "
            f"{version_a} vs {version_b} for schema {schema_name} returned None"
        )
        assert isinstance(result, str), (
            f"Warning should be a string, got {type(result)}"
        )
        assert len(result) > 0, "Warning string should not be empty"

    @given(
        major=version_component,
        minor=version_component,
        patch=version_component,
        schema_name=schema_name_strategy,
    )
    @settings(max_examples=500)
    def test_identical_versions_no_warning(
        self,
        major: int,
        minor: int,
        patch: int,
        schema_name: str,
    ) -> None:
        """Property 4: Identical versions produce no warning (returns None).

        **Validates: Requirements 23.4**

        When producer and consumer have the exact same version,
        log_version_mismatch returns None.
        """
        version = f"{major}.{minor}.{patch}"

        result = log_version_mismatch(version, version, schema_name)

        assert result is None, (
            f"Identical versions should produce no warning: "
            f"{version} vs {version} for schema {schema_name} returned {result!r}"
        )

    @given(
        version_a=version_strategy,
        version_b=version_strategy,
    )
    @settings(max_examples=500)
    def test_compatibility_is_symmetric(
        self,
        version_a: str,
        version_b: str,
    ) -> None:
        """Property 5: Compatibility is symmetric (A compat B iff B compat A).

        **Validates: Requirements 23.2**

        If version A is compatible with version B, then version B must also
        be compatible with version A.
        """
        result_ab = validate_compatibility(version_a, version_b)
        result_ba = validate_compatibility(version_b, version_a)

        assert result_ab == result_ba, (
            f"Compatibility should be symmetric: "
            f"validate_compatibility({version_a}, {version_b}) = {result_ab}, "
            f"validate_compatibility({version_b}, {version_a}) = {result_ba}"
        )
