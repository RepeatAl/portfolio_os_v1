# Owner-Verified P4 Decision Record — Peer Group Registry Preflight

> **Scope**: Owner-verified P4 regional / structural decision record
> **production_authority**: NONE
> **registry_creation_authority**: NONE
> **candidate_approval_authority**: NONE
> **decision_authority**: OWNER_VERIFIED_REVIEW_DECISION
> **Status**: P4_OWNER_VERIFIED_DECISION_RECORD_READY

---

## Purpose

This document records owner-verified P4 regional and structural decisions for five unresolved observations identified during the completed Peer Group Registry Creation Preflight.

These are owner-verified review decisions for future spec input. They:

- Do **not** create production registry authority
- Do **not** approve candidates
- Do **not** create final production peer assignments
- Do **not** mint canonical peer_group_id values
- Do **not** mutate SAI
- Do **not** start Production Registry Creation Spec

---

## Decision Basis

Decisions are based on:

1. **MoneyHorst scope alignment** — classifying regional and structural comparability for portfolio intelligence and decision governance
2. **Institutional regional comparability** — respecting that different regions have materially different market structures
3. **Structural comparability discipline** — not mechanically mixing assets across structural breaks
4. **Avoidance of mechanically mixing regional peers** with different currencies, market structures, legal environments, or capital-market regimes
5. **Separation of peer comparability from benchmark_context and regional_context** — each has distinct analytical meaning
6. **Production-readiness discipline** — ensuring decisions are structurally sound before production use
7. **MoneyHorst taxonomy distinction** between asset class, instrument, investment style, factor, method, asset allocation, strategy, and system layer
8. **Asset Type and Analyst Sentiment Guidance** for PGF-09 ETF/fund handling

MoneyHorst is not deciding based on whether an asset is "Growth", "Value", "Quant", or simply a "stock". MoneyHorst is classifying regional and structural comparability for future portfolio intelligence and decision governance.

**References**:
- `docs/moneyhorst/investment_style_method_taxonomy_ssot.md`
- `docs/README_asset_type_and_sentiment_guidance.md`

---

## P4 Decision Summary Table

| Gap ID | Asset / Topic | Owner-Verified Decision | Status | Production Spec Effect |
|--------|---------------|------------------------|--------|------------------------|
| CTX-GAP-009 | MELI | Treat as LatAm regional subcluster/context; do not mechanically merge with US/EU e-commerce peers | APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION | Future production spec must preserve LatAm regional comparability caveat |
| CTX-GAP-010 | STNE | Treat as LatAm payments context; do not mechanically compare as fully equivalent to US/EU payments peers | APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION | Future production spec must preserve LatAm payments/regional caveat |
| CTX-GAP-012 | GRAB | Treat as SE Asia regional platform context; do not mechanically merge with US mobility/delivery peers | APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION | Future production spec must preserve SE Asia regional platform caveat |
| CTX-GAP-018 | UBS | Treat as comparable only with post-Credit-Suisse integration caveat | APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION | Future production spec must preserve structural break and integration-period caveat |
| CTX-GAP-019 | PGF-09 ETF Membership | Do not manually finalize ETF membership; require production data feeds for AUM, TER, holdings, methodology, liquidity, domicile, and replication method | DEFER_WITH_PRODUCTION_DATA_REQUIREMENT | Future production spec must source ETF/fund membership from approved production data feeds and asset-type guidance |

---

## Individual Decision Records

### CTX-GAP-009 — MELI

**Decision**: Regional handling: **LatAm regional subcluster/context required**.

**Peer handling**:
- MELI may remain relevant to commerce/platform peer analysis.
- MELI must not be mechanically merged with US/EU e-commerce or marketplace peers without regional comparability adjustment.
- Future production spec should preserve LatAm regional_context or LatAm subcluster treatment.

**Rationale**: MercadoLibre is structurally relevant to e-commerce, marketplace, fintech, and logistics platform analysis, but Latin America introduces distinct currency, inflation, interest-rate, legal, payment, logistics, and consumer-market structures. For MoneyHorst, MELI should be handled as LatAm regional context rather than treated as directly equivalent to US/EU peers.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION

**Conditions**:
- Future production spec must preserve LatAm regional comparability caveat.
- Peer analytics must not compare MELI mechanically against US/EU peers without regional adjustment.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-010 — STNE

**Decision**: Regional handling: **LatAm payments context required**.

**Peer handling**:
- STNE may remain relevant to payments/fintech peer analysis.
- STNE must not be mechanically treated as fully equivalent to US/EU payments networks or processors.
- Future production spec should preserve LatAm payments/regional_context.

**Rationale**: StoneCo is a LatAm/Brazil payments and merchant-acquiring platform with regional currency, rate, credit, regulatory, inflation, and merchant-structure exposures. It should be treated as LatAm payments context, not as a clean equivalent to US/EU card networks or payment processors.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION

