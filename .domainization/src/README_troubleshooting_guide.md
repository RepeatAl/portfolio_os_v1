# Troubleshooting Guide

## Overview

This guide helps resolve common validation errors in the domainization system. All validation currently operates in **OBSERVABILITY MODE** — warnings are displayed but commits are never blocked. Use this guide to understand what warnings mean and how to resolve them proactively.

## Current System Mode

| Setting | Value |
|---------|-------|
| Enforcement Mode | OBSERVABILITY (warnings only) |
| Pre-commit Hook | Optional, never blocks |
| Commit Blocking | Disabled |
| Audit Logging | Active |

**Key Point**: No commit will ever be blocked during the FAST LANE phase. All errors appear as warnings for visibility only.

---

## Validation Error Codes Reference

### E001: Artifact Not Registered

**Severity**: HIGH  
**Gate**: Gate 1 (Artifact Registration)  
**Description**: A file was created or modified but has no metadata in the domainization system.

**Symptoms**:
```
🟠 [E001] Gate 1: Artifact Registration (WARNING)
  Artifact: docs/my_new_file.md
  Error:    Artifact 'docs/my_new_file.md' is not registered in the domainization system
```

**Resolution**:

1. **For markdown files** — Add YAML frontmatter at the top of the file:
   ```yaml
   ---
   artifact_id: my_new_file_md
   primary_domain: ARCH
   artifact_type: SSOT
   lifecycle_status: draft
   created_date: "2025-01-01"
   last_modified: "2025-01-01"
   owner_role: "System Architect"
   ssot_relationship: canonical
   allowed_writers: ["ARCH"]
   allowed_readers: ["ALL"]
   ---
   ```

2. **For non-markdown files** — Add an entry to `.domainization/artifact_registry.yaml`:
   ```yaml
   - artifact_id: my_new_engine_py
     file_path: engines/my_new_engine.py
     primary_domain: SIGNALS
     artifact_type: ENGINE
     lifecycle_status: development
     created_date: "2025-01-01"
     last_modified: "2025-01-01"
     owner_role: "Signal Engineer"
     ssot_relationship: implementation
     allowed_writers: ["SIGNALS"]
     allowed_readers: ["ALL"]
   ```

3. **During FAST LANE phase** — This warning can be safely ignored. Registration is encouraged but not required.

---

### E002: Invalid Domain Assignment

**Severity**: HIGH  
**Gate**: Gate 2 (Domain Assignment)  
**Description**: An artifact is assigned to a domain that cannot own its artifact type.

**Symptoms**:
```
🟠 [E002] Gate 2: Domain Assignment (WARNING)
  Artifact: engines/new_feature.py
  Error:    Domain 'REPORT' cannot own artifact type 'ENGINE'
```

**Resolution**:

1. Check which domains can own your artifact type in `.domainization/domain_registry.yaml`
2. Change the `primary_domain` field to a valid domain

**Quick Reference — Domain-to-Type Mapping**:

| Artifact Type | Valid Domains |
|---------------|--------------|
| SSOT | GOV, ARCH, SIGNALS, SEMANTICS, REASONING, REPORT, STATE, DATA, USER, DEPLOY, MEMORY, SIM |
| ENGINE | SIGNALS, SEMANTICS, REASONING, DATA, SIM, USER, ARCH |
| REPORT_OUT | REPORT |
| DATA_IN | DATA, STATE |
| DATA_OUT | SIGNALS, SEMANTICS, REASONING, DATA, STATE |
| RUNTIME | DEPLOY, ARCH |
| DASHBOARD | USER |

---

### E003: Invalid Lifecycle Transition

**Severity**: MEDIUM  
**Gate**: Gate 3 (Lifecycle Validation)  
**Description**: A lifecycle state change was attempted that is not allowed by the state machine.

**Symptoms**:
```
🟡 [E003] Gate 3: Lifecycle Validation (WARNING)
  Artifact: docs/my_doc.md
  Error:    Invalid lifecycle transition: draft -> deprecated
```

**Resolution**:

1. Check valid transitions in `.domainization/lifecycle_state_machine.yaml`
2. Follow the correct transition path

**Valid Transitions by Type**:

| Type | Valid Transitions |
|------|-------------------|
| SSOT | draft → review → canonical → deprecated; canonical → draft (revision) |
| ENGINE | planned → development → active → deprecated; development → development (iteration) |
| REPORT_OUT | generated → current → archived |
| DATA_OUT | generated → current → archived |
| DATA_IN | active → stale → archived |

---

### E004: Domain Boundary Violation

**Severity**: HIGH  
**Gate**: Gate 4 (Boundary Enforcement)  
**Description**: A domain attempted to modify an artifact it does not have write permission for.

