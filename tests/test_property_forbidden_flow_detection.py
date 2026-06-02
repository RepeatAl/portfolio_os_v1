"""Property-based tests for Forbidden Flow Detection.

**Validates: Requirements 1.2, 1.3, 10.4**

Tests that any Signal→Report shortcut is detected with source engine, target
section, and skipped layers. Hypothesis generates random engine output routing;
verifies all shortcuts are caught.

Properties:
1. All uncovered categories produce forbidden flow entries
2. Each flow contains source_engine, target_section, skipped_layers
3. skipped_layers always contains "SEMANTICS" and "REASONING" for uncovered categories
4. Number of detected flows equals uncovered categories (plus report shortcut if present)
5. Detection is deterministic (same inputs → same flows)
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from engines.pipeline_orchestrator import (
    ALL_SIGNAL_CATEGORIES,
    CATEGORY_TO_SECTION,
    PipelineOrchestrator,
)


# Strategy: random subsets of signal categories to simulate engine outputs
category_subset_strategy = st.lists(
    st.sampled_from(ALL_SIGNAL_CATEGORIES),
    min_size=0,
    max_size=len(ALL_SIGNAL_CATEGORIES),
    unique=True,
)

# Strategy: random engine output dicts with arbitrary keys
engine_output_keys_strategy = st.lists(
    st.sampled_from(ALL_SIGNAL_CATEGORIES + ["report", "summary", "debug"]),
    min_size=0,
    max_size=10,
    unique=True,
)

# Strategy: engine outputs dict (keys → placeholder values)
engine_outputs_strategy = engine_output_keys_strategy.map(
    lambda keys: {k: {"data": f"{k}_output"} for k in keys}
)

# Strategy: engine outputs that include "report" key
engine_outputs_with_report_strategy = engine_output_keys_strategy.map(
    lambda keys: {k: {"data": f"{k}_output"} for k in (set(keys) | {"report"})}
)

# Strategy: engine outputs that do NOT include "report" key
engine_outputs_without_report_strategy = engine_output_keys_strategy.map(
    lambda keys: {k: {"data": f"{k}_output"} for k in keys if k != "report"}
)


class TestForbiddenFlowDetectionProperties:
    """Property-based tests for PipelineOrchestrator.detect_forbidden_flows()."""

    @given(engine_outputs=engine_outputs_strategy)
    @settings(max_examples=200)
    def test_all_uncovered_categories_produce_forbidden_flows(
        self, engine_outputs: dict
    ) -> None:
        """Property 1: All uncovered categories produce forbidden flow entries.

        **Validates: Requirements 1.2, 1.3**

        For any engine output routing, every signal category that lacks semantic
        coverage (all except 'allocation') must produce a forbidden flow entry.
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator.config_path = ".domainization/config.yaml"
        orchestrator.config = {}
        orchestrator.enforcement_mode = "observability"

        flows = orchestrator.detect_forbidden_flows(engine_outputs)

        # The covered categories (only 'allocation' has semantic coverage)
        covered_categories = {"allocation"}
        uncovered_categories = [
            c for c in ALL_SIGNAL_CATEGORIES if c not in covered_categories
        ]

        # All uncovered categories must appear as forbidden flows
        flow_sources = [f["source_engine"] for f in flows]
        for category in uncovered_categories:
            expected_source = f"{category}_engine"
            assert expected_source in flow_sources, (
                f"Uncovered category '{category}' did not produce a forbidden flow. "
                f"Expected source_engine='{expected_source}' in flows."
            )

    @given(engine_outputs=engine_outputs_strategy)
    @settings(max_examples=200)
    def test_each_flow_contains_required_fields(self, engine_outputs: dict) -> None:
        """Property 2: Each flow contains source_engine, target_section, skipped_layers.

        **Validates: Requirements 1.3, 10.4**

        Every forbidden flow entry must contain all three required fields:
        source_engine (string), target_section (string), and skipped_layers (list).
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator.config_path = ".domainization/config.yaml"
        orchestrator.config = {}
        orchestrator.enforcement_mode = "observability"

        flows = orchestrator.detect_forbidden_flows(engine_outputs)

        for flow in flows:
            assert "source_engine" in flow, (
                f"Flow missing 'source_engine' field: {flow}"
            )
            assert "target_section" in flow, (
                f"Flow missing 'target_section' field: {flow}"
            )
            assert "skipped_layers" in flow, (
                f"Flow missing 'skipped_layers' field: {flow}"
            )

            # Validate types
            assert isinstance(flow["source_engine"], str), (
                f"source_engine must be a string, got {type(flow['source_engine'])}"
            )
            assert isinstance(flow["target_section"], str), (
                f"target_section must be a string, got {type(flow['target_section'])}"
            )
            assert isinstance(flow["skipped_layers"], list), (
                f"skipped_layers must be a list, got {type(flow['skipped_layers'])}"
            )
            assert len(flow["skipped_layers"]) > 0, (
                f"skipped_layers must not be empty for flow: {flow}"
            )

    @given(engine_outputs=engine_outputs_strategy)
    @settings(max_examples=200)
    def test_skipped_layers_contains_semantics_and_reasoning(
        self, engine_outputs: dict
    ) -> None:
        """Property 3: skipped_layers always contains SEMANTICS and REASONING for uncovered categories.

        **Validates: Requirements 1.2, 1.3, 10.4**

        For every forbidden flow produced by an uncovered signal category,
        the skipped_layers field must contain both "SEMANTICS" and "REASONING"
        since these categories bypass both layers entirely.
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator.config_path = ".domainization/config.yaml"
        orchestrator.config = {}
        orchestrator.enforcement_mode = "observability"

        flows = orchestrator.detect_forbidden_flows(engine_outputs)

        # Filter to only category-based flows (not the report shortcut)
        covered_categories = {"allocation"}
        uncovered_categories = [
            c for c in ALL_SIGNAL_CATEGORIES if c not in covered_categories
        ]
        expected_sources = {f"{c}_engine" for c in uncovered_categories}

        for flow in flows:
            if flow["source_engine"] in expected_sources:
                assert "SEMANTICS" in flow["skipped_layers"], (
                    f"Flow for '{flow['source_engine']}' missing 'SEMANTICS' in "
                    f"skipped_layers: {flow['skipped_layers']}"
                )
                assert "REASONING" in flow["skipped_layers"], (
                    f"Flow for '{flow['source_engine']}' missing 'REASONING' in "
                    f"skipped_layers: {flow['skipped_layers']}"
                )

    @given(engine_outputs=engine_outputs_without_report_strategy)
    @settings(max_examples=200)
    def test_flow_count_equals_uncovered_categories_plus_report_shortcut(
        self, engine_outputs: dict
    ) -> None:
        """Property 4: Number of detected flows equals uncovered categories (plus report shortcut if present).

        **Validates: Requirements 1.2, 1.3**

        The total number of forbidden flows must equal the number of uncovered
        signal categories when no report key is present, and uncovered + 1
        when the report key is present.
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator.config_path = ".domainization/config.yaml"
        orchestrator.config = {}
        orchestrator.enforcement_mode = "observability"

        covered_categories = {"allocation"}
        uncovered_count = len(
            [c for c in ALL_SIGNAL_CATEGORIES if c not in covered_categories]
        )

        # Without report key: flows == uncovered categories
        flows_without_report = orchestrator.detect_forbidden_flows(engine_outputs)
        assert len(flows_without_report) == uncovered_count, (
            f"Expected {uncovered_count} flows (one per uncovered category), "
            f"got {len(flows_without_report)} flows."
        )

        # With report key: flows == uncovered categories + 1
        engine_outputs_with_report = dict(engine_outputs)
        engine_outputs_with_report["report"] = {"data": "report_output"}
        flows_with_report = orchestrator.detect_forbidden_flows(
            engine_outputs_with_report
        )
        assert len(flows_with_report) == uncovered_count + 1, (
            f"Expected {uncovered_count + 1} flows (uncovered + report shortcut), "
            f"got {len(flows_with_report)} flows."
        )

    @given(engine_outputs=engine_outputs_strategy)
    @settings(max_examples=200)
    def test_detection_is_deterministic(self, engine_outputs: dict) -> None:
        """Property 5: Detection is deterministic (same inputs → same flows).

        **Validates: Requirements 1.2, 1.3**

        Running detect_forbidden_flows twice with the same engine_outputs
        must produce identical results.
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator.config_path = ".domainization/config.yaml"
        orchestrator.config = {}
        orchestrator.enforcement_mode = "observability"

        flows_1 = orchestrator.detect_forbidden_flows(engine_outputs)
        flows_2 = orchestrator.detect_forbidden_flows(engine_outputs)

        assert flows_1 == flows_2, (
            f"Determinism violated: same engine_outputs produced different flows.\n"
            f"First call: {flows_1}\n"
            f"Second call: {flows_2}"
        )
