# Peer Group Registry Methodology Framework — Market Data Readiness Specification

**Artifact**: market_data_readiness_specification_2026-06-08.md
**Task**: Task 7 — Create Market Data Readiness Specification
**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: PGMF_TASK_7_MARKET_DATA_READINESS_READY_FOR_HUMAN_REVIEW

**Purpose**: Specifies market data readiness fields, clearly separating CURRENT_MODEL_NULLABLE (schema reservations) from FUTURE_VENDOR_INTEGRATION (require commercial agreements), and defining the boundary preventing premature data integration.

**Boundary statement**: Market data readiness evidence is included to prevent architectural drift. It does not authorize real-time market data consumption, broker integration, exchange connectivity, trading enablement, order-routing logic, or regulated activity. No API keys, credentials, vendor accounts, or data entitlements are requested or created.

**Hard boundaries**: No peer_group_registry.yaml. No final peer assignments. No canonical peer_group_id. No SAI mutation. No code. No market data integration. No broker/exchange/ATS. No trading logic.

Source authority: SRC-I-01 (identity_authority — ISO 10383 MIC), SRC-I-02/03/04/05 (exchange licensing — Euronext, Deutsche Börse, Nasdaq, NYSE), SRC-I-06 (LSEG data vendor), SRC-I-07 (Euronext non-display policy).


---

## 1. Scope Classification

| Scope Label | Meaning | v1 Status |
|-------------|---------|-----------|
| `CURRENT_MODEL_NULLABLE` | Field MUST exist in v1 registry schema; value is null until data vendor agreement exists | Present in schema, null |
| `FUTURE_VENDOR_INTEGRATION` | Field is NOT in v1 schema; requires active commercial data agreement before it can be added | Excluded from v1 schema |
| `FUTURE_COMPLIANCE_REFERENCE` | Reserved vocabulary for trading governance; no current obligations | Excluded from v1 schema |

---

## 2. CURRENT_MODEL_NULLABLE Fields (Must Exist in v1 Schema)

These 8 fields MUST be present in the Layer 2 registry schema from day one, even with null values. They prevent architectural rewrite when market data is later integrated.

| Field | Type | Allowed Values | asset_type Applicability | Why It Must Exist Now |
|-------|------|----------------|--------------------------|----------------------|
| `exchange_mic` | string | ISO 10383 four-character MIC (e.g., XNAS, XETR, XAMS, XNYS) | company, etf, fund (listed) | Cross-listing normalization: ASML on XAMS vs. XNAS are distinct listings of one canonical_object_id. Without exchange_mic, the registry cannot differentiate listings when quote data is added. |
| `market_data_source` | string | Exchange origin identifier (e.g., "XETR", "XNAS") | company, etf, fund (listed) | Exchange origin of price data — distinct from data_vendor (aggregator). If these are one field, the registry conflates where data originates (exchange) with who delivers it (vendor). |
| `data_vendor` | string | Aggregator/distributor name (e.g., "LSEG", "Bloomberg") | company, etf, fund (listed) | Data aggregator/distributor — distinct from market_data_source. LSEG aggregates from 550+ venues (SRC-I-06); Bloomberg is an alternative. Separation enables vendor switching without changing source attribution. |
| `data_latency_class` | enum | real_time / delayed_15min / end_of_day | company, etf, fund (listed) | Declares data freshness class at record level. Required for data governance: a record declared delayed_15min has different staleness thresholds than real_time. Without this field, data quality assertions are impossible. |
| `exchange_timezone` | string | IANA timezone (e.g., Europe/Berlin, America/New_York, Europe/Amsterdam) | company, etf, fund (listed) | Quote timestamp normalization: XETR (CET) and XNAS (ET) timestamps cannot be compared without knowing each venue's timezone. Without this, cross-region quote staleness calculations are architecturally impossible. |
| `trading_calendar_id` | string | Exchange trading calendar reference (e.g., "XETR_2026", "XNAS_2026") | company, etf, fund (listed) | Quote staleness calculation: a delayed quote from XETR's last session must be evaluated against XETR's specific trading calendar (German holidays, 09:00–17:30 CET session). Without this, staleness logic has no session boundary reference. |
| `derived_data_policy` | enum | open / non_display_license_required / restricted | etf, fund, index | Whether analytics derived from this data require a non-display license. Euronext (SRC-I-07) defines non-display usage broadly: indices, VWAP, portfolio evaluation, analytics from real-time data all require separate licensing. Without this field, computed peer analytics may silently violate licensing terms. |
| `index_license_required` | boolean | true / false | index, etf | Whether an index data license is required. Nasdaq (SRC-I-04) and Euronext (SRC-I-02) license index data separately from quote data. Without this, the registry cannot flag unlicensed index consumption when benchmark context instruments are used. |

