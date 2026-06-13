# Owner-Verified P3 Decision Record — Peer Group Registry Preflight

> **Scope**: Owner-verified P3 subcluster decision record
> **production_authority**: NONE
> **registry_creation_authority**: NONE
> **candidate_approval_authority**: NONE
> **decision_authority**: OWNER_VERIFIED_REVIEW_DECISION
> **Status**: P3_OWNER_VERIFIED_DECISION_RECORD_READY

---

## Purpose

This document records owner-verified P3 subcluster assignment decisions for five unresolved subcluster context observations identified during the completed Peer Group Registry Creation Preflight.

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

1. **MoneyHorst scope alignment** — classifying subcluster fit for portfolio intelligence and decision governance
2. **Institutional subcluster comparability** — which assets belong together for comparative analysis
3. **Avoidance of forcing multi-segment businesses into a single simplistic category** — complex businesses need multi-context handling
4. **Separation of primary_subcluster from secondary_context and dependency_context** — each layer has distinct analytical meaning
5. **Production-readiness discipline** — ensuring decisions are structurally sound before production use
6. **MoneyHorst taxonomy distinction** between asset class, instrument, investment style, factor, method, asset allocation, strategy, and system layer

MoneyHorst is not deciding based on whether an asset is "Growth", "Value", "Quant", or simply a "stock". MoneyHorst is classifying subcluster fit for future portfolio intelligence and decision governance.

**Reference**: `docs/moneyhorst/investment_style_method_taxonomy_ssot.md`

---

## P3 Decision Summary Table

| Gap ID | Asset | Owner-Verified Decision | Status | Production Spec Effect |
|--------|-------|------------------------|--------|------------------------|
| CTX-GAP-001 | AVGO | Primary subcluster = AI Silicon / AI Acceleration; Networking/Connectivity retained as secondary_context | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may model AVGO with AI Silicon primary and connectivity context |
| CTX-GAP-002 | MU | Primary subcluster = Memory / Storage; AI Silicon retained as dependency/AI-demand context | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may model MU as memory/storage infrastructure rather than AI silicon peer |
| CTX-GAP-008 | AXP | Subcluster = Hybrid Payments / Closed-loop / Charge-card model | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec must not treat AXP as identical to pure card networks |
| CTX-GAP-011 | UBER | Primary subcluster = Mobility; Delivery / Local Commerce retained as secondary_context | APPROVE_FOR_PRODUCTION_SPEC_INPUT | Future production spec may model UBER with mobility primary and delivery context |
| CTX-GAP-014 | AMZN | Multi-segment context required; Cloud/AI Infrastructure primary for AI relevance, Retail/Logistics retained as context | APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION | Future production spec must not force AMZN into one simplistic subcluster without multi-segment handling |

---

## Individual Decision Records

### CTX-GAP-001 — AVGO

**Decision**: Primary subcluster: **AI Silicon / AI Acceleration**. Secondary context: Networking / Connectivity.

**Subcluster handling**:
- AVGO may be modeled with AI Silicon / AI Acceleration as primary subcluster for future production-spec input.
- Networking/connectivity must be preserved as secondary_context because it is material to Broadcom's business and AI infrastructure relevance.
- Do not collapse AVGO into only legacy networking/connectivity.

**Rationale**: Broadcom is materially relevant to AI infrastructure through custom silicon, accelerator-adjacent components, and networking/connectivity for AI data-center architectures. For MoneyHorst, AI Silicon / AI Acceleration is the primary analytical frame, while networking/connectivity remains essential context.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve networking/connectivity secondary_context.
- Future production spec must not compare AVGO mechanically to pure GPU/accelerator companies without context adjustment.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-002 — MU

**Decision**: Primary subcluster: **Memory / Storage**. Secondary context: AI-demand infrastructure context.

**Subcluster handling**:
- MU should not be classified as AI Silicon primary.
- MU should be modeled as Memory / Storage infrastructure exposed to AI demand.
- AI-related demand should be retained as dependency_context or demand_context.

