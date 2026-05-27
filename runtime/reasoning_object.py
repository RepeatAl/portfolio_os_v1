"""Reasoning Object schema and TemporalValidity model.

Formal contract between the REASONING and REPORT layers of the canonical chain.
Each Reasoning Engine produces exactly one ReasoningObject per signal category.
The Report Engine rejects objects failing validate().

Requirements: 9.1, 9.2
"""

from dataclasses import dataclass
from datetime import datetime, timezone


VALID_PRODUCING_ENGINES = frozenset({
    "decision_engine",
    "quality_engine",
    "priority_engine",
})


@dataclass
class TemporalValidity:
    """Explicit temporal validity model (Hardening 5).

    Replaces anonymous tuple semantics with named fields and stale-state handling.
    All timestamps are ISO 8601 UTC.
    """

    valid_from: str
    valid_until: str
    stale_after: str | None = None

    @property
    def validity_state(self) -> str:
        """Return 'valid', 'stale', or 'expired' based on current time vs boundaries."""
        now = datetime.now(timezone.utc)
        try:
            until = datetime.fromisoformat(self.valid_until)
            if until.tzinfo is None:
                until = until.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            return "expired"

        if now >= until:
            return "expired"

        if self.stale_after is not None:
            try:
                stale = datetime.fromisoformat(self.stale_after)
                if stale.tzinfo is None:
                    stale = stale.replace(tzinfo=timezone.utc)
                if now >= stale:
                    return "stale"
            except (ValueError, TypeError):
                pass

        return "valid"


@dataclass
class ActionImplication:
    """What could be done and why it matters."""

    action: str
    rationale: str


@dataclass
class Conclusion:
    """Portfolio-level conclusion from reasoning.

    summary: 1-1000 characters describing the conclusion.
    category: Signal category this conclusion addresses.
    """

    summary: str
    category: str


@dataclass
class ReasoningObject:
    """Formal schema for the interface between REASONING and REPORT layers.

    Each Reasoning Engine produces exactly one ReasoningObject per signal category.
    The Report Engine rejects objects failing validate().
    source_semantic_states must reference signal_ids from the current RunContext's
    semantic snapshot.
    """

    reasoning_id: str
    source_semantic_states: list[str]
    conclusion: Conclusion
    confidence_level: int
    confidence_explanation: str
    action_implications: list[ActionImplication]
    temporal_validity: TemporalValidity
    producing_engine: str
    schema_version: str = "1.0.0"

    def validate(self) -> list[str]:
        """Return list of validation errors. Empty list = valid."""
        errors: list[str] = []

        # reasoning_id: 1-128 characters, non-empty
        if not self.reasoning_id or not isinstance(self.reasoning_id, str):
            errors.append("reasoning_id must be a non-empty string")
        elif len(self.reasoning_id) > 128:
            errors.append("reasoning_id must be 1-128 characters")

        # source_semantic_states: 1-50 entries, each non-empty string
        if not isinstance(self.source_semantic_states, list):
            errors.append("source_semantic_states must be a list")
        elif len(self.source_semantic_states) < 1:
            errors.append("source_semantic_states must have at least 1 entry")
        elif len(self.source_semantic_states) > 50:
            errors.append("source_semantic_states must have at most 50 entries")
        else:
            for i, state_id in enumerate(self.source_semantic_states):
                if not state_id or not isinstance(state_id, str):
                    errors.append(
                        f"source_semantic_states[{i}] must be a non-empty string"
                    )

        # conclusion.summary: 1-1000 characters
        if not isinstance(self.conclusion, Conclusion):
            errors.append("conclusion must be a Conclusion instance")
        else:
            if not self.conclusion.summary or not isinstance(self.conclusion.summary, str):
                errors.append("conclusion.summary must be a non-empty string")
            elif len(self.conclusion.summary) > 1000:
                errors.append("conclusion.summary must be 1-1000 characters")
            # conclusion.category: non-empty string
            if not self.conclusion.category or not isinstance(self.conclusion.category, str):
                errors.append("conclusion.category must be a non-empty string")

        # confidence_level: integer 0-100
        if not isinstance(self.confidence_level, int):
            errors.append("confidence_level must be an integer")
        elif self.confidence_level < 0 or self.confidence_level > 100:
            errors.append("confidence_level must be between 0 and 100")

        # confidence_explanation: 1-500 characters
        if not self.confidence_explanation or not isinstance(self.confidence_explanation, str):
            errors.append("confidence_explanation must be a non-empty string")
        elif len(self.confidence_explanation) > 500:
            errors.append("confidence_explanation must be 1-500 characters")

        # action_implications: 0-20 entries, each with non-empty action and rationale
        if not isinstance(self.action_implications, list):
            errors.append("action_implications must be a list")
        elif len(self.action_implications) > 20:
            errors.append("action_implications must have at most 20 entries")
        else:
            for i, impl in enumerate(self.action_implications):
                if not isinstance(impl, ActionImplication):
                    errors.append(
                        f"action_implications[{i}] must be an ActionImplication instance"
                    )
                else:
                    if not impl.action or not isinstance(impl.action, str):
                        errors.append(
                            f"action_implications[{i}].action must be a non-empty string"
                        )
                    if not impl.rationale or not isinstance(impl.rationale, str):
                        errors.append(
                            f"action_implications[{i}].rationale must be a non-empty string"
                        )

        # producing_engine: must be one of the valid engines
        if self.producing_engine not in VALID_PRODUCING_ENGINES:
            errors.append(
                f"producing_engine must be one of: {', '.join(sorted(VALID_PRODUCING_ENGINES))}"
            )

        # schema_version: non-empty string
        if not self.schema_version or not isinstance(self.schema_version, str):
            errors.append("schema_version must be a non-empty string")

        return errors