### 2.1 Exchange-Specific Notes

| Exchange | MIC | Timezone | Calendar Notes |
|----------|-----|----------|---------------|
| Xetra (Deutsche Börse) | XETR | Europe/Berlin (CET/CEST) | Regular: 09:00–17:30 CET; extended hours in development (08:00–22:00); German/Hesse holidays |
| Nasdaq | XNAS | America/New_York (ET) | Day Session: 04:00–20:00 ET; Night Session: 21:00–04:00 ET; maintenance gap 20:00–21:00 ET for corporate actions |
| NYSE | XNYS | America/New_York (ET) | NYSE Group operates 5 venues (XNYS, ARCX, XASE, XCIS, XNMS); each has distinct MIC; standard hours 09:30–16:00 ET with pre/post-market |
| Euronext Amsterdam | XAMS | Europe/Amsterdam (CET/CEST) | Regular: 09:00–17:30 CET; Dutch/French/Portuguese/Irish holidays per venue |
| Euronext Paris | XPAR | Europe/Paris (CET/CEST) | Regular: 09:00–17:30 CET; French bank holidays |
| Borsa Italiana (Euronext Milan) | XMIL | Europe/Rome (CET/CEST) | Regular: 09:00–17:30 CET; Italian bank holidays |
| Stockholm (Nasdaq Nordic) | STO | Europe/Stockholm (CET/CEST) | Regular: 09:00–17:30 CET; Swedish holidays |
| SIX Swiss Exchange | XSWX | Europe/Zurich (CET/CEST) | Regular: 09:00–17:30 CET; Swiss holidays |
| London Stock Exchange | XLON | Europe/London (GMT/BST) | Regular: 08:00–16:30 GMT; UK bank holidays |

---

## 3. FUTURE_VENDOR_INTEGRATION Fields (Not in v1 Schema)

These 9 fields are excluded from the v1 registry schema. They require active commercial data vendor agreements before they can be populated. Their absence from v1 prevents creating implied obligations or false data readiness claims.

| Field | Type | Description | Activation Condition |
|-------|------|-------------|---------------------|
| `realtime_entitlement_required` | boolean | Whether real-time data entitlement is needed for this asset at this venue | Active real-time data contract per exchange |
| `display_usage_allowed` | boolean | Whether data may be displayed to end users without additional license | Explicit display usage license per exchange |
| `non_display_usage_allowed` | boolean | Whether non-display derived analytics (VWAP, indices, portfolio evaluation) are licensed | Explicit non-display / derived-data license per exchange |
| `redistribution_allowed` | boolean | Whether data may be shared with or redistributed to third parties | Redistribution authorization per exchange |
| `professional_user_flag` | boolean | Whether the user/system is classified as professional (higher fees) or non-professional | User classification infrastructure and exchange-specific definition |
| `market_data_audit_required` | boolean | Whether compliance audit trail for data usage reporting is needed | Audit and compliance reporting infrastructure |
| `bid_ask_source` | string | Venue providing live bid/ask quote data | Active live feed subscription |
| `stale_quote_threshold` | integer | Minutes after which a quote from this venue is considered stale | Session-aware data infrastructure with exchange calendar integration |
| `quote_timestamp_required` | boolean | Whether bid/ask timestamps must be stored per quote | Feed integration infrastructure before timestamps can be captured |

---

## 4. Exchange / Listing Separation

### 4.1 Identity Layer Architecture

The market data readiness layer builds on the three-layer identity model:

```
Layer 1 — canonical_object_id: the economic entity (ASML the company)
Layer 2 — security_id + exchange_mic: a specific listing at a specific venue (ASML on XAMS; ASML ADR on XNAS)
Layer 2 — market_data_source: which exchange generated the price data for this listing
Layer 2 — data_vendor: which aggregator delivered the data
```

- `canonical_object_id` is the economic object — never a ticker, never a listing
- `security_id` / `figi` / `isin` identify instruments (listing-level)
- `exchange_mic` identifies the venue where the instrument is listed and traded
- `ticker` is a human-readable lookup key — NOT a stable identifier (changes on relisting)

### 4.2 Market Data Source vs. Data Vendor

These are distinct concepts that must be separate fields:

| Concept | Field | What It Represents | Example |
|---------|-------|-------------------|---------|
| Where data originates | `market_data_source` | The exchange where the price was formed | XETR (Xetra produced this price) |
| Who delivers data | `data_vendor` | The aggregator/distributor that transmits the data | LSEG (formerly Refinitiv — delivered this data from XETR) |

Why separation matters:
- A vendor switch (from LSEG to Bloomberg) changes `data_vendor` but NOT `market_data_source` — the price still originated at XETR
- An exchange migration (company moves primary listing from XLON to XNYS) changes `market_data_source` and `exchange_mic` but may not change `data_vendor`
- Provenance tracing requires knowing both: "this price came from XETR (source) via LSEG (vendor)"

