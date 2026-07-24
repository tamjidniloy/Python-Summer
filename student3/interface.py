from stuedent1.expense_model import CATEGORIES, MENU_OPTIONS, Expense, validate_date


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def read_date(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and value == "":
            return None
        try:
            return validate_date(value)
        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")


def read_positive_amount(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and value == "":
            return None
        try:
            amount = float(value)
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Enter a valid numeric amount.")


def choose_category(allow_blank=False):
    while True:
        print("\nCategories:")
        for index, category in enumerate(CATEGORIES, start=1):
            print(f"{index}. {category}")

        value = input("Choose category number: ").strip()
        if allow_blank and value == "":
            return None

        try:
            choice = int(value)
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print("Category choice is out of range.")
        except ValueError:
            print("Enter a number for the category.")


def create_expense_from_input(manager):
    while True:
        expense_id = read_non_empty("Expense ID: ")
        if expense_id.lower() not in manager.used_ids:
            break
        print("Duplicate expense ID. Please enter a unique ID.")

    expense_date = read_date("Date (YYYY-MM-DD): ")
    category = choose_category()
    description = read_non_empty("Description: ")
    amount = read_positive_amount("Amount: ")
    return Expense(expense_id, expense_date, category, description, amount)


def format_expense_table(expenses):
    if not expenses:
        return "No expense records found."

    lines = [
        f"{'ID':<10} {'Date':<12} {'Category':<15} {'Amount':>10} Description",
        "-" * 70,
    ]
    for expense in expenses:
        lines.append(
            f"{expense.expense_id:<10} "
            f"{expense.expense_date:<12} "
            f"{expense.category:<15} "
            f"{expense.amount:>10.2f} "
            f"{expense.description}"
        )
    return "\n".join(lines)


def display_menu():
    print("\nMoneyWise Tracker")
    print("Personal Expense and Budget Management System")
    for option in MENU_OPTIONS:
        print(option)


def add_expense_screen(manager):
    print("\nAdd Expense")
    expense = create_expense_from_input(manager)
    success, message = manager.add_expense(expense)
    print(message)
    if success:
        print(manager.save_expenses())


def view_expenses_screen(manager):
    print("\nAll Expenses")
    print(format_expense_table(manager.expenses))


def search_expense_screen(manager):
    print("\nSearch Expense")
    expense_id = read_non_empty("Enter expense ID: ")
    expense = manager.find_expense(expense_id)
    if expense is None:
        print("Expense not found.")
    else:
        print(format_expense_table([expense]))


def update_expense_screen(manager):
    print("\nUpdate Expense")
    expense_id = read_non_empty("Enter expense ID to update: ")
    expense = manager.find_expense(expense_id)
    if expense is None:
        print("Expense not found.")
        return

    print("Press Enter to keep the current value.")
    expense_date = read_date(f"Date ({expense.expense_date}): ", allow_blank=True)
    category = choose_category(allow_blank=True)
    description = input(f"Description ({expense.description}): ").strip() or None
    amount = read_positive_amount(f"Amount ({expense.amount:.2f}): ", allow_blank=True)

    success, message = manager.update_expense(
        expense_id,
        expense_date,
        category,
        description,
        amount,
    )
    print(message)
    if success:
        print(manager.save_expenses())


def delete_expense_screen(manager):
    print("\nDelete Expense")
    expense_id = read_non_empty("Enter expense ID to delete: ")
    success, message = manager.delete_expense(expense_id)
    print(message)
    if success:
        print(manager.save_expenses())


def analysis_screen(manager):
    print("\nSpending Analysis")
    statistics = manager.spending_statistics()
    if statistics is None:
        print("No expense records are available for analysis.")
        return

    print(f"Total spending: {statistics['total']:.2f}")
    print(f"Average expense: {statistics['average']:.2f}")
    print(f"Median expense: {statistics['median']:.2f}")
    print(f"Standard deviation: {statistics['standard_deviation']:.2f}")
    print(f"Minimum expense: {statistics['minimum']:.2f}")
    print(f"Maximum expense: {statistics['maximum']:.2f}")
    print(f"Highest spending category: {statistics['highest_category']}")
    print(
        "Highest single expense: "
        f"{statistics['highest_expense'].description} "
        f"({statistics['highest_expense'].amount:.2f})"
    )
    print(f"Monthly average spending: {statistics['monthly_average']:.2f}")
    print("Unique categories used:", ", ".join(statistics["unique_categories"]))

    print("\nCategory Summary")
    for category, total in statistics["category_totals"].items():
        print(f"{category:<15} {total:>10.2f}")

    print("\nMonthly Summary")
    for month_key, total in statistics["monthly_totals"].items():
        print(f"{month_key:<15} {total:>10.2f}")

    monthly_budget = read_positive_amount("\nEnter monthly budget for warning: ")
    print(manager.budget_status(monthly_budget))


def run_application(manager):
    print(manager.load_expenses())

    while True:
        display_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_expense_screen(manager)
        elif choice == "2":
            view_expenses_screen(manager)
        elif choice == "3":
            search_expense_screen(manager)
        elif choice == "4":
            update_expense_screen(manager)
        elif choice == "5":
            delete_expense_screen(manager)
        elif choice == "6":
            analysis_screen(manager)
        elif choice == "7":
            print(manager.save_expenses())
        elif choice == "8":
            print(manager.load_expenses())
        elif choice == "0":
            print(manager.save_expenses())
            print("Thank you for using MoneyWise Tracker.")
            break
        else:
            print("Invalid menu choice. Please try again.")
