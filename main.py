from pathlib import Path

from student2.expense_manager import ExpenseManager
from student3.interface import run_application


DATA_FILE = Path(__file__).with_name("expenses.json")


def main():
    manager = ExpenseManager(DATA_FILE)
    run_application(manager)


if __name__ == "__main__":
    main()
