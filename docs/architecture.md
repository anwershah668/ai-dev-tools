# AI Dev Tools - Architecture

## Overview

AI Dev Tools is a Python toolkit that automates common developer workflows. The project provides four core tools, each as an independent module.

## Module Architecture

```
src/ai_dev_tools/
├── __init__.py           # Package initialization and version
├── cli.py                # Command-line interface
├── issue_summarizer.py   # Issue summarization logic
├── pr_description.py     # PR description generation
├── code_reviewer.py      # Automated code review
└── doc_generator.py      # Documentation generation
```

## Core Modules

### Issue Summarizer (`issue_summarizer.py`)

Analyzes GitHub issue titles, bodies, and labels to produce:
- Concise summaries by extracting key sentences
- Automatic categorization (bug, feature, docs, question)
- Priority estimation (high, medium, low)

### PR Description Generator (`pr_description.py`)

Parses unified diffs to generate structured PR descriptions including:
- File change statistics (insertions, deletions)
- Change type classification (feature, bugfix, docs, etc.)
- Formatted Markdown output with checklists

### Code Reviewer (`code_reviewer.py`)

Static analysis tool that checks for:
- Long functions exceeding configurable line limits
- Missing docstrings on functions and classes
- TODO/FIXME comments that need attention

### Documentation Generator (`doc_generator.py`)

Extracts and formats documentation from Python source:
- Function signatures, arguments, return types
- Class definitions and inheritance
- Docstrings formatted as Markdown

## Design Principles

1. **Modular**: Each tool works independently
2. **No external AI dependencies**: Core tools use pattern matching and heuristics
3. **Extensible**: Easy to add new analysis rules or output formats
4. **Well-tested**: Comprehensive test suite for all modules
