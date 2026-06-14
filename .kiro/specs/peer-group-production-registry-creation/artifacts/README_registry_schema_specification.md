# README: Registry Schema Specification

> **Artifact**: registry_schema_specification.md
> **Spec**: peer-group-production-registry-creation | **Task**: 2
> **Authority**: CTO / Architecture
> **Purpose**: Prevent drift between schema specification and registry creation

---

## What This Artifact Defines

The `registry_schema_specification.md` defines the **complete schema** for the future `peer_group_registry.yaml` file. It documents:

- All field names, types, constraints, and default values
- The YAML structure (root metadata, family sections, record format)
- Multi-segment representation model (4 context layers)
- Regional context field structure
- Structural break caveat field structure
- Dependency relationships array structure with all governed types
- Authority and approval fields
- Source traceability fields
- Confidence and evidence fields
- Prohibited fields that must NEVER appear in the schema

---

## What This Artifact Does NOT Do

| This artifact does NOT... | Because... |
|---------------------------|-----------|
| Create `peer_group_registry.yaml` | Registry creation requires Human_Approval_Gate passage |
| Mint any `peer_group_id` values | ID minting requires Stage 3 approval |
| Approve any candidate records | Approval requires explicit CTO governance |
| Implement validation code | This is a documentation-only spec |
| Define runtime behavior | Runtime belongs to future implementation |
| Create APIs or data pipelines | Implementation requires separate approval |

---

## Multi-Segment Representation Purpose (AMZN Use Case)

Complex businesses like Amazon operate across multiple material segments:
- **Cloud/AI Infrastructure** (AWS)
- **Retail / Marketplace**
- **Logistics**
- **Advertising**

Forcing AMZN into a single subcluster assignment would destroy analytical information. The multi-segment representation model provides four context layers:

1. **primary_context** — The primary analytical frame (Cloud/AI for AMZN)
2. **secondary_context** — Material secondary segments (Retail, Marketplace, Logistics, Advertising)
3. **dependency_context** — External dependencies shaping the asset's profile
4. **benchmark_context** — Reference frame for comparability (Hyperscaler peers)

This model preserves the analytical distinction between primary AI-relevance and material secondary segments as required by P3 decisions (R15.4).

**If multi-segment representation cannot be confirmed**, AMZN is assigned `lifecycle_state: CONTEXT_ONLY` until schema capability is verified (R15.3).

---

## Regional Context Purpose (MELI, STNE, GRAB)

Assets operating in non-US/EU markets carry structural comparability caveats:

| Asset | Region | Why |
|-------|--------|-----|
| MELI (MercadoLibre) | LATAM | LatAm e-commerce/marketplace cannot be mechanically compared to US/EU peers without regional adjustment |
| STNE (StoneCo) | LATAM_BR | Brazilian payments infrastructure cannot be mechanically compared to US/EU payments networks |
| GRAB (Grab Holdings) | SEA | SE Asian super-app platform cannot be mechanically merged with US mobility/delivery peers |

The `regional_context` field is a structured object carrying:
- **region**: Geographic identifier
- **caveat**: Human-readable comparability limitation
- **prohibition**: Boolean flag — if true, cross-region mechanical comparison is prohibited without explicit adjustment

**Once assigned, regional_context may NEVER be silently removed or cleared** (R16.4).

---

## Structural Break Caveat Purpose (GEV, UBS)

Assets with post-merger, spin-off, or integration-period events carry comparability limitations that prevent overstating historical data continuity:

| Asset | Event | Impact |
|-------|-------|--------|
| GEV (GE Vernova) | Spin-off from GE (April 2024) | Limited standalone operating history — historical comparability must not be overstated |
| UBS | Acquisition of Credit Suisse (June 2023) | Integration period — must distinguish between pre-acquisition and post-acquisition comparability data |

The `structural_break_caveat` field documents:
- **type**: Event type (SPINOFF, ACQUISITION, MERGER, RESTRUCTURING)
- **entity**: Related entity
- **date**: Event date
- **note**: Comparability limitation description

**Once assigned, structural_break_caveat may NEVER be silently removed or cleared.**

---

## Critical Governance Statement

**Creating `peer_group_registry.yaml` from this schema specification requires:**

1. Human_Approval_Gate Stage 2 (Schema Finalization Approval) — CTO must explicitly approve the finalized schema
2. Human_Approval_Gate Stage 3 (Canonical ID Minting Authorization) — CTO must authorize ID minting
3. Human_Approval_Gate Stage 4 (Production Registry Activation) — CTO must authorize registry creation
4. Verification Gate VG-PGRC-PRODUCTION-1 must PASS with zero violations

**No automated process may create the production registry.** The schema specification is a reference document — NOT an execution authorization.

---

## Controlling Sources

| Source | Role |
|--------|------|
| Design.md Section 7 | Registry Schema Model definition |
| Design.md Section 11 | Conditional Caveat Encoding Model |
| Design.md Section 12 | Dependency Relationship Model |
| Design.md Section 19 | Confidence and Evidence Model |
| Requirements R1 | Production Registry Schema Definition |
| Requirements R15 | Multi-Segment Representation |
| Requirements R16 | Regional Comparability Preservation |
| PGMF | Sole methodology authority for field rules |

---

## Authority vs Lifecycle — Critical Distinction

The schema defines two independent fields that must never be conflated:

| Field | Describes | Governs |
|-------|-----------|---------|
| `production_authority` | **Governance authorization** | Whether the record has passed the Human_Approval_Gate |
| `lifecycle_state` | **Operational lifecycle** | The current functional state of the record in the registry |

**Key rules:**

- `production_authority: HUMAN_CTO_APPROVED` is valid ONLY for records that have passed the Human_Approval_Gate and are authorized for production activation.
- `production_authority: NONE` applies to candidate, deferred, context-only, or pre-production documentation records.
- A record with `lifecycle_state: DEFERRED` or `lifecycle_state: CONTEXT_ONLY` must NOT be treated as a production-approved peer assignment unless and until explicit Human/CTO approval changes its authority state.
- Verification Gate VG-PGRC-PRODUCTION-1 must FAIL if any deferred/context-only record is silently promoted to `HUMAN_CTO_APPROVED` without documented approval evidence.

---

## Agent Drift Prevention

Future agents reading this README must understand:

1. **Schema ≠ Registry**: The schema specification defines structure. The registry is the instantiation. They are separate artifacts with separate approval requirements.
2. **Specification ≠ Authorization**: Defining how the registry SHOULD look does not authorize creating it.
3. **No premature creation**: Even if the schema is complete and correct, the registry cannot be created without explicit Human_Approval_Gate passage at Stages 2, 3, and 4.
4. **No field invention**: Only fields defined in this specification may appear in the registry. Adding fields requires governance proposal and CTO approval.
5. **No prohibited fields**: The Prohibited Fields Table (Section 11 of the specification) is absolute. Any prohibited field appearing in registry artifacts triggers verification gate failure.
6. **Authority ≠ Lifecycle**: A record's `lifecycle_state` (DEFERRED, CONTEXT_ONLY) does not imply production authorization. Only `production_authority: HUMAN_CTO_APPROVED` with documented approval evidence grants production status.

---

```
README_REGISTRY_SCHEMA_SPECIFICATION_COMPLETE
```

---

*End of README.*
