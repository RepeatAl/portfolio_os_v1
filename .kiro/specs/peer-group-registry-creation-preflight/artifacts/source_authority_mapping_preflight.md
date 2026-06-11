# Source Authority Mapping Specification

> **Peer Group Registry Creation Preflight — Task 4: Source Authority Mapping**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture
> production_authority: NONE | preliminary: true

---

## Document Boundary

This artifact defines source authority mapping rules only. It does not populate source references on candidate records, create candidate records, create registry files, assign peers, mint peer_group_id values, or produce production content. All mapping tables and rules defined herein govern future preflight task execution.

---

## 1. Field-Level Source Authority Requirement

**Core Rule**: Every CURRENT_METHODOLOGY field in a candidate record requires at least one source reference from the PGMF source registry (`.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`).

| Principle | Rule |
|-----------|------|
| Minimum coverage | At least one Source_Authority reference per methodology-decision field |
| Source registry scope | Only sources registered in the PGMF source registry may be cited |
| Authority domain constraint | Each source may only be cited within its designated authority_domain |
| Tier enforcement | Tier 1 sources produce hard rules; Tier 2/3 sources support but do not override Tier 1 within the same domain |
| Gap handling | If a CURRENT_METHODOLOGY field cannot trace to any PGMF source → SOURCE_EVIDENCE_MISSING → CANDIDATE_BLOCKED |

---

## 2. Source Reference Structure

Every source authority reference on a candidate record field follows this structure:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `source_id` | string | Unique identifier from PGMF source registry | SRC-B-01 |
| `authority_domain` | enum | The designated authority domain of the source | classification_authority |
| `tier_level` | enum | Institutional authority tier (Tier 1 / Tier 2 / Tier 3) | Tier 1 |
| `field_name` | string | The specific candidate record field being justified | primary_family |
| `methodology_decision` | string | The PGMF-DEC governing this field-source relationship | PGMF-DEC-01 |

### Authority Domain Registry

The following authority domains are recognized in the PGMF source registry:

| Authority Domain | Description | Primary Sources |
|-----------------|-------------|-----------------|
| `classification_authority` | Taxonomy classification, family assignment, sector/industry mapping | SRC-B-01, SRC-B-02, SRC-B-03, SRC-C-01, SRC-C-02 |
| `strategic_peer_logic_authority` | Competitive positioning, peer role logic, multi-family rationale | SRC-D-01 |
| `financial_comparability_authority` | Comparability gates, valuation peer eligibility, margin/growth comparability | SRC-E-01, SRC-E-02, SRC-E-03 |
| `ETF_methodology_authority` | ETF/fund comparison dimensions, tracking metrics, replication method | SRC-F-01, SRC-F-02, SRC-F-03, SRC-F-04 |
| `identity_authority` | Entity identification, security-level IDs, listing normalization | SRC-G-01, SRC-G-02, SRC-G-03, SRC-I-01 |
| `accounting_authority` | Accounting standards, GAAP/IFRS comparability, cross-region normalization | SRC-H-01, SRC-H-02, SRC-H-03 |
| `governance_authority` | Methodology versioning, review governance, disclosure standards | SRC-A-01, SRC-A-02, SRC-A-03 |
| `market_data_authority` | Exchange identification, data licensing, venue normalization | SRC-I-01 through SRC-I-07 |
| `future_trading_reference` | Future compliance vocabulary only — not operational | SRC-I-08 through SRC-I-11 |


---

## 3. Methodology-Decision Field Mapping Table

The following table maps each PGMF methodology decision (PGMF-DEC-01 through PGMF-DEC-10) to the CURRENT_METHODOLOGY fields it governs and the source authority domains those fields require.

### 3.1 PGMF-DEC-01 (Q1) — Peer Group Organization Principle

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `canonical_object_id` | REQUIRED | identity_authority | SRC-G-01, SRC-G-02, SRC-I-01 | Tier 1 |
| `object_type` | REQUIRED | identity_authority | SRC-G-01, SRC-G-02 | Tier 1 |
| `object_name` | REQUIRED | identity_authority | SRC-G-01, SRC-G-02 | Tier 1 |
| `family_id` | REQUIRED | classification_authority | SRC-B-01, SRC-C-01 | Tier 1 |
| `family_name` | REQUIRED | classification_authority | SRC-B-01, SRC-C-01 | Tier 1 |
| `primary_family` | REQUIRED | classification_authority | SRC-B-01 | Tier 1 |
| `asset_type` | REQUIRED | identity_authority | SRC-G-01, SRC-G-02 | Tier 1 |

