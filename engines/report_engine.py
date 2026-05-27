"""Report Engine — Chain-compliant report rendering from Reasoning Objects.

Decomposes report generation into 4 sub-components (Hardening 2):
- SectionCompletenessClassifier: classifies sections into completeness states
- ProvenanceAssembler: assembles provenance metadata per section
- SectionRenderer: renders markdown content based on completeness state
- DegradationRenderer: renders degradation notices, confidence warnings, errors

HARDENING 7 — REPORT ENGINE BOUNDARY:
ReportEngine must NOT create semantics, NOT create reasoning, NOT infer
missing conclusions. May ONLY render Reasoning_Object content and
degradation notices.

Requirements: 24.1, 24.2, 24.4, 6.1, 6.4
"""

from __future__ import annotations

import warnings
from datetime import datetime

from runtime.reasoning_object import ReasoningObject
from runtime.run_context import RunContext
from governance.provenance_schema import SectionProvenance, ReportProvenance


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CANONICAL_SECTIONS = [
    "Executive Summary",
    "Market Regime",
    "Portfolio Structure",
    "Concentration and Dependency",
    "Deployment Analysis",
    "Scenario Analysis",
    "Action Space",
    "Confidence Interpretation",
    "PM Summary",
]

# Mapping from signal categories to canonical report sections
CATEGORY_TO_SECTION = {
    "allocation": "Portfolio Structure",
    "attribution": "Portfolio Structure",
    "correlation": "Concentration and Dependency",
    "cross_asset": "Market Regime",
    "divergence": "Market Regime",
    "early_warning": "Confidence Interpretation",
    "flow": "Market Regime",
    "liquidity": "Market Regime",
    "market_breadth": "Market Regime",
    "narrative_dependency": "Concentration and Dependency",
    "regime": "Market Regime",
    "relative_strength": "Deployment Analysis",
    "scenario": "Scenario Analysis",
    "portfolio_memory": "PM Summary",
}

# Valid completeness states (Requirement 24.1)
COMPLETENESS_STATES = frozenset({
    "complete",
    "partial",
    "degraded",
    "unavailable",
    "invalid",
})


# ---------------------------------------------------------------------------
# Sub-component: Section Completeness Classifier (Requirement 24.1)
# ---------------------------------------------------------------------------

class SectionCompletenessClassifier:
    """Classifies each section into a completeness state based on available
    Reasoning Objects.

    States:
    - complete: all Reasoning Objects available and valid
    - partial: some Reasoning Objects available, others degraded
    - degraded: Reasoning Objects available but with low confidence
    - unavailable: no Reasoning Objects available for this section
    - invalid: Reasoning Objects present but failing schema validation
    """

    def classify(
        self, section_name: str, available_objects: list[ReasoningObject]
    ) -> str:
        """Classify a section into exactly one completeness state.

        Args:
            section_name: Name of the canonical report section.
            available_objects: Reasoning Objects mapped to this section.

        Returns:
            One of: complete, partial, degraded, unavailable, invalid.
        """
        if not available_objects:
            return "unavailable"

        # Check for invalid objects (schema validation failures)
        valid_objects = []
        invalid_count = 0
        for obj in available_objects:
            errors = obj.validate()
            if errors:
                invalid_count += 1
            else:
                valid_objects.append(obj)

        # All objects invalid → invalid state
        if invalid_count > 0 and len(valid_objects) == 0:
            return "invalid"

        # No valid objects at all → unavailable
        if not valid_objects:
            return "unavailable"

        # Check confidence levels for degradation
        low_confidence_count = sum(
            1 for obj in valid_objects if obj.confidence_level < 50
        )

        # All valid objects have low confidence → degraded
        if low_confidence_count == len(valid_objects):
            return "degraded"

        # Some objects invalid but some valid → partial
        if invalid_count > 0:
            return "partial"

        # Some objects have low confidence but not all → partial
        if low_confidence_count > 0:
            return "partial"

        # All objects valid with adequate confidence → complete
        return "complete"


# ---------------------------------------------------------------------------
# Sub-component: Provenance Assembler (Requirement 13.1, 13.5)
# ---------------------------------------------------------------------------

