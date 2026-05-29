"""Runtime Integrity Hash for detecting deployment drift.

Computes a SHA-256 fingerprint over behavior-defining files to detect
drift between CI validation and runtime execution. The hash covers
governance configuration, governance runtime modules, runtime pipeline
modules, and the engine registry — but NOT individual engine implementations.

Computation:
1. Resolve TARGET_PATHS (including glob patterns) to concrete file paths
2. Sort paths lexicographically for deterministic ordering
3. Canonicalize each file via HashCanonicalizer
4. Concatenate canonicalized content
5. Compute SHA-256 digest

CI produces the hash and persists it in GateSummary alongside git SHA.
Runtime verifies against last CI-computed hash; mismatch → DEGRADED event.

Requirements: 36.1, 36.2, 36.5, 36.6
"""

import glob
import os

from governance.hash_canonicalizer import HashCanonicalizer


class RuntimeIntegrityHash:
    """SHA-256 fingerprint for detecting deployment drift.

    Hashes behavior-defining files to detect changes between CI validation
    and runtime execution. Uses HashCanonicalizer for platform-independent
    deterministic content normalization.
    """

    TARGET_PATHS = [
        # Governance Configuration (SSOT)
        ".domainization/config.yaml",
        ".domainization/lifecycle_state_machine.yaml",
        ".domainization/domain_registry.yaml",
        ".domainization/artifact_registry.yaml",
        ".domainization/fail_mode_config.yaml",
        "governance/confidence_policy.yaml",
        # Governance Runtime (enforcement logic)
        "governance/*.py",
        # Runtime (pipeline logic)
        "runtime/*.py",
        # Engine Registry (dependency graph only — not engine implementations)
        "engines/engine_registry.py",
    ]

    def __init__(self, base_path: str, canonicalizer: HashCanonicalizer) -> None:
        """Initialize RuntimeIntegrityHash.

        Args:
            base_path: Root directory of the repository (used to resolve
                relative TARGET_PATHS).
            canonicalizer: HashCanonicalizer instance for platform-independent
                file content normalization.
        """
        self.base_path = base_path
        self.canonicalizer = canonicalizer

    def _resolve_paths(self) -> list[str]:
        """Resolve TARGET_PATHS (including globs) to concrete file paths.

        Expands glob patterns (e.g., 'governance/*.py') and filters to
        only existing files. Excludes __pycache__ directories and .pyc files.

        Returns:
            Sorted list of absolute file paths that exist on disk.
        """
        resolved = set()

        for pattern in self.TARGET_PATHS:
            full_pattern = os.path.join(self.base_path, pattern)

            if "*" in pattern:
                # Expand glob pattern
                matches = glob.glob(full_pattern)
                for match in matches:
                    if os.path.isfile(match) and "__pycache__" not in match:
                        resolved.add(match)
            else:
                # Direct file path
                if os.path.isfile(full_pattern):
                    resolved.add(full_pattern)

        return sorted(resolved)

    def compute(self) -> str:
        """Compute the runtime integrity hash.

        Resolves all target paths, canonicalizes their content via the
        HashCanonicalizer, and produces a SHA-256 digest.

        Returns:
            SHA-256 hex digest string prefixed with "sha256:".
            Returns "sha256:empty" if no target files are found.
        """
        file_paths = self._resolve_paths()

        if not file_paths:
            return "sha256:empty"

        return self.canonicalizer.compute_hash(file_paths)

    def verify_against(self, expected_hash: str) -> tuple[bool, dict]:
        """Verify current hash against an expected value.

        Computes the current hash and compares it to the expected hash.
        Returns match status and diagnostic details.

        Args:
            expected_hash: The expected SHA-256 hash (from CI artifact).

        Returns:
            Tuple of (match: bool, details: dict) where details contains:
            - current_hash: the computed hash
            - expected_hash: the provided expected hash
            - match: True if computed hash equals expected hash
            - details: Dict containing computed_hash, expected_hash,
              file_count, and mismatch info if hashes differ.
        """
        computed_hash = self.compute()
        resolved_paths = self._resolve_paths()

        match = computed_hash == expected_hash

        details: dict = {
            "computed_hash": computed_hash,
            "expected_hash": expected_hash,
            "match": match,
            "file_count": len(resolved_paths),
        }

        if not match:
            details["mismatch"] = {
                "reason": "Runtime file contents differ from CI-validated state",
                "resolved_files": [
                    os.path.relpath(p, self.base_path) for p in resolved_paths
                ],
            }

        return match, details
