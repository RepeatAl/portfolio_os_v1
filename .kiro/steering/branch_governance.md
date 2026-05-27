# Branch Governance Policy

## inclusion: always

**Status**: MANDATORY | **Owner**: CTO | **Scope**: all-git-operations

## Core Rule

**NEVER commit or push directly to `main`.** All work MUST happen on named branches with proper prefixes.

## Required Branch Prefixes

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New functionality or capabilities | `feature/daily-report-mvp` |
| `fix/` | Bug fixes and corrections | `fix/semantic-engine-timeout` |
| `governance/` | Architecture decisions, specs, governance docs | `governance/runtime-foundation` |
| `spec/` | Spec creation and refinement | `spec/report-runtime-integrity` |
| `chore/` | Maintenance, cleanup, dependency updates | `chore/registry-cleanup` |
| `refactor/` | Code restructuring without behavior change | `refactor/report-engine-decomposition` |

## Workflow

1. **Before any work**: Create a branch from `main`
   ```bash
   git checkout main
   git pull origin main
   git checkout -b <prefix>/<descriptive-name>
   ```

2. **During work**: Commit to the branch (never to main)

3. **After work**: Push branch and create PR
   ```bash
   git push -u origin <prefix>/<descriptive-name>
   ```

4. **Merge**: Only via PR review (or explicit CTO approval for governance branches)

## Naming Conventions

- Use kebab-case: `feature/report-runtime-integrity` not `feature/reportRuntimeIntegrity`
- Be descriptive: `fix/semantic-engine-allocation-timeout` not `fix/bug`
- Keep under 50 characters after prefix

## Exceptions

- Emergency hotfixes MAY be committed directly to main with `hotfix:` commit prefix
- This requires explicit justification in the commit message

## Enforcement

- Kiro SHALL check current branch before any commit operation
- If on `main`, Kiro SHALL refuse to commit and suggest creating a branch
- This rule applies to ALL commits: code, docs, governance, specs

## Rationale

Portfolio OS uses SSOT/Domainization architecture where:
- Governance changes affect the entire system's authority model
- Runtime changes must be validated before merging
- Spec changes need review before implementation begins
- Clean git history enables institutional replayability
