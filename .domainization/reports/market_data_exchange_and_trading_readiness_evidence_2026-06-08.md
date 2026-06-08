# Market Data, Exchange, and Trading Readiness Evidence

**Artifact**: market_data_exchange_and_trading_readiness_evidence_2026-06-08.md
**Date**: 2026-06-08
**Branch**: spec/peer-group-methodology-source-screening
**Authority**: Research / Source Screening — Addendum
**Status**: evidence documentation only — NOT implementation, NOT trading enablement
**Purpose**: Dedicated evidence appendix for future market data, exchange connectivity, and trading readiness. This document is evidence-only and must not define final implementation.

**Boundary statement**: Market data and trading readiness evidence is included to prevent architectural drift. It does not authorize real-time market data consumption, broker integration, trading enablement, order-routing logic, or regulated activity. MoneyHorst is not a broker-dealer, investment firm, exchange participant, or regulated trading venue. All regulatory references are FUTURE_COMPLIANCE_REFERENCE only, not current legal obligations.

---

## Source Category I.A — Exchange Identification and Market Data Licensing

---

### SRC-I-01

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-01 |
| **institution** | ISO / SWIFT |
| **title** | ISO 10383 — Market Identifier Code (MIC) |
| **url** | https://www.iso10383.org / https://www.iso.org/standard/61067.html |
| **access_date** | 2026-06-08 |
| **source_type** | official_standard |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | MIC is the canonical ISO standard for uniquely identifying exchanges, trading platforms, and trade reporting facilities as sources of prices. Every exchange where MoneyHorst-covered assets trade has a four-character MIC. The `exchange_mic` registry field must store the MIC — not a free-text exchange name — to enable unambiguous venue identification. MIC is used in FIX protocol (FIX 4.3+), ISO 20022 messaging, and MiFID II reporting. |
| **Q1_Q10_mapping** | Q4 (ADR/cross-listing normalization — venue identification), Q8 (cross-region — venue-specific data source) |
| **extracted_principles** | (1) ISO 10383 specifies a universal method for identifying exchanges and trading venues as sources of prices and related information. (2) MIC is a four-character alphanumeric code. (3) SWIFT is the ISO 10383 Registration Authority. (4) Each venue has a distinct MIC: XETR (Xetra), XPAR (Euronext Paris), XAMS (Euronext Amsterdam), XNYS (NYSE), XNAS (Nasdaq). (5) A single economic entity may have listings on multiple MIC-identified venues. (6) Included in FIX 4.3+ and ISO 20022 for automated processing. |
| **future_fields_impacted** | exchange_mic, venue_code, primary_listing, listing_exchange, market_data_source |
| **scope_classification** | CURRENT_SCOPE — exchange_mic is a registry design field needed now for correct cross-listed security identification |
| **limitations** | MIC identifies the venue, not the economic entity. canonical_entity_id layer is still required above MIC. |
| **licensing_or_access_notes** | ISO standard. MIC list publicly accessible via iso10383.org. |
| **can_be_cited_in_methodology** | Yes — as canonical venue identification standard |
| **rule_type** | hard_rule — exchange_mic (ISO 10383) required for all listing records |

---

