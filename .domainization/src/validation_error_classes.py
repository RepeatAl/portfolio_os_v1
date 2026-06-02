"""
Validation Error Classes

Defines structured error types for commit gate validation failures.
Provides error codes E001-E010 for common validation failures with
actionable suggestions and severity levels.

Operates alongside ValidationWarning (observability mode) to provide
blocking validation in post-MVP enforcement mode.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ErrorSeverity(str, Enum):
    """Severity levels for validation errors"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EnforcementMode(str, Enum):
    """Enforcement mode determines whether errors block or warn"""
    BLOCKING = "blocking"
    WARNING = "warning"


class ErrorCode(str, Enum):
    """
    Standard error codes for validation gate failures.
    
    E001-E010 cover the most common validation failures
    across all 5 commit gates.
    """
    E001_ARTIFACT_NOT_REGISTERED = "E001"
    E002_INVALID_DOMAIN_ASSIGNMENT = "E002"
    E003_INVALID_LIFECYCLE_TRANSITION = "E003"
    E004_DOMAIN_BOUNDARY_VIOLATION = "E004"
    E005_SSOT_CONFLICT_DETECTED = "E005"
    E006_MISSING_REQUIRED_METADATA = "E006"
    E007_DEPRECATED_ARTIFACT_MODIFICATION = "E007"
    E008_AUTHORITY_CHAIN_VIOLATION = "E008"
    E009_FORBIDDEN_CLOUD_PROVIDER_REFERENCE = "E009"
    E010_FEATURE_WITHOUT_REPORT_VALUE = "E010"


# Human-readable descriptions for each error code
ERROR_CODE_DESCRIPTIONS = {
    ErrorCode.E001_ARTIFACT_NOT_REGISTERED: "Artifact not registered in domainization system",
    ErrorCode.E002_INVALID_DOMAIN_ASSIGNMENT: "Domain cannot own this artifact type",
    ErrorCode.E003_INVALID_LIFECYCLE_TRANSITION: "Lifecycle state transition is not allowed",
    ErrorCode.E004_DOMAIN_BOUNDARY_VIOLATION: "Modification violates domain boundary rules",
    ErrorCode.E005_SSOT_CONFLICT_DETECTED: "Multiple canonical SSOTs detected for same topic",
    ErrorCode.E006_MISSING_REQUIRED_METADATA: "Required metadata fields are missing",
    ErrorCode.E007_DEPRECATED_ARTIFACT_MODIFICATION: "Cannot modify a deprecated artifact",
    ErrorCode.E008_AUTHORITY_CHAIN_VIOLATION: "Modification violates authority chain order",
    ErrorCode.E009_FORBIDDEN_CLOUD_PROVIDER_REFERENCE: "Forbidden cloud provider reference detected",
    ErrorCode.E010_FEATURE_WITHOUT_REPORT_VALUE: "Feature does not demonstrate report value",
}

# Default severity for each error code
ERROR_CODE_SEVERITIES = {
    ErrorCode.E001_ARTIFACT_NOT_REGISTERED: ErrorSeverity.HIGH,
    ErrorCode.E002_INVALID_DOMAIN_ASSIGNMENT: ErrorSeverity.HIGH,
    ErrorCode.E003_INVALID_LIFECYCLE_TRANSITION: ErrorSeverity.MEDIUM,
    ErrorCode.E004_DOMAIN_BOUNDARY_VIOLATION: ErrorSeverity.HIGH,
    ErrorCode.E005_SSOT_CONFLICT_DETECTED: ErrorSeverity.CRITICAL,
    ErrorCode.E006_MISSING_REQUIRED_METADATA: ErrorSeverity.MEDIUM,
    ErrorCode.E007_DEPRECATED_ARTIFACT_MODIFICATION: ErrorSeverity.HIGH,
    ErrorCode.E008_AUTHORITY_CHAIN_VIOLATION: ErrorSeverity.CRITICAL,
    ErrorCode.E009_FORBIDDEN_CLOUD_PROVIDER_REFERENCE: ErrorSeverity.CRITICAL,
    ErrorCode.E010_FEATURE_WITHOUT_REPORT_VALUE: ErrorSeverity.LOW,
}

