# Report-First Observability

## Overview

Report-first observability integrates the `ReportValueDetector` into the domainization validation pipeline, ensuring that all artifacts are assessed for their contribution to report quality. This operates in **WARNING mode only** — it never blocks commits or enforces decisions.

The system answers the core question for every artifact: **"How does this improve the report?"**

## Features

- **Report value detection in Observer 4** — `BoundaryAwarenessValidator.check_report_value()` assesses artifacts for report value justification
- **Missing report value warnings** — Artifacts without `report_value` metadata generate low-severity warnings
- **Infrastructure drift detection** — Infrastructure-heavy artifacts (DEPLOY, ARCH, CONFIG, RUNTIME) without report value are flagged
- **Speculative claim detection** — Justifications using words like "might", "could", "potentially" are flagged
- **Invalid category detection** — Report value categories not in the 10 allowed list are flagged
- **Report-value health score in health reports** — Coverage percentage, valid percentage, and infrastructure drift tracked
- **Category distribution tracking** — Shows which report value categories are most used

## Usage

### Check Report Value via Observer 4

```python
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from observer_boundary_awareness import BoundaryAwarenessValidator

registry = ArtifactRegistry()
domain_reg = DomainRegistry()
validator = BoundaryAwarenessValidator(registry, domain_reg)

# Check all registered artifacts
warnings = validator.check_report_value()

# Check specific artifact metadata dicts
artifact_dicts = [
    {
        "artifact_id": "my_feature",
        "file_path": "src/my_feature.py",
        "primary_domain": "SIGNALS",
        "artifact_type": "ENGINE",
        "report_value": {
            "category": "confidence_explanation",
            "justification": "Generates confidence signals for the PM report"
        }
    }
]
warnings = validator.check_report_value(artifact_dicts)
```

### Get Report-Value Health Score

```python
# From Observer 4
health_score = validator.get_report_value_health_score()
print(f"Valid: {health_score.valid_percentage:.1f}%")
print(f"Infrastructure drift: {health_score.infrastructure_drift_percentage:.1f}%")
```

### Health Report with Report-Value Section

```python
from health_reporter import HealthReporter

reporter = HealthReporter()
report = reporter.generate_health_report()

# Access report-value health score
rv_health = report['report_value_health']
print(f"Coverage: {rv_health['coverage_percentage']:.1f}%")
print(f"Valid: {rv_health['valid_percentage']:.1f}%")
print(f"Infrastructure Drift: {rv_health['infrastructure_drift_percentage']:.1f}%")

# Format as text (includes REPORT-VALUE HEALTH SCORE section)
text = reporter.format_report_text(report)
print(text)
```

## Warning Codes

| Code | Name | Severity | Description |
|------|------|----------|-------------|
| W600 | MISSING_REPORT_VALUE | low | Artifact has no report_value field |
| W601 | INVALID_REPORT_VALUE_CATEGORY | medium | Category not in allowed list |
| W602 | SPECULATIVE_REPORT_VALUE | medium | Justification uses speculative language |
| W603 | INFRASTRUCTURE_WITHOUT_REPORT_VALUE | medium | Infrastructure-heavy artifact lacks report value |

## Testing

Run integration tests:

```bash
cd .domainization/src
python -m pytest test_report_value_integration.py -v
```

Run all report-value related tests:

```bash
cd .domainization/src
python -m pytest test_report_value_detector.py test_report_value_integration.py -v
```

## Requirements Satisfied

| Requirement | Description | Implementation |
|-------------|-------------|----------------|
| 12.1 | New features answer "How does this improve the report?" | `check_report_value()` generates W600 warning |
| 12.2 | No report value → feature deferred | W600 warning with deferral suggestion |
| 12.8 | Infrastructure without report value → deferred | W603 warning for infra-heavy artifacts |
| 12.9 | Governance without report quality → deferred | ARCH/STEERING artifacts flagged as infrastructure |
| 12.10 | Report value precedence over architectural elegance | W603 warning mentions precedence |

## Related Files

- `report_value_detector.py` — Core detection framework (created in task 17.1)
- `observer_boundary_awareness.py` — Observer 4 with `check_report_value()` method
- `health_reporter.py` — Health reports with report-value health score section
- `validation_result.py` — Warning codes W600-W604
- `test_report_value_integration.py` — Integration tests (19 tests)
- `test_report_value_detector.py` — Unit tests for detector (62 tests)

## Design Principles

1. **WARNING mode only** — Never blocks, never enforces, only informs
2. **Actionable suggestions** — Every warning includes guidance on resolution
3. **Non-intrusive** — Existing workflows continue unaffected
4. **Gradual awareness** — Health scores build visibility over time
5. **Report-first priority** — Report value takes precedence over architectural elegance
