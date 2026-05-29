"""Enforcement mode configuration loader.

Reads the governance enforcement mode from `.domainization/config.yaml`
and provides it to GateFramework, LifecycleEnforcer, and BoundaryEnforcer
during initialization.

The enforcement mode is the single source of truth for how governance
checks behave across the entire runtime:
    - observability: warnings only, never block
    - soft: block on gates configured as blocking_in_soft
    - hard: block on all configured gates

Cold-start overrides: If the ColdStartHandler detects missing governance
state, enforcement mode is forced to 'observability' regardless of config.

Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


# Valid enforcement mode values
VALID_ENFORCEMENT_MODES = frozenset({"observability", "soft", "hard"})

# Default enforcement mode when config is missing or invalid
DEFAULT_ENFORCEMENT_MODE = "observability"

# Default path to the domainization config file
DEFAULT_CONFIG_PATH = ".domainization/config.yaml"


class EnforcementConfigError(Exception):
    """Raised when enforcement configuration cannot be loaded."""

    pass


def load_enforcement_mode(
    config_path: str | None = None,
    base_path: str | None = None,
) -> str:
    """Load the governance enforcement mode from config.yaml.

    Reads `governance_enforcement.mode` from the domainization config file.
    Falls back to the legacy `enforcement_mode` field if the new structured
    section is not present. Defaults to 'observability' if neither is found.

    Args:
        config_path: Explicit path to config.yaml. If None, uses
            base_path / DEFAULT_CONFIG_PATH.
        base_path: Project root directory. Defaults to current working
            directory if not specified.

    Returns:
        The enforcement mode string: 'observability', 'soft', or 'hard'.

    Raises:
        EnforcementConfigError: If the config file exists but cannot be
            parsed, and no fallback is available.
    """
    if config_path is None:
        if base_path is None:
            base_path = os.getcwd()
        config_path = os.path.join(base_path, DEFAULT_CONFIG_PATH)

    config = _load_config_file(config_path)

    # Primary: governance_enforcement.mode (new structured section)
    governance_enforcement = config.get("governance_enforcement")
    if isinstance(governance_enforcement, dict):
        mode = governance_enforcement.get("mode")
        if mode is not None:
            return _validate_mode(str(mode))

    # Fallback: legacy enforcement_mode field
    legacy_mode = config.get("enforcement_mode")
    if legacy_mode is not None:
        return _validate_mode(str(legacy_mode))

    # Default when neither field is present
    return DEFAULT_ENFORCEMENT_MODE


def _load_config_file(config_path: str) -> dict[str, Any]:
    """Load and parse the YAML config file.

    Args:
        config_path: Path to the config.yaml file.

    Returns:
        Parsed YAML content as a dictionary.

    Raises:
        EnforcementConfigError: If the file cannot be read or parsed.
    """
    path = Path(config_path)

    if not path.is_file():
        # Config file missing — return empty dict to trigger defaults
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise EnforcementConfigError(
            f"Failed to parse config file '{config_path}': {e}"
        ) from e
    except OSError as e:
        raise EnforcementConfigError(
            f"Failed to read config file '{config_path}': {e}"
        ) from e

    if content is None:
        return {}
    if not isinstance(content, dict):
        raise EnforcementConfigError(
            f"Config file '{config_path}' does not contain a YAML mapping"
        )

    return content


def _validate_mode(mode: str) -> str:
    """Validate that the mode is one of the allowed values.

    Args:
        mode: The enforcement mode string to validate.

    Returns:
        The validated mode string (lowercased).

    Raises:
        EnforcementConfigError: If the mode is not valid.
    """
    normalized = mode.strip().lower()
    if normalized not in VALID_ENFORCEMENT_MODES:
        raise EnforcementConfigError(
            f"Invalid enforcement mode '{mode}'. "
            f"Must be one of: {sorted(VALID_ENFORCEMENT_MODES)}"
        )
    return normalized


def initialize_enforcers(
    config_path: str | None = None,
    base_path: str | None = None,
    cold_start_override: bool = False,
) -> dict[str, Any]:
    """Initialize governance enforcers with the configured enforcement mode.

    Reads the enforcement mode from config.yaml and creates initialized
    instances of GateFramework, LifecycleEnforcer, and BoundaryEnforcer.

    If cold_start_override is True, forces observability mode regardless
    of the configured value.

    Args:
        config_path: Explicit path to config.yaml.
        base_path: Project root directory. Defaults to cwd.
        cold_start_override: If True, force observability mode (cold-start).

    Returns:
        Dictionary with keys:
            - 'enforcement_mode': The active enforcement mode string
            - 'gate_framework': Initialized GateFramework instance
            - 'lifecycle_enforcer': Initialized LifecycleEnforcer instance
            - 'boundary_enforcer': Initialized BoundaryEnforcer instance
    """
    from governance.boundary_enforcer import BoundaryEnforcer
    from governance.gate_framework import GateFramework
    from governance.lifecycle_enforcer import LifecycleEnforcer

    if base_path is None:
        base_path = os.getcwd()

    # Determine enforcement mode
    if cold_start_override:
        enforcement_mode = "observability"
    else:
        enforcement_mode = load_enforcement_mode(
            config_path=config_path, base_path=base_path
        )

    # Resolve paths for enforcer dependencies
    domainization_path = os.path.join(base_path, ".domainization")
    state_machine_path = os.path.join(
        domainization_path, "lifecycle_state_machine.yaml"
    )
    artifact_registry_path = os.path.join(
        domainization_path, "artifact_registry.yaml"
    )
    domain_registry_path = os.path.join(
        domainization_path, "domain_registry.yaml"
    )

    # Initialize GateFramework with empty gate config (gates registered separately)
    gate_config = {"gates": {}}
    gate_framework = GateFramework(
        config=gate_config, enforcement_mode=enforcement_mode
    )

    # Initialize LifecycleEnforcer
    lifecycle_enforcer = LifecycleEnforcer(
        state_machine_path=state_machine_path,
        enforcement_mode=enforcement_mode,
    )

    # Initialize BoundaryEnforcer
    boundary_enforcer = BoundaryEnforcer(
        artifact_registry_path=artifact_registry_path,
        domain_registry_path=domain_registry_path,
        enforcement_mode=enforcement_mode,
    )

    return {
        "enforcement_mode": enforcement_mode,
        "gate_framework": gate_framework,
        "lifecycle_enforcer": lifecycle_enforcer,
        "boundary_enforcer": boundary_enforcer,
    }