class ProvenanceAssembler:
    """Assembles provenance metadata for each section from Reasoning Objects
    and their referenced Semantic States."""

    def assemble(
        self,
        section_name: str,
        objects: list[ReasoningObject],
        completeness: str,
    ) -> SectionProvenance:
        """Build provenance block for a section.

        Args:
            section_name: Name of the canonical report section.
            objects: Reasoning Objects contributing to this section.
            completeness: The section's completeness state.

        Returns:
            SectionProvenance with all chain layer identifiers populated.
        """
        reasoning_object_ids: list[str] = []
        semantic_state_ids: list[str] = []
        signal_engine_ids: list[str] = []
        unavailable_layers: list[dict] = []

        for obj in objects:
            errors = obj.validate()
            if not errors:
                reasoning_object_ids.append(obj.reasoning_id)
                semantic_state_ids.extend(obj.source_semantic_states)
                # Signal engine IDs are derived from the producing engine
                if obj.producing_engine not in signal_engine_ids:
                    signal_engine_ids.append(obj.producing_engine)

        # Deduplicate while preserving order
        semantic_state_ids = list(dict.fromkeys(semantic_state_ids))

        # Mark unavailable layers if no data at any level
        if not reasoning_object_ids:
            unavailable_layers.append({
                "layer": "REASONING",
                "reason": f"No valid Reasoning Objects for section '{section_name}'",
            })
        if not semantic_state_ids:
            unavailable_layers.append({
                "layer": "SEMANTICS",
                "reason": f"No Semantic State references for section '{section_name}'",
            })
        if not signal_engine_ids:
            unavailable_layers.append({
                "layer": "SIGNALS",
                "reason": f"No Signal Engine references for section '{section_name}'",
            })

        return SectionProvenance(
            section_name=section_name,
            reasoning_object_ids=reasoning_object_ids,
            semantic_state_ids=semantic_state_ids,
            signal_engine_ids=signal_engine_ids,
            completeness_state=completeness,
            unavailable_layers=unavailable_layers,
        )


# ---------------------------------------------------------------------------
# Sub-component: Section Renderer (Requirement 24.2)
# ---------------------------------------------------------------------------

class SectionRenderer:
    """Renders markdown content for a single section based on completeness state.

    HARDENING 7: Renders ONLY Reasoning_Object content. Does NOT create
    semantics, reasoning, or infer missing conclusions.

    Rendering rules by completeness state:
    - complete → full content from Reasoning Objects
    - partial → available content + partial-data notice
    - degraded → content + confidence warning
    - unavailable → degradation notice only (no synthetic content)
    - invalid → error notice with remediation guidance
    """

    def __init__(self) -> None:
        self._degradation_renderer = DegradationRenderer()

    def render(
        self,
        section_name: str,
        objects: list[ReasoningObject],
        completeness: str,
    ) -> str:
        """Render section markdown. Behavior determined by completeness state.

        Args:
            section_name: Name of the canonical report section.
            objects: Reasoning Objects mapped to this section.
            completeness: The section's completeness state.

        Returns:
            Rendered markdown string for the section.
        """
        if completeness == "unavailable":
            # No synthetic content — degradation notice only
            return self._degradation_renderer.render_degradation_notice(
                section_name,
                ["No Reasoning Objects available for this section"],
            )

        if completeness == "invalid":
            # Collect validation errors from all objects
            all_errors: list[str] = []
            for obj in objects:
                errors = obj.validate()
                all_errors.extend(errors)
            return self._degradation_renderer.render_error_notice(
                section_name, all_errors
            )

        # Render content from valid objects
        valid_objects = [obj for obj in objects if not obj.validate()]
        content_lines = self._render_content(section_name, valid_objects)

        if completeness == "degraded":
            # Find lowest confidence for warning
            min_confidence = min(
                obj.confidence_level for obj in valid_objects
            ) if valid_objects else 0
            warning = self._degradation_renderer.render_confidence_warning(
                section_name, min_confidence
            )
            return warning + "\n\n" + content_lines

        if completeness == "partial":
            # Render available content with partial-data notice
            notice = (
                f"> **Partial Data Notice:** Some data sources for "
                f"'{section_name}' are unavailable or invalid. "
                f"Content below reflects only available Reasoning Objects."
            )
            return notice + "\n\n" + content_lines

        # completeness == "complete" → full content
        return content_lines

    def _render_content(
        self, section_name: str, objects: list[ReasoningObject]
    ) -> str:
        """Render content paragraphs from valid Reasoning Objects.

        HARDENING 7: Only renders existing Reasoning_Object content.
        No inference, no synthesis, no gap-filling.
        """
        if not objects:
            return ""

        paragraphs: list[str] = []
        for obj in objects:
            # Render conclusion
            paragraphs.append(obj.conclusion.summary)

            # Render action implications if present
            if obj.action_implications:
                implications = []
                for impl in obj.action_implications:
                    implications.append(f"- **{impl.action}:** {impl.rationale}")
                if implications:
                    paragraphs.append("\n".join(implications))

        return "\n\n".join(paragraphs)


