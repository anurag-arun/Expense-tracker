import csv
from datetime import datetime

def add_expense():
    date = input("Enter date(YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')

    category = input("Enter category (e.g. Food, Transport, etc.): ")
    amount = input("Enter amount: ")

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    
    with open("expenses.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])
        print("Expense added successfully.")

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

view_expenses()

def show_total_by_category():
    totals = {}

    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header 

            for row in reader:
                category = row[1]
                amount = float(row[2])
                totals[category] = totals.get(category, 0) + amount
        
        print("\nTotal expenses by category:")
        for category, total in totals.items():
            print(f"{category}: Rs{amount:.2f}")

    except FileNotFoundError:
        print("No expenses found.")

show_total_by_category()

def main_menu():
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Expenses by Category")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_total_by_category()
        elif choice == "4":
            print("Exiting the Expense Tracker.")
            break
        else:
            print("Invalid choice. Please try again.")

main_menu()
