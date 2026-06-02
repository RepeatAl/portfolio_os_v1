"""Property-based tests for Governance Influence Graph.

**Property 1: Dependency Declaration Round-Trip**
**Property 2: Cycle Detection Completeness**
**Property 3: Directionality Enforcement**

**Validates: Requirements 1.4, 1.5, 2.1, 2.2, 2.3, 2.5, 3.1, 3.2, 3.4**

Tests that:
1. For any valid ModuleDependencyDeclaration, serializing to dict and deserializing
   back produces an equivalent object (round-trip property).
2. For any directed graph, cycle detection correctly identifies cyclic graphs
   (reports has_cycle=True with valid cycle_path) and acyclic graphs (reports
   has_cycle=False). Violations emit critical audit records.
3. For any set of module declarations with direction assignments, downstream modules
   with write_dependencies on upstream modules produce directionality violations,
   and configurations without such violations produce no violations. Malformed
   declarations fail validation.
"""

from __future__ import annotations

import os
import tempfile
import uuid
from datetime import datetime, timezone

import yaml
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from governance.influence_graph import (
    CycleDetectionResult,
    DirectionalityViolation,
    GovernanceInfluenceGraph,
    InfluenceDirection,
    ModuleDependencyDeclaration,
)
from governance.mutation_audit_ledger import MutationAuditLedger


# ---------------------------------------------------------------------------
# Shared Strategies
# ---------------------------------------------------------------------------

# Module IDs: non-empty alphanumeric + underscore strings (realistic identifiers)
module_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_"),
    min_size=1,
    max_size=40,
).filter(lambda s: s.strip() != "")

# Influence direction
direction_strategy = st.sampled_from([InfluenceDirection.UPSTREAM, InfluenceDirection.DOWNSTREAM])

# Dependency lists (tuples of module IDs)
dependency_list_strategy = st.lists(
    module_id_strategy,
    min_size=0,
    max_size=5,
).map(tuple)


# ---------------------------------------------------------------------------
# Property 1: Dependency Declaration Round-Trip
# ---------------------------------------------------------------------------


class TestDependencyDeclarationRoundTrip:
    """Property 1: Dependency Declaration Round-Trip.

    **Validates: Requirements 1.4, 1.5**

    For any valid ModuleDependencyDeclaration object (with arbitrary module_id,
    arbitrary tuples of read/write dependency strings, and any valid
    InfluenceDirection), serializing to a YAML-compatible dict and deserializing
    back SHALL produce an object equal to the original.
    """

    @given(
        module_id=module_id_strategy,
        read_deps=dependency_list_strategy,
        write_deps=dependency_list_strategy,
        direction=direction_strategy,
    )
    @settings(max_examples=200)
    def test_roundtrip_serialization(
        self,
        module_id: str,
        read_deps: tuple[str, ...],
        write_deps: tuple[str, ...],
        direction: InfluenceDirection,
    ) -> None:
        """For any valid ModuleDependencyDeclaration, to_dict() then from_dict()
        produces an equivalent object.

        **Validates: Requirements 1.4, 1.5**
        """
        original = ModuleDependencyDeclaration(
            module_id=module_id,
            read_dependencies=read_deps,
            write_dependencies=write_deps,
            influence_direction=direction,
        )

        serialized = original.to_dict()
        deserialized = ModuleDependencyDeclaration.from_dict(serialized)

        assert deserialized.module_id == original.module_id
        assert deserialized.read_dependencies == original.read_dependencies
        assert deserialized.write_dependencies == original.write_dependencies
        assert deserialized.influence_direction == original.influence_direction
        assert deserialized == original


# ---------------------------------------------------------------------------
# Property 2: Cycle Detection Completeness
# ---------------------------------------------------------------------------

