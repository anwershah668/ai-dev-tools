"""
Pull Request Description Generator
====================================
Generates structured pull request descriptions from a diff and/or a list of
commit messages.

Usage::

    from src.pr_description import PRDescriptionGenerator

    generator = PRDescriptionGenerator()
    description = generator.generate(diff, commit_messages=["feat: add login"])
    print(description)
"""

import re
import textwrap


class PRDescriptionGenerator:
    """Generate a structured pull request description.

    The generator analyses the provided *diff* text and *commit_messages* list
    to produce a Markdown PR description that includes a summary, a list of
    changes, and a testing checklist.  No external API is required.
    """

    # Regex for unified diff file headers.
    _FILE_HEADER = re.compile(r'^(?:\+\+\+|---)\s+(?:a/|b/)?(.+)$')
    # Lines added / removed in the diff.
    _ADDED_LINE = re.compile(r'^\+(?!\+\+)')
    _REMOVED_LINE = re.compile(r'^-(?!--)')

    def generate(
        self,
        diff: str = "",
        commit_messages: list = None,
        pr_type: str = "feature",
    ) -> str:
        """Return a Markdown-formatted pull request description.

        Args:
            diff: Unified diff string (optional).
            commit_messages: List of commit message strings (optional).
            pr_type: One of ``"feature"``, ``"bugfix"``, ``"docs"``,
                ``"refactor"``, ``"chore"`` – used in the type badge.

        Returns:
            A multi-line Markdown string suitable for a GitHub PR body.

        Raises:
            ValueError: If both *diff* and *commit_messages* are empty/None.
        """
        if not diff and not commit_messages:
            raise ValueError("Provide at least a diff or commit_messages.")

        commit_messages = commit_messages or []
        changed_files = self._parse_changed_files(diff)
        stats = self._diff_stats(diff)
        change_summary = self._build_change_summary(commit_messages, changed_files)

        parts = [
            f"## Pull Request – {pr_type.capitalize()}",
            "",
            "### Summary",
            "",
            change_summary,
            "",
            "### Changes",
            "",
        ]

        if commit_messages:
            for msg in commit_messages:
                parts.append(f"- {msg.strip()}")
        elif changed_files:
            for f in changed_files:
                parts.append(f"- Modified `{f}`")

        if changed_files:
            parts += [
                "",
                "### Files Changed",
                "",
            ]
            for f in changed_files:
                parts.append(f"- `{f}`")

        parts += [
            "",
            f"**Diff stats:** +{stats['added']} lines / -{stats['removed']} lines",
            "",
            "### Testing",
            "",
            "- [ ] Unit tests added / updated",
            "- [ ] Manual testing performed",
            "- [ ] No regressions observed",
            "",
            "### Checklist",
            "",
            "- [ ] Code follows project style guidelines",
            "- [ ] Self-review completed",
            "- [ ] Documentation updated (if applicable)",
        ]

        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _parse_changed_files(self, diff: str) -> list:
        """Return a deduplicated list of file paths mentioned in *diff*."""
        files = []
        for line in diff.splitlines():
            m = self._FILE_HEADER.match(line)
            if m:
                path = m.group(1).strip()
                if path not in files and path != "/dev/null":
                    files.append(path)
        return files

    def _diff_stats(self, diff: str) -> dict:
        """Return counts of added and removed lines in *diff*."""
        added = sum(1 for l in diff.splitlines() if self._ADDED_LINE.match(l))
        removed = sum(1 for l in diff.splitlines() if self._REMOVED_LINE.match(l))
        return {"added": added, "removed": removed}

    def _build_change_summary(self, commit_messages: list, changed_files: list) -> str:
        """Derive a one-sentence summary from commits or file names."""
        if commit_messages:
            # Use the first commit message as the basis.
            first = commit_messages[0].strip()
            # Strip conventional commit prefix (e.g. "feat: ").
            first = re.sub(r'^[a-z]+\s*:\s*', '', first, flags=re.IGNORECASE)
            return textwrap.shorten(
                first[0].upper() + first[1:] if first else first,
                width=200,
                placeholder="…",
            )
        if changed_files:
            return f"Updates to {', '.join(changed_files[:3])}."
        return "Various improvements and fixes."
