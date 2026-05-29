"""Unit tests for governance/policy_versioner.py.

Tests the PolicyVersioner class including:
- Version computation (SHA-256 of combined sorted governance file contents)
- Change detection (comparing current vs previous version)
- Graceful handling of missing files
- Deterministic output
- Version string format

Requirements: 34.1, 34.2, 34.3, 34.4, 34.5, 34.6
"""

import hashlib
import os
import tempfile

import pytest

from governance.policy_versioner import PolicyVersioner


@pytest.fixture
def temp_project():
    """Create a temporary project directory with governance files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create directory structure
        os.makedirs(os.path.join(tmpdir, ".domainization"))
        os.makedirs(os.path.join(tmpdir, "governance"))

        # Create governance files with known content
        files = {
            ".domainization/config.yaml": "enforcement_mode: observability\n",
            ".domainization/lifecycle_state_machine.yaml": "states:\n  active: {}\n",
            ".domainization/domain_registry.yaml": "domains:\n  core: {}\n",
            "governance/confidence_policy.yaml": "policy_name: default\n",
        }
        for rel_path, content in files.items():
            full_path = os.path.join(tmpdir, rel_path)
            with open(full_path, "w") as f:
                f.write(content)

        yield tmpdir


@pytest.fixture
def empty_project():
    """Create a temporary project directory with no governance files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestPolicyVersionerComputeVersion:
    """Tests for PolicyVersioner.compute_version()."""

    def test_returns_sha256_prefixed_string(self, temp_project):
        """Version string starts with 'sha256:' prefix."""
        pv = PolicyVersioner(temp_project)
        version = pv.compute_version()
        assert version.startswith("sha256:")

    def test_returns_valid_hex_digest(self, temp_project):
        """Version contains a valid 64-character hex digest after prefix."""
        pv = PolicyVersioner(temp_project)
        version = pv.compute_version()
        hex_part = version.removeprefix("sha256:")
        assert len(hex_part) == 64
        # Verify it's valid hex
        int(hex_part, 16)

    def test_deterministic_output(self, temp_project):
        """Multiple calls produce the same version."""
        pv = PolicyVersioner(temp_project)
        v1 = pv.compute_version()
        v2 = pv.compute_version()
        assert v1 == v2

    def test_sorts_files_alphabetically(self, temp_project):
        """Files are sorted alphabetically before concatenation."""
        pv = PolicyVersioner(temp_project)
        version = pv.compute_version()

        # Manually compute expected hash with sorted files
        sorted_files = sorted(PolicyVersioner.GOVERNANCE_FILES)
        combined = b""
        for rel_path in sorted_files:
            full_path = os.path.join(temp_project, rel_path)
            with open(full_path, "rb") as f:
                combined += f.read()

        expected = "sha256:" + hashlib.sha256(combined).hexdigest()
        assert version == expected

    def test_content_change_produces_different_version(self, temp_project):
        """Changing file content produces a different version."""
        pv = PolicyVersioner(temp_project)
        v1 = pv.compute_version()

        # Modify one governance file
        config_path = os.path.join(temp_project, ".domainization/config.yaml")
        with open(config_path, "w") as f:
            f.write("enforcement_mode: hard\n")

        v2 = pv.compute_version()
        assert v1 != v2

    def test_empty_directory_produces_empty_content_hash(self, empty_project):
        """When no files exist, produces hash of empty content."""
        pv = PolicyVersioner(empty_project)
        version = pv.compute_version()
        expected = "sha256:" + hashlib.sha256(b"").hexdigest()
        assert version == expected


class TestPolicyVersionerDetectChange:
    """Tests for PolicyVersioner.detect_change()."""

    def test_no_change_when_version_matches(self, temp_project):
        """Returns False when previous version matches current."""
        pv = PolicyVersioner(temp_project)
        current = pv.compute_version()
        assert pv.detect_change(current) is False

    def test_change_detected_with_different_version(self, temp_project):
        """Returns True when previous version differs from current."""
        pv = PolicyVersioner(temp_project)
        fake_previous = "sha256:0" * 64
        assert pv.detect_change(fake_previous) is True

    def test_change_detected_after_file_modification(self, temp_project):
        """Returns True after a governance file is modified."""
        pv = PolicyVersioner(temp_project)
        original_version = pv.compute_version()

        # Modify a governance file
        config_path = os.path.join(temp_project, ".domainization/config.yaml")
        with open(config_path, "a") as f:
            f.write("# new comment\n")

        assert pv.detect_change(original_version) is True


class TestPolicyVersionerGetCurrentVersion:
    """Tests for PolicyVersioner.get_current_version()."""

    def test_matches_compute_version(self, temp_project):
        """get_current_version returns same result as compute_version."""
        pv = PolicyVersioner(temp_project)
        assert pv.get_current_version() == pv.compute_version()

    def test_returns_sha256_format(self, temp_project):
        """Returns properly formatted version string."""
        pv = PolicyVersioner(temp_project)
        version = pv.get_current_version()
        assert version.startswith("sha256:")
        assert len(version) == 71  # "sha256:" (7) + 64 hex chars


class TestPolicyVersionerMissingFiles:
    """Tests for graceful handling of missing governance files."""

    def test_partial_files_still_produces_version(self, temp_project):
        """Version is computed even when some files are missing."""
        # Remove one file
        os.remove(os.path.join(temp_project, "governance/confidence_policy.yaml"))

        pv = PolicyVersioner(temp_project)
        version = pv.compute_version()
        assert version.startswith("sha256:")
        assert len(version) == 71

    def test_missing_file_does_not_raise(self, empty_project):
        """Missing files are skipped without raising exceptions."""
        pv = PolicyVersioner(empty_project)
        # Should not raise
        version = pv.compute_version()
        assert version.startswith("sha256:")


class TestPolicyVersionerGovernanceFiles:
    """Tests for the GOVERNANCE_FILES class attribute."""

    def test_contains_expected_files(self):
        """GOVERNANCE_FILES contains the four required governance files."""
        expected = {
            ".domainization/config.yaml",
            ".domainization/lifecycle_state_machine.yaml",
            ".domainization/domain_registry.yaml",
            "governance/confidence_policy.yaml",
        }
        assert set(PolicyVersioner.GOVERNANCE_FILES) == expected

    def test_file_count(self):
        """GOVERNANCE_FILES contains exactly 4 files."""
        assert len(PolicyVersioner.GOVERNANCE_FILES) == 4


class TestPolicyVersionerIntegration:
    """Integration tests using the actual project governance files."""

    def test_real_project_version(self):
        """Compute version against actual project files."""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pv = PolicyVersioner(base_path)
        version = pv.compute_version()
        assert version.startswith("sha256:")
        # Should not be empty hash since real files exist
        empty_hash = "sha256:" + hashlib.sha256(b"").hexdigest()
        assert version != empty_hash