### 3.2 PGMF-DEC-02 (Q2) — Multi-Family Membership

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `primary_family` | REQUIRED | classification_authority | SRC-B-01 | Tier 1 |
| `secondary_family` | OPTIONAL | strategic_peer_logic_authority | SRC-D-01 | Tier 1 |

### 3.3 PGMF-DEC-03 (Q3) — Peer Role Taxonomy

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `peer_role` | REQUIRED | strategic_peer_logic_authority / financial_comparability_authority / ETF_methodology_authority | SRC-D-01, SRC-E-01, SRC-F-01 | Tier 1 |
| `comparison_mode_allowed` | REQUIRED | financial_comparability_authority | SRC-E-01 | Tier 1 |
| `valuation_peer_allowed` | REQUIRED | financial_comparability_authority | SRC-E-01, SRC-E-03 | Tier 1 |

### 3.4 PGMF-DEC-04 (Q4) — Entity / Security / Listing Identity Model

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `canonical_object_id` | REQUIRED | identity_authority | SRC-G-01 | Tier 1 |
| `security_id` | REQUIRED | identity_authority | SRC-G-01, SRC-G-02 | Tier 1 |
| `isin` | REQUIRED_IF_AVAILABLE | identity_authority | SRC-G-03 | Tier 2 |
| `figi` | REQUIRED_IF_AVAILABLE | identity_authority | SRC-G-01 | Tier 1 |
| `ticker` | REQUIRED_IF_LISTED | identity_authority | SRC-G-02 | Tier 2 |
| `exchange_mic` | REQUIRED_IF_LISTED | identity_authority | SRC-I-01 | Tier 1 |
| `primary_listing` | REQUIRED_IF_LISTED | identity_authority | SRC-G-01, SRC-G-02 | Tier 1 |
| `listing_variant_type` | REQUIRED_IF_LISTED | identity_authority | SRC-G-01, SRC-G-02 | Tier 1 |
| `adr_flag` | REQUIRED_IF_LISTED | identity_authority | SRC-G-01, SRC-G-02 | Tier 1 |
| `trading_currency` | REQUIRED_IF_LISTED | accounting_authority | SRC-H-01 | Tier 1 |

### 3.5 PGMF-DEC-05 (Q5) — ETF / Fund / Index Boundary

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `benchmark_index` | REQUIRED_IF_APPLICABLE | ETF_methodology_authority | SRC-F-01 | Tier 1 |
| `TER` | REQUIRED_IF_AVAILABLE | ETF_methodology_authority | SRC-F-01, SRC-F-04 | Tier 1 |
| `AUM` | REQUIRED_IF_AVAILABLE | ETF_methodology_authority | SRC-F-01 | Tier 1 |
| `tracking_difference` | REQUIRED_IF_AVAILABLE | ETF_methodology_authority | SRC-F-01, SRC-F-03 | Tier 1 |
| `tracking_error` | REQUIRED_IF_AVAILABLE | ETF_methodology_authority | SRC-F-01 | Tier 1 |
| `spread` | REQUIRED_IF_AVAILABLE | ETF_methodology_authority | SRC-F-01 | Tier 1 |
| `holdings_overlap` | REQUIRED_IF_AVAILABLE | ETF_methodology_authority | SRC-F-02 | Tier 2 |
| `replication_method` | REQUIRED_IF_AVAILABLE | ETF_methodology_authority | SRC-F-01, SRC-F-02 | Tier 1 |
| `distribution_policy` | REQUIRED_IF_AVAILABLE | ETF_methodology_authority | SRC-F-04 | Tier 2 |
| `lookthrough_concentration` | REQUIRED_IF_AVAILABLE | ETF_methodology_authority | SRC-F-02 | Tier 2 |

### 3.6 PGMF-DEC-06 (Q6) — Liquidity / Market-Cap Thresholds

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `market_cap_band` | REQUIRED | financial_comparability_authority | SRC-E-01 | Tier 1 |
| `liquidity_band` | REQUIRED | financial_comparability_authority | SRC-E-01 | Tier 1 |
| `threshold_calibration_status` | REQUIRED (DEFERRED) | financial_comparability_authority | SRC-E-01 | Tier 1 |

