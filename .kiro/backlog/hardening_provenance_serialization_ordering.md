# Hardening: Provenance Serialization Ordering Instability

**Priority:** MEDIUM  
**Category:** governance/provenance-integrity  
**Owner:** System Architect  
**Created:** 2026-05-27  
**Status:** OPEN  

## Problem

`tests/test_property_provenance_parseability.py::test_round_trip_yaml_preserves_field_values` fails because YAML serialization sorts list elements alphabetically during round-trip. Input `['1', '0']` becomes `['0', '1']` after serialize → parse.

This is currently the ONLY failing test in the entire suite (1/447).

## Why This Matters

Serialization instability in provenance data can cause:
- **Audit drift:** Two identical provenance blocks produce different YAML bytes
- **Provenance inconsistency:** Diff tools report false changes
- **False diffs:** CI/CD pipelines flag unchanged provenance as modified
- **Determinism violation:** Same inputs → different serialized outputs (violates Req 15.1)

## Root Cause

`governance/provenance_schema.py` uses `yaml.dump()` which sorts sequences. The `SectionProvenance.to_yaml()` method does not preserve insertion order for list fields (`reasoning_object_ids`, `semantic_state_ids`, `signal_engine_ids`).

## Required Fix

1. Use `yaml.dump(..., default_flow_style=False, sort_keys=False)` — but this only affects dict keys, not list ordering
2. The real issue: YAML round-trip through `yaml.safe_load()` preserves list order, but the test may be comparing against a re-sorted version
3. Investigate whether the serialization or the test assertion is wrong
4. Fix whichever is incorrect to ensure: serialize(data) → parse → data == original

## Acceptance Criteria

- [ ] `test_round_trip_yaml_preserves_field_values` passes
- [ ] List ordering is preserved through serialize → parse round-trip
- [ ] No other tests regress
- [ ] Determinism property (Req 15.1) explicitly verified for provenance serialization

## Classification

- NOT a permanent tolerated failure
- MUST be resolved before Phase D completion
- Blocks full determinism verification
