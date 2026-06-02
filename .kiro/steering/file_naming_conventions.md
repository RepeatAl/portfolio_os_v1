# File Naming Conventions

## inclusion: always

**Status**: MANDATORY | **Owner**: CTO | **Scope**: all-files

## Core Principle

File names MUST be self-descriptive and indicate their purpose and content. Generic names like `README.md`, `utils.py`, or `helpers.js` are FORBIDDEN unless they are the only file in a directory.

## Rules

### 1. README Files

README files MUST include a descriptive suffix that indicates what they document:

**Format**: `README_<topic>_<scope>.md`

**Examples**:
- ✓ `README_registry_layer_python_api.md` - Documents the registry layer Python API
- ✓ `README_domainization_system.md` - Documents the domainization system
- ✓ `README_cli_tools_usage.md` - Documents CLI tools usage
- ✓ `README_deployment_guide.md` - Documents deployment procedures
- ✗ `README.md` - Too generic, what does it document?

**Exception**: A single `README.md` is allowed ONLY at the repository root level.

### 2. Generic Utility Files

Utility and helper files MUST have descriptive names:

**Examples**:
- ✓ `date_formatting_utils.py` - Date formatting utilities
- ✓ `string_validation_helpers.js` - String validation helpers
- ✓ `api_request_utils.ts` - API request utilities
- ✗ `utils.py` - What utilities?
- ✗ `helpers.js` - What helpers?
- ✗ `common.ts` - What common functionality?

### 3. Test Files

Test files MUST clearly indicate what they test:

**Format**: `test_<component_or_feature>.py`

**Examples**:
- ✓ `test_artifact_registry_ops.py` - Tests artifact registry operations
- ✓ `test_domain_validation.py` - Tests domain validation
- ✓ `test_lifecycle_transitions.py` - Tests lifecycle transitions
- ✗ `test_utils.py` - What utilities are being tested?

### 4. Configuration Files

Configuration files SHOULD indicate their scope:

**Examples**:
- ✓ `eslint.config.js` - ESLint configuration
- ✓ `pytest.ini` - Pytest configuration
- ✓ `tsconfig.json` - TypeScript configuration
- ✓ `domain_registry.yaml` - Domain registry configuration
- ✗ `config.yaml` - What configuration?

### 5. Documentation Files

Documentation files MUST indicate their content:

**Examples**:
- ✓ `architecture_decision_records.md` - Architecture decisions
- ✓ `api_reference_guide.md` - API reference
- ✓ `deployment_runbook.md` - Deployment procedures
- ✗ `docs.md` - What documentation?
- ✗ `notes.md` - What notes?

### 6. Script Files

Script files MUST indicate their purpose:

**Examples**:
- ✓ `deploy_to_production.sh` - Production deployment script
- ✓ `backup_database.py` - Database backup script
- ✓ `generate_reports.js` - Report generation script
- ✗ `script.sh` - What does it do?
- ✗ `run.py` - Run what?

## Naming Conventions by Language

### Python
- Use `snake_case` for all file names
- Module names should be short but descriptive
- Test files: `test_<module_name>.py`

### TypeScript/JavaScript
- Use `camelCase` or `kebab-case` consistently within a project
- Component files: `ComponentName.tsx` (PascalCase for React components)
- Utility files: `utilityName.ts` or `utility-name.ts`

### YAML/JSON
- Use `snake_case` or `kebab-case`
- Be explicit: `domain_registry.yaml`, not `domains.yaml`

### Markdown
- Use `snake_case` or `kebab-case`
- Be descriptive: `README_api_guide.md`, not `api.md`

## Rationale

1. **Searchability**: Descriptive names make files easier to find
2. **Indexing**: AI agents and search tools can better understand file purpose
3. **Maintenance**: Future developers immediately understand file purpose
4. **Scalability**: As projects grow, generic names create confusion
5. **Documentation**: File names serve as inline documentation

## Enforcement

- Code reviews MUST reject generic file names
- Automated linters SHOULD flag generic names where possible
- Refactoring existing generic names is encouraged but not required

## Migration Strategy

When encountering generic file names:
1. If the file is actively being modified, rename it
2. If renaming would break many imports, add a TODO comment
3. Update all references when renaming
4. Document the rename in commit messages

## Examples from Domainization Project

✓ Good naming:
- `.domainization/src/README_registry_layer_python_api.md`
- `.domainization/src/artifact_registry.py`
- `.domainization/src/test_lifecycle_manager.py`
- `.domainization/domain_registry.yaml`

✗ Bad naming (to avoid):
- `.domainization/src/README.md`
- `.domainization/src/utils.py`
- `.domainization/src/test.py`
- `.domainization/config.yaml`
