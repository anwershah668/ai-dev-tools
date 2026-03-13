"""Example: using DocGenerator to produce Markdown docs for a module."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.doc_generator import DocGenerator


def main():
    generator = DocGenerator()

    # Generate docs for the issue_summarizer module
    module_path = os.path.join(
        os.path.dirname(__file__), "..", "src", "issue_summarizer.py"
    )
    docs = generator.generate_docs(module_path)
    print(docs)


if __name__ == "__main__":
    main()
