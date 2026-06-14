# Requirements Document

> **Spec**: peer-group-production-registry-creation | **Revision**: v2 (hardened against MoneyHorst SSOT)
> **Date**: 2026-06-14 | **Authority**: CTO / Architecture
> **Status**: HARDENED_AGAINST_MONEYHORST_SSOT

## Introduction

This specification defines the controlled path for future production registry creation for the MoneyHorst Peer Group system. It carries forward all conditions, deferred decisions, blockers, guardrails, and non-authorization boundaries established in the Peer Group Production Registry Readiness Review.

**Critical Scope Statement**: This spec DEFINES the process for production registry creation. It does NOT execute registry creation itself. No `peer_group_registry.yaml` file will be created during spec preparation. No canonical `peer_group_id` values will be minted. No candidate records will be approved. Task execution under this spec produces documentation-only preparation artifacts. Actual registry creation occurs only after all requirements, design, verification gates, and explicit human/CTO approval are satisfied in a subsequent controlled execution phase.

**Readiness Category**: `READY_FOR_PRODUCTION_REGISTRY_CREATION_SPEC_PREPARATION_WITH_CONDITIONS`

**Source Authority**: Peer Group Production Registry Readiness Review (`docs/moneyhorst/reviews/peer_group_production_registry_readiness_review.md`)

---

## MoneyHorst / Portfolio OS Architectural Position

The production peer group registry is not a standalone database. It is a **canonical structural intelligence layer** inside Portfolio OS.

It supports:
- Portfolio reasoning and asset comparability
- Peer context and evidence traceability
- Future semantic interpretation and report reasoning
- SAI read-only consumption through deferred interfaces
- Opportunity evaluation context
- Watchlist normalization context
- Portfolio health and dependency analysis context

It is **not**:
- A trading system
- A portfolio allocator
- A recommendation engine
- A market-data engine
- An autonomous investment AI
- A scoring or ranking system
- A conviction or expected-return generator

It must remain compatible with Portfolio OS principles: **Signals decide, AI interprets, Human decides.**

---

## SSOT Source Authority

| Authority Type | Source | Role |
|---------------|--------|------|
| Controlling | `docs/moneyhorst/reviews/peer_group_production_registry_readiness_review.md` | Direct governing source for P1–P4 decisions and readiness conditions |
| Methodology | PGMF (`.kiro/specs/peer-group-registry-methodology-framework/`) | Sole peer methodology authority for field rules, families, subclusters |
| Terminology | `docs/moneyhorst/investment_style_method_taxonomy_ssot.md` | Layer separation: asset class, instrument, style, factor, method, allocation, strategy, system |
| Research/Evidence | `docs/moneyhorst/research_mechanism_ssot.md` | Research behavior, evidence quality, signal governance |
| Asset Type Boundary | `docs/README_asset_type_and_sentiment_guidance.md` | ETF/fund and analyst sentiment boundaries |
| System Identity | `docs/system_architecture.md` | Portfolio OS system architecture and identity |
| Decision Governance | `docs/decision_governance.md` | Human governance, no-autonomous-decision constraints |
| Signal Hierarchy | `docs/semantic_signal_registry.md`, `docs/signal_calculation_framework.md`, `docs/trusted_signal_sources.md` | Signal authority model |
| Semantic Reasoning | `docs/semantic_reasoning_rules.md` | Semantic interpretation constraints |
| Report Behavior | `docs/report_reasoning_system.md`, `docs/report_pipeline_architecture.md` | Report rendering boundaries |
| Portfolio State | `docs/portfolio_state_model.md` | Portfolio state ownership |
| Portfolio Health | `docs/portfolio_health_framework.md` | Health/dependency analysis boundaries |
| Opportunity Engine | `docs/opportunity_engine_design.md` | Opportunity screening boundaries |
| Action Space | `docs/action_space_framework.md` | Action-space generation boundaries |
| Correlation/Dependency | `docs/correlation_dependency_framework.md` | Dependency interpretation boundaries |
| Watchlist/Asset Registry | `docs/watchlist_asset_registry_framework.md` | Asset identity ownership |
| Confidence Model | `docs/confidence_model.md` | Confidence = evidence alignment, not prediction |
| Data Ingestion | `docs/data_ingestion_normalization_framework.md` | Ingestion boundary — no implementation here |
| Scoring Methodology | `docs/scoring_methodology_framework.md` | No scoring/ranking from registry |
| Market Regime | `docs/market_regime_framework.md` | No regime conclusions from registry |
| Deployment Intelligence | `docs/deployment_intelligence_framework.md` | Deployment boundary |
| Multilingual Rendering | `docs/multilingual_rendering_framework.md` | Language-independent structural states |
| Dashboard Philosophy | `docs/dashboard_philosophy.md` | Rendering belongs downstream |
| Engine Design | `docs/engine_design_principles.md` | Engine architecture principles |
| Portfolio Memory | `docs/portfolio_memory_architecture.md` | Memory layer boundaries |
| Future Backlog | `docs/future_framework_backlog.md` | Context only |

---

## Glossary

