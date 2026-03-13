"""Unit tests for src.code_review."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.code_review import CodeReviewer, ReviewSuggestion


class TestCodeReviewerBasic(unittest.TestCase):
    def setUp(self):
        self.reviewer = CodeReviewer()

    def test_empty_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.reviewer.review("")

    def test_whitespace_only_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.reviewer.review("   ")

    def test_clean_code_returns_list(self):
        code = 'def add(a, b):\n    """Add."""\n    return a + b\n'
        result = self.reviewer.review(code)
        self.assertIsInstance(result, list)

    def test_hardcoded_secret_detected(self):
        code = 'password = "hunter2"\n'
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("hardcoded-secret", rules)

    def test_hardcoded_api_key_detected(self):
        code = 'api_key = "my_secret_key_123"\n'
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("hardcoded-secret", rules)

    def test_eval_detected(self):
        code = 'def f():\n    """D."""\n    eval("x + 1")\n'
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("eval-exec", rules)

    def test_exec_detected(self):
        code = 'def f():\n    """D."""\n    exec("x = 1")\n'
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("eval-exec", rules)

    def test_bare_except_detected(self):
        code = (
            'def f():\n'
            '    """D."""\n'
            '    try:\n'
            '        pass\n'
            '    except:\n'
            '        pass\n'
        )
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("broad-except", rules)

    def test_missing_docstring_detected(self):
        code = 'def add(a, b):\n    return a + b\n'
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("missing-docstring", rules)

    def test_mutable_default_arg_detected(self):
        code = 'def f(items=[]):\n    """D."""\n    return items\n'
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("mutable-default-arg", rules)

    def test_todo_comment_detected(self):
        code = '# TODO: fix this later\nx = 1\n'
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("todo-comment", rules)

    def test_fixme_comment_detected(self):
        code = '# FIXME: this is broken\nx = 1\n'
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("todo-comment", rules)

    def test_long_line_detected(self):
        code = "x = " + "a" * 130 + "\n"
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("line-too-long", rules)

    def test_syntax_error_reported(self):
        code = 'def broken(\n'
        suggestions = self.reviewer.review(code)
        rules = [s.rule for s in suggestions]
        self.assertIn("syntax-error", rules)

    def test_suggestions_sorted_by_line(self):
        code = (
            'password = "secret"\n'
            '# TODO: remove\n'
            'def f():\n'
            '    pass\n'
        )
        suggestions = self.reviewer.review(code)
        lines = [s.line for s in suggestions]
        self.assertEqual(lines, sorted(lines))

    def test_review_suggestion_str(self):
        s = ReviewSuggestion(line=5, severity="error", rule="test-rule", message="Test message")
        text = str(s)
        self.assertIn("ERROR", text)
        self.assertIn("Line 5", text)
        self.assertIn("Test message", text)
        self.assertIn("test-rule", text)

    def test_review_suggestion_warning_str(self):
        s = ReviewSuggestion(line=10, severity="warning", rule="warn-rule", message="Watch out")
        self.assertIn("⚠️", str(s))

    def test_review_suggestion_info_str(self):
        s = ReviewSuggestion(line=1, severity="info", rule="info-rule", message="FYI")
        self.assertIn("ℹ️", str(s))


if __name__ == "__main__":
    unittest.main()
