# Usage Guide

This guide provides detailed usage instructions for each tool in the `ai-dev-tools` toolkit.

---

## Table of Contents

1. [Issue Summarizer](#issue-summarizer)
2. [PR Description Generator](#pr-description-generator)
3. [Code Review Tool](#code-review-tool)
4. [Documentation Generator](#documentation-generator)

---

## Issue Summarizer

**Module:** `src/issue_summarizer.py`  
**Class:** `IssueSummarizer`

### What it does

The issue summarizer takes a list of comment strings from a GitHub issue thread and returns a concise plain-text summary including:
- A representative headline sentence
- The key topics/keywords mentioned across all comments
- A note about the total number of contributions

It uses an extractive approach — no external API or LLM required.

### API

```python
IssueSummarizer.summarize(comments: List[str], top_keywords: int = 5) -> str
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `comments` | `List[str]` | List of comment strings |
| `top_keywords` | `int` | Number of keywords to surface (default: 5) |

### Example

```python
from src.issue_summarizer import IssueSummarizer

summarizer = IssueSummarizer()
result = summarizer.summarize([
    "The login button is broken on mobile.",
    "Reproduced on iOS and Android.",
    "The CSS media query is incorrect.",
])
print(result)
```

**Output:**
```
Summary (3 comments):
  The CSS media query is incorrect.
Key topics: login, button, mobile, css, broken.
```

---

## PR Description Generator

**Module:** `src/pr_description_generator.py`  
**Class:** `PRDescriptionGenerator`

### What it does

Parses a unified git diff and generates a structured Markdown pull-request description template that includes:
- A summary of files changed and line counts
- A per-file breakdown (with new/deleted/renamed labels)
- Sections for motivation, testing checklist, and related issues

### API

```python
PRDescriptionGenerator.generate(diff: str, title: Optional[str] = None) -> str
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `diff` | `str` | Unified git diff string |
| `title` | `Optional[str]` | Optional PR title |

### Example

```python
import subprocess
from src.pr_description_generator import PRDescriptionGenerator

diff = subprocess.check_output(["git", "diff", "HEAD~1"], text=True)
generator = PRDescriptionGenerator()
print(generator.generate(diff, title="feat: add new feature"))
```

---

## Code Review Tool

**Module:** `src/code_review_tool.py`  
**Class:** `CodeReviewTool`

### What it does

Performs lightweight static analysis on Python source code and returns a list of `Suggestion` objects covering:

| Category | Checks |
|----------|--------|
| **Style** | Lines over 99 chars, trailing whitespace |
| **Complexity** | Functions with >5 args, high branch count |
| **Best Practice** | Bare `except`, mutable default arguments |
| **Documentation** | Missing docstrings on public functions/classes |

### API

```python
# Review a file
CodeReviewTool.review_file(filepath: str) -> List[Suggestion]

# Review source code directly
CodeReviewTool.review(source: str) -> List[Suggestion]
```

### Suggestion object

```python
@dataclass
class Suggestion:
    line: Optional[int]   # Line number (None for general suggestions)
    category: str         # "Style", "Complexity", "Best Practice", "Documentation"
    message: str          # Human-readable message
```

### Example

```python
from src.code_review_tool import CodeReviewTool

reviewer = CodeReviewTool()
for s in reviewer.review_file("mymodule.py"):
    print(s)
# [Style] Line 42: Line is 120 characters (limit: 99).
# [Best Practice] Line 10: Bare 'except' clause catches all exceptions...
```

---

## Documentation Generator

**Module:** `src/doc_generator.py`  
**Class:** `DocGenerator`

### What it does

Parses a Python module using the `ast` module and generates a Markdown documentation page containing:
- Module-level docstring
- All public classes with docstrings and method listings
- All public top-level functions with signatures and docstrings

### API

```python
DocGenerator.generate_docs(filepath: str, output_path: Optional[str] = None) -> str
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `filepath` | `str` | Path to the Python source file |
| `output_path` | `Optional[str]` | If provided, the Markdown is also written to this file |

### Example

```python
from src.doc_generator import DocGenerator

gen = DocGenerator()
# Print to console
print(gen.generate_docs("src/issue_summarizer.py"))

# Save to docs/
gen.generate_docs("src/issue_summarizer.py", output_path="docs/issue_summarizer.md")
```

---

## Running All Examples

```bash
python examples/example_issue_summarizer.py
python examples/example_pr_description.py
python examples/example_code_review.py
python examples/example_doc_generator.py
```

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v --cov=src --cov-report=term-missing
```
