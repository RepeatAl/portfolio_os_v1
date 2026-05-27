"""
Tests for validation error classes.

Validates:
- ValidationError dataclass fields and behavior
- Error codes E001-E010 definitions and defaults
- Error message formatting with actionable suggestions
- Factory functions for common error types
- Enforcement mode handling (blocking vs warning)
"""

import pytest
from validation_error_classes import (
    ValidationError,
    ErrorCode,
    ErrorSeverity,
    EnforcementMode,
    ERROR_CODE_DESCRIPTIONS,
    ERROR_CODE_SEVERITIES,
    ERROR_CODE_SUGGESTIONS,
    create_registration_error,
    create_invalid_domain_error,
    create_invalid_lifecycle_error,
    create_boundary_violation_error,
    create_ssot_conflict_error,
    create_missing_metadata_error,
    create_deprecated_modification_error,
    create_authority_chain_error,
    create_forbidden_provider_error,
    create_no_report_value_error,
)


class TestValidationErrorDataclass:
    """Tests for the ValidationError dataclass structure"""

    def test_create_validation_error_with_all_fields(self):
        """All fields are stored correctly on the dataclass"""
        error = ValidationError(
            gate_name="Gate 1: Artifact Registration",
            artifact_id="my_artifact_md",
            error_code="E001",
            error_message="Artifact not registered",
            suggestion="Register the artifact",
            severity="high",
            enforcement_mode="warning",
        )
        assert error.gate_name == "Gate 1: Artifact Registration"
        assert error.artifact_id == "my_artifact_md"
        assert error.error_code == "E001"
        assert error.error_message == "Artifact not registered"
        assert error.suggestion == "Register the artifact"
        assert error.severity == "high"
        assert error.enforcement_mode == "warning"

    def test_is_blocking_returns_true_for_blocking_mode(self):
        """is_blocking() returns True when enforcement_mode is blocking"""
        error = ValidationError(
            gate_name="Gate 2: Domain Assignment",
            artifact_id="test_artifact",
            error_code="E002",
            error_message="Invalid domain",
            suggestion="Fix domain",
            severity="high",
            enforcement_mode="blocking",
        )
        assert error.is_blocking() is True

    def test_is_blocking_returns_false_for_warning_mode(self):
        """is_blocking() returns False when enforcement_mode is warning"""
        error = ValidationError(
            gate_name="Gate 2: Domain Assignment",
            artifact_id="test_artifact",
            error_code="E002",
            error_message="Invalid domain",
            suggestion="Fix domain",
            severity="high",
            enforcement_mode="warning",
        )
        assert error.is_blocking() is False

    def test_str_representation(self):
        """__str__ provides concise log-friendly output"""
        error = ValidationError(
            gate_name="Gate 3: Lifecycle",
            artifact_id="engine_py",
            error_code="E003",
            error_message="Invalid transition: draft -> active",
            suggestion="Use development first",
            severity="medium",
            enforcement_mode="warning",
        )
        result = str(error)
        assert "[E003]" in result
        assert "engine_py" in result
        assert "Invalid transition" in result


