"""Unit tests for src.pr_description."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.pr_description import PRDescriptionGenerator


SAMPLE_DIFF = """\
--- a/src/utils.py
+++ b/src/utils.py
@@ -0,0 +1,3 @@
+def hello():
+    return "hello"
+
"""


class TestPRDescriptionGeneratorBasic(unittest.TestCase):
    def setUp(self):
        self.gen = PRDescriptionGenerator()

    def test_generate_with_diff_and_commits(self):
        result = self.gen.generate(
            diff=SAMPLE_DIFF,
            commit_messages=["feat: add hello function"],
        )
        self.assertIn("## Pull Request", result)
        self.assertIn("feat: add hello function", result)

    def test_generate_with_commits_only(self):
        result = self.gen.generate(commit_messages=["fix: correct typo"])
        self.assertIn("fix: correct typo", result)

    def test_generate_with_diff_only(self):
        result = self.gen.generate(diff=SAMPLE_DIFF)
        self.assertIn("## Pull Request", result)

    def test_empty_inputs_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.gen.generate()

    def test_none_commits_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.gen.generate(diff="", commit_messages=None)

    def test_changed_files_in_output(self):
        result = self.gen.generate(diff=SAMPLE_DIFF)
        self.assertIn("src/utils.py", result)

    def test_diff_stats_in_output(self):
        result = self.gen.generate(diff=SAMPLE_DIFF)
        self.assertIn("Diff stats:", result)

    def test_testing_checklist_present(self):
        result = self.gen.generate(commit_messages=["chore: update deps"])
        self.assertIn("### Testing", result)
        self.assertIn("- [ ]", result)

    def test_pr_type_in_output(self):
        result = self.gen.generate(
            commit_messages=["fix: patch vulnerability"],
            pr_type="bugfix",
        )
        self.assertIn("Bugfix", result)

    def test_returns_string(self):
        result = self.gen.generate(commit_messages=["docs: update readme"])
        self.assertIsInstance(result, str)

    def test_multiple_commits(self):
        commits = ["feat: add feature A", "feat: add feature B", "test: add tests"]
        result = self.gen.generate(commit_messages=commits)
        for msg in commits:
            self.assertIn(msg, result)

    def test_summary_derived_from_first_commit(self):
        result = self.gen.generate(commit_messages=["feat: implement caching layer"])
        # Conventional prefix stripped: "feat:" removed, "Implement..." capitalised
        self.assertIn("Implement caching layer", result)


if __name__ == "__main__":
    unittest.main()
