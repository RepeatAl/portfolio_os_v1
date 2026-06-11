# Requirements Document

> **Peer Group Registry Creation Preflight — Requirements v2**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Revision: v2 (hardened) | Authority: CTO / Architecture | Status: hardened — ready for design

---

## Introduction

This spec begins after the Peer Group Registry Methodology Framework (PGMF) completion and exists to prepare a future peer group registry creation process. PGMF is complete (12/12 tasks, VG-PGMF-1 PASS, status COMPLETE_PENDING_FINAL_HUMAN_REVIEW) but is methodology-only. This preflight does not activate the registry. This preflight prepares candidate records only.

The 9 confirmed family universes (PGF-01 through PGF-09) from the scope preflight (2026-06-07) will be mapped against the completed PGMF methodology fields and converted into candidate registry records for future human/CTO approval. No production registry content is created. No final peer assignments are made. No canonical peer_group_id values are minted.

---

## Document Boundary

This requirements document defines the requirements for the Peer Group Registry Creation Preflight. It does not execute the preflight, create candidate records, create registry files, assign peers, mint peer_group_id values, or activate production use.

All references to candidate record creation, field population, and lifecycle transitions in this document describe rules that will govern future preflight task execution. They do not describe actions taken by this document itself. This document is a specification artifact only.

---

## Scope

### In Scope

- Identify and reference the 9 confirmed family universes from scope preflight
- Define candidate record preparation workflow
- Map family universe inputs to PGMF methodology fields
- Define source authority requirements for every candidate record
- Define candidate registry record shape as non-production draft
- Define evidence requirements per candidate record
- Define block/defer/context-only states for candidate records
- Define human/CTO approval gates before any candidate becomes production
- Define validation expectations for a future implementation spec
- Define final preflight readiness criteria (verification gate)

### Out of Scope

- Production peer_group_registry.yaml creation
- Final peer group assignments
- Production peer_group_id creation
- SAI artifact mutation
- Runtime code or validation code
- Market data integration
- Broker connectivity
- Exchange connectivity
- ATS connectivity
- Trading venue connectivity
- Order routing
- Execution logic
- Compliance claims
- Tactical Momentum Execution Gate Framework implementation

---

## Glossary

| Term | Definition |
|------|-----------|
| **PGMF** | Peer Group Registry Methodology Framework — the completed methodology-only specification governing how the future registry must be structured (12/12 tasks, VG-PGMF-1 PASS) |
| **Candidate_Record** | A non-production, draft-only registry record that has not received human/CTO approval and carries no production authority |
| **Preflight** | A preparation and readiness-verification phase that precedes actual registry creation; produces specifications and draft artifacts only |
| **Family_Universe** | One of the 9 confirmed peer group families (PGF-01 through PGF-09) from the scope preflight document |
| **Source_Authority** | An institutional evidence source (Tier 1, Tier 2, or Tier 3) from the PGMF source registry that provides methodology justification for a candidate record field |
| **Candidate_Status** | The lifecycle state of a candidate record: CANDIDATE_DRAFT, CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, CANDIDATE_CONTEXT_ONLY, or CANDIDATE_READY_FOR_REVIEW |
| **Production_Registry** | The future peer_group_registry.yaml file that will contain canonical, human-approved peer group assignments — NOT created by this preflight |
| **Verification_Gate** | An explicit pass/fail checkpoint that must produce evidence artifacts before downstream work may begin |
| **SAI** | Single Asset Intelligence Framework — the downstream consumer of future registry output via deferred_interfaces.md Section 2.3 |
| **Canonical_Object_ID** | The polymorphic primary key from PGMF design identifying economic entities, ETFs, funds, indices, or private companies |
| **Peer_Role** | The six-role taxonomy from PGMF: core_peer, adjacent_peer, benchmark_context, etf_peer, excluded_non_peer, private_comparable_context |
| **Drift** | Any unauthorized deviation from the approved methodology, candidate states, source authorities, or architectural boundaries |


---

## Requirements

### Requirement 1: PGMF Dependency

**User Story:** As a CTO, I want the preflight to treat the completed PGMF artifacts as the sole methodology authority, so that all candidate records are grounded in verified, institutionally sourced methodology rather than ad-hoc decisions.

#### Acceptance Criteria