### SRC-I-02

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-02 |
| **institution** | Euronext |
| **title** | Euronext Market Data Pricing Policies and Real-Time Data Contracts |
| **url** | https://www.euronext.com/en/data/pricing-specs-agreements/market-data-pricing-policies |
| **access_date** | 2026-06-08 |
| **source_type** | methodology |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Euronext operates markets in Amsterdam (XAMS), Brussels (XBRU), Paris (XPAR), Lisbon (XLIS), Milan (XMIL), Oslo (XOSL), and Dublin (XDUB). Relevant for ASML, ADYEN, and other European peers. Euronext distinguishes: display usage (showing quotes to users), non-display usage (algorithmic or derived data including indices, VWAP, portfolio evaluation, analytics), real-time vs. delayed, and internal use vs. redistribution. These distinctions determine the licensing fields that must exist in the data model. |
| **Q1_Q10_mapping** | Q4 (cross-listing: XAMS for ASML, ADYEN), Q8 (cross-region: EU market data licensing framework) |
| **extracted_principles** | (1) Real-time market data requires a data agreement with Euronext or an authorized vendor. (2) Non-display usage — derived data, indices, VWAP, portfolio evaluation, analytic reference figures computed from real-time data — requires a separate non-display license. (3) Redistribution of Euronext data to third parties requires separate redistribution authorization. (4) Delayed data (typically 15 minutes) may be available without real-time entitlement. (5) User entitlement counting — professional users consuming real-time data are subject to audit reporting. (6) Index data licensing is separate from quote data licensing. |
| **future_fields_impacted** | realtime_entitlement_required, delayed_data_allowed, display_usage_allowed, non_display_usage_allowed, redistribution_allowed, professional_user_flag, market_data_audit_required, index_license_required, data_latency_class, derived_data_policy |
| **scope_classification** | CURRENT_SCOPE_FOR_DATA_MODEL — fields must be reserved; FUTURE_SCOPE_FOR_VENDOR_INTEGRATION — actual data agreement is a future commercial step |
| **limitations** | Full fee schedules require commercial engagement. Principle structure is consistent across exchanges. |
| **licensing_or_access_notes** | Euronext copyright. Policy framework publicly accessible. Non-display and redistribution agreements require commercial engagement. |
| **can_be_cited_in_methodology** | Yes — as primary source for display/non-display distinction |
| **rule_type** | hard_rule — display vs. non-display distinction must be modeled in data layer |

---

### SRC-I-03

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-03 |
| **institution** | Deutsche Börse / Xetra |
| **title** | Deutsche Börse Cash Market — Market Data Services and Xetra Trading |
| **url** | https://www.deutsche-boerse-cash-market.com / https://live.deutsche-boerse.com/en/xetra |
| **access_date** | 2026-06-08 |
| **source_type** | methodology |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Xetra (MIC: XETR) is the primary electronic trading venue for German-listed equities including Rheinmetall, Siemens, Deutsche Bank, and other PGF-06/PGF-07/PGF-08 European peers. Deutsche Börse Group operates Xetra, Eurex (derivatives), and Clearstream (settlement) as vertically integrated market infrastructure, managing MiFIR data products centrally. |
| **Q1_Q10_mapping** | Q4 (cross-listing normalization — XETR for German peers), Q8 (cross-region — EUR-denominated, CET timezone) |
| **extracted_principles** | (1) Xetra regular trading: 09:00–17:30 CET (continuous trading) with extended hours under development. (2) Deutsche Börse Group manages MiFIR data products centrally for Xetra, Eurex, and EEX. (3) Market data licensing follows a MiFIR-compliant framework. (4) MIC code XETR is the canonical identifier for the Xetra electronic trading system; XFRA is the Frankfurt floor venue — distinct from Xetra. (5) Trading calendar: German national and Hesse state holidays apply. |
| **future_fields_impacted** | exchange_mic (XETR), trading_calendar_id, exchange_timezone, market_session_status, continuous_trading_hours, stale_quote_threshold, market_data_source |
| **scope_classification** | CURRENT_SCOPE — XETR MIC and CET timezone are current registry fields; FUTURE_SCOPE_FOR_VENDOR_INTEGRATION for data agreement |
| **limitations** | Specific fee schedules require commercial engagement. Technical documentation available via Deutsche Börse Data Services. |
| **licensing_or_access_notes** | Deutsche Börse copyright. MIC codes publicly available. |
| **can_be_cited_in_methodology** | Yes |
| **rule_type** | hard_rule — XETR MIC and CET timezone required for German-listed peers |

---

