# Acceptance Test Scenarios

## Overview

BDD-style acceptance tests using Gherkin format (Given/When/Then) that validate the domainization system works correctly from a user perspective. These tests cover real-world scenarios that developers encounter when working with the system.

## Features

- **Gherkin-style BDD format**: Each test uses Given/When/Then structure in docstrings
- **4 scenario groups**: New developer workflow, invalid domain assignment, SSOT conflict, gradual migration
- **20 acceptance tests**: Comprehensive coverage of user-facing behavior
- **End-to-end validation**: Tests exercise multiple components together
- **Performance verification**: Validates system meets <5 second target

## Scenarios

### Scenario 1: New Developer Adding a Feature

Tests the complete workflow a new developer follows when adding a feature:
- Creating an unregistered file triggers a warning
- Properly registering an artifact succeeds without errors
- Progressing through lifecycle states is validated
- Invalid lifecycle transitions are rejected with guidance
- Full workflow completes within performance target

### Scenario 2: Invalid Domain Assignment

Tests that the system detects and reports invalid domain assignments:
- ENGINE assigned to GOV domain (cannot own ENGINE)
- REPORT_OUT assigned to SIGNALS domain (cannot own REPORT_OUT)
- Assignment to nonexistent domain
- Validation orchestrator detects invalid assignments in registry
- Valid assignments produce no warnings

### Scenario 3: SSOT Conflict Detection

Tests that the system prevents multiple canonical SSOTs for the same topic:
- Duplicate canonical SSOT for same topic is detected
- Derived documents without canonical reference are flagged
- Properly linked derived documents produce no warnings
- Conflict warnings provide actionable resolution suggestions

### Scenario 4: Gradual Migration Support

Tests that the system supports incremental adoption:
- Unregistered artifacts are allowed during migration (warnings only)
- Incremental registration reduces warning count
- Existing files remain in current locations (no forced moves)
- Migration phases can be validated independently
- Validation is deterministic across multiple runs
- Health report tracks migration progress

## Usage

```bash
# Run all acceptance tests
cd .domainization/src
python -m pytest test_acceptance_scenarios.py -v

# Run a specific scenario group
python -m pytest test_acceptance_scenarios.py::TestScenarioNewDeveloperAddingFeature -v
python -m pytest test_acceptance_scenarios.py::TestScenarioInvalidDomainAssignment -v
python -m pytest test_acceptance_scenarios.py::TestScenarioSSOTConflict -v
python -m pytest test_acceptance_scenarios.py::TestScenarioGradualMigration -v
```

## Testing

```bash
# Run with coverage
python -m pytest test_acceptance_scenarios.py --cov=. --cov-report=term-missing -v

# Run with timing information
python -m pytest test_acceptance_scenarios.py -v --durations=10
```

## Requirements Satisfied

| Requirement | Description | Coverage |
|-------------|-------------|----------|
| 15.1 | Commit gates execute in <5 seconds | Performance assertions in workflow tests |
| 15.2 | Registry supports 1000+ artifacts | Tested via domain assignment and registration |
| 15.3 | Health reports complete in <10 seconds | Health report generation test |
| 15.5 | Deterministic validation results | Determinism test with 3 consecutive runs |

## Related Files

- `test_acceptance_scenarios.py` - The acceptance test implementation
- `validation_orchestrator.py` - Orchestrator tested in end-to-end scenarios
- `artifact_registry.py` - Registry operations tested in developer workflow
- `domain_registry.py` - Domain validation tested in assignment scenarios
- `lifecycle_manager.py` - Lifecycle transitions tested in developer workflow
- `observer_ssot_consistency.py` - SSOT conflict detection tested
- `observer_registration.py` - Registration detection tested
- `observer_domain_assignment.py` - Domain assignment validation tested
- `health_reporter.py` - Health reporting tested in migration scenario
