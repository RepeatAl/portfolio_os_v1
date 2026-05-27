"""Chain Validator — pre-normalized graph-based provenance verification.

Verifies provenance chain integrity for each report section at runtime.
Operates on pre-normalized identifier graphs (Hardening 4) with O(1) lookups,
preventing recursive deep graph walking during section validation.

Reads provenance from the canonical sidecar file (<run_id>_provenance.yaml),
NOT from markdown parsing.

Operates in OBSERVABILITY MODE: warnings only, never blocks report generation.

Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 20.1, 20.2, 20.3, 20.4, 20.5
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


# --- Governance Violation Structure ---

VALID_BROKEN_LAYERS = frozenset({"SIGNALS", "SEMANTICS", "REASONING"})

VALID_COMPLETENESS_STATES = frozenset({
    "complete", "partial", "degraded", "unavailable", "invalid",
})


def make_governance_violation(
    section_name: str,
    broken_layer: str,
    last_valid_id: str,
    remediation: str,
) -> dict[str, str]:
    """Create a structured governance violation dict.

    Args:
        section_name: Name of the report section with the broken chain.
        broken_layer: Layer where the chain breaks (SIGNALS, SEMANTICS, REASONING).
        last_valid_id: Last valid identifier before the break.
        remediation: Suggested remediation action.

    Returns:
        Governance violation dict with severity "warning" (observability mode).
    """
    return {
        "section_name": section_name,
        "broken_layer": broken_layer,
        "last_valid_id": last_valid_id,
        "remediation": remediation,
        "severity": "warning",
    }


# --- Data Classes ---

@dataclass(frozen=True)
class ProvenanceBlock:
    """Provenance metadata for a single report section.

    Represents the chain of identifiers that produced a section's content.
    Used by the ChainValidator to verify chain completeness.
    """

    section_name: str
    reasoning_object_ids: list[str]
    semantic_state_ids: list[str]
    signal_engine_ids: list[str]
    completeness_state: str
    unavailability_reasons: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate completeness_state is a known value."""
        if self.completeness_state not in VALID_COMPLETENESS_STATES:
            raise ValueError(
                f"Invalid completeness_state '{self.completeness_state}'. "
                f"Must be one of: {sorted(VALID_COMPLETENESS_STATES)}"
            )


@dataclass(frozen=True)
class IdentifierGraph:
    """Pre-normalized, immutable identifier graph built once per pipeline run.

    Enables O(1) lookups and prevents recursive traversal during validation.
    All maps are built at construction time and never mutated.
    """

    reasoning_to_semantics: dict[str, list[str]]
    semantics_to_signals: dict[str, list[str]]
    all_reasoning_ids: frozenset[str]
    all_semantic_ids: frozenset[str]
    all_signal_engine_ids: frozenset[str]


# --- Chain Validator ---

