"""Property-based tests for Sunset Governance Behavior.

**Validates: Requirements 25.3, 25.4**

Tests that Phase 1→2→3→4 transitions follow date and dependency rules.
Tests that files at sunset with zero deps transition to RUNTIME_DISABLED;
files at sunset with deps remain in sunset-blocked state + CRITICAL warning.
Tests that phase evaluation is deterministic given same dates and dependency counts.
"""

from __future__ import annotations

import tempfile
from datetime import date, timedelta
from pathlib import Path

import yaml
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from governance.sunset_governance import (
    CompatibilityImpact,
    DeprecationGovernance,
    SunsetGovernance,
    SunsetPhase,
)


# ---------------------------------------------------------------------------
# Hypothesis Strategies
# ---------------------------------------------------------------------------

# Generate random dates within a reasonable range (2024-2030)
date_strategy = st.dates(
    min_value=date(2024, 1, 1),
    max_value=date(2030, 12, 31),
)

# Generate dependency counts (0 to 20 downstream consumers)
dependency_count_strategy = st.integers(min_value=0, max_value=20)

# Generate artifact IDs
artifact_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_-"),
    min_size=3,
    max_size=40,
).filter(lambda s: s[0].isalpha())

# Generate deprecation reasons (max 200 chars)
deprecation_reason_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Z"), whitelist_characters="._- "),
    min_size=5,
    max_size=100,
)

# Generate compatibility impacts
compatibility_impact_strategy = st.sampled_from(["none", "minor", "breaking"])


def _create_registry_yaml(
    artifact_id: str,
    deprecated_date: str | None = None,
    sunset_date: str | None = None,
    replacement_artifact: str | None = None,
    deprecation_reason: str | None = None,
    compatibility_impact: str | None = None,
    lifecycle_status: str = "current",
    dependents: list[str] | None = None,
) -> str:
    """Create a temporary registry YAML file and return its path.

    Args:
        artifact_id: The artifact to test.
        deprecated_date: ISO 8601 date string or None.
        sunset_date: ISO 8601 date string or None.
        replacement_artifact: Replacement artifact_id or None.
        deprecation_reason: Reason string or None.
        compatibility_impact: Impact classification or None.
        lifecycle_status: Lifecycle status of the artifact.
        dependents: List of artifact_ids that depend on this artifact.

    Returns:
        Path to the temporary YAML file.
    """
    artifacts = [
        {
            "artifact_id": artifact_id,
            "file_path": f"engines/{artifact_id}.txt",
            "primary_domain": "REPORT",
            "artifact_type": "REPORT_OUT",
            "lifecycle_status": lifecycle_status,
            "created_date": "2024-01-01",
            "last_modified": "2024-06-01",
            "owner_role": "system",
            "dependencies": [],
        }
    ]

    if deprecated_date:
        artifacts[0]["deprecated_date"] = deprecated_date
    if sunset_date:
        artifacts[0]["sunset_date"] = sunset_date
    if replacement_artifact:
        artifacts[0]["replacement_artifact"] = replacement_artifact
    if deprecation_reason:
        artifacts[0]["deprecation_reason"] = deprecation_reason
    if compatibility_impact:
        artifacts[0]["compatibility_impact"] = compatibility_impact

    # Add dependent artifacts that reference our target artifact
    if dependents:
        for dep_id in dependents:
            artifacts.append(
                {
                    "artifact_id": dep_id,
                    "file_path": f"engines/{dep_id}.py",
                    "primary_domain": "SIGNALS",
                    "artifact_type": "ENGINE",
                    "lifecycle_status": "current",
                    "created_date": "2024-01-01",
                    "last_modified": "2024-06-01",
                    "owner_role": "system",
                    "dependencies": [artifact_id],
                }
            )

    registry_data = {"artifacts": artifacts}

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, prefix="test_registry_"
    )
    yaml.dump(registry_data, tmp, default_flow_style=False)
    tmp.close()
    return tmp.name