# Default suggestions for each error code
ERROR_CODE_SUGGESTIONS = {
    ErrorCode.E001_ARTIFACT_NOT_REGISTERED: (
        "Add YAML frontmatter to markdown files or register in artifact_registry.yaml. "
        "Required fields: artifact_id, primary_domain, artifact_type, lifecycle_status."
    ),
    ErrorCode.E002_INVALID_DOMAIN_ASSIGNMENT: (
        "Check domain_registry.yaml for allowed_artifact_types per domain. "
        "Reassign the artifact to a domain that supports its type."
    ),
    ErrorCode.E003_INVALID_LIFECYCLE_TRANSITION: (
        "Check lifecycle_state_machine.yaml for valid transitions. "
        "Only transitions defined in the state machine are allowed."
    ),
    ErrorCode.E004_DOMAIN_BOUNDARY_VIOLATION: (
        "Only domains listed in allowed_writers can modify this artifact. "
        "Request write permission from the primary domain owner."
    ),
    ErrorCode.E005_SSOT_CONFLICT_DETECTED: (
        "Only one canonical SSOT is allowed per topic. "
        "Mark one as canonical and others as derived or implementation."
    ),
    ErrorCode.E006_MISSING_REQUIRED_METADATA: (
        "Add the missing required fields: artifact_id, primary_domain, "
        "artifact_type, lifecycle_status, created_date, last_modified."
    ),
    ErrorCode.E007_DEPRECATED_ARTIFACT_MODIFICATION: (
        "Deprecated artifacts cannot be modified except for metadata updates. "
        "Create a new artifact or revert the deprecated status first."
    ),
    ErrorCode.E008_AUTHORITY_CHAIN_VIOLATION: (
        "Follow the authority chain: SIGNALS -> SEMANTICS -> REASONING -> REPORT. "
        "Each domain can only create meaning within its authority level."
    ),
    ErrorCode.E009_FORBIDDEN_CLOUD_PROVIDER_REFERENCE: (
        "Only Google Cloud Platform and Google Sheets API are allowed. "
        "Remove references to AWS, Supabase, or Azure services."
    ),
    ErrorCode.E010_FEATURE_WITHOUT_REPORT_VALUE: (
        "Every feature must answer: 'How does this improve the report?' "
        "Defer features that do not directly improve report quality."
    ),
}


