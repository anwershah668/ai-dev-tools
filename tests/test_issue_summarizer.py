"""Tests for the Issue Summarizer module."""

from ai_dev_tools.issue_summarizer import (
    extract_key_sentences,
    summarize_issue,
    _categorize_issue,
    _estimate_priority,
)


class TestExtractKeySentences:
    def test_empty_text(self):
        assert extract_key_sentences("") == ""
        assert extract_key_sentences("   ") == ""

    def test_single_sentence(self):
        result = extract_key_sentences("This is a bug report.")
        assert result == "This is a bug report."

    def test_fewer_sentences_than_max(self):
        text = "First sentence. Second sentence."
        result = extract_key_sentences(text, max_sentences=5)
        assert "First sentence" in result
        assert "Second sentence" in result

    def test_prioritizes_keyword_sentences(self):
        text = (
            "This is a general intro. "
            "The application crashes on startup. "
            "I like the color blue. "
            "There is an error in the login page."
        )
        result = extract_key_sentences(text, max_sentences=2)
        assert "crashes" in result or "error" in result

    def test_first_sentence_boost(self):
        text = "Main point here. Filler content. More filler. Extra noise."
        result = extract_key_sentences(text, max_sentences=1)
        assert "Main point" in result


class TestSummarizeIssue:
    def test_basic_summary(self):
        result = summarize_issue(
            title="Login button broken",
            body="The login button does not respond when clicked.",
        )
        assert result["title"] == "Login button broken"
        assert result["summary"] != ""
        assert result["category"] == "bug"

    def test_empty_body_uses_title(self):
        result = summarize_issue(title="Add dark mode", body="")
        assert result["summary"] == "Add dark mode"

    def test_labels_counted(self):
        result = summarize_issue(
            title="Test",
            body="Test body.",
            labels=["bug", "priority"],
        )
        assert result["label_count"] == 2


class TestCategorizeIssue:
    def test_bug_category(self):
        assert _categorize_issue("App crashes", "It crashes on load", []) == "bug"

    def test_feature_category(self):
        assert _categorize_issue("Add search feature", "We need search", []) == "feature"

    def test_docs_category(self):
        assert _categorize_issue("Fix typo in docs", "Typo in documentation", []) == "documentation"

    def test_question_category(self):
        assert _categorize_issue("How to configure?", "Question about setup", []) == "question"

    def test_general_category(self):
        assert _categorize_issue("Update version", "Bump to 2.0", []) == "general"


class TestEstimatePriority:
    def test_high_priority(self):
        assert _estimate_priority("Security vulnerability", "", []) == "high"
        assert _estimate_priority("Critical crash", "", []) == "high"

    def test_medium_priority(self):
        assert _estimate_priority("Bug in login", "", []) == "medium"

    def test_low_priority(self):
        assert _estimate_priority("Update readme", "", []) == "low"