### SRC-I-04

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-04 |
| **institution** | NasdaqTrader.com |
| **title** | Nasdaq Global Data — Market Data Product Matrix and Data Policies |
| **url** | http://www.nasdaqtrader.com |
| **access_date** | 2026-06-08 |
| **source_type** | methodology |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Nasdaq (MIC: XNAS) is the primary listing venue for NVDA, AMD, ASML-ADR, CRWD, PANW, and many other MoneyHorst assets. Nasdaq's data policies distinguish professional vs. non-professional users for fee purposes, display vs. non-display usage, and index data licensing from quote data licensing. Nasdaq's near-24-hour trading model (Day Session 04:00–20:00 ET, Night Session 21:00–04:00 ET) has implications for session-aware staleness calculations. |
| **Q1_Q10_mapping** | Q4 (primary listing for US-listed assets and ADRs), Q6 (liquidity data depends on licensed feed quality) |
| **extracted_principles** | (1) Nasdaq distinguishes professional and non-professional user categories for data licensing — professional users pay materially more for real-time data. (2) Display and non-display usage are licensed separately. (3) Index data (Nasdaq-100, sector indices) requires a separate index data license from quote data. (4) Nasdaq has an SEC-approved near-23/24-hour trading model with Day and Night Sessions — this changes staleness threshold and quote timestamp logic for Nasdaq-listed assets. |
| **future_fields_impacted** | professional_user_flag, display_usage_allowed, non_display_usage_allowed, index_license_required, quote_timestamp_required, trading_calendar_id, market_session_status, after_hours_supported |
| **scope_classification** | CURRENT_SCOPE_FOR_DATA_MODEL for professional_user_flag and display/non-display; FUTURE_SCOPE for data subscription |
| **limitations** | Specific fee schedules subject to change. Extended trading hours model is recent. |
| **licensing_or_access_notes** | Nasdaq copyright. Policy framework publicly available via NasdaqTrader.com. |
| **can_be_cited_in_methodology** | Yes |
| **rule_type** | hard_rule — professional_user_flag required; index and quote data must be licensed separately |

---

### SRC-I-05

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-05 |
| **institution** | NYSE Group / ICE |
| **title** | NYSE Market Data and Trading Venue Overview |
| **url** | https://www.nyse.com/equities |
| **access_date** | 2026-06-08 |
| **source_type** | methodology |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | NYSE (MIC: XNYS) is a primary or secondary listing venue for JPM, BAC, C, WFC, GS, MS, V, MA, AXP, and many other MoneyHorst assets in PGF-03 and PGF-08. NYSE Group operates five equity markets under NYSE Pillar (NYSE, NYSE Arca, NYSE American, NYSE Chicago, NYSE National), each with a distinct MIC. Market data redistribution requires authorization. NYSE Regulation governs corporate actions relevant to corporate_action_source. |
| **Q1_Q10_mapping** | Q4 (primary listing for NYSE-listed assets), Q6 (liquidity and real-time data quality) |
| **extracted_principles** | (1) NYSE Group operates five distinct equity markets each with its own MIC under one technology platform. (2) Real-time vs. delayed data is a product choice with licensing implications. (3) Market data redistribution to third parties is restricted without authorization. (4) NYSE Regulation governs corporate actions (mergers, spinoffs, stock splits) — relevant to corporate_action_source field. |
| **future_fields_impacted** | exchange_mic (XNYS, ARCX, etc.), market_data_source, realtime_entitlement_required, redistribution_allowed, corporate_action_source |
| **scope_classification** | CURRENT_SCOPE — correct MIC per NYSE Group venue; FUTURE_SCOPE for data agreements |
| **limitations** | Multiple MICs within NYSE Group — selection of correct MIC is required per listing. |
| **licensing_or_access_notes** | NYSE Group copyright. MIC codes publicly available. |
| **can_be_cited_in_methodology** | Yes |
| **rule_type** | hard_rule — correct NYSE Group MIC must be stored per listing |

---

### SRC-I-06

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-06 |
| **institution** | LSEG Data and Analytics |
| **title** | LSEG Real-Time Managed Distribution Service |
| **url** | https://www.lseg.com/en/data-analytics/market-data/data-management/real-time-managed-distribution-service |
| **access_date** | 2026-06-08 |
| **source_type** | institutional_research |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | LSEG (formerly Refinitiv) is one of the two dominant global real-time market data vendors alongside Bloomberg. LSEG aggregates data from 550+ global venues. This confirms that the data model must separate market_data_source (exchange origin) from data_vendor (aggregator/distributor). Institutional real-time data infrastructure requires entitlement controls and audit capability as regulatory requirements. |
| **Q1_Q10_mapping** | Q4 (multi-venue aggregation), Q8 (cross-region data distribution) |
| **extracted_principles** | (1) Enterprise real-time data distribution requires entitlement and permissioning controls. (2) Data governance must include audit and access control layers. (3) A single data vendor aggregates from hundreds of global venues — market_data_source (exchange) and data_vendor (aggregator) are distinct fields. (4) Real-time data infrastructure must meet rising regulatory compliance requirements. |
| **future_fields_impacted** | data_vendor, market_data_source, realtime_entitlement_required, market_data_audit_required, data_confidence_tier |
| **scope_classification** | CURRENT_SCOPE_FOR_DATA_MODEL — market_data_source vs. data_vendor distinction must be in data model; FUTURE_SCOPE for vendor integration |
| **limitations** | Commercial pricing requires engagement. Competes with Bloomberg and other vendors. |
| **licensing_or_access_notes** | LSEG copyright. Service overview publicly accessible. |
| **can_be_cited_in_methodology** | Yes — confirms market_data_source vs. data_vendor field distinction |
| **rule_type** | hard_rule — market_data_source and data_vendor are separate fields |

