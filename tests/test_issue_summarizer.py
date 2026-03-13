"""Unit tests for src.issue_summarizer."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.issue_summarizer import IssueSummarizer


class TestIssueSummarizerBasic(unittest.TestCase):
    def setUp(self):
        self.summarizer = IssueSummarizer()

    def test_summary_contains_header(self):
        result = self.summarizer.summarize("Login button is broken on iOS.")
        self.assertIn("## Issue Summary", result)

    def test_summary_contains_problem(self):
        result = self.summarizer.summarize("Login button is broken on iOS.")
        self.assertIn("**Problem:**", result)
        self.assertIn("Login button is broken on iOS.", result)

    def test_empty_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.summarizer.summarize("")

    def test_whitespace_only_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.summarizer.summarize("   \n  ")

    def test_steps_section_extracted(self):
        issue = (
            "App crashes.\n"
            "Steps to reproduce:\n"
            "1. Open the app\n"
            "2. Click submit\n"
        )
        result = self.summarizer.summarize(issue)
        self.assertIn("Steps to Reproduce", result)
        self.assertIn("Open the app", result)
        self.assertIn("Click submit", result)

    def test_expected_section_extracted(self):
        issue = (
            "Bug in login.\n"
            "Expected behavior: Modal appears.\n"
            "Actual behavior: Nothing happens.\n"
        )
        result = self.summarizer.summarize(issue)
        self.assertIn("**Expected:**", result)
        self.assertIn("Modal appears.", result)

    def test_actual_section_extracted(self):
        issue = (
            "Bug in login.\n"
            "Expected behavior: Modal appears.\n"
            "Actual behavior: Nothing happens.\n"
        )
        result = self.summarizer.summarize(issue)
        self.assertIn("**Actual:**", result)
        self.assertIn("Nothing happens.", result)

    def test_environment_section_extracted(self):
        issue = "Bug. Environment: macOS 13, Python 3.11."
        result = self.summarizer.summarize(issue)
        self.assertIn("**Environment:**", result)

    def test_returns_string(self):
        result = self.summarizer.summarize("Some issue text here.")
        self.assertIsInstance(result, str)

    def test_single_word_input(self):
        # Should not raise; returns a minimal summary.
        result = self.summarizer.summarize("Crash")
        self.assertIn("## Issue Summary", result)


if __name__ == "__main__":
    unittest.main()
