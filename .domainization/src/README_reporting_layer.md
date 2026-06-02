# Reporting Layer Documentation

## Overview

The reporting layer provides health monitoring and violation detection for the domainization system. It consists of two main components:

1. **Health Reporter** - Generates comprehensive health reports showing system status
2. **Violation Detector** - Detects governance violations and provides actionable recommendations

## Components

### Health Reporter (`health_reporter.py`)

The `HealthReporter` class generates comprehensive health reports that include:

- **Summary Statistics**
  - Total artifacts
  - Registration coverage
  - Domain distribution
  - Lifecycle distribution
  - Violation counts by severity

- **Domain Coverage**
  - Artifact count per domain
  - Breakdown by artifact type
  - Core vs surface domain distribution

- **Lifecycle Distribution**
  - Artifact count per lifecycle state
  - Distribution by artifact type

- **Violations** (optional)
  - All detected violations with severity levels
  - Grouped by type and severity
  - Actionable recommendations

#### Usage

```python
from health_reporter import HealthReporter

# Create reporter (uses default registries)
reporter = HealthReporter()

# Generate health report with violations
report = reporter.generate_health_report(include_violations=True)

# Save report to YAML
reporter.save_report(report, Path("health_report.yaml"))

# Format as human-readable text
text = reporter.format_report_text(report)
print(text)
```

#### Report Structure

```yaml
report_date: "2026-05-25"
report_time: "14:30:00"
report_version: "1.0"
enforcement_mode: "observability"

summary:
  total_artifacts: 150
  registered_artifacts: 150
  registration_percentage: 100.0
  total_domains: 12
  domains_with_artifacts: 8
  total_violations: 5
  violations_by_severity:
    critical: 2
    high: 1
    medium: 2
    low: 0

domain_coverage:
  - domain_id: "SIGNALS"
    domain_name: "Signal Generation"
    priority: "core"
    artifact_count: 45
    artifact_types:
      - type: "SSOT"
        count: 12
      - type: "ENGINE"
        count: 33

lifecycle_distribution:
  - artifact_type: "SSOT"
    total_count: 35
    states:
      - state: "canonical"
        count: 28
      - state: "draft"
        count: 5
      - state: "deprecated"
        count: 2

violations:
  - artifact_id: "test_ssot_1"
    file_path: "docs/test1.md"
    violation_type: "ssot_conflict"
    severity: "critical"
    description: "Multiple canonical SSOTs for topic 'test_topic'"
    recommendation: "Mark one as canonical, others as derived"

recommendations:
  - priority: "high"
    action: "Resolve 2 SSOT conflict(s)"
    rationale: "Multiple canonical SSOTs create ambiguity about authoritative source"
```

### Violation Detector (`violation_detector.py`)

The `ViolationDetector` class detects governance violations:

#### Violation Types

1. **Unregistered Artifacts** (`unregistered`)
   - Severity: High
   - Files that should be registered but aren't
   - Scans: `docs/`, `engines/`, `reports/`, `data/`

2. **Missing Lifecycle Status** (`missing_lifecycle`)
   - Severity: Medium
   - Artifacts with empty or invalid lifecycle status

3. **SSOT Conflicts** (`ssot_conflict`)
   - Severity: Critical
   - Multiple canonical SSOTs for the same topic

4. **Missing SSOT Reference** (`missing_ssot_reference`)
   - Severity: High
   - Derived/implementation artifacts without SSOT dependencies

5. **Deprecated Modifications** (`deprecated_modification`)
   - Severity: High
   - Recently modified deprecated artifacts

#### Usage

```python
from violation_detector import ViolationDetector

# Create detector (uses default registries)
detector = ViolationDetector()

# Detect all violations
violations = detector.detect_all_violations()

# Group by severity
by_severity = detector.get_violations_by_severity(violations)
print(f"Critical: {len(by_severity.get('critical', []))}")

# Group by type
by_type = detector.get_violations_by_type(violations)
print(f"SSOT conflicts: {len(by_type.get('ssot_conflict', []))}")

# Format as text
text = detector.format_violations_text(violations)
print(text)
```

#### Violation Object

```python
class Violation:
    artifact_id: Optional[str]  # None if unregistered
    file_path: str
    violation_type: str
    severity: str  # "critical" | "high" | "medium" | "low"
    description: str
    recommendation: str
```

## Integration

The health reporter and violation detector are integrated:

