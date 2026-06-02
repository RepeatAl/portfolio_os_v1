"""Unit tests for governance/schema_version_registry.py.

Validates: Requirements 23.1, 23.2, 23.3, 23.4
"""

import pytest

from governance.schema_version_registry import (
    DEPLOYMENT_MATRIX_VERSION,
    PROVENANCE_VERSION,
    REASONING_OBJECT_VERSION,
    RUN_CONTEXT_VERSION,
    SCHEMA_VERSIONS,
    SEMANTIC_STATE_VERSION,
    _parse_version,
    get_schema_version,
    log_version_mismatch,
    validate_compatibility,
)


class TestVersionConstants:
    """Requirement 23.1: All 5 schemas carry canonical version identifiers."""

    def test_all_five_schemas_registered(self):
        expected_schemas = {
            "Semantic_State",
            "Reasoning_Object",
            "Run_Context",
            "Deployment_Matrix",
            "Provenance",
        }
        assert set(SCHEMA_VERSIONS.keys()) == expected_schemas

    def test_all_versions_start_at_1_0_0(self):
        for schema_name, version in SCHEMA_VERSIONS.items():
            assert version == "1.0.0", f"{schema_name} should start at 1.0.0"

    def test_individual_constants_match_registry(self):
        assert SEMANTIC_STATE_VERSION == SCHEMA_VERSIONS["Semantic_State"]
        assert REASONING_OBJECT_VERSION == SCHEMA_VERSIONS["Reasoning_Object"]
        assert RUN_CONTEXT_VERSION == SCHEMA_VERSIONS["Run_Context"]
        assert DEPLOYMENT_MATRIX_VERSION == SCHEMA_VERSIONS["Deployment_Matrix"]
        assert PROVENANCE_VERSION == SCHEMA_VERSIONS["Provenance"]

    def test_versions_use_semantic_versioning_format(self):
        for schema_name, version in SCHEMA_VERSIONS.items():
            parts = version.split(".")
            assert len(parts) == 3, f"{schema_name} version must be MAJOR.MINOR.PATCH"
            for part in parts:
                assert part.isdigit(), f"{schema_name} version components must be integers"


class TestParseVersion:
    """Tests for the internal version parsing utility."""

    def test_valid_version(self):
        assert _parse_version("1.0.0") == (1, 0, 0)
        assert _parse_version("2.3.4") == (2, 3, 4)
        assert _parse_version("10.20.30") == (10, 20, 30)

    def test_invalid_format_too_few_parts(self):
        with pytest.raises(ValueError, match="expected MAJOR.MINOR.PATCH"):
            _parse_version("1.0")

    def test_invalid_format_too_many_parts(self):
        with pytest.raises(ValueError, match="expected MAJOR.MINOR.PATCH"):
            _parse_version("1.0.0.0")

    def test_invalid_format_non_integer(self):
        with pytest.raises(ValueError, match="must be integers"):
            _parse_version("1.x.0")

    def test_invalid_format_negative(self):
        with pytest.raises(ValueError, match="must be non-negative"):
            _parse_version("-1.0.0")


class TestValidateCompatibility:
    """Requirement 23.4: Same MAJOR version = compatible."""

    def test_same_version_is_compatible(self):
        assert validate_compatibility("1.0.0", "1.0.0") is True

    def test_same_major_different_minor_is_compatible(self):
        assert validate_compatibility("1.2.0", "1.0.0") is True
        assert validate_compatibility("1.0.0", "1.3.0") is True

    def test_same_major_different_patch_is_compatible(self):
        assert validate_compatibility("1.0.1", "1.0.0") is True

    def test_different_major_is_incompatible(self):
        assert validate_compatibility("2.0.0", "1.0.0") is False
        assert validate_compatibility("1.0.0", "3.0.0") is False

    def test_invalid_version_raises(self):
        with pytest.raises(ValueError):
            validate_compatibility("bad", "1.0.0")
        with pytest.raises(ValueError):
            validate_compatibility("1.0.0", "bad")


class TestLogVersionMismatch:
    """Requirement 23.4: Log warning if MINOR versions differ."""

    def test_identical_versions_returns_none(self):
        result = log_version_mismatch("1.0.0", "1.0.0", "Reasoning_Object")
        assert result is None

    def test_minor_difference_returns_warning(self):
        result = log_version_mismatch("1.2.0", "1.0.0", "Reasoning_Object")
        assert result is not None
        assert "SCHEMA VERSION WARNING" in result
        assert "Reasoning_Object" in result
        assert "1.2.0" in result
        assert "1.0.0" in result

    def test_minor_difference_reverse_returns_warning(self):
        result = log_version_mismatch("1.0.0", "1.3.0", "Run_Context")
        assert result is not None
        assert "Run_Context" in result

    def test_patch_only_difference_returns_none(self):
        # Same MAJOR and MINOR, only PATCH differs — no MINOR mismatch warning
        result = log_version_mismatch("1.0.1", "1.0.0", "Provenance")
        assert result is None

    def test_different_major_returns_none(self):
        # MAJOR incompatibility is handled by validate_compatibility, not here
        result = log_version_mismatch("2.0.0", "1.0.0", "Semantic_State")
        assert result is None

    def test_invalid_version_raises(self):
        with pytest.raises(ValueError):
            log_version_mismatch("bad", "1.0.0", "Test")


class TestGetSchemaVersion:
    """Tests for schema version retrieval."""

    def test_get_known_schema(self):
        assert get_schema_version("Semantic_State") == "1.0.0"
        assert get_schema_version("Reasoning_Object") == "1.0.0"
        assert get_schema_version("Run_Context") == "1.0.0"
        assert get_schema_version("Deployment_Matrix") == "1.0.0"
        assert get_schema_version("Provenance") == "1.0.0"

    def test_get_unknown_schema_raises(self):
        with pytest.raises(KeyError, match="Unknown schema"):
            get_schema_version("NonExistent")
