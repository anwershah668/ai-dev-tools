"""Tests for the PR Description Generator module."""

from ai_dev_tools.pr_description import (
    parse_diff_stats,
    classify_change_type,
    generate_pr_description,
)

SAMPLE_DIFF = """diff --git a/src/main.py b/src/main.py
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,5 @@
+import os
+import sys
 def main():
-    print("hello")
+    print("hello world")
     return 0
diff --git a/tests/test_main.py b/tests/test_main.py
--- /dev/null
+++ b/tests/test_main.py
@@ -0,0 +1,5 @@
+def test_main():
+    assert True
+
+def test_other():
+    assert 1 == 1
"""


class TestParseDiffStats:
    def test_empty_diff(self):
        result = parse_diff_stats("")
        assert result["files_changed"] == 0
        assert result["insertions"] == 0
        assert result["deletions"] == 0

    def test_sample_diff(self):
        result = parse_diff_stats(SAMPLE_DIFF)
        assert result["files_changed"] == 2
        assert result["insertions"] == 8
        assert result["deletions"] == 1
        assert len(result["files"]) == 2

    def test_file_paths_extracted(self):
        result = parse_diff_stats(SAMPLE_DIFF)
        paths = [f["path"] for f in result["files"]]
        assert "src/main.py" in paths
        assert "tests/test_main.py" in paths


class TestClassifyChangeType:
    def test_feature(self):
        files = [
            {"path": "src/feature.py", "insertions": 10, "deletions": 0},
            {"path": "tests/test_feature.py", "insertions": 5, "deletions": 0},
        ]
        assert classify_change_type(files) == "feature"

    def test_docs(self):
        files = [{"path": "README.md", "insertions": 5, "deletions": 2}]
        assert classify_change_type(files) == "docs"

    def test_bugfix(self):
        files = [{"path": "src/fix.py", "insertions": 2, "deletions": 1}]
        assert classify_change_type(files) == "bugfix"

    def test_empty(self):
        assert classify_change_type([]) == "unknown"

    def test_test_only(self):
        files = [{"path": "tests/test_new.py", "insertions": 10, "deletions": 0}]
        assert classify_change_type(files) == "test"

    def test_chore(self):
        files = [{"path": "requirements.txt", "insertions": 1, "deletions": 0}]
        assert classify_change_type(files) == "chore"


class TestGeneratePrDescription:
    def test_generates_markdown(self):
        result = generate_pr_description(SAMPLE_DIFF, title="Add new feature")
        assert "## Add new feature" in result
        assert "### Summary" in result
        assert "### Files Changed" in result
        assert "### Checklist" in result

    def test_includes_stats(self):
        result = generate_pr_description(SAMPLE_DIFF)
        assert "2" in result  # files changed
        assert "8" in result  # insertions

    def test_includes_branch(self):
        result = generate_pr_description(SAMPLE_DIFF, branch_name="feature/new")
        assert "`feature/new`" in result

    def test_empty_diff(self):
        result = generate_pr_description("")
        assert "0" in result