class TestErrorMessageFormatting:
    """Tests for format_error() output with actionable suggestions"""

    def test_format_error_includes_severity_icon(self):
        """Formatted error includes appropriate severity icon"""
        error = ValidationError(
            gate_name="Gate 1: Artifact Registration",
            artifact_id="test_file_py",
            error_code="E001",
            error_message="Artifact not registered",
            suggestion="Add frontmatter",
            severity="critical",
            enforcement_mode="blocking",
        )
        formatted = error.format_error()
        assert "🔴" in formatted

    def test_format_error_includes_error_code(self):
        """Formatted error includes the error code"""
        error = ValidationError(
            gate_name="Gate 4: Boundary Enforcement",
            artifact_id="some_artifact",
            error_code="E004",
            error_message="Boundary violation",
            suggestion="Request permission",
            severity="high",
            enforcement_mode="warning",
        )
        formatted = error.format_error()
        assert "[E004]" in formatted

    def test_format_error_includes_gate_name(self):
        """Formatted error includes the gate name"""
        error = ValidationError(
            gate_name="Gate 5: SSOT Consistency",
            artifact_id="doc_md",
            error_code="E005",
            error_message="SSOT conflict",
            suggestion="Mark one as canonical",
            severity="critical",
            enforcement_mode="blocking",
        )
        formatted = error.format_error()
        assert "Gate 5: SSOT Consistency" in formatted

    def test_format_error_includes_artifact_id(self):
        """Formatted error includes the artifact identifier"""
        error = ValidationError(
            gate_name="Gate 1: Artifact Registration",
            artifact_id="engines/allocation_engine_py",
            error_code="E001",
            error_message="Not registered",
            suggestion="Register it",
            severity="high",
            enforcement_mode="warning",
        )
        formatted = error.format_error()
        assert "engines/allocation_engine_py" in formatted

    def test_format_error_includes_suggestion(self):
        """Formatted error includes actionable suggestion"""
        error = ValidationError(
            gate_name="Gate 3: Lifecycle",
            artifact_id="test_artifact",
            error_code="E003",
            error_message="Invalid transition",
            suggestion="Valid transitions from draft: review",
            severity="medium",
            enforcement_mode="warning",
        )
        formatted = error.format_error()
        assert "Valid transitions from draft: review" in formatted

    def test_format_error_shows_blocking_label(self):
        """Formatted error shows BLOCKING when enforcement_mode is blocking"""
        error = ValidationError(
            gate_name="Gate 4: Boundary Enforcement",
            artifact_id="test",
            error_code="E004",
            error_message="Violation",
            suggestion="Fix it",
            severity="high",
            enforcement_mode="blocking",
        )
        formatted = error.format_error()
        assert "BLOCKING" in formatted

    def test_format_error_shows_warning_label(self):
        """Formatted error shows WARNING when enforcement_mode is warning"""
        error = ValidationError(
            gate_name="Gate 4: Boundary Enforcement",
            artifact_id="test",
            error_code="E004",
            error_message="Violation",
            suggestion="Fix it",
            severity="high",
            enforcement_mode="warning",
        )
        formatted = error.format_error()
        assert "WARNING" in formatted

    def test_format_error_severity_icons(self):
        """Each severity level maps to the correct icon"""
        severities_and_icons = [
            ("critical", "🔴"),
            ("high", "🟠"),
            ("medium", "🟡"),
            ("low", "🟢"),
        ]
        for severity, expected_icon in severities_and_icons:
            error = ValidationError(
                gate_name="Gate 1: Registration",
                artifact_id="test",
                error_code="E001",
                error_message="Test",
                suggestion="Test",
                severity=severity,
                enforcement_mode="warning",
            )
            assert expected_icon in error.format_error()


class TestErrorCodes:
    """Tests for error code definitions E001-E010"""

    def test_all_ten_error_codes_defined(self):
        """All 10 error codes E001-E010 are defined"""
        expected_codes = [
            "E001", "E002", "E003", "E004", "E005",
            "E006", "E007", "E008", "E009", "E010",
        ]
        actual_codes = [code.value for code in ErrorCode]
        for expected in expected_codes:
            assert expected in actual_codes

    def test_error_code_descriptions_complete(self):
        """Every error code has a description"""
        for code in ErrorCode:
            assert code in ERROR_CODE_DESCRIPTIONS
            assert len(ERROR_CODE_DESCRIPTIONS[code]) > 0

    def test_error_code_severities_complete(self):
        """Every error code has a default severity"""
        for code in ErrorCode:
            assert code in ERROR_CODE_SEVERITIES
            assert ERROR_CODE_SEVERITIES[code] in ErrorSeverity

    def test_error_code_suggestions_complete(self):
        """Every error code has a default suggestion"""
        for code in ErrorCode:
            assert code in ERROR_CODE_SUGGESTIONS
            assert len(ERROR_CODE_SUGGESTIONS[code]) > 0

    def test_critical_severity_codes(self):
        """E005, E008, E009 are critical severity by default"""
        critical_codes = [
            ErrorCode.E005_SSOT_CONFLICT_DETECTED,
            ErrorCode.E008_AUTHORITY_CHAIN_VIOLATION,
            ErrorCode.E009_FORBIDDEN_CLOUD_PROVIDER_REFERENCE,
        ]
        for code in critical_codes:
            assert ERROR_CODE_SEVERITIES[code] == ErrorSeverity.CRITICAL

    def test_high_severity_codes(self):
        """E001, E002, E004, E007 are high severity by default"""
        high_codes = [
            ErrorCode.E001_ARTIFACT_NOT_REGISTERED,
            ErrorCode.E002_INVALID_DOMAIN_ASSIGNMENT,
            ErrorCode.E004_DOMAIN_BOUNDARY_VIOLATION,
            ErrorCode.E007_DEPRECATED_ARTIFACT_MODIFICATION,
        ]
        for code in high_codes:
            assert ERROR_CODE_SEVERITIES[code] == ErrorSeverity.HIGH

    def test_medium_severity_codes(self):
        """E003, E006 are medium severity by default"""
        medium_codes = [
            ErrorCode.E003_INVALID_LIFECYCLE_TRANSITION,
            ErrorCode.E006_MISSING_REQUIRED_METADATA,
        ]
        for code in medium_codes:
            assert ERROR_CODE_SEVERITIES[code] == ErrorSeverity.MEDIUM

    def test_low_severity_codes(self):
        """E010 is low severity by default"""
        assert ERROR_CODE_SEVERITIES[ErrorCode.E010_FEATURE_WITHOUT_REPORT_VALUE] == ErrorSeverity.LOW


