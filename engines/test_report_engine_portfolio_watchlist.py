"""Unit tests for Portfolio State / Watchlist separation in ReportEngine.

Tests the render_portfolio_watchlist_blocks() method and its sub-methods
that implement Requirements 5.1–5.7:
- 5.1: "Current Portfolio Reality" block appears before "Watchlist" block
- 5.2: Watchlist block presents potential future exposures
- 5.3: Portfolio block sourced exclusively from Portfolio_State
- 5.4: Watchlist block sourced exclusively from Watchlist data
- 5.5: Position transitions include transition notice
- 5.6: Duplicate positions classified per Portfolio_State, omitted from Watchlist
- 5.7: Empty states render explicit empty-state notice

Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7
"""

import logging
from datetime import datetime, timezone, timedelta

import pytest

from engines.report_engine import ReportEngine
from runtime.reasoning_object import (
    ActionImplication,
    Conclusion,
    ReasoningObject,
    TemporalValidity,
)
from runtime.run_context import RunContext


# --- Helpers ---


def _make_run_context() -> RunContext:
    """Create a minimal RunContext for testing."""
    return RunContext(
        run_id="test-run-001",
        timestamp="2026-06-01T08:00:00Z",
        data_sources=[],
        schema_version="1.0.0",
        pipeline_state="healthy",
        report_hash=None,
    )


# --- Portfolio/Watchlist Block Tests ---


class TestPortfolioWatchlistSeparation:
    """Tests for ReportEngine.render_portfolio_watchlist_blocks().

    Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7
    """

    def setup_method(self):
        self.engine = ReportEngine()

    def test_portfolio_block_appears_before_watchlist_block(self):
        """Requirement 5.1: Current Portfolio Reality appears before Watchlist."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": ["momentum"], "risks": ["concentration"]},
            ],
        }
        watchlist = {
            "positions": [
                {"position_id": "MSFT", "entry_conditions": ["breakout"], "rationale": "diversification"},
            ],
        }
        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        portfolio_idx = result.index("## Current Portfolio Reality")
        watchlist_idx = result.index("## Watchlist and Deployment Candidates")
        assert portfolio_idx < watchlist_idx

    def test_portfolio_block_renders_positions(self):
        """Requirement 5.3: Portfolio block sourced from Portfolio_State."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": ["momentum", "earnings"], "risks": ["concentration"]},
                {"position_id": "NVDA", "drivers": ["AI growth"], "risks": ["valuation"]},
            ],
        }
        watchlist = {"positions": []}

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        assert "AAPL" in result
        assert "NVDA" in result
        assert "momentum, earnings" in result
        assert "AI growth" in result

    def test_watchlist_block_renders_positions(self):
        """Requirement 5.4: Watchlist block sourced from Watchlist data."""
        portfolio_state = {"positions": []}
        watchlist = {
            "positions": [
                {"position_id": "MSFT", "entry_conditions": ["breakout above 400"], "rationale": "diversification"},
                {"position_id": "AMZN", "entry_conditions": ["pullback to support"], "rationale": "cloud exposure"},
            ],
        }

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        assert "MSFT" in result
        assert "AMZN" in result
        assert "breakout above 400" in result
        assert "cloud exposure" in result

    def test_empty_portfolio_renders_empty_state_notice(self):
        """Requirement 5.7: Empty Portfolio_State renders explicit notice."""
        portfolio_state = {"positions": []}
        watchlist = {
            "positions": [
                {"position_id": "MSFT", "entry_conditions": ["breakout"], "rationale": "test"},
            ],
        }

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        assert "Empty State Notice" in result
        assert "No positions are currently present" in result

    def test_empty_watchlist_renders_empty_state_notice(self):
        """Requirement 5.7: Empty Watchlist renders explicit notice."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": ["momentum"], "risks": ["concentration"]},
            ],
        }
        watchlist = {"positions": []}

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        assert "Empty State Notice" in result
        assert "No deployment candidates" in result

    def test_both_empty_renders_both_empty_state_notices(self):
        """Requirement 5.7: Both empty states render notices."""
        portfolio_state = {"positions": []}
        watchlist = {"positions": []}

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        assert "No positions are currently present" in result
        assert "No deployment candidates" in result

    def test_duplicate_positions_classified_per_portfolio_state(self, caplog):
        """Requirement 5.6: Duplicates classified per Portfolio_State, omitted from Watchlist."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": ["momentum"], "risks": ["concentration"]},
            ],
        }
        watchlist = {
            "positions": [
                {"position_id": "AAPL", "entry_conditions": ["should not appear"], "rationale": "duplicate"},
                {"position_id": "MSFT", "entry_conditions": ["breakout"], "rationale": "valid"},
            ],
        }

        with caplog.at_level(logging.WARNING):
            result = self.engine.render_portfolio_watchlist_blocks(
                portfolio_state, watchlist
            )

        # AAPL should appear in portfolio block
        portfolio_idx = result.index("## Current Portfolio Reality")
        watchlist_idx = result.index("## Watchlist and Deployment Candidates")
        portfolio_area = result[portfolio_idx:watchlist_idx]
        assert "AAPL" in portfolio_area

        # AAPL should NOT appear in watchlist block
        watchlist_area = result[watchlist_idx:]
        # MSFT should be in watchlist
        assert "MSFT" in watchlist_area
        # "should not appear" text from the duplicate AAPL entry should not be in watchlist
        assert "should not appear" not in watchlist_area

        # Warning should be logged
        assert "Data conflict" in caplog.text
        assert "AAPL" in caplog.text

    def test_transition_notice_in_portfolio(self):
        """Requirement 5.5: Transitions include position_id, previous, new classification."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": ["momentum"], "risks": ["concentration"]},
            ],
            "transitions": [
                {
                    "position_id": "AAPL",
                    "previous_classification": "watchlist",
                    "new_classification": "portfolio",
                },
            ],
        }
        watchlist = {"positions": []}

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        assert "Position Transitions" in result
        assert "AAPL" in result
        assert "watchlist" in result
        assert "portfolio" in result
        assert "transitioned from" in result

    def test_transition_notice_in_watchlist(self):
        """Requirement 5.5: Transitions in watchlist block."""
        portfolio_state = {"positions": []}
        watchlist = {
            "positions": [
                {"position_id": "MSFT", "entry_conditions": ["breakout"], "rationale": "test"},
            ],
            "transitions": [
                {
                    "position_id": "MSFT",
                    "previous_classification": "portfolio",
                    "new_classification": "watchlist",
                },
            ],
        }

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        assert "Position Transitions" in result
        assert "MSFT" in result
        assert "portfolio" in result
        assert "watchlist" in result

    def test_no_transitions_when_none_provided(self):
        """No transition section when no transitions exist."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": ["momentum"], "risks": ["concentration"]},
            ],
        }
        watchlist = {
            "positions": [
                {"position_id": "MSFT", "entry_conditions": ["breakout"], "rationale": "test"},
            ],
        }

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        assert "Position Transitions" not in result

    def test_drivers_and_risks_as_strings(self):
        """Handles drivers/risks as plain strings (not lists)."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": "momentum", "risks": "concentration"},
            ],
        }
        watchlist = {"positions": []}

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        assert "momentum" in result
        assert "concentration" in result

    def test_missing_fields_use_defaults(self):
        """Positions with missing fields render gracefully."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL"},  # No drivers or risks
            ],
        }
        watchlist = {
            "positions": [
                {"position_id": "MSFT"},  # No entry_conditions or rationale
            ],
        }

        result = self.engine.render_portfolio_watchlist_blocks(
            portfolio_state, watchlist
        )

        # Should render with dash defaults
        assert "AAPL" in result
        assert "MSFT" in result