- **Production_Registry**: The future `peer_group_registry.yaml` file containing canonical peer group definitions with production authority
- **PGMF**: Peer Group Methodology Framework — sole methodology authority for peer group field rules, family definitions, and subcluster logic
- **Canonical_Peer_Group_ID**: A unique, immutable identifier (`peer_group_id`) minted exactly once per production peer group record during controlled registry creation
- **Candidate_Record**: A preflight-stage draft record carrying `production_authority: NONE` and `preliminary: true` status; not yet approved for production use
- **SAI**: Signal Architecture Interface — the system-layer intelligence framework that consumes peer group data through deferred interfaces
- **Verification_Gate**: A deterministic checkpoint (VG-PGRC-PRODUCTION-1) that must pass before production registry activation
- **Human_Approval_Gate**: An explicit human/CTO approval requirement with recorded approver identity and date before any production-state transition
- **P1_Decision**: Owner-verified Priority 1 family assignment decisions (SMCI, NET, PLTR)
- **P2_Decision**: Owner-verified Priority 2 peer role decisions (ARM, DDOG, TENB, BKNG, AXON, GEV)
- **P3_Decision**: Owner-verified Priority 3 subcluster assignment decisions (AVGO, MU, AXP, UBER, AMZN)
- **P4_Decision**: Owner-verified Priority 4 regional/structural decisions (MELI, STNE, GRAB, UBS, PGF-09)
- **Multi_Segment_Representation**: Registry schema capability to represent assets with multiple business segments without forcing single-subcluster assignment
- **Regional_Context**: A registry field preserving regional comparability caveats for assets operating in non-US/EU markets
- **Structural_Break_Caveat**: A registry field documenting post-merger/spin-off comparability limitations
- **ETF_Data_Feed_Precondition**: The requirement that PGF-09 ETF/fund membership depends on approved production data feeds before population
- **Trading_Boundary**: Absolute prohibition on trading, broker, exchange, ATS, routing, allocation, or execution scope within this spec
- **Structural_Intelligence_Layer**: The registry's role as a canonical structural context provider, not a reasoning engine or decision maker

---

## Requirements

### Requirement 1: Production Registry Schema Definition

**User Story:** As a CTO, I want the production registry schema fully defined before any registry creation, so that all structural decisions are explicit and reviewable.

#### Acceptance Criteria

1. THE Production_Registry_Schema_Spec SHALL define all required fields for a production peer group record including: peer_group_id, family_id, family_name, subcluster, peer_role, primary_context, secondary_context, dependency_context, regional_context, structural_break_caveat, production_authority, lifecycle_state, source_authority, and created_date
2. THE Production_Registry_Schema_Spec SHALL define the YAML structure of `peer_group_registry.yaml` including root-level metadata, family sections, and individual record format
3. THE Production_Registry_Schema_Spec SHALL require that every production record carries `production_authority: HUMAN_CTO_APPROVED` with approver_identity and approval_date fields
4. THE Production_Registry_Schema_Spec SHALL define Multi_Segment_Representation capability as a schema-level feature supporting multiple primary/secondary/dependency context fields per record
5. THE Production_Registry_Schema_Spec SHALL define regional_context as a mandatory field for assets with non-US/EU market comparability caveats
6. THE Production_Registry_Schema_Spec SHALL define structural_break_caveat as an optional field for assets with post-merger, spin-off, or integration-period comparability limitations


### Requirement 2: Canonical ID Minting Rules

**User Story:** As a CTO, I want canonical peer_group_id minting rules defined before any IDs are created, so that identifiers are immutable, traceable, and never minted prematurely.

#### Acceptance Criteria

1. THE Canonical_ID_Minting_Rules SHALL define the format and structure of peer_group_id values including prefix, family identifier, sequence number, and checksum components
2. THE Canonical_ID_Minting_Rules SHALL require that no peer_group_id is minted until explicit Human_Approval_Gate passage with recorded approver identity and date
3. THE Canonical_ID_Minting_Rules SHALL require that every minted peer_group_id is immutable once created and must never be reused or reassigned
4. THE Canonical_ID_Minting_Rules SHALL prohibit minting peer_group_id values during spec preparation tasks
5. WHEN a peer_group_id is minted, THE Minting_Process SHALL record the minting timestamp, approver identity, source candidate record reference, and verification gate passage evidence

### Requirement 3: P1 Family Assignment Decision Carry-Forward

**User Story:** As a CTO, I want all P1 family assignment decisions encoded as production spec requirements, so that owner-verified decisions are not lost or silently modified.

#### Acceptance Criteria

1. THE Production_Spec SHALL encode SMCI as PGF-01 AI Infrastructure primary family with PGF-07 dependency/adjacent context preserved
2. THE Production_Spec SHALL encode NET as PGF-02 Cybersecurity/Security Platform primary family with PGF-01 adjacent context preserved
3. THE Production_Spec SHALL encode PLTR with DEFER_WITH_ARCHITECTURE_REQUIREMENT status requiring explicit CTO resolution between PGF-10 AI Software/Decision Intelligence Platform introduction or context/benchmark treatment
4. THE Production_Spec SHALL prohibit silent promotion of PLTR to PGF-06 core peer without explicit PGF-10 architecture decision or CTO-approved context-only treatment