### 3.7 PGMF-DEC-07 (Q7) — Private Company Handling

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `peer_role` (= private_comparable_context) | REQUIRED | financial_comparability_authority | SRC-E-01 | Tier 1 |
| `valuation_peer_allowed` (= false) | REQUIRED | financial_comparability_authority | SRC-E-01 | Tier 1 |
| `comparison_mode_allowed` (= ecosystem_context_only) | REQUIRED | financial_comparability_authority | SRC-E-01 | Tier 1 |
| `canonical_object_id` (internal only) | REQUIRED | identity_authority | SRC-G-01 | Tier 1 |

### 3.8 PGMF-DEC-08 (Q8) — Cross-Region Comparability

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `accounting_standard` | REQUIRED | accounting_authority | SRC-H-01, SRC-H-02, SRC-H-03 | Tier 1 |
| `reporting_currency` | REQUIRED | accounting_authority | SRC-H-01 | Tier 1 |
| `trading_currency` | REQUIRED_IF_LISTED | accounting_authority | SRC-H-01 | Tier 1 |
| `fiscal_year_end` | REQUIRED | accounting_authority | SRC-H-01 | Tier 1 |
| `taxonomy_reference` | REQUIRED | classification_authority | SRC-C-01, SRC-B-01 | Tier 1 |
| `comparability_adjustment_required` | REQUIRED | accounting_authority | SRC-H-02, SRC-H-03 | Tier 1 |
| `comparability_note` | REQUIRED_IF_APPLICABLE | accounting_authority | SRC-H-02, SRC-H-03 | Tier 1 |
| `domicile` | REQUIRED | accounting_authority | SRC-H-01 | Tier 1 |

### 3.9 PGMF-DEC-09 (Q9) — Governance and Validation

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `review_cycle` | REQUIRED | governance_authority | SRC-A-01, SRC-B-03, SRC-C-01 | Tier 1 |
| `challenge_status` | REQUIRED | governance_authority | SRC-C-01 | Tier 1 |
| `review_status` | REQUIRED | governance_authority | SRC-A-01 | Tier 1 |
| `subcluster_id` | REQUIRED_IF_APPLICABLE | classification_authority | SRC-B-01, SRC-C-01 | Tier 1 |
| `subcluster_name` | REQUIRED_IF_APPLICABLE | classification_authority | SRC-B-01, SRC-C-01 | Tier 1 |
| `approved_by` | REQUIRED | governance_authority | SRC-A-01, SRC-A-02 | Tier 1 |

### 3.10 PGMF-DEC-10 (Q10) — Versioning and Lifecycle

| Field | Requirement | Source Authority Domain | Primary Sources | Tier |
|-------|-------------|------------------------|-----------------|------|
| `effective_date` | REQUIRED | governance_authority | SRC-A-01, SRC-B-03 | Tier 1 |
| `end_date` | OPTIONAL | governance_authority | SRC-A-01, SRC-B-03 | Tier 1 |
| `lifecycle_status` | REQUIRED | governance_authority | SRC-A-01, SRC-B-03 | Tier 1 |
| `methodology_version` | REQUIRED | governance_authority | SRC-A-01, SRC-A-03 | Tier 1 |
| `change_reason` | OPTIONAL | governance_authority | SRC-A-01, SRC-B-03 | Tier 1 |
| `source_authority` | REQUIRED | governance_authority | SRC-A-01 | Tier 1 |


---

## 4. Financial Comparability Gate Fields — Source Authority Mapping

These fields are governed jointly by PGMF-DEC-03, PGMF-DEC-06, and PGMF-DEC-08. Their source authority domain is `financial_comparability_authority`.

| Field | Source Authority Domain | Primary Sources | Tier |
|-------|------------------------|-----------------|------|
| `business_model_similarity` | financial_comparability_authority | SRC-E-01, SRC-E-03 | Tier 1 |
| `growth_profile_comparable` | financial_comparability_authority | SRC-E-01, SRC-E-03 | Tier 1 |
| `margin_structure_comparable` | financial_comparability_authority | SRC-E-01, SRC-E-03 | Tier 1 |
| `capital_intensity_comparable` | financial_comparability_authority | SRC-E-01, SRC-E-03 | Tier 1 |
| `leverage_comparable` | financial_comparability_authority | SRC-E-01, SRC-E-03 | Tier 1 |
| `comparability_note_required` | financial_comparability_authority | SRC-E-01 | Tier 1 |
| `financial_comparability_gate_status` | financial_comparability_authority | SRC-E-01, SRC-E-03 | Tier 1 |

