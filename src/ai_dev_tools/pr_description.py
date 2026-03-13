"""PR Description Generator - Auto-generate pull request descriptions from diffs."""

import re
from typing import Optional


def parse_diff_stats(diff_text: str) -> dict:
    """Parse a unified diff to extract file change statistics.

    Args:
        diff_text: The raw unified diff text.

    Returns:
        A dict with files_changed, insertions, deletions, and file details.
    """
    if not diff_text or not diff_text.strip():
        return {
            "files_changed": 0,
            "insertions": 0,
            "deletions": 0,
            "files": [],
        }

    files = []
    current_file = None
    insertions = 0
    deletions = 0

    for line in diff_text.splitlines():
        # Detect file header
        file_match = re.match(r'^diff --git a/(.*) b/(.*)', line)
        if file_match:
            if current_file:
                files.append(current_file)
            current_file = {
                "path": file_match.group(2),
                "insertions": 0,
                "deletions": 0,
            }
            continue

        if current_file is None:
            continue

        if line.startswith('+') and not line.startswith('+++'):
            current_file["insertions"] += 1
            insertions += 1
        elif line.startswith('-') and not line.startswith('---'):
            current_file["deletions"] += 1
            deletions += 1

    if current_file:
        files.append(current_file)

    return {
        "files_changed": len(files),
        "insertions": insertions,
        "deletions": deletions,
        "files": files,
    }


def classify_change_type(files: list) -> str:
    """Classify the type of change based on files modified.

    Args:
        files: List of file detail dicts from parse_diff_stats.

    Returns:
        A string describing the change type (e.g. 'feature', 'bugfix', 'docs').
    """
    if not files:
        return "unknown"

    paths = [f["path"] for f in files]

    test_patterns = ["test_", "_test.", "tests/", "spec/"]
    config_files = {"setup.py", "setup.cfg", "pyproject.toml", "requirements.txt",
                    "package.json", "Makefile", ".gitignore"}
    doc_extensions = {".md", ".rst"}

    has_config = any(any(p.endswith(c) or p == c for c in config_files) for p in paths)
    has_docs = any(any(p.endswith(ext) for ext in doc_extensions) for p in paths)
    has_tests = any(any(pat in p for pat in test_patterns) for p in paths)
    has_source = any(p.endswith(".py") and not any(pat in p for pat in test_patterns)
                     for p in paths)

    if has_source and has_tests:
        return "feature"
    if has_source and not has_tests and not has_docs:
        return "bugfix"
    if has_config and not has_source:
        return "chore"
    if has_docs and not has_source:
        return "docs"
    if has_tests and not has_source:
        return "test"

    return "mixed"


def generate_pr_description(
    diff_text: str,
    title: Optional[str] = None,
    branch_name: Optional[str] = None,
) -> str:
    """Generate a pull request description from a diff.

    Args:
        diff_text: The raw unified diff text.
        title: Optional PR title.
        branch_name: Optional branch name for context.

    Returns:
        A formatted PR description string in Markdown.
    """
    stats = parse_diff_stats(diff_text)
    change_type = classify_change_type(stats["files"])

    sections = []

    # Title section
    if title:
        sections.append(f"## {title}")
    else:
        sections.append(f"## {change_type.capitalize()} changes")

    sections.append("")

    # Summary
    sections.append("### Summary")
    sections.append(
        f"This PR modifies **{stats['files_changed']}** file(s) "
        f"with **{stats['insertions']}** insertion(s) and "
        f"**{stats['deletions']}** deletion(s)."
    )
    sections.append(f"- **Change type:** {change_type}")
    if branch_name:
        sections.append(f"- **Branch:** `{branch_name}`")
    sections.append("")

    # Files changed
    if stats["files"]:
        sections.append("### Files Changed")
        for f in stats["files"]:
            sections.append(f"- `{f['path']}` (+{f['insertions']}, -{f['deletions']})")
        sections.append("")

    # Checklist
    sections.append("### Checklist")
    sections.append("- [ ] Code has been tested locally")
    sections.append("- [ ] Documentation updated (if applicable)")
    sections.append("- [ ] Tests added/updated (if applicable)")

    return "\n".join(sections)