@dataclass
class ValidationError:
    """
    Structured validation error for commit gate failures.
    
    Provides machine-readable error codes, human-readable messages,
    and actionable suggestions for resolution.
    
    In FAST LANE phase (observability mode), errors are downgraded to warnings.
    In post-MVP phase (enforcement mode), critical/high errors block commits.
    """
    
    gate_name: str  # Which gate failed (e.g., "Gate 1: Registration")
    artifact_id: str  # Affected artifact identifier
    error_code: str  # Machine-readable error code (E001-E010)
    error_message: str  # Human-readable description of the failure
    suggestion: str  # Actionable resolution guidance
    severity: str  # "critical" | "high" | "medium" | "low"
    enforcement_mode: str  # "blocking" | "warning"
    
    def is_blocking(self) -> bool:
        """Check if this error should block the commit"""
        return self.enforcement_mode == EnforcementMode.BLOCKING
    
    def format_error(self) -> str:
        """
        Format error as a human-readable message with actionable guidance.
        
        Returns:
            Formatted multi-line error string with icon, context, and suggestion.
        """
        severity_icon = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
        }.get(self.severity, "⚪")
        
        mode_label = "BLOCKING" if self.is_blocking() else "WARNING"
        
        lines = [
            f"{severity_icon} [{self.error_code}] {self.gate_name} ({mode_label})",
            f"",
            f"  Artifact: {self.artifact_id}",
            f"  Error:    {self.error_message}",
            f"",
            f"  Suggestion: {self.suggestion}",
        ]
        return "\n".join(lines)
    
    def __str__(self) -> str:
        """Short string representation for logging"""
        return f"[{self.error_code}] {self.artifact_id}: {self.error_message}"
    
    @staticmethod
    def from_error_code(
        gate_name: str,
        artifact_id: str,
        error_code: ErrorCode,
        error_message: Optional[str] = None,
        suggestion: Optional[str] = None,
        severity: Optional[str] = None,
        enforcement_mode: str = EnforcementMode.WARNING,
    ) -> "ValidationError":
        """
        Create a ValidationError from a standard error code with defaults.
        
        Uses default description, suggestion, and severity from the error code
        definitions unless explicitly overridden.
        
        Args:
            gate_name: Which validation gate generated this error
            artifact_id: The affected artifact identifier
            error_code: Standard error code (E001-E010)
            error_message: Override default error message (optional)
            suggestion: Override default suggestion (optional)
            severity: Override default severity (optional)
            enforcement_mode: "blocking" or "warning" (defaults to "warning" for FAST LANE)
        
        Returns:
            Configured ValidationError instance
        """
        resolved_message = error_message or ERROR_CODE_DESCRIPTIONS.get(
            error_code, "Unknown validation error"
        )
        resolved_suggestion = suggestion or ERROR_CODE_SUGGESTIONS.get(
            error_code, "Review the domainization documentation for guidance."
        )
        resolved_severity = severity or ERROR_CODE_SEVERITIES.get(
            error_code, ErrorSeverity.MEDIUM
        ).value
        
        return ValidationError(
            gate_name=gate_name,
            artifact_id=artifact_id,
            error_code=error_code.value,
            error_message=resolved_message,
            suggestion=resolved_suggestion,
            severity=resolved_severity,
            enforcement_mode=enforcement_mode,
        )