---

### SRC-I-07

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-07 |
| **institution** | Euronext (Athens venue — illustrative policy) |
| **title** | Vendors — Non-Display Usage Policy |
| **url** | https://athens.euronext.com/en/more-options/announcements/vendors-non-display |
| **access_date** | 2026-06-08 |
| **source_type** | methodology |
| **authority_tier** | Tier 2 |
| **MoneyHorst_use_case** | Confirms that non-display usage of real-time data — including indices, VWAP calculations, portfolio evaluation services, and any analytic reference figure calculated from real-time data — requires a non-display license. Directly applicable: any computed peer-relative analytics derived from real-time exchange data are non-display derived data and require appropriate licensing. |
| **Q1_Q10_mapping** | Q4, Q8 |
| **extracted_principles** | (1) Non-display usage is broadly defined: indices, VWAP, portfolio evaluation, analytics calculated from real-time data. (2) Non-display license required regardless of whether underlying data is displayed to users. (3) Consistent with Euronext group policy across venues. |
| **future_fields_impacted** | non_display_usage_allowed, derived_data_policy, index_license_required, market_data_audit_required |
| **scope_classification** | CURRENT_SCOPE_FOR_DATA_MODEL — derived_data_policy field must be reserved; FUTURE_SCOPE for vendor integration |
| **limitations** | Greece-specific Euronext entity. Principle is consistent with group policy. |
| **licensing_or_access_notes** | Euronext copyright. Publicly accessible. |
| **can_be_cited_in_methodology** | Yes — illustrative example of non-display derived data policy |
| **rule_type** | hard_rule — derived data usage requires explicit license; tracked in derived_data_policy |

---

## Source Category I.B — Best Execution and Order Routing Governance

---

### SRC-I-08

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-08 |
| **institution** | ESMA |
| **title** | MiFID II Article 27 — Obligation to Execute Orders on Most Favourable Terms |
| **url** | https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifid-ii/article-27-obligation-execute-orders |
| **access_date** | 2026-06-08 |
| **source_type** | official_standard |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | MiFID II Article 27 establishes the EU regulatory framework for best execution obligations: price, costs, speed, likelihood of execution and settlement, size, nature, and other relevant considerations. For MoneyHorst future trading readiness, these factors define the fields that must exist in an execution venue selection policy. Currently FUTURE_COMPLIANCE_REFERENCE — MoneyHorst is not a regulated investment firm. |
| **Q1_Q10_mapping** | Q4 (venue accessibility), Q6 (liquidity — likelihood of execution), Q8 (cross-region — EU venue obligations), Q9 (governance — annual execution policy review) |
| **extracted_principles** | (1) Best execution is multi-factor: price, costs, speed, likelihood of execution and settlement, size, nature, and other considerations. (2) Firms must maintain an order execution policy listing venues and the factors influencing venue selection. (3) The execution policy must be reviewed at least annually and when material changes occur. (4) Firms must demonstrate best execution was achieved. (5) MiFID II review (2024) has removed RTS 28 annual venue reporting obligation — ESMA statement February 2024. |
| **future_fields_impacted** | execution_venue_eligible, execution_venue_preference, best_execution_required, order_routing_policy_required, execution_quality_review_required, venue_accessibility_status, settlement_risk_flag, liquidity_review_frequency |
| **scope_classification** | FUTURE_SCOPE_TRADING_GOVERNANCE — applies only when MoneyHorst becomes a regulated EU investment firm; not current obligation |
| **limitations** | Applies to regulated investment firms in EU/EEA. MoneyHorst is not a regulated investment firm. |
| **licensing_or_access_notes** | EU legislative text. Publicly accessible via EUR-Lex and ESMA interactive rulebook. |
| **can_be_cited_in_methodology** | Yes — as FUTURE_COMPLIANCE_REFERENCE for EU trading governance |
| **rule_type** | future_compliance_reference |

