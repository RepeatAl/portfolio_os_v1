# Boundary Rules Specification

> **Peer Group Registry Creation Preflight — Task 6: Boundary Rules**
> Spec: peer-group-registry-creation-preflight | Date: 2026-06-10 | Authority: CTO / Architecture

---

## 1. Document Metadata

| Key | Value |
|-----|-------|
| title | Boundary Rules Specification |
| spec | peer-group-registry-creation-preflight |
| task | Task 6 |
| report_type | Boundary Rules Report |
| production_authority | NONE |
| preliminary | true |
| status | RULE_DEFINITION_ONLY |

---

## 2. Document Boundary Statement

This artifact defines boundary rules only. It does not:

- Create candidate records
- Enforce boundaries on records
- Assign peers
- Create peer_group_id values
- Create registry content
- Activate production use

All boundary rules defined herein govern future preflight task execution (Task 10 candidate record drafts). Task 6 itself does not apply these rules — it defines them.

---

## 3. ETF/Fund Boundary (PGMF-DEC-05)

### 3.1 Core Rule

ETFs and funds must never become company peers. The ETF/company boundary is absolute and enforced in both directions.

### 3.2 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| ETF-B-01 | ETFs and funds (asset_type ∈ {etf, fund}) are NEVER assigned peer_role = core_peer or peer_role = adjacent_peer against company assets |
| ETF-B-02 | PGF-09 uses ETF/fund-specific peer logic only (peer_role = etf_peer) |
| ETF-B-03 | ETFs/funds appearing in company families (PGF-01 through PGF-08) may only carry peer_role = benchmark_context |
| ETF-B-04 | No ETF-to-company fallback: an ETF may not receive company peer methodology treatment |
| ETF-B-05 | No company-to-ETF fallback: a company (asset_type = company) may not be assigned peer_role = etf_peer |
| ETF-B-06 | ETF/fund lookthrough analysis must not create company peer assignments (constituent analysis is informational only) |

### 3.3 Violation Handling

- **Violation block state**: `BLOCK_ETF_COMPANY_FALLBACK`
- **Candidate_Status outcome**: `CANDIDATE_BLOCKED` (ETF/company boundary violation) or `CANDIDATE_CONTEXT_ONLY` (ETF correctly scoped as benchmark_context)
- **Detection**: Any candidate record where asset_type ∈ {etf, fund} AND peer_role ∈ {core_peer, adjacent_peer} against a company asset, OR asset_type = company AND peer_role = etf_peer
- **Response**: Reject record, log BOUNDARY_VIOLATION_ETF_COMPANY_FALLBACK, set Candidate_Status = CANDIDATE_BLOCKED

### 3.4 PGF-09 ETF-Specific Fields

Within PGF-09 (and only PGF-09), ETF/fund candidates use the 10 ETF/fund comparison dimensions:
- benchmark_index, TER, AUM, tracking_difference, tracking_error, spread, holdings_overlap, replication_method, distribution_policy, lookthrough_concentration

These fields are NOT populated on ETF/fund records that appear as benchmark_context in company families (PGF-01 through PGF-08).

### 3.5 PGMF Reference

- Decision: PGMF-DEC-05
- Source artifact: `.kiro/specs/peer-group-registry-methodology-framework/artifacts/etf_fund_peer_methodology_2026-06-08.md`

---

## 4. Cross-Region Comparability Boundary (PGMF-DEC-08)

### 4.1 Core Rule

Cross-region differences must remain visible and must never be silently normalized. When peers in the same family differ in accounting standard, reporting currency, or domicile, explicit comparability documentation is required.

### 4.2 Required Cross-Region Fields

All 7 fields are REQUIRED when cross-region conditions are detected:

| # | Field | Type | Purpose |
|---|-------|------|---------|
| 1 | `accounting_standard` | enum (GAAP / IFRS / other) | Identifies accounting framework |
| 2 | `reporting_currency` | string (ISO 4217) | Currency in which financials are reported |
| 3 | `trading_currency` | string (ISO 4217) | Currency in which the asset trades on its primary venue |
| 4 | `fiscal_year_end` | string (three-letter month) | Fiscal year alignment |
| 5 | `taxonomy_reference` | enum (GICS / ICB / other) | Industry classification framework |
| 6 | `comparability_adjustment_required` | boolean | Must be true when accounting_standard differs between peers |
| 7 | `comparability_note` | string | Documents which adjustments are needed |

### 4.3 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| CR-B-01 | GAAP/IFRS differences between peers in same family require comparability_adjustment_required = true on BOTH records |
| CR-B-02 | ADR/GDR/multi-venue assets require listing_variant_type identification (primary / ADR / GDR / secondary) |
| CR-B-03 | Currency differences require explicit reporting_currency and trading_currency values |
| CR-B-04 | comparability_adjustment_required = true with empty/null comparability_note → CANDIDATE_BLOCKED |
| CR-B-05 | Missing any of the 7 required cross-region fields → CANDIDATE_BLOCKED |
| CR-B-06 | Cross-region differences may NOT be silently normalized — visibility is mandatory |

