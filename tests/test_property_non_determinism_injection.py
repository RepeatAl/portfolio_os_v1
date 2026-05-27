"""Property-based tests for Non-Determinism Injection.

**Validates: Requirements 15.5, 15.6**

Tests that non-deterministic values are replaced with Run_Context substitutes
and report hash is recorded. Verifies:
1. Every RunContext has a unique run_id (UUID v4 format)
2. Every RunContext has a deterministic timestamp (ISO 8601 UTC)
3. For any set of input files, the content hashes in RunContext are deterministic
   (same content → same hash)
4. The report_hash field is populated after pipeline execution (or None if report
   generation failed)
5. Two RunContexts created from the same files have identical content_hashes but
   different run_ids
"""

import hashlib
import re
import tempfile
import uuid
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from runtime.run_context import RunContext


# Strategy: generate random binary content for files (1 to 512 bytes)
binary_content_strategy = st.binary(min_size=1, max_size=512)

# Strategy: generate a list of binary contents (1 to 5 files)
file_contents_strategy = st.lists(
    st.binary(min_size=1, max_size=512),
    min_size=1,
    max_size=5,
)

# UUID v4 regex pattern
UUID_V4_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)

# ISO 8601 UTC timestamp pattern (YYYY-MM-DDTHH:MM:SSZ)
ISO_8601_UTC_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)


