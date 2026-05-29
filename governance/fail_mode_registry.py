"""Fail-mode classification registry for governance components.

Provides persisted classification of each governance component's failure
behavior (fail_open, fail_soft, fail_closed). Supports enforcement-mode-
dependent fail modes where a component's behavior varies by the current
enforcement mode. Includes freeze/thaw semantics for self-disable
protection (Requirement 49).

Requirements: 29.1, 29.7, 49.1, 49.2, 49.4
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

import yaml


class FailMode(StrEnum):
    """Classification of a governance component's failure behavior.

    - FAIL_OPEN: Skip governance, continue pipeline execution.
    - FAIL_SOFT: Log degradation, continue pipeline execution.
    - FAIL_CLOSED: Block until resolved; pipeline cannot proceed.
    """

    FAIL_OPEN = "fail_open"
    FAIL_SOFT = "fail_soft"
    FAIL_CLOSED = "fail_closed"


class FailModeRegistry:
    """Registry of fail-mode classifications loaded from YAML config.

    Loads component fail-mode classifications from
    `.domainization/fail_mode_config.yaml`. Supports both simple fail modes
    (a single mode for all enforcement modes) and enforcement-mode-dependent
    fail modes (a dict mapping enforcement mode to fail mode).

    The registry can be frozen at pipeline start to prevent any modifications
    during execution, satisfying the self-disable protection requirement
    (Req 49).

    Attributes:
        config_path: Path to the fail_mode_config.yaml file.
    """

    def __init__(self, config_path: str) -> None:
        """Initialize the registry by loading config from YAML.

        Args:
            config_path: Path to the fail_mode_config.yaml file.

        Raises:
            FileNotFoundError: If the config file does not exist.
            yaml.YAMLError: If the config file is malformed YAML.
            ValueError: If a fail_mode value is not a valid FailMode.
        """
        self._config_path = config_path
        self._frozen = False
        self._classifications: dict[str, FailMode | dict[str, FailMode]] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load and parse the fail_mode_config.yaml file."""
        path = Path(self._config_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Fail-mode config not found: {self._config_path}"
            )

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data or "components" not in data:
            raise ValueError(
                f"Invalid fail_mode_config.yaml: missing 'components' key"
            )

        components = data["components"]
        for component_name, component_data in components.items():
            fail_mode_raw = component_data.get("fail_mode")
            if fail_mode_raw is None:
                raise ValueError(
                    f"Component '{component_name}' missing 'fail_mode' field"
                )

            if isinstance(fail_mode_raw, str):
                # Simple fail mode (same for all enforcement modes)
                self._classifications[component_name] = FailMode(fail_mode_raw)
            elif isinstance(fail_mode_raw, dict):
                # Enforcement-mode-dependent fail modes
                mode_map: dict[str, FailMode] = {}
                for enforcement_mode, mode_value in fail_mode_raw.items():
                    mode_map[enforcement_mode] = FailMode(mode_value)
                self._classifications[component_name] = mode_map
            else:
                raise ValueError(
                    f"Component '{component_name}' has invalid fail_mode type: "
                    f"{type(fail_mode_raw)}"
                )

    def get_fail_mode(
        self, component_name: str, enforcement_mode: str | None = None
    ) -> FailMode:
        """Get the fail mode for a component.

        For components with a simple (single) fail mode, the enforcement_mode
        parameter is ignored. For components with enforcement-mode-dependent
        fail modes, the enforcement_mode is used to resolve the correct mode.

        Args:
            component_name: The governance component name (e.g.,
                "mutation_audit_ledger", "yaml_config_parser").
            enforcement_mode: Optional enforcement mode to resolve
                mode-dependent classifications. One of "observability",
                "soft", "hard". Required for components with mode-dependent
                fail modes.

        Returns:
            The FailMode classification for the component.

        Raises:
            KeyError: If the component is not registered.
            ValueError: If the component has mode-dependent fail modes but
                no enforcement_mode was provided, or if the enforcement_mode
                is not found in the component's mode map.
        """
        if component_name not in self._classifications:
            raise KeyError(
                f"Component '{component_name}' not found in fail-mode registry"
            )

        classification = self._classifications[component_name]

        if isinstance(classification, FailMode):
            return classification

        # Mode-dependent: resolve using enforcement_mode
        if enforcement_mode is None:
            raise ValueError(
                f"Component '{component_name}' has enforcement-mode-dependent "
                f"fail modes; enforcement_mode parameter is required. "
                f"Available modes: {list(classification.keys())}"
            )

        if enforcement_mode not in classification:
            raise ValueError(
                f"Enforcement mode '{enforcement_mode}' not found for "
                f"component '{component_name}'. "
                f"Available modes: {list(classification.keys())}"
            )

        return classification[enforcement_mode]

    def get_all_classifications(self) -> dict[str, FailMode | dict[str, FailMode]]:
        """Get all component fail-mode classifications.

        Returns:
            A dictionary mapping component names to their fail-mode
            classification. Values are either a single FailMode or a dict
            mapping enforcement mode strings to FailMode values.
        """
        return dict(self._classifications)

    def freeze(self) -> None:
        """Freeze the registry to prevent modifications.

        Called at pipeline start to lock fail-mode classifications.
        Once frozen, no modifications are permitted until the pipeline
        completes. This satisfies Requirement 49 (self-disable protection).
        """
        self._frozen = True

    def is_frozen(self) -> bool:
        """Check whether the registry is currently frozen.

        Returns:
            True if the registry is frozen (locked), False otherwise.
        """
        return self._frozen

    def attempt_modification(
        self, component_name: str, target_field: str, new_value: str
    ) -> tuple[bool, str]:
        """Attempt to modify a component's fail-mode classification.

        When the registry is frozen, all modifications are rejected. When
        not frozen, the modification is allowed and applied.

        Args:
            component_name: The component whose classification to modify.
            target_field: The field being modified (e.g., "fail_mode").
            new_value: The new value to set.

        Returns:
            A tuple of (allowed, reason):
            - (True, "Modification applied") when not frozen and successful.
            - (False, "Registry is frozen: modifications are not permitted
              during pipeline execution") when frozen.
            - (False, reason) for other validation failures.
        """
        if self._frozen:
            return (
                False,
                "Registry is frozen: modifications are not permitted "
                "during pipeline execution",
            )

        # Validate the new value is a valid FailMode
        if target_field == "fail_mode":
            try:
                new_fail_mode = FailMode(new_value)
            except ValueError:
                return (
                    False,
                    f"Invalid fail_mode value '{new_value}'. "
                    f"Must be one of: {[m.value for m in FailMode]}",
                )

            if component_name not in self._classifications:
                return (
                    False,
                    f"Component '{component_name}' not found in registry",
                )

            self._classifications[component_name] = new_fail_mode
            return (True, "Modification applied")

        return (
            False,
            f"Unknown target field '{target_field}'. "
            f"Only 'fail_mode' modifications are supported.",
        )
