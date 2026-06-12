# PGF-09: ETF / Fund Peer Rule — Candidate Record Drafts (Preflight)

---
production_authority: NONE
preliminary: true
family_id: PGF-09
family_name: ETF / Fund Peer Rule
---

## 1. Document Boundary

This document contains **rule-based subcluster records** for PGF-09: ETF / Fund Peer Rule.

**IMPORTANT**: PGF-09 is fundamentally different from PGF-01 through PGF-08. It is a **rule-based family**, NOT a ticker-based family. There are no individual company ticker records. Instead, PGF-09 defines subclusters by rule, and individual ETF membership within each subcluster is deferred to future production registry creation.

This document produces 4 rule-based subcluster records (not individual ticker candidate records).

---

## 2. Source Authority

| Source ID | Authority Domain | Tier Level | Description |
|-----------|-----------------|------------|-------------|
| SRC-F-01 | ETF_methodology_authority | Tier 1 | ETF peer methodology and role assignment |
| SRC-B-01 | classification_authority | Tier 1 | Family classification and boundary enforcement |

---

## 3. Rule-Based Family Context

### 3.1 Core Principle

PGF-09 is **rule-based** rather than **ticker-based**. Unlike company families (PGF-01 through PGF-08) which enumerate specific tickers with specific peer roles, PGF-09 defines classification rules that determine ETF/fund peer grouping.

### 3.2 Boundary Rules

- **ETFs and funds do NOT receive company peer groups.** An ETF is never treated as a "company peer" of another entity.
- **ETFs in company families (PGF-01 through PGF-08) carry `peer_role = benchmark_context`.** When an ETF appears in a company family, it serves only as a benchmark reference — never as a direct peer.
- **Within PGF-09, ETFs carry `peer_role = etf_peer`.** ETFs are peers only to other ETFs within the same subcluster.
- **No ETF-to-company fallback permitted.** An ETF must never fall back into a company peer group if its ETF peer group is unavailable.
- **No company-to-ETF fallback permitted.** A company must never fall back into an ETF peer group if its company peer group is unavailable.

### 3.3 Implication

The boundary between ETF peers and company peers is absolute and enforced at the registry level. Cross-boundary fallback is blocked by rule `BLOCK_ETF_COMPANY_FALLBACK`.

---

## 4. ETF/Fund Comparison Dimensions

The following 10 dimensions define comparability within the ETF/Fund peer universe (sourced from scope preflight):

| # | Dimension | Description | Applicability |
|---|-----------|-------------|---------------|
| 1 | Expense Ratio (TER) | Total expense ratio as primary cost comparator | All subclusters |
| 2 | Tracking Difference | Deviation from benchmark index return | ETF-B, ETF-C |
| 3 | AUM (Assets Under Management) | Fund size and liquidity proxy | All subclusters |
| 4 | Bid-Ask Spread | Trading cost and liquidity measure | All subclusters |
| 5 | Index/Benchmark Alignment | Which index the ETF tracks or references | ETF-B, ETF-C |
| 6 | Holdings Concentration | Top-N holdings weight (HHI or similar) | All subclusters |
| 7 | Sector/Theme Exposure | Primary sector or thematic tilt | ETF-A, ETF-C |
| 8 | Geographic Exposure | Regional allocation breakdown | All subclusters |
| 9 | Active Share | Degree of deviation from passive benchmark | ETF-D |
| 10 | Fund Structure | ETF vs. mutual fund vs. UCITS wrapper | All subclusters |

---

## 5. Subcluster Definitions

### 5.1 ETF-A: Thematic ETFs

**Definition**: ETFs organized around investment themes rather than traditional sector/index classification.

**Scope**: Technology, AI/machine learning, cybersecurity, defense/aerospace, clean energy, genomics, blockchain, robotics, and other thematic mandates.

**Key Comparison Dimensions**: Expense Ratio, AUM, Holdings Concentration, Sector/Theme Exposure, Geographic Exposure.

**Boundary**: A thematic ETF is one whose prospectus mandate is defined by a theme rather than a market-cap-weighted index or traditional GICS sector.

