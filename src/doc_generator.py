"""
Documentation Generator
========================
Generates Google-style docstrings and a README stub for Python source code.

Usage::

    from src.doc_generator import DocGenerator

    gen = DocGenerator()
    result = gen.generate(source_code)
    print(result)
"""

import ast
import inspect
import textwrap
from typing import List, Optional


class DocGenerator:
    """Generate documentation stubs for Python source code.

    Given a Python source string, :meth:`generate` returns:

    - A README stub with module-level overview.
    - Google-style docstring stubs for each function / class / method
      that currently lacks one.

    No external tools or APIs are required.
    """

    def generate(self, source_code: str) -> str:
        """Generate documentation stubs for *source_code*.

        Args:
            source_code: Valid Python source code as a string.

        Returns:
            A Markdown-formatted documentation report containing a README
            stub and docstring stubs for all public symbols.

        Raises:
            ValueError: If *source_code* is empty.
            SyntaxError: If *source_code* cannot be parsed.
        """
        if not source_code or not source_code.strip():
            raise ValueError("source_code must not be empty.")

        tree = ast.parse(source_code)  # raises SyntaxError on bad input
        symbols = self._collect_symbols(tree)

        parts = [
            "# Documentation Report",
            "",
            "## Module Overview",
            "",
            self._module_overview(tree, symbols),
            "",
            "## Docstring Stubs",
            "",
            "> Copy the stubs below into your source code and fill in the details.",
            "",
        ]

        for sym in symbols:
            parts.append(self._render_stub(sym))
            parts.append("")

        if not symbols:
            parts.append("*No public functions or classes found.*")

        return "\n".join(parts)

    def generate_docstring(self, func_name: str, args: List[str], has_return: bool = True) -> str:
        """Generate a Google-style docstring stub for a single function.

        Args:
            func_name: Name of the function.
            args: List of argument names (excluding ``self`` / ``cls``).
            has_return: Whether the function returns a value.

        Returns:
            A formatted docstring stub string.
        """
        lines = [f'"""Summary line for {func_name}.', ""]

        if args:
            lines += ["Args:"]
            for arg in args:
                lines.append(f"    {arg}: Description of `{arg}`.")
            lines.append("")

        if has_return:
            lines += ["Returns:", "    Description of the return value.", ""]

        lines += ['Raises:', '    ValueError: If inputs are invalid.', '"""']
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _collect_symbols(self, tree: ast.AST) -> list:
        """Return a list of symbol info dicts for top-level + class members."""
        symbols = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_"):
                    continue  # skip private symbols
                symbols.append(self._symbol_info(node))
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith("_"):
                    symbols.append(self._class_info(node))
        return symbols

    def _symbol_info(self, node) -> dict:
        """Extract metadata from a function / method AST node."""
        args = [
            a.arg
            for a in node.args.args
            if a.arg not in ("self", "cls")
        ]
        has_return = any(
            isinstance(n, ast.Return) and n.value is not None
            for n in ast.walk(node)
        )
        has_docstring = (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        )
        return {
            "kind": "function",
            "name": node.name,
            "line": node.lineno,
            "args": args,
            "has_return": has_return,
            "has_docstring": has_docstring,
        }

    def _class_info(self, node: ast.ClassDef) -> dict:
        """Extract metadata from a class AST node."""
        has_docstring = (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        )
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not item.name.startswith("_") or item.name == "__init__":
                    methods.append(item.name)
        return {
            "kind": "class",
            "name": node.name,
            "line": node.lineno,
            "methods": methods,
            "has_docstring": has_docstring,
        }

    def _module_overview(self, tree: ast.AST, symbols: list) -> str:
        """Generate a short module overview paragraph."""
        funcs = [s["name"] for s in symbols if s["kind"] == "function"]
        classes = [s["name"] for s in symbols if s["kind"] == "class"]

        module_doc = ast.get_docstring(tree) or ""
        lines = []
        if module_doc:
            lines.append(module_doc.strip())
            lines.append("")

        if classes:
            lines.append(f"**Classes:** {', '.join(f'`{c}`' for c in classes)}")
        if funcs:
            lines.append(f"**Functions:** {', '.join(f'`{f}`' for f in funcs)}")
        if not classes and not funcs:
            lines.append("*No public symbols detected.*")

        return "\n".join(lines)

    def _render_stub(self, sym: dict) -> str:
        """Render a Markdown code block with the docstring stub."""
        status = "✅ has docstring" if sym.get("has_docstring") else "❌ missing docstring"
        header = f"### `{sym['name']}` (line {sym['line']}) – {status}"

        if sym.get("has_docstring"):
            return header  # nothing to generate

        if sym["kind"] == "function":
            stub = self.generate_docstring(
                sym["name"], sym["args"], sym["has_return"]
            )
        else:
            methods_str = ", ".join(sym.get("methods", []))
            stub = (
                f'"""{sym["name"]} – TODO: add class description.\n\n'
                f"Methods: {methods_str}\n"
                '"""'
            )

        return f"{header}\n\n```python\n{stub}\n```"
