# REPORT_OUT Type Splitting Evaluation

## HARDENING 13 — REPORT_OUT Semantic Breadth Analysis

**Date:** 2026-05-27  
**Status:** EVALUATION ONLY — No implementation changes  
**Requirements:** 16.1, 16.2  
**Triggered by:** REPORT_OUT currently covers 16 artifacts spanning semantically distinct categories (briefing files, daily report, health reports) under a single type.

---

## 1. Current State Analysis

### 1.1 REPORT_OUT Artifact Inventory (16 total)

The artifact registry contains **16 artifacts** typed as `REPORT_OUT`, all in `current` lifecycle status:

| # | artifact_id | file_path | Semantic Role |
|---|-------------|-----------|---------------|
| 1 | portfolio_report_txt | portfolio_report.txt | Legacy daily report |
| 2 | morning_briefing_txt | morning_briefing.txt | Legacy briefing |
| 3 | allocation_briefing_txt | allocation_briefing.txt | Legacy briefing |
| 4 | attribution_briefing_txt | attribution_briefing.txt | Legacy briefing |
| 5 | correlation_briefing_txt | correlation_briefing.txt | Legacy briefing |
| 6 | cross_asset_briefing_txt | cross_asset_briefing.txt | Legacy briefing |
| 7 | divergence_briefing_txt | divergence_briefing.txt | Legacy briefing |
| 8 | early_warning_briefing_txt | early_warning_briefing.txt | Legacy briefing |
| 9 | flow_briefing_txt | flow_briefing.txt | Legacy briefing |
| 10 | liquidity_briefing_txt | liquidity_briefing.txt | Legacy briefing |
| 11 | market_breadth_briefing_txt | market_breadth_briefing.txt | Legacy briefing |
| 12 | narrative_dependency_briefing_txt | narrative_dependency_briefing.txt | Legacy briefing |
| 13 | portfolio_memory_briefing_txt | portfolio_memory_briefing.txt | Legacy briefing |
| 14 | regime_briefing_txt | regime_briefing.txt | Legacy briefing |
| 15 | relative_strength_briefing_txt | relative_strength_briefing.txt | Legacy briefing |
| 16 | scenario_briefing_txt | scenario_briefing.txt | Legacy briefing |

### 1.2 Artifacts NOT Yet Registered as REPORT_OUT (but semantically belong)

The following artifacts are produced by the runtime pipeline but are not yet registered in the artifact registry:

