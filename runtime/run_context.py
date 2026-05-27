"""Run Context — temporal snapshot for pipeline consistency.

Creates and validates temporal snapshots ensuring all engines in a single
pipeline execution operate on the same data. Each RunContext captures input
file references with content hashes at creation time, enabling downstream
validation that no source has mutated during execution.

Requirements: 8.1, 8.2, 8.4, 8.6
"""

from __future__ import annotations

import hashlib
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

from runtime.runtime_state_model import RuntimeState


@dataclass
class DataSourceReference:
    """Reference to an input data source with integrity hash.

    Attributes:
        file_path: Relative path from project root.
        content_hash: SHA-256 hex digest of file content at snapshot time.
        status: One of "available", "unavailable", "inconsistent".
    """

    file_path: str
    content_hash: str
    status: str  # "available" | "unavailable" | "inconsistent"


@dataclass
class RunContext:
    """Temporal snapshot identifier for a single pipeline execution.

    Immutable after creation — no field mutation during pipeline run.
    All engines receive the same RunContext instance to ensure temporal
    consistency across the canonical chain.

    Attributes:
        run_id: UUID v4 string identifying this execution.
        timestamp: ISO 8601 UTC with second precision.
        data_sources: List of input file references with hashes.
        schema_version: Semantic version for this schema ("1.0.0").
        pipeline_state: Runtime state from canonical model.
        report_hash: SHA-256 of final daily_report.md (set after completion).
    """

    run_id: str
    timestamp: str
    data_sources: list[DataSourceReference] = field(default_factory=list)
    schema_version: str = "1.0.0"
    pipeline_state: str = RuntimeState.HEALTHY
    report_hash: str | None = None

    @classmethod
    def create(cls, input_files: list[str]) -> RunContext:
        """Snapshot all input files, compute hashes, return frozen context.

        For each input file:
        - If the file exists and is readable, compute SHA-256 hash and mark "available".
        - If the file does not exist or is unreadable, mark "unavailable" with empty hash.

        Args:
            input_files: List of file paths (relative or absolute) to snapshot.

        Returns:
            A new RunContext with all data sources referenced.
        """
        run_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        data_sources: list[DataSourceReference] = []
        for file_path in input_files:
            try:
                content = Path(file_path).read_bytes()
                content_hash = hashlib.sha256(content).hexdigest()
                data_sources.append(
                    DataSourceReference(
                        file_path=file_path,
                        content_hash=content_hash,
                        status="available",
                    )
                )
            except (FileNotFoundError, PermissionError, OSError):
                data_sources.append(
                    DataSourceReference(
                        file_path=file_path,
                        content_hash="",
                        status="unavailable",
                    )
                )

        return cls(
            run_id=run_id,
            timestamp=timestamp,
            data_sources=data_sources,
            schema_version="1.0.0",
            pipeline_state=RuntimeState.HEALTHY,
            report_hash=None,
        )

    def validate_source(self, file_path: str) -> bool:
        """Verify file content hash matches recorded hash.

        Reads the file at file_path, computes its current SHA-256 hash,
        and compares against the hash recorded at snapshot time.

        Args:
            file_path: Path to the file to validate.

        Returns:
            True if the current hash matches the recorded hash.
            False if the file is not found in data_sources, is unavailable,
            or the hash does not match.
        """
        source = self._find_source(file_path)
        if source is None:
            return False
        if source.status != "available":
            return False

        try:
            content = Path(file_path).read_bytes()
            current_hash = hashlib.sha256(content).hexdigest()
            return current_hash == source.content_hash
        except (FileNotFoundError, PermissionError, OSError):
            return False

    def persist(self, output_dir: str) -> str:
        """Write run context as YAML to output directory.

        Creates the output directory if it does not exist.
        File is named: <run_id>_run_context.yaml

        Args:
            output_dir: Directory path where the YAML file will be written.

        Returns:
            Absolute file path of the persisted YAML file.
        """
        os.makedirs(output_dir, exist_ok=True)
        file_name = f"{self.run_id}_run_context.yaml"
        file_path = os.path.join(output_dir, file_name)

        data = {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "schema_version": self.schema_version,
            "pipeline_state": str(self.pipeline_state),
            "report_hash": self.report_hash,
            "data_sources": [
                {
                    "file_path": ds.file_path,
                    "content_hash": ds.content_hash,
                    "status": ds.status,
                }
                for ds in self.data_sources
            ],
        }

        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=True)

        return os.path.abspath(file_path)

    @classmethod
    def load(cls, file_path: str) -> RunContext:
        """Load previously persisted run context for replay.

        Reads a YAML file and reconstructs the RunContext with all
        data source references.

        Args:
            file_path: Path to the persisted YAML file.

        Returns:
            Reconstructed RunContext instance.

        Raises:
            FileNotFoundError: If the YAML file does not exist.
            yaml.YAMLError: If the file is not valid YAML.
            KeyError: If required fields are missing from the YAML.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        data_sources = [
            DataSourceReference(
                file_path=ds["file_path"],
                content_hash=ds["content_hash"],
                status=ds["status"],
            )
            for ds in data.get("data_sources", [])
        ]

        return cls(
            run_id=data["run_id"],
            timestamp=data["timestamp"],
            data_sources=data_sources,
            schema_version=data.get("schema_version", "1.0.0"),
            pipeline_state=data.get("pipeline_state", RuntimeState.HEALTHY),
            report_hash=data.get("report_hash"),
        )

    def _find_source(self, file_path: str) -> DataSourceReference | None:
        """Find a data source reference by file path."""
        for source in self.data_sources:
            if source.file_path == file_path:
                return source
        return None
