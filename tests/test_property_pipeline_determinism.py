"""Property-based tests for Pipeline Determinism.

**Validates: Requirements 6.5, 15.1, 15.2, 15.3, 15.4, 22.1, 22.2**

Tests that identical Run_Context inputs produce semantically equivalent outputs;
byte-identity for governed YAML serializations. Verifies:
1. RunContext.persist() with same inputs produces byte-identical YAML
2. ReportProvenance.persist() with same inputs produces byte-identical YAML
3. SemanticStateStore.save_snapshot() with same inputs produces byte-identical YAML
4. SectionProvenance.to_yaml() with same inputs produces identical strings
"""

from __future__ import annotations

import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from governance.provenance_schema import ReportProvenance, SectionProvenance
from runtime.run_context import DataSourceReference, RunContext
from runtime.semantic_state_store import SemanticStateStore


# --- Strategies ---

# Strategy: generate a valid identifier string (alphanumeric + underscore/dash)
identifier_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_-"),
    min_size=3,
    max_size=30,
).filter(lambda s: len(s.strip()) >= 3)

# Strategy: generate a SHA-256 hex digest
sha256_hash_strategy = st.text(
    alphabet="0123456789abcdef",
    min_size=64,
    max_size=64,
)

# Strategy: generate a file path string
file_path_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_-/. "),
    min_size=5,
    max_size=50,
).filter(lambda s: len(s.strip()) >= 5 and "/" in s)

# Strategy: generate a data source status
status_strategy = st.sampled_from(["available", "unavailable", "inconsistent"])

# Strategy: generate a pipeline state
pipeline_state_strategy = st.sampled_from([
    "healthy", "degraded", "unavailable", "invalid",
    "inconsistent", "collapsed", "deterministic_failure", "canonical_break",
])

# Strategy: generate a completeness state
completeness_strategy = st.sampled_from([
    "complete", "partial", "degraded", "unavailable", "invalid",
])

# Strategy: generate a category string
category_strategy = st.sampled_from([
    "allocation", "attribution", "correlation", "cross_asset",
    "divergence", "early_warning", "flow", "liquidity",
    "market_breadth", "narrative_dependency", "regime",
    "relative_strength", "scenario", "portfolio_memory",
])

# Strategy: generate a timestamp in ISO 8601 UTC format
timestamp_strategy = st.builds(
    lambda y, mo, d, h, mi, s: f"{y:04d}-{mo:02d}-{d:02d}T{h:02d}:{mi:02d}:{s:02d}Z",
    y=st.integers(min_value=2020, max_value=2030),
    mo=st.integers(min_value=1, max_value=12),
    d=st.integers(min_value=1, max_value=28),
    h=st.integers(min_value=0, max_value=23),
    mi=st.integers(min_value=0, max_value=59),
    s=st.integers(min_value=0, max_value=59),
)


# --- Composite Strategies ---

def data_source_reference_strategy():
    """Generate a DataSourceReference with valid fields."""
    return st.builds(
        DataSourceReference,
        file_path=file_path_strategy,
        content_hash=sha256_hash_strategy,
        status=status_strategy,
    )


def run_context_strategy():
    """Generate a RunContext with deterministic fields (fixed run_id and timestamp)."""
    return st.builds(
        RunContext,
        run_id=st.builds(lambda: str(uuid.uuid4())),
        timestamp=timestamp_strategy,
        data_sources=st.lists(data_source_reference_strategy(), min_size=0, max_size=5),
        schema_version=st.just("1.0.0"),
        pipeline_state=pipeline_state_strategy,
        report_hash=st.one_of(st.none(), sha256_hash_strategy),
    )