```python
from health_reporter import HealthReporter
from violation_detector import ViolationDetector

# Create shared registries
artifact_registry = ArtifactRegistry()
domain_registry = DomainRegistry()
lifecycle_manager = LifecycleManager()

# Create detector
detector = ViolationDetector(
    artifact_registry=artifact_registry,
    domain_registry=domain_registry,
    lifecycle_manager=lifecycle_manager
)

# Create reporter with detector
reporter = HealthReporter(
    artifact_registry=artifact_registry,
    domain_registry=domain_registry,
    lifecycle_manager=lifecycle_manager,
    violation_detector=detector
)

# Generate comprehensive report
report = reporter.generate_health_report(include_violations=True)
```

## Performance

### Targets

- Health report generation: < 10 seconds for 1000 artifacts
- Violation detection: < 5 seconds for 1000 artifacts

### Optimization

The reporting layer is optimized for performance:

1. **Lazy Loading** - Registries loaded only when needed
2. **Efficient Queries** - Uses registry query methods
3. **Minimal File I/O** - Only scans when detecting unregistered artifacts
4. **Caching** - Registries cached after first load

## Testing

Comprehensive test coverage:

- `test_health_reporter.py` - Health reporter unit tests (7 tests)
- `test_violation_detector.py` - Violation detector unit tests (10 tests)
- `test_health_reporter_with_violations.py` - Integration tests (6 tests)

Run tests:

```bash
pytest .domainization/src/test_health_reporter.py -v
pytest .domainization/src/test_violation_detector.py -v
pytest .domainization/src/test_health_reporter_with_violations.py -v
```

## Observability Mode

During the FAST LANE REPORT MVP phase, the reporting layer operates in **observability mode**:

- Violations are detected and reported
- No blocking or enforcement
- Warnings only, commits always proceed
- Builds visibility without friction

This aligns with the governance principle: "A visible unhealthy system is preferable to an invisible blocked system during FAST LANE phase."

## Future Enhancements

Planned improvements:

1. **Trend Analysis** - Track violations over time
2. **Custom Violation Rules** - User-defined violation patterns
3. **Automated Fixes** - Suggest or apply automatic fixes
4. **Dashboard Integration** - Visual health dashboard
5. **Notification System** - Alert on critical violations
6. **Performance Metrics** - Track report generation time

## Requirements Satisfied

This implementation satisfies the following requirements:

- **10.1** - Health report shows total, registered, and unregistered artifacts
- **10.2** - Domain coverage with artifact counts per domain
- **10.3** - Lifecycle distribution across all artifact types
- **10.4** - Violations listed with severity levels
- **10.5** - Actionable recommendations for violations
- **10.6** - Report includes timestamp and version
- **10.7** - Healthy system shows 100% registration and zero violations
- **15.3** - Performance target < 10 seconds for 1000 artifacts

## Examples

### Generate and Save Report

```python
from health_reporter import HealthReporter
from pathlib import Path

reporter = HealthReporter()
report = reporter.generate_health_report(include_violations=True)

# Save as YAML
yaml_path = reporter.save_report(report)
print(f"Report saved to: {yaml_path}")

# Save as text
text = reporter.format_report_text(report)
text_path = Path(".domainization/reports/health_report.txt")
text_path.write_text(text)
```

### Detect Specific Violations

```python
from violation_detector import ViolationDetector

detector = ViolationDetector()

# Detect only SSOT conflicts
violations = detector.detect_ssot_conflicts()
for v in violations:
    print(f"{v.severity.upper()}: {v.description}")
    print(f"  → {v.recommendation}")

# Detect only missing lifecycle
violations = detector.detect_missing_lifecycle_status()
print(f"Found {len(violations)} artifacts with missing lifecycle status")
```

### Custom Violation Filtering

```python
from violation_detector import ViolationDetector

detector = ViolationDetector()
violations = detector.detect_all_violations()

# Get only critical violations
critical = [v for v in violations if v.severity == 'critical']
print(f"Critical violations: {len(critical)}")

# Get violations for specific artifact
artifact_violations = [v for v in violations if v.artifact_id == 'my_artifact']
for v in artifact_violations:
    print(v)
```

## See Also

- [Registry Layer Documentation](README_registry_layer_python_api.md)
- [Validation Observers Documentation](README_validation_observers.md)
- [Design Document](../.kiro/specs/domainization/design.md)
- [Requirements Document](../.kiro/specs/domainization/requirements.md)