---

## 5. DOMAIN_SCOPE_VIOLATION Rule

**Rule**: A source may NOT be cited outside its designated authority domain.

### Definition

A DOMAIN_SCOPE_VIOLATION occurs when a source reference is applied to a candidate record field whose source authority domain does not match the source's designated authority_domain in the PGMF source registry.

### Examples

| Violation | Source | Source Domain | Field | Field Domain | Result |
|-----------|--------|--------------|-------|-------------|--------|
| VIOLATION | SRC-B-01 (GICS) | classification_authority | `comparability_adjustment_required` | accounting_authority | DOMAIN_SCOPE_VIOLATION |
| VIOLATION | SRC-E-01 (Damodaran) | financial_comparability_authority | `primary_family` | classification_authority | DOMAIN_SCOPE_VIOLATION |
| VIOLATION | SRC-F-01 (Morningstar ETF) | ETF_methodology_authority | `accounting_standard` | accounting_authority | DOMAIN_SCOPE_VIOLATION |
| VIOLATION | SRC-H-02 (KPMG) | accounting_authority | `peer_role` | strategic_peer_logic_authority | DOMAIN_SCOPE_VIOLATION |
| VALID | SRC-B-01 (GICS) | classification_authority | `primary_family` | classification_authority | ACCEPTED |
| VALID | SRC-E-01 (Damodaran) | financial_comparability_authority | `valuation_peer_allowed` | financial_comparability_authority | ACCEPTED |

### Enforcement

1. When a DOMAIN_SCOPE_VIOLATION is detected, the source-to-field mapping SHALL be rejected
2. The affected field SHALL be flagged as DOMAIN_SCOPE_VIOLATION
3. The candidate record's Candidate_Status SHALL be set to CANDIDATE_BLOCKED
4. The blocked_reason SHALL document: the source_id, the source's designated domain, the field name, and the field's required domain
5. The record remains CANDIDATE_BLOCKED until a valid within-domain source is provided for the affected field

### Testability

A DOMAIN_SCOPE_VIOLATION is testable by comparing:
- `source.authority_domain` (from the PGMF source registry entry)
- `field.source_authority_domain` (from the field taxonomy reference, Section 1 column "Source Authority Domain")

If these values do not match, the violation is confirmed.

---

## 6. SOURCE_EVIDENCE_MISSING Rule

**Rule**: If a CURRENT_METHODOLOGY field cannot trace to any source in the PGMF source registry, the field is flagged as SOURCE_EVIDENCE_MISSING and the record is CANDIDATE_BLOCKED.

### Definition

SOURCE_EVIDENCE_MISSING occurs when:
1. A candidate record contains a CURRENT_METHODOLOGY field (per the PGMF field taxonomy scope classification)
2. That field has requirement status REQUIRED or REQUIRED_IF_APPLICABLE for the record's asset_type
3. No source_authority_reference entry exists linking that field to a source in the PGMF source registry

### Enforcement

1. The affected field SHALL be flagged with source_authority_status = SOURCE_EVIDENCE_MISSING
2. The candidate record's Candidate_Status SHALL be set to CANDIDATE_BLOCKED
3. The blocked_reason SHALL document: the field_name, the expected source_authority_domain, and the statement that no valid source was found in the PGMF source registry
4. The blocking state is BLOCK_SOURCE_INSUFFICIENT
5. The record remains CANDIDATE_BLOCKED until a valid source from the PGMF source registry within the correct authority domain is provided

### Remediation

To resolve SOURCE_EVIDENCE_MISSING:
1. Identify the field's required source_authority_domain from the field taxonomy
2. Locate a source in the PGMF source registry whose authority_domain matches
3. Verify the source's tier_level is appropriate (Tier 1 preferred; Tier 2/3 acceptable as supporting evidence if a Tier 1 source is also cited for the same domain)
4. Record the source_authority_reference with: source_id, authority_domain, tier_level, field_name
5. Update source_authority_status to VERIFIED
6. Transition record from CANDIDATE_BLOCKED back to CANDIDATE_DRAFT for further processing

