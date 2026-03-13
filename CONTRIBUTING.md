# Contributing to AI Dev Tools

Thank you for your interest in contributing to AI Dev Tools! This guide will help you get started.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:

- A clear description of the bug
- Steps to reproduce the behavior
- Expected behavior
- Screenshots or logs if applicable
- Your environment (OS, Python version)

### Suggesting Features

We welcome feature requests! Please open an issue with:

- A clear description of the feature
- Why it would be useful
- Any implementation ideas you have

### Submitting Pull Requests

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and write tests
5. **Run the tests** to ensure everything passes:
   ```bash
   python -m pytest tests/
   ```
6. **Commit** your changes with a clear message:
   ```bash
   git commit -m "Add: description of your change"
   ```
7. **Push** to your fork and open a Pull Request

### Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints where possible
- Write docstrings for all public functions and classes
- Keep functions focused and small

### Testing

- Write unit tests for new features
- Ensure all existing tests pass before submitting
- Aim for good test coverage

## Development Setup

```bash
# Clone the repository
git clone https://github.com/anwershah668/ai-dev-tools.git
cd ai-dev-tools

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

## Project Structure

```
ai-dev-tools/
├── src/ai_dev_tools/     # Core source code
│   ├── issue_summarizer.py
│   ├── pr_description.py
│   ├── code_reviewer.py
│   ├── doc_generator.py
│   └── cli.py
├── docs/                  # Documentation
├── examples/              # Usage examples
├── tests/                 # Unit tests
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── requirements.txt
└── setup.py
```

## Questions?

Feel free to open an issue or reach out if you have any questions. We're happy to help!
