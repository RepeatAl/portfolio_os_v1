# Hardening: Semantic Engine Unit Test Coverage

**Priority:** HIGH  
**Category:** test/quality  
**Owner:** Quality Engineer  
**Created:** 2026-05-27  
**Status:** OPEN  

## Problem

`engines/semantic_engine.py` has only 16% test coverage from unit tests. Property tests cover behavior indirectly via the pipeline orchestrator, but the emission logic in `interpret_narrative_dependency_signals()` lacks explicit deterministic unit tests with controlled DataFrame fixtures.

Relying solely on property tests for semantic-state emission logic is dangerous because:
- Property tests exercise the function through the orchestrator (indirect)
- Threshold logic (>20%, >15%) is not explicitly boundary-tested
- DataFrame edge cases (empty, single row, mixed categories) are not covered
- Regression detection is slower through property tests than unit tests

## Target

`engines/semantic_engine.py` coverage > 75%

## Required Work

1. Create `engines/test_semantic_engine_emission.py`
2. Test `interpret_narrative_dependency_signals()` with controlled DataFrames:
   - Semiconductor allocation at boundary (19%, 20%, 21%)
   - Energy allocation at boundary (14%, 15%, 16%)
   - Datacenter allocation at boundary (14%, 15%, 16%)
   - Empty DataFrame (zero rows)
   - Single category DataFrame
   - Multiple categories summing above threshold
   - Category name variations (e.g., "Semiconductor" vs "Semiconductors")
3. Test `interpret_allocation_signals()` with controlled DataFrames:
   - Defense > 25% threshold
   - Semiconductor > 25% threshold
   - Concentration > 25% threshold
4. Test `get_registry_entry()`, `get_all_registry_entries()`, `get_protected_state_ids()`, `get_new_state_ids()`

## Acceptance Criteria

- [ ] Coverage of `engines/semantic_engine.py` > 75%
- [ ] All threshold boundaries explicitly tested
- [ ] Empty/edge-case DataFrames tested
- [ ] No reliance on property tests for emission logic validation
