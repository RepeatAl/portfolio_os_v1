"""Property-based tests for Run_Context Temporal Consistency.

**Validates: Requirements 8.1, 8.3**

Tests that hash mismatches between recorded and current content are detected
and rejected. Hypothesis generates file content pairs; verify hash validation
catches any mutation. Also verifies that unchanged files always pass validation,
hash detection is deterministic, and unavailable files always fail validation.
"""

import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from runtime.run_context import DataSourceReference, RunContext


# Strategy: generate random binary content (1 to 1024 bytes)
binary_content_strategy = st.binary(min_size=1, max_size=1024)

# Strategy: generate two different binary contents
different_binary_pair_strategy = st.tuples(
    st.binary(min_size=1, max_size=1024),
    st.binary(min_size=1, max_size=1024),
).filter(lambda pair: pair[0] != pair[1])


class TestRunContextTemporalConsistencyProperties:
    """Property-based tests for Run_Context temporal consistency validation."""

    @given(content=binary_content_strategy)
    @settings(max_examples=200)
    def test_unchanged_file_always_validates(self, content: bytes) -> None:
        """Property 1: Creating a RunContext and immediately validating returns True.

        **Validates: Requirements 8.1**

        For any file content, creating a RunContext that snapshots the file
        and immediately calling validate_source() returns True because the
        file has not been mutated.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "source_data.xlsx"
            test_file.write_bytes(content)

            # Create RunContext that snapshots the file
            ctx = RunContext.create([str(test_file)])

            # Immediately validate — file has not changed
            result = ctx.validate_source(str(test_file))
            assert result is True, (
                f"Unchanged file should validate True, got {result} "
                f"for content of length {len(content)}"
            )

    @given(pair=different_binary_pair_strategy)
    @settings(max_examples=200)
    def test_mutated_file_fails_validation(self, pair: tuple[bytes, bytes]) -> None:
        """Property 2: Mutating file content after snapshot causes validation to fail.

        **Validates: Requirements 8.3**

        For any two different file contents A and B, creating a RunContext with
        content A then writing content B causes validate_source() to return False.
        """
        content_a, content_b = pair

        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "source_data.xlsx"
            test_file.write_bytes(content_a)

            # Create RunContext that snapshots content A
            ctx = RunContext.create([str(test_file)])

            # Mutate file to content B
            test_file.write_bytes(content_b)

            # Validate should detect the mutation
            result = ctx.validate_source(str(test_file))
            assert result is False, (
                f"Mutated file should validate False, got {result}. "
                f"Content A length={len(content_a)}, Content B length={len(content_b)}"
            )

    @given(content=binary_content_strategy)
    @settings(max_examples=200)
    def test_hash_detection_is_deterministic(self, content: bytes) -> None:
        """Property 3: Same content always produces same hash.

        **Validates: Requirements 8.1**

        Hash detection is deterministic — creating two RunContexts from the
        same file content produces identical content hashes.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_1 = Path(tmp_dir) / "file_1.xlsx"
            file_2 = Path(tmp_dir) / "file_2.xlsx"
            file_1.write_bytes(content)
            file_2.write_bytes(content)

            # Create RunContexts for each file
            ctx_1 = RunContext.create([str(file_1)])
            ctx_2 = RunContext.create([str(file_2)])

            # Hashes should be identical for same content
            hash_1 = ctx_1.data_sources[0].content_hash
            hash_2 = ctx_2.data_sources[0].content_hash
            assert hash_1 == hash_2, (
                f"Determinism violated: same content produced different hashes "
                f"{hash_1} vs {hash_2}"
            )

    @given(content=binary_content_strategy)
    @settings(max_examples=200)
    def test_unavailable_file_fails_validation(self, content: bytes) -> None:
        """Property 4: Unavailable files always fail validation.

        **Validates: Requirements 8.3**

        For any file content, creating a RunContext and then deleting the file
        causes validate_source() to return False.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = Path(tmp_dir) / "source_data.xlsx"
            test_file.write_bytes(content)

            # Create RunContext that snapshots the file
            ctx = RunContext.create([str(test_file)])

            # Delete the file to make it unavailable
            test_file.unlink()

            # Validate should fail because file is unavailable
            result = ctx.validate_source(str(test_file))
            assert result is False, (
                f"Unavailable file should validate False, got {result}"
            )