class TestPortfolioWatchlistInFullReport:
    """Tests that Portfolio/Watchlist blocks appear correctly in full render() output.

    Validates: Requirements 5.1, 5.2
    """

    def setup_method(self):
        self.engine = ReportEngine()
        self.run_context = _make_run_context()

    def test_full_render_includes_portfolio_and_watchlist_blocks(self):
        """Full render() includes both blocks."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": ["momentum"], "risks": ["concentration"]},
            ],
        }
        watchlist = {
            "positions": [
                {"position_id": "MSFT", "entry_conditions": ["breakout"], "rationale": "diversification"},
            ],
        }

        result = self.engine.render(
            reasoning_objects=[],
            deployment_matrix=None,
            portfolio_state=portfolio_state,
            watchlist=watchlist,
            run_context=self.run_context,
        )

        assert "## Current Portfolio Reality" in result
        assert "## Watchlist and Deployment Candidates" in result

    def test_full_render_portfolio_before_watchlist(self):
        """In full render, portfolio block appears before watchlist block."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": ["momentum"], "risks": ["concentration"]},
            ],
        }
        watchlist = {
            "positions": [
                {"position_id": "MSFT", "entry_conditions": ["breakout"], "rationale": "diversification"},
            ],
        }

        result = self.engine.render(
            reasoning_objects=[],
            deployment_matrix=None,
            portfolio_state=portfolio_state,
            watchlist=watchlist,
            run_context=self.run_context,
        )

        portfolio_idx = result.index("## Current Portfolio Reality")
        watchlist_idx = result.index("## Watchlist and Deployment Candidates")
        assert portfolio_idx < watchlist_idx

    def test_full_render_portfolio_watchlist_before_data_availability(self):
        """Portfolio/Watchlist blocks appear before Data Availability."""
        portfolio_state = {"positions": []}
        watchlist = {"positions": []}

        result = self.engine.render(
            reasoning_objects=[],
            deployment_matrix=None,
            portfolio_state=portfolio_state,
            watchlist=watchlist,
            run_context=self.run_context,
        )

        portfolio_idx = result.index("## Current Portfolio Reality")
        data_avail_idx = result.index("## Data Availability")
        assert portfolio_idx < data_avail_idx

    def test_full_render_with_empty_dicts(self):
        """Full render handles empty portfolio_state and watchlist dicts."""
        result = self.engine.render(
            reasoning_objects=[],
            deployment_matrix=None,
            portfolio_state={},
            watchlist={},
            run_context=self.run_context,
        )

        assert "## Current Portfolio Reality" in result
        assert "## Watchlist and Deployment Candidates" in result
        assert "Empty State Notice" in result

    def test_full_render_duplicate_handling(self, caplog):
        """Full render handles duplicates correctly."""
        portfolio_state = {
            "positions": [
                {"position_id": "AAPL", "drivers": ["momentum"], "risks": ["concentration"]},
            ],
        }
        watchlist = {
            "positions": [
                {"position_id": "AAPL", "entry_conditions": ["duplicate"], "rationale": "should be omitted"},
                {"position_id": "TSLA", "entry_conditions": ["breakout"], "rationale": "valid entry"},
            ],
        }

        with caplog.at_level(logging.WARNING):
            result = self.engine.render(
                reasoning_objects=[],
                deployment_matrix=None,
                portfolio_state=portfolio_state,
                watchlist=watchlist,
                run_context=self.run_context,
            )

        # AAPL in portfolio, not in watchlist
        watchlist_idx = result.index("## Watchlist and Deployment Candidates")
        data_avail_idx = result.index("## Data Availability")
        watchlist_area = result[watchlist_idx:data_avail_idx]

        assert "TSLA" in watchlist_area
        assert "should be omitted" not in watchlist_area

        # Warning logged
        assert "Data conflict" in caplog.text
