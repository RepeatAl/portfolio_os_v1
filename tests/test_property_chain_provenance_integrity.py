"""Property-based tests for Chain Provenance Integrity.

**Validates: Requirements 1.1, 10.1, 13.1, 13.4, 13.6**

Tests that complete/partial sections have unbroken chain from SIGNALS through
SEMANTICS through REASONING to REPORT. Hypothesis generates random provenance
graphs; verify all complete sections have full chain.
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from runtime.chain_validator import (
    ChainValidator,
    IdentifierGraph,
    ProvenanceBlock,
    VALID_COMPLETENESS_STATES,
)


# --- Strategies for identifier generation ---

identifier_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N")),
    min_size=1,
    max_size=30,
)

identifier_list_strategy = st.lists(
    identifier_strategy,
    min_size=1,
    max_size=5,
)

section_name_strategy = st.sampled_from([
    "Executive Summary",
    "Market Regime",
    "Portfolio Structure",
    "Concentration and Dependency",
    "Deployment Analysis",
    "Scenario Analysis",
    "Action Space",
    "Confidence Interpretation",
    "PM Summary",
])


# --- Strategy for building a complete, valid provenance graph ---

@st.composite
def complete_provenance_graph_strategy(draw):
    """Generate a complete provenance graph where all IDs are present and linked.

    Produces:
    - A list of reasoning objects (dicts) with reasoning_id and source_semantic_states
    - A list of semantic states (dicts) with signal_id and signal_origin
    - A ProvenanceBlock referencing IDs that exist in the graph
    """
    # Generate signal engine IDs (SIGNALS layer)
    signal_engine_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=3, unique=True
    ))

    # Generate semantic state IDs (SEMANTICS layer)
    semantic_state_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=4, unique=True
    ))

    # Generate reasoning object IDs (REASONING layer)
    reasoning_object_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=3, unique=True
    ))

    # Build semantic states: each maps to at least one signal engine
    semantic_states = []
    for sem_id in semantic_state_ids:
        # Each semantic state traces to at least one signal engine
        origin = draw(st.sampled_from(signal_engine_ids))
        semantic_states.append({
            "signal_id": sem_id,
            "signal_origin": origin,
        })

    # Build reasoning objects: each maps to at least one semantic state
    reasoning_objects = []
    for r_id in reasoning_object_ids:
        # Each reasoning object references at least one semantic state
        source_count = draw(st.integers(min_value=1, max_value=len(semantic_state_ids)))
        sources = draw(st.lists(
            st.sampled_from(semantic_state_ids),
            min_size=source_count,
            max_size=source_count,
        ))
        reasoning_objects.append({
            "reasoning_id": r_id,
            "source_semantic_states": sources,
        })

    # Build provenance block referencing the generated IDs
    section_name = draw(section_name_strategy)
    completeness = draw(st.sampled_from(["complete", "partial"]))

    provenance_block = ProvenanceBlock(
        section_name=section_name,
        reasoning_object_ids=reasoning_object_ids,
        semantic_state_ids=semantic_state_ids,
        signal_engine_ids=signal_engine_ids,
        completeness_state=completeness,
    )

    return reasoning_objects, semantic_states, provenance_block



@st.composite
def missing_reasoning_ids_strategy(draw):
    """Generate a provenance graph where reasoning IDs in the block are NOT in the graph.

    The provenance block references reasoning_object_ids that do not exist
    in the identifier graph, causing a REASONING violation.
    """
    # Generate signal engine IDs and semantic states that ARE in the graph
    signal_engine_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=3, unique=True
    ))
    semantic_state_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=3, unique=True
    ))

    # Build semantic states in the graph
    semantic_states = []
    for sem_id in semantic_state_ids:
        origin = draw(st.sampled_from(signal_engine_ids))
        semantic_states.append({
            "signal_id": sem_id,
            "signal_origin": origin,
        })

    # Build reasoning objects that ARE in the graph (with different IDs)
    graph_reasoning_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=2, unique=True
    ))
    reasoning_objects = []
    for r_id in graph_reasoning_ids:
        reasoning_objects.append({
            "reasoning_id": r_id,
            "source_semantic_states": [semantic_state_ids[0]],
        })

    # Generate reasoning IDs for the provenance block that are NOT in the graph
    missing_reasoning_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=3, unique=True
    ))
    # Ensure they don't accidentally match graph IDs
    assume(not set(missing_reasoning_ids) & set(graph_reasoning_ids))

    section_name = draw(section_name_strategy)
    completeness = draw(st.sampled_from(["complete", "partial"]))

    provenance_block = ProvenanceBlock(
        section_name=section_name,
        reasoning_object_ids=missing_reasoning_ids,
        semantic_state_ids=semantic_state_ids,
        signal_engine_ids=signal_engine_ids,
        completeness_state=completeness,
    )

    return reasoning_objects, semantic_states, provenance_block


@st.composite
def missing_semantic_ids_strategy(draw):
    """Generate a provenance graph where reasoning objects reference semantic IDs not in graph.

    The reasoning objects in the graph have source_semantic_states that do NOT
    exist in the semantic states collection, causing a SEMANTICS violation.
    """
    # Generate signal engine IDs
    signal_engine_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=3, unique=True
    ))

    # Generate semantic state IDs that ARE in the graph
    graph_semantic_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=2, unique=True
    ))
    semantic_states = []
    for sem_id in graph_semantic_ids:
        origin = draw(st.sampled_from(signal_engine_ids))
        semantic_states.append({
            "signal_id": sem_id,
            "signal_origin": origin,
        })

    # Generate semantic IDs that are NOT in the graph (missing)
    missing_semantic_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=3, unique=True
    ))
    assume(not set(missing_semantic_ids) & set(graph_semantic_ids))

    # Build reasoning objects that reference the MISSING semantic IDs
    reasoning_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=2, unique=True
    ))
    reasoning_objects = []
    for r_id in reasoning_ids:
        reasoning_objects.append({
            "reasoning_id": r_id,
            "source_semantic_states": missing_semantic_ids,
        })

    section_name = draw(section_name_strategy)
    completeness = draw(st.sampled_from(["complete", "partial"]))

    provenance_block = ProvenanceBlock(
        section_name=section_name,
        reasoning_object_ids=reasoning_ids,
        semantic_state_ids=graph_semantic_ids + missing_semantic_ids,
        signal_engine_ids=signal_engine_ids,
        completeness_state=completeness,
    )

    return reasoning_objects, semantic_states, provenance_block


@st.composite
def missing_signal_engines_strategy(draw):
    """Generate a provenance graph where semantic states have no signal_origin.

    The semantic states in the graph have empty signal_origin, causing a
    SIGNALS violation.
    """
    # Generate semantic state IDs
    semantic_state_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=3, unique=True
    ))

    # Build semantic states with EMPTY signal_origin (no signal engines)
    semantic_states = []
    for sem_id in semantic_state_ids:
        semantic_states.append({
            "signal_id": sem_id,
            "signal_origin": "",  # Empty — no signal engine
        })

    # Build reasoning objects that reference the semantic states
    reasoning_ids = draw(st.lists(
        identifier_strategy, min_size=1, max_size=2, unique=True
    ))
    reasoning_objects = []
    for r_id in reasoning_ids:
        reasoning_objects.append({
            "reasoning_id": r_id,
            "source_semantic_states": semantic_state_ids,
        })

    section_name = draw(section_name_strategy)
    completeness = draw(st.sampled_from(["complete", "partial"]))

    provenance_block = ProvenanceBlock(
        section_name=section_name,
        reasoning_object_ids=reasoning_ids,
        semantic_state_ids=semantic_state_ids,
        signal_engine_ids=[],
        completeness_state=completeness,
    )

    return reasoning_objects, semantic_states, provenance_block



class TestChainProvenanceIntegrity:
    """Property-based tests for Chain Provenance Integrity validation."""

    @given(data=complete_provenance_graph_strategy())
    @settings(max_examples=200)
    def test_complete_provenance_graph_produces_no_violations(self, data) -> None:
        """Property 1: Complete provenance graphs produce zero violations.

        **Validates: Requirements 1.1, 10.1, 13.1, 13.4**

        For any complete provenance graph (all IDs present in graph with full
        chain from SIGNALS through SEMANTICS through REASONING),
        validate_section returns no violations.
        """
        reasoning_objects, semantic_states, provenance_block = data

        validator = ChainValidator()
        validator.build_graph(reasoning_objects, semantic_states)
        violations = validator.validate_section(provenance_block)

        assert violations == [], (
            f"Complete provenance graph produced violations: {violations}\n"
            f"Section: {provenance_block.section_name}\n"
            f"Reasoning IDs: {provenance_block.reasoning_object_ids}\n"
            f"Graph reasoning IDs: {validator.graph.all_reasoning_ids}\n"
            f"Graph semantic IDs: {validator.graph.all_semantic_ids}\n"
            f"Graph signal engine IDs: {validator.graph.all_signal_engine_ids}"
        )

    @given(data=missing_reasoning_ids_strategy())
    @settings(max_examples=200)
    def test_missing_reasoning_ids_produce_reasoning_violation(self, data) -> None:
        """Property 2: Missing reasoning IDs produce REASONING violations.

        **Validates: Requirements 10.1, 13.6**

        For any provenance block with reasoning_object_ids not present in the
        identifier graph, a REASONING violation is produced.
        """
        reasoning_objects, semantic_states, provenance_block = data

        validator = ChainValidator()
        validator.build_graph(reasoning_objects, semantic_states)
        violations = validator.validate_section(provenance_block)

        assert len(violations) > 0, (
            f"Missing reasoning IDs did not produce violations\n"
            f"Block reasoning IDs: {provenance_block.reasoning_object_ids}\n"
            f"Graph reasoning IDs: {validator.graph.all_reasoning_ids}"
        )
        reasoning_violations = [
            v for v in violations if v["broken_layer"] == "REASONING"
        ]
        assert len(reasoning_violations) > 0, (
            f"Expected REASONING violation but got: {violations}\n"
            f"Block reasoning IDs: {provenance_block.reasoning_object_ids}\n"
            f"Graph reasoning IDs: {validator.graph.all_reasoning_ids}"
        )

    @given(data=missing_semantic_ids_strategy())
    @settings(max_examples=200)
    def test_missing_semantic_ids_produce_semantics_violation(self, data) -> None:
        """Property 3: Missing semantic IDs produce SEMANTICS violations.

        **Validates: Requirements 10.1, 13.6**

        For any provenance block where reasoning objects reference semantic IDs
        not traced in the graph, a SEMANTICS violation is produced.
        """
        reasoning_objects, semantic_states, provenance_block = data

        validator = ChainValidator()
        validator.build_graph(reasoning_objects, semantic_states)
        violations = validator.validate_section(provenance_block)

        assert len(violations) > 0, (
            f"Missing semantic IDs did not produce violations\n"
            f"Reasoning objects: {reasoning_objects}\n"
            f"Graph semantic IDs: {validator.graph.all_semantic_ids}"
        )
        semantics_violations = [
            v for v in violations if v["broken_layer"] == "SEMANTICS"
        ]
        assert len(semantics_violations) > 0, (
            f"Expected SEMANTICS violation but got: {violations}\n"
            f"Reasoning objects: {reasoning_objects}\n"
            f"Graph semantic IDs: {validator.graph.all_semantic_ids}"
        )

    @given(data=missing_signal_engines_strategy())
    @settings(max_examples=200)
    def test_missing_signal_engines_produce_signals_violation(self, data) -> None:
        """Property 4: Missing signal engines produce SIGNALS violations.

        **Validates: Requirements 10.1, 13.6**

        For any provenance block where semantic states have no signal_origin
        (not traced from semantics to signals), a SIGNALS violation is produced.
        """
        reasoning_objects, semantic_states, provenance_block = data

        validator = ChainValidator()
        validator.build_graph(reasoning_objects, semantic_states)
        violations = validator.validate_section(provenance_block)

        assert len(violations) > 0, (
            f"Missing signal engines did not produce violations\n"
            f"Semantic states: {semantic_states}\n"
            f"Graph signal engine IDs: {validator.graph.all_signal_engine_ids}"
        )
        signals_violations = [
            v for v in violations if v["broken_layer"] == "SIGNALS"
        ]
        assert len(signals_violations) > 0, (
            f"Expected SIGNALS violation but got: {violations}\n"
            f"Semantic states: {semantic_states}\n"
            f"Graph signal engine IDs: {validator.graph.all_signal_engine_ids}"
        )

    @given(
        section_name=section_name_strategy,
        reasoning_ids=st.lists(identifier_strategy, min_size=0, max_size=3),
        semantic_ids=st.lists(identifier_strategy, min_size=0, max_size=3),
        signal_ids=st.lists(identifier_strategy, min_size=0, max_size=3),
    )
    @settings(max_examples=200)
    def test_unavailable_sections_produce_zero_violations(
        self,
        section_name: str,
        reasoning_ids: list[str],
        semantic_ids: list[str],
        signal_ids: list[str],
    ) -> None:
        """Property 5: Unavailable sections always produce zero violations.

        **Validates: Requirements 1.1, 10.1**

        For any provenance block with completeness_state "unavailable",
        validate_section returns zero violations regardless of chain content.
        Unavailable sections are allowed to have empty chains.
        """
        provenance_block = ProvenanceBlock(
            section_name=section_name,
            reasoning_object_ids=reasoning_ids,
            semantic_state_ids=semantic_ids,
            signal_engine_ids=signal_ids,
            completeness_state="unavailable",
            unavailability_reasons=["Engine failure"],
        )

        # Build a minimal graph (may or may not contain the IDs)
        validator = ChainValidator()
        validator.build_graph([], [])
        violations = validator.validate_section(provenance_block)

        assert violations == [], (
            f"Unavailable section produced violations: {violations}\n"
            f"Section: {section_name}\n"
            f"Completeness: unavailable"
        )
