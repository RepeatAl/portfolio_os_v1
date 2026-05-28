"""Property-based tests for Provenance Parseability.

**Validates: Requirements 13.3, 24.3**

Tests that any provenance block serialized to YAML/JSON parses successfully
with standard parsers and contains completeness state. Hypothesis generates
random SectionProvenance instances with varying field values; verify
serialization round-trip integrity.
"""

import json

import yaml
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from governance.provenance_schema import SectionProvenance


# --- Strategies for SectionProvenance field generation ---

section_name_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
    min_size=1,
    max_size=80,
)

id_string_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P")),
    min_size=1,
    max_size=50,
)

reasoning_object_ids_strategy = st.lists(id_string_strategy, min_size=0, max_size=10)

semantic_state_ids_strategy = st.lists(id_string_strategy, min_size=0, max_size=10)

signal_engine_ids_strategy = st.lists(id_string_strategy, min_size=0, max_size=10)

completeness_state_strategy = st.sampled_from(
    ["complete", "partial", "degraded", "unavailable", "invalid"]
)

unavailable_layer_strategy = st.fixed_dictionaries(
    {"layer": st.sampled_from(["SIGNALS", "SEMANTICS", "REASONING"]),
     "reason": st.text(
         alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
         min_size=1,
         max_size=80,
     )}
)

unavailable_layers_strategy = st.lists(unavailable_layer_strategy, min_size=0, max_size=5)

schema_version_strategy = st.just("1.0.0")


# --- Strategy for a fully populated SectionProvenance ---

section_provenance_strategy = st.builds(
    SectionProvenance,
    section_name=section_name_strategy,
    reasoning_object_ids=reasoning_object_ids_strategy,
    semantic_state_ids=semantic_state_ids_strategy,
    signal_engine_ids=signal_engine_ids_strategy,
    completeness_state=completeness_state_strategy,
    unavailable_layers=unavailable_layers_strategy,
    schema_version=schema_version_strategy,
)


