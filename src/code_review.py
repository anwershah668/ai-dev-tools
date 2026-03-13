"""
Code Review Tool
================
Surfaces common Python code quality issues and best-practice violations using
static analysis heuristics (no external tools required).

Usage::

    from src.code_review import CodeReviewer

    reviewer = CodeReviewer()
    suggestions = reviewer.review(source_code)
    for s in suggestions:
        print(s)
"""

import ast
import re
import tokenize
import io
from dataclasses import dataclass, field
from typing import List


@dataclass
class ReviewSuggestion:
    """A single code review suggestion.

    Attributes:
        line: 1-based line number where the issue was detected (0 if n/a).
        severity: One of ``"error"``, ``"warning"``, ``"info"``.
        rule: Short rule identifier (e.g. ``"hardcoded-secret"``).
        message: Human-readable description of the issue.
    """

    line: int
    severity: str
    rule: str
    message: str

    def __str__(self) -> str:
        prefix = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(self.severity, "•")
        loc = f"Line {self.line}: " if self.line else ""
        return f"{prefix} [{self.severity.upper()}] {loc}{self.message} (rule: {self.rule})"


class CodeReviewer:
    """Perform lightweight static analysis on Python source code.

    Checks performed:
    - Hardcoded secrets / passwords
    - Use of ``eval`` or ``exec``
    - Broad ``except`` clauses (bare ``except`` or ``except Exception``)
    - Functions/methods without docstrings
    - Mutable default arguments
    - TODO / FIXME comments
    - Lines exceeding 120 characters
    """

    _SECRET_PATTERNS = [
        re.compile(
            r'(?:password|passwd|secret|api_key|token|auth)\s*=\s*["\'].+["\']',
            re.IGNORECASE,
        ),
        re.compile(r'(?:password|passwd|secret)\s*=\s*["\'][^"\']{3,}["\']', re.IGNORECASE),
    ]
    _TODO_PATTERN = re.compile(r'#\s*(?:TODO|FIXME|HACK|XXX)\b', re.IGNORECASE)
    _MAX_LINE_LENGTH = 120

    def review(self, source_code: str) -> List[ReviewSuggestion]:
        """Analyse *source_code* and return a list of :class:`ReviewSuggestion`.

        Args:
            source_code: Python source code as a string.

        Returns:
            List of :class:`ReviewSuggestion` objects; empty list if no issues found.

        Raises:
            ValueError: If *source_code* is empty.
        """
        if not source_code or not source_code.strip():
            raise ValueError("source_code must not be empty.")

        suggestions: List[ReviewSuggestion] = []
        lines = source_code.splitlines()

        # --- Text-based checks ---
        for i, line in enumerate(lines, start=1):
            suggestions.extend(self._check_line(i, line))

        # --- AST-based checks ---
        try:
            tree = ast.parse(source_code)
            suggestions.extend(self._check_ast(tree))
        except SyntaxError as exc:
            suggestions.append(
                ReviewSuggestion(
                    line=exc.lineno or 0,
                    severity="error",
                    rule="syntax-error",
                    message=f"Syntax error: {exc.msg}",
                )
            )

        suggestions.sort(key=lambda s: s.line)
        return suggestions

    # ------------------------------------------------------------------
    # Line-level checks
    # ------------------------------------------------------------------

    def _check_line(self, lineno: int, line: str) -> List[ReviewSuggestion]:
        issues = []

        # Hardcoded secrets
        for pattern in self._SECRET_PATTERNS:
            if pattern.search(line):
                issues.append(
                    ReviewSuggestion(
                        line=lineno,
                        severity="error",
                        rule="hardcoded-secret",
                        message=(
                            "Possible hardcoded secret detected. "
                            "Use environment variables or a secrets manager instead."
                        ),
                    )
                )
                break  # one report per line

        # TODO/FIXME
        if self._TODO_PATTERN.search(line):
            issues.append(
                ReviewSuggestion(
                    line=lineno,
                    severity="info",
                    rule="todo-comment",
                    message="TODO/FIXME comment found – consider opening a tracked issue.",
                )
            )

        # Long lines
        if len(line) > self._MAX_LINE_LENGTH:
            issues.append(
                ReviewSuggestion(
                    line=lineno,
                    severity="warning",
                    rule="line-too-long",
                    message=(
                        f"Line exceeds {self._MAX_LINE_LENGTH} characters "
                        f"({len(line)} chars)."
                    ),
                )
            )

        return issues

    # ------------------------------------------------------------------
    # AST-level checks
    # ------------------------------------------------------------------

    def _check_ast(self, tree: ast.AST) -> List[ReviewSuggestion]:
        issues = []
        for node in ast.walk(tree):
            issues.extend(self._check_node(node))
        return issues

    def _check_node(self, node: ast.AST) -> List[ReviewSuggestion]:
        issues = []

        # eval / exec usage
        if isinstance(node, ast.Call):
            func = node.func
            name = ""
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name in ("eval", "exec"):
                issues.append(
                    ReviewSuggestion(
                        line=node.lineno,
                        severity="error",
                        rule="eval-exec",
                        message=(
                            f"Use of `{name}()` detected. "
                            "This can be a security risk; avoid dynamic code execution."
                        ),
                    )
                )

        # Broad except clauses
        if isinstance(node, ast.ExceptHandler):
            if node.type is None or (
                isinstance(node.type, ast.Name) and node.type.id == "Exception"
            ):
                issues.append(
                    ReviewSuggestion(
                        line=node.lineno,
                        severity="warning",
                        rule="broad-except",
                        message=(
                            "Broad `except` clause detected. "
                            "Catch specific exception types to avoid masking errors."
                        ),
                    )
                )

        # Missing docstrings
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                issues.append(
                    ReviewSuggestion(
                        line=node.lineno,
                        severity="info",
                        rule="missing-docstring",
                        message=(
                            f"Function `{node.name}` is missing a docstring."
                        ),
                    )
                )

        # Mutable default arguments
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults + node.args.kw_defaults:
                if default is not None and isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    issues.append(
                        ReviewSuggestion(
                            line=node.lineno,
                            severity="warning",
                            rule="mutable-default-arg",
                            message=(
                                f"Function `{node.name}` uses a mutable default argument. "
                                "Use `None` as default and initialise inside the function."
                            ),
                        )
                    )

        return issues
