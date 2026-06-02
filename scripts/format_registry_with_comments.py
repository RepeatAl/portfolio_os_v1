"""
Reformats artifact_registry.yaml with proper header comments and section organization.
"""

import yaml
import sys
from pathlib import Path

REGISTRY_PATH = Path(".domainization/artifact_registry.yaml")

HEADER = """# Artifact Registry
# Central index of all artifacts in Portfolio OS with metadata
#
# This file tracks artifacts that cannot embed YAML frontmatter (non-markdown files).
# Markdown files should use YAML frontmatter instead of entries here.
#
# METADATA SCHEMA:
#
# Required Fields:
#   artifact_id: string - Unique identifier (e.g., "system_architecture_md")
#   file_path: string - Relative path from repo root (e.g., "docs/system_architecture.md")
#   primary_domain: string - Domain ID from domain_registry.yaml (e.g., "ARCH")
#   artifact_type: string - Type ID from lifecycle_state_machine.yaml (e.g., "SSOT")
#   lifecycle_status: string - Current state from state machine (e.g., "canonical")
#   created_date: string - Creation date in YYYY-MM-DD format
#   last_modified: string - Last modification date in YYYY-MM-DD format
#   owner_role: string - Responsibility description (e.g., "System architect")
#   ssot_relationship: string - One of: canonical, derived, implementation, none
#   allowed_writers: list[string] - Domain IDs with write permission
#   allowed_readers: list[string] - Domain IDs with read permission (use "ALL" for public)
#
# Optional Fields:
#   secondary_domains: list[string] - Additional domain associations
#   dependencies: list[string] - Artifact IDs this depends on
#   topic: string - Topic for SSOT conflict detection
#   description: string - Human-readable description
#   tags: list[string] - Categorization tags
#   report_value: object - Report value metadata (category + justification)
#
# Deprecation Governance Fields (HARDENING 12 — optional, for sunset lifecycle):
#   deprecated_date: string - ISO 8601 date when artifact was deprecated
#   sunset_date: string - ISO 8601 date after which artifact stops being generated
#   replacement_artifact: string - artifact_id of the replacement artifact
#   deprecation_reason: string - Reason for deprecation (max 200 chars)
#   compatibility_impact: string - One of: none, minor, breaking
#
# Report Value Categories (10 accepted):
#   semantic_interpretation, pm_reasoning, concentration_explanation,
#   dependency_explanation, scenario_interpretation, confidence_explanation,
#   action_space_clarity, multilingual_rendering, traceability, user_understanding

"""


def format_artifact(artifact, indent="  "):
    """Format a single artifact entry as YAML text."""
    lines = []
    lines.append(f"- artifact_id: {artifact['artifact_id']}")

    # Standard fields in preferred order
    field_order = [
        "file_path", "primary_domain", "artifact_type", "lifecycle_status",
        "created_date", "last_modified", "owner_role", "ssot_relationship",
        "allowed_writers", "allowed_readers", "secondary_domains",
        "metadata_source", "registry_mode", "dependencies",
        "topic", "description",
        "deprecated_date", "sunset_date", "replacement_artifact",
        "deprecation_reason", "compatibility_impact",
        "report_value", "tags",
    ]

    for field in field_order:
        if field not in artifact or field == "artifact_id":
            continue
        value = artifact[field]

        # Skip None values
        if value is None:
            continue

        if field == "report_value" and isinstance(value, dict):
            lines.append(f"{indent}report_value:")
            lines.append(f"{indent}  category: {value.get('category', '')}")
            justification = value.get('justification', '')
            lines.append(f'{indent}  justification: "{justification}"')
        elif isinstance(value, list):
            if len(value) == 0:
                lines.append(f"{indent}{field}: []")
            else:
                lines.append(f"{indent}{field}:")
                for item in value:
                    lines.append(f"{indent}  - {item}")
        elif isinstance(value, str) and ('"' in value or ':' in value or '#' in value or value.startswith('{')):
            lines.append(f'{indent}{field}: "{value}"')
        elif isinstance(value, str) and value.startswith("2026"):
            lines.append(f'{indent}{field}: "{value}"')
        elif isinstance(value, str) and '\n' in value:
            lines.append(f'{indent}{field}: "{value}"')
        else:
            lines.append(f"{indent}{field}: {value}")

    # Any remaining fields not in field_order
    for field, value in artifact.items():
        if field == "artifact_id" or field in field_order:
            continue
        if isinstance(value, list):
            lines.append(f"{indent}{field}:")
            for item in value:
                lines.append(f"{indent}  - {item}")
        else:
            lines.append(f"{indent}{field}: {value}")

    return "\n".join(lines)