### 4.4 Affected Families

| Family | Cross-Region Assets | Currency Context |
|--------|--------------------|-----------------| 
| PGF-01 | TSM (TWD/USD ADR), ASML (EUR/USD ADR), ARM (GBP/USD ADR) | TWD, EUR, GBP reporting vs. USD trading |
| PGF-03 | ADYEN (EUR) | EUR reporting and trading |
| PGF-04 | DHER (EUR), MEIT (CNY), GRAB (SGD/USD) | EUR, CNY, SGD vs. USD |
| PGF-05 | ADS/Adidas (EUR) | EUR reporting |
| PGF-06 | Rheinmetall, Hensoldt, Thales (EUR), Leonardo (EUR), Saab (SEK), BAE (GBP) | EUR, SEK, GBP |
| PGF-07 | Schneider Electric (EUR), Siemens (EUR), ABB (CHF), Prysmian (EUR) | EUR, CHF |
| PGF-08 | SAN (EUR), BNP (EUR), DB (EUR), UBS (CHF) | EUR, CHF |

### 4.5 Violation Handling

- **Violation block state**: `BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED`
- **Candidate_Status outcome**: `CANDIDATE_BLOCKED` until all comparability fields are documented
- **Sub-reasons**: CROSS_REGION_COMPARABILITY_INCOMPLETE (note missing), CROSS_REGION_FIELDS_INCOMPLETE (fields missing)

### 4.6 PGMF Reference

- Decision: PGMF-DEC-08
- Source artifact: `.kiro/specs/peer-group-registry-methodology-framework/artifacts/cross_region_comparability_2026-06-08.md`


---

## 5. Unsupported Asset Protection Boundary (PGMF-DEC-07)

### 5.1 Core Rule

All unsupported asset classes are blocked from final peer assignment. Only assets with defined methodology coverage may enter the candidate pipeline as peer members.

### 5.2 Unsupported Asset Classes

The following asset classes are NOT supported by the current peer group methodology (v1):

1. Derivatives
2. Structured products
3. Options
4. Warrants
5. Turbos (turbo certificates, knock-outs)
6. Leveraged products (factor certificates)
7. Private companies (except private_comparable_context)
8. Indices (except benchmark_context)
9. Baskets
10. Synthetic instruments (swaps, CFDs, total return swaps)
11. Commodities (gold, oil, wheat, physical assets)
12. FX pairs (currencies)
13. Crypto / tokenized assets
14. Fixed income (corporate bonds, government bonds, money market)
15. Cash instruments (T-bills, commercial paper, repos)

### 5.3 Handling Rules

| Rule ID | Rule Statement |
|---------|---------------|
| UA-B-01 | Unsupported assets receive Candidate_Status = CANDIDATE_BLOCKED or CANDIDATE_DEFERRED |
| UA-B-02 | peer_comparison_allowed = false for all unsupported assets |
| UA-B-03 | peer_role restricted to: excluded_non_peer (default), private_comparable_context (private companies only), benchmark_context (indices only) |
| UA-B-04 | unsupported_status must carry specific reason (e.g., UNSUPPORTED_ASSET_CLASS_NEEDS_SCOPE_DECISION) |
| UA-B-05 | No ad-hoc peer sets created to fill coverage gaps |
| UA-B-06 | If a scope-confirmed asset is found to be unsupported → remove from active candidate preparation, document removal |

### 5.4 Candidate_Status Outcomes

| Outcome | When Applied |
|---------|-------------|
| `CANDIDATE_BLOCKED` | Asset is unsupported and no future extension pathway is identified |
| `CANDIDATE_DEFERRED` | Asset requires future methodology extension (FUTURE_EXTENSION_REQUIRED) |
| `CANDIDATE_CONTEXT_ONLY` | Asset provides context only (private_comparable_context or benchmark_context) |

### 5.5 Violation Handling

- **Violation block state**: `BLOCK_UNSUPPORTED_ASSET_CLASS`
- **Required fields**: unsupported_status populated with specific handling status, blocked_reason populated
- **PGMF Reference**: PGMF Task 9 (Unsupported Asset Class Handling)
- **Source artifact**: `.kiro/specs/peer-group-registry-methodology-framework/artifacts/unsupported_asset_class_handling_2026-06-08.md`

---

## 6. Private Company Handling

### 6.1 Core Rule

Private companies cannot become final peer members. They provide competitive landscape context only.

### 6.2 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| PC-B-01 | Private companies may only carry peer_role = private_comparable_context |
| PC-B-02 | valuation_peer_allowed = false (always, for all private companies) |
| PC-B-03 | comparison_mode_allowed = ecosystem_context_only |
| PC-B-04 | No FIGI, ISIN, exchange_mic, or market_data fields apply to private companies |
| PC-B-05 | Source limitations (no public filings, no exchange data) must be visible on the record |
| PC-B-06 | Private companies may be referenced as strategic comparables, customer/supplier context, or ecosystem context |