# Strategy to generate a random DAG (acyclic graph)
# We generate nodes with a topological ordering and only allow edges from
# lower-index to higher-index nodes, guaranteeing acyclicity.
@st.composite
def dag_strategy(draw):
    """Generate a random directed acyclic graph as a list of ModuleDependencyDeclarations.

    Nodes are assigned indices; edges only go from lower to higher index,
    guaranteeing no cycles exist.
    """
    num_nodes = draw(st.integers(min_value=2, max_value=8))
    node_names = [f"mod_{i}" for i in range(num_nodes)]

    declarations = []
    for i, node in enumerate(node_names):
        # Write deps can only point to nodes with HIGHER index (forward edges only)
        possible_targets = node_names[i + 1:]
        if possible_targets:
            write_deps = draw(
                st.lists(
                    st.sampled_from(possible_targets),
                    min_size=0,
                    max_size=min(3, len(possible_targets)),
                    unique=True,
                )
            )
        else:
            write_deps = []

        decl = ModuleDependencyDeclaration(
            module_id=node,
            read_dependencies=(),
            write_dependencies=tuple(write_deps),
            influence_direction=InfluenceDirection.DOWNSTREAM,
        )
        declarations.append(decl)

    return declarations


@st.composite
def cyclic_graph_strategy(draw):
    """Generate a graph with at least one injected back-edge creating a cycle.

    Starts with a DAG, then adds a back-edge from a higher-index node to a
    lower-index node, guaranteeing a cycle exists.
    """
    num_nodes = draw(st.integers(min_value=2, max_value=8))
    node_names = [f"mod_{i}" for i in range(num_nodes)]

    # Build base DAG declarations
    declarations = []
    for i, node in enumerate(node_names):
        possible_targets = node_names[i + 1:]
        if possible_targets:
            write_deps = draw(
                st.lists(
                    st.sampled_from(possible_targets),
                    min_size=0,
                    max_size=min(2, len(possible_targets)),
                    unique=True,
                )
            )
        else:
            write_deps = []

        declarations.append({
            "module_id": node,
            "write_deps": write_deps,
        })

    # Inject a back-edge: pick a node with index > 0 and add an edge to a
    # node with a lower index. This creates a cycle.
    back_edge_source_idx = draw(st.integers(min_value=1, max_value=num_nodes - 1))
    back_edge_target_idx = draw(st.integers(min_value=0, max_value=back_edge_source_idx - 1))

    # Ensure there's a forward path from target to source (to complete the cycle)
    # We add edges along the path target -> target+1 -> ... -> source
    for idx in range(back_edge_target_idx, back_edge_source_idx):
        target_node = node_names[idx + 1]
        if target_node not in declarations[idx]["write_deps"]:
            declarations[idx]["write_deps"].append(target_node)

    # Add the back-edge
    back_target = node_names[back_edge_target_idx]
    if back_target not in declarations[back_edge_source_idx]["write_deps"]:
        declarations[back_edge_source_idx]["write_deps"].append(back_target)

    # Convert to ModuleDependencyDeclaration objects
    result = []
    for decl_data in declarations:
        decl = ModuleDependencyDeclaration(
            module_id=decl_data["module_id"],
            read_dependencies=(),
            write_dependencies=tuple(decl_data["write_deps"]),
            influence_direction=InfluenceDirection.DOWNSTREAM,
        )
        result.append(decl)

    return result


