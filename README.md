# MoneyWise Tracker

MoneyWise Tracker is a menu-driven Python project for recording personal expenses and checking basic budget information.

## Files

- `main.py` - small starter file that runs the full application
- `stuedent1/expense_model.py` - expense class, categories, menu choices, and date validation
- `student2/expense_manager.py` - expense collection, JSON save/load, search/update/delete, and NumPy analysis
- `student3/interface.py` - menu screens, user input, validation messages, and output display
- `expenses.json` - sample saved data with 10 expense records

## Setup

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

## Main Features

- Add a new expense with validation
- View all saved expenses
- Search expense by ID
- Update existing expense
- Delete expense
- Save and load JSON data
- Show NumPy-based spending analysis and budget warning
