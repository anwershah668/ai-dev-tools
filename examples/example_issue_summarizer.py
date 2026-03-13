"""
Example: Issue Summarizer
=========================
Demonstrates how to use IssueSummarizer to condense a GitHub issue into a
structured summary.

Run with:
    python examples/example_issue_summarizer.py
"""

import sys
import os

# Allow running from the project root without installing the package.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.issue_summarizer import IssueSummarizer


def main():
    summarizer = IssueSummarizer()

    # --- Example 1: Mobile bug report ---
    issue_1 = """
    Login button does not work on mobile Safari iOS 16.

    Steps to reproduce:
    1. Open the app on an iPhone running iOS 16.
    2. Tap the Login button.
    3. Observe nothing happens.

    Expected behavior: The login modal should appear.
    Actual behavior: Nothing happens; no error message is shown.

    Environment: iPhone 13, iOS 16.2, Safari 16.
    """

    print("=" * 60)
    print("EXAMPLE 1 – Mobile Bug Report")
    print("=" * 60)
    print(summarizer.summarize(issue_1))
    print()

    # --- Example 2: Feature request ---
    issue_2 = """
    Feature request: Add dark mode support.

    Many users have requested a dark mode option. The current bright white
    background is hard on the eyes in low-light environments.

    Expected behavior: Users can toggle dark mode in Settings.
    Actual behavior: No dark mode option exists.
    """

    print("=" * 60)
    print("EXAMPLE 2 – Feature Request")
    print("=" * 60)
    print(summarizer.summarize(issue_2))
    print()


if __name__ == "__main__":
    main()