def section_provenance_strategy():
    """Generate a SectionProvenance with valid fields."""
    return st.builds(
        SectionProvenance,
        section_name=st.sampled_from([
            "Executive Summary", "Market Regime", "Portfolio Structure",
            "Concentration and Dependency", "Deployment Analysis",
            "Scenario Analysis", "Action Space",
            "Confidence Interpretation", "PM Summary",
        ]),
        reasoning_object_ids=st.lists(identifier_strategy, min_size=1, max_size=5),
        semantic_state_ids=st.lists(identifier_strategy, min_size=1, max_size=5),
        signal_engine_ids=st.lists(identifier_strategy, min_size=1, max_size=5),
        completeness_state=completeness_strategy,
        unavailable_layers=st.just([]),
        schema_version=st.just("1.0.0"),
    )


def report_provenance_strategy():
    """Generate a ReportProvenance with valid fields."""
    return st.builds(
        ReportProvenance,
        run_context_id=st.builds(lambda: str(uuid.uuid4())),
        timestamp=timestamp_strategy,
        sections=st.lists(section_provenance_strategy(), min_size=1, max_size=5),
        schema_version=st.just("1.0.0"),
    )


def semantic_state_strategy():
    """Generate a single semantic state dict with required fields."""
    return st.fixed_dictionaries({
        "signal_id": identifier_strategy,
        "category": category_strategy,
        "meaning": st.text(min_size=5, max_size=80).filter(lambda s: len(s.strip()) >= 5),
        "source": identifier_strategy,
    })


def unique_semantic_states_strategy(min_size=1, max_size=8):
    """Generate a list of semantic states with unique signal_ids."""
    return st.lists(
        semantic_state_strategy(),
        min_size=min_size,
        max_size=max_size,
    ).filter(
        lambda states: len({s["signal_id"] for s in states}) == len(states)
    )