| Artifact | Location | Semantic Role |
|----------|----------|---------------|
| daily_report.md | output/daily_report.md | Chain-compliant daily report |
| Provenance sidecar | output/<run_id>_provenance.yaml | Machine-readable provenance |
| Run_Context metadata | output/<run_id>_run_context.yaml | Pipeline execution context |
| Semantic snapshots | state/snapshots/<run_id>_semantic_snapshot.yaml | Semantic state archive |
| Semantic delta log | state/semantic_delta_log.yaml | Append-only delta record |
| Health reports | .domainization/reports/*.yaml | Governance health reports |

### 1.3 The Semantic Breadth Problem

`REPORT_OUT` currently conflates:
- **Legacy briefing .txt files** (14 files) — direct Signal→Report shortcuts, deprecated path
- **Portfolio report** (1 file) — legacy daily report, pre-chain
- **Morning briefing** (1 file) — legacy summary briefing

Additionally, the new chain-compliant pipeline produces artifacts that would logically be typed `REPORT_OUT` but serve fundamentally different governance purposes:
- `daily_report.md` — canonical chain-compliant output (the product)
- Provenance sidecars — machine-readable governance metadata
- Semantic snapshots — immutable state archives
- Run context files — temporal consistency records

A single `REPORT_OUT` type cannot distinguish between "deprecated legacy briefing scheduled for sunset" and "canonical chain-compliant daily report that IS the product."

---

## 2. Proposed Sub-Type Evaluation

### 2.1 REPORT_RUNTIME_OUTPUT

**Definition:** Chain-compliant outputs produced through the full Canonical Chain (SIGNALS → SEMANTICS → REASONING → REPORT) with provenance metadata.

**Candidate artifacts:**
| Artifact | Current Status |
|----------|---------------|
| daily_report.md | Not yet registered (Phase B output) |
| Provenance sidecar YAML | Not yet registered (Phase B output) |

**Count:** 2 artifacts (per pipeline run)

**Governance characteristics:**
- Subject to full chain validation
- Requires provenance metadata
- Deterministic (byte-identical for same inputs)
- Canonical truth (per Requirement 21)
- Active lifecycle: generated → current → archived

### 2.2 GOVERNANCE_BRIEFING

**Definition:** Legacy briefing .txt files produced by direct Signal→Report flows, scheduled for deprecation under Requirement 25 sunset governance.

**Candidate artifacts:**
| Artifact | Signal Category |
|----------|----------------|
| allocation_briefing.txt | allocation |
| attribution_briefing.txt | attribution |
| correlation_briefing.txt | correlation |
| cross_asset_briefing.txt | cross_asset |
| divergence_briefing.txt | divergence |
| early_warning_briefing.txt | early_warning |
| flow_briefing.txt | flow |
| liquidity_briefing.txt | liquidity |
| market_breadth_briefing.txt | market_breadth |
| narrative_dependency_briefing.txt | narrative_dependency |
| portfolio_memory_briefing.txt | portfolio_memory |
| regime_briefing.txt | regime |
| relative_strength_briefing.txt | relative_strength |
| scenario_briefing.txt | scenario |
| morning_briefing.txt | summary |
| portfolio_report.txt | daily_summary |

**Count:** 16 artifacts (all current REPORT_OUT entries)

**Governance characteristics:**
- Deprecated path (Requirement 25 sunset governance applies)
- NOT chain-compliant (forbidden Signal→Report flows)
- Sunset dates required (deprecation_start_date, sunset_target_date)
- Lifecycle: current → deprecated → sunset_pending → archived
- Zero provenance metadata

### 2.3 HISTORICAL_REPORT

**Definition:** Archived reports and snapshots from previous pipeline runs, retained for forensic replay and audit.

**Candidate artifacts:**
| Artifact | Current Type |
|----------|-------------|
| history/briefing_2026-05-23.txt | SNAPSHOT (MEMORY domain) |
| Archived daily reports | Not yet produced |

**Count:** 1 currently registered (as SNAPSHOT, not REPORT_OUT)

**Governance characteristics:**
- Read-only after archival
- No regeneration permitted
- Forensic replay support
- Already partially covered by SNAPSHOT type

### 2.4 SNAPSHOT_OUTPUT

**Definition:** Semantic state snapshots and delta logs — point-in-time captures of system truth.

**Candidate artifacts:**
| Artifact | Location |
|----------|----------|
| Semantic snapshots (16 files) | state/snapshots/<run_id>_semantic_snapshot.yaml |
| Latest snapshot pointer | state/latest_snapshot.yaml |
| Semantic delta log | state/semantic_delta_log.yaml |
| Protected states snapshot | state/hardening_8_protected_states_snapshot.yaml |

**Count:** 19 artifacts currently on disk

**Governance characteristics:**
- Immutable after creation (Hardening 6)
- Append-only delta log
- Not human-readable reports — machine state
- Already partially covered by SNAPSHOT type in lifecycle state machine
- Subject to Semantic State Store governance (Requirement 12)

### 2.5 TRANSIENT_RUNTIME_OUTPUT

**Definition:** Intermediate pipeline artifacts that exist temporarily during execution but are not canonical truth.

**Candidate artifacts:**
| Artifact | Nature |
|----------|--------|
| Orchestration buffers | In-memory only |
| Pre-validation staging | In-memory only |
| Intermediate draft reasoning | In-memory only |
| In-memory transforms | In-memory only |

**Count:** 0 persisted artifacts (by definition, transient artifacts are NOT persisted)

**Governance characteristics:**
- Exempt from canonical governance (Requirement 16.3)
- Never persisted to disk
- Never crosses runtime boundaries
- If persisted → promoted to canonical (Requirement 16.5)
- Already handled by `governance/canonical_boundary.py` classification

---

## 3. Migration Impact Assessment

### 3.1 Registry Schema Changes Required

| Change | Scope | Risk |
|--------|-------|------|
| Add new `artifact_type` values to lifecycle_state_machine.yaml | 1 file | LOW — additive only |
| Update 16 existing REPORT_OUT entries to GOVERNANCE_BRIEFING | 16 entries | MEDIUM — bulk update |
| Add lifecycle states for new types | 1 file | LOW — additive |
| Update domain_registry.yaml `cannot_own` lists | 12 domains | MEDIUM — cross-cutting |
| Update validation logic in domainization tools | 3-5 files | MEDIUM — behavioral change |

### 3.2 Code Impact

| Component | Change Required |
|-----------|----------------|
| `.domainization/src/artifact_registry.py` | Add new type validation |
| `.domainization/src/health_reporter.py` | Report on new types separately |
| `.domainization/src/report_value_detector.py` | Type-aware validation rules |
| `.domainization/src/runtime_flow_detector.py` | Type-aware flow detection |
| `governance/canonical_boundary.py` | Map new types to canonical/transient |
| `runtime/pipeline_result.py` | Type-aware artifact classification |

### 3.3 Backward Compatibility Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Existing tooling queries `artifact_type == "REPORT_OUT"` | HIGH | Provide `REPORT_OUT` as alias/umbrella during transition |
| Health report baselines break (counts change) | MEDIUM | Re-baseline after migration |
| Pre-commit hooks validate against known types | LOW | Update type list in hooks |
| Backup registry files become inconsistent | LOW | Backups are point-in-time, no migration needed |
| External consumers (if any) expect REPORT_OUT | UNKNOWN | Audit downstream consumers first |

---

## 4. Cost-Benefit Analysis

### 4.1 Benefits of Splitting

1. **Governance precision:** Different lifecycle rules per semantic category (sunset governance only applies to GOVERNANCE_BRIEFING, not to REPORT_RUNTIME_OUTPUT)
2. **Query clarity:** "Show me all chain-compliant outputs" becomes a type filter, not a tag search
3. **Deprecation tracking:** Legacy briefings are explicitly typed as deprecated-path artifacts
4. **Canonical boundary alignment:** REPORT_RUNTIME_OUTPUT maps directly to Requirement 16.2 canonical artifacts
5. **Health report accuracy:** Type-level metrics distinguish between "16 legacy briefings" and "1 canonical daily report"

### 4.2 Costs of Splitting

1. **Migration effort:** 16 registry entries + lifecycle state machine + domain registry + validation code
2. **Complexity increase:** 5 types where 1 existed — more cognitive load for maintainers
3. **TRANSIENT_RUNTIME_OUTPUT is empty:** By definition, transient artifacts are never persisted, making this type vacuous in the registry
4. **HISTORICAL_REPORT overlaps SNAPSHOT:** Already a SNAPSHOT type exists with appropriate lifecycle
5. **SNAPSHOT_OUTPUT overlaps SNAPSHOT:** Semantic snapshots are already conceptually SNAPSHOT-type artifacts

### 4.3 Net Assessment

| Proposed Type | Value | Recommendation |
|---------------|-------|----------------|
| REPORT_RUNTIME_OUTPUT | HIGH | Clearly needed — separates canonical product from legacy |
| GOVERNANCE_BRIEFING | HIGH | Clearly needed — enables sunset governance (Req 25) |
| HISTORICAL_REPORT | LOW | Redundant with existing SNAPSHOT type |
| SNAPSHOT_OUTPUT | LOW | Redundant with existing SNAPSHOT type |
| TRANSIENT_RUNTIME_OUTPUT | NONE | Vacuous — transient artifacts are never registered |

---

## 5. Alternative: Unified Type with Tags

Instead of splitting, REPORT_OUT could remain unified with mandatory sub-classification tags:

```yaml
artifact_type: REPORT_OUT
tags:
  - report_class: chain_compliant    # or: legacy_briefing, governance_report
  - sunset_eligible: true            # or: false
  - provenance_required: true        # or: false
```

**Pros:**
- Zero migration of existing entries (additive tags only)
- No lifecycle state machine changes
- No domain registry updates
- Simpler mental model (one type, filtered by tags)

**Cons:**
- Tags are not enforced by lifecycle state machine (no state transitions per tag)
- Sunset governance (Req 25) cannot use type-level lifecycle states
- Queries require tag filtering rather than type filtering
- Canonical boundary classification becomes tag-dependent rather than type-dependent
- Health reports cannot distinguish at the type level

---

## 6. Recommendation

### Split NOW — but only into 2 sub-types, not 5

**Recommended action:** Split `REPORT_OUT` into exactly 2 new types:

1. **`REPORT_RUNTIME_OUTPUT`** — Chain-compliant canonical outputs (daily_report.md, provenance sidecars)
2. **`GOVERNANCE_BRIEFING`** — Legacy briefing files on the sunset path

**Do NOT create:**
- `HISTORICAL_REPORT` — Use existing `SNAPSHOT` type
- `SNAPSHOT_OUTPUT` — Use existing `SNAPSHOT` type  
- `TRANSIENT_RUNTIME_OUTPUT` — Vacuous (never persisted, never registered)

### Rationale

1. The 2-type split directly enables Requirement 25 (sunset governance) at the type level
2. It aligns with Requirement 16.2 (canonical artifact classification) without ambiguity
3. It avoids the 5-type explosion that adds complexity without governance value
4. The existing `SNAPSHOT` type already handles historical and state-capture semantics
5. Transient artifacts are explicitly NOT registered (Requirement 16.3-4), making a registry type for them contradictory

### Implementation Timing

**Split LATER (Phase D — Compatibility Cleanup)** is the recommended timing because:
- Phase D already handles briefing deprecation and sunset governance
- The lifecycle state machine extension (Hardening 11) already added sunset states to REPORT_OUT
- Splitting during Phase D aligns with the natural deprecation workflow
- Splitting now would require re-running Phase B/C verification gates

### Migration Path (when executed)

1. Add `REPORT_RUNTIME_OUTPUT` and `GOVERNANCE_BRIEFING` to lifecycle_state_machine.yaml
2. Retype 16 existing REPORT_OUT entries as `GOVERNANCE_BRIEFING`
3. Register `daily_report.md` and provenance sidecars as `REPORT_RUNTIME_OUTPUT`
4. Update domain_registry.yaml `cannot_own` lists
5. Update health reporter to track new types
6. Re-baseline health report metrics
7. Retain `REPORT_OUT` as deprecated alias for 1 release cycle

---

## 7. Summary

| Dimension | Finding |
|-----------|---------|
| Current REPORT_OUT count | 16 artifacts |
| Semantic breadth problem | Confirmed — conflates deprecated legacy with canonical product |
| Recommended split | 2 types (REPORT_RUNTIME_OUTPUT + GOVERNANCE_BRIEFING) |
| Types NOT recommended | HISTORICAL_REPORT, SNAPSHOT_OUTPUT, TRANSIENT_RUNTIME_OUTPUT |
| Implementation timing | Phase D (Compatibility Cleanup) |
| Backward compatibility | Retain REPORT_OUT as deprecated alias during transition |
| Registry schema changes | lifecycle_state_machine.yaml + domain_registry.yaml + 16 entry updates |
| Code changes | 5-6 files in .domainization/src/ and governance/ |
| Risk level | MEDIUM (bulk update, but additive and reversible) |
