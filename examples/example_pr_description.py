"""
Example: PR Description Generator
===================================
Demonstrates how to use PRDescriptionGenerator to create a structured pull
request description from a diff and commit messages.

Run with:
    python examples/example_pr_description.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.pr_description import PRDescriptionGenerator


SAMPLE_DIFF = """
--- a/src/utils.py
+++ b/src/utils.py
@@ -0,0 +1,8 @@
+def calculate_tax(amount, rate):
+    \"\"\"Return the tax amount for a given rate.
+
+    Args:
+        amount: The base amount.
+        rate: Tax rate as a percentage.
+
+    Returns:
+        Calculated tax value.
+    \"\"\"
+    return amount * rate / 100
+
"""


def main():
    generator = PRDescriptionGenerator()

    # --- Example 1: Feature PR with diff and commits ---
    print("=" * 60)
    print("EXAMPLE 1 – Feature PR")
    print("=" * 60)
    description = generator.generate(
        diff=SAMPLE_DIFF,
        commit_messages=[
            "feat: add calculate_tax utility function",
            "test: add unit tests for calculate_tax",
        ],
        pr_type="feature",
    )
    print(description)
    print()

    # --- Example 2: Bugfix PR with commits only ---
    print("=" * 60)
    print("EXAMPLE 2 – Bugfix PR (commits only)")
    print("=" * 60)
    description = generator.generate(
        commit_messages=["fix: handle division by zero in tax calculation"],
        pr_type="bugfix",
    )
    print(description)
    print()


if __name__ == "__main__":
    main()
