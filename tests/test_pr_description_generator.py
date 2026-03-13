"""Unit tests for PRDescriptionGenerator."""

import pytest
from src.pr_description_generator import PRDescriptionGenerator, FileSummary


SIMPLE_DIFF = """\
diff --git a/src/auth.py b/src/auth.py
index 1234567..abcdefg 100644
--- a/src/auth.py
+++ b/src/auth.py
@@ -10,6 +10,8 @@ def login(user, password):
+    if not user:
+        raise ValueError("user must not be empty")
"""

NEW_FILE_DIFF = """\
diff --git a/src/new_module.py b/src/new_module.py
new file mode 100644
index 0000000..1111111
--- /dev/null
+++ b/src/new_module.py
@@ -0,0 +1,5 @@
+\"\"\"New module.\"\"\"
+
+
+def hello():
+    return "Hello, world!"
"""

DELETED_FILE_DIFF = """\
diff --git a/src/old_module.py b/src/old_module.py
deleted file mode 100644
index 2222222..0000000
--- a/src/old_module.py
+++ /dev/null
@@ -1,3 +0,0 @@
-\"\"\"Old module.\"\"\"
-def goodbye():
-    pass
"""


@pytest.fixture
def generator():
    return PRDescriptionGenerator()


class TestPRDescriptionGeneratorBasic:
    def test_returns_string(self, generator):
        result = generator.generate(SIMPLE_DIFF)
        assert isinstance(result, str)

    def test_contains_summary_section(self, generator):
        result = generator.generate(SIMPLE_DIFF)
        assert "### Summary" in result

    def test_contains_changes_section(self, generator):
        result = generator.generate(SIMPLE_DIFF)
        assert "### Changes" in result

    def test_contains_filename(self, generator):
        result = generator.generate(SIMPLE_DIFF)
        assert "src/auth.py" in result

    def test_custom_title_appears(self, generator):
        result = generator.generate(SIMPLE_DIFF, title="feat: add validation")
        assert "feat: add validation" in result

    def test_default_title_used_when_none(self, generator):
        result = generator.generate(SIMPLE_DIFF)
        assert "##" in result  # Some title present

    def test_empty_diff_raises(self, generator):
        with pytest.raises(ValueError):
            generator.generate("")

    def test_whitespace_only_diff_raises(self, generator):
        with pytest.raises(ValueError):
            generator.generate("   \n  ")


class TestPRDescriptionGeneratorParsing:
    def test_new_file_labeled(self, generator):
        result = generator.generate(NEW_FILE_DIFF)
        assert "new file" in result

    def test_deleted_file_labeled(self, generator):
        result = generator.generate(DELETED_FILE_DIFF)
        assert "deleted" in result

    def test_addition_count(self, generator):
        summaries = generator._parse_diff(SIMPLE_DIFF)
        assert len(summaries) == 1
        assert summaries[0].additions == 2

    def test_deletion_count(self, generator):
        summaries = generator._parse_diff(DELETED_FILE_DIFF)
        assert summaries[0].deletions == 3

    def test_multi_file_diff(self, generator):
        combined = SIMPLE_DIFF + "\n" + NEW_FILE_DIFF
        summaries = generator._parse_diff(combined)
        assert len(summaries) == 2

    def test_hunk_count(self, generator):
        summaries = generator._parse_diff(SIMPLE_DIFF)
        assert summaries[0].hunks == 1
