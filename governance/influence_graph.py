"""Governance Influence Graph — dependency declarations, cycle detection, directionality enforcement.

Manages governance module dependency declarations loaded from
`.domainization/governance_influence_declarations.yaml`. Performs:
- Cycle detection (DFS-based) on the directed write-dependency graph
- Directionality enforcement: downstream modules MUST NOT write to upstream modules
- Validation at governance initialization (before any enforcement decisions)

All violations emit CRITICAL severity events to the Mutation_Audit_Ledger.

Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3
"""

from __future__ import annotations

import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from governance.mutation_audit_ledger import MutationAuditLedger

logger = logging.getLogger(__name__)


class InfluenceDirection(StrEnum):
    """Direction of governance influence for a module."""

    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"


@dataclass(frozen=True)
class ModuleDependencyDeclaration:
    """Immutable declaration of a governance module's dependencies.

    Attributes:
        module_id: Unique identifier for the governance module.
        read_dependencies: Modules whose output this module consumes.
        write_dependencies: Modules whose state this module modifies.
        influence_direction: Whether this module is upstream or downstream.
    """

    module_id: str
    read_dependencies: tuple[str, ...]
    write_dependencies: tuple[str, ...]
    influence_direction: InfluenceDirection

    def to_dict(self) -> dict:
        """Serialize to a YAML-compatible dictionary."""
        return {
            "module_id": self.module_id,
            "read_dependencies": list(self.read_dependencies),
            "write_dependencies": list(self.write_dependencies),
            "influence_direction": str(self.influence_direction),
        }

    @classmethod
    def from_dict(cls, data: dict) -> ModuleDependencyDeclaration:
        """Deserialize from a dictionary (e.g., loaded from YAML).

        Args:
            data: Dictionary with keys matching declaration fields.

        Returns:
            A ModuleDependencyDeclaration instance.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If influence_direction is invalid.
        """
        return cls(
            module_id=data["module_id"],
            read_dependencies=tuple(data.get("read_dependencies", [])),
            write_dependencies=tuple(data.get("write_dependencies", [])),
            influence_direction=InfluenceDirection(data["influence_direction"]),
        )


@dataclass
class CycleDetectionResult:
    """Result of cycle detection on the governance influence graph.

    Attributes:
        has_cycle: True if a cycle was detected.
        cycle_path: The cycle path (e.g., ["A", "B", "C", "A"]). Empty if no cycle.
    """

    has_cycle: bool
    cycle_path: list[str] = field(default_factory=list)


@dataclass
class DirectionalityViolation:
    """A detected directionality violation in the influence graph.

    Attributes:
        violating_module: The module that violates directionality.
        target_module: The upstream module being written to.
        violator_direction: The declared direction of the violating module.
        target_direction: The declared direction of the target module.
        reason: Human-readable explanation of the violation.
    """

    violating_module: str
    target_module: str
    violator_direction: InfluenceDirection
    target_direction: InfluenceDirection
    reason: str