### 6.3 Violation Handling

- **Violation block state**: `BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT`
- **Candidate_Status outcome**: `CANDIDATE_BLOCKED` if assigned core_peer or adjacent_peer; `CANDIDATE_CONTEXT_ONLY` when correctly scoped
- **Detection**: Private company (asset_type = private_company) with peer_role ∈ {core_peer, adjacent_peer, etf_peer}
- **Response**: Reject assignment, restrict peer_role to private_comparable_context

### 6.4 PGMF Reference

- PGMF Task 9, Section 7 (Private Company Rule)
- PGMF-DEC-07 (Unsupported Asset Handling)
- Q7 EVIDENCE_INSUFFICIENT (private comparable methodology deferred)

---

## 7. Derivative and Structured Product Handling

### 7.1 Core Rule

Derivatives and structured products are never peer members. The derivative instrument itself must not create asset or peer identity.

### 7.2 Covered Instrument Types

- Options (calls, puts, covered warrants)
- Warrants
- Turbos (turbo certificates, knock-outs)
- Factor certificates
- CFDs (contracts for difference)
- Futures
- Structured products (autocallables, reverse convertibles, certificates)
- Swaps (total return swaps, interest rate swaps)

### 7.3 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| DV-B-01 | All derivative/structured instruments receive peer_role = excluded_non_peer |
| DV-B-02 | Derivative instrument itself must not create asset or peer identity |
| DV-B-03 | Underlying asset may be classified separately if independently eligible |
| DV-B-04 | Derivative status: DERIVATIVE_ON_SUPPORTED_UNDERLYING or SYNTHETIC_EXPOSURE_ONLY |
| DV-B-05 | No derivative peer registry exists in v1; no derivative methodology may be applied |

### 7.4 Violation Handling

- **Violation block state**: `BLOCK_DERIVATIVE_AS_PEER_MEMBER`
- **Candidate_Status outcome**: `CANDIDATE_BLOCKED` 
- **Detection**: Any derivative/structured product assigned peer_role other than excluded_non_peer
- **Response**: Reject record, enforce excluded_non_peer classification

### 7.5 PGMF Reference

- PGMF Task 9, Section 6 (Derivative and Structured Product Rule)

---

## 8. Index and Basket Handling

### 8.1 Core Rule

Indices and baskets are reference structures only. They may provide benchmark context but must never receive operating-company or ETF peer assignments.

### 8.2 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| IB-B-01 | Indices may only carry peer_role = benchmark_context |
| IB-B-02 | Baskets may only carry peer_role = benchmark_context when allowed |
| IB-B-03 | Index/basket membership must NOT create implied peer assignment for constituents |
| IB-B-04 | No production peer comparison may be derived from index/basket composition |
| IB-B-05 | Indices never receive peer_role = etf_peer (etf_peer is for funds, not indices) |
| IB-B-06 | Custom baskets without canonical index_provider → INDEX_OR_BASKET_REFERENCE_ONLY status |

### 8.3 Handling

- **Candidate_Status**: `CANDIDATE_CONTEXT_ONLY` (when correctly scoped as benchmark_context)
- **peer_role**: `benchmark_context` exclusively
- **Index constituents**: Evaluated separately and individually if eligible

### 8.4 PGMF Reference

- PGMF Task 9, Section 9 (Index / Basket Boundary)
- PGMF Task 4 (ETF/Fund methodology — benchmark_context role)


---

## 9. Market Data Boundary (R9)

### 9.1 Core Rule

Market data availability must NEVER affect peer methodology decisions. No price, volume, liquidity, spread, market cap, or vendor data may serve as a methodology proxy for peer_role assignment or Candidate_Status determination.

### 9.2 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| MD-B-01 | Market data availability must NEVER affect Candidate_Status |
| MD-B-02 | Market data availability must NEVER affect peer_role assignment |
| MD-B-03 | Market data availability must NEVER affect peer_comparison_allowed |
| MD-B-04 | Market data availability must NEVER affect source_authority_status |
| MD-B-05 | Market data availability must NEVER affect family assignment |
| MD-B-06 | Market data availability must NEVER affect subcluster assignment |
| MD-B-07 | No price, volume, liquidity, spread, market cap, or vendor data as methodology proxy |

### 9.3 Preflight Field Status

- **market_data_fields_status** = `NOT_POPULATED_IN_PREFLIGHT`
- All market data readiness fields (market_data_source, data_vendor, data_latency_class, exchange_timezone, trading_calendar_id, derived_data_policy, index_license_required, and all FUTURE_VENDOR_INTEGRATION fields) carry NOT_POPULATED_IN_PREFLIGHT

