# Registry Schema Specification

> **Spec**: peer-group-production-registry-creation | **Task**: 2
> **Date**: 2026-06-14 | **Authority**: CTO / Architecture
> **Status**: SCHEMA_SPECIFICATION_ONLY — NO REGISTRY CREATED

---

## 1. Purpose

This document defines the complete production registry schema for `peer_group_registry.yaml`. It specifies the YAML structure, all field definitions, types, constraints, and governance rules.

**This is a specification document.** It does NOT create the registry file. The actual `peer_group_registry.yaml` may only be created after all Human_Approval_Gate stages pass in a future controlled execution phase.

---

## 2. YAML Structure Definition

### 2.1 Root Structure

```yaml
peer_group_registry.yaml:
  metadata:
    # Root-level metadata fields (see Section 3.1)
  families:
    PGF-01:
      family_name: "<string>"
      records:
        - <record fields>  # (see Section 3.3)
    PGF-02:
      # ... same structure
    # PGF-01 through PGF-09 (future PGF-10)
```

### 2.2 Root Metadata Section

```yaml
metadata:
  schema_version: "1.0.0"
  created_date: "<ISO 8601 datetime>"
  created_by: "<CTO approver identity>"
  methodology_authority: "PGMF"
  source_authority_chain:
    - readiness_review
    - p1_decision_record
    - p2_decision_record
    - p3_decision_record
    - p4_decision_record
  production_authority: "HUMAN_CTO_APPROVED"
  lifecycle_state: "NOT_CREATED | ACTIVE | DEPRECATED"
```

### 2.3 Family Section Structure

```yaml
families:
  PGF-XX:
    family_name: "<human-readable family name>"
    records:
      - <record>
      - <record>
```

Families: PGF-01 through PGF-09 (future PGF-10 pending architecture decision).

| Family ID | Family Name |
|-----------|-------------|
| PGF-01 | AI Semiconductors / AI Infrastructure |
| PGF-02 | Cybersecurity / Security Platform |
| PGF-03 | Fintech / Payments / Financial Infrastructure |
| PGF-04 | Mobility / Delivery / Local Commerce |
| PGF-05 | E-Commerce / Marketplace / Retail Platform |
| PGF-06 | Defense / Aerospace / Government Technology |
| PGF-07 | Energy / Infrastructure / Industrials |
| PGF-08 | Financial Services / Banking / Capital Markets |
| PGF-09 | ETF / Fund / Passive Vehicles (DEFERRED) |
| PGF-10 | AI Software / Decision Intelligence Platform (FUTURE — requires CTO architecture decision) |

### 2.4 Record Format

Each record within a family `records` array follows the structure defined in Section 3.3.

---

## 3. Complete Field Table

### 3.1 Root Metadata Fields

| Field Name | Type | Required | Default Value | Description | Source Requirement |
|-----------|------|----------|---------------|-------------|-------------------|
| schema_version | string (semver) | REQUIRED | "1.0.0" | Schema version identifier | R1.2 |
| created_date | string (ISO 8601) | REQUIRED | null (set at creation) | Registry creation timestamp | R1.1 |
| created_by | string | REQUIRED | null (set at creation) | CTO approver identity who authorized creation | R1.3, R9.1 |
| methodology_authority | string (enum) | REQUIRED | "PGMF" | Sole methodology authority identifier | R12.1 |
| source_authority_chain | array[string] | REQUIRED | [] | Ordered list of source authority references | R12.2 |
| production_authority | string (enum) | REQUIRED | "HUMAN_CTO_APPROVED" | Production authorization status | R1.3, R9.1 |
| lifecycle_state | string (enum) | REQUIRED | "NOT_CREATED" | Registry lifecycle state | R1.1 |


### 3.2 Family-Level Fields

| Field Name | Type | Required | Default Value | Description | Source Requirement |
|-----------|------|----------|---------------|-------------|-------------------|
| family_name | string | REQUIRED | — | Human-readable family name | R1.2 |

### 3.3 Record Fields (per peer group entry)