### Testability

SOURCE_EVIDENCE_MISSING is testable by checking:
- For each CURRENT_METHODOLOGY field with requirement status REQUIRED or REQUIRED_IF_APPLICABLE on the record's asset_type
- Whether `source_authority_references` contains at least one entry where `field_name` matches and `source_id` exists in the PGMF source registry

If no such entry exists, SOURCE_EVIDENCE_MISSING is confirmed.


---

## 7. Tier Hierarchy Enforcement

### Tier Definitions

| Tier | Authority Level | Rule Production | Override Capability |
|------|----------------|-----------------|---------------------|
| **Tier 1** | Official standards, academic authorities, institutional methodology | Produces hard rules within its designated authority domain | Cannot be overridden by Tier 2 or Tier 3 within the same domain |
| **Tier 2** | Institutional research, supplementary methodology, practitioner frameworks | Supports and contextualizes Tier 1 rules; does not produce independent hard rules | Cannot override Tier 1 within the same domain; may supplement |
| **Tier 3** | Educational references, confirmatory context | Confirms widely accepted principles; does not produce rules | Cannot override Tier 1 or Tier 2; context reference only |

### Enforcement Rules

1. **Tier 1 produces hard rules within its domain only**: A Tier 1 source produces binding methodology rules exclusively within its designated authority_domain. A Tier 1 source in `classification_authority` does not produce hard rules for `financial_comparability_authority` fields.

2. **Tier 2/3 support but do not override**: Tier 2 and Tier 3 sources may be cited alongside Tier 1 sources for additional context and confirmation. They may NOT:
   - Override a Tier 1 rule within the same domain
   - Serve as the sole authority for a REQUIRED field when a Tier 1 source exists for the same domain
   - Establish a new hard rule without Tier 1 support

3. **Minimum Tier 1 coverage**: Every authority domain that governs REQUIRED fields MUST have at least one Tier 1 source in the PGMF source registry. If a field's authority domain has no Tier 1 source, the methodology gap must be documented and the record classified as CANDIDATE_BLOCKED.

4. **Tier 2 standalone exception**: A Tier 2 source may serve as primary authority for a REQUIRED_IF_AVAILABLE field ONLY when:
   - No Tier 1 source covers that specific sub-domain
   - The Tier 2 source is institutional research (not educational)
   - The gap is documented in the evidence gap register

### Source Tier Summary (from PGMF Source Registry)

| Authority Domain | Tier 1 Sources | Tier 2 Sources | Tier 3 Sources |
|-----------------|----------------|----------------|----------------|
| classification_authority | SRC-B-01, SRC-B-02, SRC-B-03, SRC-C-01 | SRC-C-02 | — |
| strategic_peer_logic_authority | SRC-D-01 | — | — |
| financial_comparability_authority | SRC-E-01, SRC-E-03 | — | SRC-E-02 |
| ETF_methodology_authority | SRC-F-01 | SRC-F-02, SRC-F-03, SRC-F-04 | — |
| identity_authority | SRC-G-01, SRC-I-01 | SRC-G-02, SRC-G-03 | — |
| accounting_authority | SRC-H-01, SRC-H-02, SRC-H-03 | — | — |
| governance_authority | SRC-A-01, SRC-A-02, SRC-A-03 | — | — |
| market_data_authority | SRC-I-01, SRC-I-02, SRC-I-03, SRC-I-04, SRC-I-05, SRC-I-06 | SRC-I-07 | — |
| future_trading_reference | SRC-I-08, SRC-I-09, SRC-I-10, SRC-I-11 | — | — |

---

## 8. Extension Rule

**Rule**: No external source outside the PGMF source registry may be used for candidate record source authority without explicit human/CTO approval.

### Requirements (per R4 and R15)

This extension rule satisfies:
- **R4 (Source Authority Mapping)**: Requirement that every candidate record references sources from the PGMF source registry
- **R15 (Drift Prevention), criterion 4**: Explicit blocking of source authority drift — no candidate record may reference sources outside the PGMF source registry without explicit human/CTO approval

### Extension Conditions

An external source extension requires ALL of the following recorded before citation:

