"""Unit tests for IssueSummarizer."""

import pytest
from src.issue_summarizer import IssueSummarizer


@pytest.fixture
def summarizer():
    return IssueSummarizer()


class TestIssueSummarizerBasic:
    def test_returns_string(self, summarizer):
        result = summarizer.summarize(["The button is broken on mobile."])
        assert isinstance(result, str)

    def test_output_contains_summary_header(self, summarizer):
        result = summarizer.summarize(["Login fails on iOS."])
        assert "Summary" in result

    def test_output_contains_key_topics(self, summarizer):
        result = summarizer.summarize(["The login button fails on mobile devices."])
        assert "Key topics" in result

    def test_comment_count_reflected_in_output(self, summarizer):
        comments = ["First comment.", "Second comment.", "Third comment."]
        result = summarizer.summarize(comments)
        assert "3" in result

    def test_single_comment(self, summarizer):
        result = summarizer.summarize(["Only one comment here."])
        assert "1 comment" in result

    def test_empty_list_raises(self, summarizer):
        with pytest.raises(ValueError):
            summarizer.summarize([])

    def test_multiple_comments_extract_keywords(self, summarizer):
        comments = [
            "The login button is broken on mobile.",
            "Reproduced on iOS and Android.",
            "The CSS media query is wrong.",
            "PR #42 fixes the button issue.",
        ]
        result = summarizer.summarize(comments)
        # Should mention at least one relevant keyword
        assert any(kw in result.lower() for kw in ["button", "login", "mobile", "css", "media"])

    def test_top_keywords_parameter(self, summarizer):
        comments = ["alpha beta gamma delta epsilon zeta eta theta."]
        result = summarizer.summarize(comments, top_keywords=3)
        assert "Key topics" in result


class TestIssueSummarizerInternals:
    def test_split_sentences_single(self, summarizer):
        sentences = summarizer._split_sentences(["Hello world. How are you?"])
        assert len(sentences) == 2

    def test_word_frequencies_excludes_stop_words(self, summarizer):
        freq = summarizer._word_frequencies("the quick brown fox and the lazy dog")
        assert "the" not in freq
        assert "and" not in freq
        assert "quick" in freq
        assert "brown" in freq

    def test_best_sentence_picks_most_relevant(self, summarizer):
        sentences = ["I had lunch today.", "The login button is broken on mobile."]
        keywords = {"login", "button", "mobile"}
        best = summarizer._best_sentence(sentences, keywords)
        assert "login" in best.lower()

    def test_best_sentence_empty_list(self, summarizer):
        assert summarizer._best_sentence([], set()) == ""
