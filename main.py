import csv
from datetime import datetime
import matplotlib.pyplot as plt
import sqlite3

def create_table():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    try:
        amount = float(input("Enter amount: Rs"))
    except ValueError:
        print("Invalid amount.")
        return

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)',
                   (date, category, amount))
    conn.commit()
    conn.close()

    print("✅ Expense added successfully.")


def view_expenses():
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            print("\nExpenses:")
            for row in reader:
                print(f"Date: {row[0]}, Category: {row[1]}, Amount: Rs{row[2]}")
    except FileNotFoundError:
        print("No expenses found.")

def view_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, category, amount FROM expenses')
    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("No expenses found.")
        return

    print("\nExpenses:")
    for expense in expenses:
        date, category, amount = expense
        print(f"Date: {date}, Category: {category}, Amount: Rs{amount:.2f}")

def show_total_by_category():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    totals = cursor.fetchall()
    conn.close()

    if not totals:
        print("No expenses found.")
        return

    print("\nTotal expenses by category:")
    for category, total in totals:
        print(f"{category}: Rs{total:.2f}")
def filter_expenses():
    print("\nFilter by:")
    print("1. Category")
    print("2. Date (YYYY-MM-DD)")
    choice = input("Choose filter type: ")

    try:
        with open('expenses.csv', 'r') as file:
            next(file)  # Skip header
            filtered = []

            if choice == '1':
                category = input("Enter category to filter by: ").strip().lower()
                for line in file:
                    date, cat, amount = line.strip().split(',')
                    if cat.lower() == category:
                        filtered.append((date, cat, amount))

            elif choice == '2':
                target_date = input("Enter date to filter by (YYYY-MM-DD): ").strip()
                for line in file:
                    date, cat, amount = line.strip().split(',')
                    if date == target_date:
                        filtered.append((date, cat, amount))

            else:
                print("⚠️ Invalid filter choice.")
                return

        if filtered:
            print("\n📋 Filtered Expenses:")
            for entry in filtered:
                print(f"{entry[0]} | {entry[1]} | ₹{entry[2]}")
        else:
            print("No matching expenses found.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    

def generate_summary_report():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Total expense
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0

    # Total by category
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_totals = cursor.fetchall()

    # Monthly total
    cursor.execute("SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM expenses GROUP BY month")
    monthly_totals = cursor.fetchall()

    # Create file
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"expense_summary_{now}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("📊 Expense Summary Report\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Expense: Rs{total:.2f}\n\n")

        f.write("Expenses by Category:\n")
        for category, amount in category_totals:
            f.write(f" - {category}: Rs{amount:.2f}\n")

        f.write("\nExpenses by Month:\n")
        for month, amount in monthly_totals:
            f.write(f" - {month}: Rs{amount:.2f}\n")

    conn.close()
    print(f"\n✅ Summary report saved as '{filename}'")


def export_filtered_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    print("\n--- Export Filtered Expenses ---")
    print("1. Filter by Category")
    print("2. Filter by Date")
    choice = input("Choose filter option: ")

    if choice == "1":
        category = input("Enter category: ")
        cursor.execute("SELECT date, category, amount FROM expenses WHERE category = ?", (category,))
        rows = cursor.fetchall()
        filter_type = f"category_{category}"

    elif choice == "2":
        date = input("Enter date (YYYY-MM-DD): ")
        cursor.execute("SELECT date, category, amount FROM expenses WHERE date = ?", (date,))
        rows = cursor.fetchall()
        filter_type = f"date_{date}"
    else:
        print("Invalid choice.")
        return

    if not rows:
        print("No records found.")
        return

    print("Choose export format:")
    print("1. .txt")
    print("2. .csv")
    format_choice = input("Your choice: ")

    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if format_choice == "1":
        filename = f"filtered_expenses_{filter_type}_{now}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Filtered Expenses - {filter_type}\n")
            for row in rows:
                f.write(f"Date: {row[0]}, Category: {row[1]}, Amount: Rs{row[2]:.2f}\n")

    elif format_choice == "2":
        filename = f"filtered_expenses_{filter_type}_{now}.csv"
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Amount"])
            writer.writerows(rows)
    else:
        print("Invalid format.")
        return

    print(f"\n✅ Filtered expenses exported to '{filename}'")
    conn.close()


