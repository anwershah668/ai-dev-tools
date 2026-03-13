"""Tests for the Documentation Generator module."""

from ai_dev_tools.doc_generator import (
    extract_functions,
    extract_classes,
    generate_markdown_docs,
)

SAMPLE_SOURCE = '''"""A sample module for testing."""

def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The sum of a and b.
    """
    return a + b


def _private_helper():
    """This is private."""
    pass


class MyClass(BaseClass):
    """A sample class."""

    def method(self):
        """A method."""
        pass
'''


class TestExtractFunctions:
    def test_extracts_all_functions(self):
        funcs = extract_functions(SAMPLE_SOURCE)
        names = [f["name"] for f in funcs]
        assert "greet" in names
        assert "add" in names
        assert "_private_helper" in names

    def test_extracts_args(self):
        funcs = extract_functions(SAMPLE_SOURCE)
        greet = next(f for f in funcs if f["name"] == "greet")
        assert len(greet["args"]) == 1
        assert "name: str" in greet["args"][0]

    def test_extracts_return_type(self):
        funcs = extract_functions(SAMPLE_SOURCE)
        greet = next(f for f in funcs if f["name"] == "greet")
        assert greet["return_type"] == "str"

    def test_extracts_docstring(self):
        funcs = extract_functions(SAMPLE_SOURCE)
        greet = next(f for f in funcs if f["name"] == "greet")
        assert "Greet someone" in greet["docstring"]

    def test_private_flag(self):
        funcs = extract_functions(SAMPLE_SOURCE)
        helper = next(f for f in funcs if f["name"] == "_private_helper")
        assert helper["is_private"] is True


class TestExtractClasses:
    def test_extracts_class(self):
        classes = extract_classes(SAMPLE_SOURCE)
        assert len(classes) >= 1
        assert classes[0]["name"] == "MyClass"

    def test_extracts_bases(self):
        classes = extract_classes(SAMPLE_SOURCE)
        assert classes[0]["bases"] == "BaseClass"

    def test_extracts_class_docstring(self):
        classes = extract_classes(SAMPLE_SOURCE)
        assert "sample class" in classes[0]["docstring"].lower()


class TestGenerateMarkdownDocs:
    def test_generates_markdown(self):
        result = generate_markdown_docs(SAMPLE_SOURCE, module_name="sample")
        assert "# sample" in result
        assert "## Functions" in result
        assert "greet" in result

    def test_excludes_private_by_default(self):
        result = generate_markdown_docs(SAMPLE_SOURCE)
        assert "_private_helper" not in result

    def test_includes_private_when_requested(self):
        result = generate_markdown_docs(SAMPLE_SOURCE, include_private=True)
        assert "_private_helper" in result

    def test_includes_classes(self):
        result = generate_markdown_docs(SAMPLE_SOURCE)
        assert "## Classes" in result
        assert "MyClass" in result
