# Governance Stabilization — Pre-Flight Execution Plan

**Date**: 2026-05-25  
**Status**: AWAITING APPROVAL  
**Reference**: `reports/governance_stabilization_audit_2026-05-25.md`  
**Objective**: Fix all findings from the governance audit in a controlled, verifiable sequence  

---

## Execution Philosophy

- One commit per fix (single intent, single domain)
- Each fix is independently verifiable via the audit script
- No fix introduces new features — stabilization only
- Each fix reduces the audit finding count measurably
- Rollback strategy: each commit is atomic and revertible

---

## Fix Sequence

### Fix 1: Remove Duplicate `data_json` Entry

**Audit Finding**: CRITICAL — DUPLICATE_ID  
**File**: `.domainization/artifact_registry.yaml`  
**Action**: Remove the "Example 9: CONFIG" entry (line ~1590) which is a leftover duplicate of the `data_json` entry already present in the PORTFOLIO STATE section (line ~1280).

**Exact change**:
```yaml
# REMOVE THIS ENTIRE BLOCK (the "Example 9" leftover):
  # Example 9: CONFIG (Configuration file)
  - artifact_id: data_json
    file_path: data.json
    primary_domain: STATE
    artifact_type: CONFIG
    lifecycle_status: active
    ...
```

**Verification**: Run audit script → CRITICAL count drops from 1 to 0.  
**Risk**: NONE — removing exact duplicate.  
**Commit**: `fix(governance): remove duplicate data_json registry entry`

---

### Fix 2: Lifecycle Model — Make `current` and `captured` Modifiable

**Audit Finding**: MEDIUM × 52 — DEPRECATED_WITH_WRITERS  
**File**: `.domainization/lifecycle_state_machine.yaml`  
**Root Cause**: DATA_OUT, REPORT_OUT, and SNAPSHOT types define `current`/`captured` as read-only, but these artifacts are regenerated daily.

**Action**: Move `current` from `read_only_states` to `modifiable_states` for DATA_OUT and REPORT_OUT. Move `captured` from `read_only_states` to `modifiable_states` for SNAPSHOT.

**Exact changes**:

```yaml
# DATA_OUT: Change from
modifiable_states: []
read_only_states:
  - generated
  - current
  - archived

# DATA_OUT: Change to
modifiable_states:
  - generated
  - current
read_only_states:
  - archived
```

```yaml
# REPORT_OUT: Change from
modifiable_states: []
read_only_states:
  - generated
  - current
  - archived

# REPORT_OUT: Change to
modifiable_states:
  - generated
  - current
read_only_states:
  - archived
```

```yaml
# SNAPSHOT: Change from
modifiable_states: []
read_only_states:
  - captured
  - archived

# SNAPSHOT: Change to
modifiable_states:
  - captured
read_only_states:
  - archived
```

**Rationale**: 
- `current` means "latest version" — it MUST be overwritable because engines regenerate outputs every run
- `captured` means "actively accumulating" — portfolio_memory.xlsx grows over time
- `archived` remains read-only — once archived, it's frozen forever
- This matches operational reality without weakening the immutability guarantee for archived data

**Verification**: Run audit script → MEDIUM count drops from 55 to 3 (only the 2 FILE_NOT_FOUND + 1 AUTHORITY_CHAIN_CONCERN remain).  
**Risk**: LOW — no existing code checks `modifiable_states` for enforcement yet. This is a schema correction.  
**Commit**: `fix(governance): make current/captured modifiable states for regenerable artifacts`

---

### Fix 3: Reassign `visual_engine_py` Domain

**Audit Finding**: HIGH — DOMAIN_TYPE_VIOLATION  
**File**: `.domainization/artifact_registry.yaml`  
**Root Cause**: USER domain's `cannot_own` list includes ENGINE, but `visual_engine_py` is assigned to USER.

**Decision Point — Two Options**:

| Option | Change | Consequence |
|--------|--------|-------------|
| A: Move to ARCH | Change `primary_domain: USER` → `primary_domain: ARCH` | Visualization logic lives in architecture layer |
| B: Allow USER to own ENGINE | Remove ENGINE from USER's `cannot_own` in domain_registry.yaml | USER domain becomes more powerful |