---

### 5.2 ETF-B: Broad Market / Index ETFs

**Definition**: ETFs that track broad market or multi-sector indices providing diversified market exposure.

**Scope**: S&P 500 trackers, Nasdaq-100 trackers, MSCI World, FTSE All-World, total market (VTI equivalents), Russell 2000/3000.

**Key Comparison Dimensions**: Expense Ratio, Tracking Difference, AUM, Bid-Ask Spread, Index/Benchmark Alignment.

**Boundary**: Broad market ETFs track indices spanning multiple sectors. Single-sector index ETFs belong in ETF-C.

---

### 5.3 ETF-C: Sector ETFs

**Definition**: ETFs that provide exposure to a single GICS sector or narrow industry group via an index-tracking methodology.

**Scope**: XLF (Financials), XLI (Industrials), XLY (Consumer Discretionary), XLK (Technology), XLE (Energy), XLV (Healthcare), XLP (Consumer Staples), XLU (Utilities), XLRE (Real Estate), XLC (Communication Services), and international sector equivalents.

**Key Comparison Dimensions**: Expense Ratio, Tracking Difference, AUM, Index/Benchmark Alignment, Sector/Theme Exposure, Geographic Exposure.

**Boundary**: Sector ETFs track a recognized sector index. Thematic ETFs that happen to be sector-adjacent but follow a thematic mandate belong in ETF-A.

---

### 5.4 ETF-D: Active / Semi-Active Funds

**Definition**: Funds employing active management or semi-active strategies (smart beta, factor-tilted, actively managed ETFs).

**Scope**: Actively managed ETFs (e.g., ARK funds), smart beta / factor ETFs, semi-transparent active ETFs, and traditional mutual funds with ETF share classes.

**Key Comparison Dimensions**: Expense Ratio, AUM, Active Share, Holdings Concentration, Geographic Exposure.

**Boundary**: Any fund where the portfolio manager exercises discretion beyond pure index replication. Active Share > 20% is a proxy threshold.

---

## 6. Subcluster Rule Records

### 6.1 Record 1: ETF-A Subcluster Rule (Thematic ETFs)

```yaml
candidate_record_id: PGF09-RULE-001
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-09
family_name: ETF / Fund Peer Rule
asset_name: ETF Subcluster ETF-A — Thematic ETFs
asset_type: etf
object_type: etf
legal_entity_name: null
instrument_type: etf
ticker_candidates: null
ISIN_candidates: null
exchange_candidates: null
region: Global
domicile: null
reporting_currency: null
trading_currency: null
accounting_standard: null
fiscal_year_end: null
listing_variant_type: null
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-F-01", authority_domain: "ETF_methodology_authority", tier_level: "Tier 1", field_name: "peer_role"}
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "family_id"}
methodology_decision_references: ["PGMF-DEC-05"]
field_taxonomy_mapping_status: COMPLETE
peer_role: etf_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: null
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Rule-based subcluster record. Thematic ETFs (technology, AI, cybersecurity, defense, clean energy). Individual ETF tickers will be populated during future production registry creation."
```

---

### 6.2 Record 2: ETF-B Subcluster Rule (Broad Market / Index ETFs)

```yaml
candidate_record_id: PGF09-RULE-002
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-09
family_name: ETF / Fund Peer Rule
asset_name: ETF Subcluster ETF-B — Broad Market / Index ETFs
asset_type: etf
object_type: etf
legal_entity_name: null
instrument_type: etf
ticker_candidates: null
ISIN_candidates: null
exchange_candidates: null
region: Global
domicile: null
reporting_currency: null
trading_currency: null
accounting_standard: null
fiscal_year_end: null
listing_variant_type: null
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-F-01", authority_domain: "ETF_methodology_authority", tier_level: "Tier 1", field_name: "peer_role"}
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "family_id"}
methodology_decision_references: ["PGMF-DEC-05"]
field_taxonomy_mapping_status: COMPLETE
peer_role: etf_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: null
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Rule-based subcluster record. Broad Market / Index ETFs (S&P 500, Nasdaq-100, MSCI World, total market trackers). Individual ETF tickers will be populated during future production registry creation."
```

