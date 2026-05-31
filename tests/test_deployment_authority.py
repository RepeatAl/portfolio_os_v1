"""Unit tests for governance/deployment_authority.py.

Covers deterministic edge cases: valid/invalid YAML loading, role count
validation, unvalidated deployment WARNING, and final 3-pair forbidden set
enforcement.

Does NOT duplicate property tests (round-trip, topology constraint across
generated inputs, provenance round-trip).

CTO Decision (2026-05-31): FORBIDDEN_AUTHORITY_PAIRS = 3 pairs (additive):
  1. (mutate_governance, deploy)
  2. (deploy, change_enforcement_mode)
  3. (change_enforcement_mode, execute_override)

Validates: Requirements 4.4, 5.3, 6.4
"""

from __future__ import annotations

import os
import tempfile

import pytest
import yaml

from governance.deployment_authority import (
    Authority,
    AuthorityAssignment,
    AuthorityRole,
    DeploymentAuthorityModel,
    DeployProvenance,
    FORBIDDEN_AUTHORITY_PAIRS,
)
from governance.mutation_audit_ledger import MutationAuditLedger


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_dir():
    """Provide a temporary directory for test YAML files."""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def ledger(tmp_dir: str) -> MutationAuditLedger:
    """Create a temporary ledger for testing."""
    ledger_path = os.path.join(tmp_dir, "ledger.yaml")
    return MutationAuditLedger(ledger_path)


@pytest.fixture
def valid_model_yaml(tmp_dir: str) -> str:
    """Create a valid deployment_authority_model.yaml with 3 roles."""
    path = os.path.join(tmp_dir, "deployment_authority_model.yaml")
    data = {
        "schema_version": "1.0.0",
        "roles": [
            {"role": "OWNER", "authorities": ["mutate_governance", "change_enforcement_mode"]},
            {"role": "CI", "authorities": ["deploy", "accept_runtime_hash"]},
            {"role": "RUNTIME", "authorities": ["execute_override", "change_fail_mode"]},
        ],
    }
    with open(path, "w") as f:
        yaml.dump(data, f)
    return path


# ---------------------------------------------------------------------------
# Test: Valid YAML Loading
# ---------------------------------------------------------------------------


class TestValidYAMLLoading:
    """Tests for successful loading of well-formed authority model."""

    def test_load_valid_model(self, valid_model_yaml: str):
        """Valid YAML with 3 roles loads correctly."""
        model = DeploymentAuthorityModel(valid_model_yaml)
        assignments = model.load_model()

        assert len(assignments) == 3
        roles = {a.role for a in assignments}
        assert roles == {AuthorityRole.OWNER, AuthorityRole.CI, AuthorityRole.RUNTIME}

    def test_owner_has_correct_authorities(self, valid_model_yaml: str):
        """OWNER role holds mutate_governance and change_enforcement_mode."""
        model = DeploymentAuthorityModel(valid_model_yaml)
        model.load_model()

        assert model.check_authority(AuthorityRole.OWNER, Authority.MUTATE_GOVERNANCE) is True
        assert model.check_authority(AuthorityRole.OWNER, Authority.CHANGE_ENFORCEMENT_MODE) is True
        assert model.check_authority(AuthorityRole.OWNER, Authority.DEPLOY) is False

    def test_ci_has_correct_authorities(self, valid_model_yaml: str):
        """CI role holds deploy and accept_runtime_hash."""
        model = DeploymentAuthorityModel(valid_model_yaml)
        model.load_model()

        assert model.check_authority(AuthorityRole.CI, Authority.DEPLOY) is True
        assert model.check_authority(AuthorityRole.CI, Authority.ACCEPT_RUNTIME_HASH) is True
        assert model.check_authority(AuthorityRole.CI, Authority.MUTATE_GOVERNANCE) is False

    def test_runtime_has_correct_authorities(self, valid_model_yaml: str):
        """RUNTIME role holds execute_override and change_fail_mode."""
        model = DeploymentAuthorityModel(valid_model_yaml)
        model.load_model()

        assert model.check_authority(AuthorityRole.RUNTIME, Authority.EXECUTE_OVERRIDE) is True
        assert model.check_authority(AuthorityRole.RUNTIME, Authority.CHANGE_FAIL_MODE) is True
        assert model.check_authority(AuthorityRole.RUNTIME, Authority.DEPLOY) is False

    def test_validate_at_init_succeeds_for_valid_model(
        self, valid_model_yaml: str, ledger: MutationAuditLedger
    ):
        """validate_at_init succeeds for a valid model with no topology violations."""
        model = DeploymentAuthorityModel(valid_model_yaml, ledger=ledger)
        is_valid, errors = model.validate_at_init()

        assert is_valid is True
        assert errors == []


# ---------------------------------------------------------------------------
# Test: Invalid YAML Loading
# ---------------------------------------------------------------------------