**My Recommendation**: Option A — move to ARCH with `secondary_domains: [USER]`. The visual engine is infrastructure that serves the USER domain, similar to how `engine_runner_py` serves all domains.

**Exact change (Option A)**:
```yaml
# In artifact_registry.yaml, change visual_engine_py:
  primary_domain: ARCH        # was: USER
  secondary_domains:
    - USER
  allowed_writers:
    - ARCH
    - USER                    # USER can still modify it
```

**Verification**: Run audit script → HIGH count drops by 1.  
**Risk**: LOW — no runtime code checks domain assignment.  
**Commit**: `fix(governance): reassign visual_engine_py to ARCH domain`

---

### Fix 4: Correct Broken File Paths

**Audit Finding**: MEDIUM × 2 — FILE_NOT_FOUND  
**File**: `.domainization/artifact_registry.yaml`

**Action**: Verify actual file locations and update registry.

**Investigation needed**:
```bash
# Check if files exist under different names/paths
find . -name "*calibration*" -not -path "./.git/*"
find . -name "*governance*baseline*" -not -path "./.git/*"
```

**Expected outcomes**:
- `kiro_calibration_report_md`: Likely at `reports/kiro_calibration_report.md` (not `docs/`)
- `execution_governance_baseline_md`: Likely at `.kiro/steering/execution_governance_baseline.md` (underscore vs hyphen)

**Exact change**: Update `file_path` fields to match actual filesystem paths.

**Verification**: Run audit script → FILE_NOT_FOUND count drops to 0.  
**Risk**: NONE — metadata correction only.  
**Commit**: `fix(governance): correct broken file_path references in registry`

---

### Fix 5: Add CLI Writer Domain Validation

**Audit Finding**: HIGH — CROSS_DOMAIN_WRITER_BYPASS  
**File**: `.domainization/src/cli_registry_commands.py`

**Action**: Add validation in `register()` and `update()` methods that checks:
1. Each domain in `--allowed-writers` must be able to own the artifact's type
2. The artifact's primary domain must always be in the writers list
3. Cross-domain writers that violate ownership rules require `--force` flag

**Exact change location**: After domain-type validation in `register()` method (~line 70):

```python
# Validate allowed_writers domains
if args.allowed_writers:
    for writer_domain_id in args.allowed_writers:
        writer_domain = self.domain_registry.get_domain(writer_domain_id)
        if writer_domain is None:
            print(f"Error: Invalid writer domain '{writer_domain_id}'", file=sys.stderr)
            return 1
        # Check if writer domain can own this artifact type
        if not writer_domain.can_own_type(args.type):
            if not getattr(args, 'force', False):
                print(f"Error: Writer domain '{writer_domain_id}' cannot own type '{args.type}'", file=sys.stderr)
                print(f"Use --force to override this check")
                return 1
            else:
                print(f"Warning: Forcing cross-domain writer '{writer_domain_id}' for type '{args.type}'")
```

**Additional change**: Add `--force` flag to register and update parsers.

**Test**: Add test case in `test_cli_registry_commands.py` that verifies:
- Valid writer domains are accepted
- Invalid writer domains are rejected
- `--force` overrides the check with warning

**Verification**: Run audit script → CROSS_DOMAIN_WRITER_BYPASS finding disappears. Run test suite → all pass.  
**Risk**: LOW — additive validation, doesn't break existing valid registrations.  
**Commit**: `fix(governance): add writer domain validation to CLI register/update`

---

### Fix 6: Register SSOT Framework Documents

**Audit Finding**: HIGH × 89 — MISSING_DEPENDENCY  
**Files**: `.domainization/artifact_registry.yaml` + 17 markdown files in `docs/`

**Decision Point — Architecture Choice**:

| Option | Description | Effort | Trade-off |
|--------|-------------|--------|-----------|
| A: Register in YAML | Add all 17 docs to artifact_registry.yaml | 1 hour | Dual source of truth (frontmatter + registry) |
| B: Frontmatter resolution | Modify dependency resolver to scan frontmatter | 2 hours | More complex code, single source of truth |
| C: Soft references | Downgrade to INFO, accept as "external refs" | 10 min | Dependency graph remains incomplete |

**My Recommendation**: Option A for now (register in YAML), with a TODO to migrate to Option B later. Reason: Option B requires changes to `artifact_registry.py`, `validation_orchestrator.py`, and all observers. That's a feature, not a stabilization fix.