class TestCycleDetectionCompleteness:
    """Property 2: Cycle Detection Completeness.

    **Validates: Requirements 2.1, 2.2, 2.3, 2.5**

    For any directed graph of governance module dependencies:
    - If the graph is acyclic, cycle detection reports has_cycle=False.
    - If the graph contains a cycle, cycle detection reports has_cycle=True
      and produces a cycle_path that is a valid cycle in the graph.
    - Cycle detection emits critical audit records when cycles are found.
    """

    @given(declarations=dag_strategy())
    @settings(max_examples=200)
    def test_acyclic_graphs_report_no_cycle(
        self, declarations: list[ModuleDependencyDeclaration]
    ) -> None:
        """For any DAG (acyclic graph), cycle detection reports has_cycle=False.

        **Validates: Requirements 2.1, 2.5**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write declarations to a temp YAML file
            yaml_path = os.path.join(tmpdir, "declarations.yaml")
            yaml_data = {
                "schema_version": "1.0.0",
                "modules": [d.to_dict() for d in declarations],
            }
            with open(yaml_path, "w") as f:
                yaml.dump(yaml_data, f)

            graph = GovernanceInfluenceGraph(declarations_path=yaml_path)
            graph.load_declarations()
            graph.build_graph()
            result = graph.detect_cycles()

            assert result.has_cycle is False, (
                f"DAG incorrectly reported as cyclic. "
                f"Declarations: {[d.module_id for d in declarations]}, "
                f"Reported cycle: {result.cycle_path}"
            )

    @given(declarations=cyclic_graph_strategy())
    @settings(max_examples=200)
    def test_cyclic_graphs_report_cycle_with_valid_path(
        self, declarations: list[ModuleDependencyDeclaration]
    ) -> None:
        """For any graph with an injected back-edge, cycle detection reports
        has_cycle=True and produces a valid cycle_path.

        **Validates: Requirements 2.1, 2.2, 2.3, 2.5**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            yaml_path = os.path.join(tmpdir, "declarations.yaml")
            yaml_data = {
                "schema_version": "1.0.0",
                "modules": [d.to_dict() for d in declarations],
            }
            with open(yaml_path, "w") as f:
                yaml.dump(yaml_data, f)

            graph = GovernanceInfluenceGraph(declarations_path=yaml_path)
            graph.load_declarations()
            graph.build_graph()
            result = graph.detect_cycles()

            assert result.has_cycle is True, (
                f"Cyclic graph not detected. "
                f"Declarations: {[(d.module_id, d.write_dependencies) for d in declarations]}"
            )

            # Validate cycle_path is a valid cycle:
            # - Must have at least 2 elements (start and end are the same node)
            # - First element == last element
            # - Each consecutive pair (path[i], path[i+1]) must be an edge in the graph
            assert len(result.cycle_path) >= 2, (
                f"Cycle path too short: {result.cycle_path}"
            )
            assert result.cycle_path[0] == result.cycle_path[-1], (
                f"Cycle path does not form a cycle (first != last): {result.cycle_path}"
            )

            # Verify each edge in the cycle path exists in the graph
            adjacency = graph._graph
            for i in range(len(result.cycle_path) - 1):
                src = result.cycle_path[i]
                dst = result.cycle_path[i + 1]
                assert dst in adjacency.get(src, []), (
                    f"Invalid edge in cycle path: {src} -> {dst}. "
                    f"Adjacency for {src}: {adjacency.get(src, [])}. "
                    f"Full cycle path: {result.cycle_path}"
                )

    @given(declarations=cyclic_graph_strategy())
    @settings(max_examples=200)
    def test_cycle_detection_emits_critical_audit_record(
        self, declarations: list[ModuleDependencyDeclaration]
    ) -> None:
        """When a cycle is detected, a CRITICAL audit record is emitted to the ledger.

        **Validates: Requirements 2.2**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            yaml_path = os.path.join(tmpdir, "declarations.yaml")
            ledger_path = os.path.join(tmpdir, "ledger.yaml")

            yaml_data = {
                "schema_version": "1.0.0",
                "modules": [d.to_dict() for d in declarations],
            }
            with open(yaml_path, "w") as f:
                yaml.dump(yaml_data, f)

            ledger = MutationAuditLedger(ledger_path)
            graph = GovernanceInfluenceGraph(
                declarations_path=yaml_path, ledger=ledger
            )
            graph.load_declarations()
            graph.build_graph()
            result = graph.detect_cycles()

            assert result.has_cycle is True

            # Verify a CRITICAL event was emitted to the ledger
            entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
            critical_entries = [e for e in entries if e.severity == "CRITICAL"]
            cycle_entries = [
                e for e in critical_entries
                if e.details.get("cycle_path") is not None
                or "cycle_detected" in str(e.actor.get("context", {}))
            ]
            assert len(cycle_entries) > 0, (
                f"No CRITICAL audit record emitted for cycle detection. "
                f"Ledger entries: {[e.to_dict() for e in entries]}"
            )


# ---------------------------------------------------------------------------
# Property 3: Directionality Enforcement
# ---------------------------------------------------------------------------

@st.composite
def modules_with_violation_strategy(draw):
    """Generate module declarations where at least one downstream module
    writes to an upstream module (guaranteed violation).
    """
    num_modules = draw(st.integers(min_value=2, max_value=6))
    module_names = [f"mod_{i}" for i in range(num_modules)]

    # Pick at least one upstream and one downstream module
    num_upstream = draw(st.integers(min_value=1, max_value=max(1, num_modules - 1)))
    upstream_modules = module_names[:num_upstream]
    downstream_modules = module_names[num_upstream:]

    # Ensure at least one downstream module exists
    if not downstream_modules:
        downstream_modules = [module_names[-1]]
        upstream_modules = module_names[:-1]

    declarations = []

    # Create upstream modules (no write deps to other upstream)
    for mod in upstream_modules:
        decl = ModuleDependencyDeclaration(
            module_id=mod,
            read_dependencies=(),
            write_dependencies=(),
            influence_direction=InfluenceDirection.UPSTREAM,
        )
        declarations.append(decl)

    # Create downstream modules — at least one writes to an upstream module
    violator_idx = 0  # First downstream module is the violator
    for i, mod in enumerate(downstream_modules):
        if i == violator_idx:
            # This module writes to an upstream module (violation)
            target = draw(st.sampled_from(upstream_modules))
            write_deps = (target,)
        else:
            # Non-violating downstream module
            write_deps = ()

        decl = ModuleDependencyDeclaration(
            module_id=mod,
            read_dependencies=(),
            write_dependencies=write_deps,
            influence_direction=InfluenceDirection.DOWNSTREAM,
        )
        declarations.append(decl)

    return declarations


@st.composite
def modules_without_violation_strategy(draw):
    """Generate module declarations where NO downstream module writes to
    an upstream module (no violations).

    Downstream modules only write to other downstream modules or nothing.
    """
    num_modules = draw(st.integers(min_value=2, max_value=6))
    module_names = [f"mod_{i}" for i in range(num_modules)]

    # Split into upstream and downstream
    num_upstream = draw(st.integers(min_value=1, max_value=max(1, num_modules - 1)))
    upstream_modules = module_names[:num_upstream]
    downstream_modules = module_names[num_upstream:]

    if not downstream_modules:
        downstream_modules = [module_names[-1]]
        upstream_modules = module_names[:-1]

    declarations = []

    # Create upstream modules
    for mod in upstream_modules:
        decl = ModuleDependencyDeclaration(
            module_id=mod,
            read_dependencies=(),
            write_dependencies=(),
            influence_direction=InfluenceDirection.UPSTREAM,
        )
        declarations.append(decl)

    # Create downstream modules — write deps only to OTHER downstream modules
    for mod in downstream_modules:
        other_downstream = [m for m in downstream_modules if m != mod]
        if other_downstream:
            write_deps = draw(
                st.lists(
                    st.sampled_from(other_downstream),
                    min_size=0,
                    max_size=min(2, len(other_downstream)),
                    unique=True,
                )
            )
        else:
            write_deps = []

        decl = ModuleDependencyDeclaration(
            module_id=mod,
            read_dependencies=(),
            write_dependencies=tuple(write_deps),
            influence_direction=InfluenceDirection.DOWNSTREAM,
        )
        declarations.append(decl)

    return declarations


class TestDirectionalityEnforcement:
    """Property 3: Directionality Enforcement.

    **Validates: Requirements 3.1, 3.2, 3.4**

    For any set of governance module declarations with valid influence directions:
    - If a downstream module has a write_dependency on an upstream module,
      directionality enforcement SHALL detect and report a DirectionalityViolation.
    - If no downstream module writes to an upstream module, no violations
      SHALL be reported.
    - Malformed module declarations (empty module_id) fail validation.
    """

    @given(declarations=modules_with_violation_strategy())
    @settings(max_examples=200)
    def test_downstream_writing_upstream_produces_violation(
        self, declarations: list[ModuleDependencyDeclaration]
    ) -> None:
        """When a downstream module writes to an upstream module, a
        DirectionalityViolation is detected.

        **Validates: Requirements 3.1, 3.2**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            yaml_path = os.path.join(tmpdir, "declarations.yaml")
            yaml_data = {
                "schema_version": "1.0.0",
                "modules": [d.to_dict() for d in declarations],
            }
            with open(yaml_path, "w") as f:
                yaml.dump(yaml_data, f)

            graph = GovernanceInfluenceGraph(declarations_path=yaml_path)
            graph.load_declarations()
            graph.build_graph()
            violations = graph.enforce_directionality()

            assert len(violations) > 0, (
                f"Expected directionality violation but none detected. "
                f"Declarations: {[(d.module_id, d.influence_direction, d.write_dependencies) for d in declarations]}"
            )

            # Verify each violation has correct structure
            for v in violations:
                assert v.violator_direction == InfluenceDirection.DOWNSTREAM
                assert v.target_direction == InfluenceDirection.UPSTREAM
                assert v.violating_module != ""
                assert v.target_module != ""
                assert v.reason != ""

    @given(declarations=modules_without_violation_strategy())
    @settings(max_examples=200)
    def test_no_downstream_upstream_writes_produces_no_violations(
        self, declarations: list[ModuleDependencyDeclaration]
    ) -> None:
        """When no downstream module writes to an upstream module, no
        violations are reported.

        **Validates: Requirements 3.1, 3.4**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            yaml_path = os.path.join(tmpdir, "declarations.yaml")
            yaml_data = {
                "schema_version": "1.0.0",
                "modules": [d.to_dict() for d in declarations],
            }
            with open(yaml_path, "w") as f:
                yaml.dump(yaml_data, f)

            graph = GovernanceInfluenceGraph(declarations_path=yaml_path)
            graph.load_declarations()
            graph.build_graph()
            violations = graph.enforce_directionality()

            assert len(violations) == 0, (
                f"Unexpected directionality violations detected: "
                f"{[(v.violating_module, v.target_module) for v in violations]}. "
                f"Declarations: {[(d.module_id, d.influence_direction, d.write_dependencies) for d in declarations]}"
            )

    @given(
        module_id=st.just(""),
        direction=direction_strategy,
    )
    @settings(max_examples=10)
    def test_malformed_declarations_fail_validation(
        self, module_id: str, direction: InfluenceDirection
    ) -> None:
        """Malformed module declarations (empty module_id) fail validation.

        **Validates: Requirements 3.4**
        """
        decl = ModuleDependencyDeclaration(
            module_id=module_id,
            read_dependencies=(),
            write_dependencies=(),
            influence_direction=direction,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            yaml_path = os.path.join(tmpdir, "declarations.yaml")
            yaml_data = {
                "schema_version": "1.0.0",
                "modules": [decl.to_dict()],
            }
            with open(yaml_path, "w") as f:
                yaml.dump(yaml_data, f)

            graph = GovernanceInfluenceGraph(declarations_path=yaml_path)
            graph.load_declarations()

            # Empty module_id should fail validation
            is_valid = graph.validate_declaration(decl)
            assert is_valid is False, (
                f"Expected validation failure for empty module_id, but got valid"
            )

    @given(declarations=modules_with_violation_strategy())
    @settings(max_examples=200, deadline=None)
    def test_directionality_violation_emits_critical_audit(
        self, declarations: list[ModuleDependencyDeclaration]
    ) -> None:
        """When directionality violations are detected, CRITICAL audit records
        are emitted to the ledger.

        **Validates: Requirements 3.2**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            yaml_path = os.path.join(tmpdir, "declarations.yaml")
            ledger_path = os.path.join(tmpdir, "ledger.yaml")

            yaml_data = {
                "schema_version": "1.0.0",
                "modules": [d.to_dict() for d in declarations],
            }
            with open(yaml_path, "w") as f:
                yaml.dump(yaml_data, f)

            ledger = MutationAuditLedger(ledger_path)
            graph = GovernanceInfluenceGraph(
                declarations_path=yaml_path, ledger=ledger
            )
            graph.load_declarations()
            graph.build_graph()
            violations = graph.enforce_directionality()

            assert len(violations) > 0

            # Verify CRITICAL events were emitted
            entries = ledger.query_by_event_type("GOVERNANCE_EVENT")
            critical_entries = [e for e in entries if e.severity == "CRITICAL"]
            directionality_entries = [
                e for e in critical_entries
                if "directionality_violation" in str(e.actor.get("context", {}))
            ]
            assert len(directionality_entries) >= 1, (
                f"Expected CRITICAL audit record for directionality violation. "
                f"Ledger entries: {[e.to_dict() for e in entries]}"
            )
