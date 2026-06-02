"""Property-based tests for Data Availability Summary Completeness.

**Validates: Requirements 11.5**

Tests that every pipeline execution includes Data Availability summary with
all 14 categories having exactly one status. Hypothesis generates random sets
of Reasoning Objects; verify the rendered report always contains the Data
Availability section with all 14 signal categories, each having exactly one
status (available or unavailable_no_output).
"""

from hypothesis import given, settings, assume, HealthCheck
from hypothesis import strategies as st

from engines.report_engine import (
    ReportEngine,
    CANONICAL_SECTIONS,
    CATEGORY_TO_SECTION,
)
from runtime.reasoning_object import (
    ActionImplication,
    Conclusion,
    ReasoningObject,
    TemporalValidity,
    VALID_PRODUCING_ENGINES,
)
from runtime.run_context import RunContext


# --- Constants ---

ALL_SIGNAL_CATEGORIES = sorted(CATEGORY_TO_SECTION.keys())
VALID_STATUSES = {"available", "unavailable_no_output"}


# --- Strategies ---

valid_temporal_validity_strategy = st.builds(
    TemporalValidity,
    valid_from=st.just("2026-01-01T00:00:00+00:00"),
    valid_until=st.just("2026-12-31T23:59:59+00:00"),
    stale_after=st.just(None),
)

valid_action_implication_strategy = st.builds(
    ActionImplication,
    action=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
        min_size=1,
        max_size=30,
    ),
    rationale=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
        min_size=1,
        max_size=30,
    ),
)


def reasoning_object_for_category(category: str) -> st.SearchStrategy[ReasoningObject]:
    """Strategy that generates a valid ReasoningObject for a given signal category."""
    return st.builds(
        ReasoningObject,
        reasoning_id=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N")),
            min_size=1,
            max_size=64,
        ),
        source_semantic_states=st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("L", "N")),
                min_size=1,
                max_size=30,
            ),
            min_size=1,
            max_size=5,
        ),
        conclusion=st.builds(
            Conclusion,
            summary=st.text(
                alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
                min_size=1,
                max_size=100,
            ),
            category=st.just(category),
        ),
        confidence_level=st.integers(min_value=50, max_value=100),
        confidence_explanation=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
            min_size=1,
            max_size=100,
        ),
        action_implications=st.lists(
            valid_action_implication_strategy, min_size=0, max_size=3
        ),
        temporal_validity=valid_temporal_validity_strategy,
        producing_engine=st.sampled_from(sorted(VALID_PRODUCING_ENGINES)),
        schema_version=st.just("1.0.0"),
    )


# Strategy for a random subset of signal categories (some available, some not)
available_categories_strategy = st.lists(
    st.sampled_from(ALL_SIGNAL_CATEGORIES),
    min_size=0,
    max_size=len(ALL_SIGNAL_CATEGORIES),
    unique=True,
)


@st.composite
def random_reasoning_objects_strategy(draw):
    """Generate a random set of ReasoningObjects for a random subset of categories."""
    categories = draw(available_categories_strategy)
    objects = []
    for category in categories:
        obj = draw(reasoning_object_for_category(category))
        assume(obj.validate() == [])
        objects.append(obj)
    return objects


def make_run_context() -> RunContext:
    """Create a minimal RunContext for testing."""
    return RunContext(
        run_id="test-run-001",
        timestamp="2026-06-01T12:00:00Z",
        data_sources=[],
        schema_version="1.0.0",
        pipeline_state="healthy",
        report_hash=None,
    )