| Field Name | Type | Required | Default Value | Description | Source Requirement |
|-----------|------|----------|---------------|-------------|-------------------|
| peer_group_id | string (PG-{FAMILY}-{SEQ:4}-{CHECK:2}) | REQUIRED | null (minted at creation) | Canonical immutable identifier. Never reused or reassigned. | R1.1, R2.1, R2.3 |
| canonical_object_id | string | REQUIRED | — | Reference to asset identity from Watchlist/Asset Registry layer | R1.1 |
| asset_name | string | REQUIRED | — | Human-readable asset name for traceability | R1.1 |
| peer_role | string (enum) | REQUIRED | — | Role classification: `core_peer`, `adjacent_peer`, `benchmark_context`, `etf_peer`, `excluded_non_peer`, `private_comparable_context` | R1.1, R4 |
| subcluster | string | REQUIRED | — | Subcluster assignment within the family | R1.1, R5 |
| primary_context | string | REQUIRED | — | Primary analytical context / business segment frame | R1.1, R1.4, R15.1 |
| secondary_context | string | OPTIONAL | null | Secondary analytical context for multi-segment assets | R1.4, R15.1, R15.2 |
| dependency_context | string | OPTIONAL | null | Dependency analytical context (e.g., AI-demand for MU) | R1.1, R1.4, R15.1 |
| benchmark_context | string | OPTIONAL | null | Benchmark reference context for comparability framing | R1.4, R15.1 |
| regional_context | object (see Section 4) | CONDITIONAL | null | Mandatory for assets with non-US/EU market comparability caveats | R1.5, R16.1, R16.2 |
| structural_break_caveat | object (see Section 5) | OPTIONAL | null | Post-merger, spin-off, or integration-period comparability limitation | R1.6, R7.1, R7.5 |
| production_authority | string (enum) | REQUIRED | "HUMAN_CTO_APPROVED" | Must be HUMAN_CTO_APPROVED for all production records | R1.3 |
| lifecycle_state | string (enum) | REQUIRED | "ACTIVE" | Record lifecycle: `ACTIVE`, `DEFERRED`, `CONTEXT_ONLY`, `DEPRECATED` | R1.1 |
| source_authority | object (see Section 7) | REQUIRED | — | Source traceability structure | R12.1, R12.2 |
| confidence_status | string (enum) | REQUIRED | — | Methodology/evidence alignment quality (NOT investment conviction) | R18.1, R19 |
| created_date | string (ISO 8601) | REQUIRED | null (set at creation) | Record creation timestamp | R1.1 |
| approver_identity | string | REQUIRED | null (set at approval) | Name of CTO who approved this record | R1.3, R9.1 |
| approval_date | string (ISO 8601) | REQUIRED | null (set at approval) | Date of CTO approval for this record | R1.3, R9.1 |
| dependency_relationships | array[object] (see Section 6) | OPTIONAL | [] | Structural dependency relationships for this record | R11, R30 |

---

## 4. Multi-Segment Representation Model

### 4.1 Purpose

Complex businesses (e.g., AMZN) operate across multiple material segments that cannot be reduced to a single subcluster assignment without information loss. The multi-segment representation model uses four context layers to preserve analytical distinction across segments.

### 4.2 Context Layer Definitions

| Layer | Field | Purpose | Example (AMZN) |
|-------|-------|---------|----------------|
| Primary | primary_context | Primary AI-relevance or business frame | "Cloud/AI Infrastructure" |
| Secondary | secondary_context | Material secondary business segment | "Retail, Marketplace, Logistics, Advertising" |
| Dependency | dependency_context | External dependency that shapes the asset's profile | "Consumer spending, logistics network" |
| Benchmark | benchmark_context | Reference frame for comparability | "Hyperscaler peers (MSFT, GOOGL)" |

### 4.3 Schema Rules

1. Every record MUST have a `primary_context` value (REQUIRED field).
2. `secondary_context`, `dependency_context`, and `benchmark_context` are OPTIONAL — used when single-context is insufficient.
3. An asset MAY carry distinct analytical frames for different business segments without being forced into a single-subcluster assignment (R15.2).
4. If a multi-segment asset cannot be adequately represented, it SHALL be assigned `lifecycle_state: CONTEXT_ONLY` until schema capability is confirmed (R15.3).
5. When multiple contexts are assigned, explicit documentation of segment weighting rationale is REQUIRED in the source_authority references (R15.5).

### 4.4 Multi-Segment YAML Example (Conceptual)

```yaml
# AMZN — Multi-segment representation
- peer_group_id: null  # Minted after approval
  canonical_object_id: "AMZN"
  asset_name: "Amazon.com Inc."
  peer_role: "core_peer"
  subcluster: "Hyperscale Cloud / Multi-Segment Platform"
  primary_context: "Cloud/AI Infrastructure"
  secondary_context: "Retail, Marketplace, Logistics, Advertising"
  dependency_context: "Consumer spending, logistics infrastructure"
  benchmark_context: "Hyperscaler peers (MSFT, GOOGL)"
  # ... remaining fields
```