---

### SRC-I-09

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-09 |
| **institution** | FINRA |
| **title** | FINRA Rule 5310 — Best Execution and Interpositioning |
| **url** | https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310 |
| **access_date** | 2026-06-08 |
| **source_type** | official_standard |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | FINRA Rule 5310 is the US regulatory source for best execution obligations for FINRA member broker-dealers. It requires reasonable diligence to ascertain the best market and execute to provide the most favorable price reasonably available. Covers equities, options, debt, and foreign securities. Best execution factors: market character, size and type of transaction, number of markets checked, accessibility of quotation, customer instructions. Currently FUTURE_COMPLIANCE_REFERENCE only. |
| **Q1_Q10_mapping** | Q4 (venue accessibility — foreign securities), Q6 (market character, liquidity), Q8 (cross-region — foreign security handling) |
| **extracted_principles** | (1) Reasonable diligence to find the most favorable market under current conditions. (2) Factors: market character (liquidity, depth, volatility), size and type of transaction, number of markets checked, accessibility of the quotation, customer instructions. (3) Applies to foreign securities — requires special handling for thinly traded or less accessible foreign listings. (4) Annual review of best execution practices is expected. |
| **future_fields_impacted** | foreign_security_execution_policy_required, execution_venue_eligibility, market_access_controls_required, venue_accessibility_status, quote_venue, primary_execution_venue, liquidity_review_frequency |
| **scope_classification** | FUTURE_SCOPE_TRADING_GOVERNANCE — FINRA member firm obligation; not current |
| **limitations** | Applies to FINRA member broker-dealers. MoneyHorst is not a broker-dealer. |
| **licensing_or_access_notes** | FINRA copyright. Rule text publicly accessible. |
| **can_be_cited_in_methodology** | Yes — as FUTURE_COMPLIANCE_REFERENCE for US trading governance |
| **rule_type** | future_compliance_reference |

---

## Source Category I.C — Pre-Trade Risk Controls and Market Access

---

### SRC-I-10

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-10 |
| **institution** | SEC |
| **title** | SEC Rule 15c3-5 — Risk Management Controls for Brokers or Dealers with Market Access |
| **url** | https://www.sec.gov/rules/final/2010/34-63241-secg.htm |
| **access_date** | 2026-06-08 |
| **source_type** | official_standard |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | SEC Rule 15c3-5 requires broker-dealers with market access to establish, document, and maintain a system of risk management controls. These controls define the field vocabulary for the tradability and risk layer of any future MoneyHorst asset registry. The rule's pre-trade and post-trade control vocabulary is the canonical US reference for this layer. Currently FUTURE_COMPLIANCE_REFERENCE only. |
| **Q1_Q10_mapping** | Q6 (liquidity/price collars, max order value), Q8 (cross-region — restricted securities), Q9 (governance — annual review, documentation) |
| **extracted_principles** | (1) Pre-trade controls must include: price collars, maximum order value, maximum order volume, message throttles. (2) Must prevent orders for securities the firm or customer is restricted from trading. (3) Must restrict market access technology to authorized persons. (4) Post-trade execution reports must flow immediately to surveillance personnel. (5) Controls must be documented, reviewed regularly, and promptly remediated. (6) Kill switch / cancel-all functionality is a standard requirement. (7) Audit trail and electronic logs are required. (8) Annual review and certification of the risk management system is required. |
| **future_fields_impacted** | pre_trade_controls_required, max_order_value_policy, max_order_volume_policy, price_collar_policy, message_throttle_policy, kill_switch_required, real_time_monitoring_required, post_trade_control_required, audit_log_required, surveillance_required, restricted_security_flag, tradability_status, market_access_controls_required |
| **scope_classification** | FUTURE_SCOPE_TRADING_GOVERNANCE — broker-dealer obligation; not current; all fields reserved for future compliance readiness |
| **limitations** | Applies to SEC-registered broker-dealers. MoneyHorst is not a broker-dealer. |
| **licensing_or_access_notes** | SEC public law. Publicly accessible via SEC.gov and eCFR. |
| **can_be_cited_in_methodology** | Yes — as FUTURE_COMPLIANCE_REFERENCE for US pre-trade control governance |
| **rule_type** | future_compliance_reference — field vocabulary is current-scope; obligation is future-scope |

