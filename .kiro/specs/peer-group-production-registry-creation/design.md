# Design Document

> **Spec**: peer-group-production-registry-creation | **Revision**: v1
> **Date**: 2026-06-14 | **Authority**: CTO / Architecture
> **Status**: DESIGN_READY_FOR_REVIEW

---

## 1. Purpose

This design defines the controlled documentation architecture for future production registry creation for the MoneyHorst Peer Group system. It translates the hardened requirements (31 requirements, v2) into an architectural model governing how the production registry will be structured, governed, and verified.

This design does NOT create the registry. It defines HOW the registry will be structured when future execution is authorized.

---

## 2. Scope and Non-Authorization

This design document:

- ✓ Defines schema, governance, verification, and compatibility models
- ✓ Carries forward all P1–P4 decisions and conditions
- ✓ Defines dependency relationship architecture

This design document does **NOT**:

- Create peer_group_registry.yaml
- Mint canonical peer_group_id values
- Approve candidate records
- Change Candidate_Status values
- Mutate SAI
- Create runtime code or validation code
- Integrate market data
- Introduce trading, broker, exchange, ATS, routing, allocation, or execution scope
- Produce semantic state activation, PM reasoning, report text, dashboard rendering
- Generate scoring, ranking, opportunity prioritization, conviction scores, target prices, or expected returns
- Calculate portfolio health, concentration, beta, covariance, or factor exposure

---

## 3. Source Authority Matrix

| Source | Path | Authority Type |
|--------|------|----------------|
| Production Registry Readiness Review | `docs/moneyhorst/reviews/peer_group_production_registry_readiness_review.md` | Controlling |
| PGMF | `.kiro/specs/peer-group-registry-methodology-framework/` | Methodology authority |
| Investment Taxonomy SSOT | `docs/moneyhorst/investment_style_method_taxonomy_ssot.md` | Terminology authority |
| Research Mechanism SSOT | `docs/moneyhorst/research_mechanism_ssot.md` | Governance authority |
| Asset Type and Sentiment Guidance | `docs/README_asset_type_and_sentiment_guidance.md` | Boundary authority |
| System Architecture | `docs/system_architecture.md` | Governance authority |
| Decision Governance | `docs/decision_governance.md` | Governance authority |
| Portfolio State Model | `docs/portfolio_state_model.md` | Downstream compatibility authority |
| Semantic Signal Registry | `docs/semantic_signal_registry.md` | Downstream compatibility authority |
| Semantic Reasoning Rules | `docs/semantic_reasoning_rules.md` | Boundary authority |
| Report Reasoning System | `docs/report_reasoning_system.md` | Downstream compatibility authority |
| Report Pipeline Architecture | `docs/report_pipeline_architecture.md` | Downstream compatibility authority |
| Portfolio Health Framework | `docs/portfolio_health_framework.md` | Downstream compatibility authority |
| Opportunity Engine Design | `docs/opportunity_engine_design.md` | Downstream compatibility authority |
| Action Space Framework | `docs/action_space_framework.md` | Boundary authority |
| Correlation/Dependency Framework | `docs/correlation_dependency_framework.md` | Downstream compatibility authority |
| Watchlist/Asset Registry | `docs/watchlist_asset_registry_framework.md` | Boundary authority |
| Confidence Model | `docs/confidence_model.md` | Boundary authority |
| Data Ingestion Framework | `docs/data_ingestion_normalization_framework.md` | Boundary authority |
| Scoring Methodology | `docs/scoring_methodology_framework.md` | Boundary authority |
| Market Regime Framework | `docs/market_regime_framework.md` | Boundary authority |
| Multilingual Rendering | `docs/multilingual_rendering_framework.md` | Boundary authority |
| Dashboard Philosophy | `docs/dashboard_philosophy.md` | Boundary authority |
| Engine Design Principles | `docs/engine_design_principles.md` | Governance authority |
| Portfolio Memory Architecture | `docs/portfolio_memory_architecture.md` | Downstream compatibility authority |
| P1–P4 Decision Records | `docs/moneyhorst/reviews/peer_group_p{1,2,3,4}_owner_verified_decision_record.md` | Controlling |
| Preflight Spec | `.kiro/specs/peer-group-registry-creation-preflight/` | Context only |

