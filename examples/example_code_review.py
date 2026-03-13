"""Example: using CodeReviewTool to review a Python snippet."""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.code_review_tool import CodeReviewTool


SAMPLE_CODE = """\
class DataProcessor:
    def process(self, data, config, logger, output, formatter, validator, cache):
        results = []
        for item in data:
            try:
                if item > 0:
                    if item < 100:
                        if item % 2 == 0:
                            results.append(item * 2)
                        else:
                            results.append(item)
            except:
                pass
        return results


def fetch_records(ids=[]):
    records = []
    for id in ids:
        records.append({"id": id})
    return records
"""


def main():
    reviewer = CodeReviewTool()

    # Write sample code to a temporary file so review_file() can be used
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(SAMPLE_CODE)
        tmp_path = tmp.name

    suggestions = reviewer.review_file(tmp_path)
    os.unlink(tmp_path)

    if suggestions:
        print(f"Found {len(suggestions)} suggestion(s):\n")
        for suggestion in suggestions:
            print(f"  {suggestion}")
    else:
        print("No suggestions — code looks good!")


if __name__ == "__main__":
    main()