**Conditions**:
- Future production spec must preserve LatAm/Brazil payments caveat.
- Peer analytics must not compare STNE mechanically against US/EU payments peers without regional adjustment.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-012 — GRAB

**Decision**: Regional handling: **SE Asia regional platform context required**.

**Peer handling**:
- GRAB may remain relevant to mobility, delivery, fintech, and super-app platform analysis.
- GRAB must not be mechanically merged with US mobility/delivery peers without regional adjustment.
- Future production spec should preserve SE Asia regional_context or regional subcluster treatment.

**Rationale**: Grab operates across Southeast Asia with different market structures, regulation, consumer behavior, logistics, payments, mobility economics, and currency environments than US/EU platform peers. It is analytically useful, but only with explicit regional platform context.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION

**Conditions**:
- Future production spec must preserve SE Asia regional platform caveat.
- Peer analytics must not compare GRAB mechanically against US mobility/delivery peers without regional adjustment.
- Final production registry still requires separate spec and gate.


---

### CTX-GAP-018 — UBS

**Decision**: Comparability handling: **comparable only with post-Credit-Suisse integration caveat**.

**Peer handling**:
- UBS may remain relevant to global bank / wealth management peer analysis.
- UBS must carry an explicit Credit Suisse integration and structural-break caveat.
- Pre-integration and post-integration data must not be mixed mechanically without adjustment.

**Rationale**: UBS remains a major global financial institution and wealth-management peer, but the Credit Suisse acquisition created a structural comparability break. For MoneyHorst, UBS can be included only with an explicit integration-period caveat and historical data adjustment discipline.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION

**Conditions**:
- Future production spec must preserve post-Credit-Suisse integration caveat.
- Peer analytics must distinguish pre-acquisition and post-acquisition comparability.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-019 — PGF-09 ETF Membership

**Decision**: ETF membership population must be **deferred until approved production data feeds exist**.

**Peer handling**:
- Do not manually finalize individual ETF membership in PGF-09.
- PGF-09 ETF/fund membership must depend on approved production data feeds and methodology fields.
- Required fields include at minimum: AUM, TER/fees, holdings date, holdings composition, benchmark methodology, issuer, domicile, liquidity/spread, replication method, and fund structure.
- Use Asset Type and Analyst Sentiment Guidance for ETF/fund asset-type handling.

**Rationale**: ETF/fund products require data provenance, holdings freshness, fee structure, benchmark methodology, replication method, liquidity, domicile, and look-through exposure. Manual finalization would create methodology risk and stale registry risk. For MoneyHorst, PGF-09 must be deferred until production-grade data sources and asset-type rules exist.

**Decision status**: DEFER_WITH_PRODUCTION_DATA_REQUIREMENT

**Conditions**:
- Future production spec must not manually finalize PGF-09 ETF membership.
- Future production spec must define approved ETF/fund data feeds before registry population.
- Future production spec must apply `docs/README_asset_type_and_sentiment_guidance.md`.
- Final production registry still requires separate spec and gate.

---

## Production Registry Readiness Effect

| Item | Readiness Effect |
|------|-----------------|
| MELI | P4 conditionally resolved for future production-spec input with LatAm regional_context |
| STNE | P4 conditionally resolved for future production-spec input with LatAm payments/regional_context |
| GRAB | P4 conditionally resolved for future production-spec input with SE Asia regional platform_context |
| UBS | P4 conditionally resolved with post-Credit-Suisse structural-break caveat |
| PGF-09 ETF Membership | Not production-final; deferred until approved production data feeds and ETF/fund methodology exist |

---

## Review Completion Status

After this P4 record:

- **P1** Family Assignment Decisions are **complete**.
- **P2** Peer Role Decisions are **complete**.
- **P3** Subcluster Assignment Decisions are **complete**.
- **P4** Regional / Structural Decisions are **complete**.

The next step is **not** immediate production registry creation.

The next step should be a **Production Registry Readiness Review** that consolidates P1–P4 and determines whether a future Production Registry Creation Spec may be started.

---

## Explicit Non-Authorization

This document does **not** authorize:

- Production registry creation
- Canonical peer_group_id creation
- peer_group_registry.yaml creation
- Final peer assignments
- Candidate approval
- Candidate_Status mutation
- SAI usage
- Market data integration
- Trading or execution usage
- Production Registry Creation Spec start
- Automated candidate promotion

---

## Boundary Confirmations

- ✓ No production registry created
- ✓ No peer_group_registry.yaml created
- ✓ No canonical peer_group_id values minted
- ✓ No candidate records modified
- ✓ No Candidate_Status values changed
- ✓ No SAI mutation
- ✓ No runtime code created
- ✓ No validation code created
- ✓ No market data integration
- ✓ No trading or execution scope
- ✓ No production registry creation spec started
- ✓ No new spec started
- ✓ Documentation-only guidance

---

```
P4_OWNER_VERIFIED_DECISION_RECORD_READY
```

---

*End of Owner-Verified P4 Decision Record.*