---

## 4. Architectural Position

The Peer Group Production Registry is a **canonical structural intelligence layer** inside Portfolio OS.

```
┌──────────────────────────────────────────────────────────┐
│ Portfolio OS Architecture                                │
├──────────────────────────────────────────────────────────┤
│  ┌─────────────────┐   ┌──────────────────────────┐     │
│  │ Asset Registry / │   │ Peer Group Production    │     │
│  │ Watchlist Layer  │──▶│ Registry (THIS DESIGN)   │     │
│  │ (identity owner) │   │ (comparability owner)    │     │
│  └─────────────────┘   └──────────┬───────────────┘     │
│                                    │ read-only            │
│         ┌──────────────────────────┼─────────────┐       │
│         ▼              ▼           ▼             ▼       │
│  ┌──────────┐  ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Portfolio │  │ Semantic  │ │  Report  │ │   SAI    │  │
│  │  State   │  │Reasoning │ │Reasoning │ │(read-only│  │
│  │(holdings)│  │(meaning) │ │(explain) │ │consumer) │  │
│  └──────────┘  └──────────┘ └──────────┘ └──────────┘  │
│         ▼              ▼           ▼             ▼       │
│  ┌──────────┐  ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Portfolio │  │Opportunity│ │  Action  │ │  Signal  │  │
│  │ Health   │  │  Engine   │ │  Space   │ │ Engines  │  │
│  └──────────┘  └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Trading / Execution — OUT OF SCOPE / PROHIBITED  │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

**Principle**: Signals decide, AI interprets, Human decides.

---

## 5. Layer Separation Diagram

| Layer | Owner | Responsibility | Registry Interaction |
|-------|-------|---------------|---------------------|
| Asset Registry / Watchlist | Asset identity layer | Canonical asset identity (ISIN, FIGI, legal entity) | Registry references identity; does not own it |
| Peer Group Registry | THIS DESIGN | Peer comparability, structural context, family/subcluster | Owns peer assignments and structural relationships |
| Portfolio State | Portfolio State layer | Holdings, weights, exposures, NAV | Consumes registry as read-only context |
| Signal Engines | Signal layer | Signal activation and calculation | Does not consume registry directly |
| Semantic Interpretation | Semantic layer | Meaning derivation from signals/context | May consume registry structure; does not modify it |
| PM Reasoning | Reasoning layer | Investment interpretation | May consume registry context for explanations |
| Report Rendering | Rendering layer | Human-readable output | May present registry context; owns language |
| Action Space | Action layer | Possible action framing | May reference peer context; does not get actions from registry |
| SAI | Intelligence framework | Deferred peer interface consumption | Read-only consumer through contract boundary |
| Trading/Execution | OUT OF SCOPE | Prohibited | No interaction whatsoever |


---

## 6. Registry Schema Boundaries

**Contains**:
- Peer group family definitions (PGF-01 through PGF-09, future PGF-10)
- Peer role assignments (core_peer, adjacent_peer, benchmark_context, etf_peer, excluded_non_peer, private_comparable_context)
- Subcluster assignments with primary/secondary/dependency context
- Regional comparability caveats
- Structural break caveats
- Source authority traceability
- Dependency relationships (structural context only)
- Canonical peer_group_id values (when minted after approval)
- Production authority and lifecycle state

**Excludes**:
- Asset identity (belongs to Watchlist/Asset Registry)
- Portfolio holdings or weights
- Market data or price information
- Trading signals or execution state
- Scores, rankings, or recommendations
- Semantic conclusions or PM interpretations
- Report text or rendered narrative
- Statistical calculations (correlation, beta, covariance)
- Portfolio health metrics
- Conviction, confidence-as-prediction, or expected returns

---

## 7. Production Registry Schema Model

```yaml
# peer_group_registry.yaml — CONCEPTUAL MODEL ONLY
# This file does NOT exist yet. Created only after full approval chain.

