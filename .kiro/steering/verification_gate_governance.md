# Verification Gate Governance

## inclusion: always

**Status**: MANDATORY | **Owner**: CTO | **Scope**: all-task-execution

## Core Rule

**Verification tasks are NOT implementation parent tasks.** They are independent gates that MUST be explicitly executed, never auto-completed, auto-inferred, or child-derived.

## Problem Statement

When a DAG-based task system auto-completes parent tasks upon child completion, verification checkpoints (e.g., "Phase X Output Contract Verification") get silently skipped. This produces "green architecture hallucinations" — the system reports success without actually running the verification.

## Rules

### 1. Verification Gates MUST Be Explicitly Executed

A verification task requires:
- Running the full test suite (not individual test files)
- Producing explicit pass/fail output with metrics
- Creating a verification artifact (document with evidence)
- Human-visible confirmation of the gate passing

### 2. Verification Gates MUST NOT Be

| Forbidden | Why |
|-----------|-----|
| Auto-skipped | Skipping verification = unverified architecture |
| Auto-inferred | "Tests passed during subtasks" ≠ integration verification |
| Child-derived | Parent completion ≠ contract verification |
| Implicitly satisfied | Explicit evidence required |

### 3. Verification Gate Checklist

Every verification task MUST produce:

```
1. Full integration test run (pytest tests/ runtime/ engines/ -v)
2. Explicit metrics: total, passed, failed, skipped, warnings, runtime
3. Interface verification script (importability, cross-module compat)
4. Additive-only confirmation (no breaking changes)
5. Verification artifact document (phase_X_output_contract_verification.md)
```

### 4. DAG Behavior

When the orchestrator encounters a verification task:
- It MUST NOT auto-complete it when sibling tasks finish
- It MUST dispatch it as a real task to a subagent
- The subagent MUST run the full test suite and produce evidence
- Only explicit test passage + artifact creation = completion

### 5. Identification

Verification tasks are identified by:
- Task name contains "Verification" or "Contract Verification"
- Task name contains "Output Contract"
- Task description mentions "verify all outputs meet"
- Task is a phase-ending checkpoint (e.g., "Phase X Output Contract Verification")

## Rationale

Without explicit verification gates:
- Integration failures hide behind passing unit tests
- Cross-module incompatibilities go undetected
- "All green" status becomes meaningless
- Architecture decisions are never validated end-to-end
- Technical debt accumulates invisibly

## Enforcement

- Kiro SHALL treat verification tasks as leaf tasks requiring explicit execution
- Kiro SHALL NOT mark verification tasks complete based on child task completion
- Kiro SHALL produce a verification artifact for every verification gate
- If a verification gate fails, Kiro SHALL stop and report to the user