### Requirement 4: P2 Peer Role Decision Carry-Forward

**User Story:** As a CTO, I want all P2 peer role decisions encoded as production spec requirements, so that role assignments are structurally sound and comparability caveats are preserved.

#### Acceptance Criteria

1. THE Production_Spec SHALL encode ARM as adjacent_peer in PGF-01 with explicit IP-licensing business-model caveat preventing mechanical comparison against chip manufacturers
2. THE Production_Spec SHALL encode DDOG as adjacent_peer in PGF-02 with observability-platform caveat distinguishing DDOG from pure cybersecurity core peers
3. THE Production_Spec SHALL encode TENB as benchmark_context in PGF-02 with narrow-specialist caveat preventing promotion to core or adjacent peer
4. THE Production_Spec SHALL encode BKNG as benchmark_context in PGF-04 with travel-marketplace distinction preventing classification as mobility core or adjacent peer
5. THE Production_Spec SHALL encode AXON as adjacent_peer in PGF-06 with public-safety/law-enforcement caveat preventing mechanical comparison against traditional defense primes
6. THE Production_Spec SHALL encode GEV as core_peer in PGF-07 with mandatory spin-off history caveat requiring that standalone historical comparability is not overstated

### Requirement 5: P3 Subcluster Assignment Decision Carry-Forward

**User Story:** As a CTO, I want all P3 subcluster assignment decisions encoded as production spec requirements, so that multi-context and subcluster decisions are preserved.

#### Acceptance Criteria

1. THE Production_Spec SHALL encode AVGO with AI Silicon/AI Acceleration as primary subcluster and networking/connectivity as mandatory secondary_context
2. THE Production_Spec SHALL encode MU with Memory/Storage as primary subcluster and AI-demand as dependency_context, prohibiting classification as pure AI accelerator peer
3. THE Production_Spec SHALL encode AXP with Hybrid Payments/Closed-loop/Charge-card subcluster, prohibiting mechanical equivalence with V/MA without business-model adjustment
4. THE Production_Spec SHALL encode UBER with Mobility as primary subcluster and Delivery/Local Commerce as secondary_context, prohibiting dual primary-subcluster assignment
5. THE Production_Spec SHALL encode AMZN as requiring Multi_Segment_Representation with Cloud/AI Infrastructure as primary AI-relevance frame and Retail, Marketplace, Logistics, Advertising as material segment contexts

### Requirement 6: P4 Regional and Structural Decision Carry-Forward

**User Story:** As a CTO, I want all P4 regional/structural decisions encoded as production spec requirements, so that regional comparability and structural-break caveats are never silently dropped.

#### Acceptance Criteria

1. THE Production_Spec SHALL encode MELI with mandatory LatAm regional_context caveat prohibiting mechanical merger with US/EU e-commerce/marketplace peers without regional adjustment
2. THE Production_Spec SHALL encode STNE with mandatory LatAm payments/regional_context caveat prohibiting mechanical comparison to US/EU payments networks without regional adjustment
3. THE Production_Spec SHALL encode GRAB with mandatory SE Asia regional platform_context caveat prohibiting mechanical merger with US mobility/delivery peers without regional adjustment
4. THE Production_Spec SHALL encode UBS with mandatory post-Credit-Suisse structural_break_caveat requiring distinction between pre-acquisition and post-acquisition comparability
5. THE Production_Spec SHALL encode PGF-09 ETF membership with DEFER_WITH_PRODUCTION_DATA_REQUIREMENT status prohibiting manual finalization until approved production data feeds exist

### Requirement 7: Conditional Decision Handling

**User Story:** As a CTO, I want conditional decisions explicitly tracked with resolution criteria, so that no conditional approval is silently promoted to unconditional production status.

#### Acceptance Criteria

1. WHEN GEV is promoted to production status, THE Production_Registry SHALL preserve the spin-off history caveat and track standalone data maturity over time
2. WHEN AMZN is considered for production assignment, THE Production_Spec SHALL verify that Multi_Segment_Representation capability exists in the registry schema before assigning a production peer_group_id
3. IF Multi_Segment_Representation cannot be confirmed for AMZN, THEN THE Production_Spec SHALL keep AMZN as context/benchmark until such capability exists
4. WHEN regional assets (MELI, STNE, GRAB) are promoted to production status, THE Production_Registry SHALL carry explicit regional_context fields preventing mechanical cross-region peer comparison
5. WHEN UBS is promoted to production status, THE Production_Registry SHALL carry the structural_break_caveat field with Credit Suisse integration-period documentation

### Requirement 8: Deferred Decision Resolution Path

**User Story:** As a CTO, I want deferred decisions documented with explicit resolution criteria and ownership, so that blockers are resolved through proper governance rather than silent promotion.

#### Acceptance Criteria

