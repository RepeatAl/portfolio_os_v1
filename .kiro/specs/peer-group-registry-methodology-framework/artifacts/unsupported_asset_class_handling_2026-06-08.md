# Peer Group Registry Methodology Framework — Unsupported Asset Class Handling Specification

**Artifact**: unsupported_asset_class_handling_2026-06-08.md
**Task**: Task 9 — Create Unsupported Asset Class Handling Specification
**Spec**: peer-group-registry-methodology-framework
**Date**: 2026-06-08
**Authority**: CTO / Architecture
**Status**: PGMF_TASK_9_UNSUPPORTED_ASSET_CLASS_HANDLING_READY_FOR_HUMAN_REVIEW

**Purpose**: Defines how the framework handles unsupported, deferred, ambiguous, private, synthetic, derivative, or non-standard asset classes without creating false peer groups, false comparability, or trading implications.

**Boundary statement**: Unsupported asset handling protects methodology integrity. It does not expand current asset-class coverage, authorize peer assignments for unsupported instruments, create trading eligibility, or imply that market data availability equals methodology support.

**Hard boundaries**: No peer_group_registry.yaml. No final peer assignments. No canonical peer_group_id. No SAI mutation. No code. No market data. No broker/exchange/ATS. No trading logic.


---

## 1. Scope

Unsupported asset handling exists to prevent methodology drift when an asset cannot safely receive a current peer methodology classification. The framework must gracefully refuse classification rather than invent false peer groups for instruments outside its current capability.

---

## 2. Unsupported / Deferred Asset Categories

The following asset categories are NOT supported by the current peer group methodology (v1). They must receive one of the canonical handling statuses defined in Section 3.

| Category | Examples | Reason Not Supported in v1 |
|----------|----------|---------------------------|
| Private companies | SpaceX, Stripe, ByteDance | No public market data; no FIGI/ISIN/MIC; private comparable methodology deferred (Q7 EVIDENCE_INSUFFICIENT) |
| Private funds / PE / VC vehicles | Blackstone funds, Sequoia vehicles | No public market pricing; fund-level methodology not defined |
| Private credit vehicles | Direct lending funds, CLO tranches | Credit instrument methodology not defined |
| Hedge funds | Multi-strategy HFs, L/S equity HFs | Different risk/return profile; not comparable to public equity |
| SPVs / structured vehicles | Securitization SPVs, SPAC shells pre-deal | No operating business model; entity resolution complex |
| Structured products | Certificates, autocallables, reverse convertibles | Product mechanics dominate; not comparable to underlying equities |
| Options / warrants | NVDA calls, covered warrants | Derivative of an underlying; payoff structure, not business model |
| Leveraged products | Turbo certificates, knock-outs, factor certificates | Product mechanics + leverage; not comparable to company equity |
| Futures | S&P 500 futures, DAX futures | Derivative contract on an index/commodity; temporal, not structural |
| Swaps / CFDs | Total return swaps, CFDs on equities | Synthetic exposure; counterparty-dependent; not a company |
| Crypto / tokenized assets | BTC, ETH, tokenized securities, NFTs | No earnings, no revenue; on-chain metrics; entirely different framework needed |
| Commodities / physical assets | Gold, oil, wheat, real estate parcels | Supply/demand/regime driven; no company fundamentals |
| Currencies / FX pairs | EUR/USD, GBP/CHF | Macro/rate/liquidity driven; no corporate entity |
| Bonds / fixed income | Corporate bonds, government bonds, money market | Issuer, duration, spread, rating, covenant, seniority — entirely different methodology |
| Money market instruments | T-bills, commercial paper, repos | Short-term liquidity instruments; not comparable to equity |
| Indices / baskets | S&P 500, Nasdaq-100, custom baskets | Mathematical constructs; not investable entities (covered by benchmark_context rule) |
| Synthetic exposures | Synthetic short positions, structured notes | Constructed payoffs; not entities with business models |
| Incomplete / unresolved identity | Assets without confirmed canonical_object_id | Cannot be classified without confirmed identity |
| Insufficient source authority | Assets where no Tier 1 source supports classification | Methodology requires evidence-backed assignment |
| Conflicting entity identity | Assets where entity resolution is ambiguous or disputed | Cannot receive peer assignment until identity is resolved |

---

## 3. Canonical Handling Statuses