**Symptoms**:
```
🟠 [E004] Gate 4: Boundary Enforcement (WARNING)
  Artifact: docs/signal_spec.md
  Error:    Domain 'REPORT' cannot modify artifact owned by 'SIGNALS'
```

**Resolution**:

1. Check the `allowed_writers` field in the artifact's metadata
2. Either:
   - Add your domain to `allowed_writers` (if appropriate)
   - Move the modification to the correct domain's responsibility
   - Request approval from the primary domain owner

---

### E005: SSOT Conflict Detected

**Severity**: CRITICAL  
**Gate**: Gate 5 (SSOT Consistency)  
**Description**: Multiple artifacts claim to be the canonical source of truth for the same topic.

**Symptoms**:
```
🔴 [E005] Gate 5: SSOT Consistency (WARNING)
  Artifact: docs/architecture_v2.md
  Error:    SSOT conflict: Multiple canonical documents for topic 'architecture'
```

**Resolution**:

1. Identify which document should be the single canonical SSOT
2. Mark the canonical document with `ssot_relationship: canonical`
3. Mark other documents as:
   - `ssot_relationship: derived` (if they extend the canonical)
   - `ssot_relationship: implementation` (if they implement the canonical)
4. Add the canonical artifact_id to the `dependencies` field of derived/implementation documents

---

### E006: Missing Required Metadata

**Severity**: MEDIUM  
**Gate**: Gate 1 (Artifact Registration)  
**Description**: An artifact is registered but missing required metadata fields.

**Symptoms**:
```
🟡 [E006] Gate 1: Artifact Registration (WARNING)
  Artifact: my_file_md
  Error:    Missing required metadata fields: lifecycle_status, owner_role
```

**Resolution**:

Add the missing fields. Required fields are:
- `artifact_id`
- `primary_domain`
- `artifact_type`
- `lifecycle_status`
- `created_date`
- `last_modified`

---

### E007: Deprecated Artifact Modification

**Severity**: HIGH  
**Gate**: Gate 3 (Lifecycle Validation)  
**Description**: A deprecated artifact was modified. Deprecated artifacts should not be changed except for metadata updates.

**Symptoms**:
```
🟠 [E007] Gate 3: Lifecycle Validation (WARNING)
  Artifact: engines/old_engine.py
  Error:    Cannot modify deprecated artifact 'engines/old_engine.py'
```

**Resolution**:

1. If the artifact needs changes, first revert its lifecycle status from `deprecated` to an active state
2. If creating a replacement, create a new artifact instead
3. Only metadata updates (frontmatter changes) are allowed on deprecated artifacts

---

### E008: Authority Chain Violation

**Severity**: CRITICAL  
**Gate**: Gate 4 (Boundary Enforcement)  
**Description**: A domain attempted to create meaning outside its authority level in the reasoning chain.

**Symptoms**:
```
🔴 [E008] Gate 4: Boundary Enforcement (WARNING)
  Artifact: semantic_output.py
  Error:    Authority chain violation: 'SIGNALS' cannot create meaning in 'SEMANTICS' domain
```

**Resolution**:

Follow the authority chain: **SIGNALS → SEMANTICS → REASONING → REPORT**

- **SIGNALS** can only write raw signal data
- **SEMANTICS** can only write semantic interpretations (consuming signals)
- **REASONING** can only write reasoning conclusions (consuming semantics)
- **REPORT** can only write human-readable text (consuming reasoning)

Move the logic to the appropriate domain in the chain.

---

### E009: Forbidden Cloud Provider Reference

**Severity**: CRITICAL  
**Gate**: Gate 2 (Domain Assignment)  
**Description**: A reference to a forbidden cloud provider (AWS, Supabase, Azure) was detected.

**Symptoms**:
```
🔴 [E009] Gate 2: Domain Assignment (WARNING)
  Artifact: config/deploy.py
  Error:    Forbidden cloud provider 'aws' referenced in 'config/deploy.py'
```

**Resolution**:

1. Remove references to forbidden providers:
   - AWS: `aws.`, `.amazonaws.com`, `boto3`, `s3://`
   - Supabase: `supabase.`, `supabase.co`
   - Azure: `azure.`, `.azure.com`
2. Replace with Google Cloud Platform equivalents:
   - `google.`, `googleapis.com`, `gcp.`
   - Google Sheets API is allowed
   - Firebase is allowed

---

### E010: Feature Without Report Value

**Severity**: LOW  
**Gate**: Gate 5 (SSOT Consistency)  
**Description**: A new feature does not demonstrate how it improves report quality.

**Symptoms**:
```
🟢 [E010] Gate 5: SSOT Consistency (WARNING)
  Artifact: engines/new_infra.py
  Error:    Feature 'new_infra' does not demonstrate direct report value
```