1. THE Production_Spec SHALL document the PLTR/PGF-10 architecture requirement as a blocking item requiring CTO decision between introducing PGF-10 AI Software/Decision Intelligence Platform family or confirming PLTR as context/benchmark
2. THE Production_Spec SHALL prohibit production registry creation for PLTR until the PGF-10 architecture decision is explicitly recorded with CTO approver identity and date
3. THE Production_Spec SHALL document the PGF-09 ETF Data Feed Precondition as a blocking item requiring definition and approval of production data feeds for AUM, TER, holdings, methodology, liquidity, domicile, and replication method
4. THE Production_Spec SHALL prohibit PGF-09 ETF/fund membership population until all required data feeds are defined, approved, and documented
5. THE Production_Spec SHALL require that deferred decisions are never silently promoted to production status without explicit resolution evidence and CTO approval

### Requirement 9: Human/CTO Approval Gate

**User Story:** As a CTO, I want explicit human approval gates at every production-state transition, so that no automated process can create production authority without human governance.

#### Acceptance Criteria

1. THE Human_Approval_Gate SHALL require recorded approver identity (name), approval date, and approval scope before any production registry creation action
2. THE Human_Approval_Gate SHALL require separate approvals for: spec initiation, schema finalization, canonical ID minting authorization, and production registry activation
3. IF the Human_Approval_Gate has not been passed, THEN THE Production_Spec SHALL prohibit creation of peer_group_registry.yaml, minting of canonical peer_group_id values, approval of candidate records, and mutation of SAI interfaces
4. THE Human_Approval_Gate SHALL produce a signed approval artifact documenting the approval decision, scope, conditions, and any limitations
5. THE Human_Approval_Gate SHALL require that all Verification_Gate checks pass before human approval is requested

### Requirement 10: SAI Integration Contract

**User Story:** As a CTO, I want the SAI integration contract defined without mutating SAI, so that the production registry satisfies SAI deferred interfaces through a clean contract boundary.

#### Acceptance Criteria

1. THE SAI_Integration_Contract SHALL define how peer group data from the Production_Registry will satisfy SAI deferred peer interfaces (peer_benchmark.md, portfolio_fit_interface.md) without modifying SAI requirements, design, or artifacts
2. THE SAI_Integration_Contract SHALL define the data format, field mapping, and delivery mechanism for peer group data consumed by SAI
3. THE SAI_Integration_Contract SHALL prohibit any SAI mutation, SAI artifact modification, or SAI requirement change during production registry creation
4. THE SAI_Integration_Contract SHALL define that SAI consumes peer data as read-only input through defined interface boundaries
5. THE SAI_Integration_Contract SHALL require that peer group data delivered to SAI respects all existing SAI boundary rules including no-scoring, no-recommendation, no-allocation, and no-trading prohibitions

### Requirement 11: Verification Gate Definition

**User Story:** As a CTO, I want a deterministic verification gate defined before production activation, so that registry correctness is provably verified rather than assumed.

#### Acceptance Criteria

1. THE Verification_Gate (VG-PGRC-PRODUCTION-1) SHALL define deterministic checks for: schema compliance, field completeness, canonical ID uniqueness, multi-segment representation correctness, regional context presence, structural break caveat preservation, and P1–P4 decision fidelity
2. THE Verification_Gate SHALL require all checks to pass with zero violations before production registry activation is permitted
3. THE Verification_Gate SHALL produce an explicit verification artifact documenting check results, metrics, pass/fail status, and execution timestamp
4. IF any Verification_Gate check fails, THEN THE Production_Spec SHALL block production registry activation and report the failure to the CTO
5. THE Verification_Gate SHALL verify that no deferred decisions have been silently promoted without explicit resolution evidence
6. THE Verification_Gate SHALL validate dependency relationship schema compliance including: relationship_type validity against allowed values, target_type validity against allowed values, source authority traceability for each relationship, and absence of unsupported circular dependencies
7. THE Verification_Gate SHALL verify that no dependency relationship introduces correlation calculation output, semantic state activation, or scoring/ranking/recommendation leakage


### Requirement 12: Source Authority Preservation

**User Story:** As a CTO, I want PGMF established as sole methodology authority with explicit SSOT references, so that no competing methodology source can introduce field rules or family definitions and so the full MoneyHorst / Portfolio OS governance scope is respected.

#### Acceptance Criteria

1. THE Production_Spec SHALL declare PGMF as the sole methodology authority for peer group family definitions, subcluster rules, peer role assignments, and field taxonomy mappings
2. THE Production_Spec SHALL require that all production registry field rules trace to PGMF methodology documentation
3. THE Production_Spec SHALL prohibit introduction of competing methodology authorities for peer group decisions
4. THE Production_Spec SHALL reference the Investment Taxonomy SSOT (`docs/moneyhorst/investment_style_method_taxonomy_ssot.md`) for terminology alignment ensuring correct distinction between asset class, instrument, investment style, factor, method, asset allocation, strategy, and system layer
5. THE Production_Spec SHALL reference the Asset Type and Sentiment Guidance (`docs/README_asset_type_and_sentiment_guidance.md`) for ETF/fund asset-type handling within the registry
6. THE Production_Spec SHALL reference all Portfolio OS governance documents listed in the SSOT Source Authority table as boundary-authority or downstream-compatibility-authority sources
7. THE future design.md SHALL include a Source Authority Matrix classifying every source as: controlling, methodology authority, terminology authority, governance authority, boundary authority, downstream compatibility authority, or context only

