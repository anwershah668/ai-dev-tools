#!/usr/bin/env python3
"""Example: Using the Issue Summarizer.

This example demonstrates how to use the issue_summarizer module
to summarize GitHub issues.
"""

from ai_dev_tools.issue_summarizer import summarize_issue


def main():
    # Example 1: Bug report
    bug_report = summarize_issue(
        title="Application crashes on startup",
        body=(
            "When I launch the application on macOS Ventura, it crashes immediately. "
            "The error log shows a segfault in the rendering engine. "
            "I've tried reinstalling but the issue persists. "
            "This started happening after the v2.1 update. "
            "Steps to reproduce: 1) Install v2.1 2) Launch the app 3) Observe crash."
        ),
        labels=["bug", "critical"],
    )
    print("=== Bug Report Summary ===")
    print(f"Title: {bug_report['title']}")
    print(f"Summary: {bug_report['summary']}")
    print(f"Category: {bug_report['category']}")
    print(f"Priority: {bug_report['priority']}")
    print()

    # Example 2: Feature request
    feature_request = summarize_issue(
        title="Add dark mode support",
        body=(
            "It would be great to have a dark mode option. "
            "Many users prefer dark themes for reduced eye strain. "
            "This feature could be toggled in the settings menu."
        ),
        labels=["enhancement"],
    )
    print("=== Feature Request Summary ===")
    print(f"Title: {feature_request['title']}")
    print(f"Summary: {feature_request['summary']}")
    print(f"Category: {feature_request['category']}")
    print(f"Priority: {feature_request['priority']}")
    print()

    # Example 3: Documentation issue
    doc_issue = summarize_issue(
        title="Fix typo in README",
        body="There is a typo in the installation documentation section.",
        labels=["documentation"],
    )
    print("=== Documentation Issue Summary ===")
    print(f"Title: {doc_issue['title']}")
    print(f"Summary: {doc_issue['summary']}")
    print(f"Category: {doc_issue['category']}")
    print(f"Priority: {doc_issue['priority']}")


if __name__ == "__main__":
    main()