| Status | Meaning | Treatment |
|--------|---------|-----------|
| `UNSUPPORTED_CURRENT_METHODOLOGY` | Asset class has no methodology in v1. Peer assignment architecturally impossible. | peer_comparison_allowed = false; peer_group_available = false; blocked_reason documented |
| `DEFERRED_ASSET_CLASS` | Methodology may exist in future but is not yet defined. Asset awaits future extension. | Same as above; additionally marked for future review |
| `CONTEXT_ONLY` | Asset may be referenced for ecosystem, competitive landscape, or macro context but receives no peer assignment. | No peer_group_id; no peer_role except private_comparable_context (private companies) or benchmark_context (indices) |
| `SOURCE_INSUFFICIENT` | Asset identity is resolved but insufficient evidence/source authority exists for classification. | Peer assignment blocked until source authority improves |
| `IDENTITY_UNRESOLVED` | Asset cannot be uniquely identified — canonical_object_id cannot be confirmed. | All assignment blocked; identity resolution required first |
| `SYNTHETIC_EXPOSURE_ONLY` | Asset is a synthetic or derivative instrument providing exposure to another asset/index. | Not a peer group member; underlying may be classified if eligible |
| `DERIVATIVE_ON_SUPPORTED_UNDERLYING` | Asset is a derivative whose underlying IS supported. The underlying may be classified; the derivative itself is not. | Derivative receives no peer assignment; underlying evaluated separately |
| `INDEX_OR_BASKET_REFERENCE_ONLY` | Asset is an index or basket used as reference. | peer_role = benchmark_context; never company peer; never etf_peer |
| `PRIVATE_COMPANY_CONTEXT_ONLY` | Private company usable as competitive landscape context. | peer_role = private_comparable_context; valuation_peer_allowed = false; comparison_mode = ecosystem_context_only |
| `FUTURE_EXTENSION_REQUIRED` | Asset class is recognized but requires a dedicated future spec before any methodology applies. | Blocked until future spec created, sourced, and approved |

---

## 4. Treatment Rules

### 4.1 Must NOT