**Resolution**:

1. Document how the feature improves the PM report
2. Valid report value categories:
   - Semantic interpretation
   - PM reasoning quality
   - Concentration explanation
   - Dependency explanation
   - Scenario interpretation
   - Confidence explanation
   - Action-space clarity
   - Multilingual rendering
   - Traceability
   - User understanding
3. If no report value exists, consider deferring the feature until after report MVP

---

## Emergency Bypass

### When to Use Emergency Bypass

The `--no-verify` flag bypasses the pre-commit hook entirely. Since the hook currently operates in observability mode (never blocks), bypass is rarely needed. Use it when:

1. **Performance concerns**: The validation check is taking too long and you need to commit quickly
2. **Module import errors**: The Python validation modules cannot be loaded (missing dependencies)
3. **Registry corruption**: The registry files are in a broken state and you need to commit a fix
4. **Hotfix deployments**: You need to push an emergency fix without waiting for validation output

### How to Use Emergency Bypass

```bash
# Bypass the pre-commit hook entirely
git commit --no-verify -m "feat(signals): emergency hotfix for signal engine"

# Short form
git commit -n -m "fix(deploy): critical deployment fix"
```

### Important Notes About Bypass

- **No audit trail**: When `--no-verify` is used, the pre-commit hook does not run, so no validation warnings are logged
- **No blocking anyway**: Since the system is in observability mode, the hook never blocks commits regardless
- **Use sparingly**: Even though bypass has no enforcement impact during FAST LANE, it skips useful visibility
- **Post-bypass**: Run `domainization validate` manually after your emergency to check system health

### When NOT to Use Emergency Bypass

- To avoid seeing warnings (they are informational only)
- To skip registration (registration is voluntary during FAST LANE)
- To work around E005 SSOT conflicts (resolve them instead)
- As a regular workflow habit (defeats the purpose of observability)

---

## CLI Validation Commands

### Run Full Validation

```bash
cd .domainization/src
python cli_main.py validate
```

### Validate Specific Files

```bash
python cli_main.py validate --files engines/my_engine.py docs/my_doc.md
```

### Run Specific Observer

```bash
# Available observers:
# - RegistrationValidator
# - DomainAssignmentValidator
# - LifecycleValidator
# - BoundaryAwarenessValidator
# - SSOTConsistencyValidator

python cli_main.py validate --observer RegistrationValidator
```

### Dry-Run Mode (No Exit Code Impact)

```bash
python cli_main.py validate --dry-run
```

### Disable Colors

```bash
python cli_main.py validate --no-color
```

### Generate Health Report

```bash
python cli_main.py health
python cli_main.py health --domain SIGNALS
python cli_main.py health --violations-only
```

---

## Frequently Asked Questions (FAQ)

### General Questions

**Q: Will the domainization system block my commits?**  
A: No. During the FAST LANE phase, all validation operates in observability mode. Warnings are displayed but commits always proceed. No commit will ever be blocked.

**Q: Do I need to install the pre-commit hook?**  
A: No. The pre-commit hook is entirely optional. It provides helpful visibility into governance status but is not required. Install it with `.domainization/hooks/install_hook.sh` if you want the observability output.

**Q: What happens if I ignore all warnings?**  
A: Nothing breaks. Warnings build visibility for future governance enforcement. Addressing them proactively makes the eventual transition to enforcement mode smoother.

**Q: How do I check the current system health?**  
A: Run `python .domainization/src/cli_main.py health` to generate a comprehensive health report showing registration coverage, domain distribution, and violations.

---

### Registration Questions

**Q: Do I need to register every file I create?**  
A: During FAST LANE phase, no. Registration is encouraged but not enforced. The health report will show unregistered artifacts for visibility.

**Q: What's the difference between frontmatter and registry entries?**  
A: Markdown files (`.md`) can use YAML frontmatter embedded in the file itself. Non-markdown files must be registered in `.domainization/artifact_registry.yaml`. Both approaches are equivalent.

**Q: I see E001 warnings for test files. Should I register them?**  
A: Test files, temporary files, and build artifacts typically do not need registration. Focus on registering source code, documentation, engines, and data files.

---

### Domain Questions

**Q: How do I know which domain my artifact belongs to?**  
A: Consider what the artifact does:
- Generates raw signals → **SIGNALS**
- Interprets signals into meaning → **SEMANTICS**
- Makes decisions based on meaning → **REASONING**
- Produces human-readable output → **REPORT**
- Manages portfolio state → **STATE**
- Handles data ingestion → **DATA**
- Provides user interface → **USER**
- Manages deployment → **DEPLOY**
- Stores historical data → **MEMORY**
- Runs simulations → **SIM**
- Defines governance rules → **GOV**
- Defines system architecture → **ARCH**