class ChainValidator:
    """Verify provenance chain integrity for each report section.

    Design (Hardening 4): Chain validation operates on pre-normalized
    identifier graphs, not on repeated nested object traversal. Immutable
    runtime identifier maps and precomputed dependency edges prevent
    recursive deep graph walking during section validation.

    Usage:
        validator = ChainValidator()
        validator.build_graph(reasoning_objects, semantic_states)
        result = validator.validate_all(provenance_blocks)
    """

    # Performance budget: 2 seconds for all 9 sections
    VALIDATION_BUDGET_SECONDS: float = 2.0

    def __init__(self) -> None:
        """Initialize the chain validator with no graph (must call build_graph first)."""
        self._graph: IdentifierGraph | None = None

    @property
    def graph(self) -> IdentifierGraph | None:
        """Access the current identifier graph (None if not yet built)."""
        return self._graph

    def build_graph(
        self,
        reasoning_objects: list[Any],
        semantic_states: list[dict[str, Any]],
    ) -> None:
        """Build immutable identifier graph with precomputed dependency edges.

        Called once per pipeline run before validation begins.
        All subsequent lookups are O(1) dict access.

        Args:
            reasoning_objects: List of ReasoningObject instances (or dicts with
                reasoning_id and source_semantic_states fields).
            semantic_states: List of semantic state dicts, each containing
                'signal_id' and 'signal_origin' fields.
        """
        reasoning_to_semantics: dict[str, list[str]] = {}
        all_reasoning_ids: set[str] = set()

        for obj in reasoning_objects:
            # Support both dataclass instances and dicts
            if isinstance(obj, dict):
                r_id = obj.get("reasoning_id", "")
                source_states = obj.get("source_semantic_states", [])
            else:
                r_id = getattr(obj, "reasoning_id", "")
                source_states = getattr(obj, "source_semantic_states", [])

            if r_id:
                all_reasoning_ids.add(r_id)
                reasoning_to_semantics[r_id] = list(source_states)

        # Build semantics → signals mapping from semantic states
        semantics_to_signals: dict[str, list[str]] = {}
        all_semantic_ids: set[str] = set()
        all_signal_engine_ids: set[str] = set()

        for state in semantic_states:
            signal_id = state.get("signal_id", "")
            signal_origin = state.get("signal_origin", "")

            if signal_id:
                all_semantic_ids.add(signal_id)
                # signal_origin can be a single engine or a list
                if isinstance(signal_origin, list):
                    engines = signal_origin
                elif isinstance(signal_origin, str) and signal_origin:
                    engines = [signal_origin]
                else:
                    engines = []

                semantics_to_signals[signal_id] = engines
                all_signal_engine_ids.update(engines)

        self._graph = IdentifierGraph(
            reasoning_to_semantics=reasoning_to_semantics,
            semantics_to_signals=semantics_to_signals,
            all_reasoning_ids=frozenset(all_reasoning_ids),
            all_semantic_ids=frozenset(all_semantic_ids),
            all_signal_engine_ids=frozenset(all_signal_engine_ids),
        )

        logger.info(
            "IdentifierGraph built: %d reasoning, %d semantic, %d signal_engine IDs",
            len(all_reasoning_ids),
            len(all_semantic_ids),
            len(all_signal_engine_ids),
        )

    def validate_section(self, provenance: ProvenanceBlock) -> list[dict[str, str]]:
        """Verify chain completeness for a single section using pre-built graph.

        No recursive traversal — only dict lookups against the immutable graph.

        Validation logic:
        1. Check that reasoning_object_ids are non-empty (or section is marked unavailable)
        2. For each reasoning_object_id, verify it exists in the identifier graph
        3. For each reasoning_object_id, verify its source_semantic_states are in the graph
        4. For each semantic_state_id, verify it traces to at least one signal_engine_id
        5. If any link is broken, log a governance violation

        Args:
            provenance: ProvenanceBlock for the section to validate.

        Returns:
            List of governance violations (empty = valid chain).
        """
        if self._graph is None:
            return [make_governance_violation(
                section_name=provenance.section_name,
                broken_layer="REASONING",
                last_valid_id="(none)",
                remediation="Call build_graph() before validation.",
            )]

        violations: list[dict[str, str]] = []

        # Step 1: Check reasoning_object_ids are non-empty
        # If section is marked unavailable, empty reasoning IDs are expected
        if provenance.completeness_state == "unavailable":
            # Unavailable sections are allowed to have empty chains
            return violations

        if not provenance.reasoning_object_ids:
            violations.append(make_governance_violation(
                section_name=provenance.section_name,
                broken_layer="REASONING",
                last_valid_id="(none)",
                remediation=(
                    f"Section '{provenance.section_name}' has no Reasoning Object IDs. "
                    "A Reasoning Engine must produce at least one object for this section."
                ),
            ))
            return violations

        # Step 2: For each reasoning_object_id, verify it exists in the graph
        for r_id in provenance.reasoning_object_ids:
            if r_id not in self._graph.all_reasoning_ids:
                violations.append(make_governance_violation(
                    section_name=provenance.section_name,
                    broken_layer="REASONING",
                    last_valid_id=r_id,
                    remediation=(
                        f"Reasoning Object '{r_id}' not found in identifier graph. "
                        "Verify the producing Reasoning Engine registered this object."
                    ),
                ))
                continue

            # Step 3: Verify source_semantic_states for this reasoning object
            source_semantics = self._graph.reasoning_to_semantics.get(r_id, [])
            if not source_semantics:
                violations.append(make_governance_violation(
                    section_name=provenance.section_name,
                    broken_layer="SEMANTICS",
                    last_valid_id=r_id,
                    remediation=(
                        f"Reasoning Object '{r_id}' has no source_semantic_states. "
                        "The Reasoning Engine must reference at least one Semantic State."
                    ),
                ))
                continue

            # Step 4: For each semantic_state_id, verify it traces to signal engines
            for sem_id in source_semantics:
                if sem_id not in self._graph.all_semantic_ids:
                    violations.append(make_governance_violation(
                        section_name=provenance.section_name,
                        broken_layer="SEMANTICS",
                        last_valid_id=sem_id,
                        remediation=(
                            f"Semantic State '{sem_id}' referenced by Reasoning Object "
                            f"'{r_id}' not found in identifier graph. "
                            "The Semantic Engine must produce this state."
                        ),
                    ))
                    continue

                signal_engines = self._graph.semantics_to_signals.get(sem_id, [])
                if not signal_engines:
                    violations.append(make_governance_violation(
                        section_name=provenance.section_name,
                        broken_layer="SIGNALS",
                        last_valid_id=sem_id,
                        remediation=(
                            f"Semantic State '{sem_id}' has no signal_origin. "
                            "A Signal Engine must produce the raw signal for this state."
                        ),
                    ))

        if violations:
            logger.warning(
                "Chain validation found %d violation(s) in section '%s'",
                len(violations),
                provenance.section_name,
            )

        return violations

    def validate_all(
        self, provenance_blocks: list[ProvenanceBlock]
    ) -> dict[str, Any]:
        """Validate all sections. Must complete within 2 seconds total.

        Reads from canonical provenance sidecar file, NOT from markdown parsing.

        Args:
            provenance_blocks: List of ProvenanceBlock instances for all sections.

        Returns:
            Validation result dict with:
                - section_results: dict mapping section_name → list of violations
                - overall_state: "valid" | "degraded" | "invalid"
                - total_violations: int
                - execution_time_ms: float
                - budget_exceeded: bool
        """
        start_time = time.time()

        section_results: dict[str, list[dict[str, str]]] = {}
        total_violations = 0

        for block in provenance_blocks:
            elapsed = time.time() - start_time
            if elapsed >= self.VALIDATION_BUDGET_SECONDS:
                # Budget exceeded — mark remaining sections as unvalidated
                logger.warning(
                    "Validation budget (%.1fs) exceeded after %d sections. "
                    "Remaining sections not validated.",
                    self.VALIDATION_BUDGET_SECONDS,
                    len(section_results),
                )
                section_results[block.section_name] = [make_governance_violation(
                    section_name=block.section_name,
                    broken_layer="REASONING",
                    last_valid_id="(budget_exceeded)",
                    remediation="Validation budget exceeded. Increase budget or reduce graph size.",
                )]
                total_violations += 1
                continue

            violations = self.validate_section(block)
            section_results[block.section_name] = violations
            total_violations += len(violations)

        execution_time_ms = (time.time() - start_time) * 1000
        budget_exceeded = execution_time_ms > (self.VALIDATION_BUDGET_SECONDS * 1000)

        # Determine overall state
        if total_violations == 0:
            overall_state = "valid"
        elif total_violations <= 3:
            overall_state = "degraded"
        else:
            overall_state = "invalid"

        result = {
            "section_results": section_results,
            "overall_state": overall_state,
            "total_violations": total_violations,
            "execution_time_ms": round(execution_time_ms, 2),
            "budget_exceeded": budget_exceeded,
        }

        logger.info(
            "Chain validation complete: state=%s, violations=%d, time=%.2fms",
            overall_state,
            total_violations,
            execution_time_ms,
        )

        return result

    @classmethod
    def load_provenance_blocks(cls, sidecar_path: str) -> list[ProvenanceBlock]:
        """Load provenance blocks from a canonical sidecar YAML file.

        Reads from the provenance sidecar file (<run_id>_provenance.yaml),
        NOT from markdown parsing.

        Args:
            sidecar_path: Path to the provenance sidecar YAML file.

        Returns:
            List of ProvenanceBlock instances parsed from the sidecar file.

        Raises:
            FileNotFoundError: If the sidecar file does not exist.
            ValueError: If the sidecar file is malformed.
        """
        path = Path(sidecar_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Provenance sidecar file not found: {sidecar_path}"
            )

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "sections" not in data:
            raise ValueError(
                f"Malformed provenance sidecar file: missing 'sections' key in {sidecar_path}"
            )

        blocks: list[ProvenanceBlock] = []
        for section_data in data["sections"]:
            # Map unavailable_layers to unavailability_reasons
            unavailable_layers = section_data.get("unavailable_layers", [])
            unavailability_reasons: list[str] = []
            for layer_info in unavailable_layers:
                if isinstance(layer_info, dict):
                    reason = layer_info.get("reason", "unknown")
                    layer = layer_info.get("layer", "unknown")
                    unavailability_reasons.append(f"{layer}: {reason}")
                elif isinstance(layer_info, str):
                    unavailability_reasons.append(layer_info)

            block = ProvenanceBlock(
                section_name=section_data.get("section_name", ""),
                reasoning_object_ids=section_data.get("reasoning_object_ids", []),
                semantic_state_ids=section_data.get("semantic_state_ids", []),
                signal_engine_ids=section_data.get("signal_engine_ids", []),
                completeness_state=section_data.get("completeness_state", "invalid"),
                unavailability_reasons=unavailability_reasons,
            )
            blocks.append(block)

        return blocks