---

### SRC-I-11

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-11 |
| **institution** | ESMA |
| **title** | MiFID II RTS 6 — Algorithmic Trading: Pre-Trade Controls, Kill Switch, Annual Review |
| **url** | https://www.jdsupra.com/legalnews/esma-announces-intention-to-publish-8540677 |
| **access_date** | 2026-06-08 |
| **source_type** | official_standard |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | MiFID II RTS 6 governs algorithmic trading requirements for EU investment firms: pre-trade controls, system resilience, kill switch, testing before deployment, annual certification, and market abuse monitoring. FCA multi-firm review of RTS 6 compliance identified common weaknesses in pre-trade controls and kill-switch documentation. Defines the EU-specific field vocabulary for the trading governance layer. Currently FUTURE_COMPLIANCE_REFERENCE only. |
| **Q1_Q10_mapping** | Q6 (pre-trade controls affect tradable instrument scope), Q9 (governance — annual review, documentation) |
| **extracted_principles** | (1) Algorithmic trading systems must be resilient, have capacity, and be subject to trading thresholds and limits. (2) Pre-trade controls must prevent incorrect orders from reaching the market. (3) Kill switch must allow immediate cancellation of all active orders. (4) Systems must be tested before deployment and after significant changes. (5) Annual review and certification required. (6) Market abuse monitoring must be embedded. (7) ESMA has announced new guidance on algorithmic pre-trade controls (2026) as part of MiFID II review. |
| **future_fields_impacted** | kill_switch_required, pre_trade_controls_required, algo_trading_flag, audit_log_required, surveillance_required, market_abuse_monitoring_required, business_continuity_required, trading_enabled, tradability_status |
| **scope_classification** | FUTURE_SCOPE_TRADING_GOVERNANCE — EU regulated firm obligation; not current |
| **limitations** | Applies to EU-regulated investment firms and algorithmic traders under MiFID II. FCA applies UK MiFID equivalent post-Brexit. |
| **licensing_or_access_notes** | ESMA / EU legislative text. Publicly accessible. |
| **can_be_cited_in_methodology** | Yes — as FUTURE_COMPLIANCE_REFERENCE for EU algorithmic trading governance |
| **rule_type** | future_compliance_reference |

---

## Source Category I.D — Trading Calendars and Session Awareness

---

### SRC-I-12

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-12 |
| **institution** | Deutsche Börse (live.deutsche-boerse.com) |
| **title** | Xetra Trading Calendar and Market Hours |
| **url** | https://live.deutsche-boerse.com/en/handeln/trading-calendar |
| **access_date** | 2026-06-08 |
| **source_type** | methodology |
| **authority_tier** | Tier 1 |
| **MoneyHorst_use_case** | Xetra (XETR) trading hours are 09:00–17:30 CET (regular continuous trading), with extended hours in development (08:00–22:00 CET). Frankfurt floor (XFRA) has partially different hours. German national and Hesse state holidays apply. Quote timestamps for XETR-listed assets must use CET/CEST. Delayed data calculations must account for session boundaries and the Xetra calendar. |
| **Q1_Q10_mapping** | Q4 (cross-listing: timezone alignment XETR vs. XNAS/XNYS), Q8 (cross-region: timestamp normalization) |
| **extracted_principles** | (1) Xetra regular hours: 09:00–17:30 CET. (2) Timezone: CET (UTC+1) / CEST (UTC+2 summer). (3) Auction phases: opening auction, intraday auctions, closing auction — timing must be recorded for price reference purposes. (4) Trading calendar: German/Hesse holiday schedule — specific non-trading dates must be tracked. (5) Delayed data calculations must reference last Xetra trading timestamp within session boundaries. |
| **future_fields_impacted** | trading_calendar_id, exchange_timezone, market_session_status, continuous_trading_hours, auction_phase_flag, holiday_calendar_source, stale_quote_threshold, timestamp_normalization_rules |
| **scope_classification** | CURRENT_SCOPE — timezone and session metadata needed for quote staleness calculation |
| **limitations** | Extended hours rollout is in progress; canonical hours are 09:00–17:30. Calendar must be maintained annually. |
| **licensing_or_access_notes** | Deutsche Börse publicly provides trading calendar. |
| **can_be_cited_in_methodology** | Yes |
| **rule_type** | hard_rule — exchange_timezone (CET/CEST) and trading_calendar_id required for XETR-listed assets |

