"""Sunset Governance — 4-phase deprecation lifecycle for legacy artifacts.

HARDENING 12 — SUNSET GOVERNANCE: Mandatory deprecation governance fields
prevent artifact zombie sprawl. Legacy briefing files progress through a
deterministic 4-phase sunset model with clear terminal state.

Phase 1 (WARNING_ONLY): deprecated_date set, artifact still generated,
    deprecation warning emitted.
Phase 2 (REPLACEMENT_PATH): warning + replacement_artifact reference
    provided to consumers.
Phase 3 (RUNTIME_DISABLED): artifact generation stops IF
    downstream_dependency_count == 0; continues + CRITICAL warning if
    dependencies remain (sunset-blocked).
Phase 4 (ARCHIVED): lifecycle_status transitions to 'archived',
    artifact frozen.

Validates: Requirements 2.5, 25.1, 25.2, 25.3, 25.4
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Sunset Phase Enum
# ---------------------------------------------------------------------------

class SunsetPhase(StrEnum):
    """4-phase sunset model for deprecated artifacts."""

    WARNING_ONLY = "warning_only"
    REPLACEMENT_PATH = "replacement_path"
    RUNTIME_DISABLED = "runtime_disabled"
    ARCHIVED = "archived"
    # Special state: not yet deprecated
    NOT_DEPRECATED = "not_deprecated"


# ---------------------------------------------------------------------------
# Compatibility Impact Enum
# ---------------------------------------------------------------------------

class CompatibilityImpact(StrEnum):
    """Impact classification for deprecation on downstream consumers."""

    NONE = "none"
    MINOR = "minor"
    BREAKING = "breaking"


# ---------------------------------------------------------------------------
# Deprecation Governance Fields
# ---------------------------------------------------------------------------

@dataclass
class DeprecationGovernance:
    """Optional deprecation governance fields for artifact registry entries.

    These fields annotate artifacts in the deprecation pipeline with
    structured sunset metadata.
    """

    deprecated_date: str | None = None  # ISO 8601 date
    sunset_date: str | None = None  # ISO 8601 date
    replacement_artifact: str | None = None  # artifact_id reference
    deprecation_reason: str | None = None  # max 200 chars
    compatibility_impact: str | None = None  # none | minor | breaking

    def validate(self) -> list[str]:
        """Return list of validation errors. Empty list = valid."""
        errors: list[str] = []

        if self.deprecated_date is not None:
            try:
                date.fromisoformat(self.deprecated_date)
            except (ValueError, TypeError):
                errors.append(
                    f"deprecated_date '{self.deprecated_date}' is not valid ISO 8601"
                )

        if self.sunset_date is not None:
            try:
                date.fromisoformat(self.sunset_date)
            except (ValueError, TypeError):
                errors.append(
                    f"sunset_date '{self.sunset_date}' is not valid ISO 8601"
                )

        if self.deprecation_reason is not None and len(self.deprecation_reason) > 200:
            errors.append(
                f"deprecation_reason exceeds 200 chars ({len(self.deprecation_reason)})"
            )

        if self.compatibility_impact is not None:
            valid_impacts = {e.value for e in CompatibilityImpact}
            if self.compatibility_impact not in valid_impacts:
                errors.append(
                    f"compatibility_impact '{self.compatibility_impact}' not in {sorted(valid_impacts)}"
                )

        # sunset_date must be after deprecated_date if both set
        if self.deprecated_date and self.sunset_date:
            try:
                dep = date.fromisoformat(self.deprecated_date)
                sun = date.fromisoformat(self.sunset_date)
                if sun < dep:
                    errors.append(
                        "sunset_date must be on or after deprecated_date"
                    )
            except (ValueError, TypeError):
                pass  # Already caught above

        return errors


# ---------------------------------------------------------------------------
# Sunset Report Entry
# ---------------------------------------------------------------------------

@dataclass
class SunsetReportEntry:
    """A single entry in the sunset report."""

    artifact_id: str
    phase: SunsetPhase
    deprecated_date: str | None
    sunset_date: str | None
    replacement_artifact: str | None
    deprecation_reason: str | None
    compatibility_impact: str | None
    age_days: int  # Days since deprecated_date
    remaining_days: int | None  # Days until sunset_date (None if no sunset_date)
    downstream_dependency_count: int
    sunset_blocked: bool  # True if at sunset but deps > 0


# ---------------------------------------------------------------------------
# SunsetGovernance Class
# ---------------------------------------------------------------------------

class SunsetGovernance:
    """Implements the 4-phase sunset model for artifact deprecation.

    Reads artifact registry to evaluate sunset phases and produce
    governance reports for deprecated artifacts.
    """

    def __init__(
        self,
        registry_path: str = ".domainization/artifact_registry.yaml",
        reference_date: date | None = None,
    ):
        """Initialize sunset governance.

        Args:
            registry_path: Path to the artifact registry YAML file.
            reference_date: Date to use for phase evaluation. Defaults to today.
        """
        self._registry_path = Path(registry_path)
        self._reference_date = reference_date or date.today()
        self._artifacts: list[dict[str, Any]] = []
        self._load_registry()

    def _load_registry(self) -> None:
        """Load artifact registry from YAML."""
        if not self._registry_path.exists():
            self._artifacts = []
            return

        with open(self._registry_path, "r") as f:
            data = yaml.safe_load(f)

        self._artifacts = data.get("artifacts", []) if data else []

    def _get_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        """Find an artifact by its artifact_id."""
        for artifact in self._artifacts:
            if artifact.get("artifact_id") == artifact_id:
                return artifact
        return None

    def _get_downstream_dependency_count(self, artifact_id: str) -> int:
        """Count how many other artifacts depend on this artifact.

        Scans the registry for artifacts that list this artifact_id
        in their dependencies list.
        """
        count = 0
        for artifact in self._artifacts:
            deps = artifact.get("dependencies", [])
            if deps and artifact_id in deps:
                count += 1
        return count

    def evaluate_sunset_phase(self, artifact_id: str) -> SunsetPhase:
        """Evaluate the current sunset phase for an artifact.

        Phase determination logic:
        - NOT_DEPRECATED: No deprecated_date set
        - WARNING_ONLY: deprecated_date set, no replacement_artifact
        - REPLACEMENT_PATH: deprecated_date set AND replacement_artifact set,
            sunset_date not yet reached
        - RUNTIME_DISABLED: sunset_date reached AND downstream_dependency_count == 0
            (or sunset-blocked if deps > 0)
        - ARCHIVED: lifecycle_status == 'archived'

        Args:
            artifact_id: The artifact_id to evaluate.

        Returns:
            The current SunsetPhase for the artifact.

        Raises:
            ValueError: If artifact_id is not found in the registry.
        """
        artifact = self._get_artifact(artifact_id)
        if artifact is None:
            raise ValueError(f"Artifact '{artifact_id}' not found in registry")

        # Check if already archived
        lifecycle_status = artifact.get("lifecycle_status", "")
        if lifecycle_status == "archived":
            return SunsetPhase.ARCHIVED

        # Get deprecation governance fields
        deprecated_date_str = artifact.get("deprecated_date")
        sunset_date_str = artifact.get("sunset_date")
        replacement_artifact = artifact.get("replacement_artifact")

        # Phase 0: Not deprecated
        if not deprecated_date_str:
            return SunsetPhase.NOT_DEPRECATED

        # Parse dates
        try:
            deprecated_dt = date.fromisoformat(deprecated_date_str)
        except (ValueError, TypeError):
            return SunsetPhase.WARNING_ONLY

        # Check if sunset date has been reached
        sunset_reached = False
        if sunset_date_str:
            try:
                sunset_dt = date.fromisoformat(sunset_date_str)
                sunset_reached = self._reference_date >= sunset_dt
            except (ValueError, TypeError):
                pass

        # Phase 3: RUNTIME_DISABLED — sunset date reached
        if sunset_reached:
            return SunsetPhase.RUNTIME_DISABLED

        # Phase 2: REPLACEMENT_PATH — replacement artifact specified
        if replacement_artifact:
            return SunsetPhase.REPLACEMENT_PATH

        # Phase 1: WARNING_ONLY — deprecated but no replacement yet
        return SunsetPhase.WARNING_ONLY

    def is_sunset_blocked(self, artifact_id: str) -> bool:
        """Check if an artifact is sunset-blocked (at RUNTIME_DISABLED but has deps).

        Args:
            artifact_id: The artifact_id to check.

        Returns:
            True if the artifact is at RUNTIME_DISABLED phase but has
            downstream dependencies preventing actual disabling.
        """
        phase = self.evaluate_sunset_phase(artifact_id)
        if phase != SunsetPhase.RUNTIME_DISABLED:
            return False
        return self._get_downstream_dependency_count(artifact_id) > 0

    def should_generate(self, artifact_id: str) -> bool:
        """Determine if an artifact should still be generated.

        Returns False only when:
        - Phase is RUNTIME_DISABLED AND downstream_dependency_count == 0
        - Phase is ARCHIVED

        In all other cases (including sunset-blocked), generation continues.

        Args:
            artifact_id: The artifact_id to check.

        Returns:
            True if the artifact should still be generated.
        """
        phase = self.evaluate_sunset_phase(artifact_id)

        if phase == SunsetPhase.ARCHIVED:
            return False

        if phase == SunsetPhase.RUNTIME_DISABLED:
            dep_count = self._get_downstream_dependency_count(artifact_id)
            # Only stop generation if zero dependencies
            return dep_count > 0

        return True

    def get_deprecation_warning(self, artifact_id: str) -> str | None:
        """Get the deprecation warning message for an artifact.

        Returns None if the artifact is not deprecated.
        Returns a CRITICAL-level message if sunset-blocked.

        Args:
            artifact_id: The artifact_id to check.

        Returns:
            Warning message string, or None if not deprecated.
        """
        phase = self.evaluate_sunset_phase(artifact_id)

        if phase == SunsetPhase.NOT_DEPRECATED:
            return None

        artifact = self._get_artifact(artifact_id)
        if artifact is None:
            return None

        replacement = artifact.get("replacement_artifact", "none")
        reason = artifact.get("deprecation_reason", "No reason specified")

        if phase == SunsetPhase.WARNING_ONLY:
            return (
                f"[DEPRECATION WARNING] Artifact '{artifact_id}' is deprecated. "
                f"Reason: {reason}"
            )

        if phase == SunsetPhase.REPLACEMENT_PATH:
            return (
                f"[DEPRECATION WARNING] Artifact '{artifact_id}' is deprecated. "
                f"Replacement: '{replacement}'. Reason: {reason}"
            )

        if phase == SunsetPhase.RUNTIME_DISABLED:
            dep_count = self._get_downstream_dependency_count(artifact_id)
            if dep_count > 0:
                return (
                    f"[CRITICAL] Artifact '{artifact_id}' has reached sunset date "
                    f"but cannot be disabled: {dep_count} downstream "
                    f"dependencies remain. Sunset-blocked."
                )
            return (
                f"[SUNSET] Artifact '{artifact_id}' generation disabled. "
                f"Sunset date reached with zero dependencies."
            )

        if phase == SunsetPhase.ARCHIVED:
            return (
                f"[ARCHIVED] Artifact '{artifact_id}' is archived and frozen."
            )

        return None

    def get_sunset_report(self) -> list[SunsetReportEntry]:
        """Generate a report of all artifacts in the deprecation pipeline.

        Returns all artifacts that have a deprecated_date set, with their
        current phase, age, remaining days, and dependency information.

        Returns:
            List of SunsetReportEntry objects for all deprecated artifacts.
        """
        entries: list[SunsetReportEntry] = []

        for artifact in self._artifacts:
            deprecated_date_str = artifact.get("deprecated_date")
            if not deprecated_date_str:
                continue

            artifact_id = artifact.get("artifact_id", "unknown")

            # Parse deprecated_date for age calculation
            try:
                deprecated_dt = date.fromisoformat(deprecated_date_str)
                age_days = (self._reference_date - deprecated_dt).days
            except (ValueError, TypeError):
                age_days = 0

            # Parse sunset_date for remaining days
            sunset_date_str = artifact.get("sunset_date")
            remaining_days: int | None = None
            if sunset_date_str:
                try:
                    sunset_dt = date.fromisoformat(sunset_date_str)
                    remaining_days = (sunset_dt - self._reference_date).days
                except (ValueError, TypeError):
                    remaining_days = None

            # Get dependency count
            dep_count = self._get_downstream_dependency_count(artifact_id)

            # Evaluate phase
            phase = self.evaluate_sunset_phase(artifact_id)

            # Determine if sunset-blocked
            sunset_blocked = (
                phase == SunsetPhase.RUNTIME_DISABLED and dep_count > 0
            )

            entries.append(
                SunsetReportEntry(
                    artifact_id=artifact_id,
                    phase=phase,
                    deprecated_date=deprecated_date_str,
                    sunset_date=sunset_date_str,
                    replacement_artifact=artifact.get("replacement_artifact"),
                    deprecation_reason=artifact.get("deprecation_reason"),
                    compatibility_impact=artifact.get("compatibility_impact"),
                    age_days=age_days,
                    remaining_days=remaining_days,
                    downstream_dependency_count=dep_count,
                    sunset_blocked=sunset_blocked,
                )
            )

        return entries

    def emit_deprecation_warnings(self) -> list[str]:
        """Emit deprecation warnings for all deprecated artifacts.

        Returns a list of warning messages for all artifacts currently
        in the deprecation pipeline.

        Returns:
            List of warning message strings.
        """
        warning_messages: list[str] = []

        for artifact in self._artifacts:
            artifact_id = artifact.get("artifact_id")
            if not artifact_id:
                continue

            msg = self.get_deprecation_warning(artifact_id)
            if msg:
                warning_messages.append(msg)
                warnings.warn(msg, DeprecationWarning, stacklevel=2)

        return warning_messages
