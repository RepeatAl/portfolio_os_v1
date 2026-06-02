# Commit Governance Rules

## inclusion: always

**Status**: MANDATORY | **Owner**: CTO | **Scope**: all-commits

## Format

`<type>(<scope>): <description>`

Valid types: `feat`, `fix`, `chore`, `docs`, `infra`, `ci`, `test`, `refactor`

## Core Rules

1. One commit = one logical change (single intent)
2. One domain per commit (governance, vc, labib, deploy, etc.)
3. Governance/CI/product changes in separate commits
4. Domain-map updates never mixed with product code
5. Cross-domain changes require explicit `refactor(cross-domain):` prefix

## Enforcement

- Hook: `.kiro/hooks/commit-prefix-validator.json`
- Pre-commit: domain naming guard, Prettier, ESLint
- Violations: CRITICAL (mixed domains) = revert; MEDIUM (wrong prefix) = amend

## References

- `.kiro/steering/execution-governance-baseline.md`
- `.kiro/steering/file_writing_staregy.md`<!------------------------------------------------------------------------------------
   Add Rules to this file or a short description and have Kiro refine them for you:   
-------------------------------------------------------------------------------------> 