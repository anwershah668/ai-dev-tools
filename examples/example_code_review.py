"""
Example: Code Review Tool
==========================
Demonstrates how to use CodeReviewer to detect common Python code quality
issues and best-practice violations.

Run with:
    python examples/example_code_review.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.code_review import CodeReviewer


PROBLEMATIC_CODE = '''
import os

# TODO: move to config file
DB_PASSWORD = "s3cr3t_password"

def fetch_data(items=[]):
    """Fetch data items."""
    try:
        result = eval("items")
        return result
    except:
        pass

def process(x, y):
    return x + y
'''

CLEAN_CODE = '''
import os


def fetch_data(items=None):
    """Fetch data items from the database.

    Args:
        items: Optional list of item IDs to fetch.

    Returns:
        List of fetched data items.
    """
    if items is None:
        items = []
    try:
        return items
    except ValueError as exc:
        raise RuntimeError("Fetch failed") from exc


def process(x, y):
    """Add two numbers together.

    Args:
        x: First operand.
        y: Second operand.

    Returns:
        Sum of x and y.
    """
    return x + y
'''


def main():
    reviewer = CodeReviewer()

    print("=" * 60)
    print("EXAMPLE 1 – Code with Issues")
    print("=" * 60)
    suggestions = reviewer.review(PROBLEMATIC_CODE)
    if suggestions:
        for s in suggestions:
            print(s)
    else:
        print("No issues found.")
    print()

    print("=" * 60)
    print("EXAMPLE 2 – Clean Code")
    print("=" * 60)
    suggestions = reviewer.review(CLEAN_CODE)
    if suggestions:
        for s in suggestions:
            print(s)
    else:
        print("✅ No issues found – code looks good!")
    print()


if __name__ == "__main__":
    main()
