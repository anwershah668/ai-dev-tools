"""CLI interface for AI Dev Tools."""

import sys


def main():
    """Main entry point for the AI Dev Tools CLI."""
    print("AI Dev Tools v0.1.0")
    print("=" * 40)
    print()
    print("Available tools:")
    print("  - Issue Summarizer: Summarize GitHub issues")
    print("  - PR Description Generator: Auto-generate PR descriptions")
    print("  - Code Reviewer: Automated code review suggestions")
    print("  - Documentation Generator: Generate docs from source code")
    print()
    print("Usage:")
    print("  from ai_dev_tools.issue_summarizer import summarize_issue")
    print("  from ai_dev_tools.pr_description import generate_pr_description")
    print("  from ai_dev_tools.code_reviewer import review_code")
    print("  from ai_dev_tools.doc_generator import generate_markdown_docs")
    print()
    print("See examples/ directory for detailed usage examples.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
