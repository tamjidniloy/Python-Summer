from dataclasses import dataclass
from datetime import datetime


CATEGORIES = (
    "Food",
    "Transport",
    "Education",
    "Health",
    "Bills",
    "Entertainment",
    "Savings",
    "Other",
)

MENU_OPTIONS = (
    "1. Add expense",
    "2. View all expenses",
    "3. Search expense by ID",
    "4. Update expense",
    "5. Delete expense",
    "6. Show spending analysis",
    "7. Save data",
    "8. Load data",
    "0. Exit",
)


@dataclass
class Expense:
    expense_id: str
    expense_date: str
    category: str
    description: str
    amount: float

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "expense_date": self.expense_date,
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
        }

    @classmethod
    def from_dict(cls, record):
        expense_id = str(record["expense_id"]).strip()
        expense_date = str(record["expense_date"]).strip()
        category = str(record["category"]).strip()
        description = str(record["description"]).strip()
        amount = float(record["amount"])

        validate_date(expense_date)
        if not expense_id or not description:
            raise ValueError("ID and description cannot be empty.")
        if category not in CATEGORIES:
            raise ValueError("Invalid category.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")

        return cls(expense_id, expense_date, category, description, amount)


def validate_date(value):
    datetime.strptime(value, "%Y-%m-%d")
    return value
