# Usage Guide

This guide covers all four tools included in **ai-dev-tools**.

---

## Table of Contents

1. [Issue Summarizer](#1-issue-summarizer)
2. [PR Description Generator](#2-pr-description-generator)
3. [Code Review Tool](#3-code-review-tool)
4. [Documentation Generator](#4-documentation-generator)

---

## 1. Issue Summarizer

The `IssueSummarizer` class parses raw issue text and produces a structured
summary with sections for the problem statement, reproduction steps, expected
vs. actual behavior, and environment details.

### Basic Example

```python
from src.issue_summarizer import IssueSummarizer

summarizer = IssueSummarizer()

issue_text = """
Login button does not work on mobile Safari iOS 16.

Steps to reproduce:
1. Open the app on an iPhone running iOS 16.
2. Tap the Login button.

Expected behavior: The login modal should appear.
Actual behavior: Nothing happens; no error is shown.

Environment: iPhone 13, iOS 16.2, Safari 16.
"""

print(summarizer.summarize(issue_text))
```

### Output

```
## Issue Summary

**Problem:** Login button does not work on mobile Safari iOS 16.

**Steps to Reproduce:**
  - Open the app on an iPhone running iOS 16.
  - Tap the Login button.

**Expected:** The login modal should appear.

**Actual:** Nothing happens; no error is shown.

**Environment:** iPhone 13, iOS 16.2, Safari 16.
```

---

## 2. PR Description Generator

The `PRDescriptionGenerator` class accepts a unified diff string and/or a list
of commit messages and produces a Markdown PR body ready to paste into GitHub.

### Basic Example

```python
from src.pr_description import PRDescriptionGenerator

generator = PRDescriptionGenerator()

diff = """
--- a/src/utils.py
+++ b/src/utils.py
@@ -0,0 +1,4 @@
+def calculate_tax(amount, rate):
+    \"\"\"Return tax amount.\"\"\"
+    return amount * rate / 100
+
"""

description = generator.generate(
    diff=diff,
    commit_messages=["feat: add calculate_tax utility function"],
    pr_type="feature",
)
print(description)
```

---

## 3. Code Review Tool

The `CodeReviewer` class performs lightweight static analysis on Python source
code and returns a list of `ReviewSuggestion` objects.

### Detected Issues

| Rule | Severity | Description |
|------|----------|-------------|
| `hardcoded-secret` | error | Password / API key assigned as a string literal |
| `eval-exec` | error | Use of `eval()` or `exec()` |
| `broad-except` | warning | Bare `except:` or `except Exception:` |
| `missing-docstring` | info | Public function / method without a docstring |
| `mutable-default-arg` | warning | List / dict / set as a default argument value |
| `todo-comment` | info | TODO / FIXME / HACK comment |
| `line-too-long` | warning | Line exceeds 120 characters |

### Basic Example

```python
from src.code_review import CodeReviewer

reviewer = CodeReviewer()

code = """
API_KEY = "abc123secret"

def process(data=[]):
    try:
        result = eval(data)
    except:
        pass
"""

suggestions = reviewer.review(code)
for s in suggestions:
    print(s)
```

---

## 4. Documentation Generator

The `DocGenerator` class analyses Python source code and generates a Markdown
report containing a module overview and Google-style docstring stubs for every
public symbol that lacks documentation.

### Basic Example

```python
from src.doc_generator import DocGenerator

gen = DocGenerator()

code = """
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
"""

print(gen.generate(code))
```
