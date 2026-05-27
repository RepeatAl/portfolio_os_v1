# Report Value Detection Framework

## Overview

The Report Value Detection Framework validates that artifacts have proper report value justification. It enforces the "report-first" principle: every feature must answer "How does this improve the report?" before being accepted.

All detection operates in **WARNING mode only** — no blocking, no enforcement. This is an observability tool that generates visibility into report-value coverage.

## Features

- **10 Allowed Report Value Categories** (Requirement 12.5)
- **Speculative/Indirect Claim Detection** (Requirement 12.4)
- **Infrastructure-Heavy Artifact Detection** (Requirement 12.7)
- **Report-Value Health Score Generation**
- **Missing Report Value Identification** (Requirement 12.2)

## Allowed Report Value Categories

The following 10 categories are the only valid report value justifications:

| Category | Description |
|----------|-------------|
| `semantic_interpretation` | Improves semantic meaning extraction for the report |
| `pm_reasoning` | Enhances PM-level reasoning in the report |
| `concentration_explanation` | Explains portfolio concentration in the report |
| `dependency_explanation` | Explains asset dependencies in the report |
| `scenario_interpretation` | Interprets scenarios for the report |
| `confidence_explanation` | Explains confidence levels in the report |
| `action_space_clarity` | Clarifies available actions in the report |
| `multilingual_rendering` | Improves multilingual report rendering |
| `traceability` | Enhances signal-to-report traceability |
| `user_understanding` | Improves user comprehension of the report |

## Usage

### Basic Assessment

```python
from report_value_detector import ReportValueDetector

detector = ReportValueDetector()

# Assess a single artifact
artifact = {
    "artifact_id": "report_engine_py",
    "file_path": "engines/report_engine.py",
    "primary_domain": "REPORT",
    "artifact_type": "ENGINE",
    "report_value": {
        "category": "pm_reasoning",
        "justification": "Generates PM reasoning section in the portfolio report"
    }
}

assessment = detector.assess_artifact(artifact)
print(assessment.is_valid)    # True
print(assessment.summary())   # "Valid report value: pm_reasoning for report_engine_py"
```

### Health Score Generation

```python
artifacts = [...]  # List of artifact metadata dicts
score = detector.generate_health_score(artifacts)

print(f"Coverage: {score.coverage_percentage:.1f}%")
print(f"Valid: {score.valid_percentage:.1f}%")
print(f"Infrastructure drift: {score.infrastructure_drift_percentage:.1f}%")
print(score.summary())
```

### Detect Missing Report Value

```python
missing = detector.detect_missing_report_value(artifacts)
for artifact in missing:
    print(f"Missing report value: {artifact['artifact_id']}")
```

### Detect Infrastructure Without Report Value

```python
infra = detector.detect_infrastructure_without_report_value(artifacts)
for artifact in infra:
    print(f"Infrastructure drift: {artifact['artifact_id']}")
```

### Category Validation

```python
# Check if a category is valid
detector.is_valid_category("pm_reasoning")           # True
detector.is_valid_category("performance_tuning")     # False

# Get all allowed categories
categories = detector.get_allowed_categories()       # List of 10 categories
```

## Speculative Claim Detection

The detector identifies speculative or indirect justifications using keyword matching. The following phrases trigger speculative detection:

- "might improve", "could help", "potentially"
- "in the future", "eventually", "indirectly"
- "may contribute", "possibly", "theoretically"
- "long-term", "someday", "aspirational"

**Example of speculative claim (rejected):**
```yaml
report_value:
  category: traceability
  justification: "This might improve report generation speed in the future"
```

**Example of direct claim (accepted):**
```yaml
report_value:
  category: pm_reasoning
  justification: "Generates the PM reasoning paragraph in the daily report"
```

## Infrastructure Detection

Artifacts are flagged as infrastructure-heavy based on:

- **Domain**: `DEPLOY` or `ARCH` primary domain
- **Artifact type**: `CONFIG`, `RUNTIME`, or `STEERING`
- **File path**: Contains infrastructure keywords (e.g., `infrastructure/`, `deployment/`)
- **Description**: Contains infrastructure keywords (e.g., "load balancing", "caching")

Infrastructure-heavy artifacts without valid report value are flagged for review.

## Testing

Run the unit tests:

```bash
.venv/bin/python -m pytest .domainization/src/test_report_value_detector.py -v
```

Test coverage includes:
- All 10 allowed categories validation
- Speculative keyword detection (case-insensitive)
- Infrastructure-heavy artifact detection
- Health score calculation (coverage, valid, drift percentages)
- Edge cases (empty dicts, None values, invalid formats)

## Requirements Satisfied

| Requirement | Description | Implementation |
|-------------|-------------|----------------|
| 12.1 | Feature must answer "How does this improve the report?" | `assess_artifact()` checks for report_value field |
| 12.2 | No report value → feature deferred | `detect_missing_report_value()` identifies gaps |
| 12.3 | Report value must be measurable and direct | Speculative detection rejects indirect claims |
| 12.4 | Speculative/indirect → rejected | `_is_speculative_claim()` keyword matching |
| 12.5 | 10 allowed categories defined | `ALLOWED_REPORT_VALUE_CATEGORIES` constant |
| 12.6 | Report domain has veto authority | Framework provides data for veto decisions |
| 12.7 | Complexity without report benefit → rejected | `detect_infrastructure_without_report_value()` |

## Related Files

- `report_value_detector.py` — Main detection framework
- `test_report_value_detector.py` — Unit tests (62 tests)
- `validation_result.py` — Warning codes W600-W604
- `observer_boundary_awareness.py` — Integration point for observer pipeline