---

### SRC-I-13

| Field | Value |
|-------|-------|
| **source_id** | SRC-I-13 |
| **institution** | JD Supra / Nasdaq regulatory filing |
| **title** | Nasdaq 23-Hour Equity Trading — SEC-Approved Extended Session Structure |
| **url** | https://www.jdsupra.com/legalnews/nasdaq-23-hour-equity-trading-proposal-4044543 |
| **access_date** | 2026-06-08 |
| **source_type** | institutional_research |
| **authority_tier** | Tier 2 |
| **MoneyHorst_use_case** | Nasdaq has SEC approval for a near-24-hour trading model: Day Session (04:00–20:00 ET) and Night Session (21:00–04:00 ET next day), with a one-hour gap for systems maintenance and corporate action processing. Relevant for quote timestamp normalization, stale_quote_threshold, and market_session_status for Nasdaq-listed assets. The maintenance gap for corporate actions is relevant to corporate_action_source. |
| **Q1_Q10_mapping** | Q4 (quote timestamp normalization for XNAS), Q6 (liquidity: extended hours may have different depth) |
| **extracted_principles** | (1) Nasdaq Day Session: 04:00–20:00 ET. (2) Night Session: 21:00–04:00 ET next day (Sunday–Thursday nights). (3) One-hour maintenance gap: 20:00–21:00 ET for systems maintenance and corporate action processing. (4) Extended hours may have different liquidity and spread characteristics. |
| **future_fields_impacted** | trading_calendar_id, market_session_status, pre_market_supported, after_hours_supported, stale_quote_threshold, corporate_action_source, timestamp_normalization_rules |
| **scope_classification** | CURRENT_SCOPE — session structure affects quote staleness and market_session_status field |
| **limitations** | Tier 2 — legal/regulatory news coverage. Session structure may evolve further. |
| **licensing_or_access_notes** | JD Supra legal news. Publicly accessible. |
| **can_be_cited_in_methodology** | Yes — as supplementary reference for Nasdaq session structure |
| **rule_type** | soft_context — session structure is evolving; field design must accommodate multi-session markets |

---

## Source Category I Summary

| source_id | Institution | Subcategory | Authority | Q-Mapping | Rule Type | Scope |
|-----------|-------------|------------|-----------|-----------|-----------|-------|
| SRC-I-01 | ISO / SWIFT | Exchange ID | Tier 1 | Q4, Q8 | hard_rule | CURRENT_SCOPE |
| SRC-I-02 | Euronext | Data Licensing | Tier 1 | Q4, Q8 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-03 | Deutsche Börse | Data Licensing | Tier 1 | Q4, Q8 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-04 | NasdaqTrader | Data Licensing | Tier 1 | Q4, Q6 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-05 | NYSE Group | Data Licensing | Tier 1 | Q4, Q6 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-06 | LSEG Data | Data Vendor | Tier 1 | Q4, Q8 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-07 | Euronext Athens | Non-Display Policy | Tier 2 | Q4, Q8 | hard_rule | CURRENT_MODEL / FUTURE_INTEGRATION |
| SRC-I-08 | ESMA | Best Execution | Tier 1 | Q4, Q6, Q8, Q9 | future_compliance | FUTURE_TRADING_GOVERNANCE |
| SRC-I-09 | FINRA | Best Execution | Tier 1 | Q4, Q6, Q8 | future_compliance | FUTURE_TRADING_GOVERNANCE |
| SRC-I-10 | SEC | Pre-Trade Controls | Tier 1 | Q6, Q8, Q9 | future_compliance | FUTURE_TRADING_GOVERNANCE |
| SRC-I-11 | ESMA | Algo Trading | Tier 1 | Q6, Q9 | future_compliance | FUTURE_TRADING_GOVERNANCE |
| SRC-I-12 | Deutsche Börse | Trading Calendar | Tier 1 | Q4, Q8 | hard_rule | CURRENT_SCOPE |
| SRC-I-13 | Nasdaq / JD Supra | Trading Calendar | Tier 2 | Q4, Q6 | soft_context | CURRENT_SCOPE |

