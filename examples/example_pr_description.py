"""Example: using PRDescriptionGenerator to generate a PR description from a diff."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.pr_description_generator import PRDescriptionGenerator


SAMPLE_DIFF = """\
diff --git a/src/auth.py b/src/auth.py
index 1234567..abcdefg 100644
--- a/src/auth.py
+++ b/src/auth.py
@@ -10,6 +10,10 @@ def login(user, password):
     \"\"\"Authenticate a user.\"\"\"
+    if not user or not password:
+        raise ValueError("Credentials must not be empty")
+
+    user = user.strip()
     return _verify(user, password)

diff --git a/tests/test_auth.py b/tests/test_auth.py
new file mode 100644
index 0000000..9876543
--- /dev/null
+++ b/tests/test_auth.py
@@ -0,0 +1,15 @@
+import pytest
+from src.auth import login
+
+
+def test_login_empty_user_raises():
+    with pytest.raises(ValueError):
+        login("", "secret")
+
+
+def test_login_empty_password_raises():
+    with pytest.raises(ValueError):
+        login("alice", "")
+
+
+def test_login_strips_whitespace():
+    assert login("  alice  ", "secret") is not None
"""


def main():
    generator = PRDescriptionGenerator()
    description = generator.generate(
        SAMPLE_DIFF,
        title="fix: validate and sanitize login credentials",
    )
    print(description)


if __name__ == "__main__":
    main()