metadata:
  schema_version: "1.0.0"
  created_date: null  # Set at registry creation time
  created_by: null    # CTO approver identity
  methodology_authority: "PGMF"
  source_authority_chain:
    - readiness_review
    - p1_decision_record
    - p2_decision_record
    - p3_decision_record
    - p4_decision_record
  production_authority: "HUMAN_CTO_APPROVED"
  lifecycle_state: "NOT_CREATED"  # Until activation

families:
  PGF-01:
    family_name: "AI Semiconductors / AI Infrastructure"
    records:
      - peer_group_id: null  # Minted at creation time
        canonical_object_id: "<asset_ref>"
        asset_name: "<name>"
        peer_role: "<role>"
        subcluster: "<subcluster>"
        primary_context: "<context>"
        secondary_context: "<context_or_null>"
        dependency_context: "<context_or_null>"
        benchmark_context: "<context_or_null>"
        regional_context: null  # Structured field if applicable
        structural_break_caveat: null  # If applicable
        production_authority: "HUMAN_CTO_APPROVED"
        lifecycle_state: "ACTIVE"
        source_authority:
          methodology_ref: "PGMF-DEC-XX"
          decision_record_ref: "P1/P2/P3/P4"
          source_registry_ref: "SRC-X-XX"
        confidence_status: "METHODOLOGY_ALIGNED"
        created_date: null
        approver_identity: null
        approval_date: null
        dependency_relationships: []  # See Section 12

  # ... PGF-02 through PGF-09 follow same structure