# ---------------------------------------------------------------------------
# Sub-component: Degradation Renderer (Requirement 24.2)
# ---------------------------------------------------------------------------

class DegradationRenderer:
    """Renders degradation notices, confidence warnings, and error notices.

    HARDENING 7: Renders ONLY notices about missing/degraded data.
    Does NOT generate synthetic analytical content.
    """

    def render_degradation_notice(
        self, section_name: str, unavailable_reasons: list[str]
    ) -> str:
        """Render unavailability notice for a section.

        Args:
            section_name: Name of the affected section.
            unavailable_reasons: List of reasons why data is unavailable.

        Returns:
            Markdown degradation notice.
        """
        reasons_text = "\n".join(f"- {reason}" for reason in unavailable_reasons)
        return (
            f"> **Section Unavailable:** '{section_name}' cannot be rendered.\n"
            f">\n"
            f"> Reasons:\n"
            f"{reasons_text}\n"
            f">\n"
            f"> No analytical content has been generated for this section. "
            f"Upstream data sources must be restored before this section "
            f"can be populated."
        )

    def render_confidence_warning(
        self, section_name: str, confidence_level: int
    ) -> str:
        """Render low-confidence warning for a section.

        Args:
            section_name: Name of the affected section.
            confidence_level: The confidence level (0-100) triggering the warning.

        Returns:
            Markdown confidence warning.
        """
        return (
            f"> **Low Confidence Warning:** '{section_name}' is rendered with "
            f"confidence level {confidence_level}/100. One or more upstream "
            f"signal categories were unavailable or degraded. Interpret "
            f"conclusions with caution."
        )

    def render_error_notice(
        self, section_name: str, validation_errors: list[str]
    ) -> str:
        """Render schema validation error with remediation guidance.

        Args:
            section_name: Name of the affected section.
            validation_errors: List of schema validation errors.

        Returns:
            Markdown error notice with remediation guidance.
        """
        errors_text = "\n".join(f"- {error}" for error in validation_errors)
        return (
            f"> **Validation Error:** '{section_name}' contains invalid "
            f"Reasoning Objects that failed schema validation.\n"
            f">\n"
            f"> Errors:\n"
            f"{errors_text}\n"
            f">\n"
            f"> **Remediation:** Verify that the producing Reasoning Engine "
            f"populates all required schema fields. Re-run the pipeline after "
            f"fixing the upstream engine."
        )


# ---------------------------------------------------------------------------
# Orchestrating class: ReportEngine (Hardening 2, Requirement 6.1)
# ---------------------------------------------------------------------------

