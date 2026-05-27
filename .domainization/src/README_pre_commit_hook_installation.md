# Pre-Commit Hook Installation and Usage

## Overview

The domainization pre-commit hook is an **optional**, **non-blocking** developer tool that provides **observability** into governance compliance at commit time. It runs validation observers against staged files and displays warnings — but never prevents a commit from proceeding.

This document covers installation, testing, team usage, and the observability-only philosophy.

## Features

### Optional Installation
- Hook installation is entirely voluntary
- Developers choose whether to install it
- No team-wide enforcement or mandatory gates
- Can be installed/uninstalled at any time

### Observability Mode (Warnings Only)
- All validation output is informational
- Exit code is always 0 (commit proceeds)
- Warnings display governance suggestions
- No emergency bypass mechanism needed (nothing to bypass)

### Validation Observers
When the hook runs, it executes all 5 validation observers:

| Observer | What It Checks |
|----------|---------------|
| RegistrationValidator | Unregistered artifacts, missing metadata |
| DomainAssignmentValidator | Invalid domain assignments |
| LifecycleValidator | Invalid lifecycle transitions |
| BoundaryAwarenessValidator | Authority chain violations, cloud provider issues |
| SSOTConsistencyValidator | SSOT conflicts, missing references |

### Performance
- Target: < 5 seconds for validation
- Typical execution: 200-600ms for standard changesets
- Performance reported in hook output

## Usage

### Install the Hook

```bash
cd /path/to/portfolio_os_v1
bash .domainization/hooks/install_hook.sh
```

The script will:
1. Check for existing pre-commit hooks
2. Backup any existing hook (if present)
3. Copy the domainization hook to `.git/hooks/pre-commit`
4. Make it executable

### Check Hook Status

```bash
bash .domainization/hooks/install_hook.sh status
```

### Uninstall the Hook

```bash
bash .domainization/hooks/install_hook.sh uninstall
```

### Normal Commit Workflow

Once installed, the hook runs automatically on every `git commit`:

```bash
git add engines/new_engine.py
git commit -m "feat(signals): add new signal engine"
```


Example output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Domainization Observability Check
Mode: WARNINGS ONLY (commit will proceed regardless)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changed files:
  - engines/new_engine.py

Running validation observers...

════════════════════════════════════════════════════════════════════════════════
DOMAINIZATION OBSERVABILITY REPORT
════════════════════════════════════════════════════════════════════════════════
Mode: OBSERVABILITY (warnings only, no blocking)
Execution Time: 312.45ms
Performance Target (<5000ms): ✓ MET

Total Warnings: 1
  Critical: 0
  High: 1
  Medium: 0
  Low: 0

Warnings by Observer:
────────────────────────────────────────────────────────────────────────────────

RegistrationValidator: 1 warning(s)
  🟠 [RegistrationValidator] new_engine: Artifact not registered
    Suggestion: Add YAML frontmatter or register in artifact_registry.yaml

════════════════════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Observability check complete. Commit proceeding.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Skip the Hook (Optional)

Use `--no-verify` to skip the hook for any commit:

```bash
git commit -m "quick fix" --no-verify
```

No audit trail is needed for bypassing since the hook never blocks.

## Testing

### Run Hook Directly

You can test the hook without committing:

```bash
bash .git/hooks/pre-commit
```

This runs the hook against currently staged files and displays the observability report.

### Verify Hook Never Blocks

```bash
bash .git/hooks/pre-commit; echo "Exit code: $?"
# Always outputs: Exit code: 0
```

### Verify Installation Status

```bash
bash .domainization/hooks/install_hook.sh status
```

### Run Hook Integration Tests

```bash
.venv/bin/python -m pytest .domainization/src/test_integration_end_to_end.py -v -k "hook"
```

## Team Documentation

### For New Developers

1. **Installation is optional** — You can develop without the hook
2. **It never blocks** — Your commits always proceed regardless of warnings
3. **Warnings are educational** — They help you learn governance rules
4. **Bypass is free** — Use `--no-verify` anytime, no justification needed

### For Team Leads

- The hook builds governance awareness without friction
- Track warning patterns to identify common issues
- Use health reports (not hook output) for compliance metrics
- Do not mandate hook installation during FAST LANE phase

### When to Install

Install the hook if you want to:
- Learn domainization governance rules through immediate feedback
- See which artifacts need registration before code review
- Understand domain boundaries and lifecycle states
- Get suggestions for metadata improvements

### When to Skip

Skip the hook if you:
- Prefer to learn through code review feedback
- Are doing rapid prototyping
- Find the output distracting during focused work
- Are working on non-governed files

## Requirements Satisfied

| Requirement | Description | How Satisfied |
|-------------|-------------|---------------|
| 5.1 | Commit validation gates execute in sequence | Hook runs all 5 observers via ValidationOrchestrator |
| 5.9 | Commit gates deferred until MVP stabilizes | Hook operates in observability mode only (warnings, never blocks) |
| 5.10 | Governance shall not block report development | Hook always exits 0; commit proceeds regardless of warnings |

## Related Files

- `.domainization/hooks/pre-commit` — The hook script itself
- `.domainization/hooks/install_hook.sh` — Installation/uninstallation script
- `.domainization/hooks/README_optional_pre_commit_hook.md` — Detailed hook documentation
- `.domainization/src/validation_orchestrator.py` — Validation engine called by the hook
- `.domainization/config.yaml` — Enforcement mode configuration
- `.domainization/src/README_observability_mode_configuration.md` — Observability mode docs