### 9.4 FUTURE_VENDOR_INTEGRATION Fields (all NOT_POPULATED_IN_PREFLIGHT)

- realtime_entitlement_required
- display_usage_allowed
- non_display_usage_allowed
- redistribution_allowed
- professional_user_flag
- market_data_audit_required
- bid_ask_source
- stale_quote_threshold
- quote_timestamp_required

### 9.5 Violation Handling

- **Violation block state**: `BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY`
- **Candidate_Status outcome**: `CANDIDATE_BLOCKED`
- **Detection**: Any peer_role assignment, Candidate_Status transition, or financial_comparability_gate_status decision that references market data availability, vendor coverage, or exchange connectivity as an input factor
- **Response**: Reject decision, restore methodology-only basis, re-evaluate on methodology grounds only

### 9.6 PGMF Reference

- PGMF Task 7 (Market Data Readiness Schema — separation principle)
- Requirements R9 (Market Data Boundary)

---

## 10. Trading Governance Boundary (R10)

### 10.1 Core Rule

All trading governance fields are future compliance references only. No trading readiness, tradability inference, execution eligibility, broker connectivity, exchange/ATS connectivity, order routing, market access, pre-trade control runtime, kill-switch runtime, surveillance runtime, or compliance certification may be derived from peer methodology or candidate records.

### 10.2 The 16 Trading Governance Fields

All carry: `trading_governance_fields_status = FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL`

| # | Field | Type | Regulatory Source |
|---|-------|------|-------------------|
| 1 | `tradability_status` | enum | SEC 15c3-5, MiFID II RTS 6 |
| 2 | `trading_enabled` | boolean | SEC 15c3-5, MiFID II RTS 6 |
| 3 | `trade_block_reason` | string | SEC 15c3-5 |
| 4 | `execution_venue_eligible` | boolean | MiFID II Art.27 |
| 5 | `best_execution_required` | boolean | MiFID II Art.27, FINRA 5310 |
| 6 | `order_routing_policy_required` | boolean | MiFID II Art.27, FINRA 5310 |
| 7 | `pre_trade_controls_required` | boolean | SEC 15c3-5, MiFID II RTS 6 |
| 8 | `price_collar_policy` | string | SEC 15c3-5 |
| 9 | `max_order_value_policy` | string | SEC 15c3-5 |
| 10 | `max_order_volume_policy` | string | SEC 15c3-5 |
| 11 | `message_throttle_policy` | string | SEC 15c3-5, MiFID II RTS 6 |
| 12 | `kill_switch_required` | boolean | SEC 15c3-5, MiFID II RTS 6 |
| 13 | `audit_log_required` | boolean | SEC 15c3-5, MiFID II RTS 6 |
| 14 | `surveillance_required` | boolean | SEC 15c3-5, MiFID II RTS 6 |
| 15 | `market_abuse_monitoring_required` | boolean | MiFID II RTS 6 |
| 16 | `algo_trading_flag` | boolean | MiFID II RTS 6 |
| 17 | `manual_trade_only_flag` | boolean | SEC 15c3-5, MiFID II RTS 6 |

### 10.3 Prohibited Inferences

No candidate record or preflight output may produce, derive, calculate, or store:

- Tradability inference
- Execution eligibility
- Broker connectivity
- Exchange/ATS connectivity
- Order routing
- Market access
- Pre-trade control runtime
- Kill-switch runtime
- Surveillance runtime
- Compliance certification

### 10.4 Violation Handling

- **Violation block state**: `BLOCK_TRADING_ELIGIBILITY_INFERENCE`
- **Candidate_Status outcome**: `CANDIDATE_BLOCKED`
- **Detection**: Any trading governance field set to a value other than FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
- **Response**: Reject record, classify as TRADING_BOUNDARY_VIOLATION, reset all trading governance fields

### 10.5 PGMF Reference

- PGMF Task 8 (Trading Governance Boundary Specification)
- Source artifact: `.kiro/specs/peer-group-registry-methodology-framework/artifacts/trading_governance_boundary_2026-06-08.md`
- Requirements R10 (Trading Boundary)


---

## 11. SAI Boundary (R11)

### 11.1 Core Rule

SAI is not mutated by this preflight. Candidate records do not satisfy the SAI deferred interface. SAI-BLK-21 remains in BLOCK_FINAL_PEER_ASSIGNMENT state.

### 11.2 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| SAI-B-01 | No SAI artifact, gate, requirement, task plan, or verification status is mutated |
| SAI-B-02 | Candidate records do not satisfy SAI deferred interface (Section 2.3) |
| SAI-B-03 | SAI-BLK-21 remains BLOCK_FINAL_PEER_ASSIGNMENT with peer_comparison_allowed = false |
| SAI-B-04 | SAI must not create peers from candidate records |
| SAI-B-05 | SAI must not create peer_group_id values from candidate records |
| SAI-B-06 | SAI must not create registry entries from candidate records |
| SAI-B-07 | SAI must not create runtime behavior from candidate records |
| SAI-B-08 | SAI must not create trading implications from candidate records |
| SAI-B-09 | No-ad-hoc-peer rule preserved: SAI must never create ad-hoc peers to compensate for missing registry |

