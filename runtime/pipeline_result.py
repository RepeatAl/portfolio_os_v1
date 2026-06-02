"""Pipeline Result Contract — Typed output for deterministic pipeline execution.

Provides an explicit typed contract for pipeline orchestration results,
replacing implicit dict-based outputs. Every field is typed and documented,
ensuring downstream consumers have a clear interface to pipeline execution
outcomes.

Design Decision (Hardening 7): Explicit PipelineResult dataclass contract
avoids implicit dict-based orchestration outputs that are fragile, untyped,
and difficult to validate at runtime.
"""

from dataclasses import dataclass


@dataclass
class PipelineResult:
    """Explicit pipeline result contract (Hardening 7).

    Avoids implicit dict-based orchestration outputs. All fields are typed
    and represent the complete output of a single pipeline execution.

    Attributes:
        run_id: Unique identifier (UUID v4) for this pipeline execution.
        runtime_state: Aggregated pipeline state from canonical RuntimeState enum.
            One of: healthy, degraded, unavailable, invalid, inconsistent,
            collapsed, deterministic_failure, canonical_break.
        generated_artifacts: File paths of all generated canonical artifacts
            produced during this pipeline execution.
        degraded_categories: Signal categories that were unavailable or failed
            during this execution (e.g., "allocation", "regime").
        severity_events: All governance events emitted during execution.
            Each dict contains at minimum: severity, message, source.
        report_path: Path to the generated daily_report.md file.
            None if the pipeline collapsed and no report was produced.
        provenance_path: Path to the provenance sidecar file
            (<run_id>_provenance.yaml). None if provenance was not generated.
        run_context_path: Path to the persisted run context file
            (<run_id>_run_context.yaml). Always present for completed runs.
        deterministic_integrity_state: Result of deterministic integrity
            verification. One of: "verified", "unverified", "failed".
        semantic_snapshot_path: Path to the archived semantic snapshot file
            for this run. None if semantic persistence was skipped or failed.
    """

    run_id: str
    runtime_state: str
    generated_artifacts: list[str]
    degraded_categories: list[str]
    severity_events: list[dict]
    report_path: str | None
    provenance_path: str | None
    run_context_path: str
    deterministic_integrity_state: str
    semantic_snapshot_path: str | None