---

### 6.3 Record 3: ETF-C Subcluster Rule (Sector ETFs)

```yaml
candidate_record_id: PGF09-RULE-003
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-09
family_name: ETF / Fund Peer Rule
asset_name: ETF Subcluster ETF-C — Sector ETFs
asset_type: etf
object_type: etf
legal_entity_name: null
instrument_type: etf
ticker_candidates: null
ISIN_candidates: null
exchange_candidates: null
region: Global
domicile: null
reporting_currency: null
trading_currency: null
accounting_standard: null
fiscal_year_end: null
listing_variant_type: null
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-F-01", authority_domain: "ETF_methodology_authority", tier_level: "Tier 1", field_name: "peer_role"}
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "family_id"}
methodology_decision_references: ["PGMF-DEC-05"]
field_taxonomy_mapping_status: COMPLETE
peer_role: etf_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: null
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Rule-based subcluster record. Sector ETFs (XLF, XLI, XLY, XLK, XLE, XLV, XLP, XLU, XLRE, XLC and international sector equivalents). Individual ETF tickers will be populated during future production registry creation."
```

---

### 6.4 Record 4: ETF-D Subcluster Rule (Active / Semi-Active Funds)

```yaml
candidate_record_id: PGF09-RULE-004
candidate_record_id_status: PREFLIGHT_NON_PRODUCTION
production_authority: NONE
preliminary: true
Candidate_Status: CANDIDATE_DRAFT
family_id: PGF-09
family_name: ETF / Fund Peer Rule
asset_name: ETF Subcluster ETF-D — Active / Semi-Active Funds
asset_type: etf
object_type: etf
legal_entity_name: null
instrument_type: etf
ticker_candidates: null
ISIN_candidates: null
exchange_candidates: null
region: Global
domicile: null
reporting_currency: null
trading_currency: null
accounting_standard: null
fiscal_year_end: null
listing_variant_type: null
source_authority_status: SOURCE_AUTHORITY_PRESENT
source_authority_references:
  - {source_id: "SRC-F-01", authority_domain: "ETF_methodology_authority", tier_level: "Tier 1", field_name: "peer_role"}
  - {source_id: "SRC-B-01", authority_domain: "classification_authority", tier_level: "Tier 1", field_name: "family_id"}
methodology_decision_references: ["PGMF-DEC-05"]
field_taxonomy_mapping_status: COMPLETE
peer_role: etf_peer
peer_group_id: PREFLIGHT_PLACEHOLDER_NOT_CANONICAL
peer_group_id_status: NOT_CREATED
peer_comparison_allowed: false
blocked_reason: null
unsupported_status: null
comparability_adjustment_required: null
comparability_note: null
market_data_fields_status: NOT_POPULATED_IN_PREFLIGHT
trading_governance_fields_status: FUTURE_COMPLIANCE_REFERENCE_NOT_OPERATIONAL
SAI_contract_status: PREFLIGHT_NOT_CANONICAL
human_review_status: NOT_REVIEWED
CTO_approval_status: NOT_APPROVED
notes: "Rule-based subcluster record. Active / Semi-Active Funds (actively managed ETFs, smart beta, factor-tilted funds). Expense ratio and active share are primary comparison dimensions. Individual fund tickers will be populated during future production registry creation."
```

---

## 7. Unresolved Decisions

The following decisions remain open and require CTO/methodology authority resolution before PGF-09 can advance to production:

| # | Decision | Context | Impact |
|---|----------|---------|--------|
| 1 | UCITS vs. US-domiciled ETF peer treatment | Same underlying index (e.g., S&P 500) can have both US-domiciled (SPY, VOO) and UCITS-domiciled (VUSA.L, CSPX.L) ETFs. Should they be peers within the same subcluster or separated by domicile? | Affects ETF-B and ETF-C subcluster composition. May require domicile-aware sub-grouping. |
| 2 | Leveraged/Inverse ETF peer universe | Leveraged (2×, 3×) and inverse (-1×, -2×) ETFs have fundamentally different risk/return profiles than 1× ETFs tracking the same index. Do they require an entirely separate peer universe (ETF-E)? | May require a 5th subcluster or explicit exclusion rule. |
| 3 | AUM and TER normalization across currencies | ETFs denominated in USD vs. EUR (or other currencies) have AUM and TER figures that are not directly comparable without FX adjustment. How should cross-currency normalization be handled? | Affects all subclusters with Global region scope. Requires FX reference date convention. |

