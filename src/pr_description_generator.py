"""Pull request description generator module.

Analyses a unified git diff and produces a structured Markdown PR description
without requiring an external API.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class FileSummary:
    """Summary of changes in a single file."""

    filename: str
    additions: int = 0
    deletions: int = 0
    hunks: int = 0
    is_new: bool = False
    is_deleted: bool = False
    is_renamed: bool = False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class PRDescriptionGenerator:
    """Generate a structured pull-request description from a unified git diff.

    The generator parses the diff to understand which files were changed,
    how many lines were added or removed, and whether files were created,
    deleted, or renamed.  It then renders a Markdown PR template that
    contributors can use as a starting point.

    No external dependencies or API keys are required.

    Example::

        generator = PRDescriptionGenerator()
        diff = open("my_changes.diff").read()
        print(generator.generate(diff))
    """

    def generate(self, diff: str, title: Optional[str] = None) -> str:
        """Generate a Markdown PR description from a unified diff.

        Args:
            diff: A string containing a unified git diff (output of
                ``git diff`` or ``git diff HEAD~1``).
            title: Optional PR title.  When omitted a generic title is used.

        Returns:
            A Markdown-formatted pull-request description string.

        Raises:
            ValueError: If *diff* is an empty string.
        """
        if not diff or not diff.strip():
            raise ValueError("diff must not be empty")

        file_summaries = self._parse_diff(diff)
        return self._render(file_summaries, title)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _parse_diff(self, diff: str) -> List[FileSummary]:
        """Parse a unified diff and return a list of FileSummary objects."""
        summaries: List[FileSummary] = []
        current: Optional[FileSummary] = None

        for line in diff.splitlines():
            # New file header: diff --git a/... b/...
            if line.startswith("diff --git"):
                if current is not None:
                    summaries.append(current)
                # Extract filename from the b/ side
                match = re.search(r" b/(.+)$", line)
                filename = match.group(1) if match else "unknown"
                current = FileSummary(filename=filename)

            elif current is not None:
                if line.startswith("new file mode"):
                    current.is_new = True
                elif line.startswith("deleted file mode"):
                    current.is_deleted = True
                elif line.startswith("rename to"):
                    current.is_renamed = True
                elif line.startswith("@@"):
                    current.hunks += 1
                elif line.startswith("+") and not line.startswith("+++"):
                    current.additions += 1
                elif line.startswith("-") and not line.startswith("---"):
                    current.deletions += 1

        if current is not None:
            summaries.append(current)

        return summaries

    def _render(
        self, summaries: List[FileSummary], title: Optional[str]
    ) -> str:
        """Render the collected file summaries as a Markdown PR description."""
        if title is None:
            title = "chore: update code"

        total_additions = sum(s.additions for s in summaries)
        total_deletions = sum(s.deletions for s in summaries)
        n_files = len(summaries)

        lines: List[str] = [
            f"## {title}",
            "",
            "### Summary",
            "",
            f"This pull request modifies **{n_files} file(s)** with "
            f"**+{total_additions}** additions and **-{total_deletions}** deletions.",
            "",
            "### Changes",
            "",
        ]

        for s in summaries:
            tag = ""
            if s.is_new:
                tag = " *(new file)*"
            elif s.is_deleted:
                tag = " *(deleted)*"
            elif s.is_renamed:
                tag = " *(renamed)*"

            lines.append(
                f"- `{s.filename}`{tag} — "
                f"+{s.additions} / -{s.deletions} across {s.hunks} hunk(s)"
            )

        lines += [
            "",
            "### Motivation",
            "",
            "<!-- Explain *why* these changes are needed. -->",
            "",
            "### Testing",
            "",
            "<!-- Describe how the changes were tested. -->",
            "- [ ] Unit tests added / updated",
            "- [ ] Manual testing performed",
            "",
            "### Related Issues",
            "",
            "<!-- Reference any related issues, e.g. Closes #123 -->",
        ]

        return "\n".join(lines)
