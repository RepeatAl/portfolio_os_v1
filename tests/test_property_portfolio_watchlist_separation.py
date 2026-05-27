"""Property-based tests for Portfolio/Watchlist Separation.

**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.6**

Tests that portfolio block appears before watchlist, positions are exclusive
to their block, duplicates resolve to Portfolio_State. Hypothesis generates
random position sets with overlaps; verify separation invariant holds.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from engines.report_engine import ReportEngine


# --- Strategies ---

position_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=1,
    max_size=20,
)

driver_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
    min_size=1,
    max_size=30,
)

risk_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
    min_size=1,
    max_size=30,
)

entry_condition_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
    min_size=1,
    max_size=30,
)

rationale_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
    min_size=1,
    max_size=50,
)


@st.composite
def portfolio_position_strategy(draw: st.DrawFn, position_id: str | None = None) -> dict:
    """Generate a portfolio position dict with position_id, drivers, risks."""
    pid = position_id if position_id else draw(position_id_strategy)
    drivers = draw(st.lists(driver_strategy, min_size=1, max_size=3))
    risks = draw(st.lists(risk_strategy, min_size=1, max_size=3))
    return {
        "position_id": pid,
        "drivers": drivers,
        "risks": risks,
    }


@st.composite
def watchlist_position_strategy(draw: st.DrawFn, position_id: str | None = None) -> dict:
    """Generate a watchlist position dict with position_id, entry_conditions, rationale."""
    pid = position_id if position_id else draw(position_id_strategy)
    entry_conditions = draw(st.lists(entry_condition_strategy, min_size=1, max_size=3))
    rationale = draw(rationale_strategy)
    return {
        "position_id": pid,
        "entry_conditions": entry_conditions,
        "rationale": rationale,
    }


@st.composite
def portfolio_watchlist_with_overlaps_strategy(draw: st.DrawFn) -> tuple[dict, dict]:
    """Generate portfolio_state and watchlist dicts with potential overlapping position_ids.

    Some positions appear in both to test duplicate resolution behavior.
    """
    # Generate unique position IDs for portfolio-only, watchlist-only, and shared
    num_portfolio_only = draw(st.integers(min_value=0, max_value=5))
    num_watchlist_only = draw(st.integers(min_value=0, max_value=5))
    num_shared = draw(st.integers(min_value=0, max_value=4))

    portfolio_only_ids = [f"PORT_{i}" for i in range(num_portfolio_only)]
    watchlist_only_ids = [f"WATCH_{i}" for i in range(num_watchlist_only)]
    shared_ids = [f"SHARED_{i}" for i in range(num_shared)]

    # Build portfolio positions (portfolio-only + shared)
    portfolio_positions = []
    for pid in portfolio_only_ids:
        portfolio_positions.append(draw(portfolio_position_strategy(position_id=pid)))
    for pid in shared_ids:
        portfolio_positions.append(draw(portfolio_position_strategy(position_id=pid)))

    # Build watchlist positions (watchlist-only + shared)
    watchlist_positions = []
    for pid in watchlist_only_ids:
        watchlist_positions.append(draw(watchlist_position_strategy(position_id=pid)))
    for pid in shared_ids:
        watchlist_positions.append(draw(watchlist_position_strategy(position_id=pid)))

    portfolio_state = {"positions": portfolio_positions}
    watchlist = {"positions": watchlist_positions}

    return portfolio_state, watchlist


class TestPortfolioWatchlistSeparation:
    """Property-based tests for Portfolio/Watchlist Separation.

    **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.6**

    Property 7: Portfolio block appears before watchlist, positions are
    exclusive to their block, duplicates resolve to Portfolio_State.
    """

    @given(data=portfolio_watchlist_with_overlaps_strategy())
    @settings(max_examples=200, deadline=None)
    def test_portfolio_block_appears_before_watchlist(
        self, data: tuple[dict, dict]
    ) -> None:
        """The "Current Portfolio Reality" heading appears before
        "Watchlist and Deployment Candidates" heading in rendered output.

        **Validates: Requirements 5.1**
        """
        portfolio_state, watchlist = data
        engine = ReportEngine()
        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        portfolio_heading = "## Current Portfolio Reality"
        watchlist_heading = "## Watchlist and Deployment Candidates"

        portfolio_idx = output.find(portfolio_heading)
        watchlist_idx = output.find(watchlist_heading)

        assert portfolio_idx != -1, (
            "Portfolio heading '## Current Portfolio Reality' not found in output."
        )
        assert watchlist_idx != -1, (
            "Watchlist heading '## Watchlist and Deployment Candidates' not found in output."
        )
        assert portfolio_idx < watchlist_idx, (
            f"Portfolio block (index {portfolio_idx}) does not appear before "
            f"Watchlist block (index {watchlist_idx})."
        )

    @given(data=portfolio_watchlist_with_overlaps_strategy())
    @settings(max_examples=200, deadline=None)
    def test_positions_are_exclusive_to_their_block(
        self, data: tuple[dict, dict]
    ) -> None:
        """No position_id appears in both the portfolio block and the watchlist block.

        **Validates: Requirements 5.3, 5.4, 5.6**

        Positions are exclusive: each position_id appears in at most one block.
        Duplicates (same position_id in both inputs) are resolved to Portfolio_State.
        """
        portfolio_state, watchlist = data
        engine = ReportEngine()
        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        # Split output into portfolio block and watchlist block
        watchlist_heading = "## Watchlist and Deployment Candidates"
        split_idx = output.find(watchlist_heading)
        assert split_idx != -1, "Watchlist heading not found in output."

        portfolio_block = output[:split_idx]
        watchlist_block = output[split_idx:]

        # Collect all position_ids from portfolio input
        portfolio_ids = {
            p["position_id"]
            for p in portfolio_state.get("positions", [])
            if p.get("position_id")
        }
        # Collect all position_ids from watchlist input
        watchlist_ids = {
            p["position_id"]
            for p in watchlist.get("positions", [])
            if p.get("position_id")
        }
        # Shared IDs (duplicates)
        shared_ids = portfolio_ids & watchlist_ids

        # Verify shared positions appear in portfolio block, NOT in watchlist block
        for shared_id in shared_ids:
            assert shared_id in portfolio_block, (
                f"Duplicate position '{shared_id}' should appear in portfolio block "
                f"but was not found there."
            )
            # The shared_id should NOT appear in the watchlist block's table rows
            # (it may appear in a transition notice, but not as a table entry)
            watchlist_table_section = watchlist_block.split("**Position Transitions:**")[0]
            # Check it's not in the watchlist table (between the heading and transitions)
            watchlist_lines = watchlist_table_section.split("\n")
            table_entries = [
                line for line in watchlist_lines
                if line.startswith("|") and "Position" not in line and "---" not in line
            ]
            watchlist_table_ids = set()
            for entry in table_entries:
                cells = [c.strip() for c in entry.split("|") if c.strip()]
                if cells:
                    watchlist_table_ids.add(cells[0])

            assert shared_id not in watchlist_table_ids, (
                f"Duplicate position '{shared_id}' should be omitted from "
                f"watchlist block but was found in watchlist table."
            )

    @given(data=portfolio_watchlist_with_overlaps_strategy())
    @settings(max_examples=200, deadline=None)
    def test_duplicates_resolve_to_portfolio_state(
        self, data: tuple[dict, dict]
    ) -> None:
        """When a position_id exists in both Portfolio_State and Watchlist,
        it is classified per Portfolio_State and omitted from Watchlist.

        **Validates: Requirements 5.6**
        """
        portfolio_state, watchlist = data
        engine = ReportEngine()
        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        # Identify shared position_ids
        portfolio_ids = {
            p["position_id"]
            for p in portfolio_state.get("positions", [])
            if p.get("position_id")
        }
        watchlist_ids = {
            p["position_id"]
            for p in watchlist.get("positions", [])
            if p.get("position_id")
        }
        shared_ids = portfolio_ids & watchlist_ids

        # Split into blocks
        watchlist_heading = "## Watchlist and Deployment Candidates"
        split_idx = output.find(watchlist_heading)
        portfolio_block = output[:split_idx]
        watchlist_block = output[split_idx:]

        # All shared IDs must be in portfolio block
        for shared_id in shared_ids:
            assert shared_id in portfolio_block, (
                f"Shared position '{shared_id}' not found in portfolio block. "
                f"Duplicates must resolve to Portfolio_State."
            )

        # Watchlist-only IDs (not shared) should appear in watchlist block
        watchlist_only_ids = watchlist_ids - shared_ids
        for wid in watchlist_only_ids:
            assert wid in watchlist_block, (
                f"Watchlist-only position '{wid}' not found in watchlist block."
            )

    @given(data=portfolio_watchlist_with_overlaps_strategy())
    @settings(max_examples=200, deadline=None)
    def test_portfolio_only_positions_in_portfolio_block(
        self, data: tuple[dict, dict]
    ) -> None:
        """Portfolio-only positions appear exclusively in the portfolio block.

        **Validates: Requirements 5.3**
        """
        portfolio_state, watchlist = data
        engine = ReportEngine()
        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        portfolio_ids = {
            p["position_id"]
            for p in portfolio_state.get("positions", [])
            if p.get("position_id")
        }
        watchlist_ids = {
            p["position_id"]
            for p in watchlist.get("positions", [])
            if p.get("position_id")
        }
        portfolio_only_ids = portfolio_ids - watchlist_ids

        # Split into blocks
        watchlist_heading = "## Watchlist and Deployment Candidates"
        split_idx = output.find(watchlist_heading)
        portfolio_block = output[:split_idx]

        for pid in portfolio_only_ids:
            assert pid in portfolio_block, (
                f"Portfolio-only position '{pid}' not found in portfolio block."
            )

    @given(data=portfolio_watchlist_with_overlaps_strategy())
    @settings(max_examples=200, deadline=None)
    def test_watchlist_only_positions_in_watchlist_block(
        self, data: tuple[dict, dict]
    ) -> None:
        """Watchlist-only positions appear exclusively in the watchlist block.

        **Validates: Requirements 5.4**
        """
        portfolio_state, watchlist = data
        engine = ReportEngine()
        output = engine.render_portfolio_watchlist_blocks(portfolio_state, watchlist)

        portfolio_ids = {
            p["position_id"]
            for p in portfolio_state.get("positions", [])
            if p.get("position_id")
        }
        watchlist_ids = {
            p["position_id"]
            for p in watchlist.get("positions", [])
            if p.get("position_id")
        }
        watchlist_only_ids = watchlist_ids - portfolio_ids

        # Split into blocks
        watchlist_heading = "## Watchlist and Deployment Candidates"
        split_idx = output.find(watchlist_heading)
        watchlist_block = output[split_idx:]

        for wid in watchlist_only_ids:
            assert wid in watchlist_block, (
                f"Watchlist-only position '{wid}' not found in watchlist block."
            )

    @given(data=portfolio_watchlist_with_overlaps_strategy())
    @settings(max_examples=200, deadline=None)
    def test_empty_portfolio_renders_empty_state_notice(
        self, data: tuple[dict, dict]
    ) -> None:
        """When portfolio has zero positions, an empty-state notice is rendered.

        **Validates: Requirements 5.1**
        """
        _, watchlist = data
        # Force empty portfolio
        empty_portfolio = {"positions": []}
        engine = ReportEngine()
        output = engine.render_portfolio_watchlist_blocks(empty_portfolio, watchlist)

        # Split into blocks
        watchlist_heading = "## Watchlist and Deployment Candidates"
        split_idx = output.find(watchlist_heading)
        portfolio_block = output[:split_idx]

        assert "Empty State Notice" in portfolio_block, (
            "Empty portfolio should render an empty-state notice in the "
            "portfolio block."
        )

    @given(data=portfolio_watchlist_with_overlaps_strategy())
    @settings(max_examples=200, deadline=None)
    def test_empty_watchlist_renders_empty_state_notice(
        self, data: tuple[dict, dict]
    ) -> None:
        """When watchlist has zero positions, an empty-state notice is rendered.

        **Validates: Requirements 5.2**
        """
        portfolio_state, _ = data
        # Force empty watchlist
        empty_watchlist = {"positions": []}
        engine = ReportEngine()
        output = engine.render_portfolio_watchlist_blocks(portfolio_state, empty_watchlist)

        # Split into blocks
        watchlist_heading = "## Watchlist and Deployment Candidates"
        split_idx = output.find(watchlist_heading)
        watchlist_block = output[split_idx:]

        assert "Empty State Notice" in watchlist_block, (
            "Empty watchlist should render an empty-state notice in the "
            "watchlist block."
        )
