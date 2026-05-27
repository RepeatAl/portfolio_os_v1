"""Property-based tests for Semantic Coverage Invariant.

**Validates: Requirements 2.1, 2.2**

Tests that for valid signal outputs covering all 14 categories, at least one
Semantic State per category and exactly one Reasoning Object per category are
produced. Hypothesis generates random valid signal outputs for all 14 categories;
verifies coverage completeness.

Properties:
1. At least one Semantic State per category is produced for valid signal outputs
2. Exactly one Reasoning Object per category is produced
3. Each Reasoning Object references at least one Semantic State from its category
4. Coverage is complete: all 14 categories have both semantic and reasoning output
5. No duplicate Reasoning Objects for the same category
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from engines.pipeline_orchestrator import (
    ALL_SIGNAL_CATEGORIES,
    PipelineOrchestrator,
)
from runtime.confidence_policy import ConfidenceDegradationPolicy
from runtime.reasoning_object import ReasoningObject
from runtime.run_context import RunContext
from runtime.runtime_state_model import RuntimeState


# Strategy: generate random valid signal output values per category
# Each category gets a dict with a "data" key and random numeric value
signal_value_strategy = st.floats(
    min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False
)

# Strategy: generate a valid signal output dict covering all 14 categories
# Each category maps to a dict with signal data
full_signal_outputs_strategy = st.fixed_dictionaries(
    {
        category: st.fixed_dictionaries({
            "data": st.text(min_size=1, max_size=50, alphabet=st.characters(
                whitelist_categories=("L", "N", "P"),
            )),
            "value": signal_value_strategy,
            "status": st.sampled_from(["active", "computed", "derived"]),
        })
        for category in ALL_SIGNAL_CATEGORIES
    }
)

# Strategy: generate random subsets of categories to simulate partial coverage
# (used to test that even with partial signal outputs, the orchestrator fills gaps)
partial_categories_strategy = st.lists(
    st.sampled_from(ALL_SIGNAL_CATEGORIES),
    min_size=1,
    max_size=len(ALL_SIGNAL_CATEGORIES),
    unique=True,
)


def _create_orchestrator() -> PipelineOrchestrator:
    """Create a PipelineOrchestrator instance without loading config from disk."""
    orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
    orchestrator.config_path = ".domainization/config.yaml"
    orchestrator.config = {}
    orchestrator.enforcement_mode = "observability"
    orchestrator.output_dir = "output"
    orchestrator.state_dir = "state"
    orchestrator._severity_events = []
    orchestrator._degraded_categories = []
    orchestrator._generated_artifacts = []
    orchestrator._component_states = []
    orchestrator._confidence_policy = ConfidenceDegradationPolicy()
    return orchestrator


def _create_run_context() -> RunContext:
    """Create a minimal RunContext for testing."""
    return RunContext.create([])


class TestSemanticCoverageInvariantProperties:
    """Property-based tests for Semantic Coverage Invariant.

    Validates that the pipeline produces at least one Semantic State per
    signal category and exactly one Reasoning Object per category when
    valid signal outputs cover all 14 categories.
    """

    @given(signal_outputs=full_signal_outputs_strategy)
    @settings(max_examples=200)
    def test_at_least_one_semantic_state_per_category(
        self, signal_outputs: dict
    ) -> None:
        """Property 1: At least one Semantic State per category is produced.

        **Validates: Requirements 2.1**

        For any valid signal outputs covering all 14 categories, the Semantic
        Engine must produce at least one Semantic State per category.
        """
        orchestrator = _create_orchestrator()
        run_context = _create_run_context()

        # Execute semantic engine with the generated signal outputs
        semantic_states = orchestrator._execute_semantic_engine(
            signal_outputs, run_context
        )

        # Group states by category
        categories_covered: dict[str, list[dict]] = {}
        for state in semantic_states:
            category = state.get("category", "unknown")
            if category not in categories_covered:
                categories_covered[category] = []
            categories_covered[category].append(state)

        # Verify at least one state per category
        for category in ALL_SIGNAL_CATEGORIES:
            assert category in categories_covered, (
                f"Category '{category}' has no Semantic State. "
                f"Expected at least one state per category. "
                f"Categories covered: {list(categories_covered.keys())}"
            )
            assert len(categories_covered[category]) >= 1, (
                f"Category '{category}' has zero Semantic States. "
                f"Expected at least one."
            )

    @given(signal_outputs=full_signal_outputs_strategy)
    @settings(max_examples=200)
    def test_exactly_one_reasoning_object_per_category(
        self, signal_outputs: dict
    ) -> None:
        """Property 2: Exactly one Reasoning Object per category is produced.

        **Validates: Requirements 2.2**

        For any valid signal outputs covering all 14 categories, the Reasoning
        Engine must produce exactly one Reasoning Object per signal category.
        """
        orchestrator = _create_orchestrator()
        run_context = _create_run_context()

        # Execute semantic engine first
        semantic_states = orchestrator._execute_semantic_engine(
            signal_outputs, run_context
        )

        # Execute reasoning engines
        reasoning_objects = orchestrator._execute_reasoning_engines(
            semantic_states, run_context
        )

        # Group reasoning objects by category
        ro_by_category: dict[str, list[ReasoningObject]] = {}
        for ro in reasoning_objects:
            category = ro.conclusion.category
            if category not in ro_by_category:
                ro_by_category[category] = []
            ro_by_category[category].append(ro)

        # Verify exactly one reasoning object per category
        for category in ALL_SIGNAL_CATEGORIES:
            assert category in ro_by_category, (
                f"Category '{category}' has no Reasoning Object. "
                f"Expected exactly one per category. "
                f"Categories with ROs: {list(ro_by_category.keys())}"
            )
            assert len(ro_by_category[category]) == 1, (
                f"Category '{category}' has {len(ro_by_category[category])} "
                f"Reasoning Objects. Expected exactly one."
            )

    @given(signal_outputs=full_signal_outputs_strategy)
    @settings(max_examples=200)
    def test_reasoning_objects_reference_semantic_states(
        self, signal_outputs: dict
    ) -> None:
        """Property 3: Each Reasoning Object references at least one Semantic State from its category.

        **Validates: Requirements 2.1, 2.2**

        Every Reasoning Object must have source_semantic_states that reference
        signal_ids from Semantic States belonging to the same category.
        """
        orchestrator = _create_orchestrator()
        run_context = _create_run_context()

        # Execute semantic engine
        semantic_states = orchestrator._execute_semantic_engine(
            signal_outputs, run_context
        )

        # Collect all signal_ids by category
        signal_ids_by_category: dict[str, set[str]] = {}
        for state in semantic_states:
            category = state.get("category", "unknown")
            signal_id = state.get("signal_id")
            if signal_id:
                if category not in signal_ids_by_category:
                    signal_ids_by_category[category] = set()
                signal_ids_by_category[category].add(signal_id)

        # Execute reasoning engines
        reasoning_objects = orchestrator._execute_reasoning_engines(
            semantic_states, run_context
        )

        # Verify each RO references states from its category
        for ro in reasoning_objects:
            category = ro.conclusion.category
            assert len(ro.source_semantic_states) >= 1, (
                f"Reasoning Object for '{category}' has no source_semantic_states. "
                f"Expected at least one reference."
            )

            # All referenced signal_ids should exist in the semantic states
            # for this category
            expected_ids = signal_ids_by_category.get(category, set())
            for ref_id in ro.source_semantic_states:
                assert ref_id in expected_ids, (
                    f"Reasoning Object for '{category}' references signal_id "
                    f"'{ref_id}' which is not in the Semantic States for that "
                    f"category. Available IDs: {expected_ids}"
                )

    @given(signal_outputs=full_signal_outputs_strategy)
    @settings(max_examples=200)
    def test_complete_coverage_all_14_categories(
        self, signal_outputs: dict
    ) -> None:
        """Property 4: Coverage is complete — all 14 categories have both semantic and reasoning output.

        **Validates: Requirements 2.1, 2.2**

        When valid signal outputs cover all 14 categories, the pipeline must
        produce both Semantic States and Reasoning Objects for every category.
        """
        orchestrator = _create_orchestrator()
        run_context = _create_run_context()

        # Execute full semantic + reasoning pipeline
        semantic_states = orchestrator._execute_semantic_engine(
            signal_outputs, run_context
        )
        reasoning_objects = orchestrator._execute_reasoning_engines(
            semantic_states, run_context
        )

        # Collect categories with semantic coverage
        semantic_categories = {
            state.get("category") for state in semantic_states
            if state.get("category")
        }

        # Collect categories with reasoning coverage
        reasoning_categories = {
            ro.conclusion.category for ro in reasoning_objects
        }

        # All 14 categories must have both
        for category in ALL_SIGNAL_CATEGORIES:
            assert category in semantic_categories, (
                f"Category '{category}' missing from semantic coverage. "
                f"Covered: {sorted(semantic_categories)}"
            )
            assert category in reasoning_categories, (
                f"Category '{category}' missing from reasoning coverage. "
                f"Covered: {sorted(reasoning_categories)}"
            )

    @given(signal_outputs=full_signal_outputs_strategy)
    @settings(max_examples=200)
    def test_no_duplicate_reasoning_objects_per_category(
        self, signal_outputs: dict
    ) -> None:
        """Property 5: No duplicate Reasoning Objects for the same category.

        **Validates: Requirements 2.2**

        The reasoning engine must produce exactly one Reasoning Object per
        category — no duplicates allowed.
        """
        orchestrator = _create_orchestrator()
        run_context = _create_run_context()

        # Execute semantic + reasoning pipeline
        semantic_states = orchestrator._execute_semantic_engine(
            signal_outputs, run_context
        )
        reasoning_objects = orchestrator._execute_reasoning_engines(
            semantic_states, run_context
        )

        # Check for duplicate categories
        categories_seen: list[str] = []
        for ro in reasoning_objects:
            category = ro.conclusion.category
            assert category not in categories_seen, (
                f"Duplicate Reasoning Object found for category '{category}'. "
                f"Each category must have exactly one Reasoning Object."
            )
            categories_seen.append(category)

        # Also verify total count matches expected
        assert len(reasoning_objects) == len(ALL_SIGNAL_CATEGORIES), (
            f"Expected {len(ALL_SIGNAL_CATEGORIES)} Reasoning Objects "
            f"(one per category), got {len(reasoning_objects)}. "
            f"Categories: {categories_seen}"
        )
