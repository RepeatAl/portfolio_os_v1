"""Property-based tests for Governance Event Completeness.

**Validates: Requirements 17.2, 17.4, 18.2, 18.4**

Tests that every governance event emitted by handle_engine_failure() includes
severity, description, component identifier, and timestamp. Hypothesis generates
random engine failures; verifies all events contain required fields with valid values.
"""

from datetime import datetime, timezone

from hypothesis import given, settings
from hypothesis import strategies as st

from engines.pipeline_orchestrator import (
    ALL_SIGNAL_CATEGORIES,
    EngineTimeoutError,
    PipelineOrchestrator,
)
from runtime.severity_taxonomy import Severity


# Valid severity names from the canonical taxonomy
VALID_SEVERITY_NAMES = [s.name for s in Severity]

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

# Strategies
engine_id_strategy = st.sampled_from(ALL_ENGINE_IDS)
error_type_strategy = st.sampled_from(["timeout", "generic"])
error_message_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
    min_size=1,
    max_size=100,
)


def _make_error(engine_id: str, error_type: str) -> Exception:
    """Create an error instance based on the error type string."""
    if error_type == "timeout":
        return EngineTimeoutError(engine_id)
    return RuntimeError(f"Engine {engine_id} failed unexpectedly")


def _create_orchestrator() -> PipelineOrchestrator:
    """Create a PipelineOrchestrator without loading config."""
    orchestrator = PipelineOrchestrator.__new__(PipelineOrchestrator)
    orchestrator._severity_events = []
    orchestrator._degraded_categories = []
    orchestrator._component_states = []
    return orchestrator


class TestGovernanceEventCompleteness:
    """Property-based tests for governance event completeness."""

    @given(engine_id=engine_id_strategy, error_type=error_type_strategy)
    @settings(max_examples=200)
    def test_severity_event_contains_all_required_fields(
        self, engine_id: str, error_type: str
    ) -> None:
        """Property 1: Every severity event emitted by handle_engine_failure()
        contains: severity, message, source, timestamp.

        **Validates: Requirements 17.2, 17.4**

        Every governance event must include all four required fields to ensure
        complete observability and auditability.
        """
        orchestrator = _create_orchestrator()
        error = _make_error(engine_id, error_type)
        orchestrator.handle_engine_failure(engine_id, error)

        assert len(orchestrator._severity_events) >= 1, (
            f"No severity event emitted for engine '{engine_id}' failure"
        )

        for event in orchestrator._severity_events:
            assert "severity" in event, (
                f"Event missing 'severity' field: {event}"
            )
            assert "message" in event, (
                f"Event missing 'message' field: {event}"
            )
            assert "source" in event, (
                f"Event missing 'source' field: {event}"
            )
            assert "timestamp" in event, (
                f"Event missing 'timestamp' field: {event}"
            )

    @given(engine_id=engine_id_strategy, error_type=error_type_strategy)
    @settings(max_examples=200)
    def test_severity_field_is_valid_severity_name(
        self, engine_id: str, error_type: str
    ) -> None:
        """Property 2: severity field is always a valid Severity name
        (INFO, WARNING, DEGRADED, CRITICAL, CANONICAL_BREAK, DETERMINISTIC_FAILURE).

        **Validates: Requirements 17.2, 18.2**

        The severity field must use one of the canonical severity level names
        defined in the severity taxonomy.
        """
        orchestrator = _create_orchestrator()
        error = _make_error(engine_id, error_type)
        orchestrator.handle_engine_failure(engine_id, error)

        for event in orchestrator._severity_events:
            assert event["severity"] in VALID_SEVERITY_NAMES, (
                f"Event severity '{event['severity']}' is not a valid Severity name. "
                f"Valid names: {VALID_SEVERITY_NAMES}"
            )

    @given(engine_id=engine_id_strategy, error_type=error_type_strategy)
    @settings(max_examples=200)
    def test_message_field_is_non_empty_string(
        self, engine_id: str, error_type: str
    ) -> None:
        """Property 3: message field is always a non-empty string.

        **Validates: Requirements 17.4, 18.4**

        The message (description) field must be a non-empty string providing
        a human-readable description of the governance event.
        """
        orchestrator = _create_orchestrator()
        error = _make_error(engine_id, error_type)
        orchestrator.handle_engine_failure(engine_id, error)

        for event in orchestrator._severity_events:
            assert isinstance(event["message"], str), (
                f"Event message is not a string: {type(event['message'])}"
            )
            assert len(event["message"]) > 0, (
                f"Event message is empty for engine '{engine_id}'"
            )

    @given(engine_id=engine_id_strategy, error_type=error_type_strategy)
    @settings(max_examples=200)
    def test_source_field_is_non_empty_string(
        self, engine_id: str, error_type: str
    ) -> None:
        """Property 4: source field is always a non-empty string identifying the component.

        **Validates: Requirements 17.2, 18.2**

        The source (component identifier) field must be a non-empty string
        that identifies which component emitted the governance event.
        """
        orchestrator = _create_orchestrator()
        error = _make_error(engine_id, error_type)
        orchestrator.handle_engine_failure(engine_id, error)

        for event in orchestrator._severity_events:
            assert isinstance(event["source"], str), (
                f"Event source is not a string: {type(event['source'])}"
            )
            assert len(event["source"]) > 0, (
                f"Event source is empty for engine '{engine_id}'"
            )

    @given(engine_id=engine_id_strategy, error_type=error_type_strategy)
    @settings(max_examples=200)
    def test_timestamp_field_is_valid_iso8601_utc(
        self, engine_id: str, error_type: str
    ) -> None:
        """Property 5: timestamp field is always a valid ISO 8601 UTC string.

        **Validates: Requirements 17.4, 18.4**

        The timestamp field must be a valid ISO 8601 UTC string ending with 'Z'
        that can be parsed into a datetime object.
        """
        orchestrator = _create_orchestrator()
        error = _make_error(engine_id, error_type)
        orchestrator.handle_engine_failure(engine_id, error)

        for event in orchestrator._severity_events:
            timestamp = event["timestamp"]
            assert isinstance(timestamp, str), (
                f"Event timestamp is not a string: {type(timestamp)}"
            )
            assert timestamp.endswith("Z"), (
                f"Event timestamp does not end with 'Z' (not UTC): '{timestamp}'"
            )
            # Verify it parses as a valid ISO 8601 datetime
            try:
                parsed = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError as e:
                raise AssertionError(
                    f"Event timestamp '{timestamp}' is not valid ISO 8601 UTC: {e}"
                )
            # Verify the parsed datetime is reasonable (not in the far past/future)
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            diff = abs((now - parsed).total_seconds())
            assert diff < 60, (
                f"Event timestamp '{timestamp}' is more than 60 seconds from now, "
                f"suggesting an invalid or stale timestamp"
            )