**Rationale**: Micron is central to AI infrastructure through memory demand, HBM, DRAM, NAND, and data-center workloads. But it is not primarily an AI accelerator or AI silicon designer in the same sense as AI compute leaders. Memory / Storage is the cleaner institutional subcluster.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve AI-demand context.
- Future production spec must not classify MU as pure AI accelerator peer.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-008 — AXP

**Decision**: Subcluster: **Hybrid Payments / Closed-loop / Charge-card model**.

**Subcluster handling**:
- AXP should be modeled separately from pure open-loop card networks.
- AXP may remain in the payments family but must carry closed-loop/credit/charge-card comparability caveat.
- Do not compare AXP mechanically to Visa/Mastercard without business-model adjustment.

**Rationale**: American Express is a payments company, but its closed-loop network, issuing model, charge-card economics, customer base, credit exposure, and merchant discount structure differ materially from pure card networks. It requires a hybrid payments subcluster.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve closed-loop/credit exposure caveat.
- Future production spec must not treat AXP as equivalent to V/MA without adjustment.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-011 — UBER

**Decision**: Primary subcluster: **Mobility**. Secondary context: Delivery / Local Commerce.

**Subcluster handling**:
- UBER should be modeled with Mobility as primary subcluster.
- Delivery / Local Commerce should remain secondary_context.
- Do not dual-classify UBER as two separate primary subclusters.

**Rationale**: Uber's identity remains anchored in mobility and ride-hailing marketplace economics, even though delivery/local commerce is strategically important. For MoneyHorst, Mobility is the primary peer frame; Delivery remains secondary context.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT

**Conditions**:
- Future production spec must preserve Delivery / Local Commerce secondary_context.
- Future production spec must avoid silent duplicate primary-subcluster assignment.
- Final production registry still requires separate spec and gate.

---

### CTX-GAP-014 — AMZN

**Decision**: Multi-segment context required. Primary AI-relevance frame: **Cloud / AI Infrastructure**. Secondary contexts: Retail, Marketplace, Logistics, Advertising.

**Subcluster handling**:
- AMZN should not be forced into one simplistic subcluster.
- For AI infrastructure analysis, AWS / Cloud / AI Infrastructure should be the primary relevance frame.
- Retail, marketplace, logistics, and advertising must remain material segment contexts.
- Future production spec must explicitly represent AMZN as a multi-segment comparability case.

**Rationale**: Amazon is a multi-segment platform whose AI relevance is primarily driven by AWS and cloud/AI infrastructure, but whose total business comparability is shaped by retail, marketplace, logistics, advertising, and consumer demand. For MoneyHorst, forcing AMZN into a single subcluster would reduce analytical quality.

**Decision status**: APPROVE_FOR_PRODUCTION_SPEC_INPUT_WITH_CONDITION

**Conditions**:
- Future production spec must preserve multi-segment context.
- AMZN must not be treated as a pure retailer, pure cloud company, or pure logistics company without explicit segment framing.
- If the production registry cannot represent multi-segment context, AMZN must remain context/benchmark until such representation exists.
- Final production registry still requires separate spec and gate.


---

## Production Registry Readiness Effect

| Item | Readiness Effect |
|------|-----------------|
| AVGO | P3 resolved for future production-spec input as AI Silicon primary with networking/connectivity secondary context |
| MU | P3 resolved for future production-spec input as Memory / Storage primary with AI-demand context |
| AXP | P3 resolved for future production-spec input as Hybrid Payments / Closed-loop / Charge-card model |
| UBER | P3 resolved for future production-spec input as Mobility primary with Delivery / Local Commerce secondary context |
| AMZN | P3 conditionally resolved for future production-spec input requiring multi-segment context handling |

---

## Remaining Review After P3

After this P3 record, the following review layer remains:

**P4 Regional / Structural Observations**:
- MELI
- STNE
- GRAB
- UBS
- PGF-09 ETF membership population

This artifact does not execute P4 decisions.

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
P3_OWNER_VERIFIED_DECISION_RECORD_READY
```

---

*End of Owner-Verified P3 Decision Record.*