### 11.3 SAI Output Contract Fields (PREFLIGHT_NOT_CANONICAL)

All 17 SAI output contract fields carry PREFLIGHT_NOT_CANONICAL or appropriate placeholder values:

| # | Field | Preflight Value |
|---|-------|----------------|
| 1 | peer_group_available | false |
| 2 | peer_comparison_allowed | false |
| 3 | blocked_reason | "Peer Group Registry not yet available" |
| 4 | unsupported_status | As applicable per asset |
| 5 | primary_family | PGF-XX (preliminary) |
| 6 | secondary_family | null or PGF-XX (preliminary) |
| 7 | peer_role | Preliminary only |
| 8 | core_peer_set | PREFLIGHT_NOT_CANONICAL |
| 9 | adjacent_peer_set | PREFLIGHT_NOT_CANONICAL |
| 10 | benchmark_context_set | PREFLIGHT_NOT_CANONICAL |
| 11 | etf_peer_set | PREFLIGHT_NOT_CANONICAL |
| 12 | comparison_mode_allowed | PREFLIGHT_NOT_CANONICAL |
| 13 | financial_comparability_gate_status | PREFLIGHT_NOT_CANONICAL |
| 14 | comparability_note | As documented per record |
| 15 | data_quality_status | PREFLIGHT_NOT_CANONICAL |
| 16 | as_of_date | Preflight execution date |
| 17 | methodology_version | PGMF v1 (methodology-only) |

### 11.4 Violation Handling

- **Violation block state**: `BLOCK_SAI_CONTRACT_SHAPE_VIOLATION`
- **Candidate_Status outcome**: `CANDIDATE_BLOCKED`
- **Detection**: Candidate record output shape omits SAI output contract field OR assigns production-authority value
- **Response**: Reject record, log SAI_CONTRACT_SHAPE_VIOLATION, add missing fields with PREFLIGHT_NOT_CANONICAL values

### 11.5 PGMF Reference

- PGMF Task 10 (SAI Compatibility Verification)
- Source artifact: `.kiro/specs/peer-group-registry-methodology-framework/artifacts/sai_compatibility_verification_2026-06-08.md`
- SAI Deferred Interfaces: `.kiro/specs/single-asset-intelligence-framework/artifacts/deferred_interfaces.md` Section 2.3
- Requirements R11 (SAI Compatibility Boundary)

---

## 12. Source Authority Boundary

### 12.1 Core Rule

No source outside the PGMF source registry may be cited without human/CTO approval. Source domain must match the field being supported.

### 12.2 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| SA-B-01 | Every CURRENT_METHODOLOGY field requires at least one source reference from the PGMF source registry |
| SA-B-02 | Source may only be cited within its designated authority_domain |
| SA-B-03 | DOMAIN_SCOPE_VIOLATION triggered for out-of-domain source citation |
| SA-B-04 | SOURCE_EVIDENCE_MISSING triggered for field without any PGMF source reference |
| SA-B-05 | Tier 1 sources produce hard rules within their domain only |
| SA-B-06 | Tier 2/3 sources support but do not override Tier 1 within the same domain |
| SA-B-07 | No external source without human/CTO approval (recorded with approver identity, approval date, extension scope, justification) |

### 12.3 Violation Outcomes

| Violation | Candidate_Status | Block Reason |
|-----------|-----------------|--------------|
| Out-of-domain citation | CANDIDATE_BLOCKED | DOMAIN_SCOPE_VIOLATION |
| Missing source evidence | CANDIDATE_BLOCKED | SOURCE_EVIDENCE_MISSING |
| Unapproved external source | CANDIDATE_BLOCKED | UNAPPROVED_EXTERNAL_SOURCE |

### 12.4 Reference

- Task 4 artifact: `.kiro/specs/peer-group-registry-creation-preflight/artifacts/source_authority_mapping_preflight.md`
- PGMF Source Registry: `.domainization/sources/peer_group_methodology_source_registry_2026-06-08.md`
- Requirements R4 (Source Authority Mapping)

---

## 13. Peer Assignment Boundary

### 13.1 Core Rule

All peer_role values in preflight are preliminary only. No candidate artifact may be treated as registry truth. peer_comparison_allowed must remain false.

### 13.2 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| PA-B-01 | peer_role is preliminary only, not final assignment |
| PA-B-02 | peer_comparison_allowed must remain false on all candidate records |
| PA-B-03 | No candidate artifact may be treated as registry truth |
| PA-B-04 | No production peer comparison from candidate records |
| PA-B-05 | Human/CTO approval required before any production elevation |

### 13.3 Related Block States

