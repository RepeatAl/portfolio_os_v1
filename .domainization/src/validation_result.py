"""
Validation result schema for observers
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ValidationWarning:
    """Represents a validation warning (non-blocking)"""
    
    observer_name: str  # Which observer generated this warning
    artifact_id: Optional[str]  # Affected artifact (None if file not registered)
    file_path: Optional[str]  # File path that triggered warning
    warning_code: str  # Machine-readable warning code
    warning_message: str  # Human-readable description
    suggestion: str  # Actionable resolution guidance
    severity: str  # "critical" | "high" | "medium" | "low"
    
    def __str__(self) -> str:
        """Format warning for display"""
        severity_icon = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }.get(self.severity, '⚪')
        
        location = self.artifact_id or self.file_path or 'unknown'
        return f"{severity_icon} [{self.observer_name}] {location}: {self.warning_message}\n   Suggestion: {self.suggestion}"


@dataclass
class ValidationResult:
    """Result from running validation observers"""
    
    observer_name: str
    warnings: List[ValidationWarning]
    execution_time_ms: float
    
    def has_warnings(self) -> bool:
        """Check if any warnings were generated"""
        return len(self.warnings) > 0
    
    def get_critical_warnings(self) -> List[ValidationWarning]:
        """Get only critical severity warnings"""
        return [w for w in self.warnings if w.severity == 'critical']
    
    def get_high_warnings(self) -> List[ValidationWarning]:
        """Get only high severity warnings"""
        return [w for w in self.warnings if w.severity == 'high']
    
    def get_medium_warnings(self) -> List[ValidationWarning]:
        """Get only medium severity warnings"""
        return [w for w in self.warnings if w.severity == 'medium']
    
    def get_low_warnings(self) -> List[ValidationWarning]:
        """Get only low severity warnings"""
        return [w for w in self.warnings if w.severity == 'low']


# Warning codes
class WarningCodes:
    """Standard warning codes for observers"""
    
    # Registration warnings (W001-W099)
    W001_UNREGISTERED_ARTIFACT = "W001"
    W002_MISSING_METADATA = "W002"
    W003_INVALID_METADATA_SCHEMA = "W003"
    W004_INCOMPLETE_METADATA = "W004"
    
    # Domain assignment warnings (W100-W199)
    W100_INVALID_DOMAIN = "W100"
    W101_DOMAIN_CANNOT_OWN_TYPE = "W101"
    W102_MISSING_DOMAIN = "W102"
    
    # Lifecycle warnings (W200-W299)
    W200_INVALID_LIFECYCLE_TRANSITION = "W200"
    W201_DEPRECATED_MODIFICATION = "W201"
    W202_MISSING_LIFECYCLE_STATUS = "W202"
    W203_INVALID_LIFECYCLE_STATE = "W203"
    
    # Boundary warnings (W300-W399)
    W300_AUTHORITY_CHAIN_VIOLATION = "W300"
    W301_SIGNALS_WRITES_NON_SIGNAL = "W301"
    W302_SEMANTICS_WRITES_NON_SEMANTIC = "W302"
    W303_REASONING_WRITES_NON_REASONING = "W303"
    W304_REPORT_WRITES_BUSINESS_LOGIC = "W304"
    W305_CROSS_DOMAIN_WRITE = "W305"
    
    # SSOT warnings (W400-W499)
    W400_MULTIPLE_CANONICAL_SSOT = "W400"
    W401_MISSING_SSOT_REFERENCE = "W401"
    W402_INVALID_SSOT_RELATIONSHIP = "W402"
    W403_ORPHANED_DERIVED_DOCUMENT = "W403"
    
    # Cloud provider warnings (W500-W599)
    W500_FORBIDDEN_CLOUD_PROVIDER = "W500"
    W501_AWS_REFERENCE_DETECTED = "W501"
    W502_SUPABASE_REFERENCE_DETECTED = "W502"
    W503_AZURE_REFERENCE_DETECTED = "W503"

    # Report value warnings (W600-W699)
    W600_MISSING_REPORT_VALUE = "W600"
    W601_INVALID_REPORT_VALUE_CATEGORY = "W601"
    W602_SPECULATIVE_REPORT_VALUE = "W602"
    W603_INFRASTRUCTURE_WITHOUT_REPORT_VALUE = "W603"
    W604_REPORT_VALUE_FORMAT_ERROR = "W604"

    # Runtime flow warnings (W700-W799)
    W700_FORBIDDEN_RUNTIME_FLOW = "W700"
    W701_AUTHORITY_CHAIN_SKIP = "W701"
    W702_BACKWARD_AUTHORITY_FLOW = "W702"
    W703_SURFACE_TO_CORE_FLOW = "W703"
    W704_MEANING_OUTSIDE_AUTHORITY = "W704"

    # Registration enforcement warnings (W800-W899)
    W800_REGISTRATION_REQUIRED = "W800"
    W801_UNREGISTERED_COUNT_INCREASE = "W801"
    W802_SIMPLIFIED_REGISTRATION_MISSING = "W802"