class GovernanceInfluenceGraph:
    """Directed graph of governance module dependencies.

    Loaded from .domainization/governance_influence_declarations.yaml.
    Performs cycle detection and directionality enforcement at init time.

    Args:
        declarations_path: Path to the governance_influence_declarations.yaml file.
        ledger: Optional MutationAuditLedger for emitting CRITICAL events.
    """

    def __init__(
        self,
        declarations_path: str,
        ledger: MutationAuditLedger | None = None,
    ) -> None:
        self._declarations_path = declarations_path
        self._ledger = ledger
        self._declarations: list[ModuleDependencyDeclaration] = []
        self._graph: dict[str, list[str]] = {}

    def load_declarations(self) -> list[ModuleDependencyDeclaration]:
        """Load module dependency declarations from the YAML file.

        Returns:
            List of ModuleDependencyDeclaration objects.

        Raises:
            FileNotFoundError: If the declarations file does not exist.
            ValueError: If the YAML structure is invalid.
        """
        if not os.path.isfile(self._declarations_path):
            self._emit_critical(
                "missing_declarations_file",
                {
                    "path": self._declarations_path,
                    "reason": "Governance influence declarations file not found",
                },
            )
            raise FileNotFoundError(
                f"Governance influence declarations file not found: "
                f"{self._declarations_path}"
            )

        with open(self._declarations_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "modules" not in data:
            raise ValueError(
                "Invalid governance_influence_declarations.yaml: "
                "missing 'modules' key"
            )

        declarations: list[ModuleDependencyDeclaration] = []
        for module_data in data["modules"]:
            try:
                decl = ModuleDependencyDeclaration.from_dict(module_data)
                declarations.append(decl)
            except (KeyError, ValueError) as exc:
                logger.warning(
                    "Skipping invalid module declaration: %s — %s",
                    module_data.get("module_id", "unknown"),
                    exc,
                )

        self._declarations = declarations
        return declarations

    def validate_declaration(self, decl: ModuleDependencyDeclaration) -> bool:
        """Validate that a module dependency declaration has all required fields.

        Args:
            decl: The declaration to validate.

        Returns:
            True if the declaration is valid, False otherwise.
        """
        if not decl.module_id or not decl.module_id.strip():
            return False
        if decl.influence_direction not in (
            InfluenceDirection.UPSTREAM,
            InfluenceDirection.DOWNSTREAM,
        ):
            return False
        return True

    def build_graph(self) -> dict[str, list[str]]:
        """Build adjacency list from write_dependencies.

        Each module has edges pointing to the modules it writes to.
        This represents the influence direction: module -> writes_to_module.

        Returns:
            Adjacency list dict mapping module_id to list of target module_ids.
        """
        graph: dict[str, list[str]] = {}

        # Initialize all declared modules as nodes
        for decl in self._declarations:
            if decl.module_id not in graph:
                graph[decl.module_id] = []

        # Add edges from write_dependencies
        for decl in self._declarations:
            for write_dep in decl.write_dependencies:
                graph[decl.module_id].append(write_dep)
                # Ensure target node exists in graph
                if write_dep not in graph:
                    graph[write_dep] = []

        self._graph = graph
        return graph

    def detect_cycles(self) -> CycleDetectionResult:
        """DFS-based cycle detection on the directed write-dependency graph.

        Detects both direct cycles (A->B->A) and transitive cycles (A->B->C->A).

        Returns:
            CycleDetectionResult with has_cycle=True and cycle_path if a cycle
            is found, otherwise has_cycle=False with empty cycle_path.
        """
        graph = self._graph
        if not graph:
            return CycleDetectionResult(has_cycle=False)

        # DFS states: 0=unvisited, 1=in current path (gray), 2=fully processed (black)
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = {node: WHITE for node in graph}
        parent: dict[str, str | None] = {node: None for node in graph}

        def dfs(node: str, path: list[str]) -> list[str] | None:
            """Returns cycle path if found, None otherwise."""
            color[node] = GRAY
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in color:
                    # Node not in graph (external dependency), skip
                    continue
                if color[neighbor] == GRAY:
                    # Found a cycle — extract the cycle path
                    cycle_start_idx = path.index(neighbor)
                    cycle_path = path[cycle_start_idx:] + [neighbor]
                    return cycle_path
                if color[neighbor] == WHITE:
                    result = dfs(neighbor, path)
                    if result is not None:
                        return result

            path.pop()
            color[node] = BLACK
            return None

        for node in graph:
            if color[node] == WHITE:
                cycle = dfs(node, [])
                if cycle is not None:
                    result = CycleDetectionResult(has_cycle=True, cycle_path=cycle)
                    self._emit_critical(
                        "cycle_detected",
                        {
                            "cycle_path": cycle,
                            "reason": (
                                f"Circular governance influence detected: "
                                f"{' -> '.join(cycle)}"
                            ),
                        },
                    )
                    return result

        return CycleDetectionResult(has_cycle=False)

    def enforce_directionality(self) -> list[DirectionalityViolation]:
        """Check that no downstream module writes to an upstream module.

        A module declared as 'downstream' MUST NOT have write_dependencies
        that target a module declared as 'upstream'. This would mean a
        downstream observer is writing to an upstream enforcer — a violation.

        Returns:
            List of DirectionalityViolation objects. Empty if no violations.
        """
        # Build a direction lookup from declarations
        direction_map: dict[str, InfluenceDirection] = {
            decl.module_id: decl.influence_direction
            for decl in self._declarations
        }

        violations: list[DirectionalityViolation] = []

        for decl in self._declarations:
            if decl.influence_direction != InfluenceDirection.DOWNSTREAM:
                continue

            # Check each write_dependency of this downstream module
            for write_target in decl.write_dependencies:
                target_direction = direction_map.get(write_target)
                if target_direction is None:
                    # Target module has no declaration — emit CRITICAL for missing
                    self._emit_critical(
                        "missing_declaration",
                        {
                            "module_id": write_target,
                            "referenced_by": decl.module_id,
                            "reason": (
                                f"Module '{write_target}' referenced in "
                                f"write_dependencies of '{decl.module_id}' "
                                f"but has no dependency declaration"
                            ),
                        },
                    )
                    continue

                if target_direction == InfluenceDirection.UPSTREAM:
                    violation = DirectionalityViolation(
                        violating_module=decl.module_id,
                        target_module=write_target,
                        violator_direction=decl.influence_direction,
                        target_direction=target_direction,
                        reason=(
                            f"Downstream module '{decl.module_id}' writes to "
                            f"upstream module '{write_target}' — "
                            f"downstream observers must not modify upstream enforcers"
                        ),
                    )
                    violations.append(violation)
                    self._emit_critical(
                        "directionality_violation",
                        {
                            "violating_module": decl.module_id,
                            "target_module": write_target,
                            "violator_direction": str(decl.influence_direction),
                            "target_direction": str(target_direction),
                            "reason": violation.reason,
                        },
                    )

        return violations

    def validate_at_init(self) -> tuple[bool, list[str]]:
        """Run full validation: load, build graph, detect cycles, enforce directionality.

        Called once at governance initialization before any enforcement decisions.

        Returns:
            Tuple of (is_valid, list_of_error_messages).
            is_valid is False if any cycles or directionality violations are found.
        """
        errors: list[str] = []

        # Step 1: Load declarations
        try:
            declarations = self.load_declarations()
        except (FileNotFoundError, ValueError) as exc:
            errors.append(str(exc))
            return False, errors

        if not declarations:
            errors.append("No valid module declarations found")
            return False, errors

        # Step 2: Validate each declaration
        for decl in declarations:
            if not self.validate_declaration(decl):
                msg = f"Invalid declaration for module '{decl.module_id}'"
                errors.append(msg)
                self._emit_critical(
                    "invalid_declaration",
                    {"module_id": decl.module_id, "reason": msg},
                )

        # Step 3: Build the directed graph
        self.build_graph()

        # Step 4: Detect cycles
        cycle_result = self.detect_cycles()
        if cycle_result.has_cycle:
            cycle_str = " -> ".join(cycle_result.cycle_path)
            errors.append(f"Cycle detected: {cycle_str}")

        # Step 5: Enforce directionality
        violations = self.enforce_directionality()
        for violation in violations:
            errors.append(violation.reason)

        is_valid = len(errors) == 0
        if is_valid:
            logger.info(
                "Governance influence graph validated successfully: "
                "%d modules, no cycles, no directionality violations",
                len(declarations),
            )
        else:
            logger.critical(
                "Governance influence graph validation FAILED: %d errors",
                len(errors),
            )

        return is_valid, errors

    def _emit_critical(self, event_subtype: str, details: dict) -> None:
        """Emit a CRITICAL severity event to the Mutation_Audit_Ledger.

        Args:
            event_subtype: Sub-type of the governance event (e.g., 'cycle_detected').
            details: Event-specific structured details.
        """
        if self._ledger is None:
            logger.critical(
                "GOVERNANCE CRITICAL [%s]: %s",
                event_subtype,
                details.get("reason", str(details)),
            )
            return

        from governance.mutation_audit_ledger import LedgerEntry

        entry = LedgerEntry(
            entry_id=str(uuid.uuid4()),
            event_type="GOVERNANCE_EVENT",
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor={
                "actor_type": "SYSTEM",
                "actor_id": "influence_graph",
                "context": {"action": event_subtype},
                "is_fallback": False,
            },
            governance_policy_version="unknown",
            severity="CRITICAL",
            details=details,
        )
        self._ledger.append(entry)
        logger.critical(
            "GOVERNANCE CRITICAL [%s]: %s",
            event_subtype,
            details.get("reason", str(details)),
        )