---

## 8. ETF/Fund Boundary Enforcement Rules

These rules are absolute and enforced at the registry level. No override or fallback is permitted.

| Rule ID | Rule Statement | Enforcement Mechanism |
|---------|---------------|----------------------|
| RULE-PGF09-01 | ETFs NEVER receive company peer groups | Registry validation gate: `object_type = etf` → BLOCK assignment to company peer_group_id |
| RULE-PGF09-02 | ETFs in company families (PGF-01 through PGF-08) carry `peer_role = benchmark_context` ONLY | Role enforcement: ETF in company family → force `peer_role = benchmark_context` |
| RULE-PGF09-03 | Within PGF-09, ETFs carry `peer_role = etf_peer` | Role enforcement: ETF in PGF-09 → force `peer_role = etf_peer` |
| RULE-PGF09-04 | No ETF-to-company fallback permitted | Fallback block: `BLOCK_ETF_COMPANY_FALLBACK` — if ETF peer group unavailable, do NOT fall back to company peer group |
| RULE-PGF09-05 | No company-to-ETF fallback permitted | Fallback block: `BLOCK_ETF_COMPANY_FALLBACK` — if company peer group unavailable, do NOT fall back to ETF peer group |

### Enforcement Summary

```
IF object_type = "etf" AND family_id IN [PGF-01..PGF-08]:
    ENFORCE peer_role = "benchmark_context"
    BLOCK peer_comparison_allowed = true

IF object_type = "etf" AND family_id = "PGF-09":
    ENFORCE peer_role = "etf_peer"
    ALLOW peer_comparison_allowed = true (within subcluster only)

IF fallback_requested AND cross_boundary(etf ↔ company):
    BLOCK with BLOCK_ETF_COMPANY_FALLBACK
    RETURN error: "Cross-boundary fallback prohibited"
```

---

## 9. Summary

| Category | Count | Status Distribution |
|----------|-------|---------------------|
| Rule-based subcluster records | 4 | 4 × CANDIDATE_DRAFT |
| Total records | 4 | — |

### Record Inventory

| Record ID | Subcluster | Asset Name | Status |
|-----------|-----------|------------|--------|
| PGF09-RULE-001 | ETF-A | Thematic ETFs | CANDIDATE_DRAFT |
| PGF09-RULE-002 | ETF-B | Broad Market / Index ETFs | CANDIDATE_DRAFT |
| PGF09-RULE-003 | ETF-C | Sector ETFs | CANDIDATE_DRAFT |
| PGF09-RULE-004 | ETF-D | Active / Semi-Active Funds | CANDIDATE_DRAFT |

### Why CANDIDATE_DRAFT?

All 4 records carry `Candidate_Status: CANDIDATE_DRAFT` because:
- The **rule framework** is defined (subcluster boundaries, comparison dimensions, enforcement rules)
- The **individual ETF membership** within each subcluster is future work (requires production data feeds)
- No individual ETF tickers have been assigned to subclusters yet
- The records represent structural placeholders for future population

---

## 10. No-Invention Confirmation

- All 4 subclusters (ETF-A, ETF-B, ETF-C, ETF-D) are sourced directly from the scope preflight document
- No new ETF tickers have been invented or assigned
- No individual ETF candidate records exist — only rule-based subcluster records
- Sector ETF examples (XLF, XLI, XLY, XLK, XLE) are referenced as illustrative scope indicators, NOT as assigned members
- Thematic ETF categories (technology, AI, cybersecurity, defense, clean energy) are scope descriptors, NOT ticker assignments

---

*End of PGF-09 candidate record drafts.*