class TestSunsetGovernanceBehaviorProperties:
    """Property-based tests for sunset governance phase transitions and behavior."""

    @given(
        deprecated_date=date_strategy,
        sunset_date=date_strategy,
        reference_date=date_strategy,
        dep_count=dependency_count_strategy,
        has_replacement=st.booleans(),
    )
    @settings(max_examples=200)
    def test_phase_transitions_follow_date_and_dependency_rules(
        self,
        deprecated_date: date,
        sunset_date: date,
        reference_date: date,
        dep_count: int,
        has_replacement: bool,
    ) -> None:
        """Property 1: Phase 1→2→3→4 transitions follow date and dependency rules.

        **Validates: Requirements 25.3, 25.4**

        Given random sunset dates, dependency counts, and current dates,
        the phase assignment must match the sunset governance policy:
        - NOT_DEPRECATED if no deprecated_date
        - WARNING_ONLY if deprecated but no replacement
        - REPLACEMENT_PATH if replacement set and sunset not reached
        - RUNTIME_DISABLED if sunset date reached (regardless of deps)
        - ARCHIVED if lifecycle_status == 'archived'
        """
        # Ensure sunset_date >= deprecated_date (valid governance constraint)
        assume(sunset_date >= deprecated_date)

        artifact_id = "test_briefing_artifact"
        replacement = "chain_compliant_output" if has_replacement else None

        # Create dependents based on dep_count
        dependents = [f"consumer_{i}" for i in range(dep_count)]

        registry_path = _create_registry_yaml(
            artifact_id=artifact_id,
            deprecated_date=deprecated_date.isoformat(),
            sunset_date=sunset_date.isoformat(),
            replacement_artifact=replacement,
            deprecation_reason="Replaced by chain-compliant output",
            compatibility_impact="breaking",
            dependents=dependents,
        )

        try:
            gov = SunsetGovernance(
                registry_path=registry_path,
                reference_date=reference_date,
            )
            phase = gov.evaluate_sunset_phase(artifact_id)

            # Verify phase assignment matches policy
            if reference_date >= sunset_date:
                # Sunset date reached → RUNTIME_DISABLED
                assert phase == SunsetPhase.RUNTIME_DISABLED, (
                    f"Expected RUNTIME_DISABLED when reference_date ({reference_date}) >= "
                    f"sunset_date ({sunset_date}), got {phase}"
                )
            elif replacement is not None:
                # Has replacement but sunset not reached → REPLACEMENT_PATH
                assert phase == SunsetPhase.REPLACEMENT_PATH, (
                    f"Expected REPLACEMENT_PATH when replacement set and sunset not reached, "
                    f"got {phase}"
                )
            else:
                # Deprecated but no replacement → WARNING_ONLY
                assert phase == SunsetPhase.WARNING_ONLY, (
                    f"Expected WARNING_ONLY when deprecated without replacement, got {phase}"
                )
        finally:
            Path(registry_path).unlink(missing_ok=True)

    @given(
        deprecated_date=date_strategy,
        sunset_offset=st.integers(min_value=1, max_value=365),
        dep_count=st.integers(min_value=1, max_value=20),
    )
    @settings(max_examples=200)
    def test_sunset_with_deps_remains_blocked_with_critical_warning(
        self,
        deprecated_date: date,
        sunset_offset: int,
        dep_count: int,
    ) -> None:
        """Property 2: Files at sunset with deps remain in sunset-blocked state + CRITICAL warning.

        **Validates: Requirements 25.4**

        When a briefing file reaches its sunset_target_date but
        downstream_dependency_count > 0, the file SHALL continue generating
        and a critical-severity warning SHALL be logged.
        """
        sunset_date = deprecated_date + timedelta(days=sunset_offset)
        # Reference date is at or after sunset
        reference_date = sunset_date + timedelta(days=1)

        artifact_id = "blocked_briefing"
        dependents = [f"consumer_{i}" for i in range(dep_count)]

        registry_path = _create_registry_yaml(
            artifact_id=artifact_id,
            deprecated_date=deprecated_date.isoformat(),
            sunset_date=sunset_date.isoformat(),
            replacement_artifact="chain_replacement",
            deprecation_reason="Legacy briefing replaced",
            compatibility_impact="breaking",
            dependents=dependents,
        )

        try:
            gov = SunsetGovernance(
                registry_path=registry_path,
                reference_date=reference_date,
            )

            # Phase should be RUNTIME_DISABLED (sunset reached)
            phase = gov.evaluate_sunset_phase(artifact_id)
            assert phase == SunsetPhase.RUNTIME_DISABLED, (
                f"Expected RUNTIME_DISABLED at sunset, got {phase}"
            )

            # Should be sunset-blocked (deps > 0)
            assert gov.is_sunset_blocked(artifact_id) is True, (
                f"Expected sunset-blocked with {dep_count} dependencies"
            )

            # Should still generate (blocked means generation continues)
            assert gov.should_generate(artifact_id) is True, (
                f"Expected should_generate=True when sunset-blocked"
            )

            # Warning should be CRITICAL level
            warning = gov.get_deprecation_warning(artifact_id)
            assert warning is not None, "Expected a deprecation warning"
            assert "[CRITICAL]" in warning, (
                f"Expected CRITICAL warning for sunset-blocked artifact, got: {warning}"
            )
            assert str(dep_count) in warning, (
                f"Expected dependency count {dep_count} in warning message"
            )
        finally:
            Path(registry_path).unlink(missing_ok=True)

    @given(
        deprecated_date=date_strategy,
        sunset_offset=st.integers(min_value=1, max_value=365),
    )
    @settings(max_examples=200)
    def test_sunset_with_zero_deps_transitions_to_runtime_disabled(
        self,
        deprecated_date: date,
        sunset_offset: int,
    ) -> None:
        """Property 3: Files at sunset with zero deps transition to RUNTIME_DISABLED.

        **Validates: Requirements 25.3**

        When a briefing file reaches its sunset_target_date and
        downstream_dependency_count is zero, the Pipeline_Orchestrator
        SHALL stop generating that file.
        """
        sunset_date = deprecated_date + timedelta(days=sunset_offset)
        # Reference date is at or after sunset
        reference_date = sunset_date + timedelta(days=1)

        artifact_id = "clean_sunset_briefing"

        registry_path = _create_registry_yaml(
            artifact_id=artifact_id,
            deprecated_date=deprecated_date.isoformat(),
            sunset_date=sunset_date.isoformat(),
            replacement_artifact="chain_replacement",
            deprecation_reason="Legacy briefing replaced",
            compatibility_impact="minor",
            dependents=[],  # Zero dependencies
        )

        try:
            gov = SunsetGovernance(
                registry_path=registry_path,
                reference_date=reference_date,
            )

            # Phase should be RUNTIME_DISABLED
            phase = gov.evaluate_sunset_phase(artifact_id)
            assert phase == SunsetPhase.RUNTIME_DISABLED, (
                f"Expected RUNTIME_DISABLED at sunset with zero deps, got {phase}"
            )

            # Should NOT be sunset-blocked (zero deps)
            assert gov.is_sunset_blocked(artifact_id) is False, (
                "Expected NOT sunset-blocked with zero dependencies"
            )

            # Should NOT generate (clean sunset = stop generation)
            assert gov.should_generate(artifact_id) is False, (
                "Expected should_generate=False when sunset reached with zero deps"
            )

            # Warning should indicate sunset completion
            warning = gov.get_deprecation_warning(artifact_id)
            assert warning is not None, "Expected a sunset warning"
            assert "[SUNSET]" in warning, (
                f"Expected [SUNSET] marker in warning for clean sunset, got: {warning}"
            )
        finally:
            Path(registry_path).unlink(missing_ok=True)

    @given(
        deprecated_date=date_strategy,
        sunset_date=date_strategy,
        reference_date=date_strategy,
        dep_count=dependency_count_strategy,
        has_replacement=st.booleans(),
    )
    @settings(max_examples=200, deadline=None)
    def test_phase_evaluation_is_deterministic(
        self,
        deprecated_date: date,
        sunset_date: date,
        reference_date: date,
        dep_count: int,
        has_replacement: bool,
    ) -> None:
        """Property 4: Phase evaluation is deterministic given same dates and dependency counts.

        **Validates: Requirements 25.3, 25.4**

        Given the same inputs (dates, dependency counts), evaluating the
        sunset phase multiple times always produces the same result.
        """
        assume(sunset_date >= deprecated_date)

        artifact_id = "determinism_test_artifact"
        replacement = "replacement_output" if has_replacement else None
        dependents = [f"dep_{i}" for i in range(dep_count)]

        registry_path = _create_registry_yaml(
            artifact_id=artifact_id,
            deprecated_date=deprecated_date.isoformat(),
            sunset_date=sunset_date.isoformat(),
            replacement_artifact=replacement,
            deprecation_reason="Testing determinism",
            compatibility_impact="none",
            dependents=dependents,
        )

        try:
            # Evaluate phase twice with identical inputs
            gov1 = SunsetGovernance(
                registry_path=registry_path,
                reference_date=reference_date,
            )
            phase1 = gov1.evaluate_sunset_phase(artifact_id)
            blocked1 = gov1.is_sunset_blocked(artifact_id)
            generate1 = gov1.should_generate(artifact_id)
            warning1 = gov1.get_deprecation_warning(artifact_id)

            gov2 = SunsetGovernance(
                registry_path=registry_path,
                reference_date=reference_date,
            )
            phase2 = gov2.evaluate_sunset_phase(artifact_id)
            blocked2 = gov2.is_sunset_blocked(artifact_id)
            generate2 = gov2.should_generate(artifact_id)
            warning2 = gov2.get_deprecation_warning(artifact_id)

            # All results must be identical
            assert phase1 == phase2, (
                f"Phase evaluation not deterministic: {phase1} != {phase2}"
            )
            assert blocked1 == blocked2, (
                f"Sunset-blocked evaluation not deterministic: {blocked1} != {blocked2}"
            )
            assert generate1 == generate2, (
                f"Should-generate evaluation not deterministic: {generate1} != {generate2}"
            )
            assert warning1 == warning2, (
                f"Warning message not deterministic: '{warning1}' != '{warning2}'"
            )
        finally:
            Path(registry_path).unlink(missing_ok=True)

    @given(reference_date=date_strategy)
    @settings(max_examples=200)
    def test_not_deprecated_artifact_has_no_phase(
        self,
        reference_date: date,
    ) -> None:
        """Property 5: Artifacts without deprecated_date are NOT_DEPRECATED regardless of date.

        **Validates: Requirements 25.3, 25.4**

        An artifact that has never been deprecated should always evaluate
        to NOT_DEPRECATED, regardless of the reference date.
        """
        artifact_id = "active_artifact"

        registry_path = _create_registry_yaml(
            artifact_id=artifact_id,
            deprecated_date=None,
            sunset_date=None,
            replacement_artifact=None,
            deprecation_reason=None,
            compatibility_impact=None,
            dependents=[],
        )

        try:
            gov = SunsetGovernance(
                registry_path=registry_path,
                reference_date=reference_date,
            )
            phase = gov.evaluate_sunset_phase(artifact_id)

            assert phase == SunsetPhase.NOT_DEPRECATED, (
                f"Expected NOT_DEPRECATED for artifact without deprecated_date, got {phase}"
            )

            # Should still generate
            assert gov.should_generate(artifact_id) is True
            # No warning
            assert gov.get_deprecation_warning(artifact_id) is None
        finally:
            Path(registry_path).unlink(missing_ok=True)

    @given(reference_date=date_strategy)
    @settings(max_examples=200)
    def test_archived_artifact_is_always_archived(
        self,
        reference_date: date,
    ) -> None:
        """Property 6: Archived artifacts always evaluate to ARCHIVED phase.

        **Validates: Requirements 25.3, 25.4**

        An artifact with lifecycle_status='archived' should always be in
        the ARCHIVED phase regardless of dates or dependencies.
        """
        artifact_id = "archived_artifact"

        registry_path = _create_registry_yaml(
            artifact_id=artifact_id,
            deprecated_date="2024-01-01",
            sunset_date="2024-06-01",
            replacement_artifact="new_output",
            deprecation_reason="Fully replaced",
            compatibility_impact="breaking",
            lifecycle_status="archived",
            dependents=[],
        )

        try:
            gov = SunsetGovernance(
                registry_path=registry_path,
                reference_date=reference_date,
            )
            phase = gov.evaluate_sunset_phase(artifact_id)

            assert phase == SunsetPhase.ARCHIVED, (
                f"Expected ARCHIVED for archived artifact, got {phase}"
            )

            # Should NOT generate
            assert gov.should_generate(artifact_id) is False
        finally:
            Path(registry_path).unlink(missing_ok=True)
