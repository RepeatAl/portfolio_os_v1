# Peer Group Registry Methodology Framework — Trading Governance Boundary Specification

**Artifact**: trading_governance_boundary_2026-06-08.md
**Task**: Task 8 — Create Trading Governance Boundary Specification
**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: PGMF_TASK_8_TRADING_GOVERNANCE_BOUNDARY_READY_FOR_HUMAN_REVIEW

**Purpose**: Defines the trading governance boundary. All trading-related fields are FUTURE_COMPLIANCE_REFERENCE vocabulary reserved to prevent architectural drift. No trading functionality is created, implied, or enabled.

**Boundary statement**: Trading governance evidence is included to prevent architectural drift. It does not authorize broker integration, exchange connectivity, order routing, execution logic, market access, trading enablement, or regulated activity.

**Hard boundaries**: No peer_group_registry.yaml. No final peer assignments. No canonical peer_group_id. No SAI mutation. No code. No market data integration. No broker/exchange/ATS. No trading logic. No API keys. No credentials. No vendor accounts.

Source authority (future_trading_reference domain): SRC-I-08 (ESMA MiFID II Art.27), SRC-I-09 (FINRA Rule 5310), SRC-I-10 (SEC Rule 15c3-5), SRC-I-11 (ESMA MiFID II RTS 6).


---

## 1. MoneyHorst Regulatory Status

**MoneyHorst is NOT:**
- A broker-dealer (US SEC/FINRA definition)
- An investment firm (EU MiFID II definition)
- An exchange participant or exchange member
- An alternative trading system (ATS)
- A systematic internaliser (EU MiFID II definition)
- A trading venue (EU MiFIR definition)
- An order-routing system
- A market maker
- A regulated entity under any securities supervision authority

**MoneyHorst IS:**
- A signal-driven PM reasoning system
- A portfolio intelligence assistant
- An explainable portfolio interpretation engine
- A methodology and governance framework for peer group analysis

No field, document, or vocabulary in this specification creates regulated-entity status, compliance obligations, broker-dealer activity, investment-firm activity, exchange participation, order routing, market access, or trading enablement.

---

## 2. FUTURE_COMPLIANCE_REFERENCE Fields

All 17 fields below are reserved in methodology vocabulary only. They are:
- NOT in the v1 registry schema
- NOT populated
- NOT operational
- NOT creating any current legal obligation

Their purpose is solely to prevent architectural drift: if these fields are not identified now, they will be added ad-hoc later and may conflate with data model or methodology fields.

| Field | Type | Regulatory Source | Activation Condition |
|-------|------|------------------|---------------------|
| `tradability_status` | enum (tradable/restricted/blocked/unknown) | SRC-I-10/11 (SEC 15c3-5, MiFID II RTS 6) | Asset-level trading enablement implemented |
| `trading_enabled` | boolean | SRC-I-10/11 | Trading system implemented and activated |
| `trade_block_reason` | string | SRC-I-10 (SEC 15c3-5) | Restricted security list maintained |
| `execution_venue_eligible` | boolean | SRC-I-08 (MiFID II Art.27) | EU order routing implemented |
| `best_execution_required` | boolean | SRC-I-08/09 (MiFID II Art.27, FINRA 5310) | Client order routing implemented |
| `order_routing_policy_required` | boolean | SRC-I-08/09 | Order routing implemented |
| `pre_trade_controls_required` | boolean | SRC-I-10/11 (SEC 15c3-5, MiFID II RTS 6) | Electronic market access implemented |
| `price_collar_policy` | string | SRC-I-10 (SEC 15c3-5) | Pre-trade risk controls implemented |
| `max_order_value_policy` | string | SRC-I-10 (SEC 15c3-5) | Pre-trade risk controls implemented |
| `max_order_volume_policy` | string | SRC-I-10 (SEC 15c3-5) | Pre-trade risk controls implemented |
| `message_throttle_policy` | string | SRC-I-10/11 | Message rate controls implemented |
| `kill_switch_required` | boolean | SRC-I-10/11 (SEC 15c3-5, MiFID II RTS 6) | Automated/algorithmic trading implemented |
| `audit_log_required` | boolean | SRC-I-10/11 | Any regulated activity commenced |
| `surveillance_required` | boolean | SRC-I-10/11 | Market access implemented |
| `market_abuse_monitoring_required` | boolean | SRC-I-11 (MiFID II RTS 6) | Algorithmic trading implemented |
| `algo_trading_flag` | boolean | SRC-I-11 (MiFID II RTS 6) | Algorithmic strategies deployed |
| `manual_trade_only_flag` | boolean | SRC-I-10/11 | Manual-only execution enforcement required |

---

## 3. Scope Separation

The following concerns must remain architecturally separate. Conflation of any two creates drift toward unintended regulated activity.

