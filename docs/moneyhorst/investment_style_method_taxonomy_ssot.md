# MoneyHorst Investment Style, Method, and Allocation Taxonomy SSOT

> **Status**: MONEYHORST_INVESTMENT_STYLE_METHOD_TAXONOMY_SSOT_ACTIVE
> **Scope**: Conceptual guidance / architecture language
> **production_authority**: NONE
> **trading_authority**: NONE
> **decision_authority**: HUMAN_GOVERNED

---

## Purpose

This SSOT prevents MoneyHorst from being misunderstood as:

- a Growth strategy
- a Value strategy
- a Quant fund
- a stock-picking bot
- an asset allocation robo-advisor
- a trading system
- a broker/execution system

MoneyHorst operates at the Portfolio Intelligence / Decision Governance layer. It evaluates many investment styles, factors, methods, and asset allocation choices — it does not reduce to any one of them.

---

## Core Taxonomy

### Asset Class

What capital is invested in.

**Examples**: equities, bonds, cash, commodities, real assets, private markets.

### Instrument

The legal/security wrapper used to express exposure.

**Examples**: single stock, ETF, fund, bond, future, option, certificate, structured product.

### Investment Style

The philosophical or analytical lens used within an asset class.

**Examples**: Growth, Value, Quality, Momentum, Income, Defensive, Thematic.

### Factor

A measurable return/risk characteristic.

**Examples**: value, size, quality, momentum, low volatility, profitability, investment.

### Method

How decisions are generated or supported.

**Examples**: fundamental discretionary, quantitative, rules-based, AI-assisted research, systematic screening.

### Asset Allocation

Portfolio-level capital distribution across asset classes, regions, factors, themes, and risk buckets.

Asset Allocation is a **portfolio construction layer**, not the same as Growth or Value. It operates above individual styles and may combine many styles, factors, and asset classes.

### Strategy

A coherent investment approach combining asset class, style, method, time horizon, risk rules, and implementation instrument.

### System Layer

The infrastructure that supports research, signals, evidence, governance, and decision workflows.

**MoneyHorst belongs primarily here.**

---

## Clarify Common Confusions

### Growth Investment

Usually means Growth Equity investing: selecting companies with above-average expected growth. It is an **investment style** within equities. In professional language it may also refer to a Growth Equity mandate/product.

### Value Investment

Usually means selecting assets trading below estimated intrinsic value. It is an **investment style**, not an asset class.

### Quant Investment

A **method**, not an asset class. Quant can be used for stock selection, factor allocation, risk control, or asset allocation.

### Asset Allocation

A **portfolio-level activity**. It can include Growth, Value, Quality, Momentum, regions, bonds, cash, commodities, and risk overlays.

### Stock Investment

Direct investment in individual equities. It is an implementation universe / instrument-level exposure, not necessarily a style.

---

## MoneyHorst Definition

### English (Canonical)

MoneyHorst is not a single investment style such as Growth, Value, Quality, Momentum, or Income. MoneyHorst is not merely a Quant model and not a trading bot. MoneyHorst is a signal-driven Portfolio Intelligence and Decision Governance System that evaluates investment styles, quantitative signals, asset allocation choices, macro regimes, peer groups, evidence gaps, portfolio state, and human approval boundaries within one coherent investment operating system.

### German (Kanonisch)

MoneyHorst ist kein einzelner Investmentstil wie Growth, Value, Quality, Momentum oder Income. MoneyHorst ist kein reines Quant-Modell und kein Trading-Bot. MoneyHorst ist ein signalgetriebenes Portfolio-Intelligence- und Decision-Governance-System, das Investmentstile, quantitative Signale, Asset Allocation, Marktregime, Peer Groups, Evidence Gaps, Portfoliozustand und menschliche Freigabegrenzen in einem Investment Operating System zusammenführt.

---

## MoneyHorst Layer Mapping Table

| Layer | Example | MoneyHorst Position |
|-------|---------|---------------------|
| Asset Class | Equities, bonds, cash | Evaluated, not owned by definition |
| Instrument | Stock, ETF, derivative | Registered/analyzed, not automatically traded |
| Style | Growth, Value, Quality | Compared as possible lenses |
| Factor | Momentum, value, quality | Used as signal primitives |
| Method | Fundamental, Quant, AI-assisted | Combined, not exclusive |
| Asset Allocation | Capital distribution | Supported through governance and signals |
| Strategy | Portfolio approach | Can be represented, reviewed, and governed |
| System Layer | Research OS / Decision OS | **MoneyHorst's primary identity** |

---

## Interpretation Note

When an investment manager says they moved from Growth investing to Asset Allocation and then to Quant investing, these are not all the same category:

- **Growth** describes a style/product mandate, usually within equities.
- **Asset Allocation** describes a portfolio construction layer.
- **Quant** describes a decision method.

This distinction is important for MoneyHorst because MoneyHorst must not be reduced to any one of these categories.

---

## MoneyHorst Non-Goals

MoneyHorst does **not**:

- decide autonomously
- place trades
- replace human portfolio management judgment
- act as a broker
- create execution routes
- turn candidate research into production decisions automatically
- convert signals into orders
- make Growth, Value, or Quant the exclusive philosophy

---

## Governance Rule

Any future MoneyHorst spec that introduces strategy language must explicitly identify whether it is referring to:

1. asset class
2. instrument
3. investment style
4. factor
5. method
6. asset allocation layer
7. strategy
8. system layer

If the spec fails to identify the layer, the wording must be treated as **ambiguous** and hardened before implementation.

---

## Cross-References

| Document | Path |
|----------|------|
| Decision Governance | `docs/decision_governance.md` |
| Engine Design Principles | `docs/engine_design_principles.md` |
| System Architecture | `docs/system_architecture.md` |
| Semantic Signal Registry | `docs/semantic_signal_registry.md` |
| Portfolio State Model | `docs/portfolio_state_model.md` |
| Research Mechanism SSOT | `docs/moneyhorst/research_mechanism_ssot.md` |

---

## Boundary Confirmations

- ✓ No runtime code created
- ✓ No trading or execution logic
- ✓ No broker/exchange/ATS connectivity
- ✓ No market data integration
- ✓ No production registry files
- ✓ No SAI mutation
- ✓ No portfolio recommendations or allocation instructions
- ✓ No production authority introduced
- ✓ Documentation-only guidance

---

```
MONEYHORST_INVESTMENT_STYLE_METHOD_TAXONOMY_SSOT_ACTIVE
```

---

*End of SSOT document.*