1. WHEN the Preflight begins execution, THE Preflight SHALL verify that the PGMF verification gate artifact (`artifacts/gate_vg_pgmf_1.md`) exists and records a PASS result for VG-PGMF-1 before proceeding with any candidate record preparation.
2. THE Preflight SHALL treat the completed PGMF specification (12/12 tasks, VG-PGMF-1 PASS) as the only methodology authority for candidate record preparation.
3. WHEN a candidate record field with scope label CURRENT_METHODOLOGY requires methodology justification, THE Preflight SHALL reference the corresponding PGMF decision (PGMF-DEC-01 through PGMF-DEC-10) as the governing rule.
4. THE Preflight SHALL reference the PGMF artifacts located at `.kiro/specs/peer-group-registry-methodology-framework/artifacts/` as the source of truth for field taxonomy, peer role taxonomy, governance rules, and boundary definitions.
5. IF a candidate record requires methodology not covered by any PGMF decision (PGMF-DEC-01 through PGMF-DEC-10), THEN THE Preflight SHALL classify that record as CANDIDATE_BLOCKED with a gap rationale documenting: the uncovered field or rule, the PGMF decisions evaluated, and the reason no existing decision applies.
6. THE Preflight SHALL NOT create, modify, or extend PGMF methodology decisions — methodology extension requires a separate spec with human/CTO approval.
7. IF the PGMF verification gate artifact is missing or records a result other than PASS, THEN THE Preflight SHALL halt execution and produce a PGMF_DEPENDENCY_UNMET error indicating that preflight cannot proceed without a completed PGMF.

---

### Requirement 2: Family Universe Intake

**User Story:** As a CTO, I want the preflight to define an intake structure for the 9 confirmed family universes, so that candidate record preparation has a systematic, traceable starting point for each family.

#### Acceptance Criteria

1. THE Preflight SHALL define an intake structure for each of the 9 confirmed family universes (PGF-01 through PGF-09) that captures the following data categories per family: family_id, family_name, purpose statement, core candidate universe tickers (with count), adjacent/subcluster candidate tickers (with count), subcluster notes and candidate subcluster definitions, benchmark/context instrument candidates, boundary notes, and unresolved decisions — all as documented in the scope preflight artifact.
2. WHEN a family universe is ingested, THE Preflight SHALL record the core candidate universe tickers, adjacent/subcluster candidate tickers, benchmark/context instrument candidates, subcluster candidate definitions with rationale, and unresolved decisions from the scope preflight document; IF a data category is absent for a given family (e.g., PGF-08 has zero adjacent candidates), THEN THE Preflight SHALL explicitly record that category as NONE_IN_SOURCE rather than omitting it.
3. WHEN PGF-09 (ETF / Fund Peer Rule) is ingested, THE Preflight SHALL record the rule statement, required ETF/fund comparison dimensions (10 dimensions as defined in the scope preflight), and subcluster rules in place of core/adjacent ticker lists, since PGF-09 is rule-based rather than ticker-based.
4. THE Preflight SHALL trace every family universe intake to the scope preflight artifact at `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` as the source document by recording the source file path and the specific section reference (e.g., "Section 5, Family PGF-01") for each ingested data point.
5. THE Preflight SHALL NOT add tickers, families, subclusters, or benchmark instruments beyond those confirmed in the scope preflight without explicit human/CTO approval.

---

### Requirement 3: Candidate-Only Record Status

**User Story:** As a CTO, I want all records produced by this preflight to carry candidate-only status, so that no preflight output is mistaken for production registry content.

#### Acceptance Criteria

1. During future preflight task execution, when a candidate record draft is produced, THE Preflight SHALL assign it an initial Candidate_Status of CANDIDATE_DRAFT; the only permitted Candidate_Status values across the record lifecycle are: CANDIDATE_DRAFT, CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, CANDIDATE_CONTEXT_ONLY, or CANDIDATE_READY_FOR_REVIEW.
2. THE Preflight SHALL NOT assign any record a lifecycle_status value of ACTIVE or APPROVED, a canonical peer_group_id, or any status value outside the permitted Candidate_Status set defined in criterion 1.
3. During future preflight task execution, when a candidate record draft is produced, THE Preflight SHALL embed a `production_authority: NONE` field indicating the record carries no production weight.
4. THE Preflight SHALL NOT create peer_group_registry.yaml, or any file whose name contains "registry" without a `candidate_` prefix or `_preflight` suffix, or any file whose name contains "production", "canonical", or "approved" in reference to peer group records.
5. IF a downstream process consumes a candidate record without verifying that production_authority equals NONE and Candidate_Status equals CANDIDATE_READY_FOR_REVIEW with human/CTO approval recorded, THEN THE Preflight SHALL define a blocking rule specifying that candidate records lacking human/CTO approval evidence (approver identity, approval date, approval scope) SHALL be rejected by the consuming process.


---

### Requirement 4: Source Authority Mapping

**User Story:** As a CTO, I want every candidate record to carry source authority evidence, so that no peer methodology decision exists without institutional traceability.

#### Acceptance Criteria