**Action (Option A)**:
1. Scan all 17 markdown files for existing frontmatter `artifact_id`
2. If frontmatter exists, use that ID; if not, derive from filename
3. Add minimal registry entries (artifact_id, file_path, primary_domain, artifact_type=SSOT, lifecycle_status=canonical)

**Expected entries to add**:

| artifact_id | file_path | domain |
|-------------|-----------|--------|
| signal_calculation_framework_md | docs/signal_calculation_framework.md | SIGNALS |
| portfolio_health_framework_md | docs/portfolio_health_framework.md | SIGNALS |
| market_regime_framework_md | docs/market_regime_framework.md | SIGNALS |
| correlation_dependency_framework_md | docs/correlation_dependency_framework.md | SIGNALS |
| scoring_methodology_framework_md | docs/scoring_methodology_framework.md | SIGNALS |
| semantic_signal_registry_md | docs/semantic_signal_registry.md | SEMANTICS |
| semantic_reasoning_rules_md | docs/semantic_reasoning_rules.md | SEMANTICS |
| decision_governance_md | docs/decision_governance.md | GOV |
| report_reasoning_system_md | docs/report_reasoning_system.md | REPORT |
| report_section_specification_md | docs/report_section_specification.md | REPORT |
| simulation_architecture_md | docs/simulation_architecture.md | SIM |
| dashboard_philosophy_md | docs/dashboard_philosophy.md | USER |
| engine_design_principles_md | docs/engine_design_principles.md | ARCH |
| portfolio_memory_architecture_md | docs/portfolio_memory_architecture.md | MEMORY |
| portfolio_state_model_md | docs/portfolio_state_model.md | STATE |
| watchlist_asset_registry_framework_md | docs/watchlist_asset_registry_framework.md | STATE |
| data_ingestion_normalization_framework_md | docs/data_ingestion_normalization_framework.md | DATA |

**Pre-condition**: Verify each file actually exists on disk before registering.

**Verification**: Run audit script → MISSING_DEPENDENCY count drops from 89 to 0.  
**Risk**: MEDIUM — creates dual source of truth if files also have frontmatter. Mitigated by adding comment "# Registered here for dependency resolution; canonical metadata in frontmatter".  
**Commit**: `feat(governance): register SSOT framework documents for dependency resolution`

---

## Execution Order and Commit Sequence

```
Fix 1 → fix(governance): remove duplicate data_json registry entry
Fix 2 → fix(governance): make current/captured modifiable states for regenerable artifacts
Fix 3 → fix(governance): reassign visual_engine_py to ARCH domain
Fix 4 → fix(governance): correct broken file_path references in registry
Fix 5 → fix(governance): add writer domain validation to CLI register/update
Fix 6 → feat(governance): register SSOT framework documents for dependency resolution
```

---

## Verification Gate

After all 6 fixes, run the full audit:

```bash
cd .domainization/src
../../.venv/bin/python governance_stabilization_audit.py
```

**Expected result**:
- CRITICAL: 0
- HIGH: 0
- MEDIUM: 1 (the false-positive "reasoning" keyword in report_engine_py description)
- LOW: 0
- Exit code: 0

---

## Decisions Required From You

Before I execute, I need your call on:

| # | Decision | Options | My Recommendation |
|---|----------|---------|-------------------|
| 1 | `visual_engine_py` domain | A: Move to ARCH / B: Allow USER to own ENGINE | A (move to ARCH) |
| 2 | SSOT dependency resolution | A: Register in YAML / B: Frontmatter resolver / C: Soft refs | A (register in YAML) |
| 3 | Execution mode | All 6 at once / One-by-one with review | All 6 at once (atomic stabilization) |

---

## Rollback Strategy

Each fix is a single commit. If any fix causes unexpected issues:

```bash
git revert <commit-hash>
```

The audit script serves as the regression test — run it after each revert to confirm the system returns to its previous state.

---

## Post-Stabilization Next Steps

Once all fixes pass the verification gate:

1. Run the full observer suite (`domainization validate`) — should produce 0-1 warnings
2. Update the health reporter to detect dead artifacts and orphaned engines (new feature, separate commit)
3. Add audit script to CI pipeline as a governance gate
4. Resume Task 12+ from the domainization spec with confidence
