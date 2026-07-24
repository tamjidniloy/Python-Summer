import json
from pathlib import Path

import numpy as np

from stuedent1.expense_model import Expense


class ExpenseManager:
    def __init__(self, data_file):
        self.data_file = Path(data_file)
        self.expenses = []
        self.used_ids = set()

    def load_expenses(self):
        if not self.data_file.exists():
            self.expenses = []
            self.used_ids = set()
            return "No data file found. A new file will be created when you save."

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                records = json.load(file)
        except json.JSONDecodeError:
            self.expenses = []
            self.used_ids = set()
            return "Data file is corrupted or empty. Started with no records."
        except OSError as error:
            self.expenses = []
            self.used_ids = set()
            return f"Could not read data file: {error}"

        if not isinstance(records, list):
            self.expenses = []
            self.used_ids = set()
            return "Data file format is invalid. Started with no records."

        loaded_expenses = []
        loaded_ids = set()
        skipped_records = 0

        for record in records:
            try:
                expense = Expense.from_dict(record)
                normalized_id = expense.expense_id.lower()
                if normalized_id in loaded_ids:
                    skipped_records += 1
                    continue
                loaded_expenses.append(expense)
                loaded_ids.add(normalized_id)
            except (KeyError, TypeError, ValueError):
                skipped_records += 1

        self.expenses = loaded_expenses
        self.used_ids = loaded_ids
        message = f"Loaded {len(self.expenses)} expense records."
        if skipped_records:
            message += f" Skipped {skipped_records} invalid records."
        return message

    def save_expenses(self):
        try:
            records = [expense.to_dict() for expense in self.expenses]
            with self.data_file.open("w", encoding="utf-8") as file:
                json.dump(records, file, indent=4)
            return "Data saved successfully."
        except OSError as error:
            return f"Could not save data: {error}"

    def add_expense(self, expense):
        normalized_id = expense.expense_id.lower()
        if normalized_id in self.used_ids:
            return False, "Duplicate expense ID. Please use a unique ID."

        self.expenses.append(expense)
        self.used_ids.add(normalized_id)
        return True, "Expense added successfully."

    def find_expense(self, expense_id):
        for expense in self.expenses:
            if expense.expense_id.lower() == expense_id.lower():
                return expense
        return None

    def update_expense(self, expense_id, expense_date, category, description, amount):
        expense = self.find_expense(expense_id)
        if expense is None:
            return False, "Expense not found."

        if expense_date is not None:
            expense.expense_date = expense_date
        if category is not None:
            expense.category = category
        if description is not None:
            expense.description = description
        if amount is not None:
            expense.amount = amount
        return True, "Expense updated successfully."

    def delete_expense(self, expense_id):
        expense = self.find_expense(expense_id)
        if expense is None:
            return False, "Expense not found."

        self.expenses.remove(expense)
        self.used_ids.remove(expense.expense_id.lower())
        return True, "Expense deleted successfully."

    def category_summary(self):
        totals = {}
        for expense in self.expenses:
            totals[expense.category] = totals.get(expense.category, 0) + expense.amount
        return totals

    def monthly_summary(self):
        totals = {}
        for expense in self.expenses:
            month_key = expense.expense_date[:7]
            totals[month_key] = totals.get(month_key, 0) + expense.amount
        return totals

    def spending_statistics(self):
        if not self.expenses:
            return None

        amounts = np.array([expense.amount for expense in self.expenses], dtype=float)
        category_totals = self.category_summary()
        monthly_totals = self.monthly_summary()
        highest_category = max(category_totals, key=category_totals.get)
        highest_expense = max(self.expenses, key=lambda expense: expense.amount)
        unique_categories = {expense.category for expense in self.expenses}

        return {
            "total": float(np.sum(amounts)),
            "average": float(np.mean(amounts)),
            "median": float(np.median(amounts)),
            "standard_deviation": float(np.std(amounts)),
            "minimum": float(np.min(amounts)),
            "maximum": float(np.max(amounts)),
            "highest_category": highest_category,
            "highest_expense": highest_expense,
            "monthly_average": float(np.mean(np.array(list(monthly_totals.values())))),
            "unique_categories": sorted(unique_categories),
            "category_totals": category_totals,
            "monthly_totals": monthly_totals,
        }

    def budget_status(self, monthly_budget):
        monthly_totals = self.monthly_summary()
        if not monthly_totals:
            return "No monthly spending data is available."

        current_month = max(monthly_totals)
        current_total = monthly_totals[current_month]
        remaining = monthly_budget - current_total

        if current_total > monthly_budget:
            return (
                f"Warning: {current_month} spending is over budget by "
                f"{abs(remaining):.2f}."
            )
        if current_total >= monthly_budget * 0.8:
            return (
                f"Careful: {current_month} spending has reached "
                f"{current_total / monthly_budget * 100:.1f}% of the budget."
            )
        return f"Good: {current_month} has {remaining:.2f} left in the budget."
