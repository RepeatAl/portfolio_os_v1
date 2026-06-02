# Domainization Pre-Commit Hook

## Overview

The domainization pre-commit hook is an **OPTIONAL** developer tool that provides **OBSERVABILITY** into domainization governance. It runs automatically before each commit and displays warnings about potential governance violations.

## Key Characteristics

### ✅ Optional
- Installation is completely optional
- Not required for development
- Can be installed or uninstalled at any time

### ✅ Non-Blocking
- **NEVER blocks commits**
- Always exits with success (exit code 0)
- Displays warnings but allows commit to proceed
- No emergency bypass needed

### ✅ Observability Mode
- Shows governance warnings and suggestions
- Helps developers understand domainization rules
- Provides actionable guidance
- Builds awareness without friction

## Installation

### Install the Hook

```bash
cd .domainization/hooks
./install_hook.sh
```

The installation script will:
1. Check if a pre-commit hook already exists
2. Backup any existing hook (if present)
3. Install the domainization hook
4. Make it executable
5. Display usage information

### Check Hook Status

```bash
cd .domainization/hooks
./install_hook.sh status
```

### Uninstall the Hook

```bash
cd .domainization/hooks
./install_hook.sh uninstall
```

The uninstallation script will:
1. Remove the domainization hook
2. Offer to restore any backed-up hook
3. Clean up safely

## Usage

### Normal Commits

Once installed, the hook runs automatically:

```bash
git add file.py
git commit -m "feat(signals): add new signal calculation"
```

Output example:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Domainization Observability Check
Mode: WARNINGS ONLY (commit will proceed regardless)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changed files:
  - engines/new_signal_engine.py

Running validation observers...

════════════════════════════════════════════════════════════════════════════════
DOMAINIZATION OBSERVABILITY REPORT
════════════════════════════════════════════════════════════════════════════════
Mode: OBSERVABILITY (warnings only, no blocking)
Execution Time: 234.56ms
Performance Target (<5000ms): ✓ MET

Total Warnings: 1
  Critical: 0
  High: 1
  Medium: 0
  Low: 0

Warnings by Observer:
────────────────────────────────────────────────────────────────────────────────

RegistrationValidator: 1 warning(s)
  [HIGH] Artifact 'engines/new_signal_engine.py' is not registered
    Suggestion: Add YAML frontmatter or register in artifact_registry.yaml
    
════════════════════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Observability check complete. Commit proceeding.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[main abc1234] feat(signals): add new signal calculation
 1 file changed, 10 insertions(+)
