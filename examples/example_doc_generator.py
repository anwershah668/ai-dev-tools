"""
Example: Documentation Generator
==================================
Demonstrates how to use DocGenerator to generate docstring stubs and a README
stub for Python source code.

Run with:
    python examples/example_doc_generator.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.doc_generator import DocGenerator


UNDOCUMENTED_CODE = '''
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


class Calculator:
    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero.")
        return x / y
'''

DOCUMENTED_CODE = '''
"""Utility module for arithmetic operations."""


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


def main():
    gen = DocGenerator()

    print("=" * 60)
    print("EXAMPLE 1 – Code Without Docstrings")
    print("=" * 60)
    print(gen.generate(UNDOCUMENTED_CODE))
    print()

    print("=" * 60)
    print("EXAMPLE 2 – Code With Docstrings")
    print("=" * 60)
    print(gen.generate(DOCUMENTED_CODE))
    print()

    print("=" * 60)
    print("EXAMPLE 3 – Single Function Docstring Stub")
    print("=" * 60)
    stub = gen.generate_docstring(
        func_name="calculate_discount",
        args=["price", "discount_pct"],
        has_return=True,
    )
    print(stub)


if __name__ == "__main__":
    main()