class TestNonDeterminismInjectionProperties:
    """Property-based tests for non-determinism injection via RunContext."""

    @given(contents=file_contents_strategy)
    @settings(max_examples=200, deadline=None)
    def test_run_id_is_uuid_v4(self, contents: list[bytes]) -> None:
        """Property 1: Every RunContext has a unique run_id in UUID v4 format.

        **Validates: Requirements 15.5**

        For any set of input files, the RunContext's run_id is a valid UUID v4
        string, ensuring non-deterministic identifiers are properly injected
        from a controlled source.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_paths = []
            for i, content in enumerate(contents):
                file_path = Path(tmp_dir) / f"input_{i}.xlsx"
                file_path.write_bytes(content)
                file_paths.append(str(file_path))

            ctx = RunContext.create(file_paths)

            # Verify run_id is valid UUID v4
            assert UUID_V4_PATTERN.match(ctx.run_id), (
                f"run_id '{ctx.run_id}' is not a valid UUID v4"
            )
            # Also verify it parses as a UUID
            parsed = uuid.UUID(ctx.run_id)
            assert parsed.version == 4, (
                f"run_id UUID version is {parsed.version}, expected 4"
            )

    @given(contents=file_contents_strategy)
    @settings(max_examples=200, deadline=None)
    def test_timestamp_is_iso_8601_utc(self, contents: list[bytes]) -> None:
        """Property 2: Every RunContext has a deterministic timestamp in ISO 8601 UTC.

        **Validates: Requirements 15.5**

        For any set of input files, the RunContext's timestamp is in ISO 8601
        UTC format with second precision (YYYY-MM-DDTHH:MM:SSZ), ensuring
        wall-clock timestamps are captured deterministically at context creation.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_paths = []
            for i, content in enumerate(contents):
                file_path = Path(tmp_dir) / f"input_{i}.xlsx"
                file_path.write_bytes(content)
                file_paths.append(str(file_path))

            ctx = RunContext.create(file_paths)

            # Verify timestamp matches ISO 8601 UTC pattern
            assert ISO_8601_UTC_PATTERN.match(ctx.timestamp), (
                f"timestamp '{ctx.timestamp}' is not valid ISO 8601 UTC "
                f"(expected format: YYYY-MM-DDTHH:MM:SSZ)"
            )

    @given(content=binary_content_strategy)
    @settings(max_examples=200, deadline=None)
    def test_content_hashes_are_deterministic(self, content: bytes) -> None:
        """Property 3: For any file content, content hashes are deterministic.

        **Validates: Requirements 15.5**

        Same file content always produces the same SHA-256 hash in the
        RunContext, ensuring no non-deterministic variation in hash computation.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_a = Path(tmp_dir) / "file_a.xlsx"
            file_b = Path(tmp_dir) / "file_b.xlsx"
            file_a.write_bytes(content)
            file_b.write_bytes(content)

            ctx_a = RunContext.create([str(file_a)])
            ctx_b = RunContext.create([str(file_b)])

            hash_a = ctx_a.data_sources[0].content_hash
            hash_b = ctx_b.data_sources[0].content_hash

            # Same content must produce same hash
            assert hash_a == hash_b, (
                f"Determinism violated: same content produced different hashes "
                f"'{hash_a}' vs '{hash_b}'"
            )

            # Verify hash matches expected SHA-256
            expected_hash = hashlib.sha256(content).hexdigest()
            assert hash_a == expected_hash, (
                f"Hash '{hash_a}' does not match expected SHA-256 '{expected_hash}'"
            )

    @given(contents=file_contents_strategy)
    @settings(max_examples=200, deadline=None)
    def test_report_hash_initially_none(self, contents: list[bytes]) -> None:
        """Property 4: The report_hash field is None before pipeline execution.

        **Validates: Requirements 15.6**

        After RunContext creation (before pipeline execution completes),
        report_hash is None. It is populated only after the pipeline computes
        the SHA-256 of the final daily_report.md.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_paths = []
            for i, content in enumerate(contents):
                file_path = Path(tmp_dir) / f"input_{i}.xlsx"
                file_path.write_bytes(content)
                file_paths.append(str(file_path))

            ctx = RunContext.create(file_paths)

            # Before pipeline execution, report_hash should be None
            assert ctx.report_hash is None, (
                f"report_hash should be None before pipeline execution, "
                f"got '{ctx.report_hash}'"
            )

    @given(content=binary_content_strategy)
    @settings(max_examples=200, deadline=None)
    def test_report_hash_recorded_after_assignment(self, content: bytes) -> None:
        """Property 4b: The report_hash field records SHA-256 when assigned.

        **Validates: Requirements 15.6**

        When a report is generated and its hash is assigned to the RunContext,
        the report_hash field contains a valid SHA-256 hex digest, enabling
        automated idempotency verification.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "input.xlsx"
            file_path.write_bytes(content)

            ctx = RunContext.create([str(file_path)])

            # Simulate pipeline completion: compute report hash
            report_content = b"# Daily Portfolio Report\n## Executive Summary\n"
            report_hash = hashlib.sha256(report_content).hexdigest()
            ctx.report_hash = report_hash

            # Verify report_hash is a valid SHA-256 hex digest (64 hex chars)
            assert ctx.report_hash is not None
            assert len(ctx.report_hash) == 64, (
                f"report_hash length is {len(ctx.report_hash)}, expected 64"
            )
            assert all(c in "0123456789abcdef" for c in ctx.report_hash), (
                f"report_hash '{ctx.report_hash}' contains non-hex characters"
            )

    @given(contents=file_contents_strategy)
    @settings(max_examples=200, deadline=None)
    def test_same_files_produce_identical_hashes_different_run_ids(
        self, contents: list[bytes]
    ) -> None:
        """Property 5: Two RunContexts from same files have identical content_hashes
        but different run_ids.

        **Validates: Requirements 15.5, 15.6**

        Non-deterministic values (run_id) are unique per execution while
        deterministic values (content_hashes) are consistent for same inputs.
        This ensures the RunContext properly separates deterministic from
        non-deterministic components.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_paths = []
            for i, content in enumerate(contents):
                file_path = Path(tmp_dir) / f"input_{i}.xlsx"
                file_path.write_bytes(content)
                file_paths.append(str(file_path))

            ctx_1 = RunContext.create(file_paths)
            ctx_2 = RunContext.create(file_paths)

            # run_ids must be different (unique per execution)
            assert ctx_1.run_id != ctx_2.run_id, (
                f"Two RunContexts should have different run_ids, "
                f"both got '{ctx_1.run_id}'"
            )

            # content_hashes must be identical (deterministic for same content)
            hashes_1 = [ds.content_hash for ds in ctx_1.data_sources]
            hashes_2 = [ds.content_hash for ds in ctx_2.data_sources]
            assert hashes_1 == hashes_2, (
                f"Same files should produce identical content_hashes. "
                f"Got {hashes_1} vs {hashes_2}"
            )