def main_menu():
    create_table()  # ensure DB table exists before anything else
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Expenses by Category")
        print("4. View total expense for a month")
        print("5. Filter expenses by category/date")
        print("6. Show bar chart of expenses by category")
        print("7. Generate Summary Report")
        print("8. Export filtered data to .txt/.csv")
        print("9. Exit")
        choice = input("Enter your choice : ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_total_by_category()
        elif choice == "4":
            view_monthly_total()
        elif choice == "5":
            filter_expenses()
        elif choice == "6":
            show_expense_chart()
        elif choice == "7":
            generate_summary_report()
        elif choice == "8":
            export_filtered_expenses()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def show_expense_chart():
    try:
        with open('expenses.csv', 'r') as file:
            next(file)  # skip header
            category_totals = {}

            for line in file:
                date, category, amount = line.strip().split(',')
                amount = float(amount)
                category_totals[category] = category_totals.get(category, 0) + amount

        if not category_totals:
            print("No data to display.")
            return

        categories = list(category_totals.keys())
        totals = list(category_totals.values())

        plt.figure(figsize=(8, 5))
        plt.bar(categories, totals, color='skyblue')
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Spent (₹)")
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("⚠️ 'expenses.csv' not found.")
    except Exception as e:
        print(f"⚠️ Error generating chart: {e}")

main_menu()

from datetime import datetime

def view_monthly_total():
    try:
        target_month = input("Enter month and year (MM/YYYY): ")
        target_date =datetime.strptime(target_month, "%m%Y")
        total = 0

        with open('expense.csv', 'r') as file:
            next(file) #skip header
            for line in file:
               date_str, _, amoun_str = line.strp().split(',')
               date_obj = datetime.strptime(date_str, "%Y-%m-%d")
               if date_obj.month == target_date.month and date_obj.year == target_date.year:
                   total += float(amount_str) # type: ignore
        print(f"Total expenses for {target_month}: Rs{total:.2f}")
    except Exception as e:
        print(f"Error: {e}")

def filter_expenses():
    print("\nFilter by:")
    print("1. Category")
    print("2. Date (YYYY-M-DD)")
    choice = input("Choose Filter Type: ")

    try:
        with open('expenses.csv', 'r') as file:
            next(file) #skip header
            filtered = []

            if choice == '1':
                category = input("Enter category to fiter by: ").strip().lower()
                for line in file:
                    date,cat, amount = line.strip().split(',')
                    if cat.lower() ==category:
                        filtered.append((date, cat, amount))
            elif choice == '2':
                target_date = input("Enter date to filter by (YYYY-MM-DD): ")
                for line in file:
                    date, cat, amount = line.strip().split(',')
                    if date == target_date:
                        filtered.append((date, cat, amount))
            else:
                print("Invalid choice.")
                return
            
        if filtered:
            print("\nFiltered Expenses:")
            for entry in filtered:
                print(f"{entry[0]} | {entry[1]} | Rs{entry[2]}")
        else:
            print("No matching expenses found.")
    except Exception as e:
        print(f"Error: {e}")


def generate_summary_report():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Total expense
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0

    # Total by category
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_totals = cursor.fetchall()

    # Monthly total
    cursor.execute("SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM expenses GROUP BY month")
    monthly_totals = cursor.fetchall()

    # Create file
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"expense_summary_{now}.txt"

    with open(filename, "w") as f:
        f.write("📊 Expense Summary Report\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Expense: Rs{total:.2f}\n\n")

        f.write("Expenses by Category:\n")
        for category, amount in category_totals:
            f.write(f" - {category}: Rs{amount:.2f}\n")

        f.write("\nExpenses by Month:\n")
        for month, amount in monthly_totals:
            f.write(f" - {month}: Rs{amount:.2f}\n")

    conn.close()
    print(f"\n✅ Summary report saved as '{filename}'")

                
