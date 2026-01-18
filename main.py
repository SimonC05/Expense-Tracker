import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker")
cursor.execute("USE expense_tracker")
cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
               Id INT AUTO_INCREMENT PRIMARY KEY,
               Expense VARCHAR(50),
               Category VARCHAR(50),
               Date DATE,
               Amount DECIMAL(10,2)
               )""")
conn.commit()

def add_expense():
    expense = input("\nExpense: ")
    category = input("Category: ")
    while True:
        date = input("Date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("\nEnter a valid date format.")
    while True:
        try:
            amount = float(input("Amount: "))
            break
        except ValueError:
            print("\nEnter a valid amount.")

    cursor.execute("""INSERT INTO expenses (expense, category, date, amount)
                   VALUES (%s, %s, %s, %s)""",
                   (expense, category, date, amount))
    conn.commit()

def delete_expense():
    try:
        delete = int(input("\nEnter ID of expense to delete: "))

        cursor.execute(f"DELETE FROM expenses WHERE Id = {delete}")
        conn.commit()

        if cursor.rowcount == 0:
            print("There is no expense with that ID.")
        else:
            print(f"Expense with ID {delete} was successfully deleted.")

    except ValueError:
        print("Not a valid ID.")

def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    if not rows:
        print("\nYou do not have any expenses.")
        return
    
    print("\nAll Expenses:")
    print("{:<5} {:<15} {:<15} {:<15} {:<10}".format("ID", "Expense", "Category", "Date", "Amount"))
    print("-"*65)

    for row in rows:
        print("{:<5} {:<15} {:<15} {:<15} ${:<10.2f}".format(row[0], row[1], row[2], str(row[3]), row[4]))

def view_filtered_expenses():
    print("\n--- Filtering Options ---")
    print("1. Category")
    print("2. Time Period")
    print("3. Price")

    choice = input("Choose an action: ")

    if choice == '1':
        cursor.execute("SELECT Category, COUNT(Category) FROM expenses GROUP BY Category ORDER BY COUNT(Category) DESC")
        categories = cursor.fetchall()
        print()

        for category in categories:
            print(f"{category[0]}: {category[1]}")

        view_category = input("\nWhich category would you like to view: ")
        cursor.execute("SELECT * FROM expenses WHERE Category = %s ORDER BY Expense", (view_category,))
        rows = cursor.fetchall()

        if not rows:
            print("\nThere are no expenses in that category.")
        else:
            print(f"\n{view_category} Expenses:")
            print("{:<5} {:<15} {:<15} {:<15} {:<10}".format("ID", "Expense", "Category", "Date", "Amount"))
            print("-"*65)

            for row in rows:
                print("{:<5} {:<15} {:<15} {:<15} ${:<10.2f}".format(row[0], row[1], row[2], str(row[3]), row[4]))

    elif choice == '2':
        try:
            year = int(input("\nEnter year to view: "))
            print("\n--- Months ---")
            print("1. January")
            print("2. February")
            print("3. March")
            print("4. April")
            print("5. May")
            print("6. June")
            print("7. July")
            print("8. August")
            print("9. September")
            print("10. October")
            print("11. November")
            print("12. December")
            print("13. Whole Year")

            try: 
                month = int(input("Enter month to view: "))

                if month == 13:
                    cursor.execute("SELECT * FROM expenses WHERE YEAR(Date) = %s ORDER BY MONTH(Date), DAY(Date)", (year,))
                else:
                    cursor.execute("SELECT * FROM expenses WHERE YEAR(Date) = %s AND MONTH(Date) = %s ORDER BY DAY(Date) ASC", (year, month))
                rows = cursor.fetchall()

                if not rows:
                    print("\nThere are no expenses in that time frame.")
                else:
                    print("\nExpenses:")
                    print("{:<5} {:<15} {:<15} {:<15} {:<10}".format("ID", "Expense", "Category", "Date", "Amount"))
                    print("-"*65)

                    for row in rows:
                        print("{:<5} {:<15} {:<15} {:<15} ${:<10.2f}".format(row[0], row[1], row[2], str(row[3]), row[4]))

            except ValueError:
                print("\nNot a valid month.")
        except ValueError:
            print("\nNot a valid year.")

    elif choice == '3':
        print("\n--- Price Filtering Options ---")
        print("1. Less Than")
        print("2. Greater Than")
        print("3. Exact")
        print("4. Range")

        filter = input("Enter filtering option: ")

        if filter == '1':
            try:
                amount = float(input("Filter expenses less than: "))
                cursor.execute("SELECT * FROM expenses WHERE Amount < %s ORDER BY Amount DESC", (amount,))
                rows = cursor.fetchall()

                if not rows:
                    print(f"\nThere are no expenses less than ${amount:.2f}.")
                else:
                    print(f"\nExpenses Less Than ${amount:.2f}:")
                    print("{:<5} {:<15} {:<15} {:<15} {:<10}".format("ID", "Expense", "Category", "Date", "Amount"))
                    print("-"*65)

                    for row in rows:
                        print("{:<5} {:<15} {:<15} {:<15} ${:<10.2f}".format(row[0], row[1], row[2], str(row[3]), row[4]))

            except ValueError:
                print("\nNot a valid amount.")

        elif filter == '2':
            try:
                amount = float(input("Filter expenses greater than: "))
                cursor.execute("SELECT * FROM expenses WHERE Amount > %s ORDER BY Amount ASC", (amount,))
                rows = cursor.fetchall()

                if not rows:
                    print(f"\nThere are no expenses greater than ${amount:.2f}.")
                else:
                    print(f"\nExpenses Greater Than ${amount:.2f}:")
                    print("{:<5} {:<15} {:<15} {:<15} {:<10}".format("ID", "Expense", "Category", "Date", "Amount"))
                    print("-"*65)

                    for row in rows:
                        print("{:<5} {:<15} {:<15} {:<15} ${:<10.2f}".format(row[0], row[1], row[2], str(row[3]), row[4]))

            except ValueError:
                print("\nNot a valid amount.")

        if filter == '3':
            try:
                amount = float(input("Filter expenses with amount: "))
                cursor.execute("SELECT * FROM expenses WHERE Amount = %s", (amount,))
                rows = cursor.fetchall()

                if not rows:
                     print(f"\nThere are no expenses that are ${amount:.2f}.")
                else:
                    print(f"\nExpenses Equal To ${amount:.2f}:")
                    print("{:<5} {:<15} {:<15} {:<15} {:<10}".format("ID", "Expense", "Category", "Date", "Amount"))
                    print("-"*65)

                    for row in rows:
                        print("{:<5} {:<15} {:<15} {:<15} ${:<10.2f}".format(row[0], row[1], row[2], str(row[3]), row[4]))

            except ValueError:
                print("\nNot a valid amount.")

        if filter == '4':
            try:
                lower_amount = float(input("Lower Bound: "))
                upper_amount = float(input("Upper Bound: "))
                if lower_amount > upper_amount:
                    print("\nInvalid Range.")
                else:
                    cursor.execute("SELECT * FROM expenses WHERE Amount >= %s AND Amount <= %s ORDER BY Amount ASC", (lower_amount, upper_amount))
                    rows = cursor.fetchall()

                    if not rows:
                        print(f"\nThere are no expenses in the range ${lower_amount:.2f} - ${upper_amount:.2f}.")
                    else:
                        print(f"\nExpenses Between ${lower_amount:.2f} - ${upper_amount:.2f}:")
                        print("{:<5} {:<15} {:<15} {:<15} {:<10}".format("ID", "Expense", "Category", "Date", "Amount"))
                        print("-"*65)

                        for row in rows:
                            print("{:<5} {:<15} {:<15} {:<15} ${:<10.2f}".format(row[0], row[1], row[2], str(row[3]), row[4]))

            except ValueError:
                print("\nNot a valid amount.")

    else:
        print("\nNot a valid option.")

def total_spending():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    total = sum(row[4] for row in rows)
    print(f"\nTotal Spending: ${total:.2f}")

def reset_expense_tracker():
    confirm = input("\nThis is delete all expenses. Are you sure? Type 'Yes' to confirm: ")
    
    if confirm == 'Yes':
        cursor.execute("DELETE FROM expenses")
        cursor.execute("ALTER TABLE expenses AUTO_INCREMENT = 1")
        conn.commit()

        print("\nExpenses Tracker Successfully Reset.")
    else:
        print("\nReset Cancelled.")

def menu():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. Delete Expense")
        print("3. View Expenses")
        print("4. View Filtered Expenses")
        print("5. Total Spending")
        print("6. Reset Expense Tracker")
        print("7. Exit")
        choice = input("Choose an action: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            delete_expense()
        elif choice == '3':
            view_expenses()
        elif choice == '4':
            view_filtered_expenses()
        elif choice == '5':
            total_spending()
        elif choice == '6':
            reset_expense_tracker()
        elif choice == '7':
            break
        else:
            print("\nInvalid Option. Try Again.")

if __name__ == "__main__":
    menu()