---

## 5. Regional Context Field Structure

### 5.1 Purpose

Assets operating in non-US/EU markets carry regional comparability caveats that prevent mechanical cross-region peer comparison. The `regional_context` field preserves these caveats as machine-readable structured data.

### 5.2 Field Structure

```yaml
regional_context:
  region: "<region identifier>"
  caveat: "<comparability caveat description>"
  prohibition: <boolean>
```

### 5.3 Field Definitions

| Sub-Field | Type | Required | Description | Source Requirement |
|-----------|------|----------|-------------|-------------------|
| region | string (enum) | REQUIRED | Geographic region identifier: `LATAM`, `LATAM_BR`, `SEA`, `APAC`, `EMEA_EX_EU`, etc. | R16.2 |
| caveat | string | REQUIRED | Human-readable comparability caveat description | R16.2 |
| prohibition | boolean | REQUIRED | If true, cross-region mechanical comparison is prohibited without explicit adjustment | R16.2, R16.3 |

### 5.4 Governed Regional Context Examples

| Asset | Region | Caveat | Prohibition |
|-------|--------|--------|-------------|
| MELI | LATAM | "No mechanical US/EU merger" | true |
| STNE | LATAM_BR | "No mechanical US/EU payments comparison" | true |
| GRAB | SEA | "No mechanical US merger" | true |

### 5.5 Rules

1. `regional_context` is MANDATORY for assets identified with non-US/EU market comparability requirements (R1.5, R16.1).
2. Once assigned, regional_context fields SHALL NOT be removed or silently cleared (R16.4).
3. The schema supports future addition of regional_context to new assets without schema migration (R16.5).
4. Cross-region comparison consuming this field requires explicit regional adjustment (R16.3).


---

## 6. Structural Break Caveat Field Structure

### 6.1 Purpose

Assets with post-merger, spin-off, or integration-period events carry comparability limitations that prevent overstating historical data continuity. The `structural_break_caveat` field documents these limitations.

### 6.2 Field Structure

```yaml
structural_break_caveat:
  type: "<break type>"
  entity: "<related entity>"
  date: "<event date>"
  note: "<comparability note>"
```

### 6.3 Field Definitions

| Sub-Field | Type | Required | Description | Source Requirement |
|-----------|------|----------|-------------|-------------------|
| type | string (enum) | REQUIRED | Break type: `SPINOFF`, `ACQUISITION`, `MERGER`, `RESTRUCTURING` | R1.6, R7.1 |
| entity | string | REQUIRED | Related entity involved in the structural event | R1.6 |
| date | string (YYYY-MM) | REQUIRED | Date of the structural event | R1.6 |
| note | string | REQUIRED | Human-readable comparability limitation description | R1.6, R7.5 |

### 6.4 Governed Structural Break Examples

| Asset | Type | Entity | Date | Note |
|-------|------|--------|------|------|
| GEV | SPINOFF | GE_VERNOVA | 2024-04 | "Limited standalone history" |
| UBS | ACQUISITION | CREDIT_SUISSE | 2023-06 | "Integration period — must distinguish pre/post data" |

### 6.5 Rules

1. `structural_break_caveat` is OPTIONAL — only populated for assets with documented structural events (R1.6).
2. Once assigned, structural_break_caveat fields SHALL NOT be removed or silently cleared (R7.5).
3. The presence of a structural break caveat signals that standalone historical comparability must not be overstated (R7.1).
4. GEV production records MUST carry the spin-off caveat when promoted (R7.1).
5. UBS production records MUST carry the Credit Suisse acquisition caveat when promoted (R7.5).

---

## 7. Dependency Relationships Array Structure

### 7.1 Purpose

Each production registry record may carry a `dependency_relationships` array describing structural context relationships. These are raw structural context for downstream systems — NOT calculation inputs within the registry.

### 7.2 Array Entry Structure

```yaml
dependency_relationships:
  - relationship_type: "<governed type>"
    target_type: "<governed target type>"
    target_id_or_token: "<identifier or token>"
    relationship_direction: "<direction>"
    source_authority: "<PGMF-DEC-XX or P1/P2/P3/P4 ref>"
    evidence_status: "<status>"
    confidence_context: "<context>"
    lifecycle_state: "<state>"
```

