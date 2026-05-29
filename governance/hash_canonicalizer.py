"""Hash Canonicalizer for platform-independent file content canonicalization.

Provides deterministic file content canonicalization so that runtime integrity
hashing produces identical results across macOS, Linux, and CI environments
(Ubuntu) for the same logical file content.

Canonicalization Algorithm:
1. Normalize line endings: CRLF (\\r\\n) and CR (\\r) converted to LF (\\n)
2. Normalize encoding: all content decoded to UTF-8
3. Strip trailing whitespace: per-line removal of trailing spaces/tabs
4. Ensure final newline: exactly one trailing newline character
5. For YAML files: parse and re-serialize with sorted keys for deterministic output
6. For Python files: apply steps 1-4 (LF + UTF-8 + strip trailing whitespace)
7. For other files: apply steps 1-4 (basic normalization)

The compute_hash() method sorts file paths lexicographically, canonicalizes each
file, concatenates the results, and computes a SHA-256 digest.

Requirements: 48.1, 48.2, 48.3, 48.4
"""

import hashlib
import os

import yaml


class HashCanonicalizer:
    """Platform-independent file content canonicalization for deterministic hashing."""

    def normalize_line_endings(self, content: str) -> str:
        """Convert CRLF and CR line endings to LF.

        Handles mixed line endings by first replacing CRLF pairs,
        then replacing any remaining standalone CR characters.

        Args:
            content: String content with potentially mixed line endings.

        Returns:
            Content with all line endings normalized to LF (\\n).
        """
        # Replace CRLF first to avoid double-replacement
        content = content.replace("\r\n", "\n")
        # Replace any remaining standalone CR
        content = content.replace("\r", "\n")
        return content

    def normalize_encoding(self, content: bytes) -> str:
        """Convert byte content to UTF-8 string.

        Attempts UTF-8 decoding first, falls back to latin-1 if UTF-8
        decoding fails (latin-1 can decode any byte sequence).

        Args:
            content: Raw bytes to decode.

        Returns:
            UTF-8 decoded string content.
        """
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            # latin-1 is a superset that can decode any byte sequence
            return content.decode("latin-1")

    def strip_trailing_whitespace(self, content: str) -> str:
        """Remove trailing whitespace from each line.

        Strips spaces and tabs from the end of every line while
        preserving line endings and leading whitespace (indentation).

        Args:
            content: String content with potential trailing whitespace.

        Returns:
            Content with trailing whitespace removed from each line.
        """
        lines = content.split("\n")
        stripped_lines = [line.rstrip(" \t") for line in lines]
        return "\n".join(stripped_lines)

    def ensure_final_newline(self, content: str) -> str:
        """Ensure content ends with exactly one trailing newline.

        Strips all trailing newlines and adds exactly one back.
        Handles empty content by returning a single newline.

        Args:
            content: String content with zero or more trailing newlines.

        Returns:
            Content ending with exactly one newline character.
        """
        # Strip all trailing newlines, then add exactly one
        content = content.rstrip("\n")
        return content + "\n"

    def canonicalize_yaml(self, content: str) -> str:
        """Parse YAML content and re-serialize with sorted keys.

        Produces deterministic YAML output regardless of original key
        ordering, whitespace, or formatting. Uses default_flow_style=False
        for readable block-style output.

        Args:
            content: Raw YAML string content.

        Returns:
            Deterministically serialized YAML with sorted keys and
            exactly one trailing newline.
        """
        parsed = yaml.safe_load(content)
        if parsed is None:
            # Empty or comment-only YAML
            return "\n"
        serialized = yaml.dump(
            parsed,
            default_flow_style=False,
            sort_keys=True,
            allow_unicode=True,
        )
        return self.ensure_final_newline(serialized)

    def canonicalize_python(self, content: str) -> str:
        """Canonicalize Python file content.

        Applies LF normalization, trailing whitespace stripping, and
        ensures exactly one final newline. Does NOT parse the Python
        AST — operates on raw text only.

        Args:
            content: Raw Python source content.

        Returns:
            Canonicalized Python content (LF endings, no trailing
            whitespace, exactly one final newline).
        """
        content = self.normalize_line_endings(content)
        content = self.strip_trailing_whitespace(content)
        content = self.ensure_final_newline(content)
        return content

    def canonicalize_file(self, file_path: str) -> str:
        """Auto-detect file type by extension and apply appropriate canonicalization.

        File type detection:
        - .yaml, .yml → canonicalize_yaml (parse + re-serialize with sorted keys)
        - .py → canonicalize_python (LF + strip trailing whitespace + final newline)
        - All others → basic normalization (LF + strip trailing whitespace + final newline)

        Args:
            file_path: Path to the file to canonicalize.

        Returns:
            Canonicalized file content as a string.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be read.
        """
        # Read raw bytes for encoding normalization
        with open(file_path, "rb") as f:
            raw_content = f.read()

        # Normalize encoding to UTF-8 string
        content = self.normalize_encoding(raw_content)

        # Detect file type by extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext in (".yaml", ".yml"):
            # Normalize line endings before YAML parsing
            content = self.normalize_line_endings(content)
            return self.canonicalize_yaml(content)
        elif ext == ".py":
            return self.canonicalize_python(content)
        else:
            # Basic normalization for all other file types
            content = self.normalize_line_endings(content)
            content = self.strip_trailing_whitespace(content)
            content = self.ensure_final_newline(content)
            return content

    def compute_hash(self, file_paths: list[str]) -> str:
        """Compute SHA-256 hash over sorted, canonicalized file contents.

        Sorts file paths lexicographically for deterministic ordering,
        canonicalizes each file, concatenates all content, and computes
        a SHA-256 digest.

        Args:
            file_paths: List of file paths to include in the hash.

        Returns:
            SHA-256 hex digest string prefixed with "sha256:".

        Raises:
            FileNotFoundError: If any file in the list does not exist.
        """
        sorted_paths = sorted(file_paths)
        hasher = hashlib.sha256()

        for path in sorted_paths:
            canonicalized = self.canonicalize_file(path)
            hasher.update(canonicalized.encode("utf-8"))

        return f"sha256:{hasher.hexdigest()}"
