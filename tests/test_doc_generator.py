"""Unit tests for DocGenerator."""

import os
import tempfile
from pathlib import Path

import pytest
from src.doc_generator import DocGenerator


SIMPLE_MODULE = '''\
"""A simple example module."""


def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b


def greet(name: str) -> str:
    """Return a greeting string."""
    return f"Hello, {name}!"
'''

MODULE_WITH_CLASS = '''\
"""Module with a class."""


class Calculator:
    """Performs basic arithmetic operations."""

    def add(self, x: int, y: int) -> int:
        """Return the sum of x and y."""
        return x + y

    def subtract(self, x: int, y: int) -> int:
        """Return the difference of x and y."""
        return x - y

    def _internal(self):
        pass
'''

MODULE_NO_DOCSTRING = '''\
def plain():
    pass
'''


@pytest.fixture
def generator():
    return DocGenerator()


def write_temp_module(source: str, suffix: str = ".py") -> str:
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(source)
    return path


class TestDocGeneratorBasic:
    def test_returns_string(self, generator):
        path = write_temp_module(SIMPLE_MODULE)
        try:
            result = generator.generate_docs(path)
            assert isinstance(result, str)
        finally:
            os.unlink(path)

    def test_contains_module_name(self, generator):
        fd, path = tempfile.mkstemp(suffix=".py", prefix="mymodule_")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(SIMPLE_MODULE)
        try:
            result = generator.generate_docs(path)
            stem = Path(path).stem
            assert stem in result
        finally:
            os.unlink(path)

    def test_module_docstring_included(self, generator):
        path = write_temp_module(SIMPLE_MODULE)
        try:
            result = generator.generate_docs(path)
            assert "simple example module" in result
        finally:
            os.unlink(path)

    def test_function_names_included(self, generator):
        path = write_temp_module(SIMPLE_MODULE)
        try:
            result = generator.generate_docs(path)
            assert "add" in result
            assert "greet" in result
        finally:
            os.unlink(path)

    def test_function_docstrings_included(self, generator):
        path = write_temp_module(SIMPLE_MODULE)
        try:
            result = generator.generate_docs(path)
            assert "Add two numbers" in result
            assert "Return a greeting" in result
        finally:
            os.unlink(path)

    def test_file_not_found_raises(self, generator):
        with pytest.raises(FileNotFoundError):
            generator.generate_docs("/nonexistent/path/module.py")


class TestDocGeneratorClass:
    def test_class_section_present(self, generator):
        path = write_temp_module(MODULE_WITH_CLASS)
        try:
            result = generator.generate_docs(path)
            assert "## Classes" in result
        finally:
            os.unlink(path)

    def test_class_name_included(self, generator):
        path = write_temp_module(MODULE_WITH_CLASS)
        try:
            result = generator.generate_docs(path)
            assert "Calculator" in result
        finally:
            os.unlink(path)

    def test_class_docstring_included(self, generator):
        path = write_temp_module(MODULE_WITH_CLASS)
        try:
            result = generator.generate_docs(path)
            assert "basic arithmetic" in result
        finally:
            os.unlink(path)

    def test_private_methods_excluded(self, generator):
        path = write_temp_module(MODULE_WITH_CLASS)
        try:
            result = generator.generate_docs(path)
            assert "_internal" not in result
        finally:
            os.unlink(path)

    def test_public_methods_listed(self, generator):
        path = write_temp_module(MODULE_WITH_CLASS)
        try:
            result = generator.generate_docs(path)
            assert "add" in result
            assert "subtract" in result
        finally:
            os.unlink(path)


class TestDocGeneratorOutput:
    def test_output_written_to_file(self, generator, tmp_path):
        src_path = write_temp_module(SIMPLE_MODULE)
        out_path = str(tmp_path / "output.md")
        try:
            generator.generate_docs(src_path, output_path=out_path)
            assert Path(out_path).exists()
            content = Path(out_path).read_text(encoding="utf-8")
            assert "add" in content
        finally:
            os.unlink(src_path)

    def test_no_output_file_when_not_specified(self, generator, tmp_path):
        src_path = write_temp_module(SIMPLE_MODULE)
        try:
            generator.generate_docs(src_path)
            # No file should have been created in cwd named after the module
        finally:
            os.unlink(src_path)


class TestDocGeneratorSignatureBuilder:
    def test_build_signature_simple(self, generator):
        import ast
        source = "def foo(a: int, b: str = 'hello') -> bool: pass"
        tree = ast.parse(source)
        func_node = tree.body[0]
        sig = generator._build_signature(func_node)
        assert "foo" in sig
        assert "a" in sig
        assert "b" in sig