```

### Bypass Hook (Optional)

You can skip the hook entirely using `--no-verify`:

```bash
git commit -m "quick fix" --no-verify
```

**Note:** No audit trail is needed for bypassing since the hook never blocks commits anyway.

## What the Hook Does

### 1. Detects Changed Files
- Scans git staging area for files to be committed
- Identifies new, modified, or renamed files
- Passes file list to validation orchestrator

### 2. Runs Validation Observers
The hook runs all 5 validation observers:

1. **RegistrationValidator** - Checks if artifacts are registered
2. **DomainAssignmentValidator** - Validates domain assignments
3. **LifecycleValidator** - Checks lifecycle state transitions
4. **BoundaryAwarenessValidator** - Enforces domain boundaries
5. **SSOTConsistencyValidator** - Prevents SSOT conflicts

### 3. Displays Warnings
- Shows warnings grouped by observer
- Includes severity levels (critical, high, medium, low)
- Provides actionable suggestions
- Reports execution time

### 4. Always Proceeds
- Never blocks the commit
- Always exits with success
- Commit proceeds regardless of warnings

## Benefits

### For Developers
- **Learn governance rules** through warnings
- **Get immediate feedback** on potential issues
- **Understand domain boundaries** before code review
- **No workflow disruption** (never blocks)

### For Teams
- **Build awareness** of domainization principles
- **Reduce governance violations** over time
- **Improve code quality** through early feedback
- **Maintain velocity** (no blocking friction)

### For the System
- **Track violations** for health reporting
- **Identify patterns** in governance issues
- **Measure adoption** of domainization
- **Guide enforcement** decisions

## Technical Details

### Requirements
- Git repository
- Python 3.7+
- Domainization system installed (`.domainization/` directory)
- Validation modules in `.domainization/src/`

### Performance
- Target: < 5 seconds for validation
- Typical: 200-500ms for small changesets
- Scales to 1000+ artifacts

### Error Handling
- Gracefully handles missing domainization system
- Skips validation if Python modules unavailable
- Never fails the commit due to validation errors
- Logs errors but proceeds

## Troubleshooting

### Hook Not Running

Check if hook is installed:
```bash
ls -la .git/hooks/pre-commit
```

If not present, install it:
```bash
cd .domainization/hooks
./install_hook.sh
```

### Hook Shows Errors

The hook is designed to handle errors gracefully. If you see errors:

1. Check that domainization system exists:
   ```bash
   ls -la .domainization/
   ```

2. Check that Python modules exist:
   ```bash
   ls -la .domainization/src/
   ```

3. Check that registries exist:
   ```bash
   ls -la .domainization/*.yaml
   ```

If any are missing, the hook will skip validation and allow the commit.

### Hook is Slow

If the hook takes > 5 seconds:

1. Check the observability report for execution time
2. Review the number of artifacts being validated
3. Consider using `--no-verify` for quick commits
4. Report performance issues to the team

### Want to Disable Temporarily

Use `--no-verify` for individual commits:
```bash
git commit -m "quick fix" --no-verify
```

Or uninstall the hook:
```bash
cd .domainization/hooks
./install_hook.sh uninstall
```

## Philosophy

### Why Optional?

The hook is optional because:
- **FAST LANE phase** prioritizes velocity over governance
- **Learning curve** varies by developer
- **Workflow preferences** differ across teams
- **Trust over enforcement** builds better culture

### Why Non-Blocking?

The hook never blocks because:
- **Observability first** - visibility before enforcement
- **Report value** - governance supports, doesn't hinder
- **Gradual adoption** - warnings build awareness
- **Developer trust** - no surprise blockers

### Why Observability Mode?

Observability mode means:
- **Warnings, not errors** - informative, not punitive
- **Suggestions, not mandates** - helpful, not prescriptive
- **Awareness, not enforcement** - educational, not restrictive
- **Support, not friction** - enabling, not blocking

## Future Evolution

### Current Phase: FAST LANE REPORT MVP
- Hook is optional
- All validation is warnings only
- No commit blocking
- Focus on building awareness

### Future Phase: Post-MVP Stabilization
- Hook may become recommended (still optional)
- Some validations may become blocking
- Critical violations may prevent commits
- Gradual hardening based on team readiness

### Transition Strategy
- Clear communication before any changes
- Opt-in period for blocking mode
- Emergency bypass mechanisms
- Team feedback drives timeline

## Related Documentation

- **Validation Observers**: `.domainization/src/README_validation_observers.md`
- **Registry Layer**: `.domainization/src/README_registry_layer_python_api.md`
- **Health Reporting**: `.domainization/src/README_reporting_layer.md`
- **Domain Boundaries**: `.domainization/domain_registry.yaml`
- **Lifecycle States**: `.domainization/lifecycle_state_machine.yaml`

## Support

If you have questions or issues:

1. Check this documentation
2. Review the observability report output
3. Check the validation observer documentation
4. Ask the team in #domainization channel
5. File an issue in the repository

## Summary

The domainization pre-commit hook is an **optional**, **non-blocking** tool that provides **observability** into governance. It helps developers understand domainization rules through warnings and suggestions, without disrupting workflow or blocking commits.

**Install it if you want governance feedback. Skip it if you prefer to learn through code review. Either way, your commits will always proceed.**