```

**Note**: This is a conceptual schema model for future implementation. No actual YAML file is created by this design.

---

## 8. Canonical ID Minting Design

**Format**: `PG-{FAMILY}-{SEQ:4}-{CHECK:2}`

Example: `PG-01-0001-A7` (PGF-01, sequence 1, checksum A7)

**Rules**:
1. No ID minted until Human_Approval_Gate passes
2. IDs are immutable once created — never reused or reassigned
3. Sequence numbers are monotonically increasing per family
4. Checksum provides integrity verification
5. No IDs minted during spec preparation tasks

**Minting Record**:
- minting_timestamp
- approver_identity
- source_candidate_record_ref
- verification_gate_evidence_ref
- family_id
- sequence_number

---

## 9. P1–P4 Carry-Forward Model

| Gap ID | Asset | Decision | Role/Subcluster | Context | Status |
|--------|-------|----------|----------------|---------|--------|
| CTX-GAP-004 | SMCI | PGF-01 primary | core_peer | PGF-07 dependency_context | APPROVED |
| CTX-GAP-005 | NET | PGF-02 primary | core_peer | PGF-01 adjacent_context | APPROVED |
| CTX-GAP-015 | PLTR | DEFERRED | — | PGF-06 context until PGF-10 decision | DEFERRED |
| CTX-GAP-003 | ARM | PGF-01 | adjacent_peer | Business-model caveat | APPROVED |
| CTX-GAP-006 | DDOG | PGF-02 | adjacent_peer | Observability caveat | APPROVED |
| CTX-GAP-007 | TENB | PGF-02 | benchmark_context | Narrow-specialist | APPROVED |
| CTX-GAP-013 | BKNG | PGF-04 | benchmark_context | Travel-marketplace | APPROVED |
| CTX-GAP-016 | AXON | PGF-06 | adjacent_peer | Public-safety caveat | APPROVED |
| CTX-GAP-017 | GEV | PGF-07 | core_peer | Spin-off history CONDITIONAL | CONDITIONAL |
| CTX-GAP-001 | AVGO | PGF-01 | AI Silicon primary | Networking secondary_context | APPROVED |
| CTX-GAP-002 | MU | PGF-01 | Memory/Storage primary | AI-demand dependency_context | APPROVED |
| CTX-GAP-008 | AXP | PGF-03 | Hybrid Payments | Closed-loop caveat | APPROVED |
| CTX-GAP-011 | UBER | PGF-04 | Mobility primary | Delivery secondary_context | APPROVED |
| CTX-GAP-014 | AMZN | PGF-05 | Multi-segment | Cloud primary, Retail/Logistics context | CONDITIONAL |
| CTX-GAP-009 | MELI | PGF-05 | LatAm context | Regional comparability | CONDITIONAL |
| CTX-GAP-010 | STNE | PGF-03 | LatAm payments context | Regional comparability | CONDITIONAL |
| CTX-GAP-012 | GRAB | PGF-04 | SE Asia context | Regional comparability | CONDITIONAL |
| CTX-GAP-018 | UBS | PGF-08 | Post-CS caveat | Structural break | CONDITIONAL |
| CTX-GAP-019 | PGF-09 | DEFERRED | — | ETF data feeds required | DEFERRED |

---

## 10. Deferred Decision Handling Model

| Item | Deferral Type | Resolution Path | Blocker Until Resolved |
|------|--------------|----------------|----------------------|
| PLTR | ARCHITECTURE_REQUIREMENT | CTO decides: introduce PGF-10 OR confirm context/benchmark | Cannot mint PLTR peer_group_id |
| PGF-09 ETF Membership | PRODUCTION_DATA_REQUIREMENT | Define + approve 10 data feeds (AUM, TER, holdings, methodology, liquidity, domicile, replication, structure, issuer, holdings_date) | Cannot populate PGF-09 membership |
| AMZN (fallback) | SCHEMA_CAPABILITY | Confirm multi-segment representation OR assign context/benchmark | Cannot force single-subcluster |

**Resolution governance**: Each deferred item requires explicit CTO approval with approver identity, date, and scope before resolution.

---

## 11. Conditional Caveat Encoding Model

| Asset | Caveat Type | Registry Field | Enforcement |
|-------|-------------|---------------|-------------|
| GEV | Spin-off history | `structural_break_caveat: {type: SPINOFF, entity: GE_VERNOVA, date: 2024-04, note: "Limited standalone history"}` | Must not overstate historical comparability |
| UBS | Post-acquisition integration | `structural_break_caveat: {type: ACQUISITION, entity: CREDIT_SUISSE, date: 2023-06, note: "Integration period"}` | Must distinguish pre/post data |
| MELI | LatAm regional | `regional_context: {region: LATAM, caveat: "No mechanical US/EU merger", prohibition: true}` | Cross-region comparison requires adjustment |
| STNE | LatAm payments | `regional_context: {region: LATAM_BR, caveat: "No mechanical US/EU payments comparison", prohibition: true}` | Regional adjustment required |
| GRAB | SE Asia platform | `regional_context: {region: SEA, caveat: "No mechanical US merger", prohibition: true}` | Regional adjustment required |
| AMZN | Multi-segment | Schema must support multi-context; if not → context/benchmark | Cannot force single subcluster |

---

## 12. Dependency Relationship Model

Each production registry record may carry a `dependency_relationships` array describing structural context relationships.

**Structure**:

```yaml
dependency_relationships:
  - relationship_type: "<type>"
    target_type: "<target_type>"
    target_id_or_token: "<identifier>"
    relationship_direction: "depends_on | depended_by | bidirectional"
    source_authority: "<PGMF-DEC-XX or P1/P2/P3/P4 ref>"
    evidence_status: "VERIFIED | INFERRED | CONTEXT_ONLY"
    confidence_context: "METHODOLOGY_ALIGNED | EVIDENCE_PARTIAL | UNVERIFIED"
    lifecycle_state: "ACTIVE | DEFERRED | CONTEXT_ONLY"
