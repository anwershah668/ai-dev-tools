"""
Issue Summarizer
================
Condenses verbose GitHub issue text into a concise, structured summary.

Usage::

    from src.issue_summarizer import IssueSummarizer

    summarizer = IssueSummarizer()
    summary = summarizer.summarize(issue_text)
    print(summary)
"""

import re
import textwrap


class IssueSummarizer:
    """Summarize GitHub issue text into structured bullet-point summaries.

    The summarizer extracts the problem statement, reproduction steps,
    expected vs. actual behavior, and any additional context using simple
    heuristic pattern matching.  No external API or model is required.
    """

    # Sentence endings used when splitting free-form text.
    _SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+')

    # Common section headers found in issue templates.
    _SECTION_PATTERNS = {
        "steps": re.compile(
            r'(?:steps?\s+to\s+repro(?:duce)?|how\s+to\s+repro(?:duce)?)',
            re.IGNORECASE,
        ),
        "expected": re.compile(r'expected\s+(?:behavior|result|output)', re.IGNORECASE),
        "actual": re.compile(r'actual\s+(?:behavior|result|output)', re.IGNORECASE),
        "environment": re.compile(
            r'(?:\benvironment\b|\bsystem\s+info\b|\bplatform\b|\bos\b|\bversion\b)',
            re.IGNORECASE,
        ),
    }

    def summarize(self, issue_text: str) -> str:
        """Return a concise summary of *issue_text*.

        Args:
            issue_text: Raw text of the GitHub issue (title + body).

        Returns:
            A multi-line string with a structured summary.

        Raises:
            ValueError: If *issue_text* is empty or contains only whitespace.
        """
        if not issue_text or not issue_text.strip():
            raise ValueError("issue_text must not be empty.")

        lines = [line.strip() for line in issue_text.strip().splitlines()]
        non_empty = [l for l in lines if l]

        sections = self._extract_sections(non_empty)
        problem = self._extract_problem(non_empty)

        parts = ["## Issue Summary", ""]

        parts.append(f"**Problem:** {problem}")

        if sections.get("steps"):
            parts.append("\n**Steps to Reproduce:**")
            for step in sections["steps"]:
                parts.append(f"  - {step}")

        if sections.get("expected"):
            parts.append(f"\n**Expected:** {' '.join(sections['expected'])}")

        if sections.get("actual"):
            parts.append(f"\n**Actual:** {' '.join(sections['actual'])}")

        if sections.get("environment"):
            parts.append(f"\n**Environment:** {' '.join(sections['environment'])}")

        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_problem(self, lines: list) -> str:
        """Return the first meaningful sentence as the problem statement."""
        for line in lines:
            if len(line) > 20:
                return textwrap.shorten(line, width=200, placeholder="…")
        return lines[0] if lines else "No description provided."

    def _extract_sections(self, lines: list) -> dict:
        """Parse labelled sections from issue lines."""
        sections: dict = {}
        current_section = None

        for line in lines:
            matched = False
            for key, pattern in self._SECTION_PATTERNS.items():
                m = pattern.search(line)
                if m:
                    current_section = key
                    sections.setdefault(key, [])
                    # Capture any inline content that follows the matched header
                    # (e.g. "Expected behavior: Modal appears." → "Modal appears.").
                    inline = line[m.end():].strip().lstrip(':').strip()
                    if inline:
                        sections[current_section].append(inline)
                    matched = True
                    break

            if not matched and current_section and line:
                # Strip common list markers (*, -, 1., 2.) before storing.
                clean = re.sub(r'^[\*\-\d\.]+\s*', '', line)
                if clean:
                    sections[current_section].append(clean)

        return sections
