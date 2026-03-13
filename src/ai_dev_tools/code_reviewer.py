"""Code Reviewer - Provide automated code review suggestions."""

import re
from typing import Optional


def check_function_length(source: str, max_lines: int = 50) -> list:
    """Check for functions that exceed a maximum line count.

    Args:
        source: Python source code as a string.
        max_lines: Maximum allowed lines per function.

    Returns:
        A list of dicts with function name, start line, and line count.
    """
    issues = []
    lines = source.splitlines()
    func_pattern = re.compile(r'^(\s*)def\s+(\w+)\s*\(')

    i = 0
    while i < len(lines):
        match = func_pattern.match(lines[i])
        if match:
            indent = len(match.group(1))
            func_name = match.group(2)
            start_line = i + 1  # 1-indexed
            func_lines = 1
            j = i + 1
            while j < len(lines):
                line = lines[j]
                stripped = line.rstrip()
                if stripped == "":
                    func_lines += 1
                    j += 1
                    continue
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= indent and stripped != "":
                    break
                func_lines += 1
                j += 1

            if func_lines > max_lines:
                issues.append({
                    "function": func_name,
                    "start_line": start_line,
                    "line_count": func_lines,
                    "suggestion": (
                        f"Function '{func_name}' is {func_lines} lines long "
                        f"(max {max_lines}). Consider breaking it into smaller functions."
                    ),
                })
            i = j
        else:
            i += 1

    return issues


def check_missing_docstrings(source: str) -> list:
    """Check for functions and classes missing docstrings.

    Args:
        source: Python source code as a string.

    Returns:
        A list of dicts with the name and line number of items missing docstrings.
    """
    issues = []
    lines = source.splitlines()
    pattern = re.compile(r'^\s*(def|class)\s+(\w+)')

    for i, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            kind = match.group(1)
            name = match.group(2)
            # Check if next non-empty line is a docstring
            has_docstring = False
            for j in range(i + 1, min(i + 5, len(lines))):
                stripped = lines[j].strip()
                if not stripped:
                    continue
                if stripped.startswith(('"""', "'''", 'r"""', "r'''")):
                    has_docstring = True
                break

            if not has_docstring:
                issues.append({
                    "type": kind,
                    "name": name,
                    "line": i + 1,
                    "suggestion": f"{kind.capitalize()} '{name}' at line {i + 1} is missing a docstring.",
                })

    return issues


def check_todo_comments(source: str) -> list:
    """Find TODO and FIXME comments in source code.

    Args:
        source: Source code as a string.

    Returns:
        A list of dicts with line number and the comment text.
    """
    issues = []
    pattern = re.compile(r'#\s*(TODO|FIXME|HACK|XXX)\b[:\s]*(.*)', re.IGNORECASE)

    for i, line in enumerate(source.splitlines()):
        match = pattern.search(line)
        if match:
            issues.append({
                "line": i + 1,
                "tag": match.group(1).upper(),
                "comment": match.group(2).strip(),
                "suggestion": f"Found {match.group(1).upper()} at line {i + 1}: {match.group(2).strip()}",
            })

    return issues


def review_code(source: str, filename: Optional[str] = None) -> dict:
    """Perform an automated code review on Python source code.

    Args:
        source: Python source code as a string.
        filename: Optional filename for context.

    Returns:
        A dict with review results grouped by category.
    """
    long_functions = check_function_length(source)
    missing_docs = check_missing_docstrings(source)
    todos = check_todo_comments(source)

    total_issues = len(long_functions) + len(missing_docs) + len(todos)

    return {
        "filename": filename or "<unknown>",
        "total_issues": total_issues,
        "long_functions": long_functions,
        "missing_docstrings": missing_docs,
        "todos": todos,
        "summary": _generate_review_summary(total_issues, long_functions, missing_docs, todos),
    }


def _generate_review_summary(total: int, long_funcs: list, missing_docs: list, todos: list) -> str:
    """Generate a human-readable review summary."""
    if total == 0:
        return "No issues found. Code looks good!"

    parts = []
    if long_funcs:
        parts.append(f"{len(long_funcs)} long function(s)")
    if missing_docs:
        parts.append(f"{len(missing_docs)} missing docstring(s)")
    if todos:
        parts.append(f"{len(todos)} TODO/FIXME comment(s)")

    return f"Found {total} issue(s): {', '.join(parts)}."
