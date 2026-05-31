---
artifact_id: market_data_governance_framework_md
primary_domain: GOV
artifact_type: SSOT
lifecycle_status: canonical
created_date: 2026-05-31
last_modified: 2026-05-31
owner_role: Defines data rights, licensing, and compliance governance for all market data in MoneyHorst
ssot_relationship: canonical
topic: market_data_governance
allowed_writers: [GOV, ARCH]
allowed_readers: [ALL]
dependencies: [market_organism_framework, engine_roadmap_framework_md, signal_calculation_framework_md]
---

# MARKET DATA GOVERNANCE FRAMEWORK

Version: v1
Status: Canonical Governance Document
Track: P0 Governance (parallel to technical roadmap, not blocking current spec)

---

## WHY THIS DOCUMENT EXISTS

The Market Organism Framework, Signal Bubble, and Engine Roadmap define
WHAT MoneyHorst computes and HOW it propagates intelligence.

But none of them answer:

> Are we ALLOWED to store, process, cache, and redistribute this data?

This is not a technical question. It is a legal and compliance question.

The architecture already contains:
- Signal Bubble (cached intelligence objects)
- Static_Asset_Context (cached and refreshed by policy)
- Intelligence_Objects (addressable, versionable, served to consumers)
- Signal_Lifecycle_Definition (provenance, cache policy, refresh policy)

All of these imply DATA STORAGE and DATA PROCESSING.

When MoneyHorst eventually consumes real-time market feeds (Xetra, Nasdaq, NYSE,
Tradegate, Polygon, Refinitiv, FactSet, etc.), every cached value, every derived
metric, and every report output becomes subject to licensing terms.

This document defines the governance framework BEFORE that becomes a problem.

---

## THE CORE QUESTION

Not: "Can we technically fetch real-time data?"

But: "May we store, process, redistribute, and use it in MoneyHorst?"

These are fundamentally different questions with fundamentally different answers.

---

## THREE DATA CLASSES

MoneyHorst will possess three distinct classes of data,
each with different ownership and governance rules:

### Class A: Proprietary Computations

**Definition:** Intelligence produced entirely by MoneyHorst's own logic
from the user's own portfolio data.

**Examples:**
- Portfolio Health score
- AI Dependency signal
- Concentration Risk assessment
- Narrative Strength evaluation
- Market Fit / Portfolio Fit / Model Fit
- Expansion path analysis
- Butterfly effect projections

**Ownership:** Fully owned by MoneyHorst / the user.
**Storage:** Unrestricted.
**Caching:** Unrestricted.
**Redistribution:** At user's discretion.
**Retention:** Unlimited.

**Rule:** Class A data has NO external governance constraints.
It is the product of our own computation on our own inputs.

---

### Class B: Derived Intelligence

**Definition:** Intelligence computed by MoneyHorst that incorporates
external market data as one of its inputs, but transforms it
sufficiently to constitute a new work.

**Examples:**
- Narrative lifecycle state (derived from price movements + news + capital flows)
- Regime classification (derived from yields + volatility + breadth)
- Scenario projections (derived from historical patterns + current state)
- Trend signals (derived from price series)
- Relative strength metrics (derived from price comparisons)

**Ownership:** Owned by MoneyHorst (derivative work).
**Storage:** Subject to source data license terms.
**Caching:** Generally permitted (transformed data, not raw).
**Redistribution:** Generally permitted (sufficiently transformed).
**Retention:** Subject to source data retention policies.

**Rule:** Class B data is generally safe but must track its source lineage.
If the source license prohibits derived works, the derivation is not permitted.

---

### Class C: External Market Data

**Definition:** Raw or minimally processed data obtained from external
market data providers (exchanges, data vendors, brokers).

**Examples:**
- Bid / Ask / Last Price
- Volume
- Order Book depth
- Real-time quotes
- Intraday price series
- Corporate actions (splits, dividends)
- Fundamental data (revenue, earnings, balance sheet)

**Ownership:** Owned by the data provider / exchange.
**Storage:** Subject to license agreement.
**Caching:** Subject to license agreement (often restricted).
**Redistribution:** Almost always prohibited without separate license.
**Retention:** Subject to license agreement (often time-limited).