class TestPipelineDeterminism:
    """Property-based tests for Pipeline Determinism (Property 9).

    Verifies that governed YAML serializations produce byte-identical output
    when given the same inputs. This is the core determinism guarantee for
    canonical artifacts.
    """

    @given(
        run_id=st.builds(lambda: str(uuid.uuid4())),
        timestamp=timestamp_strategy,
        data_sources=st.lists(data_source_reference_strategy(), min_size=0, max_size=5),
        pipeline_state=pipeline_state_strategy,
        report_hash=st.one_of(st.none(), sha256_hash_strategy),
    )
    @settings(max_examples=200, deadline=None)
    def test_run_context_persist_byte_identical(
        self,
        run_id: str,
        timestamp: str,
        data_sources: list[DataSourceReference],
        pipeline_state: str,
        report_hash: str | None,
    ) -> None:
        """Property 1: RunContext.persist() with same inputs produces byte-identical YAML.

        **Validates: Requirements 15.1, 22.1**

        For any valid RunContext, calling persist() twice with the same inputs
        produces byte-identical YAML files. This ensures deterministic
        serialization of the Run_Context canonical artifact.
        """
        ctx = RunContext(
            run_id=run_id,
            timestamp=timestamp,
            data_sources=data_sources,
            schema_version="1.0.0",
            pipeline_state=pipeline_state,
            report_hash=report_hash,
        )

        with tempfile.TemporaryDirectory() as tmp_dir_1:
            with tempfile.TemporaryDirectory() as tmp_dir_2:
                path_1 = ctx.persist(tmp_dir_1)
                path_2 = ctx.persist(tmp_dir_2)

                content_1 = Path(path_1).read_bytes()
                content_2 = Path(path_2).read_bytes()

                assert content_1 == content_2, (
                    f"RunContext.persist() produced different YAML for same inputs.\n"
                    f"First ({len(content_1)} bytes):\n{content_1.decode()}\n"
                    f"Second ({len(content_2)} bytes):\n{content_2.decode()}"
                )

    @given(
        run_context_id=st.builds(lambda: str(uuid.uuid4())),
        timestamp=timestamp_strategy,
        sections=st.lists(section_provenance_strategy(), min_size=1, max_size=5),
    )
    @settings(max_examples=200, deadline=None)
    def test_report_provenance_persist_byte_identical(
        self,
        run_context_id: str,
        timestamp: str,
        sections: list[SectionProvenance],
    ) -> None:
        """Property 2: ReportProvenance.persist() with same inputs produces byte-identical YAML.

        **Validates: Requirements 15.1, 22.1**

        For any valid ReportProvenance, calling persist() twice with the same
        inputs produces byte-identical YAML sidecar files. This ensures
        deterministic serialization of the provenance canonical artifact.
        """
        provenance = ReportProvenance(
            run_context_id=run_context_id,
            timestamp=timestamp,
            sections=sections,
            schema_version="1.0.0",
        )

        with tempfile.TemporaryDirectory() as tmp_dir_1:
            with tempfile.TemporaryDirectory() as tmp_dir_2:
                path_1 = provenance.persist(tmp_dir_1)
                path_2 = provenance.persist(tmp_dir_2)

                content_1 = Path(path_1).read_bytes()
                content_2 = Path(path_2).read_bytes()

                assert content_1 == content_2, (
                    f"ReportProvenance.persist() produced different YAML for same inputs.\n"
                    f"First ({len(content_1)} bytes):\n{content_1.decode()}\n"
                    f"Second ({len(content_2)} bytes):\n{content_2.decode()}"
                )

    @given(states=unique_semantic_states_strategy(min_size=1, max_size=8))
    @settings(max_examples=200, deadline=None)
    def test_semantic_state_store_save_byte_identical(
        self, states: list[dict]
    ) -> None:
        """Property 3: SemanticStateStore.save_snapshot() with same inputs produces byte-identical YAML.

        **Validates: Requirements 15.2, 22.1**

        For any list of semantic states and a fixed RunContext, calling
        save_snapshot() twice produces byte-identical snapshot YAML files.
        This ensures deterministic serialization of semantic state snapshots.
        """
        run_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        run_ctx = RunContext(
            run_id=run_id,
            timestamp=timestamp,
            data_sources=[],
            schema_version="1.0.0",
            pipeline_state="healthy",
            report_hash=None,
        )

        with tempfile.TemporaryDirectory() as tmp_dir_1:
            with tempfile.TemporaryDirectory() as tmp_dir_2:
                store_1 = SemanticStateStore(state_dir=tmp_dir_1)
                store_2 = SemanticStateStore(state_dir=tmp_dir_2)

                store_1.save_snapshot(states, run_ctx)
                store_2.save_snapshot(states, run_ctx)

                # Compare the snapshot files
                snapshot_path_1 = (
                    Path(tmp_dir_1) / "snapshots" / f"{run_id}_semantic_snapshot.yaml"
                )
                snapshot_path_2 = (
                    Path(tmp_dir_2) / "snapshots" / f"{run_id}_semantic_snapshot.yaml"
                )

                content_1 = snapshot_path_1.read_bytes()
                content_2 = snapshot_path_2.read_bytes()

                assert content_1 == content_2, (
                    f"SemanticStateStore.save_snapshot() produced different YAML "
                    f"for same inputs.\n"
                    f"First ({len(content_1)} bytes):\n{content_1.decode()}\n"
                    f"Second ({len(content_2)} bytes):\n{content_2.decode()}"
                )

    @given(section=section_provenance_strategy())
    @settings(max_examples=200, deadline=None)
    def test_section_provenance_to_yaml_identical(
        self, section: SectionProvenance
    ) -> None:
        """Property 4: SectionProvenance.to_yaml() with same inputs produces identical strings.

        **Validates: Requirements 15.3, 22.2**

        For any valid SectionProvenance, calling to_yaml() twice produces
        identical string output. This ensures deterministic serialization
        of provenance metadata blocks.
        """
        yaml_1 = section.to_yaml()
        yaml_2 = section.to_yaml()

        assert yaml_1 == yaml_2, (
            f"SectionProvenance.to_yaml() produced different output for same inputs.\n"
            f"First:\n{yaml_1}\n"
            f"Second:\n{yaml_2}"
        )