def main():
    with open(REGISTRY_PATH, "r") as f:
        data = yaml.safe_load(f)

    artifacts = data.get("artifacts", [])

    # Group artifacts by section
    sections = {
        "SIGNAL GENERATION ENGINES": [],
        "SEMANTIC INTERPRETATION ENGINES": [],
        "REASONING ENGINES": [],
        "REPORT GENERATION ENGINES": [],
        "SIMULATION ENGINES": [],
        "USER INTERFACE ENGINES": [],
        "ARCHITECTURE ENGINES": [],
        "REPORT OUTPUTS": [],
        "SIGNAL OUTPUT DATA FILES (DATA_OUT)": [],
        "PORTFOLIO STATE DATA FILES": [],
        "DATA INPUT FILES": [],
        "RUNTIME ENTRY POINTS": [],
        "HISTORICAL SNAPSHOT FILES (MEMORY DOMAIN)": [],
        "CALIBRATION AND STEERING": [],
        "SSOT FRAMEWORK DOCUMENTS (mirror_only)": [],
        "RUNTIME GOVERNANCE MODULES": [],
        "GOVERNANCE MODULES": [],
        "PIPELINE AND CHAIN MODULES": [],
        "PHASE C ARTIFACTS": [],
        "PHASE D: PREVIOUSLY UNREGISTERED ARTIFACTS": [],
        "PHASE D: NEW FEATURE IMPLEMENTATION ARTIFACTS": [],
        "OTHER": [],
    }

    def classify(a):
        aid = a.get("artifact_id", "")
        fpath = a.get("file_path", "")
        atype = a.get("artifact_type", "")
        domain = a.get("primary_domain", "")
        registry_mode = a.get("registry_mode", "")

        # Phase D unregistered
        if aid in ["action_space_framework_md", "opportunity_engine_design_md",
                   "portfolio_os_domainization_steering_md", "future_framework_backlog_md",
                   "confidence_model_md", "report_pipeline_architecture_md",
                   "deployment_intelligence_framework_md", "multilingual_rendering_framework_md",
                   "trusted_signal_sources_md", "governance_stabilization_verification_md",
                   "task_1_execution_report_md", "governance_stabilization_preflight_md",
                   "governance_stabilization_audit_md"]:
            return "PHASE D: PREVIOUSLY UNREGISTERED ARTIFACTS"

        # Phase D new implementation
        if aid in ["confidence_policy_yaml", "governance_init_py", "runtime_init_py"]:
            return "PHASE D: NEW FEATURE IMPLEMENTATION ARTIFACTS"

        # Phase C
        if "phase-c" in a.get("tags", []) or "phase_c" in aid:
            return "PHASE C ARTIFACTS"

        # Sunset governance
        if aid == "sunset_governance_py":
            return "PHASE D: NEW FEATURE IMPLEMENTATION ARTIFACTS"

        # mirror_only SSOT docs
        if registry_mode == "mirror_only":
            return "SSOT FRAMEWORK DOCUMENTS (mirror_only)"

        # Runtime governance
        if fpath.startswith("runtime/") and aid not in ["deployment_matrix_py"]:
            return "RUNTIME GOVERNANCE MODULES"

        # Governance modules
        if fpath.startswith("governance/"):
            return "GOVERNANCE MODULES"

        # Pipeline orchestrator and chain validator
        if aid in ["pipeline_orchestrator_py", "deployment_matrix_py"]:
            return "PIPELINE AND CHAIN MODULES"

        # Signal engines
        if domain == "SIGNALS" and atype == "ENGINE":
            return "SIGNAL GENERATION ENGINES"

        # Semantic engines
        if domain == "SEMANTICS" and atype == "ENGINE":
            return "SEMANTIC INTERPRETATION ENGINES"

        # Reasoning engines
        if domain == "REASONING" and atype == "ENGINE":
            return "REASONING ENGINES"

        # Report engines
        if domain == "REPORT" and atype == "ENGINE":
            return "REPORT GENERATION ENGINES"

        # Simulation engines
        if domain == "SIM" and atype == "ENGINE":
            return "SIMULATION ENGINES"

        # UI engines
        if aid == "visual_engine_py":
            return "USER INTERFACE ENGINES"

        # Architecture engines
        if domain == "ARCH" and atype == "ENGINE":
            return "ARCHITECTURE ENGINES"

        # Report outputs
        if atype == "REPORT_OUT":
            return "REPORT OUTPUTS"

        # Signal data outputs
        if domain == "SIGNALS" and atype == "DATA_OUT":
            return "SIGNAL OUTPUT DATA FILES (DATA_OUT)"

        # Portfolio state
        if domain == "STATE":
            return "PORTFOLIO STATE DATA FILES"

        # Data input
        if domain == "DATA":
            return "DATA INPUT FILES"

        # Runtime entry points
        if aid in ["main_py", "app_py"]:
            return "RUNTIME ENTRY POINTS"

        # Memory/history
        if domain == "MEMORY":
            return "HISTORICAL SNAPSHOT FILES (MEMORY DOMAIN)"

        # Calibration
        if "calibration" in aid or aid == "execution_governance_baseline_md":
            return "CALIBRATION AND STEERING"

        # SSOT docs
        if aid == "system_architecture_md":
            return "SSOT FRAMEWORK DOCUMENTS (mirror_only)"

        return "OTHER"

    for a in artifacts:
        section = classify(a)
        sections[section].append(a)

    # Write output
    output = HEADER + "artifacts:\n"

    for section_name, section_artifacts in sections.items():
        if not section_artifacts:
            continue
        output += f"\n  # {'=' * 70}\n"
        output += f"  # {section_name}\n"
        output += f"  # {'=' * 70}\n\n"
        for a in section_artifacts:
            output += format_artifact(a) + "\n\n"

    with open(REGISTRY_PATH, "w") as f:
        f.write(output)

    print(f"Wrote formatted registry with {len(artifacts)} artifacts")


if __name__ == "__main__":
    main()