### 4.3 Ticker Alone Is Never Sufficient

Ticker symbols:
- Are not globally unique ("ASML" on XAMS vs. "ASML" on XNAS are same company but different venues)
- Change on relisting, acquisition, exchange transfer (SRC-G-02 Intrinio)
- Do not identify which venue produced a price

Market data fields always require `exchange_mic` to disambiguate. A price without venue context is architecturally ambiguous.

---

## 5. Data Latency Classes

| data_latency_class | Description | Staleness Implication | Use Case |
|-------------------|-------------|----------------------|----------|
| `real_time` | Quotes delivered with sub-second to seconds delay from exchange | Stale after session close + stale_quote_threshold (future field) | Live trading decision support (future) |
| `delayed_15min` | Quotes delayed by 15 minutes from exchange (standard free-tier delay) | Stale after session close + 15 minutes + end-of-day threshold | Non-professional analytics, report generation |
| `end_of_day` | Closing prices only, available after session close | Stale after next session opens without update | Historical analysis, overnight reporting, peer comparison at close |

v1 implication: All CURRENT_MODEL_NULLABLE market data fields are null. No data_latency_class is active. When data is integrated, the class declaration governs staleness logic and display entitlement.

---

## 6. Timestamp, Timezone, and Trading Calendar

### 6.1 Why These Fields Are Needed Before Quotes Arrive

Quote freshness evaluation requires three pieces of context:
1. **exchange_timezone**: What timezone was the quote generated in? (A XETR quote at 17:30 CET is end-of-session; a XNAS quote at 17:30 ET is post-market.)
2. **trading_calendar_id**: Was the exchange open? (A Monday may be a holiday for XETR but a trading day for XNAS.)
3. **data_latency_class**: How delayed is this data? (A 15-minute delayed quote has different staleness meaning than a real-time quote.)

Without these three fields pre-defined in the schema, adding quote data later requires adding the fields AND backfilling all existing records. Schema reservation now prevents that rewrite.

### 6.2 Cross-Region Timestamp Normalization

When comparing a XETR-sourced quote (CET) with a XNAS-sourced quote (ET):
- The timestamp must be normalized to a common reference (UTC or the comparison logic must account for timezone offset)
- A quote from XETR at 17:30 CET is equivalent to 11:30 ET — well within XNAS trading hours
- A XETR end-of-day close at 17:30 CET is stale by the time XNAS closes at 16:00 ET (21:00 CET)
- `exchange_timezone` per listing record makes this normalization possible

---

## 7. Derived Data and Index Licensing

### 7.1 Non-Display / Derived Data Policy

Euronext (SRC-I-07) defines non-display usage broadly: any analytics computed from real-time exchange data — including indices, VWAP calculations, portfolio evaluation services, and analytic reference figures — require a non-display license separate from display usage.

For MoneyHorst:
- Any future computed peer analytics (e.g., peer-relative performance from exchange prices) are derived data
- If those analytics use licensed real-time or delayed exchange data, a non-display license is required
- The `derived_data_policy` field at record level declares whether this constraint applies

### 7.2 Index Licensing

Nasdaq (SRC-I-04) and Euronext (SRC-I-02) license index data separately from quote data. The index value (e.g., Nasdaq-100 level) requires a separate index data license from the constituent stock quotes.

For MoneyHorst:
- Benchmark context instruments (SMH, QQQ, CIBR, XLF, etc.) may track licensed indices
- The `index_license_required` field flags whether index data licensing applies
- No index data is consumed in v1 — the field is a compliance readiness placeholder

---

## 8. Validation Behavior in v1

### 8.1 Null Values Are Expected

In v1, all CURRENT_MODEL_NULLABLE fields carry null values for most records. This is correct behavior — no data vendor agreement exists yet. Null does not indicate an error; it indicates readiness-without-activation.

### 8.2 FUTURE_VENDOR_INTEGRATION Fields Are Absent

These 9 fields are NOT in the v1 schema at all. Attempting to populate them produces a schema violation. They will be added to the schema only when a commercial data vendor agreement is signed.

### 8.3 Missing exchange_mic for Listed Assets

If a listed asset (asset_type = company/etf/fund with primary_listing = true) does NOT have exchange_mic populated:
- This creates a **readiness warning** (the record is missing a structural field needed for future data integration)
- It does NOT create a runtime failure in this methodology phase (no data integration is active)
- The warning is governance-level, not blocking for peer comparison methodology purposes
- Peer comparison based on financial metrics, comparability gates, and governance fields proceeds normally without exchange_mic

### 8.4 Market Data Fields Must Not Create Trading Eligibility

