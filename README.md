# ai-dev-tools

> **Open-source developer productivity toolkit** that automates common development workflows using Python.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Overview

`ai-dev-tools` helps open-source maintainers automate repetitive tasks so they can focus on what matters — shipping great software. The toolkit ships as a set of standalone Python scripts that can be used individually or composed into larger automation pipelines.

### Features

| Tool | Description |
|------|-------------|
| **Issue Summarizer** | Condenses long GitHub issue threads into a short, actionable summary |
| **PR Description Generator** | Generates a structured pull-request description from a git diff |
| **Code Review Tool** | Provides style, complexity, and best-practice suggestions for Python files |
| **Documentation Generator** | Extracts docstrings and produces Markdown documentation for a module |

---

## Project Structure

```
ai-dev-tools/
├── src/                        # Core library modules
│   ├── __init__.py
│   ├── issue_summarizer.py     # Issue summarization tool
│   ├── pr_description_generator.py  # PR description generator
│   ├── code_review_tool.py     # Code review suggestion tool
│   └── doc_generator.py        # Documentation generator
├── examples/                   # Runnable usage examples
│   ├── example_issue_summarizer.py
│   ├── example_pr_description.py
│   ├── example_code_review.py
│   └── example_doc_generator.py
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_issue_summarizer.py
│   ├── test_pr_description_generator.py
│   ├── test_code_review_tool.py
│   └── test_doc_generator.py
├── docs/                       # Extended documentation
│   └── usage.md
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/anwershah668/ai-dev-tools.git
cd ai-dev-tools

# (Recommended) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Issue Summarizer

Summarizes a list of GitHub-style issue comments into a concise summary.

```python
from src.issue_summarizer import IssueSummarizer

comments = [
    "The login button is broken on mobile devices.",
    "I can reproduce this on iOS 16 and Android 13.",
    "Looks like the CSS media query is incorrect.",
    "PR #42 should fix this.",
]

summarizer = IssueSummarizer()
print(summarizer.summarize(comments))
```

### PR Description Generator

Generates a structured PR description from a git diff string.

```python
from src.pr_description_generator import PRDescriptionGenerator

diff = """
diff --git a/src/auth.py b/src/auth.py
--- a/src/auth.py
+++ b/src/auth.py
@@ -10,6 +10,8 @@ def login(user, password):
+    if not user or not password:
+        raise ValueError("Credentials must not be empty")
"""

generator = PRDescriptionGenerator()
print(generator.generate(diff))
```

### Code Review Tool

Analyses a Python source file and returns improvement suggestions.

```python
from src.code_review_tool import CodeReviewTool

reviewer = CodeReviewTool()
suggestions = reviewer.review_file("src/auth.py")
for s in suggestions:
    print(s)
```

### Documentation Generator

Extracts docstrings from a Python module and outputs Markdown docs.

```python
from src.doc_generator import DocGenerator

generator = DocGenerator()
docs = generator.generate_docs("src/issue_summarizer.py")
print(docs)
```

---

## Running Examples

Each script in `examples/` is self-contained and can be run directly:

```bash
python examples/example_issue_summarizer.py
python examples/example_pr_description.py
python examples/example_code_review.py
python examples/example_doc_generator.py
```

---

## Running Tests

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Roadmap

- [ ] GitHub Actions integration for automated PR descriptions
- [ ] OpenAI / LLM backend for smarter summaries and reviews
- [ ] CLI wrapper (`aidev` command) via `argparse`
- [ ] Support for non-Python languages in the code review tool
- [ ] Web dashboard for viewing generated reports

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## License

Released under the [MIT License](LICENSE). Copyright © 2026 Anwer Shah.
