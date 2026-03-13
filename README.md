# ai-dev-tools

**Open-source developer productivity toolkit** that automates common development workflows using Python.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Overview

`ai-dev-tools` helps open-source maintainers and developers automate repetitive tasks, including:

- **Issue Summarization** – Condense long GitHub issues into concise summaries.
- **Pull Request Description Generator** – Auto-generate structured PR descriptions from diffs or commit messages.
- **Code Review Suggestions** – Surface common code quality issues and best-practice violations.
- **Documentation Generator** – Generate module/function docstrings and README stubs from source code.

---

## Project Structure

```
ai-dev-tools/
├── src/                        # Core Python source modules
│   ├── __init__.py
│   ├── issue_summarizer.py     # Issue summarization tool
│   ├── pr_description.py       # PR description generator
│   ├── code_review.py          # Code review suggestion tool
│   └── doc_generator.py        # Documentation generator
├── docs/                       # Project documentation
│   ├── usage.md
│   └── api_reference.md
├── examples/                   # Runnable usage examples
│   ├── example_issue_summarizer.py
│   ├── example_pr_description.py
│   ├── example_code_review.py
│   └── example_doc_generator.py
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_issue_summarizer.py
│   ├── test_pr_description.py
│   ├── test_code_review.py
│   └── test_doc_generator.py
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- `pip` package manager

### Clone and Install

```bash
git clone https://github.com/anwershah668/ai-dev-tools.git
cd ai-dev-tools
pip install -r requirements.txt
```

---

## Usage

### Issue Summarizer

```python
from src.issue_summarizer import IssueSummarizer

summarizer = IssueSummarizer()
issue_text = """
Users are reporting that the login button does not respond on mobile Safari.
Steps to reproduce: open the app on iOS 16, tap Login.
Expected: login modal appears. Actual: nothing happens.
Additional context: works fine on Chrome Android.
"""
summary = summarizer.summarize(issue_text)
print(summary)
```

### Pull Request Description Generator

```python
from src.pr_description import PRDescriptionGenerator

generator = PRDescriptionGenerator()
diff = """
+ def calculate_tax(amount, rate):
+     return amount * rate / 100
"""
description = generator.generate(diff, commit_messages=["Add tax calculation utility"])
print(description)
```

### Code Review Tool

```python
from src.code_review import CodeReviewer

reviewer = CodeReviewer()
code = """
password = "hunter2"
def login(user, pwd):
    if pwd == password:
        return True
"""
suggestions = reviewer.review(code)
for suggestion in suggestions:
    print(suggestion)
```

### Documentation Generator

```python
from src.doc_generator import DocGenerator

generator = DocGenerator()
code = """
def add(a, b):
    return a + b
"""
docs = generator.generate(code)
print(docs)
```

---

## Running Examples

```bash
python examples/example_issue_summarizer.py
python examples/example_pr_description.py
python examples/example_code_review.py
python examples/example_doc_generator.py
```

---

## Running Tests

```bash
pip install pytest
pytest tests/
```

---

## Roadmap

- [x] Issue summarization
- [x] PR description generation
- [x] Code review suggestions
- [x] Documentation generation
- [ ] GitHub Actions integration
- [ ] CLI interface (`ai-dev-tools` command)
- [ ] LLM backend support (OpenAI, Ollama, Hugging Face)
- [ ] VS Code extension
- [ ] Slack/Discord bot integration

---

## Contributing

Contributions are very welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started, submit issues, and open pull requests.

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold these standards.

---

## License

This project is licensed under the [MIT License](LICENSE).

