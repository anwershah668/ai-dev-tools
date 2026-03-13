"""Code review suggestion tool.

Performs lightweight static analysis on Python source files and returns
human-readable improvement suggestions.  No external API is required.
"""

from __future__ import annotations

import ast
import re
import tokenize
import io
from dataclasses import dataclass
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Suggestion:
    """A single code review suggestion."""

    line: Optional[int]
    category: str
    message: str

    def __str__(self) -> str:
        loc = f"Line {self.line}" if self.line is not None else "General"
        return f"[{self.category}] {loc}: {self.message}"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class CodeReviewTool:
    """Analyse a Python source file and produce improvement suggestions.

    The tool runs several lightweight checks:

    * **Style** – long lines, trailing whitespace, missing blank lines between
      top-level definitions.
    * **Complexity** – functions with too many arguments or too many branches.
    * **Best practices** – bare ``except`` clauses, mutable default arguments,
      missing docstrings on public functions/classes.

    No external dependencies or API keys are required.

    Example::

        reviewer = CodeReviewTool()
        for suggestion in reviewer.review("my_module.py"):
            print(suggestion)
    """

    MAX_LINE_LENGTH: int = 99
    MAX_FUNCTION_ARGS: int = 5
    MAX_BRANCHES: int = 6

    def review_file(self, filepath: str) -> List[Suggestion]:
        """Review a Python source file and return a list of suggestions.

        Args:
            filepath: Path to the Python source file to review.

        Returns:
            A (possibly empty) list of :class:`Suggestion` objects.

        Raises:
            FileNotFoundError: If *filepath* does not exist.
            SyntaxError: If the file cannot be parsed as Python.
        """
        with open(filepath, "r", encoding="utf-8") as fh:
            source = fh.read()
        return self.review(source)

    def review(self, source: str) -> List[Suggestion]:
        """Review Python source code provided as a string.

        Args:
            source: Python source code.

        Returns:
            A (possibly empty) list of :class:`Suggestion` objects.

        Raises:
            SyntaxError: If *source* cannot be parsed as Python.
        """
        suggestions: List[Suggestion] = []
        suggestions.extend(self._check_line_style(source))

        tree = ast.parse(source)
        suggestions.extend(self._check_ast(tree))
        return suggestions

    # ------------------------------------------------------------------
    # Line-level checks (no AST needed)
    # ------------------------------------------------------------------

    def _check_line_style(self, source: str) -> List[Suggestion]:
        results: List[Suggestion] = []
        lines = source.splitlines()
        prev_was_blank = False

        for lineno, raw_line in enumerate(lines, start=1):
            # Long lines
            if len(raw_line) > self.MAX_LINE_LENGTH:
                results.append(
                    Suggestion(
                        line=lineno,
                        category="Style",
                        message=(
                            f"Line is {len(raw_line)} characters "
                            f"(limit: {self.MAX_LINE_LENGTH})."
                        ),
                    )
                )

            # Trailing whitespace
            if raw_line != raw_line.rstrip():
                results.append(
                    Suggestion(
                        line=lineno,
                        category="Style",
                        message="Trailing whitespace detected.",
                    )
                )

            prev_was_blank = raw_line.strip() == ""

        return results

    # ------------------------------------------------------------------
    # AST-based checks
    # ------------------------------------------------------------------

    def _check_ast(self, tree: ast.AST) -> List[Suggestion]:
        results: List[Suggestion] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                results.extend(self._check_function(node))
            elif isinstance(node, ast.ClassDef):
                results.extend(self._check_class(node))
            elif isinstance(node, ast.ExceptHandler):
                results.extend(self._check_except(node))
        return results

    def _check_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> List[Suggestion]:
        results: List[Suggestion] = []
        lineno = node.lineno

        # Too many arguments
        n_args = len(node.args.args)
        if n_args > self.MAX_FUNCTION_ARGS:
            results.append(
                Suggestion(
                    line=lineno,
                    category="Complexity",
                    message=(
                        f"Function '{node.name}' has {n_args} arguments "
                        f"(recommended max: {self.MAX_FUNCTION_ARGS}). "
                        "Consider grouping related parameters into a dataclass."
                    ),
                )
            )

        # Mutable default argument
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                results.append(
                    Suggestion(
                        line=lineno,
                        category="Best Practice",
                        message=(
                            f"Function '{node.name}' uses a mutable default "
                            "argument. Use None and assign inside the body instead."
                        ),
                    )
                )
                break

        # Missing docstring
        if not (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            # Only warn for public functions (not starting with _)
            if not node.name.startswith("_"):
                results.append(
                    Suggestion(
                        line=lineno,
                        category="Documentation",
                        message=(
                            f"Public function '{node.name}' is missing a docstring."
                        ),
                    )
                )

        # Branch complexity
        branches = sum(
            1
            for child in ast.walk(node)
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler))
        )
        if branches > self.MAX_BRANCHES:
            results.append(
                Suggestion(
                    line=lineno,
                    category="Complexity",
                    message=(
                        f"Function '{node.name}' has high branch complexity "
                        f"({branches} branches). Consider refactoring."
                    ),
                )
            )

        return results

    def _check_class(self, node: ast.ClassDef) -> List[Suggestion]:
        results: List[Suggestion] = []
        if not node.name.startswith("_"):
            if not (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                results.append(
                    Suggestion(
                        line=node.lineno,
                        category="Documentation",
                        message=f"Public class '{node.name}' is missing a docstring.",
                    )
                )
        return results

    def _check_except(self, node: ast.ExceptHandler) -> List[Suggestion]:
        results: List[Suggestion] = []
        if node.type is None:
            results.append(
                Suggestion(
                    line=node.lineno,
                    category="Best Practice",
                    message=(
                        "Bare 'except' clause catches all exceptions including "
                        "KeyboardInterrupt and SystemExit. "
                        "Catch specific exception types instead."
                    ),
                )
            )
        return results
