"""Unit tests for runtime/severity_taxonomy.py.

Validates the canonical severity taxonomy structure and semantics.
Requirements: 17.1, 17.3, 17.5
"""

from runtime.severity_taxonomy import Severity, SEVERITY_DEFINITIONS


class TestSeverityEnum:
    """Tests for the Severity IntEnum."""

    def test_has_six_levels(self):
        assert len(Severity) == 6

    def test_level_values_are_ordered(self):
        assert Severity.INFO < Severity.WARNING
        assert Severity.WARNING < Severity.DEGRADED
        assert Severity.DEGRADED < Severity.CRITICAL
        assert Severity.CRITICAL < Severity.CANONICAL_BREAK
        assert Severity.CANONICAL_BREAK < Severity.DETERMINISTIC_FAILURE

    def test_info_is_zero(self):
        assert Severity.INFO == 0

    def test_deterministic_failure_is_five(self):
        assert Severity.DETERMINISTIC_FAILURE == 5

    def test_severity_is_int_comparable(self):
        assert Severity.CRITICAL > 2
        assert Severity.WARNING < 3


class TestSeverityDefinitions:
    """Tests for the SEVERITY_DEFINITIONS dict."""

    def test_all_levels_have_definitions(self):
        for level in Severity:
            assert level in SEVERITY_DEFINITIONS, f"Missing definition for {level.name}"

    def test_definitions_have_required_keys(self):
        required_keys = {
            "meaning",
            "blocks_pipeline_hard_mode",
            "triggers_audit_log",
            "appears_in_data_availability",
        }
        for level, definition in SEVERITY_DEFINITIONS.items():
            assert set(definition.keys()) == required_keys, (
                f"{level.name} has unexpected keys: {set(definition.keys())}"
            )

    def test_info_does_not_block_or_trigger(self):
        info = SEVERITY_DEFINITIONS[Severity.INFO]
        assert info["blocks_pipeline_hard_mode"] is False
        assert info["triggers_audit_log"] is False
        assert info["appears_in_data_availability"] is False

    def test_critical_and_above_block_pipeline(self):
        for level in (Severity.CRITICAL, Severity.CANONICAL_BREAK, Severity.DETERMINISTIC_FAILURE):
            assert SEVERITY_DEFINITIONS[level]["blocks_pipeline_hard_mode"] is True

    def test_warning_and_above_trigger_audit_log(self):
        for level in (Severity.WARNING, Severity.DEGRADED, Severity.CRITICAL,
                      Severity.CANONICAL_BREAK, Severity.DETERMINISTIC_FAILURE):
            assert SEVERITY_DEFINITIONS[level]["triggers_audit_log"] is True

    def test_degraded_and_above_appear_in_data_availability(self):
        for level in (Severity.DEGRADED, Severity.CRITICAL,
                      Severity.CANONICAL_BREAK, Severity.DETERMINISTIC_FAILURE):
            assert SEVERITY_DEFINITIONS[level]["appears_in_data_availability"] is True

    def test_meaning_is_non_empty_string(self):
        for level, definition in SEVERITY_DEFINITIONS.items():
            assert isinstance(definition["meaning"], str)
            assert len(definition["meaning"]) > 0, f"{level.name} has empty meaning"
