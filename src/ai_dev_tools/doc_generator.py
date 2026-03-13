"""Documentation Generator - Auto-generate documentation from Python source code."""

import re
from typing import Optional


def extract_functions(source: str) -> list:
    """Extract function signatures and docstrings from Python source code.

    Args:
        source: Python source code as a string.

    Returns:
        A list of dicts with function name, args, docstring, and line number.
    """
    functions = []
    lines = source.splitlines()
    func_pattern = re.compile(r'^(\s*)def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*(.+?))?\s*:')

    for i, line in enumerate(lines):
        match = func_pattern.match(line)
        if match:
            indent = match.group(1)
            name = match.group(2)
            args_str = match.group(3).strip()
            return_type = match.group(4)

            # Parse arguments
            args = _parse_args(args_str) if args_str else []

            # Extract docstring
            docstring = _extract_docstring(lines, i + 1)

            functions.append({
                "name": name,
                "args": args,
                "return_type": return_type.strip() if return_type else None,
                "docstring": docstring,
                "line": i + 1,
                "is_private": name.startswith("_"),
            })

    return functions


def extract_classes(source: str) -> list:
    """Extract class definitions and their methods from Python source code.

    Args:
        source: Python source code as a string.

    Returns:
        A list of dicts with class name, docstring, and methods.
    """
    classes = []
    lines = source.splitlines()
    class_pattern = re.compile(r'^class\s+(\w+)(?:\(([^)]*)\))?\s*:')

    for i, line in enumerate(lines):
        match = class_pattern.match(line)
        if match:
            name = match.group(1)
            bases = match.group(2)
            docstring = _extract_docstring(lines, i + 1)

            classes.append({
                "name": name,
                "bases": bases.strip() if bases else None,
                "docstring": docstring,
                "line": i + 1,
            })

    return classes


def generate_markdown_docs(
    source: str,
    module_name: Optional[str] = None,
    include_private: bool = False,
) -> str:
    """Generate Markdown documentation from Python source code.

    Args:
        source: Python source code as a string.
        module_name: Optional module name for the header.
        include_private: Whether to include private functions (starting with _).

    Returns:
        A Markdown-formatted documentation string.
    """
    functions = extract_functions(source)
    classes = extract_classes(source)

    if not include_private:
        functions = [f for f in functions if not f["is_private"]]

    sections = []

    # Module header
    header = module_name or "Module Documentation"
    sections.append(f"# {header}")
    sections.append("")

    # Module docstring (first docstring in file)
    module_doc = _extract_module_docstring(source)
    if module_doc:
        sections.append(module_doc)
        sections.append("")

    # Classes
    if classes:
        sections.append("## Classes")
        sections.append("")
        for cls in classes:
            sections.append(f"### `{cls['name']}`")
            if cls["bases"]:
                sections.append(f"Inherits from: `{cls['bases']}`")
            if cls["docstring"]:
                sections.append("")
                sections.append(cls["docstring"])
            sections.append("")

    # Functions
    if functions:
        sections.append("## Functions")
        sections.append("")
        for func in functions:
            sig = _format_signature(func)
            sections.append(f"### `{sig}`")
            if func["docstring"]:
                sections.append("")
                sections.append(func["docstring"])
            sections.append("")

    return "\n".join(sections)


def _parse_args(args_str: str) -> list:
    """Parse a function argument string into individual arguments."""
    if not args_str:
        return []

    args = []
    depth = 0
    current = []

    for char in args_str:
        if char in "([{":
            depth += 1
            current.append(char)
        elif char in ")]}":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            arg = "".join(current).strip()
            if arg:
                args.append(arg)
            current = []
        else:
            current.append(char)

    last = "".join(current).strip()
    if last:
        args.append(last)

    return args


def _extract_docstring(lines: list, start_idx: int) -> Optional[str]:
    """Extract a docstring starting from the line after a def/class statement."""
    if start_idx >= len(lines):
        return None

    # Skip empty lines
    idx = start_idx
    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    if idx >= len(lines):
        return None

    stripped = lines[idx].strip()

    # Check for single-line docstring
    for quote in ['"""', "'''"]:
        if stripped.startswith(quote) and stripped.endswith(quote) and len(stripped) > 6:
            return stripped[3:-3].strip()

    # Check for multi-line docstring
    for quote in ['"""', "'''"]:
        if stripped.startswith(quote):
            doc_lines = [stripped[3:]]
            idx += 1
            while idx < len(lines):
                line = lines[idx].strip()
                if quote in line:
                    end_pos = line.index(quote)
                    doc_lines.append(line[:end_pos])
                    return "\n".join(doc_lines).strip()
                doc_lines.append(line)
                idx += 1

    return None


def _extract_module_docstring(source: str) -> Optional[str]:
    """Extract the module-level docstring from source code."""
    stripped = source.lstrip()
    for quote in ['"""', "'''"]:
        if stripped.startswith(quote):
            end = stripped.find(quote, 3)
            if end != -1:
                return stripped[3:end].strip()
    return None


def _format_signature(func: dict) -> str:
    """Format a function signature for documentation."""
    args_str = ", ".join(func["args"])
    sig = f"{func['name']}({args_str})"
    if func["return_type"]:
        sig += f" -> {func['return_type']}"
    return sig