### 7.3 Relationship Entry Field Definitions

| Sub-Field | Type | Required | Description | Source Requirement |
|-----------|------|----------|-------------|-------------------|
| relationship_type | string (enum) | REQUIRED | Type of structural relationship (see Section 7.4) | R11.6 |
| target_type | string (enum) | REQUIRED | Type of the relationship target (see Section 7.5) | R11.6 |
| target_id_or_token | string | REQUIRED | Identifier or semantic token for the relationship target | R11.6 |
| relationship_direction | string (enum) | REQUIRED | Direction: `depends_on`, `depended_by`, `bidirectional` | R11.6 |
| source_authority | string | REQUIRED | PGMF decision reference or P1/P2/P3/P4 record reference | R11.6, R12.2 |
| evidence_status | string (enum) | REQUIRED | Evidence quality: `VERIFIED`, `INFERRED`, `CONTEXT_ONLY` | R11.6, R19 |
| confidence_context | string (enum) | REQUIRED | Confidence level: `METHODOLOGY_ALIGNED`, `EVIDENCE_PARTIAL`, `UNVERIFIED` | R11.6, R19 |
| lifecycle_state | string (enum) | REQUIRED | Relationship state: `ACTIVE`, `DEFERRED`, `CONTEXT_ONLY` | R11.6 |

### 7.4 Governed relationship_type Values

| Value | Definition |
|-------|-----------|
| `narrative_dependency` | Asset story/thesis depends on another asset's or entity's narrative |
| `thematic_overlap` | Shared thematic exposure across assets or families |
| `business_model_dependency` | Revenue or operational dependency on another entity |
| `macro_dependency` | Shared macroeconomic factor sensitivity |
| `liquidity_dependency` | Liquidity linkage between assets or markets |
| `regional_dependency` | Regional market structure linkage |
| `supply_chain_dependency` | Supply chain relationship (upstream/downstream) |
| `benchmark_context_dependency` | Benchmark reference relationship for comparability |
| `valuation_comparability_dependency` | Valuation framework linkage enabling comparison |
| `structural_break_dependency` | Post-event structural linkage (merger, spinoff, integration) |

### 7.5 Governed target_type Values

| Value | Definition |
|-------|-----------|
| `asset` | Another asset in the registry |
| `family` | A peer group family (PGF-XX) |
| `subcluster` | A subcluster within a family |
| `theme` | A thematic concept (e.g., "AI infrastructure", "cloud computing") |
| `region` | A geographic region (e.g., "LATAM", "SEA") |
| `macro_factor` | A macroeconomic factor (e.g., "interest rates", "consumer spending") |
| `benchmark` | A benchmark index or reference (e.g., "SOX", "S&P 500") |
| `structural_event` | A corporate event (merger, spinoff, integration) |

### 7.6 Extension Governance

New `relationship_type` or `target_type` values may only be added through:

1. Documented governance proposal with CTO approval
2. Evidence that existing types are insufficient for the structural context requirement
3. Source authority reference for the new type
4. Verification that the new type does not introduce prohibited scope (trading, scoring, recommendation, correlation calculation, etc.)
5. Update to this specification and the verification gate checks

No ad-hoc extension without governance.


---

## 8. Authority Fields

### 8.1 Production Authority

| Field | Value | Meaning |
|-------|-------|---------|
| production_authority | `HUMAN_CTO_APPROVED` | Record has passed Human_Approval_Gate and is production-authorized |
| production_authority | `NONE` | Record is in candidate/preflight state — NOT production |

**Rule**: Every production record MUST carry `production_authority: HUMAN_CTO_APPROVED` (R1.3). No record may exist in the production registry without this value.

### 8.2 Lifecycle State

| Value | Meaning |
|-------|---------|
| `ACTIVE` | Record is live and production-authorized |
| `DEFERRED` | Record is blocked pending resolution of conditions |
| `CONTEXT_ONLY` | Record provides context but is not a full production peer assignment |
| `DEPRECATED` | Record has been superseded or retired |
| `NOT_CREATED` | Registry-level state before activation |

### 8.3 Approver Identity

| Field | Type | Constraint |
|-------|------|-----------|
| approver_identity | string | REQUIRED — must contain the name of the CTO who approved the record |

**Rule**: No record may be created without a recorded approver identity (R9.1).

