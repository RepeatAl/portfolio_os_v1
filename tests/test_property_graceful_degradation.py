"""Property-based tests for Graceful Degradation Propagation.

**Validates: Requirements 1.4, 2.6, 8.5, 11.1, 11.2**

Tests that engine failures mark categories unavailable and remaining categories
continue independently. Hypothesis generates random subsets of failing engines;
verifies non-failing categories still produce output.
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from engines.pipeline_orchestrator import (
    ALL_SIGNAL_CATEGORIES,
    EngineTimeoutError,
    PipelineOrchestrator,
)
from runtime.severity_taxonomy import Severity


# All known engine IDs that map to categories in handle_engine_failure
ALL_ENGINE_IDS = [
    "allocation_engine",
    "regime_engine",
    "attribution_engine",
    "scoring_engine",
    "scenario_engine",
    "decision_engine",
    "quality_engine",
    "priority_engine",
    "semantic_engine",
]

# Engine-to-categories mapping (mirrors pipeline_orchestrator.py)
ENGINE_TO_CATEGORIES = {
    "allocation_engine": ["allocation"],
    "regime_engine": ["regime", "liquidity"],
    "attribution_engine": ["attribution"],
    "scoring_engine": ["correlation", "relative_strength"],
    "scenario_engine": ["scenario"],
    "decision_engine": ["cross_asset", "divergence", "flow"],
    "quality_engine": ["early_warning", "market_breadth"],
    "priority_engine": ["narrative_dependency", "portfolio_memory"],
    "semantic_engine": list(ALL_SIGNAL_CATEGORIES),
}

# Strategy: generate a non-empty subset of engine IDs (excluding semantic_engine
# which degrades ALL categories, tested separately)
failing_engines_strategy = st.lists(
    st.sampled_from([e for e in ALL_ENGINE_IDS if e != "semantic_engine"]),
    min_size=1,
    max_size=6,
    unique=True,
)

# Strategy: generate a single engine ID
single_engine_strategy = st.sampled_from(ALL_ENGINE_IDS)

# Strategy: generate error types (EngineTimeoutError or generic Exception)
error_type_strategy = st.sampled_from(["timeout", "generic"])


def _make_error(engine_id: str, error_type: str) -> Exception:
    """Create an error instance based on the error type string."""
    if error_type == "timeout":
        return EngineTimeoutError(engine_id)
    return RuntimeError(f"Engine {engine_id} failed unexpectedly")


class TestGracefulDegradationProperties:
    """Property-based tests for PipelineOrchestrator.handle_engine_failure()."""

    @given(engine_id=single_engine_strategy, error_type=error_type_strategy)
    @settings(max_examples=200)
    def test_affected_categories_marked_degraded(
        self, engine_id: str, error_type: str
    ) -> None:
        """Property 1: After handle_engine_failure(), affected categories are in _degraded_categories.

        **Validates: Requirements 1.4, 11.1**

        When an engine fails, all signal categories mapped to that engine
        must appear in the orchestrator's _degraded_categories list.
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator._severity_events = []
        orchestrator._degraded_categories = []
        orchestrator._component_states = []

        error = _make_error(engine_id, error_type)
        orchestrator.handle_engine_failure(engine_id, error)

        expected_categories = ENGINE_TO_CATEGORIES.get(engine_id, [engine_id])
        for category in expected_categories:
            assert category in orchestrator._degraded_categories, (
                f"Category '{category}' should be in _degraded_categories after "
                f"engine '{engine_id}' failure, but got: {orchestrator._degraded_categories}"
            )

    @given(failing_engines=failing_engines_strategy)
    @settings(max_examples=200)
    def test_non_affected_categories_remain_available(
        self, failing_engines: list[str]
    ) -> None:
        """Property 2: Non-affected categories remain available (not in _degraded_categories).

        **Validates: Requirements 2.6, 8.5**

        When a subset of engines fail, categories NOT mapped to those engines
        must NOT appear in _degraded_categories.
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator._severity_events = []
        orchestrator._degraded_categories = []
        orchestrator._component_states = []

        # Compute which categories SHOULD be degraded
        expected_degraded: set[str] = set()
        for engine_id in failing_engines:
            error = RuntimeError(f"{engine_id} failed")
            orchestrator.handle_engine_failure(engine_id, error)
            expected_degraded.update(ENGINE_TO_CATEGORIES.get(engine_id, [engine_id]))

        # All categories NOT in expected_degraded should NOT be in _degraded_categories
        all_categories = set(ALL_SIGNAL_CATEGORIES)
        expected_available = all_categories - expected_degraded

        for category in expected_available:
            assert category not in orchestrator._degraded_categories, (
                f"Category '{category}' should remain available but was found in "
                f"_degraded_categories. Failing engines: {failing_engines}"
            )

    @given(failing_engines=failing_engines_strategy)
    @settings(max_examples=200)
    def test_multiple_failures_accumulate_without_duplicates(
        self, failing_engines: list[str]
    ) -> None:
        """Property 3: Multiple engine failures accumulate degraded categories without duplicates.

        **Validates: Requirements 1.4, 11.1, 11.2**

        When multiple engines fail sequentially, their affected categories
        accumulate in _degraded_categories with no duplicate entries.
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator._severity_events = []
        orchestrator._degraded_categories = []
        orchestrator._component_states = []

        for engine_id in failing_engines:
            error = RuntimeError(f"{engine_id} failed")
            orchestrator.handle_engine_failure(engine_id, error)

        # Check no duplicates
        assert len(orchestrator._degraded_categories) == len(
            set(orchestrator._degraded_categories)
        ), (
            f"Duplicate categories found in _degraded_categories: "
            f"{orchestrator._degraded_categories}"
        )

        # Check all expected categories are present
        expected_degraded: set[str] = set()
        for engine_id in failing_engines:
            expected_degraded.update(ENGINE_TO_CATEGORIES.get(engine_id, [engine_id]))

        for category in expected_degraded:
            assert category in orchestrator._degraded_categories, (
                f"Category '{category}' missing from _degraded_categories after "
                f"multiple failures: {failing_engines}"
            )

    @given(engine_id=single_engine_strategy, error_type=error_type_strategy)
    @settings(max_examples=200)
    def test_severity_event_emitted_for_each_failure(
        self, engine_id: str, error_type: str
    ) -> None:
        """Property 4: Severity events are emitted for each failure.

        **Validates: Requirements 1.4, 11.1**

        Every call to handle_engine_failure() must produce at least one
        severity event in _severity_events.
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator._severity_events = []
        orchestrator._degraded_categories = []
        orchestrator._component_states = []

        error = _make_error(engine_id, error_type)
        events_before = len(orchestrator._severity_events)
        orchestrator.handle_engine_failure(engine_id, error)
        events_after = len(orchestrator._severity_events)

        assert events_after > events_before, (
            f"No severity event emitted for engine '{engine_id}' failure "
            f"(error_type={error_type})"
        )

    @given(engine_id=single_engine_strategy, error_type=error_type_strategy)
    @settings(max_examples=200)
    def test_timeout_produces_critical_other_produces_degraded(
        self, engine_id: str, error_type: str
    ) -> None:
        """Property 5: EngineTimeoutError produces CRITICAL severity, other errors produce DEGRADED.

        **Validates: Requirements 11.1, 11.2**

        The severity of the emitted event depends on the error type:
        - EngineTimeoutError → CRITICAL
        - Any other exception → DEGRADED
        """
        orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
        orchestrator._severity_events = []
        orchestrator._degraded_categories = []
        orchestrator._component_states = []

        error = _make_error(engine_id, error_type)
        orchestrator.handle_engine_failure(engine_id, error)

        # Find the severity event emitted
        assert len(orchestrator._severity_events) >= 1, (
            f"No severity event emitted for engine '{engine_id}'"
        )

        event = orchestrator._severity_events[-1]
        if error_type == "timeout":
            assert event["severity"] == "CRITICAL", (
                f"EngineTimeoutError should produce CRITICAL severity, "
                f"got '{event['severity']}' for engine '{engine_id}'"
            )
        else:
            assert event["severity"] == "DEGRADED", (
                f"Generic error should produce DEGRADED severity, "
                f"got '{event['severity']}' for engine '{engine_id}'"
            )
