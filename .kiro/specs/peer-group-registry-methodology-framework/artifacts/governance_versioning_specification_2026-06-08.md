# Peer Group Registry Methodology Framework — Governance and Versioning Specification

**Artifact**: governance_versioning_specification_2026-06-08.md
**Task**: Task 6 — Create Governance and Versioning Specification
**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: PGMF_TASK_6_GOVERNANCE_VERSIONING_READY_FOR_HUMAN_REVIEW

**Purpose**: Specifies the governance model, versioning mechanics, review cycles, event triggers, challenge/appeal process, non-overlap property, historical reproducibility, and SAI-BLK-21 governance-aware behavior for peer group assignment records.

**Hard boundaries**: No peer_group_registry.yaml. No final peer assignments. No canonical peer_group_id. No SAI mutation. No code. No market data. No broker/exchange/ATS. No trading logic.

Source authority: SRC-A-01/02/03 (governance_authority — CFA/GIPS), SRC-B-03 (classification_authority — GICS versioning), SRC-C-01 (classification_authority — ICB challenge/appeal).

---

## 1. Required Governance Fields

| Field | Type | Requirement | Allowed Values | Description |
|-------|------|-------------|----------------|-------------|
| `effective_date` | date | REQUIRED | ISO 8601 | Date assignment becomes active. No record valid without it. |
| `end_date` | date | OPTIONAL | ISO 8601 or null | Null = active. Set when superseded. |
| `lifecycle_status` | enum | REQUIRED | active / deprecated / under_review | Current record state. |
| `review_cycle` | enum | REQUIRED | annual / semi_annual / event_triggered | When next reviewed. |
| `approved_by` | string | REQUIRED | Role or identifier | Who approved this assignment. |
| `source_authority` | string | REQUIRED | Source reference | Evidence basis (e.g., SRC-B-01). |
| `change_reason` | string | OPTIONAL | Free text | Rationale for creation or change. |
| `challenge_status` | enum | REQUIRED | none / under_review / resolved | Challenge/appeal status. |
| `review_status` | enum | REQUIRED | current / due_for_review / overdue | Whether reviewed within schedule. |
| `methodology_version` | string | REQUIRED | Semantic version (v1.0.0) | Framework version under which record was created. |


---

## 2. Versioning Rules

### 2.1 Non-Overlap Property

For any `canonical_object_id + family_id` combination, active records MUST NOT overlap in time. Two records both `lifecycle_status = active` and `end_date = null` for the same object+family at the same date is INVALID. SAI-BLK-21 must refuse comparison and log a governance violation if this occurs.

### 2.2 Gaps Allowed When Documented

Gaps in effective_date / end_date sequence are permitted only when documented by: `lifecycle_status = under_review`, `blocked_reason` (delisted/unavailable), `unsupported_status` (scope decision pending), or `challenge_status = under_review`.

### 2.3 Deprecated Records Must Retain History

When superseded: old record receives `end_date` and `lifecycle_status = deprecated`. It is NEVER deleted. No field on a deprecated record may be modified except lifecycle_status and end_date.

### 2.4 Under-Review Records

- Existing active record's lifecycle_status → under_review
- Record retains end_date = null until review concludes
- No new active record created until review decision
- If confirmed: lifecycle_status → active, review_status = current
- If changed: under_review record → deprecated + new active record created
- Under-review records must NOT silently replace active records — requires explicit approved_by

---

## 3. Review-Cycle Logic

### 3.1 Annual (review_cycle = annual)

Reviewed at least once per calendar year (anniversary of effective_date). Process: review_status transitions current → due_for_review at anniversary → overdue after 30 days without review. If confirmed: review_status → current with documented confirmation. If changed: versioned change process applies.

### 3.2 Semi-Annual (review_cycle = semi_annual)

Same as annual but every 6 months. Applicable to rapidly evolving sectors (PGF-01 AI Semiconductors) or newly assigned assets with limited track record.

### 3.3 Event-Triggered (review_cycle = event_triggered)

No periodic review scheduled. Assignment remains valid until a material event trigger fires. Reviewed ONLY when an event occurs.

---

## 4. Event Triggers