1. THE Preflight SHALL require every candidate record to reference at least one Source_Authority from the PGMF source registry (`.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`) for each methodology-decision field classified as CURRENT_METHODOLOGY in the PGMF field taxonomy.
2. WHEN a candidate record references a source, THE Preflight SHALL record the source ID (e.g., SRC-B-01), authority domain (e.g., classification_authority), and tier level (Tier 1, Tier 2, or Tier 3) at the field level, linking each methodology-decision field to its justifying source.
3. IF a candidate record methodology-decision field cannot be traced to any source in the PGMF source registry, THEN THE Preflight SHALL classify that field as SOURCE_EVIDENCE_MISSING and set the record Candidate_Status to CANDIDATE_BLOCKED with a documented gap rationale identifying the missing evidence.
4. IF a source is referenced outside its designated authority domain (e.g., a classification_authority source cited for financial_comparability decisions), THEN THE Preflight SHALL reject that source-to-field mapping, flag the field as DOMAIN_SCOPE_VIOLATION, and set the record Candidate_Status to CANDIDATE_BLOCKED until a valid within-domain source is provided.
5. THE Preflight SHALL enforce that a Tier 1 source produces hard rules only within its designated authority domain and that Tier 2 and Tier 3 sources do not override Tier 1 sources within that domain.

---

### Requirement 5: Field Taxonomy Mapping

**User Story:** As a CTO, I want candidate records to be mapped against the PGMF field taxonomy, so that every candidate record demonstrates structural compliance with the methodology framework without requiring production IDs.

#### Acceptance Criteria

1. THE Preflight SHALL map each candidate record against the PGMF field taxonomy reference artifact (`field_taxonomy_reference_2026-06-08.md`) to verify structural completeness, where structural completeness means: all fields with requirement status REQUIRED for the record's asset_type are present and carry a non-empty value, all fields with requirement status REQUIRED_IF_AVAILABLE are either populated or carry a documented gap rationale, and all fields with requirement status NOT_APPLICABLE for the record's asset_type are absent or explicitly marked NOT_APPLICABLE.
2. During future preflight task execution, when a candidate record draft is prepared, THE Preflight SHALL populate CURRENT_METHODOLOGY fields as defined in PGMF, set CURRENT_MODEL_NULLABLE fields to null, set DEFERRED fields to their mandated deferred value (e.g., threshold_calibration_status = NUMERIC_THRESHOLDS_DEFERRED), and mark FUTURE_SCOPE fields as NOT_POPULATED_IN_PREFLIGHT.
3. THE Preflight SHALL NOT assign values other than NOT_POPULATED_IN_PREFLIGHT or FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL to any field marked FUTURE_SCOPE, FUTURE_VENDOR_INTEGRATION, or FUTURE_COMPLIANCE_REFERENCE in the PGMF field taxonomy.
4. THE Preflight SHALL NOT mint or assign canonical peer_group_id values — the peer_group_id field in candidate records SHALL carry the value PREFLIGHT_PLACEHOLDER_NOT_CANONICAL.
5. WHEN a candidate record is missing a REQUIRED field from the PGMF asset-type-aware identity matrix (PGMF-DEC-04), THE Preflight SHALL document the gap by recording the missing field name, the asset_type requiring it, and the source authority domain responsible, and set Candidate_Status to CANDIDATE_BLOCKED until the gap is resolved.
6. WHEN mapping fields for a candidate record, THE Preflight SHALL determine field applicability by referencing the record's asset_type value against the asset_type applicability column in the field taxonomy, applying only those fields whose applicability includes the record's asset_type.

---

### Requirement 6: ETF/Fund Boundary Preservation

**User Story:** As a CTO, I want the preflight to preserve the ETF/Fund methodology boundary from PGMF, so that ETF assets are never incorrectly treated as company peers during candidate preparation.

#### Acceptance Criteria

1. THE Preflight SHALL enforce the PGMF-DEC-05 rule: ETFs and funds (asset_type ∈ {etf, fund}) are never company peers; within PGF-09, ETF/fund assets use peer_role = etf_peer; as reference instruments in company families (PGF-01 through PGF-08), they use peer_role = benchmark_context exclusively.
2. THE Preflight SHALL NOT produce any candidate record where an ETF or fund asset (asset_type ∈ {etf, fund}) carries peer_role = core_peer or peer_role = adjacent_peer against a company asset, nor any candidate record where a company asset (asset_type = company) carries peer_role = etf_peer.
3. WHEN preparing PGF-09 candidate records, THE Preflight SHALL require structural presence of the ETF/fund comparison field set (benchmark_index, TER, AUM, tracking_difference, tracking_error, spread, holdings_overlap, replication_method, distribution_policy, lookthrough_concentration) as defined in PGMF-DEC-05, with each field populated where source data is available or documented as SOURCE_EVIDENCE_MISSING where unavailable.
4. IF an ETF-to-company boundary violation is detected in any candidate record — defined as an ETF or fund asset assigned peer_role ∈ {core_peer, adjacent_peer} against a company asset, or a company asset assigned peer_role = etf_peer — THEN THE Preflight SHALL reject that record, set its Candidate_Status to CANDIDATE_BLOCKED, and log a BOUNDARY_VIOLATION_ETF_COMPANY_FALLBACK error documenting the violating asset, the invalid peer_role, and the target asset.
5. WHEN an ETF or fund asset appears as benchmark_context in a company family (PGF-01 through PGF-08), THE Preflight SHALL NOT populate ETF-specific comparison fields (TER, AUM, tracking_difference, tracking_error, spread, holdings_overlap, replication_method, distribution_policy, lookthrough_concentration) on that record, as those fields apply only within PGF-09 etf_peer comparisons.

