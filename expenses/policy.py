"""The company's rules, in plain code. Same input, same answer, whatever the receipt says."""

from enum import Enum

from pydantic import BaseModel


class Category(str, Enum):
    WORK_EQUIPMENT = "work_equipment"
    TRAVEL = "travel"
    MEALS = "meals"
    OTHER = "other"


class Expense(BaseModel):
    amount: float
    vendor: str
    category: Category


ALLOWED = {Category.WORK_EQUIPMENT, Category.TRAVEL, Category.MEALS}
HUMAN_REVIEW_ABOVE = 100


def decide(expense: Expense) -> str:
    if expense.category not in ALLOWED:
        return "reject"
    if expense.amount > HUMAN_REVIEW_ABOVE:
        return "human_review"
    return "approve"