class TestDataAvailabilitySummaryCompleteness:
    """Property-based tests for Data Availability Summary Completeness (Property 24)."""

    @given(reasoning_objects=random_reasoning_objects_strategy())
    @settings(max_examples=200, deadline=None)
    def test_render_output_contains_data_availability_section(
        self, reasoning_objects: list[ReasoningObject]
    ) -> None:
        """Property 1: render() output always contains "## Data Availability".

        **Validates: Requirements 11.5**

        For any random set of Reasoning Objects (including empty set),
        the rendered report must always contain the Data Availability
        section header.
        """
        engine = ReportEngine()
        run_context = make_run_context()

        report = engine.render(
            reasoning_objects=reasoning_objects,
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=run_context,
        )

        assert "## Data Availability" in report, (
            f"Data Availability section header not found in rendered report. "
            f"Available categories: "
            f"{[obj.conclusion.category for obj in reasoning_objects]}"
        )

    @given(reasoning_objects=random_reasoning_objects_strategy())
    @settings(max_examples=200, deadline=None)
    def test_all_14_categories_appear_in_data_availability_table(
        self, reasoning_objects: list[ReasoningObject]
    ) -> None:
        """Property 2: All 14 categories appear in the Data Availability table.

        **Validates: Requirements 11.5**

        For any random set of Reasoning Objects, the Data Availability
        table must list all 14 signal categories regardless of which
        categories have available Reasoning Objects.
        """
        engine = ReportEngine()
        run_context = make_run_context()

        report = engine.render(
            reasoning_objects=reasoning_objects,
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=run_context,
        )

        # Extract the Data Availability section
        da_start = report.index("## Data Availability")
        da_content = report[da_start:]

        # Verify all 14 categories appear in the table
        for category in ALL_SIGNAL_CATEGORIES:
            assert f"| {category} |" in da_content, (
                f"Signal category '{category}' not found in Data Availability table. "
                f"Expected all 14 categories to be listed. "
                f"Available reasoning objects for categories: "
                f"{[obj.conclusion.category for obj in reasoning_objects]}"
            )

    @given(reasoning_objects=random_reasoning_objects_strategy())
    @settings(max_examples=200, deadline=None)
    def test_each_category_has_exactly_one_status(
        self, reasoning_objects: list[ReasoningObject]
    ) -> None:
        """Property 3: Each category has exactly one status (available or unavailable_no_output).

        **Validates: Requirements 11.5**

        For any random set of Reasoning Objects, each signal category
        in the Data Availability table must have exactly one status value
        that is either "available" or "unavailable_no_output".
        """
        engine = ReportEngine()
        run_context = make_run_context()

        report = engine.render(
            reasoning_objects=reasoning_objects,
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=run_context,
        )

        # Extract the Data Availability section
        da_start = report.index("## Data Availability")
        da_content = report[da_start:]

        # Parse the table rows to extract category → status mapping
        category_statuses: dict[str, list[str]] = {cat: [] for cat in ALL_SIGNAL_CATEGORIES}

        for line in da_content.split("\n"):
            # Table rows look like: | category | status |
            if line.startswith("| ") and " | " in line and not line.startswith("|-"):
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) == 2:
                    cat_name, status = parts[0], parts[1]
                    if cat_name in category_statuses:
                        category_statuses[cat_name].append(status)

        # Verify each category has exactly one status
        for category in ALL_SIGNAL_CATEGORIES:
            statuses = category_statuses[category]
            assert len(statuses) == 1, (
                f"Category '{category}' has {len(statuses)} status entries "
                f"(expected exactly 1). Statuses found: {statuses}"
            )

            # Verify the status is one of the valid values
            assert statuses[0] in VALID_STATUSES, (
                f"Category '{category}' has invalid status '{statuses[0]}'. "
                f"Expected one of: {VALID_STATUSES}"
            )

        # Additionally verify that categories with valid reasoning objects
        # are marked "available" and those without are "unavailable_no_output"
        available_categories = set()
        for obj in reasoning_objects:
            if not obj.validate():
                available_categories.add(obj.conclusion.category)

        for category in ALL_SIGNAL_CATEGORIES:
            expected_status = (
                "available" if category in available_categories
                else "unavailable_no_output"
            )
            actual_status = category_statuses[category][0]
            assert actual_status == expected_status, (
                f"Category '{category}' has status '{actual_status}' but expected "
                f"'{expected_status}'. Category {'has' if category in available_categories else 'does not have'} "
                f"valid Reasoning Objects."
            )
