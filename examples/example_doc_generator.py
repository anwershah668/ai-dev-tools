#!/usr/bin/env python3
"""Example: Using the Documentation Generator.

This example demonstrates how to use the doc_generator module
to auto-generate Markdown documentation from Python source code.
"""

from ai_dev_tools.doc_generator import generate_markdown_docs


def main():
    # Sample source code to generate docs for
    sample_source = '''"""Math utilities for common calculations."""

def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The sum of a and b.
    """
    return a + b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The product of a and b.
    """
    return a * b


class Statistics:
    """Statistical calculations on a dataset."""

    def __init__(self, data: list):
        """Initialize with a list of numbers."""
        self.data = data

    def mean(self) -> float:
        """Calculate the arithmetic mean."""
        return sum(self.data) / len(self.data)

    def total(self) -> float:
        """Calculate the sum of all values."""
        return sum(self.data)
'''

    print("=== Generated Documentation ===")
    print()
    docs = generate_markdown_docs(sample_source, module_name="math_utils")
    print(docs)


if __name__ == "__main__":
    main()