| Event | Description | Example |
|-------|-------------|---------|
| Material M&A | Acquisition, merger, spinoff, divestiture materially changing business composition | AVGO acquiring VMware; GE spinning off GE Vernova |
| Revenue mix shift >30% | Principal revenue source shifts such that primary_family may no longer reflect principal business | AMZN cloud surpassing retail revenue |
| Business model restructuring | Fundamental change to value generation model | Hardware company pivoting to subscription SaaS |
| Primary listing change | Company relists on different exchange or changes primary venue | XLON → XNYS |
| Accounting standard change | Transition from GAAP to IFRS or vice versa | Re-domiciliation from US to EU adopting IFRS |
| Taxonomy classification change | GICS or ICB reclassifies company to different sub-industry | GICS annual review reassignment |
| Benchmark methodology change | Index tracked by ETF/fund changes constituent methodology | Nasdaq-100 reconstitution |

**Response**: Affected record's lifecycle_status → under_review; change_reason documents which trigger fired; review initiated; concludes with confirmation or versioned change.

---

## 5. Challenge / Review Process

### 5.1 Challenge Initiation

Any stakeholder may challenge an assignment. Sets challenge_status from none → under_review. Does NOT automatically change lifecycle_status — assignment remains active during challenge. Challenge rationale documented.

### 5.2 Challenge Resolution

- **Rejected**: challenge_status → resolved. Assignment unchanged. Rationale documented.
- **Accepted**: challenge_status → resolved. Standard versioned change process (current deprecated, new active created).

### 5.3 review_status Lifecycle

| Status | Meaning | Transition |
|--------|---------|-----------|
| `current` | Reviewed within schedule | Default after creation or successful review |
| `due_for_review` | Review period arrived, not yet completed | From current when review_cycle anniversary passes |
| `overdue` | 30 days past due without review | From due_for_review after 30 days |

Overdue assignments remain valid — they do not auto-invalidate. SAI-BLK-21 must surface the overdue state.

---

## 6. Anti-Cherry-Picking and Disclosure

### 6.1 Anti-Cherry-Picking (SRC-A-02)

- Subcluster definitions must not be altered to make an asset appear stronger or weaker
- Peer role assignments must not be changed without documented material rationale
- secondary_family must not be added/removed to shift relative performance context without justification
- Challenge outcomes must not be pre-determined

### 6.2 Disclosure (SRC-A-01)

Every assignment must be auditable: approved_by documents who; source_authority documents evidence; change_reason documents why; methodology_version documents under which rules; effective_date documents when. Deprecated records retained for historical audit.

---

## 7. methodology_version vs. Record Version

### 7.1 methodology_version

Tracks which framework version was in effect at record creation. Changes only when methodology framework itself is updated.

Increment rules:
- MAJOR: breaking change to peer_role taxonomy, field taxonomy, or comparison_mode taxonomy
- MINOR: additive change (new optional field, new event trigger, new governance rule)
- PATCH: clarification without structural change

All v1 records carry v1.0.0 (or current minor/patch if incremented).

### 7.2 Record Version

Handled by effective_date / end_date mechanism. Each material field change creates a new record with new effective_date. Previous record receives end_date + deprecated. effective_date IS the version identifier for record-level changes. No separate version counter needed.

---

## 8. Historical Reproducibility

### 8.1 As-of-Date Lookup

Any query specifies as_of_date. Returns record(s) where: effective_date <= as_of_date AND (end_date is null OR end_date > as_of_date) AND lifecycle_status = active at that historical point.

### 8.2 Current Active Record

end_date = null AND lifecycle_status = active AND latest effective_date for that canonical_object_id + family_id.

### 8.3 Audit Trail

