"""Issue Summarizer - Summarize GitHub issues into concise descriptions."""

import re
from typing import Optional


def extract_key_sentences(text: str, max_sentences: int = 3) -> str:
    """Extract the most important sentences from issue text.

    Args:
        text: The full issue body text.
        max_sentences: Maximum number of sentences to return.

    Returns:
        A string containing the key sentences.
    """
    if not text or not text.strip():
        return ""

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    # Prioritize sentences with keywords indicating importance
    priority_keywords = [
        "bug", "error", "fix", "issue", "problem", "crash",
        "feature", "request", "add", "implement", "should",
        "expected", "actual", "steps", "reproduce",
    ]

    scored = []
    for i, sentence in enumerate(sentences):
        score = 0
        lower = sentence.lower()
        for keyword in priority_keywords:
            if keyword in lower:
                score += 1
        # Boost first sentence (usually the main point)
        if i == 0:
            score += 2
        scored.append((score, i, sentence))

    scored.sort(key=lambda x: (-x[0], x[1]))
    top = sorted(scored[:max_sentences], key=lambda x: x[1])

    return " ".join(item[2] for item in top)


def summarize_issue(title: str, body: str, labels: Optional[list] = None) -> dict:
    """Generate a summary of a GitHub issue.

    Args:
        title: The issue title.
        body: The issue body text.
        labels: Optional list of issue labels.

    Returns:
        A dict with summary, category, and priority fields.
    """
    labels = labels or []

    summary = extract_key_sentences(body)

    # Determine category from labels and content
    category = _categorize_issue(title, body, labels)

    # Estimate priority
    priority = _estimate_priority(title, body, labels)

    return {
        "title": title,
        "summary": summary if summary else title,
        "category": category,
        "priority": priority,
        "label_count": len(labels),
    }


def _categorize_issue(title: str, body: str, labels: list) -> str:
    """Categorize an issue based on its content and labels."""
    combined = f"{title} {body} {' '.join(labels)}".lower()

    if any(word in combined for word in ["bug", "error", "crash", "broken", "fail"]):
        return "bug"
    if any(word in combined for word in ["feature", "enhancement", "request", "add"]):
        return "feature"
    if any(word in combined for word in ["doc", "documentation", "readme", "typo"]):
        return "documentation"
    if any(word in combined for word in ["question", "help", "how to", "support"]):
        return "question"

    return "general"


def _estimate_priority(title: str, body: str, labels: list) -> str:
    """Estimate issue priority based on content and labels."""
    combined = f"{title} {body} {' '.join(labels)}".lower()

    if any(word in combined for word in ["critical", "urgent", "security", "crash", "data loss"]):
        return "high"
    if any(word in combined for word in ["bug", "error", "broken", "regression"]):
        return "medium"

    return "low"