class TestInvalidYAMLLoading:
    """Tests for malformed or structurally invalid YAML files."""

    def test_missing_roles_key(self, tmp_dir: str, ledger: MutationAuditLedger):
        """YAML without 'roles' key causes validate_at_init to fail."""
        path = os.path.join(tmp_dir, "bad.yaml")
        with open(path, "w") as f:
            yaml.dump({"schema_version": "1.0.0", "not_roles": []}, f)

        model = DeploymentAuthorityModel(path, ledger=ledger)
        is_valid, errors = model.validate_at_init()

        assert is_valid is False
        assert len(errors) >= 1
        assert any("roles" in e.lower() for e in errors)

    def test_invalid_role_name(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Invalid role name causes validate_at_init to fail."""
        path = os.path.join(tmp_dir, "bad_role.yaml")
        data = {
            "schema_version": "1.0.0",
            "roles": [
                {"role": "INVALID_ROLE", "authorities": ["deploy"]},
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        model = DeploymentAuthorityModel(path, ledger=ledger)
        is_valid, errors = model.validate_at_init()

        assert is_valid is False

    def test_invalid_authority_name(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Invalid authority name causes validate_at_init to fail."""
        path = os.path.join(tmp_dir, "bad_auth.yaml")
        data = {
            "schema_version": "1.0.0",
            "roles": [
                {"role": "OWNER", "authorities": ["nonexistent_authority"]},
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        model = DeploymentAuthorityModel(path, ledger=ledger)
        is_valid, errors = model.validate_at_init()

        assert is_valid is False

    def test_missing_file(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Non-existent file causes validate_at_init to fail."""
        path = os.path.join(tmp_dir, "nonexistent.yaml")
        model = DeploymentAuthorityModel(path, ledger=ledger)
        is_valid, errors = model.validate_at_init()

        assert is_valid is False
        assert len(errors) >= 1


# ---------------------------------------------------------------------------
# Test: Role Count Validation
# ---------------------------------------------------------------------------


class TestRoleCountValidation:
    """Tests for role count and assignment structure."""

    def test_model_with_role_id_key(self, tmp_dir: str):
        """Model using 'role_id' key (actual YAML format) loads correctly."""
        path = os.path.join(tmp_dir, "role_id_format.yaml")
        data = {
            "schema_version": "1.0.0",
            "roles": [
                {"role_id": "OWNER", "authorities": ["mutate_governance", "change_enforcement_mode"]},
                {"role_id": "CI", "authorities": ["deploy", "accept_runtime_hash"]},
                {"role_id": "RUNTIME", "authorities": ["execute_override", "change_fail_mode"]},
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        model = DeploymentAuthorityModel(path)
        assignments = model.load_model()

        assert len(assignments) == 3

    def test_check_authority_returns_false_for_unknown_role(self, valid_model_yaml: str):
        """check_authority returns False when role has no assignments loaded."""
        model = DeploymentAuthorityModel(valid_model_yaml)
        # Don't load model — no assignments
        assert model.check_authority(AuthorityRole.OWNER, Authority.DEPLOY) is False


# ---------------------------------------------------------------------------
# Test: Forbidden Authority Pairs (3-pair CTO Decision)
# ---------------------------------------------------------------------------


class TestForbiddenAuthorityPairs:
    """Tests for the final 3-pair forbidden set enforcement.

    CTO Decision (2026-05-31): FORBIDDEN_AUTHORITY_PAIRS is additive and stricter.
    Final set = 3 pairs:
      1. (mutate_governance, deploy)
      2. (deploy, change_enforcement_mode)
      3. (change_enforcement_mode, execute_override)
    """

    def test_forbidden_pairs_constant_has_three_pairs(self):
        """FORBIDDEN_AUTHORITY_PAIRS contains exactly 3 pairs."""
        assert len(FORBIDDEN_AUTHORITY_PAIRS) == 3

    def test_pair_1_mutate_governance_and_deploy(self):
        """Pair 1: (mutate_governance, deploy) is in the forbidden set."""
        assert (Authority.MUTATE_GOVERNANCE, Authority.DEPLOY) in FORBIDDEN_AUTHORITY_PAIRS

    def test_pair_2_deploy_and_change_enforcement_mode(self):
        """Pair 2: (deploy, change_enforcement_mode) is in the forbidden set."""
        assert (Authority.DEPLOY, Authority.CHANGE_ENFORCEMENT_MODE) in FORBIDDEN_AUTHORITY_PAIRS

    def test_pair_3_change_enforcement_mode_and_execute_override(self):
        """Pair 3: (change_enforcement_mode, execute_override) is in the forbidden set."""
        assert (Authority.CHANGE_ENFORCEMENT_MODE, Authority.EXECUTE_OVERRIDE) in FORBIDDEN_AUTHORITY_PAIRS

    def test_topology_violation_pair_1(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Role holding mutate_governance + deploy is rejected."""
        path = os.path.join(tmp_dir, "violation_p1.yaml")
        data = {
            "schema_version": "1.0.0",
            "roles": [
                {"role": "OWNER", "authorities": ["mutate_governance", "deploy"]},
                {"role": "CI", "authorities": ["accept_runtime_hash"]},
                {"role": "RUNTIME", "authorities": ["execute_override", "change_fail_mode"]},
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        model = DeploymentAuthorityModel(path, ledger=ledger)
        is_valid, errors = model.validate_at_init()

        assert is_valid is False
        assert any("mutate_governance" in e and "deploy" in e for e in errors)

    def test_topology_violation_pair_2(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Role holding deploy + change_enforcement_mode is rejected."""
        path = os.path.join(tmp_dir, "violation_p2.yaml")
        data = {
            "schema_version": "1.0.0",
            "roles": [
                {"role": "OWNER", "authorities": ["mutate_governance"]},
                {"role": "CI", "authorities": ["deploy", "change_enforcement_mode"]},
                {"role": "RUNTIME", "authorities": ["execute_override", "change_fail_mode"]},
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        model = DeploymentAuthorityModel(path, ledger=ledger)
        is_valid, errors = model.validate_at_init()

        assert is_valid is False
        assert any("deploy" in e and "change_enforcement_mode" in e for e in errors)

    def test_topology_violation_pair_3(self, tmp_dir: str, ledger: MutationAuditLedger):
        """Role holding change_enforcement_mode + execute_override is rejected."""
        path = os.path.join(tmp_dir, "violation_p3.yaml")
        data = {
            "schema_version": "1.0.0",
            "roles": [
                {"role": "OWNER", "authorities": ["mutate_governance", "change_enforcement_mode", "execute_override"]},
                {"role": "CI", "authorities": ["deploy", "accept_runtime_hash"]},
                {"role": "RUNTIME", "authorities": ["change_fail_mode"]},
            ],
        }
        with open(path, "w") as f:
            yaml.dump(data, f)

        model = DeploymentAuthorityModel(path, ledger=ledger)
        is_valid, errors = model.validate_at_init()

        assert is_valid is False
        assert any("change_enforcement_mode" in e and "execute_override" in e for e in errors)

    def test_valid_topology_passes(self, valid_model_yaml: str):
        """Standard 3-role model with no forbidden pairs passes topology check."""
        model = DeploymentAuthorityModel(valid_model_yaml)
        model.load_model()
        is_valid, violations = model.validate_topology()

        assert is_valid is True
        assert violations == []


# ---------------------------------------------------------------------------
# Test: Unvalidated Deployment WARNING
# ---------------------------------------------------------------------------


class TestUnvalidatedDeploymentWarning:
    """Tests for WARNING severity on unvalidated (manual) deployments."""

    def test_unvalidated_provenance_emits_warning(
        self, valid_model_yaml: str, ledger: MutationAuditLedger
    ):
        """Recording unvalidated provenance (is_validated=False) emits WARNING to ledger."""
        model = DeploymentAuthorityModel(valid_model_yaml, ledger=ledger)
        model.load_model()

        provenance = DeployProvenance(
            deploy_id="manual-deploy-001",
            timestamp="2026-06-01T14:00:00Z",
            actor_role=AuthorityRole.OWNER,
            authority_used=Authority.DEPLOY,
            is_validated=False,
            runtime_hash="sha256:abc123",
            details={"reason": "manual hotfix"},
        )

        model.record_deploy_provenance(provenance)

        # Check ledger has a WARNING entry
        entries = ledger.query_by_event_type("deployment_authorized")
        assert len(entries) >= 1
        warning_entries = [e for e in entries if e.severity == "WARNING"]
        assert len(warning_entries) >= 1

    def test_validated_provenance_emits_info(
        self, valid_model_yaml: str, ledger: MutationAuditLedger
    ):
        """Recording validated provenance (is_validated=True) emits INFO to ledger."""
        model = DeploymentAuthorityModel(valid_model_yaml, ledger=ledger)
        model.load_model()

        provenance = DeployProvenance(
            deploy_id="ci-deploy-001",
            timestamp="2026-06-01T14:00:00Z",
            actor_role=AuthorityRole.CI,
            authority_used=Authority.DEPLOY,
            is_validated=True,
            runtime_hash="sha256:def456",
            details={"ci_run": "12345"},
        )

        model.record_deploy_provenance(provenance)

        entries = ledger.query_by_event_type("deployment_authorized")
        assert len(entries) >= 1
        info_entries = [e for e in entries if e.severity == "INFO"]
        assert len(info_entries) >= 1

    def test_no_ledger_does_not_crash(self, valid_model_yaml: str):
        """Recording provenance without a ledger does not raise."""
        model = DeploymentAuthorityModel(valid_model_yaml, ledger=None)
        model.load_model()

        provenance = DeployProvenance(
            deploy_id="no-ledger-deploy",
            timestamp="2026-06-01T14:00:00Z",
            actor_role=AuthorityRole.CI,
            authority_used=Authority.DEPLOY,
            is_validated=True,
            runtime_hash="sha256:ghi789",
            details={},
        )

        # Should not raise
        model.record_deploy_provenance(provenance)
