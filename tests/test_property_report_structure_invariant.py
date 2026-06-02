"""Property-based tests for Report Structure Invariant.

**Validates: Requirements 6.1, 6.4**

Tests that all 9 sections appear in fixed order with either content or
degradation notice. Hypothesis generates random sets of available/unavailable
Reasoning Objects; verify section order is always preserved and each section
has non-empty content.
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


# --- Strategies ---

# All signal categories that map to report sections
ALL_SIGNAL_CATEGORIES = sorted(CATEGORY_TO_SECTION.keys())

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
def reasoning_objects_for_categories(draw, categories):
    """Generate a list of valid ReasoningObjects for the given categories."""
    objects = []
    for category in categories:
        obj = draw(reasoning_object_for_category(category))
        assume(obj.validate() == [])
        objects.append(obj)
    return objects


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


class TestReportStructureInvariant:
    """Property-based tests for Report Structure Invariant (Property 8)."""

    @given(reasoning_objects=random_reasoning_objects_strategy())
    @settings(max_examples=200, deadline=None)
    def test_render_output_contains_all_9_section_headers_in_canonical_order(
        self, reasoning_objects: list[ReasoningObject]
    ) -> None:
        """Property 1: render() output always contains all 9 section headers in canonical order.

        **Validates: Requirements 6.1**

        For any random set of available/unavailable Reasoning Objects,
        the rendered report must contain all 9 canonical section headers
        in the fixed canonical order.
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

        # Verify all 9 section headers appear
        for section_name in CANONICAL_SECTIONS:
            header = f"## {section_name}"
            assert header in report, (
                f"Section header '## {section_name}' not found in rendered report. "
                f"Available categories: "
                f"{[obj.conclusion.category for obj in reasoning_objects]}"
            )

        # Verify canonical order is preserved
        section_positions = []
        for section_name in CANONICAL_SECTIONS:
            header = f"## {section_name}"
            pos = report.index(header)
            section_positions.append(pos)

        for i in range(len(section_positions) - 1):
            assert section_positions[i] < section_positions[i + 1], (
                f"Section order violated: '{CANONICAL_SECTIONS[i]}' (pos {section_positions[i]}) "
                f"appears after '{CANONICAL_SECTIONS[i + 1]}' (pos {section_positions[i + 1]}). "
                f"Expected canonical order to be preserved."
            )

    @given(reasoning_objects=random_reasoning_objects_strategy())
    @settings(max_examples=200, deadline=None)
    def test_each_section_has_content_or_degradation_notice(
        self, reasoning_objects: list[ReasoningObject]
    ) -> None:
        """Property 2: Each section has either content or degradation notice (never empty).

        **Validates: Requirements 6.4**

        For any random set of available/unavailable Reasoning Objects,
        every section in the rendered report must contain either
        Reasoning Object-derived content or a degradation notice.
        No section may be empty.
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

        # Extract content between section headers
        lines = report.split("\n")
        section_contents: dict[str, str] = {}

        for i, section_name in enumerate(CANONICAL_SECTIONS):
            header = f"## {section_name}"
            # Find the header line
            header_idx = None
            for line_idx, line in enumerate(lines):
                if line.strip() == header:
                    header_idx = line_idx
                    break

            assert header_idx is not None, (
                f"Section header '## {section_name}' not found in report"
            )

            # Find the next section header or end of report
            next_header_idx = len(lines)
            for line_idx in range(header_idx + 1, len(lines)):
                if lines[line_idx].startswith("## "):
                    next_header_idx = line_idx
                    break

            # Extract content between headers (skip empty lines right after header)
            content_lines = lines[header_idx + 1 : next_header_idx]
            content = "\n".join(content_lines).strip()
            section_contents[section_name] = content

        # Verify each section has non-empty content
        for section_name, content in section_contents.items():
            assert len(content) > 0, (
                f"Section '{section_name}' has empty content. "
                f"Expected either Reasoning Object content or degradation notice. "
                f"Available categories: "
                f"{[obj.conclusion.category for obj in reasoning_objects]}"
            )

    @given(reasoning_objects=random_reasoning_objects_strategy())
    @settings(max_examples=200, deadline=None)
    def test_section_order_is_deterministic_regardless_of_input_order(
        self, reasoning_objects: list[ReasoningObject]
    ) -> None:
        """Property 3: Section order is deterministic regardless of input order.

        **Validates: Requirements 6.1**

        For any set of Reasoning Objects, rendering the report with the
        objects in different orders must produce the same section ordering.
        The canonical section order is fixed and independent of input order.
        """
        engine = ReportEngine()
        run_context = make_run_context()

        # Render with original order
        report_original = engine.render(
            reasoning_objects=reasoning_objects,
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=run_context,
        )

        # Render with reversed order
        reversed_objects = list(reversed(reasoning_objects))
        report_reversed = engine.render(
            reasoning_objects=reversed_objects,
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=run_context,
        )

        # Extract section header positions from both reports
        def get_section_order(report_text: str) -> list[str]:
            """Extract section names in order of appearance."""
            sections_found = []
            for line in report_text.split("\n"):
                if line.startswith("## ") and line[3:] in CANONICAL_SECTIONS:
                    sections_found.append(line[3:])
            return sections_found

        order_original = get_section_order(report_original)
        order_reversed = get_section_order(report_reversed)

        assert order_original == order_reversed, (
            f"Section order differs between original and reversed input order.\n"
            f"Original order: {order_original}\n"
            f"Reversed order: {order_reversed}\n"
            f"Expected canonical order to be preserved regardless of input order."
        )

        # Both should match canonical order
        assert order_original == CANONICAL_SECTIONS, (
            f"Section order does not match canonical order.\n"
            f"Got: {order_original}\n"
            f"Expected: {CANONICAL_SECTIONS}"
        )
