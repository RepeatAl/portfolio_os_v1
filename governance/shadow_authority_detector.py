"""Shadow Authority Detector — observation engine for undeclared mutation paths.

Detects when a module writes to an artifact without being listed in that
artifact's allowed_writers field. This is an OBSERVATION ENGINE only:
it observes, measures, and reports. It does NOT decide severity, block
anything, apply hard thresholds, or make enforcement decisions.

Severity assignment and blocking decisions belong to GateFramework/EnforcementMode.

CTO Directive: No check_threshold(), no CRITICAL classification, no blocking logic.

Requirements: 40.1, 40.2, 40.3, 40.4, 40.5
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class ShadowAuthorityDetector:
    """Observation engine for undeclared mutation authority paths.

    Detects writes not listed in allowed_writers, distinguishes registered
    engine shadow authority from unregistered module shadow authority, and
    produces structured observation reports.

    This class MUST:
    - Observe undeclared write paths
    - Measure (count unique paths, list undeclared writers)
    - Report (return structured observation data)

    This class MUST NOT:
    - Decide severity (no CRITICAL classification)
    - Block anything
    - Apply hard thresholds
    - Make enforcement decisions
    """

    def __init__(self, artifact_registry_path: str) -> None:
        """Initialize ShadowAuthorityDetector with artifact registry.

        Args:
            artifact_registry_path: Path to artifact_registry.yaml.
        """
        self.artifact_registry_path = artifact_registry_path
        self._artifact_registry: list[dict[str, Any]] = self._load_artifact_registry()
        self._artifact_index: dict[str, dict[str, Any]] = {
            a["artifact_id"]: a
            for a in self._artifact_registry
            if "artifact_id" in a
        }
        self._registered_engines: frozenset[str] = self._load_registered_engines()
        self._shadow_events: list[dict[str, Any]] = []

    def _load_artifact_registry(self) -> list[dict[str, Any]]:
        """Load and parse the artifact registry YAML file.

        Returns:
            List of artifact dictionaries. Empty list on failure.
        """
        path = Path(self.artifact_registry_path)
        if not path.exists():
            logger.warning(
                "Artifact registry not found at %s — shadow detection degraded",
                self.artifact_registry_path,
            )
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
        except (yaml.YAMLError, OSError) as exc:
            logger.warning(
                "Failed to load artifact registry: %s — shadow detection degraded",
                exc,
            )
            return []

    def _load_registered_engines(self) -> frozenset[str]:
        """Load registered engine names from ENGINE_REGISTRY.

        Attempts to import the engine registry to identify which modules
        are registered engines (potentially legitimate shadow authority)
        vs unregistered modules (likely violations).

        Returns:
            Frozenset of registered engine names.
        """
        try:
            from engines.engine_registry import ENGINE_REGISTRY

            return frozenset(ENGINE_REGISTRY.keys())
        except (ImportError, AttributeError):
            logger.warning(
                "Could not load ENGINE_REGISTRY — all modules treated as unregistered"
            )
            return frozenset()

    def check_write_authority(
        self, writing_module: str, target_artifact_id: str
    ) -> bool:
        """Check if a module has declared write authority for an artifact.

        Looks up the artifact's allowed_writers and checks whether the
        writing module (or its domain) is listed.

        Args:
            writing_module: Module path or identifier attempting the write.
            target_artifact_id: Identifier of the target artifact.

        Returns:
            True if the write is authorized (module is in allowed_writers
            or allowed_writers contains 'ALL'). False if undeclared.
            Returns True if artifact is not found (cannot determine authority).
        """
        artifact = self._artifact_index.get(target_artifact_id)
        if artifact is None:
            # Artifact not in registry — cannot determine authority
            return True

        allowed_writers = artifact.get("allowed_writers", [])
        if not isinstance(allowed_writers, list):
            return True

        # ALL grants universal write permission
        if "ALL" in allowed_writers:
            return True

        # Check if writing_module matches any allowed writer
        # Match by exact name, or by engine name prefix
        for writer in allowed_writers:
            if writer == writing_module:
                return True
            # Check if module name contains the writer domain/engine name
            if writer.lower() in writing_module.lower():
                return True

        return False

    def record_shadow_event(
        self,
        writing_module: str,
        target_artifact_id: str,
        declared_writers: list[str],
    ) -> dict[str, Any]:
        """Record a shadow authority event (undeclared write detected).

        Creates a structured event record and appends it to the internal
        event list for this run.

        Args:
            writing_module: Module path or identifier that performed the write.
            target_artifact_id: Identifier of the artifact written to.
            declared_writers: The artifact's allowed_writers list.

        Returns:
            Event dictionary with structured observation data.
        """
        # Determine if this is a registered engine or unregistered module
        engine_name = self._extract_engine_name(writing_module)
        is_registered_engine = engine_name in self._registered_engines

        event: dict[str, Any] = {
            "writing_module": writing_module,
            "target_artifact_id": target_artifact_id,
            "declared_writers": declared_writers,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "is_registered_engine": is_registered_engine,
            "engine_name": engine_name if is_registered_engine else None,
            "authority_type": (
                "registered_engine_shadow"
                if is_registered_engine
                else "unregistered_module_shadow"
            ),
        }

        self._shadow_events.append(event)
        logger.info(
            "Shadow authority event recorded: %s -> %s (type: %s)",
            writing_module,
            target_artifact_id,
            event["authority_type"],
        )

        return event

    def get_observation_report(self) -> dict[str, Any]:
        """Generate structured observation report for this run.

        Returns a report containing:
        - unique_paths: Count of unique (module, artifact) pairs
        - undeclared_writers: List of undeclared writer details
        - severity_recommendation: Advisory string ("info", "warning", "elevated")

        The severity_recommendation is ADVISORY ONLY — it is a recommendation,
        not a decision. The GateFramework decides what to do with it.

        Returns:
            Structured observation report dictionary.
        """
        # Calculate unique paths (unique module->artifact combinations)
        unique_paths_set: set[tuple[str, str]] = set()
        for event in self._shadow_events:
            unique_paths_set.add(
                (event["writing_module"], event["target_artifact_id"])
            )

        unique_path_count = len(unique_paths_set)

        # Build undeclared writers list
        undeclared_writers: list[dict[str, Any]] = [
            {
                "module": event["writing_module"],
                "artifact_id": event["target_artifact_id"],
                "declared_writers": event["declared_writers"],
            }
            for event in self._shadow_events
        ]

        # Advisory severity recommendation (NOT a decision)
        # 0 undeclared paths → "info"
        # 1-5 undeclared paths → "warning"
        # >5 undeclared paths → "elevated"
        if unique_path_count == 0:
            severity_recommendation = "info"
        elif unique_path_count <= 5:
            severity_recommendation = "warning"
        else:
            severity_recommendation = "elevated"

        return {
            "unique_paths": unique_path_count,
            "undeclared_writers": undeclared_writers,
            "severity_recommendation": severity_recommendation,
        }

    def reset(self) -> None:
        """Clear all recorded events for a new run.

        Call this at the start of each pipeline execution to ensure
        observations are scoped to the current run only.
        """
        self._shadow_events.clear()

    def _extract_engine_name(self, writing_module: str) -> str:
        """Extract engine name from a module path for registry lookup.

        Handles various module path formats:
        - "engines/allocation_engine.py" → "allocation"
        - "engines.allocation_engine" → "allocation"
        - "allocation_engine" → "allocation"
        - "allocation" → "allocation"
        - "some_random_module" → "some_random_module"

        Args:
            writing_module: Module path or identifier.

        Returns:
            Extracted engine name for registry lookup.
        """
        # Strip file extension
        name = writing_module.replace(".py", "")

        # Handle path separators
        if "/" in name:
            name = name.split("/")[-1]
        if "." in name:
            name = name.split(".")[-1]

        # Strip _engine suffix for registry lookup
        if name.endswith("_engine"):
            name = name[: -len("_engine")]

        return name