### Requirement 13: Output Restrictions

**User Story:** As a CTO, I want explicit output restrictions defined so that the production spec cannot produce unauthorized artifacts or actions.

#### Acceptance Criteria

1. THE Production_Spec SHALL prohibit creation of runtime code, validation code, or executable logic during spec preparation tasks
2. THE Production_Spec SHALL prohibit market data integration, trading system integration, broker connectivity, exchange connectivity, ATS routing, allocation logic, or execution scope
3. THE Production_Spec SHALL prohibit SAI mutation including SAI requirement changes, SAI design changes, SAI artifact modification, or SAI gate execution
4. THE Production_Spec SHALL prohibit candidate record approval or Candidate_Status mutation during spec preparation
5. THE Production_Spec SHALL restrict spec preparation task outputs to documentation-only artifacts including schema definitions, rule specifications, contract documents, verification gate definitions, and governance process documentation
6. THE Production_Spec SHALL prohibit portfolio recommendations, position sizing, conviction scores, target prices, or expected return outputs
7. THE Production_Spec SHALL prohibit semantic state activation, PM reasoning generation, report text generation, scoring outputs, portfolio health calculation, opportunity ranking, tactical momentum outputs, derivative/trading instrument selection, market regime conclusions, and dashboard rendering

### Requirement 14: ETF/Fund Data Feed Preconditions

**User Story:** As a CTO, I want ETF/fund data feed requirements defined before PGF-09 membership population, so that fund membership is sourced from approved production data rather than manual assignment.

#### Acceptance Criteria

1. THE Production_Spec SHALL define the following required data feeds before PGF-09 ETF/fund membership population: AUM, TER/fees, holdings date, holdings composition, benchmark methodology, issuer, domicile, liquidity/spread, replication method, and fund structure
2. THE Production_Spec SHALL require that each data feed has defined provenance including source provider, update frequency, data format, and quality validation rules
3. THE Production_Spec SHALL apply Asset Type and Sentiment Guidance for ETF/fund analysis boundaries including prohibition of fund scoring, ranking, or recommendation
4. THE Production_Spec SHALL prohibit manual finalization of individual ETF membership in PGF-09 without approved production data feeds
5. WHEN PGF-09 data feeds are defined, THE Production_Spec SHALL require CTO approval of the data feed specification before membership population proceeds

### Requirement 15: Multi-Segment Representation

**User Story:** As a CTO, I want the registry schema to support multi-segment representation, so that complex businesses like AMZN are not forced into simplistic single-subcluster assignments.

#### Acceptance Criteria

1. THE Production_Registry_Schema SHALL support multiple context layers per record: primary_context, secondary_context, dependency_context, and benchmark_context
2. THE Production_Registry_Schema SHALL allow an asset to carry distinct analytical frames for different business segments without forcing single-subcluster assignment
3. IF a multi-segment asset cannot be adequately represented by the schema, THEN THE Production_Spec SHALL assign that asset context/benchmark status until schema capability is confirmed
4. THE Production_Registry_Schema SHALL preserve the analytical distinction between primary AI-relevance frame and material secondary segment contexts as defined in P3 decisions
5. THE Production_Registry_Schema SHALL require explicit documentation of segment weighting rationale when multiple contexts are assigned

### Requirement 16: Regional Comparability Preservation

**User Story:** As a CTO, I want regional comparability caveats preserved as registry field requirements, so that peer analytics never mechanically merge assets across materially different market structures.

#### Acceptance Criteria

1. THE Production_Registry SHALL carry explicit regional_context fields for all assets identified with regional comparability requirements (MELI: LatAm, STNE: LatAm/Brazil, GRAB: SE Asia)
2. THE Production_Registry SHALL define regional_context as a structured field containing: region identifier, comparability_caveat description, and cross-region_comparison_prohibition flag
3. WHEN peer analytics consume registry data, THE Production_Registry regional_context fields SHALL signal that cross-region mechanical comparison requires explicit adjustment
4. THE Production_Spec SHALL prohibit removal or silent clearing of regional_context fields once assigned
5. THE Production_Registry SHALL support future addition of regional_context to assets not yet identified, without requiring schema migration

### Requirement 17: Trading and Market Data Boundary

**User Story:** As a CTO, I want an absolute boundary preserved from preflight prohibiting any trading, market data, or execution scope, so that the production registry remains a governance artifact and never becomes a trading system component.

#### Acceptance Criteria

1. THE Production_Spec SHALL carry an absolute prohibition on trading, broker, exchange, ATS, routing, allocation, or execution scope
2. THE Production_Spec SHALL carry an absolute prohibition on market-data-as-methodology where market data prices, volumes, or signals become peer group assignment criteria
3. THE Production_Spec SHALL carry an absolute prohibition on position sizing, portfolio recommendation, conviction scoring, or expected return generation from peer group data
4. THE Production_Spec SHALL require that any future integration between the Production_Registry and downstream systems is governed by separate specs with their own approval gates
5. IF any task or artifact under this spec introduces trading, execution, or market data methodology scope, THEN THE Verification_Gate SHALL flag the violation and block production activation

