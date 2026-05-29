"""Ontology Growth Observer — observation engine for governance concept tracking.

Measures, reports, and trends governance ontology growth over time.
Tracks artifact types, governance dimensions (domains), severity levels,
and total governance concepts.

This module is an OBSERVATION ENGINE only:
- It MUST: measure, report, trend
- It MUST NOT: block, reject, enforce

No pre-registration blocking. Observation only.

CTO DIRECTIVE: This is an observation engine, not a constraint enforcer.

Requirements: 39.1, 39.2, 39.3, 39.4
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class OntologyGrowthObserver:
    """Observation engine for governance ontology growth.

    Reads from:
    - .domainization/artifact_registry.yaml (artifact types and counts)
    - .domainization/domain_registry.yaml (governance dimensions / domains)
    - runtime/severity_taxonomy.py (severity levels)
    - governance/ modules (governance concepts)

    This class MUST:
    - Measure current ontology counts
    - Report structured growth data
    - Trend against previous measurements

    This class MUST NOT:
    - Block any operation
    - Reject any registration
    - Enforce any constraint
    """

    def __init__(self, base_path: str) -> None:
        """Initialize OntologyGrowthObserver with project root path.

        Args:
            base_path: Absolute path to the project root directory.
        """
        self.base_path = Path(base_path)
        self._artifact_registry_path = (
            self.base_path / ".domainization" / "artifact_registry.yaml"
        )
        self._domain_registry_path = (
            self.base_path / ".domainization" / "domain_registry.yaml"
        )

    def measure(self) -> dict[str, Any]:
        """Measure current ontology counts.

        Returns:
            Dictionary with current counts:
            - artifact_type_count: number of unique artifact types
            - governance_dimension_count: number of domains
            - severity_level_count: number of severity levels
            - total_concepts: sum of all tracked concepts
            - timestamp: ISO 8601 measurement timestamp
        """
        artifact_type_count = self._count_artifact_types()
        governance_dimension_count = self._count_governance_dimensions()
        severity_level_count = self._count_severity_levels()
        total_concepts = (
            artifact_type_count + governance_dimension_count + severity_level_count
        )

        return {
            "artifact_type_count": artifact_type_count,
            "governance_dimension_count": governance_dimension_count,
            "severity_level_count": severity_level_count,
            "total_concepts": total_concepts,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def report(self) -> dict[str, Any]:
        """Generate structured observability report.

        Returns:
            Dictionary with:
            - counts: current measurement data
            - growth_rate: None (no previous data available in single report)
            - recommendation: string assessment of current state
        """
        counts = self.measure()
        recommendation = self._compute_recommendation(counts["total_concepts"])

        return {
            "counts": counts,
            "growth_rate": None,
            "recommendation": recommendation,
        }

    def trend(self, previous_report: dict[str, Any]) -> dict[str, Any]:
        """Compare current measurement with a previous measurement.

        Args:
            previous_report: A previous report dict (from report() or measure())
                containing at minimum a 'total_concepts' field or a 'counts'
                dict with 'total_concepts'.

        Returns:
            Dictionary with:
            - current: current measurement
            - previous: previous measurement data
            - growth_rate: percentage change from previous
            - recommendation: string assessment based on growth
            - deltas: per-dimension change details
        """
        current = self.measure()

        # Extract previous counts — support both flat measure() and nested report()
        if "counts" in previous_report:
            previous_counts = previous_report["counts"]
        else:
            previous_counts = previous_report

        previous_total = previous_counts.get("total_concepts", 0)
        current_total = current["total_concepts"]

        # Compute growth rate as percentage change
        if previous_total == 0:
            growth_rate = 100.0 if current_total > 0 else 0.0
        else:
            growth_rate = (
                (current_total - previous_total) / previous_total
            ) * 100.0

        # Compute per-dimension deltas
        deltas = {
            "artifact_type_delta": (
                current["artifact_type_count"]
                - previous_counts.get("artifact_type_count", 0)
            ),
            "governance_dimension_delta": (
                current["governance_dimension_count"]
                - previous_counts.get("governance_dimension_count", 0)
            ),
            "severity_level_delta": (
                current["severity_level_count"]
                - previous_counts.get("severity_level_count", 0)
            ),
            "total_concept_delta": current_total - previous_total,
        }

        recommendation = self._compute_recommendation_from_growth(growth_rate)

        return {
            "current": current,
            "previous": previous_counts,
            "growth_rate": growth_rate,
            "recommendation": recommendation,
            "deltas": deltas,
        }

    def _count_artifact_types(self) -> int:
        """Count unique artifact types from the artifact registry.

        Returns:
            Number of unique artifact types. 0 on failure.
        """
        if not self._artifact_registry_path.exists():
            logger.warning(
                "Artifact registry not found at %s — artifact type count unavailable",
                self._artifact_registry_path,
            )
            return 0

        try:
            with open(self._artifact_registry_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data is None:
                return 0

            # Handle both list format and dict with 'artifacts' key
            artifacts: list[dict[str, Any]] = []
            if isinstance(data, dict) and "artifacts" in data:
                artifacts = data["artifacts"] or []
            elif isinstance(data, list):
                artifacts = data
            else:
                return 0

            # Collect unique artifact types
            artifact_types: set[str] = set()
            for artifact in artifacts:
                if isinstance(artifact, dict) and "artifact_type" in artifact:
                    artifact_types.add(artifact["artifact_type"])

            return len(artifact_types)

        except (yaml.YAMLError, OSError) as exc:
            logger.warning(
                "Failed to read artifact registry: %s — artifact type count unavailable",
                exc,
            )
            return 0

    def _count_governance_dimensions(self) -> int:
        """Count governance dimensions (domains) from the domain registry.

        Returns:
            Number of domains. 0 on failure.
        """
        if not self._domain_registry_path.exists():
            logger.warning(
                "Domain registry not found at %s — dimension count unavailable",
                self._domain_registry_path,
            )
            return 0

        try:
            with open(self._domain_registry_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data is None:
                return 0

            # Handle dict with 'domains' key
            if isinstance(data, dict) and "domains" in data:
                domains = data["domains"]
                if isinstance(domains, list):
                    return len(domains)

            return 0

        except (yaml.YAMLError, OSError) as exc:
            logger.warning(
                "Failed to read domain registry: %s — dimension count unavailable",
                exc,
            )
            return 0

    def _count_severity_levels(self) -> int:
        """Count severity levels from the severity taxonomy.

        Imports from runtime.severity_taxonomy to get the canonical count.
        Falls back to reading the file if import fails.

        Returns:
            Number of severity levels. 0 on failure.
        """
        try:
            from runtime.severity_taxonomy import Severity

            return len(Severity)
        except ImportError:
            logger.warning(
                "Could not import runtime.severity_taxonomy — "
                "attempting file-based count"
            )
            return self._count_severity_levels_from_file()

    def _count_severity_levels_from_file(self) -> int:
        """Count severity levels by reading the severity_taxonomy.py file.

        Fallback when import is not available.

        Returns:
            Number of severity levels found. 0 on failure.
        """
        severity_path = self.base_path / "runtime" / "severity_taxonomy.py"
        if not severity_path.exists():
            return 0

        try:
            content = severity_path.read_text(encoding="utf-8")
            # Count lines matching the IntEnum member pattern (NAME = value)
            count = 0
            in_enum = False
            for line in content.splitlines():
                stripped = line.strip()
                if "class Severity(IntEnum)" in line:
                    in_enum = True
                    continue
                if in_enum:
                    if stripped == "" or stripped.startswith("class "):
                        break
                    if "=" in stripped and not stripped.startswith("#"):
                        count += 1
            return count
        except OSError:
            return 0

    def _compute_recommendation(self, total_concepts: int) -> str:
        """Compute recommendation based on current total concept count.

        This is ADVISORY ONLY — no enforcement, no blocking.

        Args:
            total_concepts: Current total governance concept count.

        Returns:
            Recommendation string.
        """
        if total_concepts <= 30:
            return "stable"
        elif total_concepts <= 50:
            return "growing"
        else:
            return "rapid growth - review needed"

    def _compute_recommendation_from_growth(self, growth_rate: float) -> str:
        """Compute recommendation based on growth rate percentage.

        This is ADVISORY ONLY — no enforcement, no blocking.

        Args:
            growth_rate: Percentage change from previous measurement.

        Returns:
            Recommendation string.
        """
        if growth_rate <= 0.0:
            return "stable"
        elif growth_rate <= 10.0:
            return "stable"
        elif growth_rate <= 25.0:
            return "growing"
        else:
            return "rapid growth - review needed"
