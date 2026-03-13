#!/usr/bin/env python3
"""Example: Using the Code Reviewer.

This example demonstrates how to use the code_reviewer module
to perform automated code reviews.
"""

from ai_dev_tools.code_reviewer import review_code


def main():
    # Sample code to review
    sample_code = '''
def calculate_total(items):
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    return total

# TODO: add input validation
def process_order(order_id, items, customer):
    total = calculate_total(items)
    tax = total * 0.08
    return {
        "order_id": order_id,
        "total": total + tax,
        "customer": customer,
    }

class OrderManager:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    # FIXME: this needs pagination
    def get_all_orders(self):
        return self.orders
'''

    print("=== Code Review Results ===")
    result = review_code(sample_code, filename="order_service.py")
    print(f"File: {result['filename']}")
    print(f"Total issues: {result['total_issues']}")
    print(f"Summary: {result['summary']}")
    print()

    if result["missing_docstrings"]:
        print("Missing Docstrings:")
        for item in result["missing_docstrings"]:
            print(f"  - {item['suggestion']}")
        print()

    if result["todos"]:
        print("TODO/FIXME Comments:")
        for item in result["todos"]:
            print(f"  - {item['suggestion']}")
        print()

    if result["long_functions"]:
        print("Long Functions:")
        for item in result["long_functions"]:
            print(f"  - {item['suggestion']}")


if __name__ == "__main__":
    main()