```

**Allowed relationship_type values**:
- `narrative_dependency` — asset story depends on another narrative
- `thematic_overlap` — shared thematic exposure
- `business_model_dependency` — revenue/operations dependency
- `macro_dependency` — shared macro factor sensitivity
- `liquidity_dependency` — liquidity linkage
- `regional_dependency` — regional market structure linkage
- `supply_chain_dependency` — supply chain relationship
- `benchmark_context_dependency` — benchmark reference relationship
- `valuation_comparability_dependency` — valuation framework linkage
- `structural_break_dependency` — post-event structural linkage

**Allowed target_type values**:
- `asset` — another asset in the registry
- `family` — a peer group family (PGF-XX)
- `subcluster` — a subcluster within a family
- `theme` — a thematic concept
- `region` — a geographic region
- `macro_factor` — a macroeconomic factor
- `benchmark` — a benchmark index or reference
- `structural_event` — a corporate event (merger, spinoff, integration)

---

## 13. Graph-Readiness Model

The `dependency_relationships` structure is designed to be **graph-readable**:

- Each relationship is a directed edge (source → target via relationship_direction)
- Each node is identified by peer_group_id (source) and target_id_or_token (target)
- The graph can be traversed for structural context exploration
- Future graph systems may consume this structure for dependency visualization

**The registry does NOT**:
- Calculate correlations, beta, covariance, or factor exposure
- Run graph algorithms to determine portfolio concentration
- Produce shortest-path, centrality, or clustering outputs
- Activate semantic dependency states
- Generate scores or rankings from graph structure
- Calculate portfolio health from dependency density

The graph structure provides **raw structural context** for downstream systems that own their own calculations.

---

## 14. Relationship Extension Governance

New `relationship_type` or `target_type` values may only be added through:

1. Documented governance proposal with CTO approval
2. Evidence that existing types are insufficient
3. Source authority reference for the new type
4. Verification that the new type does not introduce prohibited scope (trading, scoring, recommendation, etc.)
5. Update to this design document and the verification gate checks

No ad-hoc extension without governance.

---

## 15. Dependency Boundary Table

| Behavior | Allowed | Prohibited |
|----------|---------|------------|
| Document structural relationships | ✓ | |
| Record source authority for relationships | ✓ | |
| Preserve evidence_status per relationship | ✓ | |
| Graph traversal by downstream systems | ✓ | |
| Dependency visualization context | ✓ | |
| | | Calculate statistical correlation |
| | | Calculate rolling correlation |
| | | Calculate beta or covariance |
| | | Calculate factor exposure |
| | | Calculate concentration from dependencies |
| | | Activate semantic dependency states |
| | | Produce scoring/ranking from graph |
| | | Generate recommendation from dependencies |
| | | Infer trading signals from structure |
| | | Calculate portfolio health from dependencies |

---

## 16. Correlation Calculation Prohibition Table

The following calculations are **absolutely prohibited** within the production registry and its tasks:

| Prohibited Calculation | Reason |
|-----------------------|--------|
| Statistical correlation | Belongs to Correlation/Dependency Engine |
| Rolling correlation | Belongs to Signal Engines |
| Beta | Belongs to Risk/Factor models |
| Covariance | Belongs to Risk/Factor models |
| Factor exposure | Belongs to Factor/Signal models |
| Concentration calculation | Belongs to Portfolio Health |
| Semantic dependency state activation | Belongs to Semantic Reasoning |
| Scoring/ranking output | Belongs to Scoring Methodology |
| Recommendation output | Prohibited everywhere in registry |
| Portfolio health metrics | Belongs to Portfolio Health Framework |
| Market regime conclusions | Belongs to Market Regime Framework |
| Expected return generation | Prohibited everywhere in registry |

---

## 17. Downstream Compatibility Map

| Downstream System | Consumption Mode | Owns Calculations | Registry Provides |
|-------------------|-----------------|-------------------|-------------------|
| Portfolio State | Read-only | Holdings, weights, exposure | Peer context for position interpretation |
| Portfolio Health | Read-only | Health metrics, concentration | Dependency structure, peer density context |
| Correlation/Dependency Engine | Read-only | Correlations, beta, factor exposure | Structural relationship context |
| Semantic Reasoning | Read-only | Semantic conclusions, meaning | Structural fields, dependency types |
| Opportunity Engine | Read-only | Opportunity scores, screening | Peer context, family membership |
| Action Space | Read-only | Action generation | Structural boundaries, comparability |
| Report Reasoning | Read-only | PM interpretation, narratives | Peer context for explanation |
| SAI | Read-only (deferred interface) | Signal intelligence | Peer group fields per contract |

Each downstream system is responsible for its own governance, calculations, and interpretation.

---

## 18. SAI Read-Only Contract Boundary

- SAI consumes peer group data through defined deferred interfaces (peer_benchmark.md, portfolio_fit_interface.md)
- SAI receives: peer_group_available, peer_comparison_allowed, peer_role, core_peer_set, adjacent_peer_set, benchmark_context_set, comparability_note, methodology_version
- SAI does NOT modify registry data
- SAI does NOT write back to the registry
- SAI does NOT trigger registry state changes
- No SAI requirement, design, artifact, or gate is modified by registry creation

---

## 19. Confidence and Evidence Model

| Field | Meaning | NOT Meaning |
|-------|---------|-------------|
| confidence_status | Methodology/evidence alignment quality | NOT investment conviction |
| evidence_status | Source traceability completeness | NOT prediction certainty |
| confidence_context | How well-supported a structural claim is | NOT probability of return |

Values: `METHODOLOGY_ALIGNED`, `EVIDENCE_PARTIAL`, `UNVERIFIED`, `CONTEXT_ONLY`

These fields are traceable to PGMF source authority quality, not to investment outcomes.

---

## 20. ETF/Fund PGF-09 Data Feed Design Boundary

Required data feed specification (fields only — no implementation):

| # | Feed | Purpose | Provenance Required |
|---|------|---------|-------------------|
| 1 | AUM | Fund size | Source + timestamp |
| 2 | TER / Fees | Cost structure | Source + effective date |
| 3 | Holdings Date | Freshness | Publication date |
| 4 | Holdings Composition | Underlying exposure | Source + date |
| 5 | Benchmark Methodology | Index reference | Methodology doc |
| 6 | Issuer | Fund provider | Legal entity |
| 7 | Domicile | Jurisdiction | Legal registration |
| 8 | Liquidity / Spread | Trading quality | Exchange + timestamp |
| 9 | Replication Method | Physical/synthetic | Prospectus |
| 10 | Fund Structure | UCITS/mutual/ETF | Legal classification |

**Boundary**: This design specifies required fields. It does NOT implement data feeds, APIs, vendor connections, or ingestion pipelines.

---

## 21. Multilingual and Rendering Boundary

- All registry structural states are canonical machine-readable tokens
- No German or English narrative embedded as structural values
- Examples of canonical tokens: `core_peer`, `adjacent_peer`, `METHODOLOGY_ALIGNED`, `LATAM`, `SPINOFF`
- Human-readable presentation belongs exclusively to downstream rendering layers
- Multilingual rendering frameworks consume tokens and produce localized text

---

## 22. Verification Gate Structure (VG-PGRC-PRODUCTION-1)

| Check | Category | Description |
|-------|----------|-------------|
| A | Schema Compliance | All records conform to defined schema structure |
| B | Field Completeness | All required fields populated or gap-documented |
| C | Canonical ID Uniqueness | Zero duplicate peer_group_id values |
| D | P1–P4 Fidelity | All carry-forward decisions correctly encoded |
| E | Deferred Decision Non-Promotion | No deferred item silently promoted |
| F | Regional Context Preservation | All regional caveats present where required |
| G | Structural Break Caveat Preservation | GEV/UBS caveats present |
| H | Dependency Relationship Schema Compliance | All relationships use valid types |
| I | Relationship Type Validity | Only governed relationship_type values used |
| J | Target Type Validity | Only governed target_type values used |
| K | Source Authority Traceability | Every record traces to PGMF/P1-P4 source |
| L | No Circular Dependencies | No unsupported self-referencing loops |
| M | No Correlation Output | Zero statistical calculation outputs |
| N | No Semantic Activation | Zero semantic state activation |
| O | No Scoring/Ranking | Zero scoring or recommendation leakage |
| P | Boundary Compliance | All prohibited outputs absent |

All checks must PASS with zero violations before production activation.

---

## 23. Human/CTO Approval Model

| Stage | Gate | Required Before |
|-------|------|----------------|
| 1 | Spec Initiation Approval | Any spec task execution |
| 2 | Schema Finalization Approval | Locking schema definition |
| 3 | Canonical ID Minting Authorization | Any peer_group_id minting |
| 4 | Production Registry Activation | peer_group_registry.yaml creation |

Each gate produces a signed approval artifact with: approver_identity, approval_date, approval_scope, conditions, and VG passage evidence.

---

## 24. Prohibited Output Table

| Category | Prohibited Outputs |
|----------|-------------------|
| Trading | Buy/sell, execution, routing, allocation, position sizing |
| Recommendation | Investment recommendation, thesis validation, conviction |
| Scoring | Asset scores, rankings, opportunity prioritization |
| Prediction | Expected returns, target prices, probability of return |
| Market Data | Price-based methodology, vendor integration, market feeds |
| Semantic | Semantic state activation, semantic conclusions |
| PM Reasoning | PM interpretation, thesis generation, narrative output |
| Report | Report text rendering, dashboard rendering |
| Portfolio | Portfolio health calculation, concentration metrics |
| Statistical | Correlation, beta, covariance, factor exposure |
| Momentum | Tactical momentum outputs, regime conclusions |
| Code | Runtime code, validation code, APIs, ETL pipelines |

---

## 25. No-Authority-Simulation Section

The Peer Group Production Registry:

- Does NOT imply that a peer assignment is an investment recommendation
- Does NOT imply that a comparable peer is a buy/sell/hold conclusion
- Does NOT imply that peer group membership validates an investment thesis
- ONLY provides structured comparability context

Any downstream system consuming registry data is responsible for its own governance boundaries and must not attribute investment conclusions to the registry.

---

## 26. Future Tasks Guidance

The future tasks.md must:

- Be documentation-only
- Produce artifacts for: source authority matrix, registry schema specification, layer separation spec, canonical ID minting rules, P1–P4 carry-forward matrix, deferred-decision resolution model, dependency relationship specification, SAI read-only interface contract, verification gate definition, human/CTO approval gate specification, final spec readiness review
- NOT include implementation tasks or registry creation tasks unless explicitly approved by subsequent Human_Approval_Gate
- NOT create peer_group_registry.yaml or mint canonical IDs

---

## 27. Boundary Confirmations

- ✓ No production registry created
- ✓ No peer_group_registry.yaml created
- ✓ No canonical peer_group_id values minted
- ✓ No candidate records approved
- ✓ No Candidate_Status values changed
- ✓ No SAI mutation
- ✓ No runtime code or validation code
- ✓ No market data integration
- ✓ No trading, broker, exchange, ATS, routing, allocation, or execution scope
- ✓ No portfolio recommendations, conviction scores, target prices, or expected returns
- ✓ No semantic state activation or PM reasoning generation
- ✓ No report text generation or dashboard rendering
- ✓ No scoring, ranking, or opportunity prioritization
- ✓ No correlation, beta, covariance, or factor exposure calculation
- ✓ No portfolio health calculation
- ✓ Documentation-only design

---

```
PEER_GROUP_PRODUCTION_REGISTRY_CREATION_DESIGN_READY
```

---

*End of design document.*
