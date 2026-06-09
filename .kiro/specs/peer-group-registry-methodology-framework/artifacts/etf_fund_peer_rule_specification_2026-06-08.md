# Peer Group Registry Methodology Framework — ETF/Fund Peer Rule Specification

**Artifact**: etf_fund_peer_rule_specification_2026-06-08.md
**Task**: Task 4 — Create ETF/Fund Peer Rule Specification
**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: PGMF_TASK_4_ETF_FUND_RULE_READY_FOR_HUMAN_REVIEW

**Purpose**: This document specifies the complete methodology for ETF and fund peer comparison within PGF-09, defines the etf_peer and benchmark_context roles, identifies required comparison fields, establishes validation rules, and documents all blocked comparison patterns.

**Hard boundaries confirmed**:
- No peer_group_registry.yaml created
- No ETFs, funds, indices, or companies assigned to final peer groups
- No canonical peer_group_id values created
- No SAI artifact modification
- No implementation code
- No market data integration
- No broker, exchange, ATS, or trading venue connection
- No order routing or execution logic

---

## 1. Why ETFs and Funds Are Never Company Peers

ETF and fund comparison requires a fundamentally different methodology from company peer comparison:

| Dimension | Company Peer Comparison | ETF/Fund Peer Comparison |
|-----------|------------------------|--------------------------|
| Business model | Revenue, margins, competitive position | Replication method, benchmark tracking |
| Valuation | P/E, EV/EBITDA, P/FCF, P/B | TER, tracking difference, tracking error |
| Quality | Earnings quality, cashflow quality, balance sheet | Replication quality, liquidity, holdings overlap |
| Risk | Credit risk, operating leverage, customer concentration | Counterparty risk (synthetic), concentration (look-through), liquidity |
| Performance | Return vs. peers on operational metrics | Return vs. benchmark (tracking), cost efficiency |

Mixing ETFs with company peers conflates two incompatible comparison frameworks. Comparing QQQ (ETF tracking Nasdaq-100) with NVDA (a constituent company) is a category error: QQQ's performance is the Nasdaq-100 index minus costs, while NVDA's performance reflects idiosyncratic business execution.

**Source authority**: SRC-F-01 (ETF_methodology_authority — Morningstar), SRC-F-02 (ETF_methodology_authority — Columbia Law)

---

## 2. Why Indices Are benchmark_context Only

An index is a mathematical construct representing an aggregation of constituent securities. It is not an investable entity. An index has no TER, no AUM, no tracking error, no domicile, no replication method.

Indices serve one purpose: they are reference instruments for relative performance measurement (SAI-BLK-19/20) and for ETF tracking quality comparison (PGF-09).

An index must NEVER be: a valuation peer, a core_peer, an adjacent_peer, or an etf_peer.
An index always receives: `asset_type = index`, `peer_role = benchmark_context`, `comparison_mode_allowed = benchmark_context_comparison`.

---

## 3. etf_peer Role Definition

### 3.1 When etf_peer Is Valid

`peer_role = etf_peer` is valid ONLY when:
- `asset_type` is etf or fund
- Comparison occurs within PGF-09 or ETF/fund comparison logic
- Subject asset and peer share the same or materially overlapping `benchmark_index`
- At least cost/tracking/liquidity evidence is available for both assets

### 3.2 When etf_peer Is Blocked

- `asset_type = company` — company assets MUST NEVER receive etf_peer
- `asset_type = index` — indices are benchmark_context only
- `asset_type = private_company` — no ETF comparison methodology applicable
- No `benchmark_index` available for the subject asset
- Proposed peer ETF tracks a different, non-overlapping benchmark_index

### 3.3 etf_peer Comparison Mode

When `peer_role = etf_peer`: `comparison_mode_allowed = ETF_fund_comparison`
- Permits: TER, tracking_difference, tracking_error, AUM, spread, holdings_overlap, domicile, replication_method, distribution_policy, lookthrough_concentration comparison
- Does NOT permit: valuation_comparison, operating_metric_comparison, market_behavior_comparison

---

## 4. benchmark_context Role Definition

### 4.1 When benchmark_context Is Valid