| Required Field | Description | Example |
|----------------|-------------|---------|
| `approver_identity` | CTO or explicitly CTO-delegated reviewer who approved the extension | "CTO" or "Architecture Lead (CTO-delegated)" |
| `approval_date` | ISO 8601 date of approval | 2026-06-15 |
| `extension_scope` | Which fields and/or authority domains the new source may support | "identity_authority for private company canonical_object_id resolution" |
| `justification` | Documented rationale for why existing PGMF sources are insufficient | "No existing PGMF source covers private equity data provider identity resolution" |
| `new_source_id` | Proposed source_id following PGMF registry naming convention | SRC-X-01 (extension prefix) |
| `new_source_tier` | Proposed tier level with evidence | Tier 2 |
| `new_source_domain` | Proposed authority_domain | identity_authority |

### Prohibition Without Approval

- If a candidate record requires a source not in the PGMF source registry AND no human/CTO approval for extension exists:
  - The field SHALL be flagged as SOURCE_EVIDENCE_MISSING
  - The record SHALL be set to CANDIDATE_BLOCKED
  - The blocked_reason SHALL state: "Required source not in PGMF source registry; extension requires human/CTO approval"
  - No workaround, ad-hoc source, or Tier 3 educational reference may substitute for the missing source without approval

### Extension Does NOT

- Modify the existing PGMF source registry entries
- Change authority tiers of existing sources
- Override Tier 1 rules from existing sources
- Create production methodology — extensions remain within preflight scope

---

## 9. Complete CURRENT_METHODOLOGY Field-to-Domain Assignment Table

This section provides the complete mapping of every CURRENT_METHODOLOGY field from the PGMF field taxonomy to its required source authority domain.

### Layer 1 — Object Identity Fields

| Field | Source Authority Domain | Governing Decision |
|-------|------------------------|--------------------|
| `canonical_object_id` | identity_authority | PGMF-DEC-01, PGMF-DEC-04 |
| `object_type` | identity_authority | PGMF-DEC-01 |
| `object_name` | identity_authority | PGMF-DEC-01 |
| `domicile` | accounting_authority | PGMF-DEC-08 |
| `reporting_currency` | accounting_authority | PGMF-DEC-08 |
| `fiscal_year_end` | accounting_authority | PGMF-DEC-08 |
| `accounting_standard` | accounting_authority | PGMF-DEC-08 |
| `taxonomy_reference` | classification_authority | PGMF-DEC-08, PGMF-DEC-09 |
| `index_provider` | classification_authority | PGMF-DEC-01 |
| `benchmark_index_id` | classification_authority | PGMF-DEC-01 |

### Layer 2 — Security / Listing Identity Fields

| Field | Source Authority Domain | Governing Decision |
|-------|------------------------|--------------------|
| `security_id` | identity_authority | PGMF-DEC-04 |
| `isin` | identity_authority | PGMF-DEC-04 |
| `figi` | identity_authority | PGMF-DEC-04 |
| `ticker` | identity_authority | PGMF-DEC-04 |
| `exchange_mic` | identity_authority | PGMF-DEC-04 |
| `primary_listing` | identity_authority | PGMF-DEC-04 |
| `listing_variant_type` | identity_authority | PGMF-DEC-04 |
| `adr_flag` | identity_authority | PGMF-DEC-04 |
| `trading_currency` | accounting_authority | PGMF-DEC-04, PGMF-DEC-08 |

### Layer 3 — Peer Group Assignment Fields

| Field | Source Authority Domain | Governing Decision |
|-------|------------------------|--------------------|
| `family_id` | classification_authority | PGMF-DEC-01 |
| `family_name` | classification_authority | PGMF-DEC-01 |
| `primary_family` | classification_authority | PGMF-DEC-01, PGMF-DEC-02 |
| `secondary_family` | strategic_peer_logic_authority | PGMF-DEC-02 |
| `subcluster_id` | classification_authority | PGMF-DEC-09 |
| `subcluster_name` | classification_authority | PGMF-DEC-09 |
| `asset_type` | identity_authority | PGMF-DEC-01 |
| `peer_role` | strategic_peer_logic_authority / financial_comparability_authority / ETF_methodology_authority | PGMF-DEC-03, PGMF-DEC-05 |
| `comparison_mode_allowed` | financial_comparability_authority | PGMF-DEC-03 |

### Financial Comparability Gate Fields

