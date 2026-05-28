"""
Report Value Detection Framework

Detects whether artifacts have valid report value justification.
Validates that claimed report value matches one of the 10 allowed categories.
Identifies speculative/indirect claims and infrastructure-heavy artifacts
without report justification. All detection operates in WARNING mode only.

Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set


# The 10 allowed report value categories (Requirement 12.5)
ALLOWED_REPORT_VALUE_CATEGORIES = [
    "semantic_interpretation",
    "pm_reasoning",
    "concentration_explanation",
    "dependency_explanation",
    "scenario_interpretation",
    "confidence_explanation",
    "action_space_clarity",
    "multilingual_rendering",
    "traceability",
    "user_understanding",
]

# Keywords that indicate speculative or indirect report value (Requirement 12.4)
SPECULATIVE_KEYWORDS = [
    "might improve",
    "could help",
    "potentially",
    "in the future",
    "eventually",
    "indirectly",
    "may contribute",
    "possibly",
    "theoretically",
    "long-term",
    "someday",
    "aspirational",
]

# Keywords that indicate infrastructure-heavy artifacts without report value
INFRASTRUCTURE_KEYWORDS = [
    "infrastructure",
    "deployment",
    "ci/cd",
    "pipeline",
    "devops",
    "monitoring",
    "logging",
    "caching",
    "scaling",
    "load balancing",
    "orchestration",
    "containerization",
]


@dataclass
class ReportValueAssessment:
    """Assessment result for a single artifact's report value"""

    artifact_id: Optional[str]
    file_path: Optional[str]
    has_report_value: bool
    report_value_category: Optional[str] = None
    is_speculative: bool = False
    is_infrastructure_heavy: bool = False
    justification: Optional[str] = None
    issues: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if the report value claim is valid (present, non-speculative, allowed category)"""
        return (
            self.has_report_value
            and not self.is_speculative
            and self.report_value_category in ALLOWED_REPORT_VALUE_CATEGORIES
        )

    def summary(self) -> str:
        """Generate human-readable summary of assessment"""
        if self.is_valid:
            return (
                f"Valid report value: {self.report_value_category} "
                f"for {self.artifact_id or self.file_path}"
            )
        if not self.has_report_value:
            return f"No report value declared for {self.artifact_id or self.file_path}"
        if self.is_speculative:
            return (
                f"Speculative report value for {self.artifact_id or self.file_path}: "
                f"{self.justification}"
            )
        return f"Invalid report value for {self.artifact_id or self.file_path}: {', '.join(self.issues)}"


@dataclass
class ReportValueHealthScore:
    """Health score for report-value coverage across artifacts"""

    total_artifacts: int = 0
    artifacts_with_report_value: int = 0
    artifacts_with_valid_report_value: int = 0
    artifacts_speculative: int = 0
    artifacts_infrastructure_heavy: int = 0
    artifacts_missing_report_value: int = 0
    category_distribution: Dict[str, int] = field(default_factory=dict)

    @property
    def coverage_percentage(self) -> float:
        """Percentage of artifacts with any report value declared"""
        if self.total_artifacts == 0:
            return 0.0
        return (self.artifacts_with_report_value / self.total_artifacts) * 100.0

    @property
    def valid_percentage(self) -> float:
        """Percentage of artifacts with valid (non-speculative, allowed category) report value"""
        if self.total_artifacts == 0:
            return 0.0
        return (self.artifacts_with_valid_report_value / self.total_artifacts) * 100.0

    @property
    def infrastructure_drift_percentage(self) -> float:
        """Percentage of artifacts that are infrastructure-heavy without report value"""
        if self.total_artifacts == 0:
            return 0.0
        return (self.artifacts_infrastructure_heavy / self.total_artifacts) * 100.0

    def summary(self) -> str:
        """Generate human-readable health score summary"""
        return (
            f"Report Value Health: {self.valid_percentage:.1f}% valid "
            f"({self.artifacts_with_valid_report_value}/{self.total_artifacts}), "
            f"{self.coverage_percentage:.1f}% declared, "
            f"{self.infrastructure_drift_percentage:.1f}% infrastructure drift"
        )


class ReportValueDetector:
    """
    Detects and validates report value justification for artifacts.

    Checks artifact metadata for report_value field, validates that claimed
    report value matches one of the 10 allowed categories, detects speculative
    or indirect claims, and generates report-value health scores.

    All detection operates in WARNING mode only (no blocking).

    Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7
    """

    def __init__(self):
        """Initialize the report value detector"""
        self.allowed_categories = list(ALLOWED_REPORT_VALUE_CATEGORIES)
        self.speculative_keywords = list(SPECULATIVE_KEYWORDS)
        self.infrastructure_keywords = list(INFRASTRUCTURE_KEYWORDS)

    def get_allowed_categories(self) -> List[str]:
        """
        Return the 10 allowed report value categories.

        Returns:
            List of allowed report value category strings

        Requirement: 12.5
        """
        return list(self.allowed_categories)

    def assess_artifact(self, artifact_metadata: dict) -> ReportValueAssessment:
        """
        Assess a single artifact's report value justification.

        Checks the artifact metadata for a 'report_value' field and validates:
        - Whether report value is declared (Requirement 12.1)
        - Whether the category is one of the 10 allowed (Requirement 12.5)
        - Whether the justification is speculative/indirect (Requirement 12.4)
        - Whether the artifact is infrastructure-heavy without report value (Requirement 12.7)

        Args:
            artifact_metadata: Dictionary containing artifact metadata.
                Expected keys: artifact_id, file_path, primary_domain, artifact_type,
                and optionally report_value (dict with 'category' and 'justification')

        Returns:
            ReportValueAssessment with validation results
        """
        artifact_id = artifact_metadata.get("artifact_id")
        file_path = artifact_metadata.get("file_path")
        report_value = artifact_metadata.get("report_value")

        # Check if report_value field exists
        if "report_value" not in artifact_metadata or report_value is None:
            is_infra = self._is_infrastructure_heavy(artifact_metadata)
            return ReportValueAssessment(
                artifact_id=artifact_id,
                file_path=file_path,
                has_report_value=False,
                is_infrastructure_heavy=is_infra,
                issues=["No report_value field in artifact metadata"],
            )

        # Extract category and justification
        category = None
        justification = None

        if isinstance(report_value, dict):
            category = report_value.get("category", "").strip().lower()
            justification = report_value.get("justification", "").strip()
        elif isinstance(report_value, str):
            # Simple string value treated as category
            category = report_value.strip().lower()
            justification = ""
        else:
            return ReportValueAssessment(
                artifact_id=artifact_id,
                file_path=file_path,
                has_report_value=False,
                issues=["report_value field has invalid format (expected dict or string)"],
            )

        issues = []

        # Validate category is in allowed list (Requirement 12.5)
        if category not in self.allowed_categories:
            issues.append(
                f"Category '{category}' is not in allowed report value categories. "
                f"Allowed: {', '.join(self.allowed_categories)}"
            )

        # Check for speculative/indirect justification (Requirement 12.4)
        is_speculative = self._is_speculative_claim(justification)
        if is_speculative:
            issues.append(
                "Report value justification appears speculative or indirect. "
                "Report value must be measurable and direct (Requirement 12.3)"
            )

        # Check infrastructure-heavy without valid report value
        is_infra = self._is_infrastructure_heavy(artifact_metadata)

        return ReportValueAssessment(
            artifact_id=artifact_id,
            file_path=file_path,
            has_report_value=True,
            report_value_category=category,
            is_speculative=is_speculative,
            is_infrastructure_heavy=is_infra,
            justification=justification,
            issues=issues,
        )

    def assess_artifacts(self, artifacts: List[dict]) -> List[ReportValueAssessment]:
        """
        Assess multiple artifacts for report value justification.

        Args:
            artifacts: List of artifact metadata dictionaries

        Returns:
            List of ReportValueAssessment objects
        """
        return [self.assess_artifact(artifact) for artifact in artifacts]

    def generate_health_score(self, artifacts: List[dict]) -> ReportValueHealthScore:
        """
        Generate a report-value health score across all artifacts.

        Calculates coverage percentage, valid percentage, and infrastructure
        drift percentage.

        Args:
            artifacts: List of artifact metadata dictionaries

        Returns:
            ReportValueHealthScore with aggregated metrics
        """
        assessments = self.assess_artifacts(artifacts)
        score = ReportValueHealthScore(total_artifacts=len(artifacts))

        category_counts: Dict[str, int] = {}

        for assessment in assessments:
            if assessment.has_report_value:
                score.artifacts_with_report_value += 1
                if assessment.is_valid:
                    score.artifacts_with_valid_report_value += 1
                    # Track category distribution
                    cat = assessment.report_value_category
                    if cat:
                        category_counts[cat] = category_counts.get(cat, 0) + 1
                if assessment.is_speculative:
                    score.artifacts_speculative += 1
            else:
                score.artifacts_missing_report_value += 1

            if assessment.is_infrastructure_heavy and not assessment.is_valid:
                score.artifacts_infrastructure_heavy += 1

        score.category_distribution = category_counts
        return score

    def detect_missing_report_value(self, artifacts: List[dict]) -> List[dict]:
        """
        Identify artifacts that are missing report value justification.

        Requirement 12.2: If no report value is identified, the feature shall be deferred.

        Args:
            artifacts: List of artifact metadata dictionaries

        Returns:
            List of artifact metadata dicts that lack report value
        """
        missing = []
        for artifact in artifacts:
            report_value = artifact.get("report_value")
            if report_value is None:
                missing.append(artifact)
        return missing

    def detect_infrastructure_without_report_value(self, artifacts: List[dict]) -> List[dict]:
        """
        Identify infrastructure-heavy artifacts without report value justification.

        Requirement 12.7: If a feature adds complexity without report benefit,
        it shall be rejected.

        Args:
            artifacts: List of artifact metadata dictionaries

        Returns:
            List of infrastructure-heavy artifact dicts without valid report value
        """
        infra_without_value = []
        for artifact in artifacts:
            assessment = self.assess_artifact(artifact)
            if assessment.is_infrastructure_heavy and not assessment.is_valid:
                infra_without_value.append(artifact)
        return infra_without_value

    def _is_speculative_claim(self, justification: str) -> bool:
        """
        Check if a report value justification is speculative or indirect.

        Requirement 12.4: If report value is speculative or indirect,
        the feature shall be rejected.

        Args:
            justification: The justification text to check

        Returns:
            True if the justification contains speculative language
        """
        if not justification:
            return False

        justification_lower = justification.lower()
        for keyword in self.speculative_keywords:
            if keyword in justification_lower:
                return True
        return False

    def _is_infrastructure_heavy(self, artifact_metadata: dict) -> bool:
        """
        Check if an artifact is infrastructure-heavy based on metadata.

        Looks at artifact_type, primary_domain, file_path, and description
        for infrastructure indicators.

        Args:
            artifact_metadata: Dictionary containing artifact metadata

        Returns:
            True if the artifact appears to be infrastructure-focused
        """
        # Check artifact type
        artifact_type = artifact_metadata.get("artifact_type", "").lower()
        if artifact_type in ("config", "runtime", "steering"):
            return True

        # Check primary domain
        primary_domain = artifact_metadata.get("primary_domain", "").upper()
        if primary_domain in ("DEPLOY", "ARCH"):
            return True

        # Check file path for infrastructure indicators
        file_path = artifact_metadata.get("file_path", "").lower()
        for keyword in self.infrastructure_keywords:
            if keyword.replace(" ", "_") in file_path or keyword.replace(" ", "-") in file_path:
                return True

        # Check description for infrastructure indicators
        description = artifact_metadata.get("description", "")
        if description:
            description_lower = description.lower()
            for keyword in self.infrastructure_keywords:
                if keyword in description_lower:
                    return True

        return False

    def is_valid_category(self, category: str) -> bool:
        """
        Check if a category string is one of the allowed report value categories.

        Args:
            category: Category string to validate

        Returns:
            True if the category is in the allowed list
        """
        return category.strip().lower() in self.allowed_categories

    def validate_registry_file(
        self, registry_path: str = ".domainization/artifact_registry.yaml"
    ) -> Dict[str, object]:
        """
        Load and validate the artifact registry YAML file for report_value compliance.

        Validates every artifact in the registry against the 10 accepted categories,
        flags speculative language, and reports missing/empty report_value fields.

        This is the canonical wiring point between the Report_Value_Detector and
        the artifact registry file on disk.

        Args:
            registry_path: Path to the artifact_registry.yaml file

        Returns:
            Dictionary with validation results:
                - total_artifacts: int
                - valid_count: int
                - missing_report_value: list of artifact_ids missing the field
                - invalid_categories: list of (artifact_id, category) tuples
                - speculative_justifications: list of (artifact_id, keyword) tuples
                - empty_fields: list of artifact_ids with empty category or justification
                - coverage_percentage: float
                - is_compliant: bool (True if 100% valid coverage)

        Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6
        """
        from pathlib import Path

        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML is required for registry validation")

        registry_file = Path(registry_path)
        if not registry_file.exists():
            raise FileNotFoundError(f"Registry file not found: {registry_path}")

        with open(registry_file, "r") as f:
            data = yaml.safe_load(f)

        artifacts = data.get("artifacts", [])
        if not artifacts:
            return {
                "total_artifacts": 0,
                "valid_count": 0,
                "missing_report_value": [],
                "invalid_categories": [],
                "speculative_justifications": [],
                "empty_fields": [],
                "coverage_percentage": 0.0,
                "is_compliant": True,
            }

        missing_report_value: List[str] = []
        invalid_categories: List[tuple] = []
        speculative_justifications: List[tuple] = []
        empty_fields: List[str] = []
        valid_count = 0

        for artifact in artifacts:
            artifact_id = artifact.get("artifact_id", "UNKNOWN")
            report_value = artifact.get("report_value")

            # Check missing report_value (Requirement 4.5)
            if report_value is None:
                missing_report_value.append(artifact_id)
                continue

            # Extract category and justification
            category = ""
            justification = ""
            if isinstance(report_value, dict):
                category = report_value.get("category", "").strip()
                justification = report_value.get("justification", "").strip()
            elif isinstance(report_value, str):
                category = report_value.strip()

            # Check empty fields (Requirement 4.5)
            if not category or not justification:
                empty_fields.append(artifact_id)
                continue

            # Validate category against 10 accepted categories (Requirement 4.2, 4.3)
            if category.lower() not in self.allowed_categories:
                invalid_categories.append((artifact_id, category))
                continue

            # Check speculative language (Requirement 4.4)
            if self._is_speculative_claim(justification):
                for keyword in self.speculative_keywords:
                    if keyword in justification.lower():
                        speculative_justifications.append((artifact_id, keyword))
                        break
                continue

            valid_count += 1

        total = len(artifacts)
        coverage = (total - len(missing_report_value)) / total * 100.0 if total > 0 else 0.0
        is_compliant = (
            len(missing_report_value) == 0
            and len(invalid_categories) == 0
            and len(speculative_justifications) == 0
            and len(empty_fields) == 0
        )

        return {
            "total_artifacts": total,
            "valid_count": valid_count,
            "missing_report_value": missing_report_value,
            "invalid_categories": invalid_categories,
            "speculative_justifications": speculative_justifications,
            "empty_fields": empty_fields,
            "coverage_percentage": coverage,
            "is_compliant": is_compliant,
        }
