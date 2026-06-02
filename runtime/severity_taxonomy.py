"""Severity Taxonomy — single canonical location for severity levels.

All governance-aware components import severity definitions from this module.
No other module may define severity levels independently.

Requirements: 17.1, 17.3, 17.5
"""

from enum import IntEnum


class Severity(IntEnum):
    """Canonical severity levels for governance events.

    Ordered by increasing impact. IntEnum allows direct comparison:
    Severity.WARNING < Severity.CRITICAL evaluates to True.
    """

    INFO = 0
    WARNING = 1
    DEGRADED = 2
    CRITICAL = 3
    CANONICAL_BREAK = 4
    DETERMINISTIC_FAILURE = 5


SEVERITY_DEFINITIONS: dict[Severity, dict] = {
    Severity.INFO: {
        "meaning": "Informational event, no action required",
        "blocks_pipeline_hard_mode": False,
        "triggers_audit_log": False,
        "appears_in_data_availability": False,
    },
    Severity.WARNING: {
        "meaning": "Non-critical issue detected, pipeline continues",
        "blocks_pipeline_hard_mode": False,
        "triggers_audit_log": True,
        "appears_in_data_availability": False,
    },
    Severity.DEGRADED: {
        "meaning": "Partial data loss, output quality reduced",
        "blocks_pipeline_hard_mode": False,
        "triggers_audit_log": True,
        "appears_in_data_availability": True,
    },
    Severity.CRITICAL: {
        "meaning": "Significant failure, section may be unavailable",
        "blocks_pipeline_hard_mode": True,
        "triggers_audit_log": True,
        "appears_in_data_availability": True,
    },
    Severity.CANONICAL_BREAK: {
        "meaning": "Chain integrity violated, canonical truth compromised",
        "blocks_pipeline_hard_mode": True,
        "triggers_audit_log": True,
        "appears_in_data_availability": True,
    },
    Severity.DETERMINISTIC_FAILURE: {
        "meaning": "Determinism guarantee broken, output not reproducible",
        "blocks_pipeline_hard_mode": True,
        "triggers_audit_log": True,
        "appears_in_data_availability": True,
    },
}
