"""Issue summarizer module.

Condenses a list of GitHub-style issue comments into a short, actionable
summary without requiring an external API.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import List


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class IssueSummarizer:
    """Summarize a list of issue comments into a concise plain-text summary.

    The summarizer uses a lightweight extractive approach:
    1. It identifies the most frequently mentioned keywords (excluding common
       stop-words) to surface the main topic.
    2. It picks the single most "representative" sentence – the one that
       contains the most high-frequency keywords – as the summary headline.
    3. It appends a brief note about the total number of contributions.

    No external dependencies or API keys are required.

    Example::

        summarizer = IssueSummarizer()
        comments = [
            "The login button is broken on mobile.",
            "Reproduces on iOS 16 and Android 13.",
            "The CSS media query looks wrong.",
        ]
        print(summarizer.summarize(comments))
    """

    # Common English stop-words to ignore when scoring keywords
    _STOP_WORDS: frozenset[str] = frozenset(
        {
            "a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
            "for", "of", "with", "is", "it", "this", "that", "was", "are",
            "be", "have", "has", "had", "do", "does", "did", "will", "would",
            "can", "could", "should", "may", "might", "i", "we", "you", "he",
            "she", "they", "my", "our", "your", "its", "their", "also",
            "just", "not", "no", "if", "as", "from", "by", "so", "up",
            "about", "into", "than", "then", "there", "when", "where",
            "which", "who", "whom", "what", "how", "all", "any", "been",
            "being", "more", "some", "such", "own", "same", "other",
        }
    )

    def summarize(self, comments: List[str], top_keywords: int = 5) -> str:
        """Summarize the provided issue comments.

        Args:
            comments: A list of comment strings from a GitHub issue thread.
            top_keywords: Number of top keywords to surface in the summary.

        Returns:
            A plain-text summary string.

        Raises:
            ValueError: If *comments* is empty.
        """
        if not comments:
            raise ValueError("comments list must not be empty")

        # Collect all sentences from all comments
        sentences = self._split_sentences(comments)

        # Score keywords across the full text
        word_freq = self._word_frequencies(" ".join(comments))
        top_words = [w for w, _ in word_freq.most_common(top_keywords)]

        # Pick the sentence that mentions the most high-frequency keywords
        best_sentence = self._best_sentence(sentences, set(top_words))

        # Compose output
        keyword_str = ", ".join(top_words) if top_words else "general"
        n = len(comments)
        noun = "comment" if n == 1 else "comments"
        lines = [
            f"Summary ({n} {noun}):",
            f"  {best_sentence}",
            f"Key topics: {keyword_str}.",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _split_sentences(self, comments: List[str]) -> List[str]:
        """Return a flat list of sentences extracted from all comments."""
        sentences: List[str] = []
        for comment in comments:
            # Split on '.', '!', '?' followed by whitespace or end-of-string
            parts = re.split(r"(?<=[.!?])\s+", comment.strip())
            sentences.extend(p.strip() for p in parts if p.strip())
        return sentences

    def _word_frequencies(self, text: str) -> Counter:
        """Return a Counter of meaningful words in *text*."""
        words = re.findall(r"[a-zA-Z]+", text.lower())
        filtered = [w for w in words if w not in self._STOP_WORDS and len(w) > 2]
        return Counter(filtered)

    def _best_sentence(self, sentences: List[str], keywords: set) -> str:
        """Return the sentence with the highest keyword overlap score."""
        if not sentences:
            return ""

        def score(sentence: str) -> int:
            words = set(re.findall(r"[a-zA-Z]+", sentence.lower()))
            return len(words & keywords)

        return max(sentences, key=score)
