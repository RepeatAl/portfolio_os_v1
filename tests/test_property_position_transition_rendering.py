"""Property-based tests for Position Transition Rendering.

**Validates: Requirements 5.5**

Tests that transitions include notice with position_id, previous classification,
and new classification. Hypothesis generates random transition lists; verify
each transition is rendered with all three required fields visible in the output.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from engines.report_engine import ReportEngine


# --- Strategies ---

# Generate valid position identifiers (non-empty alphanumeric strings)
position_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=1,
    max_size=30,
)

# Generate classification labels (non-empty strings without markdown special chars)
classification_strategy = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N", "Z"),
        blacklist_characters="*_`|[]{}#<>",
    ),
    min_size=1,
    max_size=30,
)


@st.composite
def transition_strategy(draw: st.DrawFn) -> dict:
    """Generate a single transition dict with position_id, previous_classification,
    and new_classification."""
    return {
        "position_id": draw(position_id_strategy),
        "previous_classification": draw(classification_strategy),
        "new_classification": draw(classification_strategy),
    }


@st.composite
def transition_list_strategy(draw: st.DrawFn) -> list[dict]:
    """Generate a non-empty list of transition dicts."""
    return draw(st.lists(transition_strategy(), min_size=1, max_size=10))


@st.composite
def portfolio_state_with_transitions_strategy(draw: st.DrawFn) -> dict:
    """Generate a portfolio_state dict containing transitions."""
    transitions = draw(transition_list_strategy())
    # Include at least one position so the portfolio block renders normally
    positions = [
        {
            "position_id": f"EXISTING_{i}",
            "drivers": ["momentum"],
            "risks": ["volatility"],
        }
        for i in range(draw(st.integers(min_value=0, max_value=3)))
    ]
    return {
        "positions": positions,
        "transitions": transitions,
    }


class TestPositionTransitionRendering:
    """Property-based tests for Position Transition Rendering.

    **Validates: Requirements 5.5**

    Property 23: When a position transitions from Watchlist to Portfolio_State
    (or vice versa), the Report_Engine renders a transition notice stating the
    position identifier, the previous classification, and the new classification.
    """

    @given(portfolio_state=portfolio_state_with_transitions_strategy())
    @settings(max_examples=200, deadline=None)
    def test_transition_notice_contains_position_id(
        self, portfolio_state: dict
    ) -> None:
        """Every transition notice contains the position_id.

        **Validates: Requirements 5.5**

        For any generated transition list, each transition's position_id
        appears in the rendered output.
        """
        engine = ReportEngine()
        watchlist: dict = {"positions": [], "transitions": []}

        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        for transition in portfolio_state["transitions"]:
            position_id = transition["position_id"]
            assert position_id in output, (
                f"Transition notice missing position_id '{position_id}' "
                f"in rendered output."
            )

    @given(portfolio_state=portfolio_state_with_transitions_strategy())
    @settings(max_examples=200, deadline=None)
    def test_transition_notice_contains_previous_classification(
        self, portfolio_state: dict
    ) -> None:
        """Every transition notice contains the previous classification.

        **Validates: Requirements 5.5**

        For any generated transition list, each transition's
        previous_classification appears in the rendered output.
        """
        engine = ReportEngine()
        watchlist: dict = {"positions": [], "transitions": []}

        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        for transition in portfolio_state["transitions"]:
            previous = transition["previous_classification"]
            assert previous in output, (
                f"Transition notice missing previous_classification "
                f"'{previous}' in rendered output."
            )

    @given(portfolio_state=portfolio_state_with_transitions_strategy())
    @settings(max_examples=200, deadline=None)
    def test_transition_notice_contains_new_classification(
        self, portfolio_state: dict
    ) -> None:
        """Every transition notice contains the new classification.

        **Validates: Requirements 5.5**

        For any generated transition list, each transition's
        new_classification appears in the rendered output.
        """
        engine = ReportEngine()
        watchlist: dict = {"positions": [], "transitions": []}

        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        for transition in portfolio_state["transitions"]:
            new_class = transition["new_classification"]
            assert new_class in output, (
                f"Transition notice missing new_classification "
                f"'{new_class}' in rendered output."
            )

    @given(portfolio_state=portfolio_state_with_transitions_strategy())
    @settings(max_examples=200, deadline=None)
    def test_transition_notice_has_all_three_fields_per_entry(
        self, portfolio_state: dict
    ) -> None:
        """Each transition renders a single line containing all three fields.

        **Validates: Requirements 5.5**

        For any generated transition, there exists a line in the rendered
        output that contains the position_id, previous_classification, and
        new_classification together, confirming the notice is complete.
        """
        engine = ReportEngine()
        watchlist: dict = {"positions": [], "transitions": []}

        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)
        output_lines = output.split("\n")

        for transition in portfolio_state["transitions"]:
            position_id = transition["position_id"]
            previous = transition["previous_classification"]
            new_class = transition["new_classification"]

            # Find at least one line containing all three fields
            found = any(
                position_id in line and previous in line and new_class in line
                for line in output_lines
            )
            assert found, (
                f"No single line contains all three transition fields: "
                f"position_id='{position_id}', "
                f"previous_classification='{previous}', "
                f"new_classification='{new_class}'."
            )

    @given(transitions=transition_list_strategy())
    @settings(max_examples=200, deadline=None)
    def test_watchlist_transitions_also_rendered(
        self, transitions: list[dict]
    ) -> None:
        """Transitions in watchlist data are also rendered with all fields.

        **Validates: Requirements 5.5**

        Transitions can appear in either portfolio_state or watchlist.
        Both sources must render complete transition notices.
        """
        engine = ReportEngine()
        portfolio_state: dict = {"positions": [], "transitions": []}
        watchlist: dict = {"positions": [], "transitions": transitions}

        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        for transition in transitions:
            position_id = transition["position_id"]
            previous = transition["previous_classification"]
            new_class = transition["new_classification"]

            assert position_id in output, (
                f"Watchlist transition notice missing position_id "
                f"'{position_id}' in rendered output."
            )
            assert previous in output, (
                f"Watchlist transition notice missing "
                f"previous_classification '{previous}' in rendered output."
            )
            assert new_class in output, (
                f"Watchlist transition notice missing "
                f"new_classification '{new_class}' in rendered output."
            )

    @given(portfolio_state=portfolio_state_with_transitions_strategy())
    @settings(max_examples=200, deadline=None)
    def test_transition_section_header_present(
        self, portfolio_state: dict
    ) -> None:
        """When transitions exist, a 'Position Transitions' header is rendered.

        **Validates: Requirements 5.5**

        The rendered output must contain a recognizable transition section
        header when transitions are provided.
        """
        engine = ReportEngine()
        watchlist: dict = {"positions": [], "transitions": []}

        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        assert "Position Transitions" in output, (
            "Rendered output missing 'Position Transitions' header "
            "when transitions are provided."
        )
