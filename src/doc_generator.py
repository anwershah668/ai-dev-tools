"""Documentation generator module.

Extracts docstrings and signatures from a Python module and produces
a Markdown documentation page, without requiring an external API.
"""

from __future__ import annotations

import ast
import inspect
import textwrap
from pathlib import Path
from typing import List, Optional


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class DocGenerator:
    """Generate Markdown documentation from a Python source file.

    The generator uses Python's :mod:`ast` module to parse the source file
    and extract:

    * Module-level docstring
    * Top-level classes (with their docstrings and methods)
    * Top-level functions (with their docstrings and signatures)

    No external dependencies or API keys are required.

    Example::

        generator = DocGenerator()
        docs = generator.generate_docs("src/issue_summarizer.py")
        print(docs)
        # Optionally save to a file:
        generator.generate_docs("src/issue_summarizer.py", output_path="docs/issue_summarizer.md")
    """

    def generate_docs(
        self, filepath: str, output_path: Optional[str] = None
    ) -> str:
        """Generate Markdown documentation for a Python source file.

        Args:
            filepath: Path to the Python source file.
            output_path: If provided, the generated Markdown is also written
                to this file.

        Returns:
            A Markdown string documenting the module.

        Raises:
            FileNotFoundError: If *filepath* does not exist.
            SyntaxError: If the file cannot be parsed as Python.
        """
        source_path = Path(filepath)
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=filepath)

        sections: List[str] = []

        # Title
        module_name = source_path.stem
        sections.append(f"# Module: `{module_name}`\n")

        # Module docstring
        module_doc = ast.get_docstring(tree)
        if module_doc:
            sections.append(f"{module_doc}\n")

        # Top-level classes
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)
                   and not n.name.startswith("_")]
        # Only include direct children of the module (not nested classes)
        top_level_classes = [
            n for n in tree.body if isinstance(n, ast.ClassDef) and not n.name.startswith("_")
        ]
        if top_level_classes:
            sections.append("---\n\n## Classes\n")
            for cls_node in top_level_classes:
                sections.append(self._render_class(cls_node, source))

        # Top-level functions
        top_level_funcs = [
            n for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not n.name.startswith("_")
        ]
        if top_level_funcs:
            sections.append("---\n\n## Functions\n")
            for func_node in top_level_funcs:
                sections.append(self._render_function(func_node, source))

        result = "\n".join(sections)

        if output_path:
            Path(output_path).write_text(result, encoding="utf-8")

        return result

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------

    def _render_class(self, node: ast.ClassDef, source: str) -> str:
        """Render a class node as a Markdown section."""
        lines: List[str] = []
        lines.append(f"### `class {node.name}`\n")

        doc = ast.get_docstring(node)
        if doc:
            lines.append(f"{textwrap.dedent(doc).strip()}\n")

        # Public methods
        methods = [
            n for n in node.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not n.name.startswith("_")
        ]
        if methods:
            lines.append("**Methods:**\n")
            for method in methods:
                sig = self._build_signature(method)
                lines.append(f"- `{sig}`")
                method_doc = ast.get_docstring(method)
                if method_doc:
                    first_line = method_doc.strip().splitlines()[0]
                    lines.append(f"  {first_line}")
            lines.append("")

        return "\n".join(lines)

    def _render_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, source: str
    ) -> str:
        """Render a function node as a Markdown section."""
        lines: List[str] = []
        sig = self._build_signature(node)
        prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
        lines.append(f"### `{prefix}def {sig}`\n")

        doc = ast.get_docstring(node)
        if doc:
            lines.append(f"{textwrap.dedent(doc).strip()}\n")
        else:
            lines.append("*No docstring provided.*\n")

        return "\n".join(lines)

    @staticmethod
    def _build_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Build a simplified function signature string."""
        args: List[str] = []
        all_args = node.args.args
        defaults = node.args.defaults

        # Align defaults to the end of args list
        n_without_defaults = len(all_args) - len(defaults)

        for i, arg in enumerate(all_args):
            default_index = i - n_without_defaults
            annotation = ""
            if arg.annotation:
                try:
                    annotation = f": {ast.unparse(arg.annotation)}"
                except Exception:
                    pass

            if default_index >= 0:
                try:
                    default_val = ast.unparse(defaults[default_index])
                except Exception:
                    default_val = "..."
                args.append(f"{arg.arg}{annotation}={default_val}")
            else:
                args.append(f"{arg.arg}{annotation}")

        # *args
        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")

        # **kwargs
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")

        return_annotation = ""
        if node.returns:
            try:
                return_annotation = f" -> {ast.unparse(node.returns)}"
            except Exception:
                pass

        return f"{node.name}({', '.join(args)}){return_annotation}"
