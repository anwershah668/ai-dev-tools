# Contributing to ai-dev-tools

Thank you for your interest in contributing! Every contribution — from bug reports to new features — makes this project better for everyone.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Running Tests](#running-tests)

---

## Code of Conduct

By participating in this project you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/ai-dev-tools.git
   cd ai-dev-tools
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Create a **feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## How to Contribute

### Reporting Bugs

- Search [existing issues](https://github.com/anwershah668/ai-dev-tools/issues) first.
- Open a new issue with a clear title and description.
- Include steps to reproduce, expected behavior, and actual behavior.
- Attach relevant logs or screenshots if applicable.

### Suggesting Features

- Open a GitHub issue with the label `enhancement`.
- Describe the problem the feature solves and your proposed solution.
- Keep the scope focused — smaller features are easier to review and merge.

### Submitting Pull Requests

1. Ensure your branch is up to date with `main`:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```
2. Write or update **tests** for the changes you make.
3. Make sure all tests pass:
   ```bash
   pytest tests/ -v
   ```
4. Write a clear PR description explaining *what* you changed and *why*.
5. Reference any related issues (e.g., `Closes #42`).

---

## Development Workflow

```
main              ← stable, release-ready code
  └── feature/*   ← your feature branches
  └── fix/*       ← bug fix branches
  └── docs/*      ← documentation-only changes
```

- Keep commits small and focused.
- Use descriptive commit messages following the format:
  ```
  <type>: <short description>

  <optional longer description>
  ```
  Where `<type>` is one of: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.

---

## Coding Standards

- Follow [PEP 8](https://pep8.org/) for Python style.
- Use type hints where practical.
- Write docstrings for every public class and function (Google style preferred).
- Keep functions short and single-purpose.

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=src --cov-report=term-missing
```

All CI checks must pass before a PR can be merged.

---

Thank you for helping make **ai-dev-tools** better! 🎉