### Requirement 18: Semantic Compatibility

**User Story:** As a CTO, I want the registry designed so future semantic systems can consume peer/context data without inventing meaning, so that structural context remains interpretable without autonomous semantic conclusions.

#### Acceptance Criteria

1. THE Production_Registry SHALL preserve the following fields in a semantically consumable format: peer_role, family_id, subcluster, primary_context, secondary_context, dependency_context, benchmark_context, regional_context, structural_break_caveat, source_authority, and confidence/evidence status where applicable
2. THE Production_Registry SHALL NOT embed semantic conclusions, interpretive narratives, or reasoning outputs within registry records
3. THE Production_Registry fields SHALL be machine-readable and consumable by future semantic reasoning layers without requiring natural-language parsing
4. THE Production_Registry SHALL preserve evidence-traceability links for every peer assignment so semantic systems can trace the institutional basis of comparability claims

### Requirement 19: Portfolio State Compatibility

**User Story:** As a CTO, I want the registry to support future portfolio state reasoning without calculating portfolio state itself, so that peer context informs portfolio analysis without creating circular ownership.

#### Acceptance Criteria

1. THE Production_Registry SHALL support future use in: position context, exposure context, dependency interpretation, thematic overlap, narrative dependency, diversification quality, and concentration analysis
2. THE Production_Registry SHALL NOT calculate, store, or produce portfolio state values including holdings, weights, exposures, NAV contributions, or return attributions
3. THE Production_Registry SHALL provide structural context fields that Portfolio State systems can consume as read-only inputs
4. THE Production_Registry SHALL NOT create circular dependencies where registry data depends on portfolio state and portfolio state depends on registry data

### Requirement 20: Action Space Compatibility

**User Story:** As a CTO, I want the registry to support future action-space reasoning by describing comparability and structural context, without generating action instructions.

#### Acceptance Criteria

1. THE Production_Registry MAY support future action-space reasoning by providing peer context, comparability signals, and structural boundaries as read-only inputs
2. THE Production_Registry SHALL NOT generate buy/sell instructions, allocation instructions, position sizing, execution instructions, conviction scores, price targets, or expected returns
3. THE Production_Registry SHALL NOT imply that peer group membership constitutes an investment thesis, trading signal, or portfolio action recommendation
4. THE Production_Registry action-space compatibility SHALL be limited to providing structural context that other systems may evaluate under their own governance

### Requirement 21: Report Reasoning Compatibility

**User Story:** As a CTO, I want the registry to support explainable PM reasoning and report rendering by preserving structural context, without generating report text or PM conclusions.

#### Acceptance Criteria

1. THE Production_Registry SHALL support future report reasoning by preserving structural peer context, family relationships, subcluster assignments, and comparability caveats in machine-readable format
2. THE Production_Registry SHALL NOT generate report text, PM conclusions, narrative output, or rendered explanations
3. THE Production_Registry SHALL NOT produce PM interpretation, thesis validation, or investment narrative from peer group data
4. Report rendering layers MAY consume registry structural context to explain peer comparisons but must attribute interpretation to the rendering layer, not the registry

### Requirement 22: Opportunity Engine Compatibility

**User Story:** As a CTO, I want the registry to support future opportunity screening by defining peer context and structural comparability, without ranking or recommending assets.

#### Acceptance Criteria

1. THE Production_Registry MAY support future opportunity screening by providing peer context, family membership, and comparability structure as read-only inputs
2. THE Production_Registry SHALL NOT rank, score, recommend, or prioritize assets by return expectation, valuation attractiveness, or investment merit
3. THE Production_Registry SHALL NOT produce opportunity lists, ranked watchlists, or screened candidate sets
4. Opportunity evaluation systems MAY consume registry peer context under their own governance rules but must not attribute opportunity rankings to the registry

### Requirement 23: Watchlist / Asset Registry Compatibility

**User Story:** As a CTO, I want the peer group registry to reference canonical asset identity without duplicating or overriding it, so that identity ownership remains with the asset registry layer.

#### Acceptance Criteria

1. THE Production_Registry SHALL reference canonical asset identity from the Watchlist / Asset Registry layer where available, using canonical_object_id or equivalent unique identifier
2. THE Production_Registry SHALL NOT duplicate, override, or compete with canonical asset identity fields (ISIN, FIGI, exchange listing, legal entity)
3. THE Production_Registry SHALL preserve exchange/currency/asset-type boundaries as defined in the Asset Type and Sentiment Guidance but SHALL NOT become the asset registry
4. THE Production_Registry asset references SHALL be linkable to the Watchlist / Asset Registry through defined interface boundaries

### Requirement 24: Confidence and Evidence

**User Story:** As a CTO, I want confidence fields to mean methodology/evidence alignment and never prediction certainty, so that confidence is never misinterpreted as investment conviction.