**Category I total sources**: 13
**Tier 1**: 11 | **Tier 2**: 2
**Hard rules (current or current model)**: 7
**Future compliance references**: 4 (SRC-I-08 through SRC-I-11)

---

## Future Fields Summary

### Fields Required NOW (current registry design)

| Field | Source | Rationale |
|-------|--------|-----------|
| `exchange_mic` | SRC-I-01 | ISO 10383 — canonical venue ID; required for all listing records |
| `market_data_source` | SRC-I-02/03/04/05 | Exchange origin, separate from data_vendor |
| `data_vendor` | SRC-I-06 | Aggregator/distributor, separate from market_data_source |
| `data_latency_class` | SRC-I-02/03/04 | real-time / delayed / end-of-day — declared per data feed |
| `trading_calendar_id` | SRC-I-12 | Required for quote staleness calculation |
| `exchange_timezone` | SRC-I-12 | CET/CEST for XETR; ET for XNAS/XNYS |
| `derived_data_policy` | SRC-I-07 | Whether analytics derived from this data require non-display license |

### Fields Reserved for Future Data Layer (model only, not implemented)

| Field | Source | When Needed |
|-------|--------|-------------|
| `realtime_entitlement_required` | SRC-I-02/03/04/05 | When real-time display is added |
| `delayed_data_allowed` | SRC-I-02 | When delayed display is configured |
| `display_usage_allowed` | SRC-I-02/03/04 | When data display feature is built |
| `non_display_usage_allowed` | SRC-I-02/07 | When derived analytics from licensed data are computed |
| `redistribution_allowed` | SRC-I-02/05 | When data is shared with third parties |
| `professional_user_flag` | SRC-I-04 | When professional vs. non-professional user distinction is needed |
| `index_license_required` | SRC-I-02/04 | When index data is separately consumed |
| `market_data_audit_required` | SRC-I-02 | When compliance reporting for data usage is required |
| `quote_timestamp_required` | SRC-I-04 | When any quote display is implemented |
| `bid_ask_source` | SRC-I-02/04/05 | When bid/ask spread display is implemented |
| `stale_quote_threshold` | SRC-I-12/13 | When quote freshness validation is required |
| `market_session_status` | SRC-I-12/13 | When session-aware data handling is implemented |
| `corporate_action_source` | SRC-I-05/13 | When corporate action adjustments are applied |

### Fields Reserved for Future Trading Governance (FUTURE_COMPLIANCE_REFERENCE)

| Field | Source | When Needed |
|-------|--------|-------------|
| `execution_venue_eligible` | SRC-I-08/09 | When order routing is implemented |
| `best_execution_required` | SRC-I-08/09 | When client order routing is implemented |
| `pre_trade_controls_required` | SRC-I-10/11 | When any electronic market access is implemented |
| `kill_switch_required` | SRC-I-10/11 | When algorithmic or automated trading is implemented |
| `audit_log_required` | SRC-I-10/11 | When any regulated activity begins |
| `tradability_status` | SRC-I-10/11 | When asset-level trading enablement is introduced |
| `restricted_security_flag` | SRC-I-10 | When restricted security lists are maintained |
| `surveillance_required` | SRC-I-10/11 | When market access or trading is implemented |
| `market_abuse_monitoring_required` | SRC-I-11 | When algorithmic trading is implemented |
| `price_collar_policy` | SRC-I-10 | When pre-trade risk controls are implemented |
| `max_order_value_policy` | SRC-I-10 | When pre-trade risk controls are implemented |
| `kill_switch_required` | SRC-I-10/11 | When any automated trading is implemented |
| `algo_trading_flag` | SRC-I-11 | When algorithmic strategies are deployed |
| `manual_trade_only_flag` | SRC-I-10/11 | When certain instruments require manual-only execution |

---

*End of market data, exchange, and trading readiness evidence document. Content was rephrased for compliance with licensing restrictions.*

*Market data and trading readiness evidence is included to prevent architectural drift. It does not authorize real-time market data consumption, broker integration, trading enablement, order-routing logic, or regulated activity.*
