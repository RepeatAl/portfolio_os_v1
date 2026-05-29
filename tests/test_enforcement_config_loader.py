"""Unit tests for governance/enforcement_config_loader.py.

Tests the enforcement mode configuration loading and enforcer initialization
wiring. Validates Requirements 7.1, 7.2, 7.3, 7.4, 7.5.
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from governance.enforcement_config_loader import (
    DEFAULT_ENFORCEMENT_MODE,
    EnforcementConfigError,
    VALID_ENFORCEMENT_MODES,
    initialize_enforcers,
    load_enforcement_mode,
)


class TestLoadEnforcementMode:
    """Tests for load_enforcement_mode function."""

    def test_reads_from_governance_enforcement_section(self, tmp_path: Path) -> None:
        """Req 7.1: Reads enforcement mode from config.yaml at startup."""
        config = {"governance_enforcement": {"mode": "soft"}}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(config_path=str(config_file))
        assert result == "soft"

    def test_supports_observability_mode(self, tmp_path: Path) -> None:
        """Req 7.2: Supports 'observability' mode."""
        config = {"governance_enforcement": {"mode": "observability"}}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(config_path=str(config_file))
        assert result == "observability"

    def test_supports_soft_mode(self, tmp_path: Path) -> None:
        """Req 7.2: Supports 'soft' mode."""
        config = {"governance_enforcement": {"mode": "soft"}}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(config_path=str(config_file))
        assert result == "soft"

    def test_supports_hard_mode(self, tmp_path: Path) -> None:
        """Req 7.2: Supports 'hard' mode."""
        config = {"governance_enforcement": {"mode": "hard"}}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(config_path=str(config_file))
        assert result == "hard"

    def test_falls_back_to_legacy_enforcement_mode(self, tmp_path: Path) -> None:
        """Falls back to legacy enforcement_mode field if new section missing."""
        config = {"enforcement_mode": "soft"}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(config_path=str(config_file))
        assert result == "soft"

    def test_defaults_to_observability_when_missing(self, tmp_path: Path) -> None:
        """Defaults to observability when no enforcement mode is configured."""
        config = {"some_other_key": "value"}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(config_path=str(config_file))
        assert result == DEFAULT_ENFORCEMENT_MODE
        assert result == "observability"

    def test_defaults_when_config_file_missing(self, tmp_path: Path) -> None:
        """Defaults to observability when config file does not exist."""
        result = load_enforcement_mode(
            config_path=str(tmp_path / "nonexistent.yaml")
        )
        assert result == "observability"

    def test_raises_on_invalid_mode(self, tmp_path: Path) -> None:
        """Raises EnforcementConfigError for invalid mode values."""
        config = {"governance_enforcement": {"mode": "invalid_mode"}}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        with pytest.raises(EnforcementConfigError, match="Invalid enforcement mode"):
            load_enforcement_mode(config_path=str(config_file))

    def test_raises_on_malformed_yaml(self, tmp_path: Path) -> None:
        """Raises EnforcementConfigError for unparseable YAML."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("{{invalid yaml: [")

        with pytest.raises(EnforcementConfigError, match="Failed to parse"):
            load_enforcement_mode(config_path=str(config_file))

    def test_normalizes_mode_case(self, tmp_path: Path) -> None:
        """Mode values are normalized to lowercase."""
        config = {"governance_enforcement": {"mode": "SOFT"}}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(config_path=str(config_file))
        assert result == "soft"

    def test_strips_whitespace_from_mode(self, tmp_path: Path) -> None:
        """Mode values have whitespace stripped."""
        config = {"governance_enforcement": {"mode": "  hard  "}}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(config_path=str(config_file))
        assert result == "hard"

    def test_prefers_governance_enforcement_over_legacy(self, tmp_path: Path) -> None:
        """New governance_enforcement section takes precedence over legacy field."""
        config = {
            "enforcement_mode": "hard",
            "governance_enforcement": {"mode": "soft"},
        }
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(config_path=str(config_file))
        assert result == "soft"

    def test_reads_from_real_config(self) -> None:
        """Reads enforcement mode from the actual project config.yaml."""
        result = load_enforcement_mode(
            base_path=os.getcwd()
        )
        assert result in VALID_ENFORCEMENT_MODES

    def test_base_path_resolution(self, tmp_path: Path) -> None:
        """Resolves config path relative to base_path."""
        domainization_dir = tmp_path / ".domainization"
        domainization_dir.mkdir()
        config = {"governance_enforcement": {"mode": "hard"}}
        config_file = domainization_dir / "config.yaml"
        config_file.write_text(yaml.dump(config))

        result = load_enforcement_mode(base_path=str(tmp_path))
        assert result == "hard"


class TestInitializeEnforcers:
    """Tests for initialize_enforcers function."""

    def test_returns_all_enforcer_instances(self) -> None:
        """Req 7.1: Wires enforcement mode into all enforcers."""
        result = initialize_enforcers()

        assert "enforcement_mode" in result
        assert "gate_framework" in result
        assert "lifecycle_enforcer" in result
        assert "boundary_enforcer" in result

    def test_enforcers_use_configured_mode(self) -> None:
        """All enforcers receive the configured enforcement mode."""
        result = initialize_enforcers()

        mode = result["enforcement_mode"]
        assert mode in VALID_ENFORCEMENT_MODES

        # GateFramework exposes enforcement_mode property
        assert result["gate_framework"].enforcement_mode == mode

    def test_cold_start_override_forces_observability(self) -> None:
        """Cold-start override forces observability regardless of config."""
        result = initialize_enforcers(cold_start_override=True)

        assert result["enforcement_mode"] == "observability"
        assert result["gate_framework"].enforcement_mode == "observability"

    def test_returns_correct_types(self) -> None:
        """Returns properly typed enforcer instances."""
        from governance.boundary_enforcer import BoundaryEnforcer
        from governance.gate_framework import GateFramework
        from governance.lifecycle_enforcer import LifecycleEnforcer

        result = initialize_enforcers()

        assert isinstance(result["gate_framework"], GateFramework)
        assert isinstance(result["lifecycle_enforcer"], LifecycleEnforcer)
        assert isinstance(result["boundary_enforcer"], BoundaryEnforcer)

    def test_custom_config_path(self, tmp_path: Path) -> None:
        """Accepts custom config path for testing."""
        config = {"governance_enforcement": {"mode": "soft"}}
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        # Need real domainization files for enforcers
        result = initialize_enforcers(config_path=str(config_file))
        assert result["enforcement_mode"] == "soft"


class TestConfigYamlStructure:
    """Tests that the actual config.yaml has the required structure."""

    def test_governance_enforcement_section_exists(self) -> None:
        """Req 7.1: config.yaml has governance_enforcement section."""
        config_path = os.path.join(
            os.getcwd(), ".domainization", "config.yaml"
        )
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        assert "governance_enforcement" in config
        assert isinstance(config["governance_enforcement"], dict)

    def test_governance_enforcement_mode_field(self) -> None:
        """Req 7.2: governance_enforcement.mode field exists with valid value."""
        config_path = os.path.join(
            os.getcwd(), ".domainization", "config.yaml"
        )
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        mode = config["governance_enforcement"]["mode"]
        assert mode in VALID_ENFORCEMENT_MODES

    def test_transition_criteria_documented(self) -> None:
        """Req 7.4: Transition criteria documented as YAML comments."""
        config_path = os.path.join(
            os.getcwd(), ".domainization", "config.yaml"
        )
        with open(config_path, "r") as f:
            content = f.read()

        # Verify transition criteria comments are present
        assert "observability" in content and "soft" in content
        assert "property tests pass" in content.lower() or "property_tests" in content.lower() or "All property tests pass" in content
        assert "30 days" in content or "30-day" in content

    def test_default_mode_is_observability(self) -> None:
        """Default enforcement mode is observability."""
        config_path = os.path.join(
            os.getcwd(), ".domainization", "config.yaml"
        )
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        assert config["governance_enforcement"]["mode"] == "observability"