- `BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT` — private companies cannot be final peers
- `BLOCK_DERIVATIVE_AS_PEER_MEMBER` — derivatives cannot be peers
- `BLOCK_PEER_GROUP_ID_CREATION` — no canonical ID creation
- `BLOCK_REGISTRY_CREATION` — no production registry

### 13.4 Reference

- Requirements R3 (Candidate-Only Record Status)
- Requirements R12 (Human Approval Gate)


---

## 14. peer_group_id Boundary

### 14.1 Core Rule

No canonical peer_group_id may be created during preflight. Every candidate record uses the placeholder value exclusively.

### 14.2 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| PG-B-01 | No canonical peer_group_id may be created in preflight |
| PG-B-02 | Every candidate record uses: peer_group_id = PREFLIGHT_PLACEHOLDER_NOT_CANONICAL |
| PG-B-03 | Every candidate record uses: peer_group_id_status = NOT_CREATED |
| PG-B-04 | Any value other than PREFLIGHT_PLACEHOLDER_NOT_CANONICAL triggers block |

### 14.3 Violation Handling

- **Violation block state**: `BLOCK_PEER_GROUP_ID_CREATION`
- **Candidate_Status outcome**: `CANDIDATE_BLOCKED`
- **Detection**: Any peer_group_id value != PREFLIGHT_PLACEHOLDER_NOT_CANONICAL, or peer_group_id_status != NOT_CREATED
- **Response**: Reject record, enforce placeholder value, remove canonical ID

### 14.4 Reference

- Requirements R3 (Candidate-Only Record Status, criterion 2)
- Requirements R5 (Field Taxonomy Mapping, criterion 4)

---

## 15. Registry Boundary

### 15.1 Core Rule

No peer_group_registry.yaml or production registry file may be created during preflight.

### 15.2 Boundary Rules

| Rule ID | Rule Statement |
|---------|---------------|
| RG-B-01 | No peer_group_registry.yaml may exist |
| RG-B-02 | No production registry file may be created |
| RG-B-03 | No production registry schema may be activated |
| RG-B-04 | No production registry write path may be opened |
| RG-B-05 | No file containing "registry" without candidate_ prefix or _preflight suffix |
| RG-B-06 | Naming convention: all artifacts must use candidate_ prefix or _preflight suffix |

### 15.3 Violation Handling

- **Violation block state**: `BLOCK_REGISTRY_CREATION`
- **Candidate_Status outcome**: `CANDIDATE_BLOCKED`
- **Detection**: Any attempt to create peer_group_registry.yaml or production registry file, or any file named with "registry" lacking candidate_ prefix or _preflight suffix
- **Response**: Halt artifact production, log OUTPUT_RESTRICTION_VIOLATION, remove forbidden artifact

### 15.4 Reference

- Requirements R3 (Candidate-Only Record Status, criterion 4)
- Requirements R13 (Preflight Output Restrictions)

---

## 16. Boundary Rule Summary Matrix