---

### Requirement 7: Cross-Region Comparability

**User Story:** As a CTO, I want the preflight to require explicit comparability treatment for cross-region candidates, so that false peer comparisons arising from accounting, currency, or listing differences are prevented at the candidate stage.

#### Acceptance Criteria

1. WHEN a candidate record involves cross-region peers (where any two assets in the same family differ in accounting_standard, reporting_currency, or domicile), THE Preflight SHALL require explicit values for: accounting_standard, reporting_currency, trading_currency, fiscal_year_end, taxonomy_reference, comparability_adjustment_required, and comparability_note on each cross-region asset record.
2. IF a candidate record has comparability_adjustment_required = true but comparability_note is null or zero-length, THEN THE Preflight SHALL set that record's Candidate_Status to CANDIDATE_BLOCKED with reason CROSS_REGION_COMPARABILITY_INCOMPLETE.
3. THE Preflight SHALL require listing_variant_type identification (primary, ADR, GDR, or secondary) for every asset that has 2 or more listing venues, including the exchange_mic for each listing (e.g., TSM on TWSE and NYSE, ASML on XAMS and XNAS).
4. IF a candidate record's accounting_standard differs from any proposed peer's accounting_standard within the same family (GAAP vs. IFRS), THEN THE Preflight SHALL require comparability_adjustment_required = true on both records, consistent with PGMF-DEC-08; records that fail this check SHALL be set to CANDIDATE_BLOCKED with reason CROSS_STANDARD_COMPARISON_UNACKNOWLEDGED.
5. WHILE preparing candidate records for PGF-06 (European defense), PGF-07 (European industrials), and PGF-08 (European banks), THE Preflight SHALL document currency normalization requirements for EUR, GBP, CHF, and SEK-denominated peers by recording reporting_currency, trading_currency, and comparability_note identifying which currency conversions affect metric comparability for each non-USD-reporting asset.
6. IF a cross-region candidate record is missing any of the 7 required cross-region fields (accounting_standard, reporting_currency, trading_currency, fiscal_year_end, taxonomy_reference, comparability_adjustment_required, comparability_note), THEN THE Preflight SHALL set Candidate_Status to CANDIDATE_BLOCKED with reason CROSS_REGION_FIELDS_INCOMPLETE and document which fields are missing.


---

### Requirement 8: Unsupported Asset Protection

**User Story:** As a CTO, I want the preflight to block unsupported asset classes from receiving peer assignments, so that only assets with defined methodology coverage enter the candidate pipeline.

#### Acceptance Criteria

1. THE Preflight SHALL block the following asset classes from receiving any peer_role other than excluded_non_peer or private_comparable_context: derivatives, options, warrants, certificates, leveraged products, structured products, crypto/tokenized assets, commodities, FX pairs, bonds/fixed-income, money-market instruments, indices (except where peer_role = benchmark_context), baskets, synthetic exposures, private equity (except where peer_role = private_comparable_context), and unresolved identities.
2. WHEN an asset's object_type matches any entry in the unsupported asset class list defined in criterion 1, THE Preflight SHALL assign it a Candidate_Status of UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION, set peer_comparison_allowed = false, and restrict its peer_role to excluded_non_peer (or private_comparable_context / benchmark_context where the stated exceptions apply).
3. THE Preflight SHALL NOT invent ad-hoc peer sets to fill coverage gaps for unsupported asset classes, consistent with PGMF Section 7 and scope preflight Section 8.2.
4. IF an asset's canonical_object_id cannot be resolved to an object_type within the set of types supported by PGMF methodology (equities, ETFs, funds, and the exception-qualified types in criterion 1), THEN THE Preflight SHALL classify that asset as IDENTITY_UNRESOLVED and set Candidate_Status to CANDIDATE_BLOCKED.
5. IF an asset already referenced in a confirmed family universe (PGF-01 through PGF-09) is determined to carry an unsupported object_type, THEN THE Preflight SHALL remove that asset from active candidate preparation for the family, set its Candidate_Status to UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION, and document the removal in the family's candidate evidence record.

