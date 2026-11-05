"""After: the model only fills a closed schema; code decides. The agent has no tool that approves or pays.

Run: python after.py [times]
"""

import sys

from openai import OpenAI

from expenses.config import MODEL, load_env
from expenses.policy import Expense, decide
from expenses.receipt import read_receipt

INSTRUCTIONS = "Extract the expense fields from the receipt. Return data only."


def extract(client, receipt) -> Expense:
    response = client.responses.parse(model=MODEL, instructions=INSTRUCTIONS, input=receipt, text_format=Expense)
    if response.output_parsed is None:
        raise SystemExit("The model returned no parsed fields (refusal or empty output).")
    return response.output_parsed


def main():
    times = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    load_env()
    client = OpenAI()
    receipt = read_receipt()
    for i in range(1, times + 1):
        expense = extract(client, receipt)
        # Even if the hidden text pushes the category to work_equipment, the amount sends it to a person.
        print(f"run {i}: {expense.category.value}, ${expense.amount:,.2f} -> {decide(expense)}")


if __name__ == "__main__":
    main()
