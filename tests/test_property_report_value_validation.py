"""Property-based tests for Report Value Validation.

**Validates: Requirements 4.2, 4.4**

Tests that invalid categories are flagged and speculative language patterns are detected.
Hypothesis generates random category strings and justification text; verifies detection accuracy.
"""

import sys
from pathlib import Path

from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure the .domainization/src directory is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".domainization" / "src"))

from report_value_detector import (
    ReportValueDetector,
    ALLOWED_REPORT_VALUE_CATEGORIES,
    SPECULATIVE_KEYWORDS,
)


# The 10 accepted report value categories
VALID_CATEGORIES = list(ALLOWED_REPORT_VALUE_CATEGORIES)

# The speculative keywords that must be detected
SPECULATIVE_PATTERNS = [
    "might improve",
    "could help",
    "potentially",
    "in the future",
    "indirectly",
]

# Strategy: generate random strings that are NOT valid categories
invalid_category_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
    min_size=1,
    max_size=50,
).filter(lambda s: s.strip().lower() not in VALID_CATEGORIES)

# Strategy: generate justification text WITHOUT speculative keywords
non_speculative_text_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
    min_size=1,
    max_size=200,
).filter(
    lambda s: not any(kw in s.lower() for kw in SPECULATIVE_KEYWORDS)
)

# Strategy: pick one of the 5 required speculative keywords
speculative_keyword_strategy = st.sampled_from(SPECULATIVE_PATTERNS)

# Strategy: generate surrounding text for embedding speculative keywords
surrounding_text_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
    min_size=0,
    max_size=80,
)


class TestReportValueValidationProperties:
    """Property-based tests for Report Value Validation (Property 6)."""

    @given(category=st.sampled_from(VALID_CATEGORIES))
    @settings(max_examples=100)
    def test_valid_categories_are_accepted(self, category: str) -> None:
        """Property 1: All 10 accepted categories are recognized as valid.

        **Validates: Requirements 4.2**

        Every category in the accepted list must return True from is_valid_category().
        """
        detector = ReportValueDetector()
        assert detector.is_valid_category(category) is True, (
            f"Valid category '{category}' was rejected by is_valid_category()"
        )

    @given(category=invalid_category_strategy)
    @settings(max_examples=300)
    def test_invalid_categories_are_rejected(self, category: str) -> None:
        """Property 2: Any category NOT in the accepted list is flagged as invalid.

        **Validates: Requirements 4.2**

        Random strings that are not one of the 10 accepted categories must
        return False from is_valid_category().
        """
        detector = ReportValueDetector()
        assert detector.is_valid_category(category) is False, (
            f"Invalid category '{category}' was accepted by is_valid_category()"
        )

    @given(
        keyword=speculative_keyword_strategy,
        prefix=surrounding_text_strategy,
        suffix=surrounding_text_strategy,
    )
    @settings(max_examples=300)
    def test_speculative_keywords_are_detected(
        self, keyword: str, prefix: str, suffix: str
    ) -> None:
        """Property 3: Justification text containing speculative keywords is flagged.

        **Validates: Requirements 4.4**

        Any justification text that contains one of the speculative keywords
        ("might improve", "could help", "potentially", "in the future", "indirectly")
        must be detected as speculative by _is_speculative_claim().
        """
        justification = f"{prefix} {keyword} {suffix}"
        detector = ReportValueDetector()
        assert detector._is_speculative_claim(justification) is True, (
            f"Speculative keyword '{keyword}' was not detected in: '{justification}'"
        )

    @given(text=non_speculative_text_strategy)
    @settings(max_examples=300)
    def test_non_speculative_text_is_not_flagged(self, text: str) -> None:
        """Property 4: Justification text without speculative keywords is not flagged.

        **Validates: Requirements 4.4**

        Text that does not contain any speculative keywords must not be
        flagged as speculative by _is_speculative_claim().
        """
        detector = ReportValueDetector()
        assert detector._is_speculative_claim(text) is False, (
            f"Non-speculative text was incorrectly flagged: '{text}'"
        )

    @given(
        category=invalid_category_strategy,
        justification=non_speculative_text_strategy,
    )
    @settings(max_examples=200)
    def test_invalid_category_flagged_in_assessment(
        self, category: str, justification: str
    ) -> None:
        """Property 5: Artifacts with invalid categories produce assessment issues.

        **Validates: Requirements 4.2**

        When an artifact has a report_value with an invalid category,
        the assessment must contain issues and is_valid must be False.
        """
        detector = ReportValueDetector()
        artifact = {
            "artifact_id": "test_artifact",
            "file_path": "test/path.py",
            "report_value": {
                "category": category,
                "justification": justification,
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert not assessment.is_valid, (
            f"Artifact with invalid category '{category}' was assessed as valid"
        )
        assert len(assessment.issues) > 0, (
            f"Artifact with invalid category '{category}' has no issues"
        )

    @given(
        category=st.sampled_from(VALID_CATEGORIES),
        keyword=speculative_keyword_strategy,
        prefix=surrounding_text_strategy,
        suffix=surrounding_text_strategy,
    )
    @settings(max_examples=200)
    def test_speculative_justification_flagged_in_assessment(
        self, category: str, keyword: str, prefix: str, suffix: str
    ) -> None:
        """Property 6: Artifacts with speculative justification produce assessment issues.

        **Validates: Requirements 4.4**

        When an artifact has a valid category but speculative justification,
        the assessment must flag it as speculative and is_valid must be False.
        """
        justification = f"{prefix} {keyword} {suffix}"
        detector = ReportValueDetector()
        artifact = {
            "artifact_id": "test_artifact",
            "file_path": "test/path.py",
            "report_value": {
                "category": category,
                "justification": justification,
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_speculative is True, (
            f"Speculative justification with keyword '{keyword}' was not flagged"
        )
        assert not assessment.is_valid, (
            f"Artifact with speculative justification was assessed as valid"
        )

    @given(
        category=st.sampled_from(VALID_CATEGORIES),
        justification=non_speculative_text_strategy,
    )
    @settings(max_examples=200)
    def test_valid_category_and_non_speculative_justification_is_valid(
        self, category: str, justification: str
    ) -> None:
        """Property 7: Artifacts with valid category and non-speculative justification pass.

        **Validates: Requirements 4.2, 4.4**

        When an artifact has a valid category and non-speculative justification,
        the assessment must be valid with no issues related to category or speculation.
        """
        detector = ReportValueDetector()
        artifact = {
            "artifact_id": "test_artifact",
            "file_path": "test/path.py",
            "report_value": {
                "category": category,
                "justification": justification,
            },
        }
        assessment = detector.assess_artifact(artifact)
        assert assessment.is_valid is True, (
            f"Valid artifact (category='{category}', justification='{justification}') "
            f"was assessed as invalid. Issues: {assessment.issues}"
        )

    @given(category=st.sampled_from(VALID_CATEGORIES))
    @settings(max_examples=50)
    def test_valid_category_case_insensitive(self, category: str) -> None:
        """Property 8: Category validation is case-insensitive.

        **Validates: Requirements 4.2**

        Valid categories should be accepted regardless of case (upper, mixed, lower).
        """
        detector = ReportValueDetector()
        # Test uppercase
        assert detector.is_valid_category(category.upper()) is True, (
            f"Uppercase category '{category.upper()}' was rejected"
        )
        # Test mixed case
        mixed = category[0].upper() + category[1:] if len(category) > 1 else category.upper()
        assert detector.is_valid_category(mixed) is True, (
            f"Mixed-case category '{mixed}' was rejected"
        )