| Concern | Fields / Layer | Status | Description |
|---------|---------------|--------|-------------|
| **Quote source eligibility** | exchange_mic, market_data_source, data_vendor, data_latency_class | CURRENT_MODEL_NULLABLE (Task 7) | Which venues and vendors can provide market data. Does NOT imply tradability. |
| **Market data readiness** | exchange_timezone, trading_calendar_id, derived_data_policy, index_license_required | CURRENT_MODEL_NULLABLE (Task 7) | Whether infrastructure exists to receive and interpret market data. Does NOT authorize data consumption. |
| **Trading eligibility** | tradability_status, trading_enabled, trade_block_reason | FUTURE_COMPLIANCE_REFERENCE | Whether an asset MAY be traded. Requires regulated-entity status. |
| **Execution venue eligibility** | execution_venue_eligible, best_execution_required, order_routing_policy_required | FUTURE_COMPLIANCE_REFERENCE | Where an order MAY be routed. Requires broker/exchange relationship. |
| **Broker connectivity** | (not modeled — entirely outside this framework) | NOT IN SCOPE | Actual connection to a broker/dealer. Requires commercial and regulatory agreements. |
| **Order-routing authority** | pre_trade_controls_required, price_collar_policy, kill_switch_required | FUTURE_COMPLIANCE_REFERENCE | How orders are risk-controlled before reaching a venue. Requires compliance infrastructure. |

**Critical rule**: The existence of CURRENT_MODEL_NULLABLE market data fields (even when populated in future) does NOT create trading eligibility. An asset with a populated exchange_mic and data_latency_class is NOT thereby tradable. Trading eligibility requires the FUTURE_COMPLIANCE_REFERENCE fields AND the three-gate activation model.

---

## 4. Three-Gate Future Activation Model

No trading governance field may become operational without passing through ALL three gates in sequence:

```
Gate 1: Regulatory Status Gate
    MoneyHorst must become a regulated entity
    (broker-dealer, investment firm, or exchange participant)
    before any trading governance field can carry a real obligation.
        ↓
Gate 2: Compliance Readiness Gate
    The applicable regulatory framework must be identified per asset/venue:
    - US assets: SEC Rule 15c3-5 + FINRA Rule 5310
    - EU assets: MiFID II Article 27 + RTS 6
    - UK assets: FCA MiFID equivalent
    - DE assets: BaFin interpretation of MiFID II
    Compliance documentation, legal review, and regulator notification
    must be complete before fields become operational.
        ↓
Gate 3: Implementation Gate
    Trading system, pre-trade controls, order routing infrastructure,
    kill switch, audit trail, surveillance systems, and market abuse
    monitoring must be built, tested, and certified before fields
    become operationally active.
```

ALL three gates must pass. No gate may be skipped. Partial gate completion does not authorize partial field activation.

---

## 5. What May Be Done Now (v1)

- **RESERVE** the field names and types in the future trading governance vocabulary (this document)
- **DOCUMENT** the regulatory source for each field (for future compliance planning)
- **DESCRIBE** the activation condition for each field (what must be true before it becomes operational)
- **SEPARATE** trading governance from market data readiness and peer comparison methodology

---

## 6. What Must NOT Be Done Now

| Prohibited Action | Reason |
|-------------------|--------|
| Populate any trading governance field | Fields are not in v1 schema; no regulatory basis |
| Build order routing logic | MoneyHorst is not a regulated order-routing entity |
| Build execution logic | MoneyHorst does not execute trades |
| Connect to any broker or exchange | No commercial or regulatory agreements exist |
| Build pre-trade risk controls runtime | No trading system exists to control |
| Build kill switch runtime | No automated trading exists to interrupt |
| Build surveillance runtime | No market access exists to monitor |
| Build market abuse monitoring | No trading activity exists to surveil |
| Claim regulatory compliance | No regulated-entity status exists |
| Imply trading capability in any output | MoneyHorst produces reasoning packages, not orders |
| Create a broker abstraction layer | No broker relationship exists |
| Create a market access controls runtime | No market access exists |
| Use trading governance vocabulary to describe current capabilities | These fields describe a future state that does not exist |

---

## 7. SAI-BLK-21 Behavior

### 7.1 Must NOT Infer Tradability from Market Data Fields

SAI-BLK-21 must NEVER conclude that an asset is "tradable" or "execution-ready" based on:
- The presence of exchange_mic (this identifies a listing venue, not trading eligibility)
- The presence of data_latency_class (this describes data freshness, not order-routing readiness)
- The presence of market_data_source or data_vendor (these describe data delivery, not execution access)

### 7.2 Must NOT Suggest Execution Eligibility

SAI-BLK-21 outputs must NEVER contain:
- "This asset is tradable on XETR"
- "Execution venue: XNAS"
- "Order routing available via..."
- "Trading enabled"
- Any language implying that MoneyHorst can execute, route, or facilitate an order

### 7.3 Must Surface Trading Fields as Future-Only if Referenced

If any SAI output or downstream consumer references a trading governance field:
- The field must be clearly labeled FUTURE_COMPLIANCE_REFERENCE
- The output must state: "Trading governance field — not operational; future compliance reference only"
- No implication of current capability may be created

### 7.4 Must Block Peer Methodology Output from Implying Orderability