---

### Requirement 9: Market Data Boundary

**User Story:** As a CTO, I want the preflight to enforce that market data availability is not treated as peer methodology eligibility, so that candidate records are based on methodology logic rather than data vendor coverage.

#### Acceptance Criteria

1. THE Preflight SHALL NOT use market data availability (price feeds, data vendor coverage, exchange connectivity) as a criterion for peer methodology eligibility or peer_role assignment.
2. THE Preflight SHALL mark all market data readiness fields (market_data_source, data_vendor, data_latency_class, exchange_timezone, trading_calendar_id, derived_data_policy, index_license_required, and all FUTURE_VENDOR_INTEGRATION fields including realtime_entitlement_required, display_usage_allowed, non_display_usage_allowed, redistribution_allowed, professional_user_flag, market_data_audit_required, bid_ask_source, stale_quote_threshold, and quote_timestamp_required) as NOT_POPULATED_IN_PREFLIGHT in candidate records.
3. IF a candidate record lacks market data coverage, THEN THE Preflight SHALL NOT downgrade or block that record's peer methodology eligibility on market data grounds alone, where market data grounds are defined as any factor enumerated in criterion 1 (price feeds, data vendor coverage, exchange connectivity).
4. THE Preflight SHALL enforce the PGMF market data boundary rule by requiring that no peer_role assignment, no Candidate_Status transition, and no financial_comparability_gate_status decision references market data availability, vendor coverage, or exchange connectivity as an input factor.
5. WHEN VG-PGRC-PREFLIGHT-1 executes market data boundary verification, THE Preflight SHALL confirm that zero candidate records have peer_role or Candidate_Status values that were derived from or conditioned on market data field availability.

---

### Requirement 10: Trading Boundary

**User Story:** As a CTO, I want the preflight to enforce that no tradability, execution eligibility, broker connectivity, order-routing authority, or trading readiness is inferred from peer methodology, so that the candidate pipeline remains methodology-only.

#### Acceptance Criteria

1. THE Preflight SHALL NOT produce, derive, calculate, or store any value indicating tradability, execution eligibility, broker connectivity, order-routing authority, or trading readiness from any peer methodology decision or candidate record.
2. THE Preflight SHALL mark all trading governance fields (execution_venue_eligible, best_execution_required, order_routing_policy_required, pre_trade_controls_required, price_collar_policy, max_order_value_policy, kill_switch_required, audit_log_required, surveillance_required, market_abuse_monitoring_required, tradability_status, trading_enabled, trade_block_reason) as FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL in candidate records.
3. THE Preflight SHALL NOT create or produce output containing connectivity endpoints, connection strings, venue identifiers, or language asserting active connectivity to any broker, exchange, ATS, or trading venue.
4. THE Preflight SHALL NOT produce any output that states, asserts, or represents MoneyHorst as a broker-dealer, investment firm, exchange participant, or regulated trading venue.
5. IF any candidate record is found with a trading governance field set to a value other than FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL, THEN THE Preflight SHALL reject that record and classify the violation as TRADING_BOUNDARY_VIOLATION with the affected field name and invalid value documented.


---

### Requirement 11: SAI Compatibility Boundary

**User Story:** As a CTO, I want the preflight to define future-safe candidate interpretation boundaries without mutating SAI artifacts, so that SAI remains stable while the candidate pipeline is prepared.

#### Acceptance Criteria

1. THE Preflight SHALL NOT mutate any SAI artifact, SAI gate, SAI requirement, SAI task plan, or SAI verification status.
2. THE Preflight SHALL define candidate interpretation boundaries that satisfy all three compatibility dimensions from `.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md` Section 2.3: (a) candidate records do not violate "What SAI Must NOT Define" constraints, (b) candidate record shape does not conflict with "What SAI Expects to Consume" field expectations, and (c) candidate records carry no production authority that would trigger SAI operational consumption.
3. WHEN defining candidate record output shape, THE Preflight SHALL include all 17 fields from the SAI output contract (PGMF Section 10.3): peer_group_available, peer_comparison_allowed, blocked_reason, unsupported_status, primary_family, secondary_family, peer_role, core_peer_set, adjacent_peer_set, benchmark_context_set, etf_peer_set, comparison_mode_allowed, financial_comparability_gate_status, comparability_note, data_quality_status, as_of_date, methodology_version — with each field carrying either a derivable candidate value or the explicit placeholder value PREFLIGHT_NOT_CANONICAL to indicate non-production status.
4. THE Preflight SHALL document that SAI-BLK-21 (Peer Comparison) remains in BLOCK_FINAL_PEER_ASSIGNMENT state with peer_comparison_allowed = false and blocked_reason referencing "Peer Group Registry not yet available" until a production registry is created and human/CTO approved — candidate records do not satisfy the SAI deferred interface and do not unblock SAI-BLK-21.
5. THE Preflight SHALL preserve the no-ad-hoc-peer rule: SAI must never create ad-hoc peers to compensate for a missing or candidate-only registry entry, consistent with the SAI deferred interface prohibition on peer group composition decisions.
6. IF a candidate record output shape omits any of the 17 SAI output contract fields or assigns a production-authority value to any field, THEN THE Preflight SHALL reject that record with a SAI_CONTRACT_SHAPE_VIOLATION error and set Candidate_Status to CANDIDATE_BLOCKED.

