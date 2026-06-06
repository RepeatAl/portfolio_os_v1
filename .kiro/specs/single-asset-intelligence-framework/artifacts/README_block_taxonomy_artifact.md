# README: Block Taxonomy Artifact (Task 1)

**Artifact**: `block_taxonomy.md`
**Task**: 1.1 Create block taxonomy document
**Status**: Completed
**Date**: 2026-06-06
**Authority**: ARCH
**Layer**: Definition — No implementation code

---

## What This Artifact Is

The Block Taxonomy is the foundational definition artifact for the Single Asset Intelligence (SAI) Framework. It defines the complete set of 24 canonical analysis blocks that organize all asset-level evidence interpretation.

Each block is a discrete diagnostic dimension — it tells you what evidence to look at, how to interpret it, and what conditions constitute red flags. Nothing more.

---

## What This Artifact Is NOT

- Not implementation code
- Not a scoring system
- Not a ranking methodology
- Not an allocation engine
- Not a recommendation framework
- Not executable architecture

---

## How to Read This Artifact

### Block Definitions (Sections 4–12)

Each block is defined with 12 fields:

| Field | What It Tells You |
|-------|-------------------|
| `block_id` | Stable identifier (SAI-BLK-01 through SAI-BLK-24) — immutable once assigned |
| `block_name` | Human-readable name |
| `category` | Organizational grouping (Foundation, Operational, Financial Stability, Risk, Earnings, Valuation, Market Position, Outlook, Portfolio Context) |
| `purpose` | One-sentence explanation of what this block diagnoses |
| `fact_families` | Which fact categories from Market Evidence Framework this block consumes |
| `signal_families` | Which signal categories this block consumes |
| `temporal_resolution` | How frequently evidence must refresh (quarterly/monthly/daily/real-time) |
| `output_type` | Always "Diagnostic interpretation" — never a score or recommendation |
| `provenance_requirement` | What source evidence must be cited for any interpretation |
| `red_flag_requirement` | Warning conditions with evidence thresholds (minimum 2 per block) |
| `deferred_dependencies` | External frameworks not yet available that this block will eventually consume |
| `non_scoring_boundary` | Explicit statement that this block does NOT produce scores/recommendations |

### Extension Mechanism (Section 13)

Documents how the taxonomy grows over time:
- New blocks get SAI-BLK-25+ (identifiers never reused)
- Existing blocks cannot be removed, renamed, or modified
- Extension proposal template defines what's required to add a block

### Deferred Dependencies (Section 14)

Lists external frameworks that SAI blocks reference but which do not yet exist:
- Earnings Intelligence Framework
- Valuation Framework
- Peer Group Registry
- Correlation/Dependency Framework
- Portfolio Health Framework

---

## Block Categories at a Glance

| Category | Blocks | What They Cover |
|----------|--------|-----------------|
| Foundation | SAI-BLK-01, 02 | Identity and business model |
| Operational | SAI-BLK-03, 04, 05, 06, 11, 14 | Revenue, demand, margins, cashflow, working capital, pricing |
| Financial Stability | SAI-BLK-07, 08, 09, 10 | Balance sheet, credit, hidden liabilities, pensions |
| Risk | SAI-BLK-12, 13 | Customer concentration, supply chain |
| Earnings | SAI-BLK-15, 16 | Earnings quality, guidance/estimates |
| Valuation | SAI-BLK-17, 18 | Valuation context, value trap guard |
| Market Position | SAI-BLK-19, 20, 21 | Relative strength, correlation, peer comparison |
| Outlook | SAI-BLK-22, 23 | Company outlook, asset-class outlook |
| Portfolio Context | SAI-BLK-24 | Portfolio fit |

---

## Verification Gates

This artifact provides evidence for two verification gates (execution pending in Task 15):

| Gate | What It Checks | Status |
|------|----------------|--------|
| VG-SAI-1 | All 24 blocks defined with stable IDs, categories, purposes | Evidence provided — gate execution pending |
| VG-SAI-5 | Block IDs frozen, extension mechanism documented, no block removal | Evidence provided — gate execution pending |

Gate execution requires separate gate artifacts with explicit PASS/FAIL determination. This artifact is evidence, not the gate itself.

---

## Requirements Traceability

| Requirement | Coverage |
|-------------|----------|
| SAI-REQ-1 (Canonical Analysis Block Taxonomy) | All 24 blocks defined with required fields |
| SAI-REQ-14 (Additive-Only Extension Mechanism) | Extension rules, immutability, backward compatibility, proposal template |

---

## Key Principles to Remember

1. **SAI interprets evidence. It does not prescribe action.**
2. **Every interpretation must trace to specific facts/signals (no orphan claims).**
3. **Blocks are independent — no block requires another block's output.**
4. **The taxonomy is additive-only — blocks cannot be removed or reassigned.**
5. **Red flags are categorical (informational/elevated/critical) — never numeric scores.**

---

## Related Documents

- `design.md` — Full SAI architecture and component design
- `requirements.md` — SAI-REQ-1, SAI-REQ-14
- `single_asset_intelligence_framework_preflight_2026-06-05.md` — Preflight analysis
- Downstream artifacts (Task 2+): fact consumption matrix, signal consumption matrix, output object spec, provenance contract, etc.

---

*Generated: 2026-06-06 | Authority: ARCH | Definition Layer Only*
