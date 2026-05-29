"""Boundary Enforcer — Write-time enforcement of domain boundaries.

Enforces allowed_writers constraints, cannot_own constraints, canonical boundary
runtime discovery, and cross-domain interaction detection.

Requirements: 16.1, 16.2, 16.3, 16.4, 16.5, 17.1, 17.2, 17.3, 17.4,
             18.1, 18.2, 18.3, 18.4, 19.1, 19.2, 19.3, 19.4
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

from governance.gate_framework import GateResult

# Artifact types considered canonical by default (fallback classification)
CANONICAL_ARTIFACT_TYPES: frozenset[str] = frozenset({
    "SSOT",
    "ENGINE",
    "CONFIG",
    "STEERING",
    "CALIBRATION",
    "RUNTIME",
})

# Artifact types considered transient by default (fallback classification)
TRANSIENT_ARTIFACT_TYPES: frozenset[str] = frozenset({
    "REPORT_OUT",
    "DATA_OUT",
    "DATA_IN",
    "SNAPSHOT",
    "DASHBOARD",
})


class BoundaryEnforcer:
    """Enforces domain boundary constraints at write time.

    Validates allowed_writers, cannot_own constraints, and detects
    cross-domain interactions. Produces GateResult objects for
    integration with the gate framework.

    Attributes:
        enforcement_mode: One of 'observability', 'soft', 'hard'.
        artifact_registry: Parsed artifact registry data.
        domain_registry: Parsed domain registry data.
    """

    def __init__(
        self,
        artifact_registry_path: str,
        domain_registry_path: str,
        enforcement_mode: str,
    ) -> None:
        """Initialize BoundaryEnforcer with registry paths and enforcement mode.

        Args:
            artifact_registry_path: Path to artifact_registry.yaml.
            domain_registry_path: Path to domain_registry.yaml.
            enforcement_mode: One of 'observability', 'soft', 'hard'.

        Raises:
            ValueError: If enforcement_mode is not valid.
        """
        valid_modes = {"observability", "soft", "hard"}
        if enforcement_mode not in valid_modes:
            raise ValueError(
                f"Invalid enforcement_mode '{enforcement_mode}'. "
                f"Must be one of: {sorted(valid_modes)}"
            )

        self.enforcement_mode = enforcement_mode
        self.artifact_registry_path = artifact_registry_path
        self.domain_registry_path = domain_registry_path

        self.artifact_registry: list[dict] = self._load_artifact_registry()
        self.domain_registry: list[dict] = self._load_domain_registry()

        # Build lookup indexes for efficient access
        self._artifact_index: dict[str, dict] = {
            a["artifact_id"]: a for a in self.artifact_registry if "artifact_id" in a
        }
        self._domain_index: dict[str, dict] = {
            d["domain_id"]: d for d in self.domain_registry if "domain_id" in d
        }

    def _load_artifact_registry(self) -> list[dict]:
        """Load and parse the artifact registry YAML file.

        Returns:
            List of artifact dictionaries.
        """
        path = Path(self.artifact_registry_path)
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data is None:
                return []
            if isinstance(data, dict) and "artifacts" in data:
                artifacts = data["artifacts"]
                return artifacts if isinstance(artifacts, list) else []
            if isinstance(data, list):
                return data
            return []
        except (yaml.YAMLError, OSError):
            return []

    def _load_domain_registry(self) -> list[dict]:
        """Load and parse the domain registry YAML file.

        Returns:
            List of domain dictionaries.
        """
        path = Path(self.domain_registry_path)
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data is None:
                return []
            if isinstance(data, dict) and "domains" in data:
                domains = data["domains"]
                return domains if isinstance(domains, list) else []
            if isinstance(data, list):
                return data
            return []
        except (yaml.YAMLError, OSError):
            return []

    def check_write_permission(self, writing_domain: str, artifact_id: str) -> bool:
        """Check if a domain has write permission for an artifact.

        Checks the artifact's allowed_writers field. If allowed_writers
        contains 'ALL', any domain is permitted to write.

        Args:
            writing_domain: Domain ID attempting the write.
            artifact_id: Identifier of the target artifact.

        Returns:
            True if the write is permitted, False otherwise.
            Returns True if artifact_id is not found (graceful handling).
        """
        artifact = self._artifact_index.get(artifact_id)
        if artifact is None:
            # Artifact not found in registry — cannot enforce, permit by default
            return True

        allowed_writers = artifact.get("allowed_writers", [])
        if not isinstance(allowed_writers, list):
            return True

        # ALL grants universal write permission (Req 16.5)
        if "ALL" in allowed_writers:
            return True

        return writing_domain in allowed_writers

    def check_cannot_own(self, domain_id: str, artifact_type: str) -> bool:
        """Check if a domain is forbidden from owning an artifact type.

        Args:
            domain_id: Domain ID to check.
            artifact_type: Artifact type to check against cannot_own.

        Returns:
            True if the domain CANNOT own the artifact type (violation exists).
            False if the domain is allowed to own it or domain is not found.
        """
        domain = self._domain_index.get(domain_id)
        if domain is None:
            # Domain not found — cannot enforce, no violation
            return False

        cannot_own = domain.get("cannot_own", [])
        if not isinstance(cannot_own, list):
            return False

        return artifact_type in cannot_own

    def enforce_write(self, writing_domain: str, artifact_id: str) -> GateResult:
        """Enforce write permission and produce a GateResult.

        Behavior by enforcement mode:
        - observability: log warning, permit (status=pass, action=warn)
        - soft: reject violation (status=fail, action=block)
        - hard: reject violation (status=fail, action=block)

        Args:
            writing_domain: Domain ID attempting the write.
            artifact_id: Identifier of the target artifact.

        Returns:
            GateResult with pass/fail status and appropriate enforcement action.
        """
        start_time = time.perf_counter()
        permitted = self.check_write_permission(writing_domain, artifact_id)
        duration_ms = (time.perf_counter() - start_time) * 1000

        if permitted:
            return GateResult(
                gate_name="boundary_write_check",
                status="pass",
                enforcement_action="info",
                duration_ms=duration_ms,
                details=[
                    f"Write permitted: domain '{writing_domain}' -> artifact '{artifact_id}'"
                ],
            )

        # Violation detected
        artifact = self._artifact_index.get(artifact_id, {})
        allowed = artifact.get("allowed_writers", [])
        violation_detail = (
            f"Boundary violation: domain '{writing_domain}' is not in "
            f"allowed_writers {allowed} for artifact '{artifact_id}'"
        )

        if self.enforcement_mode == "observability":
            return GateResult(
                gate_name="boundary_write_check",
                status="pass",
                enforcement_action="warn",
                duration_ms=duration_ms,
                details=[f"[WARN] {violation_detail} (observability mode — permitted)"],
            )

        # soft or hard mode: block the violation
        return GateResult(
            gate_name="boundary_write_check",
            status="fail",
            enforcement_action="block",
            duration_ms=duration_ms,
            details=[violation_detail],
        )

    def enforce_domain_assignment(
        self, domain_id: str, artifact_id: str, artifact_type: str
    ) -> GateResult:
        """Enforce cannot_own constraints for domain assignment.

        Checks that the target domain is not forbidden from owning the
        given artifact type. Also validates consistency between cannot_own
        and allowed_artifact_types.

        Behavior by enforcement mode:
        - observability: log warning, permit (status=pass, action=warn)
        - soft: reject violation (status=fail, action=block)
        - hard: reject violation (status=fail, action=block)

        Args:
            domain_id: Target domain for the assignment.
            artifact_id: Identifier of the artifact being assigned.
            artifact_type: Type of the artifact being assigned.

        Returns:
            GateResult with pass/fail status and appropriate enforcement action.
        """
        start_time = time.perf_counter()
        violation = self.check_cannot_own(domain_id, artifact_type)
        duration_ms = (time.perf_counter() - start_time) * 1000

        if not violation:
            # Also check allowed_artifact_types consistency (Req 17.4)
            domain = self._domain_index.get(domain_id)
            if domain is not None:
                allowed_types = domain.get("allowed_artifact_types", [])
                if isinstance(allowed_types, list) and allowed_types:
                    if artifact_type not in allowed_types:
                        consistency_detail = (
                            f"Artifact type '{artifact_type}' not in "
                            f"allowed_artifact_types {allowed_types} for domain '{domain_id}'"
                        )
                        if self.enforcement_mode == "observability":
                            return GateResult(
                                gate_name="boundary_domain_assignment",
                                status="pass",
                                enforcement_action="warn",
                                duration_ms=duration_ms,
                                details=[
                                    f"[WARN] {consistency_detail} "
                                    f"(observability mode — permitted)"
                                ],
                            )
                        return GateResult(
                            gate_name="boundary_domain_assignment",
                            status="fail",
                            enforcement_action="block",
                            duration_ms=duration_ms,
                            details=[consistency_detail],
                        )

            return GateResult(
                gate_name="boundary_domain_assignment",
                status="pass",
                enforcement_action="info",
                duration_ms=duration_ms,
                details=[
                    f"Assignment permitted: domain '{domain_id}' can own "
                    f"artifact '{artifact_id}' (type: {artifact_type})"
                ],
            )

        # cannot_own violation detected
        violation_detail = (
            f"Cannot-own violation: domain '{domain_id}' cannot own "
            f"artifact type '{artifact_type}' (artifact: '{artifact_id}')"
        )

        if self.enforcement_mode == "observability":
            return GateResult(
                gate_name="boundary_domain_assignment",
                status="pass",
                enforcement_action="warn",
                duration_ms=duration_ms,
                details=[f"[WARN] {violation_detail} (observability mode — permitted)"],
            )

        # soft or hard mode: block the violation
        return GateResult(
            gate_name="boundary_domain_assignment",
            status="fail",
            enforcement_action="block",
            duration_ms=duration_ms,
            details=[violation_detail],
        )

    def detect_cross_domain_interaction(
        self,
        source_domain: str,
        target_domain: str,
        artifact_id: str,
        interaction_type: str,
    ) -> dict:
        """Detect and log cross-domain interactions.

        Cross-domain interactions occur when a module in one domain reads
        or writes an artifact owned by a different domain.

        Behavior by enforcement mode:
        - observability: log as informational, never block
        - soft: log as informational, never block
        - hard: block if interaction_type is 'write' and violates allowed_writers

        Args:
            source_domain: Domain initiating the interaction.
            target_domain: Domain owning the target artifact.
            artifact_id: Identifier of the artifact being accessed.
            interaction_type: One of 'read' or 'write'.

        Returns:
            Dictionary with interaction details including:
            - source_domain, target_domain, artifact_id, interaction_type
            - timestamp, is_cross_domain, permitted, enforcement_action
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        is_cross_domain = source_domain != target_domain

        result = {
            "source_domain": source_domain,
            "target_domain": target_domain,
            "artifact_id": artifact_id,
            "interaction_type": interaction_type,
            "timestamp": timestamp,
            "is_cross_domain": is_cross_domain,
            "permitted": True,
            "enforcement_action": "info",
        }

        if not is_cross_domain:
            # Same-domain interaction — always permitted
            return result

        # Cross-domain interaction detected (Req 19.1, 19.2)
        if interaction_type == "write":
            # Check allowed_writers for write interactions
            write_permitted = self.check_write_permission(source_domain, artifact_id)

            if not write_permitted and self.enforcement_mode == "hard":
                # Hard mode blocks cross-domain writes that violate allowed_writers (Req 19.4)
                result["permitted"] = False
                result["enforcement_action"] = "block"
                result["violation"] = (
                    f"Cross-domain write blocked: '{source_domain}' cannot write "
                    f"to artifact '{artifact_id}' owned by '{target_domain}'"
                )
            elif not write_permitted:
                # observability/soft: log as informational (Req 19.3)
                result["enforcement_action"] = "warn"
                result["violation"] = (
                    f"Cross-domain write detected: '{source_domain}' writing to "
                    f"artifact '{artifact_id}' owned by '{target_domain}' "
                    f"(not in allowed_writers)"
                )
            else:
                result["enforcement_action"] = "info"
        else:
            # Read interactions are always informational (Req 19.3)
            result["enforcement_action"] = "info"

        return result

    def classify_artifact(self, artifact_id: str) -> str:
        """Classify an artifact using runtime discovery with fallback.

        Derives canonical/transient classification from Artifact_Registry
        metadata (artifact_type and lifecycle_status). Falls back to
        hardcoded frozensets if registry-based classification cannot
        determine status.

        Classification rules:
        - Artifact types in CANONICAL_ARTIFACT_TYPES -> 'canonical'
        - Artifact types in TRANSIENT_ARTIFACT_TYPES -> 'transient'
        - Lifecycle status 'canonical' -> 'canonical'
        - Unknown -> fallback to hardcoded sets, then 'unknown'

        Args:
            artifact_id: Identifier of the artifact to classify.

        Returns:
            One of 'canonical', 'transient', or 'unknown'.
        """
        artifact = self._artifact_index.get(artifact_id)

        if artifact is None:
            # Artifact not in registry — attempt fallback classification
            # Import the existing canonical_boundary module for fallback
            try:
                from governance.canonical_boundary import (
                    CANONICAL_ARTIFACTS,
                    TRANSIENT_ARTIFACTS,
                )

                if artifact_id in CANONICAL_ARTIFACTS:
                    return "canonical"
                if artifact_id in TRANSIENT_ARTIFACTS:
                    return "transient"
            except ImportError:
                pass
            return "unknown"

        # Runtime discovery from registry metadata (Req 18.1, 18.2)
        artifact_type = artifact.get("artifact_type", "")
        lifecycle_status = artifact.get("lifecycle_status", "")

        # Classify by artifact type
        if artifact_type in CANONICAL_ARTIFACT_TYPES:
            return "canonical"
        if artifact_type in TRANSIENT_ARTIFACT_TYPES:
            return "transient"

        # Classify by lifecycle status
        if lifecycle_status == "canonical":
            return "canonical"

        # Fallback to hardcoded sets (Req 18.3)
        try:
            from governance.canonical_boundary import (
                CANONICAL_ARTIFACTS,
                TRANSIENT_ARTIFACTS,
            )

            if artifact_id in CANONICAL_ARTIFACTS:
                return "canonical"
            if artifact_id in TRANSIENT_ARTIFACTS:
                return "transient"
        except ImportError:
            pass

        # Cannot determine classification (Req 18.4 — log warning case)
        return "unknown"
