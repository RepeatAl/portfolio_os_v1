"""Governance State Provenance Tagger.

Tags governance state with provenance indicators that communicate the source
and reliability of the current governance state. Every governance decision
carries an explicit provenance tag so auditors and downstream consumers know
whether the state is authoritative, cached, derived from fallback logic,
generated during cold-start, partially degraded, or indeterminate.

Validates: Requirements 41.1, 41.2, 41.3, 41.4, 41.5, 41.6
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from dataclasses import dataclass, field


class GovernanceProvenance(StrEnum):
    """Provenance indicator for governance state.

    Each value communicates the source and reliability of the governance
    state under which a decision was made.

    Values:
        AUTHORITATIVE: Loaded from canonical source and validated.
        CACHED: Loaded from last-known-good cache; source unavailable.
        FALLBACK_DERIVED: Computed from fallback logic due to component failure.
        BOOTSTRAP_DERIVED: Generated during cold-start initialization.
        PARTIALLY_DEGRADED: Some components authoritative, some unavailable.
        INDETERMINATE: Provenance cannot be determined.
    """

    AUTHORITATIVE = "authoritative"
    CACHED = "cached"
    FALLBACK_DERIVED = "fallback_derived"
    BOOTSTRAP_DERIVED = "bootstrap_derived"
    PARTIALLY_DEGRADED = "partially_degraded"
    INDETERMINATE = "indeterminate"

    @classmethod
    def from_string(cls, value: str) -> GovernanceProvenance:
        """Deserialize a string value to a GovernanceProvenance enum member.

        Args:
            value: The string representation of the provenance tag.

        Returns:
            The corresponding GovernanceProvenance enum member.

        Raises:
            ValueError: If the value does not match any known provenance tag.
        """
        try:
            return cls(value)
        except ValueError:
            valid = ", ".join(member.value for member in cls)
            raise ValueError(
                f"Invalid provenance value '{value}'. "
                f"Valid values: {valid}"
            )

    def to_string(self) -> str:
        """Serialize the provenance tag to its string representation.

        Returns:
            The string value of this provenance tag.
        """
        return self.value


# Sentinel sources that indicate fallback behavior
FALLBACK_SOURCES: frozenset[str] = frozenset({
    "fallback",
    "fallback_config",
    "fallback_registry",
    "default_fallback",
    "emergency_fallback",
})


@dataclass
class ProvenanceEvent:
    """A recorded provenance tagging event for audit purposes.

    Attributes:
        provenance: The provenance tag that was assigned.
        source: The source identifier that was evaluated.
        timestamp: ISO 8601 timestamp of when the tag was assigned.
        reason: Human-readable explanation of why this provenance was assigned.
    """

    provenance: GovernanceProvenance
    source: str
    timestamp: str
    reason: str

    def to_dict(self) -> dict:
        """Serialize to a dictionary for YAML persistence.

        Returns:
            Dictionary representation suitable for YAML serialization.
        """
        return {
            "provenance": self.provenance.to_string(),
            "source": self.source,
            "timestamp": self.timestamp,
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ProvenanceEvent:
        """Deserialize from a dictionary (e.g., loaded from YAML).

        Args:
            data: Dictionary with provenance, source, timestamp, reason keys.

        Returns:
            A ProvenanceEvent instance.
        """
        return cls(
            provenance=GovernanceProvenance.from_string(data["provenance"]),
            source=data["source"],
            timestamp=data["timestamp"],
            reason=data["reason"],
        )



class StateProvenanceTagger:
    """Tags governance state with provenance indicators.

    Tracks the current provenance of the governance system and provides
    tagging logic that determines provenance based on source characteristics.

    The tagger maintains internal state so that downstream consumers
    (GateResult, health reports, governance summaries) can query the
    current provenance at any time.

    Usage:
        tagger = StateProvenanceTagger()
        provenance = tagger.tag(
            source="config.yaml",
            is_validated=True,
            is_cached=False,
            is_cold_start=False,
        )
        # Later...
        current = tagger.get_current_provenance()
    """

    def __init__(self) -> None:
        """Initialize the tagger with INDETERMINATE provenance."""
        self._current_provenance: GovernanceProvenance = (
            GovernanceProvenance.INDETERMINATE
        )
        self._history: list[ProvenanceEvent] = []
        self._cache_timestamp: str | None = None
        self._degraded_components: list[str] = []

    def tag(
        self,
        source: str,
        is_validated: bool,
        is_cached: bool,
        is_cold_start: bool,
    ) -> GovernanceProvenance:
        """Determine and assign the governance state provenance.

        Applies the following priority-ordered logic:
        1. If cold_start → bootstrap_derived
        2. If cached and not validated → cached
        3. If validated and not cached and not cold_start → authoritative
        4. If source indicates fallback → fallback_derived
        5. If partially degraded conditions → partially_degraded
        6. Otherwise → indeterminate

        Args:
            source: Identifier of the data source (e.g., "config.yaml",
                "fallback_registry", "cache").
            is_validated: Whether the loaded state has been validated against
                its schema or integrity checks.
            is_cached: Whether the state was loaded from a cache rather than
                the canonical source.
            is_cold_start: Whether the system is in cold-start mode (no prior
                history, ledger, or baseline exists).

        Returns:
            The determined GovernanceProvenance tag.
        """
        provenance = self._determine_provenance(
            source=source,
            is_validated=is_validated,
            is_cached=is_cached,
            is_cold_start=is_cold_start,
        )

        reason = self._build_reason(
            provenance=provenance,
            source=source,
            is_validated=is_validated,
            is_cached=is_cached,
            is_cold_start=is_cold_start,
        )

        # Track cache timestamp when provenance is cached (Req 41.3)
        if provenance == GovernanceProvenance.CACHED:
            self._cache_timestamp = datetime.now(timezone.utc).isoformat()

        # Record the event
        event = ProvenanceEvent(
            provenance=provenance,
            source=source,
            timestamp=datetime.now(timezone.utc).isoformat(),
            reason=reason,
        )
        self._history.append(event)

        # Update current provenance
        self._current_provenance = provenance
        return provenance

    def get_current_provenance(self) -> GovernanceProvenance:
        """Return the current governance state provenance.

        Returns:
            The most recently assigned GovernanceProvenance tag, or
            INDETERMINATE if no tagging has occurred.
        """
        return self._current_provenance

    def get_cache_timestamp(self) -> str | None:
        """Return the timestamp when cached provenance was last assigned.

        Per Requirement 41.3, cached provenance includes the cache timestamp.

        Returns:
            ISO 8601 timestamp string, or None if provenance has never been
            tagged as cached.
        """
        return self._cache_timestamp

    def get_history(self) -> list[ProvenanceEvent]:
        """Return the full history of provenance tagging events.

        Returns:
            List of ProvenanceEvent instances in chronological order.
        """
        return list(self._history)

    def mark_component_degraded(self, component_name: str) -> None:
        """Mark a component as degraded for partially_degraded detection.

        When some components are authoritative but others are unavailable,
        the overall provenance becomes partially_degraded.

        Args:
            component_name: Name of the degraded component.
        """
        if component_name not in self._degraded_components:
            self._degraded_components.append(component_name)

    def clear_degraded_components(self) -> None:
        """Clear all degraded component markers.

        Call this when all components have recovered.
        """
        self._degraded_components.clear()

    def has_degraded_components(self) -> bool:
        """Check whether any components are currently marked as degraded.

        Returns:
            True if at least one component is marked degraded.
        """
        return len(self._degraded_components) > 0

    def to_dict(self) -> dict:
        """Serialize the tagger state for YAML persistence.

        Returns:
            Dictionary representation of the tagger's current state.
        """
        return {
            "current_provenance": self._current_provenance.to_string(),
            "cache_timestamp": self._cache_timestamp,
            "degraded_components": list(self._degraded_components),
            "history": [event.to_dict() for event in self._history],
        }

    @classmethod
    def from_dict(cls, data: dict) -> StateProvenanceTagger:
        """Deserialize tagger state from a dictionary (e.g., loaded from YAML).

        Args:
            data: Dictionary with current_provenance, cache_timestamp,
                degraded_components, and history keys.

        Returns:
            A StateProvenanceTagger instance with restored state.
        """
        tagger = cls()
        tagger._current_provenance = GovernanceProvenance.from_string(
            data["current_provenance"]
        )
        tagger._cache_timestamp = data.get("cache_timestamp")
        tagger._degraded_components = list(
            data.get("degraded_components", [])
        )
        tagger._history = [
            ProvenanceEvent.from_dict(event)
            for event in data.get("history", [])
        ]
        return tagger

    def _determine_provenance(
        self,
        source: str,
        is_validated: bool,
        is_cached: bool,
        is_cold_start: bool,
    ) -> GovernanceProvenance:
        """Apply priority-ordered tagging logic.

        Priority order:
        1. cold_start → bootstrap_derived
        2. cached and not validated → cached
        3. validated and not cached and not cold_start → authoritative
        4. source indicates fallback → fallback_derived
        5. degraded components present → partially_degraded
        6. otherwise → indeterminate
        """
        # Priority 1: Cold-start overrides everything
        if is_cold_start:
            return GovernanceProvenance.BOOTSTRAP_DERIVED

        # Priority 2: Cached but not validated
        if is_cached and not is_validated:
            return GovernanceProvenance.CACHED

        # Priority 3: Validated from canonical source
        if is_validated and not is_cached and not is_cold_start:
            return GovernanceProvenance.AUTHORITATIVE

        # Priority 4: Source indicates fallback
        if source.lower() in FALLBACK_SOURCES or "fallback" in source.lower():
            return GovernanceProvenance.FALLBACK_DERIVED

        # Priority 5: Partially degraded (some components unavailable)
        if self.has_degraded_components():
            return GovernanceProvenance.PARTIALLY_DEGRADED

        # Priority 6: Cannot determine provenance
        return GovernanceProvenance.INDETERMINATE

    def _build_reason(
        self,
        provenance: GovernanceProvenance,
        source: str,
        is_validated: bool,
        is_cached: bool,
        is_cold_start: bool,
    ) -> str:
        """Build a human-readable reason for the provenance assignment."""
        match provenance:
            case GovernanceProvenance.AUTHORITATIVE:
                return (
                    f"Loaded from canonical source '{source}' and validated"
                )
            case GovernanceProvenance.CACHED:
                return (
                    f"Loaded from cache (source: '{source}'), "
                    f"not yet validated"
                )
            case GovernanceProvenance.FALLBACK_DERIVED:
                return (
                    f"Computed from fallback logic (source: '{source}')"
                )
            case GovernanceProvenance.BOOTSTRAP_DERIVED:
                return (
                    f"Generated during cold-start initialization "
                    f"(source: '{source}')"
                )
            case GovernanceProvenance.PARTIALLY_DEGRADED:
                degraded = ", ".join(self._degraded_components)
                return (
                    f"Some components unavailable: [{degraded}] "
                    f"(source: '{source}')"
                )
            case GovernanceProvenance.INDETERMINATE:
                return (
                    f"Provenance cannot be determined for source '{source}' "
                    f"(validated={is_validated}, cached={is_cached}, "
                    f"cold_start={is_cold_start})"
                )