### 8.4 Approval Date

| Field | Type | Constraint |
|-------|------|-----------|
| approval_date | string (ISO 8601) | REQUIRED — must contain the date of CTO approval |

**Rule**: No record may be created without a recorded approval date (R9.1).

---

## 9. Source Traceability Fields

### 9.1 source_authority Object Structure

```yaml
source_authority:
  methodology_ref: "<PGMF-DEC-XX>"
  decision_record_ref: "<P1/P2/P3/P4 reference>"
  source_registry_ref: "<SRC-X-XX>"
```

### 9.2 Field Definitions

| Sub-Field | Type | Required | Description | Source Requirement |
|-----------|------|----------|-------------|-------------------|
| methodology_ref | string | REQUIRED | PGMF methodology decision reference (e.g., "PGMF-DEC-01") | R12.1, R12.2 |
| decision_record_ref | string | REQUIRED | P1/P2/P3/P4 owner-verified decision record reference | R12.2, R3–R6 |
| source_registry_ref | string | REQUIRED | Source candidate registry reference (e.g., "SRC-01-AVGO") | R12.2 |

### 9.3 Rules

1. Every production record MUST trace to a PGMF methodology reference (R12.1, R12.2).
2. Every production record MUST trace to a P1–P4 decision record (R12.2).
3. No competing methodology authorities may be introduced for peer group decisions (R12.3).
4. Source traceability enables future semantic systems to trace the institutional basis of comparability claims (R18.4).

---

## 10. Confidence and Evidence Fields

### 10.1 confidence_status

| Value | Meaning | NOT Meaning |
|-------|---------|-------------|
| `METHODOLOGY_ALIGNED` | Record fully aligns with PGMF methodology and has complete evidence | NOT investment conviction |
| `EVIDENCE_PARTIAL` | Record has partial evidence — some methodology gaps exist | NOT prediction certainty |
| `UNVERIFIED` | Record exists but evidence has not been fully verified | NOT probability of return |
| `CONTEXT_ONLY` | Record provides context only — not a full peer assignment | NOT expected performance |

### 10.2 evidence_status (within dependency_relationships)

| Value | Meaning |
|-------|---------|
| `VERIFIED` | Relationship has verified source evidence |
| `INFERRED` | Relationship is inferred from structural analysis |
| `CONTEXT_ONLY` | Relationship provides context without verified evidence |

### 10.3 Rules

1. `confidence_status` reflects methodology/evidence alignment quality — it is NEVER investment conviction (R19).
2. `evidence_status` reflects source traceability completeness — it is NEVER prediction certainty (R19).
3. These fields are traceable to PGMF source authority quality, not to investment outcomes.
4. Confidence and evidence fields are machine-readable for future semantic consumption (R18.3).

---

## 11. Prohibited Fields Table

The following fields, data types, and content MUST NOT exist in the production registry schema. Their presence constitutes a boundary violation and would trigger verification gate failure.

| Prohibited Field/Content | Reason | Violates |
|--------------------------|--------|----------|
| price | Market data belongs to data ingestion layer | R17.2 |
| volume | Market data belongs to signal engines | R17.2 |
| market_cap | Market data calculation — not structural context | R17.2 |
| score | Scoring belongs to Scoring Methodology layer | R13.6 |
| rank | Ranking belongs to downstream systems | R13.6 |
| recommendation | Investment recommendations prohibited | R13.6, R17.3 |
| target_price | Expected returns prohibited | R13.6, R17.3 |
| expected_return | Expected returns prohibited | R13.6, R17.3 |
| conviction | Conviction scoring prohibited | R13.6, R17.3 |
| buy_sell_hold | Trading signals prohibited | R17.1 |
| position_size | Portfolio allocation prohibited | R17.3 |
| weight | Portfolio holdings belong to Portfolio State | R13.2 |
| allocation | Portfolio allocation prohibited | R13.2, R17.1 |
| correlation | Statistical calculation belongs to Correlation/Dependency Engine | R13.7, design Section 16 |
| beta | Statistical calculation belongs to Risk/Factor models | R13.7, design Section 16 |
| covariance | Statistical calculation belongs to Risk/Factor models | R13.7, design Section 16 |
| factor_exposure | Factor calculation belongs to Factor/Signal models | R13.7, design Section 16 |
| concentration_score | Portfolio health belongs to Portfolio Health Framework | R13.7, design Section 16 |
| health_metric | Portfolio health belongs to Portfolio Health Framework | R13.7 |
| semantic_state | Semantic conclusions belong to Semantic Reasoning layer | R13.7 |
| report_text | Report rendering belongs to Report Reasoning layer | R13.7 |
| narrative | PM interpretation belongs to Reasoning layer | R13.7 |
| trading_signal | Trading absolutely prohibited | R17.1 |
| execution_instruction | Trading absolutely prohibited | R17.1 |
| broker_connection | Trading absolutely prohibited | R17.1 |
| exchange_routing | Trading absolutely prohibited | R17.1 |
| order_type | Trading absolutely prohibited | R17.1 |
| momentum_output | Tactical momentum belongs to Signal Engines | R13.7 |
| regime_conclusion | Market regime belongs to Market Regime Framework | R13.7 |
| opportunity_score | Opportunity scoring belongs to Opportunity Engine | R13.7 |
| dashboard_render | Rendering belongs to downstream layers | R13.7 |

