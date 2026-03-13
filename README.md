# AI Dev Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Open-source developer productivity toolkit that automates common development workflows using Python.

AI Dev Tools helps open-source maintainers automate repetitive tasks like issue summarization, pull request descriptions, documentation generation, and code review suggestions.

## Features

- **Issue Summarizer** — Automatically summarize GitHub issues, categorize them, and estimate priority
- **PR Description Generator** — Generate structured pull request descriptions from git diffs
- **Code Reviewer** — Automated code review suggestions (long functions, missing docstrings, TODO tracking)
- **Documentation Generator** — Auto-generate Markdown docs from Python source code

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

# Install the package in development mode
pip install -e .
```

## Quick Start

### Issue Summarizer

```python
from ai_dev_tools.issue_summarizer import summarize_issue

result = summarize_issue(
    title="Login page crashes on Safari",
    body="When users try to log in using Safari, the page crashes with a TypeError.",
    labels=["bug", "critical"]
)
print(result)
# {'title': 'Login page crashes on Safari', 'summary': '...', 'category': 'bug', 'priority': 'high', ...}
```

### PR Description Generator

```python
from ai_dev_tools.pr_description import generate_pr_description

description = generate_pr_description(diff_text, title="Fix auth bug", branch_name="fix/auth")
print(description)
```

### Code Reviewer

```python
from ai_dev_tools.code_reviewer import review_code

result = review_code(open("my_file.py").read(), filename="my_file.py")
print(result["summary"])
```

### Documentation Generator

```python
from ai_dev_tools.doc_generator import generate_markdown_docs

docs = generate_markdown_docs(open("module.py").read(), module_name="module")
print(docs)
```

## Project Structure

```
ai-dev-tools/
├── src/ai_dev_tools/          # Core source code
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── issue_summarizer.py    # Issue summarization
│   ├── pr_description.py      # PR description generation
│   ├── code_reviewer.py       # Code review suggestions
│   └── doc_generator.py       # Documentation generation
├── tests/                     # Unit tests
├── examples/                  # Usage examples
├── docs/                      # Documentation
│   ├── architecture.md
│   └── usage.md
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── requirements.txt
└── setup.py
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Running Examples

```bash
python examples/example_issue_summarizer.py
python examples/example_code_reviewer.py
python examples/example_doc_generator.py
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Roadmap

- [ ] GitHub API integration for live issue/PR fetching
- [ ] AI-powered summarization using language models
- [ ] Support for more languages beyond Python
- [ ] GitHub Actions integration for automated reviews
- [ ] Plugin system for custom review rules
- [ ] Web dashboard for project health metrics

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