- Asset is an index serving as reference frame for relative performance (SAI-BLK-19/20)
- Asset is an ETF or sector fund listed as reference instrument in a company peer family
- Asset is used as benchmark reference for tracking_difference comparison within PGF-09

### 4.2 benchmark_context Comparison Mode

`comparison_mode_allowed = benchmark_context_comparison`
- Permits only: comparison of the subject asset's performance relative to this benchmark reference
- Does NOT permit: valuation_comparison, operating_metric_comparison, ETF_fund_comparison, ecosystem_context_only
- benchmark_context is NOT a valuation peer role under any circumstances

### 4.3 Benchmark Context Instrument Examples (Illustrative — Not Final Assignments)

| Company Family | Illustrative benchmark_context Instruments | Role |
|---------------|-------------------------------------------|------|
| PGF-01 (AI Semiconductors) | SOX, SMH, QQQ | Relative strength reference |
| PGF-02 (Cybersecurity) | CIBR, HACK, IGV | Sector performance context |
| PGF-03 (Payments) | IPAY, XLF | Sector performance context |
| PGF-06 (Defense) | ITA, XAR | Sector performance context |
| PGF-07 (Industrials) | XLI, GRID | Sector performance context |
| PGF-08 (Banks/Financials) | XLF, EUFN, KRE | Sector and regional context |

These ETFs/indices appear in company families ONLY as `peer_role = benchmark_context`. They NEVER appear as core_peer or adjacent_peer. Their ETF-specific fields are NOT used in this context — only price/return data serves as a reference frame.

---

## 5. ETF/Fund Comparison Field Set

Source authority: SRC-F-01 (Morningstar), SRC-F-02 (Columbia Law), SRC-F-03 (etf.com), SRC-F-04 (Morningstar).

| Field | Type | Requirement | Description | Why It Matters |
|-------|------|-------------|-------------|---------------|
| `benchmark_index` | string | REQUIRED_IF_APPLICABLE | Index the ETF/fund replicates | Defines the ETF peer universe: same benchmark_index = valid peer group |
| `TER` | decimal | REQUIRED_IF_AVAILABLE | Total Expense Ratio (annual %) | Primary cost indicator but insufficient alone (excludes transaction costs, lending income) |
| `AUM` | decimal | REQUIRED_IF_AVAILABLE | Assets Under Management (millions) | Scale indicator: larger AUM correlates with tighter spreads and better tracking |
| `tracking_difference` | decimal | REQUIRED_IF_AVAILABLE | Annual fund return minus benchmark return | Most comprehensive cost measure — captures ALL net costs to investor |
| `tracking_error` | decimal | REQUIRED_IF_AVAILABLE | Std dev of daily return differences (annualized) | Consistency/risk measure, NOT cost measure. High = inconsistent replication |
| `spread` | decimal | REQUIRED_IF_AVAILABLE | Bid-ask spread (% or bps) | Market microstructure quality — wider spreads = higher implicit transaction costs |
| `holdings_overlap` | decimal | REQUIRED_IF_AVAILABLE | Overlap with other ETFs (0.0–1.0) | Hidden concentration risk: "different" ETFs may share 60–80% of same holdings |
| `domicile` | string | REQUIRED_IF_AVAILABLE | UCITS / 1940-Act / other | Affects TER range, tax treatment, distribution policy, regulatory structure |
| `replication_method` | enum | REQUIRED_IF_AVAILABLE | physical_full / physical_sampled / synthetic | Affects tracking quality, cost structure, and counterparty risk |
| `distribution_policy` | enum | REQUIRED_IF_AVAILABLE | accumulating / distributing | Affects total return tracking and tax treatment |
| `lookthrough_concentration` | decimal | REQUIRED_IF_AVAILABLE | Top-10 holdings weight (0.0–1.0) | Single-name concentration risk in underlying portfolio |

### 5.1 Tracking Difference vs. Tracking Error

| Metric | Measures | Type | Use Case |
|--------|----------|------|----------|
| **tracking_difference** | Cumulative deviation from benchmark over period | Cost measure | Total real cost over 12 months vs. holding index directly |
| **tracking_error** | Volatility of daily return deviations | Consistency/risk measure | How reliably the ETF replicates the index day-to-day |