def create_registration_error(
    artifact_id: str,
    file_path: str,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E001 error for unregistered artifacts"""
    return ValidationError.from_error_code(
        gate_name="Gate 1: Artifact Registration",
        artifact_id=artifact_id or file_path,
        error_code=ErrorCode.E001_ARTIFACT_NOT_REGISTERED,
        error_message=f"Artifact '{file_path}' is not registered in the domainization system",
        enforcement_mode=enforcement_mode,
    )


def create_invalid_domain_error(
    artifact_id: str,
    domain_id: str,
    artifact_type: str,
    valid_domains: Optional[list] = None,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E002 error for invalid domain assignments"""
    message = f"Domain '{domain_id}' cannot own artifact type '{artifact_type}'"
    suggestion = ERROR_CODE_SUGGESTIONS[ErrorCode.E002_INVALID_DOMAIN_ASSIGNMENT]
    if valid_domains:
        suggestion = f"Valid domains for {artifact_type}: {', '.join(valid_domains)}. " + suggestion
    
    return ValidationError.from_error_code(
        gate_name="Gate 2: Domain Assignment",
        artifact_id=artifact_id,
        error_code=ErrorCode.E002_INVALID_DOMAIN_ASSIGNMENT,
        error_message=message,
        suggestion=suggestion,
        enforcement_mode=enforcement_mode,
    )


def create_invalid_lifecycle_error(
    artifact_id: str,
    from_state: str,
    to_state: str,
    allowed_transitions: Optional[list] = None,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E003 error for invalid lifecycle transitions"""
    message = f"Invalid lifecycle transition: {from_state} -> {to_state}"
    suggestion = ERROR_CODE_SUGGESTIONS[ErrorCode.E003_INVALID_LIFECYCLE_TRANSITION]
    if allowed_transitions:
        suggestion = f"Valid transitions from '{from_state}': {', '.join(allowed_transitions)}. " + suggestion
    
    return ValidationError.from_error_code(
        gate_name="Gate 3: Lifecycle Validation",
        artifact_id=artifact_id,
        error_code=ErrorCode.E003_INVALID_LIFECYCLE_TRANSITION,
        error_message=message,
        suggestion=suggestion,
        enforcement_mode=enforcement_mode,
    )


def create_boundary_violation_error(
    artifact_id: str,
    modifier_domain: str,
    primary_domain: str,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E004 error for domain boundary violations"""
    message = f"Domain '{modifier_domain}' cannot modify artifact owned by '{primary_domain}'"
    
    return ValidationError.from_error_code(
        gate_name="Gate 4: Boundary Enforcement",
        artifact_id=artifact_id,
        error_code=ErrorCode.E004_DOMAIN_BOUNDARY_VIOLATION,
        error_message=message,
        enforcement_mode=enforcement_mode,
    )


def create_ssot_conflict_error(
    artifact_id: str,
    topic: str,
    conflicting_artifact_id: str,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E005 error for SSOT conflicts"""
    message = f"SSOT conflict: Multiple canonical documents for topic '{topic}'"
    suggestion = (
        f"Mark one as canonical, others as derived. "
        f"Conflicting artifact: {conflicting_artifact_id}"
    )
    
    return ValidationError.from_error_code(
        gate_name="Gate 5: SSOT Consistency",
        artifact_id=artifact_id,
        error_code=ErrorCode.E005_SSOT_CONFLICT_DETECTED,
        error_message=message,
        suggestion=suggestion,
        enforcement_mode=enforcement_mode,
    )


def create_missing_metadata_error(
    artifact_id: str,
    missing_fields: Optional[list] = None,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E006 error for missing required metadata"""
    message = "Required metadata fields are missing"
    suggestion = ERROR_CODE_SUGGESTIONS[ErrorCode.E006_MISSING_REQUIRED_METADATA]
    if missing_fields:
        message = f"Missing required metadata fields: {', '.join(missing_fields)}"
    
    return ValidationError.from_error_code(
        gate_name="Gate 1: Artifact Registration",
        artifact_id=artifact_id,
        error_code=ErrorCode.E006_MISSING_REQUIRED_METADATA,
        error_message=message,
        suggestion=suggestion,
        enforcement_mode=enforcement_mode,
    )


def create_deprecated_modification_error(
    artifact_id: str,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E007 error for deprecated artifact modification"""
    message = f"Cannot modify deprecated artifact '{artifact_id}'"
    
    return ValidationError.from_error_code(
        gate_name="Gate 3: Lifecycle Validation",
        artifact_id=artifact_id,
        error_code=ErrorCode.E007_DEPRECATED_ARTIFACT_MODIFICATION,
        error_message=message,
        enforcement_mode=enforcement_mode,
    )


def create_authority_chain_error(
    artifact_id: str,
    modifier_domain: str,
    target_domain: str,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E008 error for authority chain violations"""
    message = (
        f"Authority chain violation: '{modifier_domain}' cannot create meaning "
        f"in '{target_domain}' domain"
    )
    
    return ValidationError.from_error_code(
        gate_name="Gate 4: Boundary Enforcement",
        artifact_id=artifact_id,
        error_code=ErrorCode.E008_AUTHORITY_CHAIN_VIOLATION,
        error_message=message,
        enforcement_mode=enforcement_mode,
    )


def create_forbidden_provider_error(
    artifact_id: str,
    provider: str,
    file_path: str,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E009 error for forbidden cloud provider references"""
    message = f"Forbidden cloud provider '{provider}' referenced in '{file_path}'"
    
    return ValidationError.from_error_code(
        gate_name="Gate 2: Domain Assignment",
        artifact_id=artifact_id,
        error_code=ErrorCode.E009_FORBIDDEN_CLOUD_PROVIDER_REFERENCE,
        error_message=message,
        enforcement_mode=enforcement_mode,
    )


def create_no_report_value_error(
    artifact_id: str,
    feature_name: str,
    enforcement_mode: str = EnforcementMode.WARNING,
) -> ValidationError:
    """Create an E010 error for features without report value"""
    message = f"Feature '{feature_name}' does not demonstrate direct report value"
    
    return ValidationError.from_error_code(
        gate_name="Gate 5: SSOT Consistency",
        artifact_id=artifact_id,
        error_code=ErrorCode.E010_FEATURE_WITHOUT_REPORT_VALUE,
        error_message=message,
        enforcement_mode=enforcement_mode,
    )
