"""Confidence Degradation Policy — configurable formula for confidence reduction.

Defines how confidence_level is reduced when upstream signal categories are
missing or degraded. Policy parameters are loaded from a YAML config file,
allowing governance changes without modifying schema or engine source code.

Requirements: 19.1, 19.2, 19.3, 19.4
"""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class ConfidenceDegradationPolicy:
    """Configurable policy for confidence degradation when inputs are missing.

    Attributes:
        base_ceiling: Maximum confidence when degradation applies (default 50).
        penalty_per_missing_category: Points deducted per missing signal category (default 10).
        minimum_floor: Confidence never goes below this value (default 0).
        version: Policy version for governance tracking.
    """

    base_ceiling: int = 50
    penalty_per_missing_category: int = 10
    minimum_floor: int = 0
    version: str = "1.0.0"

    def compute(self, missing_category_count: int) -> int:
        """Return degraded confidence level.

        Formula: max(minimum_floor, base_ceiling - (penalty_per_missing_category * missing_category_count))

        Args:
            missing_category_count: Number of signal categories that are unavailable.

        Returns:
            Degraded confidence level as an integer between minimum_floor and base_ceiling.
        """
        return max(
            self.minimum_floor,
            self.base_ceiling - (self.penalty_per_missing_category * missing_category_count),
        )

    @classmethod
    def load(cls, config_path: str = "governance/confidence_policy.yaml") -> "ConfidenceDegradationPolicy":
        """Load policy from YAML config file.

        If the config file does not exist, returns the default policy.

        Args:
            config_path: Path to the YAML configuration file.

        Returns:
            ConfidenceDegradationPolicy instance with values from config or defaults.
        """
        path = Path(config_path)
        if not path.exists():
            return cls()

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data or not isinstance(data, dict):
            return cls()

        return cls(
            base_ceiling=data.get("base_ceiling", 50),
            penalty_per_missing_category=data.get("penalty_per_missing_category", 10),
            minimum_floor=data.get("minimum_floor", 0),
            version=data.get("version", "1.0.0"),
        )
