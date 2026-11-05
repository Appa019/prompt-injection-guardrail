import unittest

from expenses.policy import Category, Expense, decide
from expenses.receipt import read_receipt


def expense(amount, category):
    return Expense(amount=amount, vendor="Coastal Marine", category=category)


class PolicyTest(unittest.TestCase):
    def test_jet_ski_goes_to_a_person_even_as_work_equipment(self):
        self.assertEqual(decide(expense(17_900, Category.WORK_EQUIPMENT)), "human_review")

    def test_category_outside_the_list_is_rejected(self):
        self.assertEqual(decide(expense(17_900, Category.OTHER)), "reject")

    def test_small_allowed_expense_is_approved(self):
        self.assertEqual(decide(expense(42, Category.TRAVEL)), "approve")
        self.assertEqual(decide(expense(100, Category.MEALS)), "approve")

    def test_one_cent_over_the_limit_goes_to_a_person(self):
        self.assertEqual(decide(expense(100.01, Category.MEALS)), "human_review")

    def test_receipt_carries_the_hidden_instruction(self):
        self.assertIn("pre-approved by the board", read_receipt())


if __name__ == "__main__":
    unittest.main()
