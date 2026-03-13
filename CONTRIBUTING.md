# Contributing to ai-dev-tools

Thank you for your interest in contributing to **ai-dev-tools**! This document explains how you can help improve the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Commit Message Guidelines](#commit-message-guidelines)

---

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a welcoming and inclusive community.

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/ai-dev-tools.git
   cd ai-dev-tools
   ```
3. **Create a branch** for your change:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Contribute

### Reporting Bugs

- Search [existing issues](https://github.com/anwershah668/ai-dev-tools/issues) to avoid duplicates.
- Open a new issue with:
  - A clear, descriptive title.
  - Steps to reproduce the problem.
  - Expected vs. actual behavior.
  - Your environment (OS, Python version).

### Suggesting Features

- Open a new issue with the label `enhancement`.
- Describe the feature and its use case clearly.
- If possible, include example code or a mockup.

### Submitting Pull Requests

1. Make sure your branch is up to date with `main`:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```
2. Write tests for any new functionality (see [Testing](#testing)).
3. Ensure all existing tests pass:
   ```bash
   pytest tests/
   ```
4. Push your branch and open a PR against `main`.
5. Fill in the PR template with a description of your changes.
6. A maintainer will review your PR within a few days.

---

## Development Setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

---

## Coding Standards

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style.
- Write clear docstrings for all public functions and classes (Google-style).
- Keep functions small and focused (single responsibility).
- Avoid unnecessary dependencies.

---

## Testing

- All new features must have corresponding unit tests in the `tests/` directory.
- Tests use the standard `unittest` module (compatible with `pytest`).
- Run the full test suite with:
  ```bash
  pytest tests/
  ```

---

## Commit Message Guidelines

Use clear and descriptive commit messages following this convention:

```
<type>: <short description>

[Optional longer description]
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

Examples:
- `feat: add PR description generator`
- `fix: handle empty input in issue summarizer`
- `docs: update README usage section`
- `test: add tests for code review tool`

---

Thank you for helping make **ai-dev-tools** better! 🚀
