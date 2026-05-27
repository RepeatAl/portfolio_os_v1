# Hardening: Verification Gates as First-Class Entities

**Priority:** CRITICAL  
**Category:** governance/task-execution  
**Owner:** CTO  
**Created:** 2026-05-27  
**Status:** PARTIALLY ADDRESSED  

## Problem

The DAG-based task execution system auto-completed Task 9 (Phase C Output Contract Verification) when all child implementation tasks finished. This produced a "green architecture hallucination" — the system reported Phase C as verified without actually running the verification.

This was manually corrected, and a steering rule was created (`verification_gate_governance.md`). However, the task system itself does not yet enforce this distinction structurally.

## What Was Done (Phase C)

- [x] Steering rule created: `.kiro/steering/verification_gate_governance.md`
- [x] Task 9 explicitly executed with full test suite
- [x] Verification artifact produced: `phase_c_output_contract_verification.md`
- [x] Task status manually corrected from `[~]` to `[x]`

## What Still Needs to Happen

### 1. Task Model Extension

Verification tasks need a structural marker in `tasks.md` that prevents auto-completion:

```markdown
- [ ] 9. Phase C Output Contract Verification  <!-- type: verification-gate -->
```

Or a metadata annotation in `.meta.json` that the task system respects.

### 2. DAG Behavior Change

When the orchestrator encounters a verification gate:
- It MUST NOT auto-complete it when sibling/child tasks finish
- It MUST dispatch it as a real task to a subagent
- The subagent MUST run the full test suite and produce evidence
- Only explicit test passage + artifact creation = completion

### 3. Verification Gate Contract

Every verification gate MUST produce:
1. Full integration test run (`pytest tests/ runtime/ engines/ -v`)
2. Explicit metrics: total, passed, failed, skipped, warnings, runtime
3. Interface verification script (importability, cross-module compat)
4. Additive-only confirmation (no breaking changes)
5. Verification artifact document (`phase_X_output_contract_verification.md`)

### 4. Future Phases

Phase D has its own verification gate (Task 12). It MUST:
- Be explicitly executed (not auto-completed)
- Produce its own verification artifact
- Include the provenance serialization fix verification
- Include warning budget compliance check

## Acceptance Criteria

- [ ] Task system structurally distinguishes verification gates from implementation tasks
- [ ] Verification gates cannot auto-complete from child task completion
- [ ] Phase D verification gate (Task 12) is explicitly executed with artifact
- [ ] Steering rule is respected by all future task executions

## Risk If Not Addressed

Without structural enforcement:
- Every future phase verification gate will be silently skipped
- "All green" status becomes meaningless
- Architecture decisions are never validated end-to-end
- Technical debt accumulates invisibly behind false confidence