**Q: Can an artifact belong to multiple domains?**  
A: Yes. Use `primary_domain` for the main owner and `secondary_domains` for additional associations. Only the primary domain has write authority by default.

**Q: What is the authority chain?**  
A: The authority chain defines how meaning flows through the system: SIGNALS (raw data) → SEMANTICS (interpretation) → REASONING (conclusions) → REPORT (human language). Each domain can only create meaning at its level.

---

### Lifecycle Questions

**Q: What lifecycle status should I use for a new file?**  
A: Use the initial state for the artifact type:
- SSOT → `draft`
- ENGINE → `planned` or `development`
- REPORT_OUT → `generated`
- DATA_IN → `active`
- DATA_OUT → `generated`

**Q: Can I change a deprecated artifact back to active?**  
A: No. The state machine does not allow transitions from `deprecated` back to active states. Create a new artifact instead.

**Q: What does "canonical" mean for SSOT documents?**  
A: A canonical SSOT is the single authoritative source of truth for a topic. Only one document can be canonical per topic. All other documents on the same topic must be marked as `derived` or `implementation`.

---

### Performance Questions

**Q: Validation is taking too long. What can I do?**  
A: 
1. Validate specific files instead of the entire repository: `--files path/to/file.py`
2. Run a specific observer: `--observer RegistrationValidator`
3. Use `--no-verify` on git commit to skip the hook temporarily
4. Check if the registry cache is working: the system caches registry data in memory

**Q: What is the performance target?**  
A: Validation should complete in under 5 seconds for up to 1000 artifacts. Health reports should complete in under 10 seconds.

---

### Troubleshooting the System Itself

**Q: The pre-commit hook shows "Could not import validation modules"**  
A: Ensure you are running Python 3.10+ and that the `.domainization/src/` directory is accessible. The hook will skip validation gracefully if modules cannot be loaded.

**Q: The registry files appear corrupted**  
A: 
1. Check `.domainization/backups/` for recent backups
2. Run `python cli_main.py recovery restore` to restore from the latest backup
3. Run `python cli_main.py health` to verify system state after recovery

**Q: I see warnings about files I deleted**  
A: The artifact registry may still contain entries for deleted files. Remove the corresponding entry from `.domainization/artifact_registry.yaml` or update the frontmatter reference.

**Q: The health report shows 0% registration coverage**  
A: Ensure the artifact registry file exists and is properly formatted. Run `python cli_main.py registry list` to verify registered artifacts.

---

## Getting Help

### Self-Service Resources

| Resource | Location |
|----------|----------|
| Domain Guide | `.domainization/src/README_validation_observers.md` |
| Error Codes | `.domainization/src/README_error_handling_and_audit_logging.md` |
| CLI Usage | `.domainization/src/README_cli_usage.md` |
| Registry API | `.domainization/src/README_registry_layer_python_api.md` |
| Backup/Recovery | `.domainization/src/README_backup_and_recovery.md` |

### Diagnostic Commands

```bash
# Check system health
python .domainization/src/cli_main.py health

# List all registered artifacts
python .domainization/src/cli_main.py registry list

# Show configuration
python .domainization/src/cli_main.py config show

# Run validation with verbose output
python .domainization/src/cli_main.py validate

# Check audit logs
ls .domainization/logs/audit_*.log
```

### Contact

- **System Owner**: CTO / System Architect
- **Documentation**: `.domainization/` directory
- **Issue Tracking**: Repository issue tracker
- **Architecture Decisions**: `docs/domainization_architecture.md`

---

## Features

- Complete error code reference (E001-E010) with symptoms and resolutions
- Emergency bypass documentation with appropriate usage guidelines
- CLI command reference for validation and health checking
- FAQ covering registration, domains, lifecycle, and performance
- Self-service diagnostic commands

## Testing

```bash
# Verify the troubleshooting guide references are accurate
cd .domainization/src
python -m pytest test_validation_error_classes.py -v
python -m pytest test_validation_orchestrator.py -v
```

## Requirements Satisfied

- **Requirement 5.7**: Actionable error messages with resolution guidance
- **Requirement 15.4**: Validation rules clearly documented with examples

## Related Files

| File | Purpose |
|------|---------|
| `validation_error_classes.py` | Error code definitions (E001-E010) |
| `validation_orchestrator.py` | Orchestrator that runs all observers |
| `cli_validation_commands.py` | CLI interface for validation |
| `audit_logger.py` | Audit logging for governance events |
| `.domainization/hooks/pre-commit` | Optional pre-commit hook |
| `.domainization/hooks/install_hook.sh` | Hook installation script |