---

### Requirement 12: Human Approval Gate

**User Story:** As a CTO, I want the preflight to require human/CTO approval before any candidate record can become production registry content, so that no automated process elevates draft records to production status.

#### Acceptance Criteria

1. THE Preflight SHALL define a human/CTO approval gate as a mandatory prerequisite before any Candidate_Record transitions from CANDIDATE_READY_FOR_REVIEW to production status.
2. THE Preflight SHALL require that human/CTO approval is recorded with: approver identity (CTO or explicitly CTO-delegated reviewer), approval decision (one of: APPROVED, DENIED, CONDITIONAL), approval date, approval scope (which specific records and/or families are approved), and if CONDITIONAL, a structured list of conditions that must be satisfied before re-submission.
3. THE Preflight SHALL NOT define any automated pathway that bypasses human/CTO approval for production elevation.
4. WHEN all candidate records for a family universe reach CANDIDATE_READY_FOR_REVIEW, THE Preflight SHALL produce a family-level approval request artifact documenting: the complete list of candidate records with their Candidate_Status history, source authority references per record, evidence gaps (if any remain as accepted risks), field taxonomy compliance summary, and a recommendation section for human/CTO review.
5. IF human/CTO approval is denied or conditional, THEN THE Preflight SHALL return rejected records to CANDIDATE_DRAFT or CANDIDATE_BLOCKED with documented rejection rationale, and require that reworked records re-enter the approval gate by transitioning back through CANDIDATE_READY_FOR_REVIEW and producing an updated approval request artifact before a subsequent approval decision may be recorded.
6. IF human/CTO approval decision is CONDITIONAL, THEN THE Preflight SHALL require that all stated conditions are resolved and documented before the affected records may be re-submitted to the approval gate for a subsequent APPROVED or DENIED decision.

---

### Requirement 13: Preflight Output Restrictions

**User Story:** As a CTO, I want the preflight to produce only preflight specifications and draft artifacts, so that no production registry files or production-authority outputs are created prematurely.

#### Acceptance Criteria

1. THE Preflight SHALL produce only: preflight specification documents, candidate record draft artifacts, mapping worksheets, evidence gap documentation, and verification gate artifacts.
2. THE Preflight SHALL NOT produce: peer_group_registry.yaml, any file containing "registry" in its name that lacks the `candidate_` prefix or `_preflight` suffix, any file containing canonical peer_group_id values, any runtime code, any validation code, or any executable implementation.
3. THE Preflight SHALL NOT produce any artifact that carries lifecycle_status = ACTIVE, lifecycle_status = APPROVED, or production_authority other than NONE.
4. WHEN naming output artifacts, THE Preflight SHALL use the prefix `candidate_` or suffix `_preflight` on every output filename to distinguish draft outputs from production artifacts.
5. THE Preflight SHALL NOT produce artifacts that imply final peer assignments — specifically, no candidate record may omit the Candidate_Status field, contain lifecycle_status = ACTIVE or APPROVED, or present peer_role values without an accompanying `preliminary: true` indicator.
6. IF any preflight output artifact violates criteria 1 through 5 (forbidden filename, forbidden field value, missing naming convention, or missing Candidate_Status), THEN THE Preflight SHALL halt production of that artifact, log an OUTPUT_RESTRICTION_VIOLATION error documenting the violation type and affected file, and set the associated record's Candidate_Status to CANDIDATE_BLOCKED.

---

### Requirement 14: Verification Gate

**User Story:** As a CTO, I want the preflight to define a verification gate that must pass before any future registry creation spec can start, so that downstream work cannot begin on an incomplete or non-compliant preflight.

#### Acceptance Criteria