Peer comparison outputs (core_peer_set, adjacent_peer_set, benchmark_context_set) describe analytical peer relationships. They must NEVER be interpreted as:
- "These are assets you can trade against each other"
- "This peer is available for pair trading"
- "Order this asset alongside its peers"

Peer methodology output is for diagnostic interpretation only (SAI-BLK-21 → Peer Comparison diagnostic). It is never an execution instruction.

---

## 8. Regulatory Source Authority

All sources in this section are `future_trading_reference` domain. They are Tier 1 institutional sources used ONLY to reserve vocabulary. They do NOT create current obligations.

### 8.1 SEC Rule 15c3-5 — Market Access Rule (SRC-I-10)

**What it governs**: US broker-dealers with market access must establish, document, and maintain risk management controls.

**Vocabulary reserved from this source**: pre_trade_controls_required, price_collar_policy, max_order_value_policy, max_order_volume_policy, message_throttle_policy, kill_switch_required, audit_log_required, surveillance_required, trade_block_reason, tradability_status, trading_enabled.

**Applicability to MoneyHorst**: NONE currently. MoneyHorst is not a US broker-dealer. These fields are future compliance references only.

### 8.2 FINRA Rule 5310 — Best Execution (SRC-I-09)

**What it governs**: US FINRA member broker-dealers must use reasonable diligence to find the most favorable market for customer orders.

**Vocabulary reserved from this source**: best_execution_required, execution_venue_eligible, order_routing_policy_required.

**Applicability to MoneyHorst**: NONE currently. MoneyHorst is not a FINRA member broker-dealer.

### 8.3 MiFID II Article 27 — Best Execution Obligation (SRC-I-08)

**What it governs**: EU investment firms must take all sufficient steps to obtain the best possible result for clients (price, costs, speed, likelihood of execution, size, nature).

**Vocabulary reserved from this source**: best_execution_required, execution_venue_eligible, order_routing_policy_required.

**Applicability to MoneyHorst**: NONE currently. MoneyHorst is not an EU-regulated investment firm.

### 8.4 MiFID II RTS 6 — Algorithmic Trading (SRC-I-11)

**What it governs**: EU investment firms using algorithmic trading must have resilient systems, pre-trade controls, kill switch, testing, annual certification, and market abuse monitoring.

**Vocabulary reserved from this source**: algo_trading_flag, kill_switch_required, pre_trade_controls_required, market_abuse_monitoring_required, surveillance_required, audit_log_required, manual_trade_only_flag.

**Applicability to MoneyHorst**: NONE currently. MoneyHorst does not deploy algorithmic trading strategies.

---

## 9. Source Authority Mapping

| Principle | Source | Authority Domain | Tier | Current Obligation? |
|-----------|--------|------------------|------|---------------------|
| Pre-trade controls: price collars, max order value/volume, message throttles | SRC-I-10 (SEC 15c3-5) | future_trading_reference | 1 | NO |
| Kill switch / cancel-all for automated trading | SRC-I-10/11 (SEC 15c3-5, MiFID II RTS 6) | future_trading_reference | 1 | NO |
| Best execution: price, costs, speed, likelihood, size, nature | SRC-I-08/09 (MiFID II Art.27, FINRA 5310) | future_trading_reference | 1 | NO |
| Algorithmic trading: resilience, testing, annual certification, surveillance | SRC-I-11 (MiFID II RTS 6) | future_trading_reference | 1 | NO |
| Restricted securities: prevent trading in blocked instruments | SRC-I-10 (SEC 15c3-5) | future_trading_reference | 1 | NO |
| Audit trail: electronic logs for supervisory review | SRC-I-10/11 | future_trading_reference | 1 | NO |
| Market abuse monitoring: detect and prevent manipulative behavior | SRC-I-11 (MiFID II RTS 6) | future_trading_reference | 1 | NO |

**All 7 principles**: Current obligation = NO. Future reference only.

---

## 10. Boundary Confirmations

| Boundary | Status |
|----------|--------|
| No peer_group_registry.yaml | CONFIRMED |
| No final peer assignments | CONFIRMED |
| No canonical peer_group_id | CONFIRMED |
| No SAI mutation | CONFIRMED |
| No code | CONFIRMED |
| No market data integration | CONFIRMED |
| No broker integration | CONFIRMED |
| No exchange connectivity | CONFIRMED |
| No ATS connection | CONFIRMED |
| No order routing | CONFIRMED |
| No execution logic | CONFIRMED |
| No market access controls runtime | CONFIRMED |
| No kill switch runtime | CONFIRMED |
| No pre-trade control runtime | CONFIRMED |
| No surveillance runtime | CONFIRMED |
| No compliance certification claim | CONFIRMED |
| No API keys or credentials | CONFIRMED |
| Tasks 1–7 unchanged | CONFIRMED |
| Task 9 not started | CONFIRMED |
| Tactical Momentum spec not started | CONFIRMED |

---

## Artifact Status

```
PGMF_TASK_8_TRADING_GOVERNANCE_BOUNDARY_READY_FOR_HUMAN_REVIEW
```

---

*End of trading governance boundary specification.*