- Unsupported assets must NOT receive final peer_group_id values
- Unsupported assets must NOT be assigned to final peer groups
- Unsupported assets must NOT be forced into equity-style peer groups
- Unsupported assets must NOT mutate SAI artifacts
- Unsupported assets must NOT create false comparability (a bond is not comparable to its issuer's equity)
- Unsupported assets must NOT imply trading eligibility
- Classification must NOT be invented to fill a gap — graceful refusal is correct behavior

### 4.2 MAY

- Unsupported assets MAY be referenced as context where appropriate (competitive landscape, ecosystem, macro exposure)
- Unsupported assets MAY require future methodology extensions
- Unsupported assets MAY hold a canonical_object_id for identity tracking (if identity is resolved) without peer assignment
- Private companies MAY receive peer_role = private_comparable_context with strict constraints (valuation_peer_allowed = false, comparison_mode = ecosystem_context_only)
- Indices MAY receive peer_role = benchmark_context (per ETF/fund spec, Task 4)

---

## 5. Key Distinctions

| Concern | What It Means | Does NOT Mean |
|---------|--------------|---------------|
| Peer group eligibility | Asset can receive a canonical peer_role within a supported family | Asset is tradable, executable, or order-routable |
| Contextual relevance | Asset is useful for understanding competitive landscape | Asset has a peer group or comparability |
| Underlying exposure relevance | A derivative references this asset as its underlying | The derivative is a peer group member |
| Tradability | Asset can be bought/sold on an exchange (FUTURE_COMPLIANCE_REFERENCE) | Asset has a peer group or methodology support |
| Market data availability | Quote data exists for this asset | Methodology has been defined for this asset class |
| Portfolio holding status | Asset is currently held in the portfolio | Asset has been classified with a peer group |
| Derivative-underlying relationship | A derivative instrument exists on this asset | The derivative receives peer classification |
| Index/basket membership | Asset is a constituent of an index | Asset IS the index (it is not) |
| Private-company relationship | A private company competes with a public peer | Private company receives valuation-peer status (it does not) |

---

## 6. Derivative and Structured Product Rule

### 6.1 Principle

If a derivative, option, warrant, certificate, leveraged product, future, swap, CFD, or structured product references an underlying company or ETF:
- The **underlying** may be classified IF it is independently eligible under the equity/ETF methodology
- The **derivative instrument itself** must NOT become a peer-group member
- The derivative receives status: `DERIVATIVE_ON_SUPPORTED_UNDERLYING` or `SYNTHETIC_EXPOSURE_ONLY`

### 6.2 Examples

| Instrument | Underlying | Derivative Status | Underlying Status |
|-----------|-----------|-------------------|-------------------|
| NVDA call option | NVDA (company) | DERIVATIVE_ON_SUPPORTED_UNDERLYING — no peer group | NVDA classified normally in PGF-01 |
| Turbo certificate on Rheinmetall | Rheinmetall (company) | DERIVATIVE_ON_SUPPORTED_UNDERLYING — no peer group | Rheinmetall classified in PGF-06 with IFRS/cross-region flags |
| DAX future | DAX index | SYNTHETIC_EXPOSURE_ONLY — no peer group | DAX = index = benchmark_context only |
| EUR/USD CFD | EUR/USD FX pair | UNSUPPORTED_CURRENT_METHODOLOGY — no peer group | EUR/USD = FX = unsupported in current methodology |
| BTC perpetual swap | Bitcoin | UNSUPPORTED_CURRENT_METHODOLOGY — no peer group | Bitcoin = crypto = unsupported in current methodology |

### 6.3 No Derivative Peer Registry in v1

No derivative methodology exists. No derivative peer group may be created. A future derivative methodology extension would need to define: product mechanics comparability, leverage normalization, expiry structure, strike/barrier semantics, issuer risk, and product-type taxonomy. This is entirely out of current scope.

---

## 7. Private Company Rule

### 7.1 Principle

Private companies may be referenced as competitive landscape context. They must NOT receive public-equity peer assignment.

### 7.2 Permitted References

Private companies may appear as:
- Strategic comparables (private competitor of a public peer)
- Customer or supplier context
- Ecosystem context (platform relationships)
- Parent, subsidiary, or affiliated entity context
- Sponsor/owner context (PE ownership affecting public company capital structure)

### 7.3 Constraints

- peer_role = `private_comparable_context` ONLY
- valuation_peer_allowed = false (always)
- comparison_mode_allowed = `ecosystem_context_only`
- No FIGI, ISIN, exchange_mic, or market_data fields apply
- canonical_object_id is internally assigned (no external standard available)
- Full private comparable methodology deferred (Q7 EVIDENCE_INSUFFICIENT)

---

## 8. ETF / Fund Boundary

ETFs and funds follow ONLY the ETF/Fund methodology from Task 4. They must NOT be forced into operating-company peer groups. If ETF/fund data is insufficient for classification within PGF-09, classify as `SOURCE_INSUFFICIENT` or `DEFERRED_ASSET_CLASS`.

An ETF without a known benchmark_index receives: peer_comparison_allowed = false, financial_comparability_gate_status = blocked, blocked_reason = "No benchmark_index available."

---

## 9. Index / Basket Boundary

Indices and baskets are reference structures only:
- peer_role = `benchmark_context` (per Task 4 specification)
- NEVER receive operating-company peer assignments
- NEVER receive etf_peer assignments (etf_peer is for funds, not for the index itself)
- Index constituents may be evaluated separately if individually eligible and identity-resolved
- Custom baskets without a canonical index_provider receive: `INDEX_OR_BASKET_REFERENCE_ONLY`

---

## 10. Crypto / Tokenized Asset Boundary

Crypto assets, tokenized assets, digital assets, and on-chain instruments are `UNSUPPORTED_CURRENT_METHODOLOGY`:
- No earnings, revenue, margin, balance sheet, or filings exist
- On-chain metrics, network effects, and liquidity regime require entirely different frameworks
- They must NOT be mapped into equity, ETF, fund, or trading peer groups
- A future crypto/digital asset methodology would require dedicated evidence sourcing, taxonomy, and CTO approval
- Status: `FUTURE_EXTENSION_REQUIRED` if future methodology is planned; otherwise `UNSUPPORTED_CURRENT_METHODOLOGY`

---

## 11. Fixed Income / Commodity / FX Boundary

### 11.1 Bonds and Fixed Income

Corporate bonds, government bonds, high-yield bonds, convertible bonds, and money market instruments:
- Comparison requires: issuer, duration, spread, rating, covenant, seniority, currency, and liquidity — entirely different from equity peer methodology
- Status: `UNSUPPORTED_CURRENT_METHODOLOGY`
- May be referenced for macro or credit exposure context only

### 11.2 Commodities and Physical Assets

Gold, oil, wheat, copper, and physical real estate:
- Supply/demand/regime driven; no corporate fundamentals
- Status: `UNSUPPORTED_CURRENT_METHODOLOGY`
- May be referenced for macro sensitivity or supply-chain context

### 11.3 Currencies / FX Pairs

EUR/USD, GBP/CHF, and all FX pairs:
- Macro, monetary policy, and liquidity regime comparisons; no corporate entity
- Status: `UNSUPPORTED_CURRENT_METHODOLOGY`
- May be referenced for currency exposure or macro context

---

## 12. SAI-BLK-21 Graceful Degradation

### 12.1 Block Unsupported from Final Assignment

SAI-BLK-21 must NOT produce peer-relative observations for unsupported assets. When an asset carries any unsupported status: peer_comparison_allowed = false; peer_group_available = false.

### 12.2 Surface Status Clearly

SAI must produce deferred_dependency_notes explaining the unsupported status:
- "Asset class not supported by current Peer Group Methodology (v1). Peer comparison blocked."
- "Private company — context only; valuation peer comparison prohibited."
- "Derivative instrument — underlying may have peers; derivative itself has no peer group."

### 12.3 Preserve Context

When an unsupported asset is referenced as competitive landscape or ecosystem context (private_comparable_context or benchmark_context), SAI may surface that context without producing peer-relative metrics:
- "SpaceX referenced as strategic comparable for PGF-06 defense/AI context. No peer metrics available — private company, context only."

### 12.4 Avoid

- Hallucinated peer_group_id values for unsupported assets
- False comparability (comparing a bond to its issuer's equity)
- Suggesting trading eligibility based on unsupported status
- Using unsupported asset presence as evidence for peer methodology completeness

---

## 13. Source Authority Requirements for Future Extension

An unsupported asset class may transition from deferred to supported ONLY if minimum source authority resolves:

| Requirement | Why Needed |
|-------------|-----------|
| Asset identity (canonical_object_id resolvable) | Cannot classify without stable identity |
| Legal entity or instrument identity | Determines object_type |
| Asset type classification | Determines which methodology applies |
| Issuer or underlying identification | Determines whether derivative-underlying rule applies |
| Exchange / venue (if applicable) | Determines listing-level context |
| Currency (if applicable) | Determines cross-region handling |
| Ownership / fund structure (if applicable) | Determines fund/PE/VC handling |
| Data availability assessment | Determines whether evidence is sufficient for peer comparison |
| Methodology-specific comparability basis | Each asset class needs its own comparability framework |

---

## 14. Future Extension Pathway

Unsupported asset classes may move from deferred to supported ONLY through:
1. Explicit future framework/spec (requirements → design → tasks)
2. Source authority review (Tier 1 institutional sources for the asset class)
3. Field taxonomy update (new asset-type-specific fields defined)
4. Methodology definition (comparability gates, peer role rules, comparison modes)
5. Governance review (CTO approval for scope expansion)
6. Human approval (additive-only extension principle)

No asset class may transition to supported without ALL six steps completed.

---

## 15. Blocked Actions

| Prohibited | Reason |
|-----------|--------|
| Final peer assignment for unsupported assets | No methodology exists |
| Forced classification into equity peer groups | Destroys methodology integrity |
| peer_group_id creation for unsupported assets | Would create false canonical groups |
| peer_group_registry.yaml creation | Registry creation is a separate future task |
| Runtime implementation | Methodology specification only |
| SAI mutation | SAI interface contract is unchanged |
| Market data integration | Market data readiness is schema-only (Task 7) |
| Broker/trading/execution logic | Trading governance is future-only (Task 8) |
| Compliance claim | MoneyHorst is not a regulated entity |
| Private-company peer registry | Full private methodology deferred (Q7) |
| Derivative peer registry | No derivative methodology exists |
| Crypto methodology | No crypto methodology exists |
| Fixed-income methodology | No bond/credit methodology exists |
| Commodity methodology | No commodity methodology exists |

---

## 16. Boundary Confirmations

| Boundary | Status |
|----------|--------|
| No peer_group_registry.yaml | CONFIRMED |
| No final peer assignments | CONFIRMED |
| No canonical peer_group_id | CONFIRMED |
| No SAI mutation | CONFIRMED |
| No code | CONFIRMED |
| No market data | CONFIRMED |
| No broker/exchange/ATS | CONFIRMED |
| No trading logic | CONFIRMED |
| No API keys or credentials | CONFIRMED |
| Tasks 1–8 unchanged | CONFIRMED |
| Task 10 not started | CONFIRMED |
| Tactical Momentum spec not started | CONFIRMED |

---

## Artifact Status

```
PGMF_TASK_9_UNSUPPORTED_ASSET_CLASS_HANDLING_READY_FOR_HUMAN_REVIEW
```

---

*End of unsupported asset class handling specification.*
