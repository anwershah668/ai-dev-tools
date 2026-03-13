"""Unit tests for src.doc_generator."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.doc_generator import DocGenerator


UNDOCUMENTED_CODE = """\
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


class Calculator:
    def multiply(self, x, y):
        return x * y
"""

DOCUMENTED_CODE = '''\
"""Module docstring."""


def add(a, b):
    """Add two numbers.

    Args:
        a: First operand.
        b: Second operand.

    Returns:
        Sum of a and b.
    """
    return a + b
'''


class TestDocGeneratorBasic(unittest.TestCase):
    def setUp(self):
        self.gen = DocGenerator()

    def test_empty_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.gen.generate("")

    def test_whitespace_only_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.gen.generate("   ")

    def test_returns_string(self):
        result = self.gen.generate(UNDOCUMENTED_CODE)
        self.assertIsInstance(result, str)

    def test_report_header_present(self):
        result = self.gen.generate(UNDOCUMENTED_CODE)
        self.assertIn("# Documentation Report", result)

    def test_module_overview_section(self):
        result = self.gen.generate(UNDOCUMENTED_CODE)
        self.assertIn("## Module Overview", result)

    def test_docstring_stubs_section(self):
        result = self.gen.generate(UNDOCUMENTED_CODE)
        self.assertIn("## Docstring Stubs", result)

    def test_missing_docstring_flagged(self):
        result = self.gen.generate(UNDOCUMENTED_CODE)
        self.assertIn("missing docstring", result)

    def test_existing_docstring_shows_checkmark(self):
        result = self.gen.generate(DOCUMENTED_CODE)
        self.assertIn("has docstring", result)

    def test_function_names_appear_in_report(self):
        result = self.gen.generate(UNDOCUMENTED_CODE)
        self.assertIn("`add`", result)
        self.assertIn("`subtract`", result)

    def test_class_name_appears_in_report(self):
        result = self.gen.generate(UNDOCUMENTED_CODE)
        self.assertIn("Calculator", result)

    def test_stub_contains_args(self):
        result = self.gen.generate(UNDOCUMENTED_CODE)
        self.assertIn("Args:", result)

    def test_stub_contains_returns(self):
        result = self.gen.generate(UNDOCUMENTED_CODE)
        self.assertIn("Returns:", result)

    def test_generate_docstring_basic(self):
        stub = self.gen.generate_docstring("my_func", ["x", "y"])
        self.assertIn("my_func", stub)
        self.assertIn("Args:", stub)
        self.assertIn("x:", stub)
        self.assertIn("y:", stub)
        self.assertIn("Returns:", stub)

    def test_generate_docstring_no_return(self):
        stub = self.gen.generate_docstring("do_something", ["value"], has_return=False)
        self.assertNotIn("Returns:", stub)

    def test_generate_docstring_empty_args(self):
        stub = self.gen.generate_docstring("greet", [])
        self.assertIn("greet", stub)
        self.assertNotIn("Args:", stub)

    def test_syntax_error_on_invalid_code(self):
        with self.assertRaises(SyntaxError):
            self.gen.generate("def broken(\n")

    def test_module_with_docstring_in_overview(self):
        code = '"""My module."""\ndef f():\n    return 1\n'
        result = self.gen.generate(code)
        self.assertIn("My module.", result)


if __name__ == "__main__":
    unittest.main()