A fund can have zero tracking error and significant tracking difference (consistent daily underperformance). Conversely, high tracking error with positive lending income may yield favorable tracking difference. Both metrics required for complete comparison (SRC-F-01).

### 5.2 TER Alone Is Insufficient

TER does not capture: transaction costs from rebalancing, securities lending income, tax drag, sampling effects, swap costs for synthetic ETFs. tracking_difference is the superior cost measure because it captures ALL net cost effects. UCITS vs. 1940-Act domicile creates TER differences due to regulatory cost structures, not efficiency (SRC-F-04).

---

## 6. Validation Rules

### 6.1 Same-Index Requirement

Direct ETF peer comparison (etf_peer, ETF_fund_comparison) requires same or materially overlapping `benchmark_index`. Comparing a Nasdaq-100 ETF with an S&P 500 ETF on tracking_difference is meaningless — differences reflect index composition, not fund quality (SRC-F-03).

Allowed: QQQ vs. QQQM (same Nasdaq-100 benchmark)
Blocked: QQQ vs. SPY (different benchmarks)

### 6.2 Multi-Dimensional Requirement (SRC-F-02 Columbia Law)

ETF peer comparison must use multiple dimensions. Name/theme similarity alone is INSUFFICIENT. A valid etf_peer comparison requires at minimum: TER + (tracking_difference OR tracking_error) + domicile + replication_method. Single-field comparison is not diagnostic.

### 6.3 UCITS vs. 1940-Act Domicile Handling

UCITS and 1940-Act variants of the same index ETF are valid peers but domicile differences MUST be documented. Domicile affects TER range, tax efficiency, distribution policy, and cross-border accessibility. TER comparisons without domicile context are misleading.

### 6.4 Synthetic vs. Physical Replication

Synthetic and physical ETFs tracking the same index are valid peers but replication method differences MUST be documented. Synthetic ETFs introduce counterparty risk not present in physical ETFs. `replication_method` must be populated before any tracking comparison is valid.

### 6.5 index_license_required Compliance

If `index_license_required = true` for an index, all ETFs referencing that benchmark must respect index data licensing terms. This is a compliance readiness placeholder — no market data integration occurs in v1.

---

## 7. Blocked Comparison Structures

| Blocked Structure | Why Invalid | Correct Alternative |
|------------------|-------------|---------------------|
| Company asset with peer_role = etf_peer | etf_peer valid ONLY for etf/fund | Use core_peer or adjacent_peer for company |
| ETF/fund with peer_role = core_peer against company | ETFs are not business rivals | ETF appears as benchmark_context in company family |
| ETF/fund with peer_role = adjacent_peer against company | ETFs are not substitutes for companies | benchmark_context only |
| Index with core_peer, adjacent_peer, or etf_peer | Index is a mathematical construct, not an entity | benchmark_context only |
| ETF comparison without benchmark_index | Tracking comparison is meaningless without knowing what is tracked | Block comparison; peer_comparison_allowed = false |
| ETF comparison with TER only | TER alone is insufficient (SRC-F-01, SRC-F-02) | Require TER + tracking data + domicile; else financial_comparability_gate_status = blocked |
| QQQ as core_peer for NVDA | ETF/constituent relationship is NOT a peer relationship | QQQ = benchmark_context in PGF-01 |
| SPY as etf_peer for QQQ | Different benchmark indices (S&P 500 vs. Nasdaq-100) | Not valid same-index peers; may compare holdings_overlap only |

---

## 8. SAI-BLK-21 Graceful Degradation for ETF/Fund Peer Data Gaps

### 8.1 When ETF/Fund Peer Data Is Incomplete

- `financial_comparability_gate_status` = partial or blocked
- `peer_comparison_allowed` = false (if below minimum threshold)
- `data_quality_status` = low or insufficient
- SAI-BLK-21 must NOT fabricate ETF comparison metrics
- SAI-BLK-21 must NOT fall back to company comparison methodology for ETFs

### 8.2 When Peer Group Registry Is Unavailable

SAI-BLK-21 produces:
```
deferred_dependency_notes: "Peer Group Registry not yet available — peer comparison interpretation blocked; ad-hoc peer comparisons are prohibited per SAI architecture."
```

Identical behavior regardless of asset_type (company or ETF/fund).

### 8.3 When Peer Group Exists But Evidence Is Partial

