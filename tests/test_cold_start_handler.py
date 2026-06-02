"""Unit tests for governance.cold_start_handler module.

Tests the simplified ColdStartHandler that detects missing governance state,
initializes minimal defaults, forces observability mode, and tags provenance
as bootstrap_derived.

Validates: Requirements 31.1, 31.2
"""

import os

import pytest
import yaml

from governance.actor_identity import ActorIdentity, ActorType
from governance.cold_start_handler import (
    ColdStartHandler,
    LedgerEntry,
    LEDGER_FILENAME,
)
from governance.state_provenance_tagger import GovernanceProvenance


@pytest.fixture
def tmp_domainization(tmp_path):
    """Create a temporary domainization directory."""
    return str(tmp_path / ".domainization")


@pytest.fixture
def handler(tmp_domainization):
    """Create a ColdStartHandler with a temporary directory."""
    return ColdStartHandler(tmp_domainization)


@pytest.fixture
def test_actor():
    """Create a test actor identity."""
    return ActorIdentity(
        actor_type=ActorType.SYSTEM,
        actor_id="cold_start_test",
        context={"source": "unit_test"},
        is_fallback=False,
    )


class TestIsColdStart:
    """Tests for ColdStartHandler.is_cold_start()."""

    def test_returns_true_when_no_ledger_file(self, handler):
        """Cold start detected when ledger file does not exist."""
        assert handler.is_cold_start() is True

    def test_returns_false_when_ledger_exists(self, handler, test_actor):
        """Not a cold start when ledger file exists."""
        handler.initialize(test_actor)
        assert handler.is_cold_start() is False

    def test_returns_true_when_directory_missing(self, tmp_path):
        """Cold start detected when entire domainization directory is missing."""
        nonexistent = str(tmp_path / "nonexistent" / ".domainization")
        handler = ColdStartHandler(nonexistent)
        assert handler.is_cold_start() is True

    def test_returns_true_when_directory_exists_but_no_ledger(self, tmp_domainization):
        """Cold start detected when directory exists but ledger file is absent."""
        os.makedirs(tmp_domainization, exist_ok=True)
        handler = ColdStartHandler(tmp_domainization)
        assert handler.is_cold_start() is True


class TestInitialize:
    """Tests for ColdStartHandler.initialize()."""

    def test_returns_ledger_entry(self, handler, test_actor):
        """Initialize returns a LedgerEntry instance."""
        entry = handler.initialize(test_actor)
        assert isinstance(entry, LedgerEntry)

    def test_entry_has_governance_event_type(self, handler, test_actor):
        """Bootstrap entry has GOVERNANCE_EVENT event type."""
        entry = handler.initialize(test_actor)
        assert entry.event_type == "GOVERNANCE_EVENT"

    def test_entry_has_info_severity(self, handler, test_actor):
        """Bootstrap entry has INFO severity."""
        entry = handler.initialize(test_actor)
        assert entry.severity == "INFO"

    def test_entry_has_bootstrap_provenance(self, handler, test_actor):
        """Bootstrap entry details include bootstrap_derived provenance."""
        entry = handler.initialize(test_actor)
        assert entry.details["provenance"] == "bootstrap_derived"

    def test_entry_forces_observability_mode(self, handler, test_actor):
        """Bootstrap entry details indicate observability enforcement mode."""
        entry = handler.initialize(test_actor)
        assert entry.details["enforcement_mode"] == "observability"

    def test_entry_contains_actor_dict(self, handler, test_actor):
        """Bootstrap entry contains serialized actor identity."""
        entry = handler.initialize(test_actor)
        assert entry.actor["actor_type"] == "SYSTEM"
        assert entry.actor["actor_id"] == "cold_start_test"
        assert entry.actor["context"] == {"source": "unit_test"}

    def test_entry_has_uuid_entry_id(self, handler, test_actor):
        """Bootstrap entry has a valid UUID entry_id."""
        import uuid

        entry = handler.initialize(test_actor)
        uuid.UUID(entry.entry_id)

    def test_entry_has_iso_timestamp(self, handler, test_actor):
        """Bootstrap entry has an ISO 8601 timestamp."""
        from datetime import datetime

        entry = handler.initialize(test_actor)
        datetime.fromisoformat(entry.timestamp)

    def test_creates_ledger_file(self, handler, test_actor):
        """Initialize creates the ledger file on disk."""
        handler.initialize(test_actor)
        assert os.path.isfile(handler.ledger_path)

    def test_creates_domainization_directory(self, handler, test_actor):
        """Initialize creates the domainization directory if missing."""
        handler.initialize(test_actor)
        assert os.path.isdir(handler._domainization_path)

    def test_ledger_file_is_valid_yaml(self, handler, test_actor):
        """Created ledger file contains valid YAML."""
        handler.initialize(test_actor)
        with open(handler.ledger_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert data is not None
        assert "schema_version" in data
        assert "entries" in data

    def test_ledger_file_has_schema_version(self, handler, test_actor):
        """Ledger file includes schema_version field."""
        handler.initialize(test_actor)
        with open(handler.ledger_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert data["schema_version"] == "1.0.0"

    def test_ledger_file_has_one_bootstrap_entry(self, handler, test_actor):
        """Ledger file contains exactly one bootstrap entry."""
        handler.initialize(test_actor)
        with open(handler.ledger_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert len(data["entries"]) == 1
        assert data["entries"][0]["event_type"] == "GOVERNANCE_EVENT"


class TestForcedEnforcementMode:
    """Tests for cold-start enforcement mode forcing."""

    def test_forced_mode_is_observability(self, handler):
        """Cold-start forces observability mode."""
        assert handler.get_forced_enforcement_mode() == "observability"


class TestProvenance:
    """Tests for cold-start provenance tagging."""

    def test_provenance_is_bootstrap_derived(self, handler):
        """Cold-start provenance is bootstrap_derived."""
        assert handler.provenance == GovernanceProvenance.BOOTSTRAP_DERIVED


class TestLedgerEntryRoundTrip:
    """Tests for LedgerEntry serialization round-trip."""

    def test_to_dict_from_dict_roundtrip(self, handler, test_actor):
        """LedgerEntry survives to_dict/from_dict round-trip."""
        entry = handler.initialize(test_actor)
        entry_dict = entry.to_dict()
        restored = LedgerEntry.from_dict(entry_dict)
        assert restored.entry_id == entry.entry_id
        assert restored.event_type == entry.event_type
        assert restored.timestamp == entry.timestamp
        assert restored.actor == entry.actor
        assert restored.governance_policy_version == entry.governance_policy_version
        assert restored.severity == entry.severity
        assert restored.details == entry.details


class TestLedgerPath:
    """Tests for ledger path construction."""

    def test_ledger_path_includes_filename(self, handler):
        """Ledger path ends with the expected filename."""
        assert handler.ledger_path.endswith(LEDGER_FILENAME)

    def test_ledger_path_includes_domainization_dir(self, tmp_domainization):
        """Ledger path is within the domainization directory."""
        handler = ColdStartHandler(tmp_domainization)
        assert tmp_domainization in handler.ledger_path
