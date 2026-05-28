"""
Tests for artifact registration enforcement policy (HARDENING 14).

Validates:
- Full registration required for runtime/ and governance/ artifacts
- Simplified registration for tests/ artifacts
- Transient exempt patterns correctly identified
- CI-compatible warning emitted when baseline exceeded
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from dataclasses import dataclass
from typing import List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent))

from validation_orchestrator import (
    RegistrationEnforcementPolicy,
    RegistrationEnforcementResult,
    ValidationOrchestrator,
    W800_REGISTRATION_REQUIRED,
    W801_UNREGISTERED_COUNT_INCREASE,
    W802_SIMPLIFIED_REGISTRATION_MISSING,
)


class TestRegistrationEnforcementPolicy:
    """Tests for RegistrationEnforcementPolicy dataclass."""

    def test_default_full_registration_dirs(self):
        policy = RegistrationEnforcementPolicy()
        assert "runtime/" in policy.full_registration_dirs
        assert "governance/" in policy.full_registration_dirs

    def test_default_simplified_registration_dirs(self):
        policy = RegistrationEnforcementPolicy()
        assert "tests/" in policy.simplified_registration_dirs

    def test_requires_full_registration_runtime(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.requires_full_registration("runtime/chain_validator.py") is True
        assert policy.requires_full_registration("runtime/reasoning_object.py") is True

    def test_requires_full_registration_governance(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.requires_full_registration("governance/provenance_schema.py") is True
        assert policy.requires_full_registration("governance/sunset_governance.py") is True

    def test_does_not_require_full_registration_for_tests(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.requires_full_registration("tests/test_something.py") is False

    def test_does_not_require_full_registration_for_engines(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.requires_full_registration("engines/report_engine.py") is False

    def test_requires_simplified_registration_tests(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.requires_simplified_registration("tests/test_property_chain.py") is True

    def test_does_not_require_simplified_for_runtime(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.requires_simplified_registration("runtime/chain_validator.py") is False

    def test_transient_exempt_pycache(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.is_transient_exempt("runtime/__pycache__/module.cpython-313.pyc") is True

    def test_transient_exempt_pytest_cache(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.is_transient_exempt("tests/.pytest_cache/v/cache/nodeids") is True

    def test_transient_exempt_init_py(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.is_transient_exempt("runtime/__init__.py") is True

    def test_transient_exempt_pyc_files(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.is_transient_exempt("runtime/chain_validator.pyc") is True

    def test_transient_exempt_coverage(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.is_transient_exempt(".coverage") is True

    def test_not_transient_exempt_normal_py(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.is_transient_exempt("runtime/chain_validator.py") is False
        assert policy.is_transient_exempt("governance/provenance_schema.py") is False

    def test_baseline_unregistered_count(self):
        policy = RegistrationEnforcementPolicy()
        assert policy.baseline_unregistered_count == 13


class TestRegistrationEnforcementResult:
    """Tests for RegistrationEnforcementResult dataclass."""

    def test_ci_warning_when_baseline_exceeded(self):
        result = RegistrationEnforcementResult(
            unregistered_count=15,
            baseline_exceeded=True,
        )
        msg = result.ci_warning_message
        assert msg is not None
        assert "::warning::" in msg
        assert "HARDENING 14" in msg
        assert "15" in msg

    def test_no_ci_warning_when_within_baseline(self):
        result = RegistrationEnforcementResult(
            unregistered_count=5,
            baseline_exceeded=False,
        )
        assert result.ci_warning_message is None

    def test_empty_result_defaults(self):
        result = RegistrationEnforcementResult()
        assert result.warnings == []
        assert result.unregistered_count == 0
        assert result.baseline_exceeded is False
        assert result.full_registration_violations == []
        assert result.simplified_registration_violations == []


class TestValidationOrchestratorEnforcement:
    """Integration tests for registration enforcement in ValidationOrchestrator."""

    def _create_orchestrator(self, registered_paths=None):
        """Create a mock orchestrator for testing."""
        mock_registry = MagicMock()
        mock_registry._loaded = True

        @dataclass
        class MockArtifact:
            file_path: str
            artifact_id: str = "mock"

        if registered_paths is None:
            registered_paths = []

        mock_registry.list_all_artifacts.return_value = [
            MockArtifact(file_path=p) for p in registered_paths
        ]

        mock_domain_registry = MagicMock()
        mock_lifecycle_manager = MagicMock()

        orchestrator = ValidationOrchestrator(
            artifact_registry=mock_registry,
            domain_registry=mock_domain_registry,
            lifecycle_manager=mock_lifecycle_manager,
            repo_root=Path("/fake/repo"),
        )
        return orchestrator

    def test_enforcement_detects_unregistered_runtime_file(self):
        orchestrator = self._create_orchestrator(registered_paths=[])
        
        result = orchestrator.validate_registration_enforcement(
            changed_files=[Path("runtime/new_module.py")]
        )
        
        assert len(result.full_registration_violations) == 1
        assert "runtime/new_module.py" in result.full_registration_violations
        assert any(w.warning_code == W800_REGISTRATION_REQUIRED for w in result.warnings)

    def test_enforcement_detects_unregistered_governance_file(self):
        orchestrator = self._create_orchestrator(registered_paths=[])
        
        result = orchestrator.validate_registration_enforcement(
            changed_files=[Path("governance/new_policy.py")]
        )
        
        assert len(result.full_registration_violations) == 1
        assert "governance/new_policy.py" in result.full_registration_violations

    def test_enforcement_detects_unregistered_test_file(self):
        orchestrator = self._create_orchestrator(registered_paths=[])
        
        result = orchestrator.validate_registration_enforcement(
            changed_files=[Path("tests/test_new_feature.py")]
        )
        
        assert len(result.simplified_registration_violations) == 1
        assert "tests/test_new_feature.py" in result.simplified_registration_violations
        assert any(w.warning_code == W802_SIMPLIFIED_REGISTRATION_MISSING for w in result.warnings)

    def test_enforcement_skips_transient_exempt(self):
        orchestrator = self._create_orchestrator(registered_paths=[])
        
        result = orchestrator.validate_registration_enforcement(
            changed_files=[Path("runtime/__init__.py")]
        )
        
        assert len(result.full_registration_violations) == 0
        assert len(result.warnings) == 0

    def test_enforcement_no_warning_for_registered_file(self):
        orchestrator = self._create_orchestrator(
            registered_paths=["runtime/chain_validator.py"]
        )
        
        result = orchestrator.validate_registration_enforcement(
            changed_files=[Path("runtime/chain_validator.py")]
        )
        
        assert len(result.full_registration_violations) == 0
        assert len(result.warnings) == 0

    def test_enforcement_baseline_exceeded_warning(self):
        orchestrator = self._create_orchestrator(registered_paths=[])
        
        # Create 14 unregistered files (exceeds baseline of 13)
        files = [Path(f"runtime/module_{i}.py") for i in range(14)]
        
        result = orchestrator.validate_registration_enforcement(changed_files=files)
        
        assert result.baseline_exceeded is True
        assert result.unregistered_count == 14
        assert any(w.warning_code == W801_UNREGISTERED_COUNT_INCREASE for w in result.warnings)

    def test_enforcement_baseline_not_exceeded(self):
        orchestrator = self._create_orchestrator(registered_paths=[])
        
        # Create 5 unregistered files (within baseline of 13)
        files = [Path(f"runtime/module_{i}.py") for i in range(5)]
        
        result = orchestrator.validate_registration_enforcement(changed_files=files)
        
        assert result.baseline_exceeded is False
        assert result.unregistered_count == 5

    def test_enforcement_mixed_file_types(self):
        orchestrator = self._create_orchestrator(
            registered_paths=["runtime/existing.py"]
        )
        
        files = [
            Path("runtime/existing.py"),       # registered - no warning
            Path("runtime/new_module.py"),      # unregistered runtime - full
            Path("tests/test_new.py"),          # unregistered test - simplified
            Path("runtime/__init__.py"),        # transient exempt - skip
        ]
        
        result = orchestrator.validate_registration_enforcement(changed_files=files)
        
        assert len(result.full_registration_violations) == 1
        assert len(result.simplified_registration_violations) == 1
        assert "runtime/new_module.py" in result.full_registration_violations
        assert "tests/test_new.py" in result.simplified_registration_violations
