"""Unit tests for CodeReviewTool."""

import os
import tempfile

import pytest
from src.code_review_tool import CodeReviewTool, Suggestion


@pytest.fixture
def reviewer():
    return CodeReviewTool()


def write_temp_py(source: str) -> str:
    """Write Python source to a temp file and return the path."""
    fd, path = tempfile.mkstemp(suffix=".py")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(source)
    return path


class TestCodeReviewToolBasic:
    def test_clean_code_returns_no_suggestions(self, reviewer):
        source = '''\
"""A clean module."""


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
'''
        suggestions = reviewer.review(source)
        assert suggestions == []

    def test_returns_list(self, reviewer):
        result = reviewer.review("x = 1\n")
        assert isinstance(result, list)

    def test_suggestion_str_format(self, reviewer):
        s = Suggestion(line=5, category="Style", message="Too long.")
        assert "Style" in str(s)
        assert "Line 5" in str(s)

    def test_suggestion_no_line(self):
        s = Suggestion(line=None, category="General", message="Check this.")
        assert "General" in str(s)
        assert "Check this" in str(s)


class TestCodeReviewToolStyleChecks:
    def test_long_line_flagged(self, reviewer):
        long_line = "x = " + "a" * 200 + "\n"
        suggestions = reviewer.review(long_line)
        categories = [s.category for s in suggestions]
        assert "Style" in categories

    def test_trailing_whitespace_flagged(self, reviewer):
        source = "x = 1   \n"
        suggestions = reviewer.review(source)
        messages = [s.message for s in suggestions]
        assert any("trailing" in m.lower() for m in messages)

    def test_no_trailing_whitespace_no_flag(self, reviewer):
        source = "x = 1\n"
        suggestions = reviewer.review(source)
        messages = [s.message for s in suggestions]
        assert not any("trailing" in m.lower() for m in messages)


class TestCodeReviewToolBestPractices:
    def test_bare_except_flagged(self, reviewer):
        source = '''\
def risky():
    """Does something risky."""
    try:
        pass
    except:
        pass
'''
        suggestions = reviewer.review(source)
        categories = [s.category for s in suggestions]
        assert "Best Practice" in categories

    def test_mutable_default_list_flagged(self, reviewer):
        source = '''\
def collect(items=[]):
    """Collect items."""
    return items
'''
        suggestions = reviewer.review(source)
        categories = [s.category for s in suggestions]
        assert "Best Practice" in categories

    def test_mutable_default_dict_flagged(self, reviewer):
        source = '''\
def configure(options={}):
    """Configure."""
    return options
'''
        suggestions = reviewer.review(source)
        categories = [s.category for s in suggestions]
        assert "Best Practice" in categories


class TestCodeReviewToolDocumentation:
    def test_missing_function_docstring_flagged(self, reviewer):
        source = "def undocumented():\n    pass\n"
        suggestions = reviewer.review(source)
        categories = [s.category for s in suggestions]
        assert "Documentation" in categories

    def test_private_function_docstring_not_flagged(self, reviewer):
        source = "def _private():\n    pass\n"
        suggestions = reviewer.review(source)
        categories = [s.category for s in suggestions]
        assert "Documentation" not in categories

    def test_missing_class_docstring_flagged(self, reviewer):
        source = "class MyClass:\n    pass\n"
        suggestions = reviewer.review(source)
        categories = [s.category for s in suggestions]
        assert "Documentation" in categories


class TestCodeReviewToolComplexity:
    def test_too_many_args_flagged(self, reviewer):
        source = '''\
def overloaded(a, b, c, d, e, f, g):
    """Has too many args."""
    pass
'''
        suggestions = reviewer.review(source)
        categories = [s.category for s in suggestions]
        assert "Complexity" in categories

    def test_acceptable_args_not_flagged(self, reviewer):
        source = '''\
def acceptable(a, b, c):
    """Three args is fine."""
    pass
'''
        suggestions = reviewer.review(source)
        complexity = [s for s in suggestions if s.category == "Complexity"]
        assert complexity == []


class TestCodeReviewToolFileReview:
    def test_review_file_works(self, reviewer):
        source = "def undocumented():\n    pass\n"
        path = write_temp_py(source)
        try:
            suggestions = reviewer.review_file(path)
            assert isinstance(suggestions, list)
        finally:
            os.unlink(path)

    def test_review_file_not_found(self, reviewer):
        with pytest.raises(FileNotFoundError):
            reviewer.review_file("/nonexistent/path/file.py")