All deprecated records retained. Full effective_date / end_date sequence creates complete history. Any historical peer comparison (what were NVDA's peers on 2025-01-15?) reproducible via as_of_date query.

---

## 9. SAI-BLK-21 Governance-Aware Behavior

### 9.1 As-of-Date Requirement

SAI-BLK-21 must specify as_of_date when querying. Without it, returns current active record. Historical diagnostic reproduction requires any past date queryable.

### 9.2 Overlapping Active Record Refusal

If two active records detected for same canonical_object_id + family_id: refuse comparison, log governance violation, set data_quality_status = invalid, output "Governance violation: overlapping active peer records detected. Peer comparison blocked."

### 9.3 Under-Review Handling

Record with lifecycle_status = under_review: comparison ALLOWED but SAI must surface "Peer assignment currently under review — interpretation based on current assignment pending review conclusion."

### 9.4 Overdue Handling

Record with review_status = overdue: comparison ALLOWED but SAI must surface "Peer assignment overdue for review — interpretation based on stale assignment not confirmed within scheduled review cycle."

### 9.5 Governance-Blocked Comparison

When governance state prevents comparison (overlapping records, unresolved violation): peer_comparison_allowed = false. Standard deferred_dependency_notes. No ad-hoc peers invented.

---

## 10. Examples

### 10.1 Valid: Normal Active Record

canonical_object_id: OBJ-NVDA-001, family_id: PGF-01, peer_role: core_peer, effective_date: 2026-06-01, end_date: null, lifecycle_status: active, review_cycle: annual, approved_by: CTO, review_status: current, methodology_version: v1.0.0. Status: VALID.

### 10.2 Valid: Deprecated (Superseded)

canonical_object_id: OBJ-UBER-001, family_id: PGF-04, effective_date: 2026-01-15, end_date: 2026-06-01, lifecycle_status: deprecated, change_reason: "Superseded: revenue mix shift triggered primary_family reassignment." Status: VALID — retained for history.

### 10.3 Valid: Under-Review

canonical_object_id: OBJ-PLTR-001, family_id: PGF-06, peer_role: adjacent_peer, effective_date: 2026-03-01, end_date: null, lifecycle_status: under_review, change_reason: "Event trigger: major defense contract — reviewing peer_role upgrade to core_peer." Status: VALID — SAI surfaces under_review note.

### 10.4 INVALID: Overlapping Active

Record A: OBJ-NVDA-001 / PGF-01 / effective_date: 2026-01-01 / end_date: null / active
Record B: OBJ-NVDA-001 / PGF-01 / effective_date: 2026-06-01 / end_date: null / active
Status: INVALID — two active records for same object+family. SAI refuses comparison. Resolution: Record A must receive end_date and deprecated before B is valid.

### 10.5 Valid: Documented Gap

Record A: effective_date: 2025-06-01, end_date: 2026-01-15, deprecated, change_reason: "Company delisted pending restructuring."
[GAP: 2026-01-15 to 2026-04-01]
Record B: effective_date: 2026-04-01, end_date: null, active, change_reason: "Relisted — peer assignment restored."
Status: VALID — gap documented by Record A's change_reason. SAI produces deferred_dependency_notes during gap period.

---

## 11. Source Authority Mapping

| Principle | Source | Domain | Tier |
|-----------|--------|--------|------|
| Fair representation / full disclosure | SRC-A-01 (CFA/GIPS) | governance_authority | 1 |
| Anti-cherry-picking | SRC-A-02 (CFA III(D)) | governance_authority | 1 |
| Methodology + output transparency | SRC-A-03 (CFA GIPS 2024) | governance_authority | 1 |
| Classification changes require advance notice | SRC-B-03 (MSCI GICS versioning) | classification_authority | 1 |
| Challenge/appeal governance model | SRC-C-01 (FTSE Russell ICB) | classification_authority | 1 |
| Revenue-primary with annual review | SRC-B-01 (MSCI/S&P GICS) | classification_authority | 1 |

---

## 12. Boundary Confirmations

| Boundary | Status |
|----------|--------|
| No peer_group_registry.yaml | CONFIRMED |
| No final peer assignments | CONFIRMED |
| No canonical peer_group_id | CONFIRMED |
| No SAI mutation | CONFIRMED |
| No code | CONFIRMED |
| No market data | CONFIRMED |
| No broker/exchange/ATS | CONFIRMED |
| Tasks 1–5 unchanged | CONFIRMED |
| Task 7 not started | CONFIRMED |
| Tactical Momentum spec not started | CONFIRMED |

---

## Artifact Status

```
PGMF_TASK_6_GOVERNANCE_VERSIONING_READY_FOR_HUMAN_REVIEW
```

---

*End of governance and versioning specification.*
