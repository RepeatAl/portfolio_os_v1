"""Governance policy versioner for content-hash-based policy identification.

Computes a SHA-256 fingerprint of combined governance configuration files,
enabling historical decision context by embedding the active policy version
in GateResult and LedgerEntry records.

This module is pure observation — it computes a fingerprint, it does NOT
make decisions. Severity assignment and blocking decisions belong to
GateFramework/EnforcementMode, not here.

Computation:
    1. Sort governance files alphabetically by path
    2. Read each file's content (skip missing files with warning)
    3. Concatenate all contents
    4. SHA-256 hash the concatenation
    5. Return as "sha256:<hex_digest>"

Requirements: 34.1, 34.2, 34.3, 34.4, 34.5, 34.6
"""

from __future__ import annotations

import hashlib
import logging
import os

logger = logging.getLogger(__name__)


class PolicyVersioner:
    """Content-hash-based governance policy versioner.

    Computes a deterministic version identifier from the combined contents
    of governance configuration files. The version changes whenever any
    governance rule, severity mapping, gate configuration, or enforcement
    mode definition changes.

    The version string format is "sha256:<hex_digest>" for consistency
    with other governance hashes.

    Attributes:
        GOVERNANCE_FILES: List of governance file paths relative to base_path.
    """

    GOVERNANCE_FILES: list[str] = [
        ".domainization/config.yaml",
        ".domainization/lifecycle_state_machine.yaml",
        ".domainization/domain_registry.yaml",
        "governance/confidence_policy.yaml",
    ]

    def __init__(self, base_path: str) -> None:
        """Initialize the policy versioner with a base path.

        Args:
            base_path: Root directory of the project. Governance files
                       are resolved relative to this path.
        """
        self._base_path = base_path

    @property
    def base_path(self) -> str:
        """The base path used for resolving governance file paths."""
        return self._base_path

    def compute_version(self) -> str:
        """Compute the governance policy version as SHA-256 of combined file contents.

        Algorithm:
            1. Sort GOVERNANCE_FILES alphabetically by path
            2. Read each file's content (skip missing files with warning)
            3. Concatenate all contents
            4. SHA-256 hash the concatenation
            5. Return as "sha256:<hex_digest>"

        Returns:
            A version string in the format "sha256:<hex_digest>".
            If no governance files are readable, returns a hash of
            empty content (deterministic zero-input hash).
        """
        sorted_files = sorted(self.GOVERNANCE_FILES)
        combined_content = b""

        for relative_path in sorted_files:
            full_path = os.path.join(self._base_path, relative_path)
            try:
                with open(full_path, "rb") as f:
                    combined_content += f.read()
            except FileNotFoundError:
                logger.warning(
                    "Governance file not found, skipping: %s", relative_path
                )
            except OSError as exc:
                logger.warning(
                    "Cannot read governance file %s: %s", relative_path, exc
                )

        digest = hashlib.sha256(combined_content).hexdigest()
        return f"sha256:{digest}"

    def detect_change(self, previous_version: str) -> bool:
        """Detect whether the governance policy has changed.

        Compares the current computed version against a previously
        stored version string.

        Args:
            previous_version: The version string from a prior computation,
                              in "sha256:<hex_digest>" format.

        Returns:
            True if the current version differs from previous_version,
            False if they are identical.
        """
        current = self.compute_version()
        return current != previous_version

    def get_current_version(self) -> str:
        """Get the current governance policy version for embedding.

        Convenience method for embedding in GateResult and LedgerEntry
        records. Equivalent to compute_version() but named for clarity
        at call sites.

        Returns:
            A version string in the format "sha256:<hex_digest>".
        """
        return self.compute_version()