class ReportEngine:
    """Chain-compliant report engine composing 4 sub-components.

    HARDENING 7 — REPORT ENGINE BOUNDARY:
    ReportEngine must NOT create semantics, NOT create reasoning, NOT infer
    missing conclusions. May ONLY render Reasoning_Object content and
    degradation notices.

    Sub-components:
    - SectionCompletenessClassifier: classifies sections into completeness states
    - ProvenanceAssembler: assembles provenance metadata per section
    - SectionRenderer: renders markdown content based on completeness state
    - DegradationRenderer: renders degradation notices, confidence warnings, errors

    Requirements: 6.1, 6.4, 24.1, 24.2, 24.4
    """

    CANONICAL_SECTIONS = [
        "Executive Summary",
        "Market Regime",
        "Portfolio Structure",
        "Concentration and Dependency",
        "Deployment Analysis",
        "Scenario Analysis",
        "Action Space",
        "Confidence Interpretation",
        "PM Summary",
    ]

    def __init__(self) -> None:
        self.classifier = SectionCompletenessClassifier()
        self.provenance_assembler = ProvenanceAssembler()
        self.section_renderer = SectionRenderer()
        self.degradation_renderer = DegradationRenderer()

    def render_section(
        self, section_name: str, objects: list[ReasoningObject]
    ) -> tuple[str, SectionProvenance]:
        """Orchestrate classification → rendering → provenance assembly for one section.

        HARDENING 7: Only renders existing Reasoning_Object content.
        No inference, no synthesis, no gap-filling.

        Args:
            section_name: Name of the canonical report section.
            objects: Reasoning Objects mapped to this section.

        Returns:
            Tuple of (rendered markdown string, SectionProvenance metadata).
        """
        # Step 1: Classify section completeness
        completeness = self.classifier.classify(section_name, objects)

        # Step 2: Render section content based on completeness state
        rendered_content = self.section_renderer.render(
            section_name, objects, completeness
        )

        # Step 3: Assemble provenance metadata
        provenance = self.provenance_assembler.assemble(
            section_name, objects, completeness
        )

        return rendered_content, provenance

    def render(
        self,
        reasoning_objects: list[ReasoningObject],
        deployment_matrix: object | None,
        portfolio_state: dict,
        watchlist: dict,
        run_context: RunContext,
    ) -> str:
        """Render full daily_report.md from Reasoning Objects.

        Must complete within 30 seconds. Delegates to sub-components for
        each section. Produces the complete markdown report with all 9
        canonical sections, provenance blocks, and Data Availability summary.

        HARDENING 7 — REPORT ENGINE BOUNDARY: Renders ONLY Reasoning_Object
        content and degradation notices. Does NOT create semantics, reasoning,
        or infer missing conclusions.

        Args:
            reasoning_objects: All Reasoning Objects produced by Reasoning Engines.
            deployment_matrix: DeploymentMatrix instance (or None if unavailable).
            portfolio_state: Dict of current portfolio holdings and positions.
            watchlist: Dict of watchlist candidates and deployment targets.
            run_context: The RunContext for this pipeline execution.

        Returns:
            Complete markdown string for daily_report.md.

        Requirements: 6.1, 6.2, 6.4, 6.6, 6.7, 13.1, 13.2
        """
        # Step 1: Group reasoning objects by canonical section
        section_objects: dict[str, list[ReasoningObject]] = {
            section: [] for section in self.CANONICAL_SECTIONS
        }
        for obj in reasoning_objects:
            category = obj.conclusion.category
            section_name = CATEGORY_TO_SECTION.get(category)
            if section_name and section_name in section_objects:
                section_objects[section_name].append(obj)

        # Step 2: Render each section in canonical order and collect provenance
        report_parts: list[str] = []
        all_provenance: list[SectionProvenance] = []

        # Report header
        report_parts.append(
            f"# Daily Portfolio Report — {run_context.timestamp}"
        )
        report_parts.append("")

        for section_name in self.CANONICAL_SECTIONS:
            objects = section_objects[section_name]

            # Render section content and provenance
            content, provenance = self.render_section(section_name, objects)
            all_provenance.append(provenance)

            # Section header
            report_parts.append(f"## {section_name}")
            report_parts.append("")

            # Section content
            report_parts.append(content)
            report_parts.append("")

            # Provenance block (embedded YAML — informational, not canonical)
            provenance_yaml = provenance.to_yaml()
            report_parts.append("```yaml")
            report_parts.append(provenance_yaml.rstrip())
            report_parts.append("```")
            report_parts.append("")

        # Step 3: Data Availability summary (Requirement 11.5)
        report_parts.append("## Data Availability")
        report_parts.append("")
        report_parts.append(
            self._render_data_availability(reasoning_objects, run_context)
        )
        report_parts.append("")

        return "\n".join(report_parts)

    def _render_data_availability(
        self,
        reasoning_objects: list[ReasoningObject],
        run_context: RunContext,
    ) -> str:
        """Render the Data Availability summary listing all 14 signal categories.

        Each category gets exactly one status:
        - "available": Reasoning Object exists for this category
        - "unavailable_no_output": No Reasoning Object produced for this category

        Args:
            reasoning_objects: All Reasoning Objects from this pipeline run.
            run_context: The RunContext for this pipeline execution.

        Returns:
            Markdown table of category availability statuses.
        """
        # All 14 signal categories
        all_categories = sorted(CATEGORY_TO_SECTION.keys())

        # Determine which categories have reasoning objects
        available_categories: set[str] = set()
        for obj in reasoning_objects:
            errors = obj.validate()
            if not errors:
                available_categories.add(obj.conclusion.category)

        # Build availability table
        lines: list[str] = []
        lines.append("| Signal Category | Status |")
        lines.append("|---|---|")
        for category in all_categories:
            if category in available_categories:
                status = "available"
            else:
                status = "unavailable_no_output"
            lines.append(f"| {category} | {status} |")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# DEPRECATED: Legacy report engine function
