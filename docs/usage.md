# Usage Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/anwershah668/ai-dev-tools.git
cd ai-dev-tools

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Issue Summarizer

The Issue Summarizer helps triage GitHub issues by extracting key information.

```python
from ai_dev_tools.issue_summarizer import summarize_issue

result = summarize_issue(
    title="Login page crashes on Safari",
    body="When users try to log in using Safari 17, the page crashes. "
         "Error: TypeError in auth module. This is a critical bug.",
    labels=["bug", "critical"]
)

print(result)
# {
#     'title': 'Login page crashes on Safari',
#     'summary': 'When users try to log in using Safari 17, the page crashes...',
#     'category': 'bug',
#     'priority': 'high',
#     'label_count': 2
# }
```

## PR Description Generator

Automatically generate pull request descriptions from git diffs.

```python
from ai_dev_tools.pr_description import generate_pr_description

diff = """diff --git a/src/auth.py b/src/auth.py
--- a/src/auth.py
+++ b/src/auth.py
@@ -10,3 +10,5 @@
+def validate_token(token):
+    return token is not None
"""

description = generate_pr_description(
    diff,
    title="Fix authentication validation",
    branch_name="fix/auth-validation"
)
print(description)
```

## Code Reviewer

Get automated code review suggestions for Python code.

```python
from ai_dev_tools.code_reviewer import review_code

source = open("my_file.py").read()
result = review_code(source, filename="my_file.py")

print(f"Issues found: {result['total_issues']}")
print(f"Summary: {result['summary']}")

for issue in result["missing_docstrings"]:
    print(f"  Line {issue['line']}: {issue['suggestion']}")
```

## Documentation Generator

Generate Markdown documentation from Python source code.

```python
from ai_dev_tools.doc_generator import generate_markdown_docs

source = open("my_module.py").read()
docs = generate_markdown_docs(source, module_name="my_module")

# Write to file
with open("docs/my_module.md", "w") as f:
    f.write(docs)
```

## Running Examples

```bash
python examples/example_issue_summarizer.py
python examples/example_code_reviewer.py
python examples/example_doc_generator.py
```