#### Acceptance Criteria

1. IF the Production_Registry includes confidence or evidence-quality fields, THEN those fields SHALL represent methodology alignment and source-evidence quality only
2. Confidence fields SHALL NOT be interpreted or presented as investment conviction, probability of return, or prediction certainty
3. Confidence fields SHALL be traceable to source/evidence quality metrics defined in PGMF source authority documentation
4. THE Production_Registry SHALL NOT produce confidence scores that could be consumed as investment signals without explicit downstream governance

### Requirement 25: Data Ingestion Boundary

**User Story:** As a CTO, I want the registry to define required data fields and provenance expectations without implementing ingestion systems, so that data requirements are specified before implementation.

#### Acceptance Criteria

1. THE Production_Registry Schema MAY define required data fields, expected provenance, and quality expectations for each field
2. THE Production_Spec SHALL NOT implement data ingestion APIs, vendor connections, freshness jobs, market feeds, or price-based methodology
3. THE Production_Spec SHALL NOT create ETL pipelines, data transformation code, or automated data population logic
4. Data ingestion implementation SHALL be governed by separate specs with their own approval gates and boundary controls

### Requirement 26: Multilingual / Rendering Compatibility

**User Story:** As a CTO, I want the registry to remain language-independent with canonical structural states, so that multilingual rendering is handled downstream without corrupting registry integrity.

#### Acceptance Criteria

1. THE Production_Registry SHALL remain language-independent; all structural states, peer roles, family IDs, and status values SHALL be canonical machine-readable tokens, not narrative text
2. THE Production_Registry SHALL NOT embed German, English, or any natural-language narrative as structural state values
3. Language rendering, localization, and human-readable presentation SHALL belong exclusively to downstream report/rendering layers
4. THE Production_Registry structural tokens SHALL be consumable by multilingual rendering frameworks without requiring registry modification

### Requirement 27: Portfolio OS Scope Preservation

**User Story:** As a CTO, I want the registry's scope explicitly bounded within the Portfolio OS architecture, so that it supports reasoning layers without performing reasoning itself.

#### Acceptance Criteria

1. THE Production_Registry supports structural reasoning but SHALL NOT perform reasoning
2. THE Production_Registry supports semantic interpretation but SHALL NOT create semantic conclusions
3. THE Production_Registry supports future reports but SHALL NOT render reports
4. THE Production_Registry supports future action-space generation but SHALL NOT produce actions
5. THE Production_Registry supports SAI read-only consumption but SHALL NOT mutate SAI
6. THE Production_Registry supports future opportunity analysis but SHALL NOT recommend assets
7. THE Production_Registry supports future portfolio health/dependency analysis but SHALL NOT calculate portfolio health

### Requirement 28: Registry Layer Separation

**User Story:** As a CTO, I want explicit layer separation documented so that no architectural layer confusion arises between the peer group registry and other Portfolio OS layers.

#### Acceptance Criteria

1. Asset identity SHALL belong to the Asset Registry / Watchlist layer — not the Peer Group Registry
2. Peer comparability SHALL belong to the Peer Group Registry — this spec's domain
3. Portfolio holdings SHALL belong to Portfolio State — not the Peer Group Registry
4. Signal activation SHALL belong to Signal Engines — not the Peer Group Registry
5. Semantic meaning SHALL belong to Semantic Interpretation layers — not the Peer Group Registry
6. PM interpretation SHALL belong to PM Reasoning layers — not the Peer Group Registry
7. Human-readable language SHALL belong to Rendering layers — not the Peer Group Registry
8. Trading/execution SHALL belong to out-of-scope future systems only and is prohibited here

### Requirement 29: No Authority Simulation

**User Story:** As a CTO, I want the registry to never imply investment authority, so that peer assignments are never confused with investment recommendations.

#### Acceptance Criteria

1. THE Production_Registry SHALL NEVER imply that a peer assignment is an investment recommendation
2. THE Production_Registry SHALL NEVER imply that a comparable peer is a buy/sell/hold conclusion
3. THE Production_Registry SHALL NEVER imply that a peer group validates an investment thesis
4. THE Production_Registry SHALL ONLY provide structured comparability context
5. Any downstream system consuming registry data SHALL be responsible for its own governance boundaries and must not attribute investment conclusions to the registry

### Requirement 30: Scalable Correlation & Dependency Context Model

**User Story:** As a CTO, I want the peer group registry to represent dependency and correlation context as scalable structured relationships, so that future Portfolio OS engines can interpret thematic overlap, narrative dependency, macro exposure, regional comparability, and hidden concentration without the registry performing calculations or reasoning itself.

#### Acceptance Criteria

