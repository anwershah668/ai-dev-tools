# API Reference

Full API reference for all public classes and methods in **ai-dev-tools**.

---

## `src.issue_summarizer.IssueSummarizer`

```
class IssueSummarizer
```

Summarize GitHub issue text into structured bullet-point summaries.

### Methods

#### `summarize(issue_text: str) -> str`

Return a concise, structured summary of a GitHub issue.

| Parameter | Type | Description |
|-----------|------|-------------|
| `issue_text` | `str` | Raw issue text (title + body). |

**Returns:** Multi-line Markdown string with the structured summary.

**Raises:** `ValueError` – if `issue_text` is empty.

---

## `src.pr_description.PRDescriptionGenerator`

```
class PRDescriptionGenerator
```

Generate a structured pull request description from a diff and commit messages.

### Methods

#### `generate(diff: str = "", commit_messages: list = None, pr_type: str = "feature") -> str`

Return a Markdown PR description.

| Parameter | Type | Description |
|-----------|------|-------------|
| `diff` | `str` | Unified diff string (optional). |
| `commit_messages` | `list[str]` | List of commit message strings (optional). |
| `pr_type` | `str` | `"feature"`, `"bugfix"`, `"docs"`, `"refactor"`, or `"chore"`. |

**Returns:** Multi-line Markdown string suitable for a GitHub PR body.

**Raises:** `ValueError` – if both `diff` and `commit_messages` are empty.

---

## `src.code_review.CodeReviewer`

```
class CodeReviewer
```

Perform lightweight static analysis on Python source code.

### Methods

#### `review(source_code: str) -> list[ReviewSuggestion]`

Analyse source code and return a list of suggestions.

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_code` | `str` | Python source code as a string. |

**Returns:** List of `ReviewSuggestion` objects sorted by line number.

**Raises:** `ValueError` – if `source_code` is empty.

---

## `src.code_review.ReviewSuggestion`

```
@dataclass
class ReviewSuggestion
```

A single code review finding.

| Attribute | Type | Description |
|-----------|------|-------------|
| `line` | `int` | 1-based line number (0 if not applicable). |
| `severity` | `str` | `"error"`, `"warning"`, or `"info"`. |
| `rule` | `str` | Short rule identifier. |
| `message` | `str` | Human-readable description. |

---

## `src.doc_generator.DocGenerator`

```
class DocGenerator
```

Generate documentation stubs for Python source code.

### Methods

#### `generate(source_code: str) -> str`

Generate a Markdown documentation report.

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_code` | `str` | Valid Python source code as a string. |

**Returns:** Markdown-formatted documentation report.

**Raises:** `ValueError` – if empty; `SyntaxError` – if source cannot be parsed.

#### `generate_docstring(func_name: str, args: list[str], has_return: bool = True) -> str`

Generate a Google-style docstring stub for a single function.

| Parameter | Type | Description |
|-----------|------|-------------|
| `func_name` | `str` | Name of the function. |
| `args` | `list[str]` | List of argument names (excluding `self`/`cls`). |
| `has_return` | `bool` | Whether the function returns a value (default `True`). |

**Returns:** Formatted docstring stub string.