1. THE Preflight SHALL define a verification gate (VG-PGRC-PREFLIGHT-1) that must produce a single aggregate PASS or FAIL verdict, documented in a verification gate artifact, before any future registry creation spec may begin.
2. WHEN VG-PGRC-PREFLIGHT-1 is executed, THE Preflight SHALL verify the following 6 check categories, all of which must pass for an aggregate PASS verdict: (a) all 9 family universes have at least one candidate record with a valid Candidate_Status value or an explicit CANDIDATE_BLOCKED record documenting why processing could not proceed, (b) every candidate record carries a Candidate_Status value from the defined set (CANDIDATE_DRAFT, CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, CANDIDATE_CONTEXT_ONLY, CANDIDATE_READY_FOR_REVIEW), (c) every candidate record references at least one Source_Authority from the PGMF source registry, (d) every candidate record has all CURRENT_METHODOLOGY fields from the PGMF field taxonomy either populated or explicitly documented as a gap with Candidate_Status set to CANDIDATE_BLOCKED, (e) zero BOUNDARY_VIOLATION errors exist across all candidate records for ETF, market data, trading, SAI, and unsupported asset boundaries as defined in Requirements 6 through 10, and (f) the human approval gate structure from Requirement 12 is defined and referenceable.
3. IF VG-PGRC-PREFLIGHT-1 fails any of the 6 check categories, THEN THE Preflight SHALL set the aggregate verdict to FAIL, block downstream registry creation work, and produce a failure report documenting which check categories failed, the specific records or families affected, and what remediation is required for each failure.
4. THE Preflight SHALL produce a verification gate artifact (`gate_vg_pgrc_preflight_1.md`) containing: the aggregate PASS/FAIL verdict, each of the 6 check categories with its individual pass/fail status, the artifact path or cross-reference to the source evidence supporting each check result, and a timestamp indicating when the gate was executed.
5. THE Preflight SHALL define that VG-PGRC-PREFLIGHT-1 must be explicitly executed as a leaf task — it must not be auto-completed, auto-inferred, or child-derived from other task completions.


---

### Requirement 15: Drift Prevention

**User Story:** As a CTO, I want the preflight to explicitly block all forms of drift, so that the candidate pipeline does not silently deviate from the approved methodology, source authorities, candidate states, or architectural boundaries.

#### Acceptance Criteria

1. THE Preflight SHALL explicitly block registry drift: no candidate record may silently transition to production status without passing through the human approval gate defined in Requirement 12.
2. THE Preflight SHALL explicitly block ID drift: no canonical peer_group_id values may be minted, assigned, or implied during the preflight phase — all ID fields remain PREFLIGHT_PLACEHOLDER_NOT_CANONICAL.
3. THE Preflight SHALL explicitly block peer assignment drift: no candidate record's peer_role may be treated as a final assignment — all peer_role values are preliminary and carry Candidate_Status indicating non-production state.
4. THE Preflight SHALL explicitly block source authority drift: no candidate record may reference sources outside the PGMF source registry (`.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`) without explicit human/CTO approval for source extension recorded with approver identity and approval date.
5. THE Preflight SHALL explicitly block market data drift: no market data availability, vendor coverage, or exchange connectivity may influence peer methodology eligibility during the preflight.
6. THE Preflight SHALL explicitly block SAI drift: no SAI artifact, gate, requirement, or verification status may be modified by the preflight process.
7. THE Preflight SHALL explicitly block runtime drift: no runtime code, validation logic, API endpoints, database schemas, or executable implementations may be created during the preflight.
8. THE Preflight SHALL explicitly block trading drift: no tradability status, execution eligibility, broker connectivity, order-routing authority, or trading readiness may be inferred, implied, or created during the preflight.
9. WHEN any drift category is detected during a candidate record state transition or field population, THE Preflight SHALL halt processing for the affected record, set its Candidate_Status to CANDIDATE_BLOCKED with blocking reason referencing the drift category, and produce a DRIFT_VIOLATION entry in the verification gate artifact documenting: the drift category (one of the 8 defined categories), the affected record identifier, the specific field or value that violated the drift rule, and the required remediation action.
10. THE Preflight SHALL define a drift detection checklist as part of VG-PGRC-PREFLIGHT-1 that explicitly verifies zero drift across all 8 drift categories (registry, ID, peer assignment, source authority, market data, SAI, runtime, trading), where each checklist item produces a per-category pass/fail result with the count of records inspected and the count of violations found (expected: 0 for each category).
11. IF a candidate record receives a DRIFT_VIOLATION block, THEN THE Preflight SHALL require the drift violation to be resolved and the record to return to CANDIDATE_DRAFT before it may resume processing toward CANDIDATE_READY_FOR_REVIEW.

---

## Evidence Foundation

All preflight decisions trace to the following completed artifacts:

| Artifact | Path | Role |
|----------|------|------|
| PGMF Requirements v2 | `.kiro/specs/peer-group-registry-methodology-framework/requirements.md` | Methodology authority (hardened, Q1–Q10) |
| PGMF Design | `.kiro/specs/peer-group-registry-methodology-framework/design.md` | Three-layer model, methodology chain, component architecture |
| PGMF README | `.kiro/specs/peer-group-registry-methodology-framework/README_peer_group_registry_methodology_framework.md` | Framework status: COMPLETE_PENDING_FINAL_HUMAN_REVIEW |
| PGMF Tasks (12/12) | `.kiro/specs/peer-group-registry-methodology-framework/tasks.md` | All tasks complete, VG-PGMF-1 PASS |
| Scope Preflight | `.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md` | 9 confirmed family universes (candidate scope) — **sole authority for family universe content** |
| Source Registry | `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md` | 35 institutional sources across 9 categories |
| Evidence Matrix | `.domainization/reports/peer_group_methodology_evidence_matrix_2026-06-08.md` | Q1–Q10 evidence mapping |
| SAI Deferred Interfaces | `.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md` | Section 2.3 — Peer Group Registry interface contract |
| SAI Compatibility Verification | `.kiro/specs/peer-group-registry-methodology-framework/artifacts/sai_compatibility_verification_2026-06-08.md` | 10 blocking states, 12 scenarios |
| Field Taxonomy Reference | `.kiro/specs/peer-group-registry-methodology-framework/artifacts/field_taxonomy_reference_2026-06-08.md` | Complete field catalog (~90 fields) |
| VG-PGMF-1 Gate | `.kiro/specs/peer-group-registry-methodology-framework/artifacts/gate_vg_pgmf_1.md` | 16 checks PASS, 10 drift categories NONE |

**Family Universe Authority Rule**: The scope preflight document (`.domainization/reports/peer_group_registry_scope_preflight_2026-06-07.md`) is the sole authority for the 9 confirmed family universes. No new family universe, ticker, subcluster, or benchmark instrument may be invented, added, or implied by this spec or any of its future task artifacts without explicit human/CTO approval recorded with approver identity and approval date.

---

## The 9 Confirmed Family Universes

For reference, the confirmed families from the scope preflight:

| Family ID | Family Name | Core Universe Size | Adjacent Size |
|-----------|-------------|-------------------|---------------|
| PGF-01 | AI Semiconductors / AI Infrastructure | 11 | 4 |
| PGF-02 | Cybersecurity / SaaS Security | 9 | 3 |
| PGF-03 | Payments / Networks / Merchant Acquiring | 9 | 4 |
| PGF-04 | Mobility / Delivery / Local Commerce Platforms | 9 | 4 |
| PGF-05 | Consumer / Retail / Event Consumption | 11 | 5 |
| PGF-06 | Defense / Security / C-UAS / Public Safety AI | 12 | 4 |
| PGF-07 | Industrials / Power / Grid / Cooling | 9 | 4 |
| PGF-08 | Banks / Financials | 10 | 0 |
| PGF-09 | ETF / Fund Peer Rule | N/A (rule-based) | N/A |

---

## Candidate Record Lifecycle

```
CANDIDATE_DRAFT
    ↓ (field taxonomy mapping complete, source authority assigned)
CANDIDATE_READY_FOR_REVIEW
    ↓ (human/CTO approval granted)
[Future: PRODUCTION — outside this preflight scope]

CANDIDATE_BLOCKED
    ↓ (blocking condition resolved)
CANDIDATE_DRAFT (re-enters pipeline)

CANDIDATE_DEFERRED
    (requires future methodology extension — not actionable in this preflight)

CANDIDATE_CONTEXT_ONLY
    (private_comparable_context or benchmark_context — limited use, no peer comparison)
```

---

## Preflight Readiness Status

```
PEER_GROUP_REGISTRY_CREATION_PREFLIGHT_REQUIREMENTS_HARDENED_READY_FOR_DESIGN
```

---

## Pre-Design Readiness Checklist

| # | Check | Status |
|---|-------|--------|
| 1 | PGMF completion referenced (12/12 tasks, VG-PGMF-1 PASS) | YES |
| 2 | VG-PGMF-1 PASS referenced as mandatory prerequisite | YES |
| 3 | 9 family universes referenced (PGF-01 through PGF-09) | YES |
| 4 | Source authority basis referenced (PGMF source registry, 35 sources, 9 categories) | YES |
| 5 | Candidate-only boundary defined (Requirement 3) | YES |
| 6 | No production registry creation (Requirement 13) | YES |
| 7 | No final peer assignment (Requirements 3, 15) | YES |
| 8 | No canonical peer_group_id creation (Requirements 5, 15) | YES |
| 9 | No SAI mutation (Requirement 11) | YES |
| 10 | No runtime code (Requirements 13, 15) | YES |
| 11 | No market data integration (Requirement 9) | YES |
| 12 | No trading or execution scope (Requirement 10) | YES |
| 13 | Requirements ready for design | YES |

**Pre-design gate**: design.md may proceed only after this checklist is confirmed and hardened requirements are accepted.

---

*End of requirements document v2 (hardened).*