1. THE Production_Registry_Schema SHALL support a structured dependency_relationships section per asset or peer record
2. THE dependency_relationships section SHALL be machine-readable and SHALL NOT depend on natural-language parsing
3. THE dependency_relationships section SHALL support multiple relationship entries per record
4. Each dependency relationship SHALL include at minimum: relationship_type, target_type, target_id_or_token, relationship_direction, source_authority, evidence_status, confidence_context, lifecycle_state
5. Allowed relationship_type values SHALL include, at minimum: narrative_dependency, thematic_overlap, business_model_dependency, macro_dependency, liquidity_dependency, regional_dependency, supply_chain_dependency, benchmark_context_dependency, valuation_comparability_dependency, structural_break_dependency
6. Allowed target_type values SHALL include, at minimum: asset, family, subcluster, theme, region, macro_factor, benchmark, structural_event
7. THE Production_Registry SHALL support one-to-many and many-to-one dependency relationships without schema migration
8. THE Production_Registry SHALL support future addition of new relationship_type and target_type values through governed extension rules
9. THE Production_Registry SHALL NOT calculate statistical correlations, rolling correlations, beta, covariance, factor exposure, or portfolio concentration
10. THE Production_Registry SHALL NOT activate semantic states such as dependency_elevated, dependency_fragile, concentration_risk_elevated, ai_dependency_high, or portfolio_health_fragile
11. THE Production_Registry SHALL provide graph-readable structural context only; correlation engines, semantic interpreters, portfolio health engines, and PM reasoning layers remain responsible for calculations and interpretations
12. THE Verification_Gate SHALL validate that dependency relationships are schema-compliant, source-traceable, non-circular where prohibited, and do not introduce reasoning or scoring output

### Requirement 31: Design Preparation Requirements

**User Story:** As a CTO, I want design.md preparation requirements defined so that the future design document carries the full architectural scope forward.

#### Acceptance Criteria

1. THE future design.md SHALL include a Source Authority Matrix classifying every SSOT source by authority type
2. THE future design.md SHALL include a Layer Separation Diagram (text-form) showing registry boundaries vs other Portfolio OS layers
3. THE future design.md SHALL include Registry Schema Boundaries defining what the schema contains and what it excludes
4. THE future design.md SHALL include a Downstream Compatibility Map showing how each Portfolio OS layer may consume registry data
5. THE future design.md SHALL include a Prohibited Output Table listing all forbidden outputs with violation-detection rules
6. THE future design.md SHALL include a No-Authority-Simulation Section confirming the registry does not imply investment authority
7. THE future design.md SHALL include a Verification Gate Structure defining VG-PGRC-PRODUCTION-1 checks
8. THE future design.md SHALL include a Human/CTO Approval Model with multi-stage gate definitions
9. THE future design.md SHALL include a Deferred-Decision Handling Model for PLTR/PGF-10 and PGF-09
10. THE future design.md SHALL include a Dependency Relationship Model defining the structured schema for dependency_relationships
11. THE future design.md SHALL include a Graph-Readiness Model describing how dependency data is consumable as graph-structured context
12. THE future design.md SHALL include a Relationship Extension Governance section defining how new relationship_type and target_type values are approved
13. THE future design.md SHALL include a Dependency Boundary Table listing what dependency-related calculations and semantic activations are prohibited
14. THE future design.md SHALL include a Correlation Calculation Prohibition Table confirming that no statistical correlation, beta, covariance, or factor-exposure calculation is performed by the registry

### Requirement 32: Tasks Preparation Requirements

**User Story:** As a CTO, I want tasks.md defined as documentation-only preparation tasks, so that no implementation or registry creation occurs until explicitly approved.

#### Acceptance Criteria

1. THE future tasks.md SHALL be documentation-only and SHALL NOT include implementation tasks or registry creation tasks unless explicitly approved by a subsequent Human_Approval_Gate
2. THE future tasks.md SHALL include artifacts for: source authority matrix, registry schema specification, layer separation and boundary specification, canonical ID minting rules, P1–P4 carry-forward matrix, deferred-decision resolution model, SAI read-only interface contract, verification gate definition, human/CTO approval gate specification, dependency_relationship_model_specification.md, and final spec readiness review
3. THE future tasks.md SHALL require that each task produces a documentation artifact only
4. THE future tasks.md SHALL NOT include tasks that create peer_group_registry.yaml, mint canonical peer_group_id values, approve candidate records, or execute production registry activation
5. THE future tasks.md SHALL include a final spec readiness review task that verifies all preparation artifacts are complete before any production execution may be proposed

---

## Boundary Confirmations

- ✓ No production registry created by this spec
- ✓ No peer_group_registry.yaml created
- ✓ No canonical peer_group_id values minted
- ✓ No candidate records approved
- ✓ No Candidate_Status values changed
- ✓ No SAI mutation
- ✓ No runtime code
- ✓ No validation code
- ✓ No market data integration
- ✓ No trading, broker, exchange, ATS, routing, allocation, or execution scope
- ✓ No portfolio recommendations, conviction scores, target prices, or expected returns
- ✓ No semantic state activation or PM reasoning generation
- ✓ No report text generation or dashboard rendering
- ✓ No scoring, ranking, or opportunity prioritization
- ✓ Documentation-only preparation spec

---

```
PEER_GROUP_PRODUCTION_REGISTRY_CREATION_REQUIREMENTS_HARDENED_AGAINST_MONEYHORST_SSOT_AND_DEPENDENCY_MODEL
```

---

*End of requirements document.*
