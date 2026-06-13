# PR #25 Audit — Asset Type and Analyst Sentiment Guidance

> **Scope**: PR audit / documentation guidance review
> **production_authority**: NONE
> **merge_authority**: HUMAN_REVIEW_REQUIRED
> **Status**: PR25_ASSET_TYPE_SENTIMENT_GUIDANCE_AUDIT_READY

---

## Purpose

PR #25 is the only remaining open PR in the repository. It must be audited before continuing peer group review work. This audit evaluates PR #25 against the current MoneyHorst SSOT documents merged since the PR was opened (June 7, 2026).

---

## PR #25 Summary

| Field | Value |
|-------|-------|
| PR title | Add asset type and analyst sentiment guidance |
| Branch | `docs/asset-type-sentiment-guidance` |
| Files changed | `docs/README_asset_type_and_sentiment_guidance.md` (289 lines, new file) |
| Intended purpose | Architecture guidance for future ETF/fund asset type support and analyst sentiment consumption |
| Created | 2026-06-07 |
| Current state | OPEN |
| Mergeability | UNKNOWN (stale — may need rebase) |
| CI status | SUCCESS (at time of PR creation, 2026-06-07) |

---

## Alignment With Current MoneyHorst SSOT

### Investment Style / Method / Allocation Taxonomy SSOT

PR #25 does not use style/method/allocation terminology incorrectly. It correctly frames:
- ETFs/funds as **instruments** (legal wrappers), not as investment styles
- Analyst sentiment as **evidence input**, not as a decision method or strategy
- Asset types as a classification layer, not as strategy preferences

**Alignment**: PASS — no conflict with the taxonomy SSOT.

### Research Mechanism SSOT

PR #25 aligns with the research mechanism principles:
- Sentiment is evidence, not truth
- No autonomous decisions from sentiment
- Provenance requirements for all inputs
- Human governance preserved

**Alignment**: PASS — conceptually consistent.

### Decision Governance Principles

PR #25 explicitly states:
- No buy/sell/hold output
- No conviction scores
- No recommendation generation
- No allocation authority
- SAI does not independently calculate sentiment

**Alignment**: PASS — boundaries are correct.

### Peer Group Preflight Boundary Rules

PR #25 does not reference or conflict with peer group preflight work. It addresses different scope (asset type guidance vs. peer group methodology).

**Alignment**: PASS — no interaction.

---

## Boundary Review

| Boundary | Status | Notes |
|----------|--------|-------|
| No autonomous investment decisions | PASS | Explicitly prohibited in document |
| No buy/sell/hold recommendations | PASS | Multiple explicit prohibitions |
| No sentiment-as-decision shortcut | PASS | "Sentiment never instructs action" |
| No price-target-as-output | PASS | "Price targets consumed as dispersion evidence only, never as SAI output" |
| No ETF/fund scoring without methodology | PASS | "Must not assign fund scores or rankings" |
| No runtime code | PASS | Non-Goals section confirms no implementation |
| No validation code | PASS | Non-Goals section confirms no validators |
| No market data integration | PASS | Guidance only, no data connections |
| No trading/execution scope | PASS | Non-Goals section confirms no trading logic |
| No SAI mutation | PASS | "Does NOT mutate current SAI requirements, design, tasks, artifacts, gates, registries, or SSOT files" |
| No production registry scope | PASS | No registry references |

---

## Conceptual Drift Review

| Concept | Risk | Assessment |
|---------|------|-----------|
| Asset class vs instrument | LOW | PR #25 treats ETF/fund as asset types for analysis purposes; the taxonomy SSOT clarifies these are instruments. Minor terminology difference but not conflicting — PR #25 uses "asset type" in the SAI classification sense, not the investment-class sense. |
| Investment style vs factor | NONE | PR #25 does not discuss styles or factors. |
| Method vs strategy | NONE | PR #25 does not discuss methods or strategies. |
| Portfolio intelligence layer vs trading system | NONE | Clear separation maintained. |
| ETF/fund as asset wrappers | NEEDS_HARDENING | PR #25 should cross-reference the taxonomy SSOT to clarify that ETFs/funds are instruments (wrappers) at the taxonomy layer, even though they are classified as "asset types" for SAI block-applicability purposes. |
| Analyst sentiment as evidence input | PASS | Correctly framed throughout. |
| Analyst sentiment as signal input | PASS | "Consumed by SAI blocks when delivered by approved upstream frameworks." |
| Analyst sentiment as recommendation source | PASS | Explicitly prohibited. |
| MoneyHorst system layer | NEEDS_HARDENING | PR #25 does not reference MoneyHorst's system-layer identity or the taxonomy SSOT. A cross-reference would prevent future confusion. |

---

## Recommendation

### **B. NEEDS_HARDENING_BEFORE_MERGE**

PR #25 is useful, boundary-safe, and conceptually sound. It does not conflict with current SSOT documents. However, it was created before the Investment Taxonomy SSOT was merged and should be updated with:

1. A cross-reference to the taxonomy SSOT
2. A clarifying note about ETF/fund as instrument-layer classification

---

## Required Hardening (Before Merge)

| # | Required Edit | Location | Reason |
|---|--------------|----------|--------|
| 1 | Add cross-reference block to `docs/moneyhorst/investment_style_method_taxonomy_ssot.md` | End of "Authority and Scope" section or new "Cross-References" section | Prevents taxonomy drift; aligns with newer SSOT |
| 2 | Add clarifying note: "In the MoneyHorst Investment Taxonomy, ETFs and funds are classified as **instruments** (legal/security wrappers). Within SAI, they are treated as distinct **asset types** for block-applicability purposes. These are compatible classifications at different architectural layers." | Within the ETF section introduction | Prevents confusion between taxonomy-layer and SAI-layer terminology |
| 3 | File naming: Consider renaming from `README_asset_type_and_sentiment_guidance.md` to stay in `docs/moneyhorst/` directory for discoverability | File path | Currently at `docs/` root level rather than `docs/moneyhorst/` — acceptable but less discoverable |

**Note**: Item 3 (file rename) is optional — the current location at `docs/` root is acceptable per existing project structure.

---

## Explicit Non-Authorization

This audit does **not** authorize:

- Merging PR #25
- Production registry creation
- Candidate approval
- SAI mutation
- Market data integration
- Trading or execution usage
- Automated recommendations

---

## Boundary Confirmations

- ✓ No production registry created
- ✓ No peer_group_registry.yaml created
- ✓ No candidate records modified
- ✓ No Candidate_Status values changed
- ✓ No SAI mutation
- ✓ No runtime code created
- ✓ No validation code created
- ✓ No market data integration
- ✓ No trading or execution scope
- ✓ No production registry creation spec started

---

```
PR25_ASSET_TYPE_SENTIMENT_GUIDANCE_AUDIT_READY
```

---

*End of PR #25 Audit.*