| Field | Source Authority Domain | Governing Decision |
|-------|------------------------|--------------------|
| `business_model_similarity` | financial_comparability_authority | PGMF-DEC-03, PGMF-DEC-06 |
| `market_cap_band` | financial_comparability_authority | PGMF-DEC-06 |
| `liquidity_band` | financial_comparability_authority | PGMF-DEC-06 |
| `growth_profile_comparable` | financial_comparability_authority | PGMF-DEC-06 |
| `margin_structure_comparable` | financial_comparability_authority | PGMF-DEC-06 |
| `capital_intensity_comparable` | financial_comparability_authority | PGMF-DEC-06 |
| `leverage_comparable` | financial_comparability_authority | PGMF-DEC-06 |
| `comparability_adjustment_required` | accounting_authority | PGMF-DEC-08 |
| `comparability_note` | accounting_authority | PGMF-DEC-08 |
| `comparability_note_required` | financial_comparability_authority | PGMF-DEC-06 |
| `valuation_peer_allowed` | financial_comparability_authority | PGMF-DEC-03, PGMF-DEC-07 |
| `financial_comparability_gate_status` | financial_comparability_authority | PGMF-DEC-03, PGMF-DEC-06 |

### ETF/Fund Boundary Fields (asset_type ∈ {etf, fund} only)

| Field | Source Authority Domain | Governing Decision |
|-------|------------------------|--------------------|
| `benchmark_index` | ETF_methodology_authority | PGMF-DEC-05 |
| `TER` | ETF_methodology_authority | PGMF-DEC-05 |
| `AUM` | ETF_methodology_authority | PGMF-DEC-05 |
| `tracking_difference` | ETF_methodology_authority | PGMF-DEC-05 |
| `tracking_error` | ETF_methodology_authority | PGMF-DEC-05 |
| `spread` | ETF_methodology_authority | PGMF-DEC-05 |
| `holdings_overlap` | ETF_methodology_authority | PGMF-DEC-05 |
| `replication_method` | ETF_methodology_authority | PGMF-DEC-05 |
| `distribution_policy` | ETF_methodology_authority | PGMF-DEC-05 |
| `lookthrough_concentration` | ETF_methodology_authority | PGMF-DEC-05 |

### Governance and Versioning Fields

| Field | Source Authority Domain | Governing Decision |
|-------|------------------------|--------------------|
| `effective_date` | governance_authority | PGMF-DEC-10 |
| `end_date` | governance_authority | PGMF-DEC-10 |
| `lifecycle_status` | governance_authority | PGMF-DEC-10 |
| `review_cycle` | governance_authority | PGMF-DEC-09 |
| `approved_by` | governance_authority | PGMF-DEC-09 |
| `source_authority` | governance_authority | PGMF-DEC-09, PGMF-DEC-10 |
| `change_reason` | governance_authority | PGMF-DEC-10 |
| `challenge_status` | governance_authority | PGMF-DEC-09 |
| `review_status` | governance_authority | PGMF-DEC-09 |
| `methodology_version` | governance_authority | PGMF-DEC-10 |

### Unsupported Asset Class Fields

| Field | Source Authority Domain | Governing Decision |
|-------|------------------------|--------------------|
| `unsupported_status` | classification_authority | PGMF-DEC-01 (scope boundary) |
| `peer_comparison_allowed` | strategic_peer_logic_authority | PGMF-DEC-03 |
| `peer_group_available` | classification_authority | PGMF-DEC-01 |
| `blocked_reason` | governance_authority | PGMF-DEC-09 |


---

## 10. Source Authority Validation Summary

### Coverage Confirmation

| Authority Domain | Fields Governed | Tier 1 Available | Coverage Status |
|-----------------|----------------|------------------|-----------------|
| identity_authority | 12 fields | SRC-G-01, SRC-I-01 | COMPLETE |
| classification_authority | 12 fields | SRC-B-01, SRC-B-02, SRC-B-03, SRC-C-01 | COMPLETE |
| strategic_peer_logic_authority | 4 fields | SRC-D-01 | COMPLETE |
| financial_comparability_authority | 13 fields | SRC-E-01, SRC-E-03 | COMPLETE |
| ETF_methodology_authority | 10 fields | SRC-F-01 | COMPLETE |
| accounting_authority | 9 fields | SRC-H-01, SRC-H-02, SRC-H-03 | COMPLETE |
| governance_authority | 10 fields | SRC-A-01, SRC-A-02, SRC-A-03 | COMPLETE |