---

## 12. Enum Value Constraints Summary

### 12.1 peer_role Allowed Values

- `core_peer`
- `adjacent_peer`
- `benchmark_context`
- `etf_peer`
- `excluded_non_peer`
- `private_comparable_context`

### 12.2 lifecycle_state Allowed Values (Record-Level)

- `ACTIVE`
- `DEFERRED`
- `CONTEXT_ONLY`
- `DEPRECATED`

### 12.3 lifecycle_state Allowed Values (Registry-Level Metadata)

- `NOT_CREATED`
- `ACTIVE`
- `DEPRECATED`

### 12.4 production_authority Allowed Values

- `HUMAN_CTO_APPROVED`
- `NONE`

### 12.5 confidence_status Allowed Values

- `METHODOLOGY_ALIGNED`
- `EVIDENCE_PARTIAL`
- `UNVERIFIED`
- `CONTEXT_ONLY`

### 12.6 evidence_status Allowed Values

- `VERIFIED`
- `INFERRED`
- `CONTEXT_ONLY`

### 12.7 relationship_direction Allowed Values

- `depends_on`
- `depended_by`
- `bidirectional`

### 12.8 structural_break_caveat.type Allowed Values

- `SPINOFF`
- `ACQUISITION`
- `MERGER`
- `RESTRUCTURING`

---

## 13. Schema Validation Rules

1. All REQUIRED fields must be non-null in production records.
2. Enum fields accept only governed values — any other value is a validation failure.
3. ISO 8601 date fields must conform to standard datetime format.
4. peer_group_id must match format: `PG-{FAMILY}-{SEQ:4}-{CHECK:2}` (e.g., PG-01-0001-A7).
5. No duplicate peer_group_id values may exist across the entire registry.
6. regional_context MUST be present for assets identified with regional comparability requirements.
7. dependency_relationships entries must use only governed relationship_type and target_type values.
8. Every record must have source_authority with all three sub-fields populated.
9. production_authority MUST be "HUMAN_CTO_APPROVED" for all production records.
10. approver_identity and approval_date MUST be non-null for all production records.

---

## 14. Boundary Confirmations

- ✓ This document is a SPECIFICATION — no `peer_group_registry.yaml` created
- ✓ No canonical peer_group_id values minted
- ✓ No candidate records approved
- ✓ No runtime code or validation code produced
- ✓ No market data, trading, or execution scope introduced
- ✓ No scoring, ranking, recommendation, or expected return fields defined
- ✓ No statistical calculations (correlation, beta, covariance) included
- ✓ No SAI mutation

---

## 15. Source References

| Reference | Path |
|-----------|------|
| Design.md Section 7 | Registry Schema Model |
| Design.md Section 11 | Conditional Caveat Encoding Model |
| Design.md Section 12 | Dependency Relationship Model |
| Design.md Section 13 | Graph-Readiness Model |
| Design.md Section 14 | Relationship Extension Governance |
| Design.md Section 15 | Dependency Boundary Table |
| Design.md Section 16 | Correlation Calculation Prohibition Table |
| Design.md Section 19 | Confidence and Evidence Model |
| Requirements R1 | Production Registry Schema Definition |
| Requirements R15 | Multi-Segment Representation |
| Requirements R16 | Regional Comparability Preservation |

---

```
REGISTRY_SCHEMA_SPECIFICATION_COMPLETE — DOCUMENTATION_ONLY
```

---

*End of registry schema specification.*