**Rule:** Class C data is the most restricted. Every use must be
validated against the specific provider's license terms.

---

## GOVERNANCE QUESTIONS PER SIGNAL

For every signal in the Signal Bubble, the following must be answerable:

| Question | Field | Example |
|----------|-------|---------|
| Where does this data come from? | data_source | "Xetra via broker API" |
| What license governs it? | license_type | "Delayed 15min, personal use only" |
| May it be stored? | storage_permission | yes / no / time-limited |
| May it be cached? | cache_permission | yes / duration-limited / no |
| May it appear in reports? | redistribution_permission | yes (personal) / no (commercial) |
| Is it real-time or delayed? | realtime_status | realtime / delayed-15min / EOD |
| How long may it be retained? | retention_policy | 30 days / 1 year / unlimited |
| Is it raw or derived? | data_class | A (proprietary) / B (derived) / C (external) |

---

## SIGNAL_LIFECYCLE_DEFINITION EXTENSION

The existing Signal_Lifecycle_Definition (Requirement 13) already contains 11 fields.

For market data governance, the following fields should be added in a future phase:

```
Signal_Lifecycle_Definition (extended):
  ... existing 11 fields ...
  data_class: A | B | C
  data_source: string (provider name + feed type)
  license_type: string (license identifier or "proprietary")
  storage_permission: unrestricted | time-limited | prohibited
  cache_permission: unrestricted | duration-limited | prohibited
  redistribution_permission: personal | commercial | prohibited
  realtime_status: realtime | delayed | EOD | static
  retention_policy: string (duration or "unlimited")
```

**Important:** These fields are NOT required for the current Market Organism spec.
They become mandatory when MoneyHorst connects to external data feeds.

---

## PROVIDER LANDSCAPE (Known Future Sources)

| Provider | Data Type | Likely License Model |
|----------|-----------|---------------------|
| Xetra (Deutsche Boerse) | German equities, ETFs | Delayed free, realtime paid |
| Nasdaq | US equities | Delayed free, realtime paid per-user |
| NYSE | US equities | Delayed free, realtime paid per-user |
| Tradegate | German retail exchange | Often free via broker |
| L&S (Lang & Schwarz) | German OTC | Often free via broker |
| CBOE | Options, VIX | Delayed free, realtime paid |
| Polygon.io | US equities, crypto | API subscription, redistribution restricted |
| Refinitiv (LSEG) | Multi-asset | Enterprise license, strict redistribution |
| FactSet | Fundamentals | Enterprise license |
| Alpha Vantage | Multi-asset | Free tier limited, paid tiers |
| Yahoo Finance | Multi-asset | Personal use, no commercial redistribution |
| Broker APIs (IBKR, etc.) | Portfolio + market data | Personal use, no redistribution |

**Key insight:** Most free/broker data is licensed for PERSONAL USE ONLY.
Commercial redistribution (even in a self-hosted tool) may require separate licensing
depending on how "commercial" is defined.

---

## CURRENT STATE ASSESSMENT

### What MoneyHorst does today (safe)

- Analyzes the user's OWN portfolio data (Excel files) — Class A
- Computes proprietary signals from own data — Class A
- Generates reports for personal use — Class A
- Stores semantic states and snapshots — Class A

### What MoneyHorst will need later (requires governance)

- Real-time price feeds for portfolio valuation — Class C
- Historical price data for trend signals — Class C (or B if sufficiently derived)
- Fundamental data for asset quality assessment — Class C
- News/sentiment data for narrative detection — Class B or C
- Market breadth/flow data for regime detection — Class C

### Current risk level: LOW