| # | Boundary Area | Rule | Forbidden Drift | Required Safe Value / Safe Role | Candidate_Status Outcome | Block State | Related Requirement | Related PGMF Decision / Artifact |
|---|--------------|------|-----------------|--------------------------------|--------------------------|-------------|--------------------|---------------------------------|
| 1 | ETF/Fund Boundary | ETFs/funds never company peers | ETF assigned core_peer/adjacent_peer vs. company | peer_role = benchmark_context (company families) or etf_peer (PGF-09) | CANDIDATE_BLOCKED | BLOCK_ETF_COMPANY_FALLBACK | R6 | PGMF-DEC-05 |
| 2 | Cross-Region Comparability | Differences visible, never normalized | Silent normalization of GAAP/IFRS/currency differences | All 7 cross-region fields populated; comparability_note present | CANDIDATE_BLOCKED | BLOCK_CROSS_REGION_COMPARABILITY_UNVERIFIED | R7 | PGMF-DEC-08 |
| 3 | Unsupported Asset Protection | Unsupported assets blocked from peer assignment | Unsupported asset given core_peer/adjacent_peer/etf_peer | peer_role = excluded_non_peer; unsupported_status populated | CANDIDATE_BLOCKED or CANDIDATE_DEFERRED | BLOCK_UNSUPPORTED_ASSET_CLASS | R8 | PGMF-DEC-07, PGMF Task 9 |
| 4 | Private Company Handling | Private companies context-only | Private company given final peer assignment | peer_role = private_comparable_context; valuation_peer_allowed = false | CANDIDATE_BLOCKED or CANDIDATE_CONTEXT_ONLY | BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT | R8 | PGMF Task 9 §7 |
| 5 | Derivative/Structured Product | Never peer members | Derivative given peer_role other than excluded_non_peer | peer_role = excluded_non_peer | CANDIDATE_BLOCKED | BLOCK_DERIVATIVE_AS_PEER_MEMBER | R8 | PGMF Task 9 §6 |
| 6 | Index/Basket Handling | Reference structures only | Index/basket given company/ETF peer assignment | peer_role = benchmark_context | CANDIDATE_CONTEXT_ONLY | N/A (handled by unsupported + context rules) | R8 | PGMF Task 9 §9 |
| 7 | Market Data Boundary | Data availability ≠ methodology | Market data used as peer_role criterion | market_data_fields_status = NOT_POPULATED_IN_PREFLIGHT | CANDIDATE_BLOCKED | BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY | R9 | PGMF Task 7 |
| 8 | Trading Governance Boundary | Future reference only | Trading field set to operational value | trading_governance_fields_status = FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL | CANDIDATE_BLOCKED | BLOCK_TRADING_ELIGIBILITY_INFERENCE | R10 | PGMF Task 8 |
| 9 | SAI Boundary | SAI not mutated | SAI artifacts modified or candidate records treated as production SAI input | SAI_contract_status = PREFLIGHT_NOT_CANONICAL | CANDIDATE_BLOCKED | BLOCK_SAI_CONTRACT_SHAPE_VIOLATION | R11 | PGMF Task 10 |
| 10 | Source Authority Boundary | Sources must be in-domain and registered | Out-of-domain citation or missing evidence | source_authority_status = VERIFIED (or documented gap) | CANDIDATE_BLOCKED | BLOCK_SOURCE_INSUFFICIENT | R4 | PGMF Source Registry |
| 11 | Peer Assignment Boundary | Preliminary only, no final assignment | Candidate treated as registry truth | peer_comparison_allowed = false; peer_role = preliminary | CANDIDATE_BLOCKED | BLOCK_PEER_GROUP_ID_CREATION | R3, R12 | Design §Candidate Lifecycle |
| 12 | peer_group_id Boundary | No canonical ID creation | Canonical peer_group_id minted | peer_group_id = PREFLIGHT_PLACEHOLDER_NOT_CANONICAL | CANDIDATE_BLOCKED | BLOCK_PEER_GROUP_ID_CREATION | R3, R5 | Design §Candidate Record Draft |
| 13 | Registry Boundary | No production registry | peer_group_registry.yaml or production file created | No registry file exists | CANDIDATE_BLOCKED | BLOCK_REGISTRY_CREATION | R3, R13 | Design §Output Restrictions |


---

## 17. Boundary Violation Response Pattern

When any boundary violation is detected during future task execution, the following response pattern applies:

```
1. DETECT    → Identify the boundary violation through rule matching
2. HALT      → Stop processing the affected candidate record
3. SET       → Set Candidate_Status = CANDIDATE_BLOCKED (or CANDIDATE_DEFERRED/CANDIDATE_CONTEXT_ONLY as applicable)
4. ASSIGN    → Assign the appropriate block state (e.g., BLOCK_ETF_COMPANY_FALLBACK)
5. DOCUMENT  → Record evidence: violation type, affected record, violated rule, expected safe value
6. ROUTE     → Route violation to Evidence Gap Register (Task 11)
7. REQUIRE   → Require remediation or human/CTO decision before record may transition out of blocked state
```

### Response Outcomes by Severity

| Severity | Outcome | Example |
|----------|---------|---------|
| Hard block | CANDIDATE_BLOCKED + remediation required | ETF assigned as company peer, trading field populated |
| Deferred | CANDIDATE_DEFERRED + future methodology required | Unsupported asset class needs new spec |
| Context limitation | CANDIDATE_CONTEXT_ONLY + scope restriction | Private company limited to ecosystem context |

### Remediation Requirements

- Every blocked record must have a documented remediation path
- Remediation evidence must reference the boundary rule that was violated
- Human/CTO approval required for boundary exceptions (no automated exception pathway)
- Resolved records return to CANDIDATE_DRAFT and must re-satisfy all boundary checks

---

## 18. Relationship to Task 10

### 18.1 Role of This Document

Task 6 defines boundary rules. Task 10 (Candidate Record Draft Artifacts for PGF-01 through PGF-09) must APPLY these boundary rules when creating candidate record drafts.

### 18.2 Application Rules

- Every Task 10 candidate record draft must be checked against ALL 13 boundary areas
- Any boundary violation detected during Task 10 candidate record creation must result in the appropriate Candidate_Status and block state
- Task 10 records that trigger boundaries are documented as CANDIDATE_BLOCKED, CANDIDATE_DEFERRED, or CANDIDATE_CONTEXT_ONLY with specific blocked_reason referencing the boundary rule
- ETF benchmark instruments in company families (PGF-01 through PGF-08) must carry peer_role = benchmark_context per Section 3
- Cross-region assets must carry all 7 comparability fields per Section 4

### 18.3 Clarification

Task 6 itself does NOT apply boundaries to records. It defines rules for future application.

---

## 19. Relationship to Task 11

### 19.1 Role of Evidence Gap Register

