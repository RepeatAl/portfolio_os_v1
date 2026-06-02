"""Provenance Schema for Portfolio OS report sections.

Defines the structure of provenance metadata for daily report sections.
Canonical provenance truth exists as a sidecar YAML file independent of
markdown rendering. Markdown-embedded provenance is informational only.

Validates: Requirements 13.1, 13.3, 13.5
"""

from dataclasses import dataclass, field, asdict
import json
import os

import yaml


@dataclass
class SectionProvenance:
    """Provenance metadata for a single report section.

    Tracks which Reasoning Objects, Semantic States, and Signal Engines
    contributed to a section's content, along with completeness state
    and any unavailable layers.
    """

    section_name: str
    reasoning_object_ids: list[str]
    semantic_state_ids: list[str]
    signal_engine_ids: list[str]
    completeness_state: str
    unavailable_layers: list[dict] = field(default_factory=list)
    schema_version: str = "1.0.0"

    def to_yaml(self) -> str:
        """Serialize to YAML for sidecar file and optional markdown embedding.

        Returns:
            YAML string representation of this section's provenance.
        """
        data = asdict(self)
        # Sort identifier lists for deterministic output
        data["reasoning_object_ids"] = sorted(data["reasoning_object_ids"])
        data["semantic_state_ids"] = sorted(data["semantic_state_ids"])
        data["signal_engine_ids"] = sorted(data["signal_engine_ids"])
        return yaml.safe_dump(data, default_flow_style=False, sort_keys=True)

    def to_json(self) -> str:
        """Serialize to JSON for sidecar file and optional markdown embedding.

        Returns:
            JSON string representation of this section's provenance.
        """
        data = asdict(self)
        return json.dumps(data, indent=2)


@dataclass
class ReportProvenance:
    """Full provenance for an entire daily report.

    Persisted as a canonical sidecar file (<run_id>_provenance.yaml).
    This is the canonical provenance truth, not the markdown embedding.
    """

    run_context_id: str
    timestamp: str
    sections: list[SectionProvenance]
    schema_version: str = "1.0.0"

    def persist(self, output_dir: str) -> str:
        """Write canonical provenance as <run_id>_provenance.yaml sidecar file.

        This is the canonical provenance truth, not the markdown embedding.

        Args:
            output_dir: Directory path where the sidecar file will be written.

        Returns:
            Absolute file path of the written provenance sidecar file.
        """
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(
            output_dir, f"{self.run_context_id}_provenance.yaml"
        )
        data = {
            "run_context_id": self.run_context_id,
            "timestamp": self.timestamp,
            "schema_version": self.schema_version,
            "sections": [
                {
                    **asdict(section),
                    "reasoning_object_ids": sorted(section.reasoning_object_ids),
                    "semantic_state_ids": sorted(section.semantic_state_ids),
                    "signal_engine_ids": sorted(section.signal_engine_ids),
                }
                for section in self.sections
            ],
        }
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=True)
        return file_path

    def embed_in_markdown(self, section_name: str) -> str:
        """Generate human-readable provenance snippet for markdown embedding.

        Returns a fenced YAML code block for the specified section.
        This is informational only — canonical truth lives in the sidecar file.

        Args:
            section_name: Name of the section to generate provenance for.

        Returns:
            A fenced code block (```yaml ... ```) containing the section's
            provenance metadata, or an empty string if the section is not found.
        """
        for section in self.sections:
            if section.section_name == section_name:
                yaml_content = section.to_yaml()
                return f"```yaml\n{yaml_content}```"
        return ""
