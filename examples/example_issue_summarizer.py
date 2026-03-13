"""Example: using IssueSummarizer to condense an issue thread."""

import sys
import os

# Allow running from the repository root without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.issue_summarizer import IssueSummarizer


def main():
    comments = [
        "The login button is broken on mobile devices.",
        "I can reproduce this on iOS 16 and Android 13. "
        "The button is visible but pressing it does nothing.",
        "Looks like the CSS media query at line 42 in styles.css is incorrect. "
        "The button loses its click event handler below 768px.",
        "I found the root cause: the JavaScript event listener is attached before "
        "the DOM is ready on mobile browsers.",
        "PR #42 should fix this. It moves the event listener attachment to "
        "the DOMContentLoaded callback.",
        "Tested the fix on Chrome for Android and Safari on iOS — works correctly now.",
    ]

    summarizer = IssueSummarizer()
    result = summarizer.summarize(comments)
    print(result)


if __name__ == "__main__":
    main()
