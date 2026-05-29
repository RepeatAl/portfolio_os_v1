"""Property test: Self-Disable Guard Immutability.

**Property 32: Self-Disable Guard Immutability**
**Validates: Requirements 49.1, 49.2, 49.4**

Tests that once FailModeRegistry.freeze() is called, ALL subsequent
attempt_modification() calls return (False, reason) regardless of
component_name, target_field, or new_value.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from governance.fail_mode_registry import FailMode, FailModeRegistry


# Strategy for component names (both registered and unregistered)
component_name_strategy = st.sampled_from([
    "mutation_audit_ledger",
    "yaml_config_parser",
    "boundary_enforcer",
    "warning_governor",
    "lifecycle_enforcer",
    "gate_framework",
    "policy_versioner",
    "nonexistent_component",
    "arbitrary_module",
])

# Strategy for target fields
target_field_strategy = st.sampled_from([
    "fail_mode",
    "enforcement_mode",
    "blocking_behavior",
    "unknown_field",
])

# Strategy for new values (valid and invalid fail modes)
new_value_strategy = st.sampled_from([
    "fail_open",
    "fail_soft",
    "fail_closed",
    "invalid_mode",
    "observability",
    "",
])


@given(
    component_name=component_name_strategy,
    target_field=target_field_strategy,
    new_value=new_value_strategy,
)
@settings(max_examples=100)
def test_frozen_registry_blocks_all_modifications(
    component_name: str,
    target_field: str,
    new_value: str,
) -> None:
    """Once freeze() is called, ALL attempt_modification() calls return (False, reason)."""
    registry = FailModeRegistry(
        config_path=".domainization/fail_mode_config.yaml"
    )

    # Freeze the registry
    registry.freeze()
    assert registry.is_frozen() is True

    # Attempt modification — must always be rejected
    allowed, reason = registry.attempt_modification(
        component_name=component_name,
        target_field=target_field,
        new_value=new_value,
    )

    assert allowed is False
    assert isinstance(reason, str)
    assert len(reason) > 0


@given(
    component_name=component_name_strategy,
    new_value=st.sampled_from(["fail_open", "fail_soft", "fail_closed"]),
)
@settings(max_examples=100)
def test_frozen_registry_preserves_original_classifications(
    component_name: str,
    new_value: str,
) -> None:
    """Frozen registry preserves original classifications after rejected modifications."""
    registry = FailModeRegistry(
        config_path=".domainization/fail_mode_config.yaml"
    )

    # Capture original classifications
    original_classifications = registry.get_all_classifications()

    # Freeze and attempt modification
    registry.freeze()
    registry.attempt_modification(component_name, "fail_mode", new_value)

    # Classifications must be unchanged
    current_classifications = registry.get_all_classifications()
    assert current_classifications == original_classifications


@given(
    component_name=component_name_strategy,
    target_field=target_field_strategy,
    new_value=new_value_strategy,
)
@settings(max_examples=100)
def test_unfrozen_registry_freeze_then_reject(
    component_name: str,
    target_field: str,
    new_value: str,
) -> None:
    """Registry transitions from unfrozen to frozen and rejects all subsequent modifications."""
    registry = FailModeRegistry(
        config_path=".domainization/fail_mode_config.yaml"
    )

    # Initially not frozen
    assert registry.is_frozen() is False

    # Freeze
    registry.freeze()
    assert registry.is_frozen() is True

    # All modifications must be rejected
    allowed, reason = registry.attempt_modification(
        component_name=component_name,
        target_field=target_field,
        new_value=new_value,
    )
    assert allowed is False