class TestFromErrorCodeFactory:
    """Tests for ValidationError.from_error_code() factory method"""

    def test_creates_error_with_defaults(self):
        """from_error_code uses default description, suggestion, severity"""
        error = ValidationError.from_error_code(
            gate_name="Gate 1: Artifact Registration",
            artifact_id="test_artifact",
            error_code=ErrorCode.E001_ARTIFACT_NOT_REGISTERED,
        )
        assert error.error_code == "E001"
        assert error.severity == "high"
        assert error.enforcement_mode == "warning"
        assert "not registered" in error.error_message.lower()
        assert len(error.suggestion) > 0

    def test_overrides_error_message(self):
        """Custom error_message overrides the default"""
        custom_msg = "Custom error message for testing"
        error = ValidationError.from_error_code(
            gate_name="Gate 2: Domain Assignment",
            artifact_id="test",
            error_code=ErrorCode.E002_INVALID_DOMAIN_ASSIGNMENT,
            error_message=custom_msg,
        )
        assert error.error_message == custom_msg

    def test_overrides_suggestion(self):
        """Custom suggestion overrides the default"""
        custom_suggestion = "Do this specific thing"
        error = ValidationError.from_error_code(
            gate_name="Gate 3: Lifecycle",
            artifact_id="test",
            error_code=ErrorCode.E003_INVALID_LIFECYCLE_TRANSITION,
            suggestion=custom_suggestion,
        )
        assert error.suggestion == custom_suggestion

    def test_overrides_severity(self):
        """Custom severity overrides the default"""
        error = ValidationError.from_error_code(
            gate_name="Gate 1: Registration",
            artifact_id="test",
            error_code=ErrorCode.E001_ARTIFACT_NOT_REGISTERED,
            severity="low",
        )
        assert error.severity == "low"

    def test_enforcement_mode_defaults_to_warning(self):
        """Default enforcement mode is warning (FAST LANE phase)"""
        error = ValidationError.from_error_code(
            gate_name="Gate 1: Registration",
            artifact_id="test",
            error_code=ErrorCode.E001_ARTIFACT_NOT_REGISTERED,
        )
        assert error.enforcement_mode == "warning"

    def test_enforcement_mode_can_be_blocking(self):
        """Enforcement mode can be set to blocking for post-MVP"""
        error = ValidationError.from_error_code(
            gate_name="Gate 1: Registration",
            artifact_id="test",
            error_code=ErrorCode.E001_ARTIFACT_NOT_REGISTERED,
            enforcement_mode=EnforcementMode.BLOCKING,
        )
        assert error.enforcement_mode == "blocking"
        assert error.is_blocking() is True


