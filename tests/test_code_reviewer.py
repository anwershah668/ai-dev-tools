"""Tests for the Code Reviewer module."""

from ai_dev_tools.code_reviewer import (
    check_function_length,
    check_missing_docstrings,
    check_todo_comments,
    review_code,
)

CLEAN_CODE = '''
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"


class Calculator:
    """A simple calculator."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b
'''

CODE_WITH_ISSUES = '''
def no_docstring():
    return 42

class BadClass:
    pass

# TODO: fix this later
# FIXME: broken logic here
def another():
    return True
'''


class TestCheckFunctionLength:
    def test_short_function(self):
        source = "def hello():\n    return 1\n"
        result = check_function_length(source, max_lines=50)
        assert len(result) == 0

    def test_long_function(self):
        lines = ["def long_func():"]
        lines.extend(["    x = 1"] * 60)
        source = "\n".join(lines) + "\n"
        result = check_function_length(source, max_lines=50)
        assert len(result) == 1
        assert result[0]["function"] == "long_func"
        assert "long_func" in result[0]["suggestion"]


class TestCheckMissingDocstrings:
    def test_clean_code(self):
        result = check_missing_docstrings(CLEAN_CODE)
        assert len(result) == 0

    def test_missing_docstrings(self):
        result = check_missing_docstrings(CODE_WITH_ISSUES)
        names = [item["name"] for item in result]
        assert "no_docstring" in names
        assert "BadClass" in names
        assert "another" in names


class TestCheckTodoComments:
    def test_no_todos(self):
        result = check_todo_comments(CLEAN_CODE)
        assert len(result) == 0

    def test_finds_todos(self):
        result = check_todo_comments(CODE_WITH_ISSUES)
        assert len(result) == 2
        tags = [item["tag"] for item in result]
        assert "TODO" in tags
        assert "FIXME" in tags


class TestReviewCode:
    def test_clean_code(self):
        result = review_code(CLEAN_CODE, filename="clean.py")
        assert result["total_issues"] == 0
        assert "looks good" in result["summary"].lower()

    def test_code_with_issues(self):
        result = review_code(CODE_WITH_ISSUES, filename="bad.py")
        assert result["total_issues"] > 0
        assert result["filename"] == "bad.py"
        assert len(result["missing_docstrings"]) > 0
        assert len(result["todos"]) > 0