class TestProvenanceParseability:
    """Property-based tests for SectionProvenance serialization parseability."""

    @given(provenance=section_provenance_strategy)
    @settings(max_examples=200, deadline=None)
    def test_yaml_serialization_parses_without_error(
        self, provenance: SectionProvenance
    ) -> None:
        """Property 1: Any SectionProvenance serialized to YAML parses back without error.

        **Validates: Requirements 13.3**

        For any SectionProvenance instance, to_yaml() produces output that
        yaml.safe_load can parse without raising an exception.
        """
        yaml_output = provenance.to_yaml()
        parsed = yaml.safe_load(yaml_output)
        assert parsed is not None, (
            f"yaml.safe_load returned None for provenance: "
            f"section_name={provenance.section_name!r}"
        )
        assert isinstance(parsed, dict), (
            f"yaml.safe_load returned {type(parsed).__name__}, expected dict"
        )

    @given(provenance=section_provenance_strategy)
    @settings(max_examples=200, deadline=None)
    def test_json_serialization_parses_without_error(
        self, provenance: SectionProvenance
    ) -> None:
        """Property 2: Any SectionProvenance serialized to JSON parses back without error.

        **Validates: Requirements 13.3**

        For any SectionProvenance instance, to_json() produces output that
        json.loads can parse without raising an exception.
        """
        json_output = provenance.to_json()
        parsed = json.loads(json_output)
        assert parsed is not None, (
            f"json.loads returned None for provenance: "
            f"section_name={provenance.section_name!r}"
        )
        assert isinstance(parsed, dict), (
            f"json.loads returned {type(parsed).__name__}, expected dict"
        )

    @given(provenance=section_provenance_strategy)
    @settings(max_examples=200, deadline=None)
    def test_parsed_yaml_contains_completeness_state(
        self, provenance: SectionProvenance
    ) -> None:
        """Property 3: Parsed YAML always contains 'completeness_state' key.

        **Validates: Requirements 24.3**

        For any SectionProvenance instance, the YAML-parsed dict always
        contains the 'completeness_state' key with the original value.
        """
        yaml_output = provenance.to_yaml()
        parsed = yaml.safe_load(yaml_output)
        assert "completeness_state" in parsed, (
            f"Parsed YAML missing 'completeness_state' key. "
            f"Keys present: {list(parsed.keys())}"
        )
        assert parsed["completeness_state"] == provenance.completeness_state, (
            f"completeness_state mismatch: "
            f"expected={provenance.completeness_state!r}, "
            f"got={parsed['completeness_state']!r}"
        )

    @given(provenance=section_provenance_strategy)
    @settings(max_examples=200, deadline=None)
    def test_parsed_yaml_contains_all_required_keys(
        self, provenance: SectionProvenance
    ) -> None:
        """Property 4: Parsed YAML contains all required provenance keys.

        **Validates: Requirements 13.3, 24.3**

        For any SectionProvenance instance, the YAML-parsed dict always
        contains section_name, reasoning_object_ids, semantic_state_ids,
        signal_engine_ids, and completeness_state keys.
        """
        yaml_output = provenance.to_yaml()
        parsed = yaml.safe_load(yaml_output)
        required_keys = [
            "section_name",
            "reasoning_object_ids",
            "semantic_state_ids",
            "signal_engine_ids",
            "completeness_state",
        ]
        for key in required_keys:
            assert key in parsed, (
                f"Parsed YAML missing required key '{key}'. "
                f"Keys present: {list(parsed.keys())}"
            )

    @given(provenance=section_provenance_strategy)
    @settings(max_examples=200, deadline=None)
    def test_round_trip_yaml_preserves_field_values(
        self, provenance: SectionProvenance
    ) -> None:
        """Property 5: YAML round-trip preserves original field values.

        **Validates: Requirements 13.3**

        For any SectionProvenance instance, serializing to YAML and parsing
        back produces data that matches the original field values.
        Note: to_yaml() intentionally sorts identifier lists for deterministic
        output (HARDENING requirement), so we compare against sorted lists.
        """
        yaml_output = provenance.to_yaml()
        parsed = yaml.safe_load(yaml_output)

        assert parsed["section_name"] == provenance.section_name, (
            f"section_name mismatch after round-trip: "
            f"expected={provenance.section_name!r}, got={parsed['section_name']!r}"
        )
        assert parsed["reasoning_object_ids"] == sorted(provenance.reasoning_object_ids), (
            f"reasoning_object_ids mismatch after round-trip"
        )
        assert parsed["semantic_state_ids"] == sorted(provenance.semantic_state_ids), (
            f"semantic_state_ids mismatch after round-trip"
        )
        assert parsed["signal_engine_ids"] == sorted(provenance.signal_engine_ids), (
            f"signal_engine_ids mismatch after round-trip"
        )
        assert parsed["completeness_state"] == provenance.completeness_state, (
            f"completeness_state mismatch after round-trip"
        )
        assert parsed["unavailable_layers"] == provenance.unavailable_layers, (
            f"unavailable_layers mismatch after round-trip"
        )
        assert parsed["schema_version"] == provenance.schema_version, (
            f"schema_version mismatch after round-trip"
        )

    @given(provenance=section_provenance_strategy)
    @settings(max_examples=200, deadline=None)
    def test_round_trip_json_preserves_field_values(
        self, provenance: SectionProvenance
    ) -> None:
        """Property 6: JSON round-trip preserves original field values.

        **Validates: Requirements 13.3**

        For any SectionProvenance instance, serializing to JSON and parsing
        back produces data that matches the original field values.
        """
        json_output = provenance.to_json()
        parsed = json.loads(json_output)

        assert parsed["section_name"] == provenance.section_name, (
            f"section_name mismatch after JSON round-trip: "
            f"expected={provenance.section_name!r}, got={parsed['section_name']!r}"
        )
        assert parsed["reasoning_object_ids"] == provenance.reasoning_object_ids, (
            f"reasoning_object_ids mismatch after JSON round-trip"
        )
        assert parsed["semantic_state_ids"] == provenance.semantic_state_ids, (
            f"semantic_state_ids mismatch after JSON round-trip"
        )
        assert parsed["signal_engine_ids"] == provenance.signal_engine_ids, (
            f"signal_engine_ids mismatch after JSON round-trip"
        )
        assert parsed["completeness_state"] == provenance.completeness_state, (
            f"completeness_state mismatch after JSON round-trip"
        )
        assert parsed["unavailable_layers"] == provenance.unavailable_layers, (
            f"unavailable_layers mismatch after JSON round-trip"
        )
        assert parsed["schema_version"] == provenance.schema_version, (
            f"schema_version mismatch after JSON round-trip"
        )

    @given(provenance=section_provenance_strategy)
    @settings(max_examples=200, deadline=None)
    def test_parsed_json_contains_completeness_state(
        self, provenance: SectionProvenance
    ) -> None:
        """Property 7: Parsed JSON always contains 'completeness_state' key.

        **Validates: Requirements 24.3**

        For any SectionProvenance instance, the JSON-parsed dict always
        contains the 'completeness_state' key with the original value.
        """
        json_output = provenance.to_json()
        parsed = json.loads(json_output)
        assert "completeness_state" in parsed, (
            f"Parsed JSON missing 'completeness_state' key. "
            f"Keys present: {list(parsed.keys())}"
        )
        assert parsed["completeness_state"] == provenance.completeness_state, (
            f"completeness_state mismatch in JSON: "
            f"expected={provenance.completeness_state!r}, "
            f"got={parsed['completeness_state']!r}"
        )

    @given(provenance=section_provenance_strategy)
    @settings(max_examples=200, deadline=None)
    def test_parsed_json_contains_all_required_keys(
        self, provenance: SectionProvenance
    ) -> None:
        """Property 8: Parsed JSON contains all required provenance keys.

        **Validates: Requirements 13.3, 24.3**

        For any SectionProvenance instance, the JSON-parsed dict always
        contains section_name, reasoning_object_ids, semantic_state_ids,
        signal_engine_ids, and completeness_state keys.
        """
        json_output = provenance.to_json()
        parsed = json.loads(json_output)
        required_keys = [
            "section_name",
            "reasoning_object_ids",
            "semantic_state_ids",
            "signal_engine_ids",
            "completeness_state",
        ]
        for key in required_keys:
            assert key in parsed, (
                f"Parsed JSON missing required key '{key}'. "
                f"Keys present: {list(parsed.keys())}"
            )