# ---------------------------------------------------------------------------

def run_report_engine(
    allocation_data,
    regime_data,
    decision_data,
    quality_data,
    scenario_data
):
    """Generate a portfolio report from raw engine outputs.

    .. deprecated::
        This function bypasses the canonical chain (SIGNALS → SEMANTICS →
        REASONING → REPORT). Use :class:`ReportEngine` instead, which
        renders from validated Reasoning Objects with full provenance.

    Args:
        allocation_data: Raw allocation engine output dict.
        regime_data: Raw regime engine output dict.
        decision_data: Raw decision engine output dict.
        quality_data: Raw quality engine output dict.
        scenario_data: Raw scenario engine output dict.

    Returns:
        Dict with keys: report, date, confidence.
    """
    warnings.warn(
        "run_report_engine() is deprecated. Use ReportEngine class which "
        "renders from validated Reasoning Objects through the canonical chain "
        "(SIGNALS → SEMANTICS → REASONING → REPORT).",
        DeprecationWarning,
        stacklevel=2,
    )

    print("\n=== FINAL REPORT ===")

    date = datetime.today().strftime("%Y-%m-%d")

    # ---------------------------------------------------
    # REGIME
    # ---------------------------------------------------
    regime_comment = regime_data.get("Regime Comment", "No regime data")

    # ---------------------------------------------------
    # DECISIONS
    # ---------------------------------------------------
    decisions = decision_data.get("decisions", [])

    primary = next(
        (d["message"] for d in decisions if d["type"] == "primary_action"),
        "No primary decision",
    )

    risk_context = next(
        (d["message"] for d in decisions if d["type"] == "risk_adjustment"),
        "No risk context",
    )

    # ---------------------------------------------------
    # QUALITY
    # ---------------------------------------------------
    confidence = quality_data.get("confidence_score", 0)
    quality_label = quality_data.get("quality_label", "UNKNOWN")

    # ---------------------------------------------------
    # TARGET VS ACTUAL
    # ---------------------------------------------------
    target_vs_actual = allocation_data.get("target_vs_actual", [])
    allocation_summary = ""
    for row in target_vs_actual:
        allocation_summary += (
            f"- {row['Risk Level']} allocation currently at "
            f"{row['Actual %']}% (Target: {row['Target %']}%)\n"
        )

    # ---------------------------------------------------
    # SCENARIOS
    # ---------------------------------------------------
    scenarios = scenario_data.get("scenarios", [])
    scenario_summary = ""
    for s in scenarios:
        scenario_summary += f"- {s['scenario']}: {s['impact']}\n"

    # ---------------------------------------------------
    # REPORT
    # ---------------------------------------------------
    report = f"""
PORTFOLIO INTELLIGENCE REPORT — {date}
=====================================

MARKET REGIME
-------------
{regime_comment}

PRIMARY ACTION
--------------
{primary}

RISK CONTEXT
------------
{risk_context}

TARGET VS ACTUAL
----------------
{allocation_summary}

SCENARIO ANALYSIS
-----------------
{scenario_summary}

CONFIDENCE
----------
Confidence Score: {confidence}
Confidence Level: {quality_label}

PM SUMMARY
----------
Portfolio currently operates with elevated
HIGH-risk exposure and concentration pressure.

Current positioning remains functional
but should be monitored closely under
current market conditions.
"""

    print(report)

    return {
        "report": report,
        "date": date,
        "confidence": confidence,
    }