The presence of CURRENT_MODEL_NULLABLE market data fields (even when populated in future) does NOT:
- Make an asset eligible for trading
- Enable order routing
- Authorize execution
- Create broker connectivity
- Imply any regulated activity

Market data fields serve analytics and peer comparison purposes only. Trading eligibility requires the FUTURE_COMPLIANCE_REFERENCE fields and the three-gate activation model defined in the trading governance boundary specification (Task 8).

---

## 9. SAI-BLK-21 Behavior

### 9.1 No Real-Time Quote Assumptions

SAI-BLK-21 must NOT assume real-time market data is available. In v1 and potentially in early data integration phases:
- No live bid/ask spreads are available
- No real-time price is available
- No intraday timestamps are available
- Peer comparison operates on methodology fields (peer_role, comparison_mode, financial comparability gate), NOT on live market data fields

### 9.2 No Fabricated Market Data

SAI-BLK-21 must NOT:
- Fabricate bid/ask spread values
- Invent timestamps for quotes
- Assume a data_latency_class without explicit field value
- Use stale_quote_threshold logic when the field is null (no threshold defined = no staleness assertion possible)

### 9.3 Degraded Output When Market Data Fields Are Null

When market data readiness fields are null (v1 default):
- Peer comparison based on financial methodology fields proceeds normally
- Market-behavior comparisons (SAI-BLK-19/20 relative strength, correlation) that require price data will surface `data_quality_status = insufficient` for real-time dimensions
- SAI-BLK-21 must document: "Market data readiness fields not yet populated — market-behavior comparisons limited to available historical data if any"

### 9.4 Peer Comparison on Methodology Fields Only

In v1, all peer comparison is based on:
- Methodology fields: peer_role, primary_family, subcluster, comparison_mode_allowed
- Financial comparability gate: business_model_similarity, market_cap_band, liquidity_band, margin/growth/leverage comparability
- Cross-region normalization: accounting_standard, reporting_currency, taxonomy_reference, comparability_adjustment_required
- Governance: effective_date, lifecycle_status, review_status

Market data fields (exchange_mic, exchange_timezone, data_latency_class, etc.) are NOT inputs to peer comparison logic in v1. They are schema reservations for future data integration.

---

## 10. Source Authority Mapping

| Principle | Source | Authority Domain | Tier |
|-----------|--------|------------------|------|
| ISO 10383 MIC as canonical venue identifier | SRC-I-01 (ISO/SWIFT) | identity_authority | 1 |
| Euronext market data licensing: display vs. non-display, real-time vs. delayed | SRC-I-02 (Euronext) | exchange_market_data | 1 |
| Deutsche Börse / Xetra market data: MIC XETR, CET timezone, German holiday calendar | SRC-I-03 (Deutsche Börse) | exchange_market_data | 1 |
| Nasdaq market data: professional vs. non-professional, index vs. quote licensing, near-24hr sessions | SRC-I-04 (Nasdaq) | exchange_market_data | 1 |
| NYSE market data: multiple MICs within NYSE Group, corporate action governance | SRC-I-05 (NYSE/ICE) | exchange_market_data | 1 |
| LSEG Real-Time Managed Distribution: market_data_source vs. data_vendor distinction, 550+ venues | SRC-I-06 (LSEG) | exchange_market_data | 1 |
| Euronext non-display derived data policy: VWAP, indices, portfolio evaluation require non-display license | SRC-I-07 (Euronext Athens) | exchange_market_data | 2 |
| OpenFIGI: one FIGI per instrument per listing venue; entity layer required above FIGIs | SRC-G-01 (OpenFIGI) | identity_authority | 1 |
| Intrinio: security master architecture; internal entity ID as primary key; ticker not stable | SRC-G-02 (Intrinio) | identity_authority | 2 |

---

## 11. Boundary Confirmations

| Boundary | Status |
|----------|--------|
| No peer_group_registry.yaml | CONFIRMED |
| No final peer assignments | CONFIRMED |
| No canonical peer_group_id | CONFIRMED |
| No SAI mutation | CONFIRMED |
| No code | CONFIRMED |
| No market data integration | CONFIRMED |
| No real-time data consumed | CONFIRMED |
| No API keys or credentials requested | CONFIRMED |
| No vendor accounts created | CONFIRMED |
| No exchange connectivity | CONFIRMED |
| No broker/ATS connection | CONFIRMED |
| No quote polling or feed ingestion | CONFIRMED |
| No trading logic | CONFIRMED |
| Tasks 1–6 unchanged | CONFIRMED |
| Task 8 not started | CONFIRMED |
| Tactical Momentum spec not started | CONFIRMED |

---

## Artifact Status

```
PGMF_TASK_7_MARKET_DATA_READINESS_READY_FOR_HUMAN_REVIEW
```

---

*End of market data readiness specification.*