- SAI-BLK-21 may produce partial observations using available dimensions
- Must flag missing comparison dimensions explicitly
- Must set `data_quality_status = low` and document the gap
- Must NOT extrapolate missing tracking data from TER alone

---

## 9. Source Authority Mapping

| Principle | Source | Authority Domain | Tier |
|-----------|--------|------------------|------|
| Tracking difference vs. tracking error are distinct; both required | SRC-F-01 (Morningstar) | ETF_methodology_authority | 1 |
| Name/theme similarity alone insufficient for ETF peer comparison | SRC-F-02 (Columbia Law) | ETF_methodology_authority | 2 |
| Same-index ETFs form the most natural peer group | SRC-F-03 (etf.com) | ETF_methodology_authority | 2 |
| Domicile (UCITS vs. 1940-Act) affects TER ranges | SRC-F-04 (Morningstar) | ETF_methodology_authority | 2 |
| ETF/fund comparison is fundamentally different from company comparison | SRC-F-01, SRC-F-02 | ETF_methodology_authority | 1, 2 |
| etf_peer role defined in six-role taxonomy | SRC-D-01 + SRC-F-01 | strategic_peer_logic_authority + ETF_methodology_authority | 1 |
| Indices are benchmark_context only | GICS/ICB inference | classification_authority | 1 |
| ISO 10383 MIC for listed ETFs | SRC-I-01 | identity_authority | 1 |

---

## 10. Allowed and Blocked Comparison Examples

These examples illustrate methodology rules. They are NOT final peer group assignments.

### 10.1 Allowed: Same-Index ETF Peer Comparison

QQQ vs. QQQM — both track Nasdaq-100, both etf, both etf_peer, valid ETF_fund_comparison on TER, tracking_difference, tracking_error, AUM, spread, domicile.

### 10.2 Allowed: Benchmark Context in Company Family

SMH in PGF-01 as benchmark_context — only price/return data used as reference for relative strength. ETF-specific fields NOT used in this context.

### 10.3 Blocked: ETF as Core Peer for Company

QQQ proposed as core_peer for NVDA — INVALID. QQQ is a container, NVDA is a constituent. Correct: QQQ = benchmark_context in PGF-01.

### 10.4 Blocked: Cross-Index ETF Peer Comparison

QQQ (Nasdaq-100) vs. SPY (S&P 500) as etf_peer — BLOCKED. Different benchmark indices. Tracking comparison meaningless.

### 10.5 Blocked: Company with etf_peer Role

NVDA with peer_role = etf_peer — INVALID. Company assets NEVER receive etf_peer. Correct: core_peer or adjacent_peer within PGF-01.

### 10.6 Allowed: UCITS vs. 1940-Act Same-Index Comparison

iShares Core S&P 500 UCITS ETF vs. IVV (1940-Act) — both track S&P 500, valid etf_peer, domicile difference documented, TER comparison with domicile context.

---

## 11. Relationship to PGF-09

This specification operationalizes PGF-09 (ETF/Fund Peer Rule) from the scope preflight by providing:
- Exact field taxonomy for ETF/fund comparison (Section 5)
- Validation rules governing when comparison is valid or blocked (Section 6)
- Role assignments with hard constraints (Sections 3–4)
- Blocked patterns preventing category errors (Section 7)
- SAI graceful degradation behavior (Section 8)

---

## 12. Boundary Confirmations

| Boundary | Status |
|----------|--------|
| No peer_group_registry.yaml created | CONFIRMED |
| No ETFs, funds, indices, or companies assigned to final peer groups | CONFIRMED |
| No canonical peer_group_id values created | CONFIRMED |
| No SAI artifact modification | CONFIRMED |
| No implementation code | CONFIRMED |
| No market data integration | CONFIRMED |
| No broker/exchange/ATS/trading venue connection | CONFIRMED |
| Tasks 1, 2, 3 artifacts unchanged | CONFIRMED |
| Task 5 not started | CONFIRMED |
| Tactical Momentum spec not started | CONFIRMED |

---

## Artifact Status

```
PGMF_TASK_4_ETF_FUND_RULE_READY_FOR_HUMAN_REVIEW
```

---

*End of ETF/fund peer rule specification.*