Task 11 (Evidence Gap Register) documents all blocked, deferred, and context-only outcomes that result from boundary rule application during Task 10.

### 19.2 Routing Rules

- Any CANDIDATE_BLOCKED record from Task 10 due to boundary violation → must have corresponding gap entry in Task 11
- Any CANDIDATE_DEFERRED record → must have gap entry explaining deferred methodology need
- Any CANDIDATE_CONTEXT_ONLY record due to boundary restriction → must have gap entry documenting limitation
- Gap entries reference the boundary rule ID, block state, and required remediation from this document

### 19.3 Gap Types Triggered by Boundaries

| Boundary | Gap Type |
|----------|----------|
| ETF/Fund | ETF_COMPANY_BOUNDARY_ISSUE |
| Cross-Region | CROSS_REGION_COMPARABILITY_INCOMPLETE, CROSS_REGION_FIELDS_INCOMPLETE |
| Unsupported Asset | UNSUPPORTED_ASSET_CLASS |
| Source Authority | SOURCE_EVIDENCE_MISSING, DOMAIN_SCOPE_VIOLATION |
| Identity | IDENTITY_UNRESOLVED |
| Field Taxonomy | FIELD_TAXONOMY_INCOMPLETE |

---

## 20. Prohibited Outputs

This document explicitly confirms that the following outputs are PROHIBITED during this preflight:

| # | Prohibited Output | Reason |
|---|-------------------|--------|
| 1 | Candidate records | Task 6 defines rules only; records are created in Task 10 |
| 2 | PGF candidate artifacts | Not produced by this task |
| 3 | peer_group_registry.yaml | Production registry is out of scope for entire preflight |
| 4 | Production registry file | No production content in preflight |
| 5 | Canonical peer_group_id | Never minted in preflight |
| 6 | Final peer assignments | All peer_role values are preliminary |
| 7 | SAI mutation | SAI artifacts remain unchanged |
| 8 | Runtime code | No executable implementations |
| 9 | Validation code | No validation logic created |
| 10 | Market data integration | Market data not consumed |
| 11 | Trading/execution output | No trading functionality |
| 12 | Broker/exchange/ATS connectivity | Not in scope |
| 13 | Order routing logic | Not in scope |
| 14 | Compliance claims | MoneyHorst is not a regulated entity |

---

## 21. Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | All boundary areas documented with their block states | SATISFIED |
| 2 | ETF/Fund boundary (PGMF-DEC-05) fully specified with BLOCK_ETF_COMPANY_FALLBACK | SATISFIED |
| 3 | Cross-region comparability (PGMF-DEC-08) fully specified with 7 required fields | SATISFIED |
| 4 | Unsupported asset protection (PGMF-DEC-07) fully specified with all classes listed | SATISFIED |
| 5 | Private company handling specified with BLOCK_PRIVATE_COMPANY_FINAL_PEER_ASSIGNMENT | SATISFIED |
| 6 | Derivative handling specified with BLOCK_DERIVATIVE_AS_PEER_MEMBER | SATISFIED |
| 7 | Index/basket handling specified as benchmark_context only | SATISFIED |
| 8 | Market data boundary specified with BLOCK_MARKET_DATA_AS_METHODOLOGY_PROXY | SATISFIED |
| 9 | Trading boundary specified with all 16 fields and BLOCK_TRADING_ELIGIBILITY_INFERENCE | SATISFIED |
| 10 | SAI boundary specified with BLOCK_SAI_CONTRACT_SHAPE_VIOLATION | SATISFIED |
| 11 | Source authority boundary specified | SATISFIED |
| 12 | Peer assignment boundary specified | SATISFIED |
| 13 | peer_group_id boundary specified with BLOCK_PEER_GROUP_ID_CREATION | SATISFIED |
| 14 | Registry boundary specified with BLOCK_REGISTRY_CREATION | SATISFIED |
| 15 | Summary matrix included with all 13 boundary areas | SATISFIED |
| 16 | production_authority: NONE confirmed | SATISFIED |
| 17 | Violation response pattern documented | SATISFIED |
| 18 | Task 10 and Task 11 relationships documented | SATISFIED |

---

## 22. Hard Boundary Confirmation

| # | Hard Boundary | Confirmed |
|---|--------------|-----------|
| 1 | No candidate records created | YES |
| 2 | No PGF candidate artifacts produced | YES |
| 3 | No peer_group_registry.yaml or production registry | YES |
| 4 | No final peer assignments | YES |
| 5 | No canonical peer_group_id values | YES |
| 6 | No SAI mutation | YES |
| 7 | No runtime code | YES |
| 8 | No validation code | YES |
| 9 | No market data integration | YES |
| 10 | No trading/execution scope | YES |
| 11 | Task 7 not started | YES |

---

## 23. Final Status Marker

```
BOUNDARY_RULES_PREFLIGHT_COMPLETE
```

---

*End of boundary rules specification.*
