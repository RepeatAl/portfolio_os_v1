# Getting Started Guide

## Overview

The domainization system is Portfolio OS's artifact governance framework. It provides structured ownership, lifecycle tracking, and boundary awareness for every file in the repository. The system answers three questions for any artifact:

1. **Who owns it?** — Which domain is responsible
2. **What is it?** — What type of artifact (SSOT, ENGINE, REPORT_OUT, etc.)
3. **Where is it in its lifecycle?** — Current state (draft, active, canonical, deprecated, etc.)

### Why Domainization Exists

Portfolio OS has 50+ root-level files, multiple engines, reports, data files, and documentation. Without governance:
- Files have no clear ownership
- Lifecycle status is invisible (is this file still active? deprecated?)
- Domain boundaries are implicit and easily violated
- The reasoning chain (SIGNALS → SEMANTICS → REASONING → REPORT) can be accidentally bypassed

Domainization makes all of this visible and trackable without blocking your workflow.

### Current Mode: OBSERVABILITY

The system operates in **observability mode** during the FAST LANE phase:
- All validation produces **warnings only** — never blocks commits
- Health reports expose gaps without requiring immediate action
- Pre-commit hooks are **optional** and non-blocking
- You can work freely while building visibility into the system's structure

## How It Affects Developer Workflow

### What Changes

1. **New files** should have metadata (domain, type, lifecycle) — but it's not enforced yet
2. **Health reports** show which artifacts are registered and which are not
3. **Validation warnings** appear if you opt into the pre-commit hook
4. **CLI commands** let you query the registry and check system health

### What Doesn't Change

- Your files stay where they are (no directory restructuring)
- Commits always succeed (no blocking)
- Existing workflows continue working
- No mandatory bureaucracy during FAST LANE phase

## Quick Start Tutorial

### Step 1: Check System Health

Run the health report to see the current state of artifact governance:

```bash
cd .domainization/src
python -m cli_main health
```

This shows:
- Total registered vs unregistered artifacts
- Domain coverage (how many artifacts per domain)
- Lifecycle distribution
- Any violations detected

### Step 2: List Registered Artifacts

Browse what's already registered:

```bash
# List all artifacts
python -m cli_main list

# Filter by domain
python -m cli_main list --domain SIGNALS

# Filter by type
python -m cli_main list --type ENGINE

# Filter by lifecycle status
python -m cli_main list --lifecycle active
```

### Step 3: Show Artifact Details

Inspect a specific artifact's metadata:

```bash
python -m cli_main show allocation_engine_py
```

### Step 4: Run Validation (Optional)

Check the repository for governance issues (warnings only):

```bash
# Validate all
python -m cli_main validate

# Validate specific files
python -m cli_main validate --files engines/allocation_engine.py

# Dry run (preview what would be checked)
python -m cli_main validate --dry-run
```

### Step 5: Install Pre-Commit Hook (Optional)

If you want validation hints at commit time:

```bash
cd .domainization/hooks
bash install_hook.sh
```

The hook only shows warnings — it never blocks your commits.


## Adding Metadata to Your Artifacts

### For Markdown Files: YAML Frontmatter

Add a YAML frontmatter block at the top of your markdown file:

```markdown
---
artifact_id: my_new_document_md
primary_domain: SIGNALS
artifact_type: SSOT
lifecycle_status: draft
created_date: "2026-06-01"
last_modified: "2026-06-01"
owner_role: Signal engineer
ssot_relationship: canonical
allowed_writers:
  - SIGNALS
allowed_readers:
  - ALL
topic: my_signal_topic
---

# My New Document

Content goes here...
```

### For Non-Markdown Files: Registry Entry

Register the artifact via CLI:

```bash
python -m cli_main register \
  --id my_new_engine_py \
  --path engines/my_new_engine.py \
  --domain SIGNALS \
  --type ENGINE \
  --lifecycle active \
  --owner "Signal engineer" \
  --ssot-relationship implementation \
  --writers SIGNALS \
  --readers ALL
```

Or add an entry directly to `.domainization/artifact_registry.yaml`:

```yaml
  - artifact_id: my_new_engine_py
    file_path: engines/my_new_engine.py
    primary_domain: SIGNALS
    artifact_type: ENGINE
    lifecycle_status: active
    created_date: "2026-06-01"
    last_modified: "2026-06-01"
    owner_role: Signal engineer
    ssot_relationship: implementation
    allowed_writers:
      - SIGNALS
    allowed_readers:
      - ALL
    dependencies:
      - signal_calculation_framework_md
    description: "Calculates my new signal"
```

### Updating Existing Artifacts

Update metadata for an already-registered artifact:

```bash
python -m cli_main update my_new_engine_py \
  --lifecycle active \
  --last-modified 2026-06-15
```

## Metadata Field Reference

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `artifact_id` | Unique identifier | `allocation_engine_py` |
| `file_path` | Relative path from repo root | `engines/allocation_engine.py` |
| `primary_domain` | Domain ID (one of 12 domains) | `SIGNALS` |
| `artifact_type` | Artifact type | `ENGINE` |
| `lifecycle_status` | Current lifecycle state | `active` |
| `created_date` | Creation date (YYYY-MM-DD) | `2026-01-15` |
| `last_modified` | Last modification date | `2026-05-20` |
| `owner_role` | Who is responsible | `Signal engineer` |
| `ssot_relationship` | Relationship to SSOT | `implementation` |
| `allowed_writers` | Domains that can modify | `[SIGNALS]` |
| `allowed_readers` | Domains that can read | `[ALL]` |

### Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| `secondary_domains` | Additional domain associations | `[ARCH, DATA]` |
| `dependencies` | Artifact IDs this depends on | `[signal_framework_md]` |
| `topic` | Topic for SSOT conflict detection | `allocation_signals` |
| `description` | Human-readable description | `"Calculates allocation signals"` |
| `tags` | Categorization tags | `[signals, allocation]` |

## The 12 Domains

Choose the correct `primary_domain` for your artifact:

### Core Reasoning Chain (priority order)

| Domain | Responsibility | Authority Level |
|--------|---------------|-----------------|
| `SIGNALS` | Raw signal calculation and generation | 1 (highest) |
| `SEMANTICS` | Semantic interpretation of signals | 2 |
| `REASONING` | Decision logic and conclusions | 3 |
| `REPORT` | Human-readable text output | 4 |

### Surface Domains

| Domain | Responsibility |
|--------|---------------|
| `GOV` | Governance frameworks and decision models |
| `ARCH` | System architecture and design principles |
| `STATE` | Portfolio state and watchlist management |
| `DATA` | Data ingestion and normalization |
| `USER` | User interface and dashboards |
| `DEPLOY` | Deployment and runtime entry points |
| `MEMORY` | Historical snapshots and portfolio memory |
| `SIM` | Simulation and scenario analysis |

## Artifact Types and Lifecycles

Choose the correct `artifact_type` and valid `lifecycle_status`:

| Type | Description | Lifecycle States |
|------|-------------|-----------------|
| `SSOT` | Source of truth documents | draft → review → canonical → deprecated |
| `ENGINE` | Python computation engines | planned → development → active → deprecated |
| `REPORT_OUT` | Generated report text files | generated → current → archived |
| `DATA_IN` | Input data files | active → stale → archived |
| `DATA_OUT` | Generated data files | generated → current → archived |
| `RUNTIME` | Runtime entry points | development → active → deprecated |
| `DASHBOARD` | User-facing dashboards | development → active → deprecated |
| `SNAPSHOT` | Historical data snapshots | captured → archived |
| `CONFIG` | Configuration files | draft → active → deprecated |
| `CALIBRATION` | Calibration reports | draft → active → superseded |
| `STEERING` | Steering/governance files | draft → active → deprecated |

## Common Scenarios

### Adding a New Engine

```bash
# 1. Create your engine file
# 2. Register it
python -m cli_main register \
  --id my_engine_py \
  --path engines/my_engine.py \
  --domain REASONING \
  --type ENGINE \
  --lifecycle development \
  --owner "Reasoning engineer" \
  --ssot-relationship implementation \
  --writers REASONING \
  --readers ALL

# 3. When it's production-ready, update lifecycle
python -m cli_main update my_engine_py --lifecycle active
```

### Adding a New SSOT Document

```markdown
---
artifact_id: my_framework_md
primary_domain: ARCH
artifact_type: SSOT
lifecycle_status: draft
created_date: "2026-06-01"
last_modified: "2026-06-01"
owner_role: System architect
ssot_relationship: canonical
allowed_writers:
  - ARCH
allowed_readers:
  - ALL
topic: my_framework
---

# My Framework

Document content...
```

### Checking What a Domain Owns

```bash
# See all SIGNALS domain artifacts
python -m cli_main list --domain SIGNALS

# See all active engines
python -m cli_main list --type ENGINE --lifecycle active
```

## Troubleshooting

### "Artifact not registered" Warning

This means a file exists without metadata. To fix:
1. Determine the correct domain and type
2. Add frontmatter (markdown) or register via CLI (other files)

### "Invalid domain assignment" Warning

The artifact's `primary_domain` doesn't match what that domain can own. Check the domain's `allowed_artifact_types` in `domain_registry.yaml`.

### "Invalid lifecycle transition" Warning

You tried to move an artifact to a state that isn't reachable from its current state. Check the lifecycle state machine for valid transitions.

### Need Help?

```bash
# Show CLI help
python -m cli_main --help

# Show command-specific help
python -m cli_main register --help
python -m cli_main validate --help
python -m cli_main health --help
```

## Testing

### Running the Domainization Test Suite

```bash
# Run all domainization tests
cd .domainization/src
python -m pytest -v

# Run specific test modules
python -m pytest test_artifact_registry.py -v
python -m pytest test_domain_registry.py -v
python -m pytest test_lifecycle_state_machine.py -v
```

## Requirements Satisfied

This documentation satisfies the following requirements:

- ✅ **Req 15.10**: Validation rules clearly documented
- ✅ **Task 15.1**: Getting started guide with what/why/how
- ✅ Developer workflow explanation (observability mode, no blocking)
- ✅ Quick start tutorial (health → list → show → validate)
- ✅ Examples of adding metadata (frontmatter and registry entry)
- ✅ Domain and artifact type reference tables
- ✅ Common scenarios with CLI examples
- ✅ Troubleshooting section

## Related Files

- `.domainization/README.md` — System overview and directory structure
- `.domainization/src/cli_main.py` — CLI entry point
- `.domainization/artifact_registry.yaml` — Central artifact index
- `.domainization/domain_registry.yaml` — 12 canonical domain definitions
- `.domainization/lifecycle_state_machine.yaml` — State machines for artifact types
- `.domainization/hooks/install_hook.sh` — Optional pre-commit hook installer
- `.domainization/src/README_cli_usage.md` — Detailed CLI command reference
- `.domainization/src/README_validation_observers.md` — Validation observer details