class TestFactoryFunctions:
    """Tests for convenience factory functions"""

    def test_create_registration_error(self):
        """create_registration_error produces E001 error"""
        error = create_registration_error(
            artifact_id="my_file_md",
            file_path="docs/my_file.md",
        )
        assert error.error_code == "E001"
        assert error.gate_name == "Gate 1: Artifact Registration"
        assert "my_file.md" in error.error_message
        assert error.severity == "high"

    def test_create_invalid_domain_error(self):
        """create_invalid_domain_error produces E002 error with valid domains"""
        error = create_invalid_domain_error(
            artifact_id="engine_py",
            domain_id="REPORT",
            artifact_type="ENGINE",
            valid_domains=["SIGNALS", "SEMANTICS", "REASONING"],
        )
        assert error.error_code == "E002"
        assert "REPORT" in error.error_message
        assert "ENGINE" in error.error_message
        assert "SIGNALS" in error.suggestion

    def test_create_invalid_lifecycle_error(self):
        """create_invalid_lifecycle_error produces E003 error with transitions"""
        error = create_invalid_lifecycle_error(
            artifact_id="doc_md",
            from_state="draft",
            to_state="deprecated",
            allowed_transitions=["review"],
        )
        assert error.error_code == "E003"
        assert "draft" in error.error_message
        assert "deprecated" in error.error_message
        assert "review" in error.suggestion

    def test_create_boundary_violation_error(self):
        """create_boundary_violation_error produces E004 error"""
        error = create_boundary_violation_error(
            artifact_id="signals_engine_py",
            modifier_domain="REPORT",
            primary_domain="SIGNALS",
        )
        assert error.error_code == "E004"
        assert "REPORT" in error.error_message
        assert "SIGNALS" in error.error_message

    def test_create_ssot_conflict_error(self):
        """create_ssot_conflict_error produces E005 error"""
        error = create_ssot_conflict_error(
            artifact_id="new_doc_md",
            topic="portfolio_architecture",
            conflicting_artifact_id="existing_doc_md",
        )
        assert error.error_code == "E005"
        assert "portfolio_architecture" in error.error_message
        assert "existing_doc_md" in error.suggestion
        assert error.severity == "critical"

    def test_create_missing_metadata_error(self):
        """create_missing_metadata_error produces E006 error with field names"""
        error = create_missing_metadata_error(
            artifact_id="incomplete_artifact",
            missing_fields=["primary_domain", "lifecycle_status"],
        )
        assert error.error_code == "E006"
        assert "primary_domain" in error.error_message
        assert "lifecycle_status" in error.error_message

    def test_create_deprecated_modification_error(self):
        """create_deprecated_modification_error produces E007 error"""
        error = create_deprecated_modification_error(
            artifact_id="old_engine_py",
        )
        assert error.error_code == "E007"
        assert "old_engine_py" in error.error_message

    def test_create_authority_chain_error(self):
        """create_authority_chain_error produces E008 error"""
        error = create_authority_chain_error(
            artifact_id="semantic_state_py",
            modifier_domain="SIGNALS",
            target_domain="SEMANTICS",
        )
        assert error.error_code == "E008"
        assert "SIGNALS" in error.error_message
        assert "SEMANTICS" in error.error_message
        assert error.severity == "critical"

    def test_create_forbidden_provider_error(self):
        """create_forbidden_provider_error produces E009 error"""
        error = create_forbidden_provider_error(
            artifact_id="deploy_config",
            provider="AWS",
            file_path="deploy/config.yaml",
        )
        assert error.error_code == "E009"
        assert "AWS" in error.error_message
        assert "deploy/config.yaml" in error.error_message
        assert error.severity == "critical"

    def test_create_no_report_value_error(self):
        """create_no_report_value_error produces E010 error"""
        error = create_no_report_value_error(
            artifact_id="new_feature",
            feature_name="fancy_dashboard_widget",
        )
        assert error.error_code == "E010"
        assert "fancy_dashboard_widget" in error.error_message
        assert error.severity == "low"

    def test_factory_functions_default_to_warning_mode(self):
        """All factory functions default to warning enforcement mode"""
        errors = [
            create_registration_error("a", "path"),
            create_invalid_domain_error("a", "D", "T"),
            create_invalid_lifecycle_error("a", "s1", "s2"),
            create_boundary_violation_error("a", "D1", "D2"),
            create_ssot_conflict_error("a", "topic", "b"),
            create_missing_metadata_error("a"),
            create_deprecated_modification_error("a"),
            create_authority_chain_error("a", "D1", "D2"),
            create_forbidden_provider_error("a", "AWS", "f"),
            create_no_report_value_error("a", "feat"),
        ]
        for error in errors:
            assert error.enforcement_mode == "warning"

    def test_factory_functions_accept_blocking_mode(self):
        """Factory functions can produce blocking errors for post-MVP"""
        error = create_registration_error(
            artifact_id="test",
            file_path="test.py",
            enforcement_mode=EnforcementMode.BLOCKING,
        )
        assert error.enforcement_mode == "blocking"
        assert error.is_blocking() is True
