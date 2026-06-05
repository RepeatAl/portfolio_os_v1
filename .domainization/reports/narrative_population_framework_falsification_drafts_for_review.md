# Narrative Population Framework — Falsification Condition Drafts for Human Review

**Date**: 2026-06-04 (revised)
**Spec**: narrative-population-framework
**Task**: 3.1
**Status**: PENDING HUMAN APPROVAL (conditions hardened)
**Revision**: v2 — hardened falsification conditions

---

## Purpose

This document presents the hardened draft falsification conditions for all 3 Wave 1 narrative candidates. Each condition requires explicit human approval before registry mutation can proceed.

**Registry mutation is BLOCKED until all 3 conditions below are approved by the Portfolio Architect (human).**

---

## Candidate 1: AI Infrastructure

| Field | Value |
|-------|-------|
| Proposed ID | `narrative.ai_infrastructure` |
| Display Name | AI Infrastructure |
| Logic Type | TWO-OF-FOUR |
| Human Approval Status | **⏳ PENDING HUMAN APPROVAL** |

### Falsification Condition (DRAFT — HARDENED)

The narrative is falsified if at least TWO of the following occur within a 12-month period:

1. The defined hyperscaler cohort reduces AI/data-center capex guidance by more than 30% YoY.
2. Data-center construction starts or committed capacity additions decline by more than 40% YoY.
3. AI accelerator / GPU / networking order backlog or lead-time indicators materially normalize, showing demand is no longer capacity-constrained.
4. Major hyperscalers explicitly state that AI infrastructure buildout is entering a digestion or overcapacity phase rather than expansion.

The hyperscaler cohort must be explicitly defined before registry mutation.

### Rationale

Avoids over-reliance on one capex metric and prevents false non-falsification. Requires convergence of multiple independent indicators rather than a single data point that could be noisy or temporary.

---

## Candidate 2: Defense Rearmament

| Field | Value |
|-------|-------|
| Proposed ID | `narrative.defense_rearmament` |
| Display Name | Defense Rearmament |
| Logic Type | BOTH |
| Human Approval Status | **⏳ PENDING HUMAN APPROVAL** |

### Falsification Condition (DRAFT — HARDENED)

The narrative is falsified if BOTH occur:

1. NATO/allied defense spending commitments are formally reduced, delayed, or materially deprioritized across the core allied spending cohort.
2. Actual defense procurement indicators weaken materially for at least 12 months, shown by falling defense budget authorizations, cancelled procurement programs, declining order intake/backlog among major defense contractors, or official de-escalation removing the structural rearmament rationale.

The condition must distinguish temporary political noise from actual procurement-cycle reversal.

### Rationale

Avoids dependence on a single numeric NATO target and requires observable procurement reversal. Political rhetoric alone does not falsify; actual spending and order behavior must confirm.

---

## Candidate 3: GLP-1 / Obesity Medicine

| Field | Value |
|-------|-------|
| Proposed ID | `narrative.glp1_obesity_medicine` |
| Display Name | GLP-1 / Obesity Medicine |
| Logic Type | ANY-OF-THREE |
| Human Approval Status | **⏳ PENDING HUMAN APPROVAL** |

### Falsification Condition (DRAFT — HARDENED)

The narrative is falsified if ANY of the following occur:

1. A major regulator such as FDA or EMA materially restricts GLP-1 usage for obesity or metabolic disease due to safety concerns.
2. Robust long-term clinical evidence shows materially impaired efficacy, unacceptable safety risk, or poor treatment durability.
3. Payor coverage or reimbursement restrictions materially reduce addressable adoption despite clinical efficacy, causing the market expansion thesis to fail.

This does not falsify the science alone; it falsifies the investable obesity-medicine expansion narrative.

### Rationale

Incorporates regulatory, clinical, and adoption/access failure paths. Recognizes that a narrative can fail not only from scientific failure but from market access barriers that prevent the thesis from playing out economically.

---

## Approval Instructions

To approve these falsification conditions, the human reviewer should:

1. Review each condition for clarity, testability, and completeness
2. Confirm each condition would genuinely falsify the narrative if met
3. Confirm the logical operators (TWO-OF-FOUR / BOTH / ANY-OF-THREE) are appropriate
4. Confirm the scope (12-month observation window, cohort definitions) is appropriate
5. Provide explicit approval for each candidate individually

**Approval format**: Explicit written confirmation per candidate (e.g., "AI Infrastructure falsification condition: APPROVED")

**After approval**: Execution may proceed to Wave 4 (Pre-Mutation Verification Gates) and eventually Wave 5 (Registry Append).

---

## Summary Table

| Candidate | Logic Type | Conditions | Status |
|-----------|-----------|------------|--------|
| AI Infrastructure | TWO-OF-FOUR | Capex reduction + construction decline + demand normalization + overcapacity statement | ⏳ PENDING |
| Defense Rearmament | BOTH | Spending commitment reversal + procurement indicator weakening (12 months) | ⏳ PENDING |
| GLP-1 / Obesity Medicine | ANY-OF-THREE | Regulatory restriction + clinical failure + payor/adoption failure | ⏳ PENDING |