**Result**: All CURRENT_METHODOLOGY fields have at least one Tier 1 source available in their designated authority domain. No authority domain is missing Tier 1 coverage.

### Domain-Scope Compliance Matrix

| Source Category | Designated Domain | May Cite For | May NOT Cite For |
|-----------------|-------------------|--------------|------------------|
| A (GIPS/CFA) | governance_authority | review_cycle, approved_by, methodology_version, effective_date, lifecycle_status | primary_family, peer_role, accounting_standard |
| B (GICS) | classification_authority | primary_family, family_id, subcluster_id, taxonomy_reference | comparability_adjustment_required, peer_role (strategic), trading_currency |
| C (ICB) | classification_authority | taxonomy_reference, challenge_status | accounting_standard, valuation_peer_allowed |
| D (Porter) | strategic_peer_logic_authority | peer_role, secondary_family, comparison_mode_allowed | accounting_standard, exchange_mic, TER |
| E (Damodaran) | financial_comparability_authority | valuation_peer_allowed, financial_comparability_gate_status, market_cap_band | primary_family, canonical_object_id, benchmark_index |
| F (ETF) | ETF_methodology_authority | benchmark_index, TER, AUM, tracking_difference, tracking_error | primary_family, accounting_standard, peer_role (non-ETF) |
| G (Identification) | identity_authority | canonical_object_id, figi, isin, ticker, security_id | peer_role, comparability_adjustment_required, TER |
| H (Accounting) | accounting_authority | accounting_standard, reporting_currency, comparability_adjustment_required | peer_role, family_id, benchmark_index |
| I (Exchange/Market) | market_data_authority / identity_authority | exchange_mic (SRC-I-01 only) | peer_role, primary_family, valuation_peer_allowed |

---

## 11. Blocking Rules Summary

| Rule | Trigger | Candidate_Status | Block State |
|------|---------|------------------|-------------|
| SOURCE_EVIDENCE_MISSING | CURRENT_METHODOLOGY field has no source_authority_reference | CANDIDATE_BLOCKED | BLOCK_SOURCE_INSUFFICIENT |
| DOMAIN_SCOPE_VIOLATION | Source cited outside its designated authority_domain | CANDIDATE_BLOCKED | BLOCK_SOURCE_INSUFFICIENT |
| Extension without approval | External source referenced without human/CTO approval | CANDIDATE_BLOCKED | BLOCK_SOURCE_INSUFFICIENT |
| Tier override violation | Tier 2/3 source contradicts Tier 1 within same domain | CANDIDATE_BLOCKED | BLOCK_SOURCE_INSUFFICIENT |

---

## 12. Boundary Confirmation

| Boundary | Status |
|----------|--------|
| No candidate records populated by this artifact | CONFIRMED |
| No source references applied to records | CONFIRMED |
| No registry files created | CONFIRMED |
| No peer assignments made | CONFIRMED |
| No canonical peer_group_id values | CONFIRMED |
| No SAI mutation | CONFIRMED |
| No runtime code | CONFIRMED |
| No market data integration | CONFIRMED |
| No trading or execution scope | CONFIRMED |
| production_authority | NONE |

---

## 13. Cross-Reference to Requirements

| Requirement | Criterion | Satisfaction |
|-------------|-----------|--------------|
| R4.1 | Every candidate record references at least one Source_Authority per CURRENT_METHODOLOGY field | Section 1 (field-level requirement), Section 9 (complete field-to-domain table) |
| R4.2 | Source reference records source_id, authority_domain, and tier_level at field level | Section 2 (source reference structure) |
| R4.3 | SOURCE_EVIDENCE_MISSING → CANDIDATE_BLOCKED | Section 6 (rule definition, enforcement, testability) |
| R4.4 | DOMAIN_SCOPE_VIOLATION → CANDIDATE_BLOCKED | Section 5 (rule definition, examples, enforcement, testability) |
| R4.5 | Tier 1 hard rules within domain; Tier 2/3 do not override | Section 7 (tier hierarchy enforcement) |
| R15.4 | No source outside PGMF registry without human/CTO approval (approver identity + date) | Section 8 (extension rule) |

---

## Final Status

```
SOURCE_AUTHORITY_MAPPING_PREFLIGHT_COMPLETE
```

---

*End of source authority mapping specification.*