Today, MoneyHorst operates entirely on Class A data (user's own Excel files).
No external market data feeds are connected.
No licensing issues exist in the current state.

---

## GOVERNANCE TIERS (When to Act)

| Tier | Trigger | Action Required |
|------|---------|-----------------|
| Tier 0 (current) | Only user's own data | No action needed |
| Tier 1 | Delayed market data via free APIs | Document data sources, confirm personal-use compliance |
| Tier 2 | Cached/stored market data | Implement retention policies, add data_class to Signal_Lifecycle |
| Tier 3 | Real-time feeds | Formal license review, per-provider compliance check |
| Tier 4 | Multi-user / commercial | Full market data licensing, redistribution agreements |

**Current position:** Tier 0. No governance action blocking.

---

## ARCHITECTURAL PREPAREDNESS

The existing architecture is well-prepared for future governance:

| Architecture Element | Governance Readiness |
|---------------------|---------------------|
| Signal_Lifecycle_Definition | Ready — add data_class + license fields when needed |
| Signal Bubble registry | Ready — central place to enforce governance per signal |
| Intelligence_Object model | Ready — provenance field already tracks source |
| Cache policy (per signal) | Ready — can enforce retention limits |
| Refresh policy (per signal) | Ready — can enforce delayed vs. realtime |
| Single-source-of-truth principle | Ready — prevents ungoverned private copies |

**Key insight:** The "no private recalculation" invariant (Req 11) is not just
architecturally clean — it is also a GOVERNANCE enabler. If all data flows through
the Signal Bubble, governance can be enforced at one point rather than everywhere.

---

## COMPLIANCE PRINCIPLES

### Principle 1: Know Your Source
Every signal that incorporates external data must declare its source.
No "magic numbers" without provenance.

### Principle 2: Classify Before Cache
Before any external data is cached, its data_class must be determined.
Class C data may NOT be cached without license verification.

### Principle 3: Derive to Own
Where possible, transform external data sufficiently to create Class B (derived)
intelligence. Derived works have fewer restrictions than raw data.

### Principle 4: Personal Use First
MoneyHorst operates as a personal portfolio intelligence tool.
Personal-use licenses are the baseline. Commercial licensing is a future concern.

### Principle 5: Governance at the Bubble
All governance enforcement happens at the Signal Bubble level.
Individual consumers never need to know licensing details —
the Bubble serves only what is permitted.

### Principle 6: Retention by Policy
No data is stored indefinitely by default.
Every Class C signal must have an explicit retention policy.
Class A and B may have unlimited retention.

---

## RELATIONSHIP TO EXISTING ARCHITECTURE

| Layer | Document | Governance Impact |
|-------|----------|-------------------|
| Layer 1 | Market Organism | None — pure definition, no data |
| Layer 2 | User Journey | None — navigation model, no data |
| Layer 3 | Capability Matrix | Minimal — capabilities are abstract |
| Layer 4 | Engine Roadmap | P0 Governance track runs parallel |
| Signal Architecture | Signal_Lifecycle_Definition | Direct — add governance fields when external data arrives |
| Signal Architecture | Signal Bubble | Direct — enforcement point for all governance |
| Signal Architecture | Signal_Bubble_v0 | Safe — all Class A (user's own data) |

---

## WHAT THIS DOCUMENT IS NOT

- NOT a legal opinion (consult legal counsel for specific licenses)
- NOT a technical implementation (no code, no APIs)
- NOT blocking current development (Tier 0 = no action needed)
- NOT a data architecture (that belongs to Signal_Lifecycle_Definition)

This document defines the GOVERNANCE FRAMEWORK that will be activated
when MoneyHorst transitions from Tier 0 (own data only) to Tier 1+ (external feeds).

---

## NEXT STEPS (When Triggered)

1. **Tier 1 activation:** When first external API is connected, document the source and confirm personal-use compliance
2. **Tier 2 activation:** When data is first cached/stored, add data_class field to Signal_Lifecycle_Definition
3. **Tier 3 activation:** When real-time feeds are needed, conduct formal license review per provider
4. **Tier 4 activation:** If MoneyHorst ever serves multiple users, engage legal for redistribution licensing

---

## KEY INSIGHT

The architecture is already governance-ready because of three decisions made earlier:

1. **Signal Bubble as single source of truth** — governance enforced at one point
2. **Signal_Lifecycle_Definition** — extensible with governance fields
3. **No private recalculation invariant** — prevents ungoverned data copies

The governance framework runs as a PARALLEL TRACK to the technical roadmap.
It does not block current development.
It activates progressively as MoneyHorst's data sources expand.

Current status: Tier 0. All clear. No action required until external feeds arrive.
