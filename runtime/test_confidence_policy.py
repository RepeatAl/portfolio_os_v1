"""Unit tests for runtime/confidence_policy.py.

Validates the confidence degradation policy computation and YAML loading.
Requirements: 19.1, 19.2, 19.3, 19.4
"""

import os
import tempfile

import yaml

from runtime.confidence_policy import ConfidenceDegradationPolicy


class TestConfidenceDegradationPolicyDefaults:
    """Tests for default policy values."""

    def test_default_base_ceiling(self):
        policy = ConfidenceDegradationPolicy()
        assert policy.base_ceiling == 50

    def test_default_penalty_per_missing_category(self):
        policy = ConfidenceDegradationPolicy()
        assert policy.penalty_per_missing_category == 10

    def test_default_minimum_floor(self):
        policy = ConfidenceDegradationPolicy()
        assert policy.minimum_floor == 0

    def test_default_version(self):
        policy = ConfidenceDegradationPolicy()
        assert policy.version == "1.0.0"


class TestConfidenceDegradationCompute:
    """Tests for the compute() method."""

    def test_zero_missing_returns_base_ceiling(self):
        policy = ConfidenceDegradationPolicy()
        assert policy.compute(0) == 50

    def test_one_missing_deducts_penalty(self):
        policy = ConfidenceDegradationPolicy()
        assert policy.compute(1) == 40

    def test_two_missing_deducts_double_penalty(self):
        policy = ConfidenceDegradationPolicy()
        assert policy.compute(2) == 30

    def test_five_missing_returns_zero(self):
        policy = ConfidenceDegradationPolicy()
        assert policy.compute(5) == 0

    def test_more_than_five_missing_clamps_to_floor(self):
        policy = ConfidenceDegradationPolicy()
        assert policy.compute(10) == 0

    def test_custom_policy_values(self):
        policy = ConfidenceDegradationPolicy(
            base_ceiling=80,
            penalty_per_missing_category=15,
            minimum_floor=10,
        )
        assert policy.compute(0) == 80
        assert policy.compute(1) == 65
        assert policy.compute(4) == 20
        assert policy.compute(5) == 10  # Clamped to floor

    def test_minimum_floor_is_respected(self):
        policy = ConfidenceDegradationPolicy(
            base_ceiling=30,
            penalty_per_missing_category=20,
            minimum_floor=5,
        )
        # 30 - (20 * 2) = -10, but floor is 5
        assert policy.compute(2) == 5

    def test_compute_returns_integer(self):
        policy = ConfidenceDegradationPolicy()
        result = policy.compute(3)
        assert isinstance(result, int)


class TestConfidenceDegradationLoad:
    """Tests for the load() class method."""

    def test_load_returns_default_when_file_missing(self):
        policy = ConfidenceDegradationPolicy.load("/nonexistent/path/policy.yaml")
        assert policy.base_ceiling == 50
        assert policy.penalty_per_missing_category == 10
        assert policy.minimum_floor == 0
        assert policy.version == "1.0.0"

    def test_load_from_yaml_file(self):
        config = {
            "base_ceiling": 70,
            "penalty_per_missing_category": 5,
            "minimum_floor": 10,
            "version": "2.0.0",
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config, f)
            tmp_path = f.name

        try:
            policy = ConfidenceDegradationPolicy.load(tmp_path)
            assert policy.base_ceiling == 70
            assert policy.penalty_per_missing_category == 5
            assert policy.minimum_floor == 10
            assert policy.version == "2.0.0"
        finally:
            os.unlink(tmp_path)

    def test_load_partial_config_uses_defaults(self):
        config = {"base_ceiling": 60}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config, f)
            tmp_path = f.name

        try:
            policy = ConfidenceDegradationPolicy.load(tmp_path)
            assert policy.base_ceiling == 60
            assert policy.penalty_per_missing_category == 10  # default
            assert policy.minimum_floor == 0  # default
            assert policy.version == "1.0.0"  # default
        finally:
            os.unlink(tmp_path)

    def test_load_empty_file_returns_default(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("")
            tmp_path = f.name

        try:
            policy = ConfidenceDegradationPolicy.load(tmp_path)
            assert policy.base_ceiling == 50
            assert policy.penalty_per_missing_category == 10
            assert policy.minimum_floor == 0
        finally:
            os.unlink(tmp_path)

    def test_load_from_project_governance_file(self):
        """Test loading from the actual governance config file."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, "governance", "confidence_policy.yaml")
        if os.path.exists(config_path):
            policy = ConfidenceDegradationPolicy.load(config_path)
            assert policy.base_ceiling == 50
            assert policy.penalty_per_missing_category == 10
            assert policy.minimum_floor == 0
            assert policy.version == "1.0.0"
