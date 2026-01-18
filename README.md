# Expense-Tracker
A simple **python** text-based expense tracker using **MySQL** for data storage.
Track your expenses, filter by category, date, or prices, view totals, and reset your tracker when needed.

---

## Features
- Automatically initalizes database expense_tracker and table expenses if they do not already exist
- Add, delete, and view expenses
- View filtered expenses by
  - Category
  - Time period (year/month)
  - Price (less than, greater than, exact, or range)
- Calculate total spending
- Reset expense tracker (deletes all expenses and resets IDs)

---

## Requirements
- Python 3.7+
- Python package: 'mysql-connector-python'
- MySQL Server installed and running
- Ensure to update MySQL credentials at top of file, changing "your_password" with your MySQL password

Install the package via pip:

```bash
pip install mysql-connector-python
