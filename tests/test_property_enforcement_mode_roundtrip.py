"""Property test: Enforcement Mode Round-Trip.

**Property 4: Enforcement Mode Round-Trip**
**Validates: Requirements 7.6**

Tests that FailMode StrEnum values survive string conversion and back.
Tests that enforcement mode strings ("observability", "soft", "hard")
round-trip through the FailModeRegistry.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from governance.fail_mode_registry import FailMode, FailModeRegistry


# Strategy for FailMode enum values
fail_mode_strategy = st.sampled_from(list(FailMode))

# Strategy for enforcement mode strings
enforcement_mode_strategy = st.sampled_from(["observability", "soft", "hard"])


@given(fail_mode=fail_mode_strategy)
@settings(max_examples=100)
def test_fail_mode_string_roundtrip(fail_mode: FailMode) -> None:
    """FailMode StrEnum values survive string conversion and back."""
    string_value = str(fail_mode)
    restored = FailMode(string_value)
    assert restored == fail_mode
    assert restored.value == fail_mode.value


@given(fail_mode=fail_mode_strategy)
@settings(max_examples=100)
def test_fail_mode_value_roundtrip(fail_mode: FailMode) -> None:
    """FailMode .value property round-trips through FailMode constructor."""
    value = fail_mode.value
    restored = FailMode(value)
    assert restored is fail_mode


@given(enforcement_mode=enforcement_mode_strategy)
@settings(max_examples=100)
def test_enforcement_mode_registry_roundtrip(enforcement_mode: str) -> None:
    """Enforcement mode strings round-trip through the FailModeRegistry.

    For components with enforcement-mode-dependent fail modes, querying
    with a valid enforcement mode returns a valid FailMode that can be
    converted back to string and re-parsed.
    """
    registry = FailModeRegistry(
        config_path=".domainization/fail_mode_config.yaml"
    )

    # yaml_config_parser has enforcement-mode-dependent fail modes
    result = registry.get_fail_mode("yaml_config_parser", enforcement_mode)

    # The result must be a valid FailMode
    assert isinstance(result, FailMode)

    # The result must survive string round-trip
    string_value = str(result)
    restored = FailMode(string_value)
    assert restored == result


@given(enforcement_mode=enforcement_mode_strategy)
@settings(max_examples=100)
def test_lifecycle_enforcer_mode_dependent_roundtrip(enforcement_mode: str) -> None:
    """lifecycle_enforcer enforcement-mode-dependent fail modes round-trip."""
    registry = FailModeRegistry(
        config_path=".domainization/fail_mode_config.yaml"
    )

    result = registry.get_fail_mode("lifecycle_enforcer", enforcement_mode)

    assert isinstance(result, FailMode)
    assert FailMode(str(result)) == result
