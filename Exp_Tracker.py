import json
import os
from datetime import datetime, date

#----Constants-----

DATA_FILE = "expense_data.json"

VALID_TYPES = ["income", "expense"]

VALID_CATEGORIES = ["food", "travel", "rent", "salary", "shopping", "health", "other"]

# _Global Data Store_

transactions = []

budgets = {}

# Data Persistence

def save_data(transactions, budgets, filename=DATA_FILE):
    data = {"transactions": transactions, "budgets": budgets}
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Data saved to {filename}")

def load_data(filename=DATA_FILE):
    if not os.path.isfile(filename):
        return[],{}

    with open(filename, "r") as f:
        data = json.load(f)
    return data.get("transactions", []), data("budgets", {})

# Entry Point

if __name__ == "__main__":
    transactions, budgets = load_data()
    print("Loaded", len(transactions), "transactions.")

#add_transaction(transactions)
def add_transaction(transaction):
    print("\n--- Add New Transaction ---")

    # Step 1 : Type
    while True:
        t_type = input(f"Type ({'/'.join(VALID_TYPES)} or 'q' to quit: ").strip().lower()
        if t_type in VALID_TYPES:
            break
        print(f" Invalid. choose from: {VALID_TYPES}")

    #Step 2: Category

    while True:
        print(f" Categories: {', '.join(VALID_CATEGORIES)}")
        category = input("Category: ").strip().lower()
        if category in VALID_CATEGORIES:
            break
        print(f" Invalid. choose from: {VALID_CATEGORIES}")

    #Step 3: Amount

    while True:
        try:
            amount = float(input("Amount (Rs.): "))
            if amount <= 0:
                print(" Invalid Entry, Amount cannot be negative.")
                continue
            break
        except ValueError:
            print(" X Enter a Valid Amount.")

    #Step 4: Date

    while True:
        date_input = input(f"Date (YYYY-MM-DD) [Enter = today]: ").strip()
        if date_input == "":
            t_date = str(date.today())
            break
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            t_date = date_input
            break
        except ValueError:
            print(" X Enter a Valid Date. Enter in YYYY-MM-DD.")

    #Step 5: Note (Optional)

    note = input("Note (optional): ").strip()

    #Step 6: Transaction Dictionary
    transaction = {
        "type": t_type,
        "category": category,
        "amount": amount,
        "date": t_date,
        "note": note,
    }


    #Step 7: Append to the list
    transactions.append(transaction)
    print(f"Added transaction! Total Records: {len(transactions)}")

#view_transaction(transactions)

def view_transactions(transactions):
    print("\n--- All Transactions ---")

    #Guard clause
    if not transactions:
        print(" no transactions found")
        return

    #Header row
    print(f"{'#':<4} {'Date':<12} {'Type':<9} {'Category':<10} {'Amount':>10}  {'Note'}")
    print("-" * 60)

    #Data Rows
    for i, txn in enumerate(transactions, start=1):
        print(
            f"{i:<4} "
            f"{txn['date']:<12} "
            f"{txn['type']:<9} "
            f"{txn['category']:<10} "
            f"₹{txn['amount']:>12,.2f}  "
            f"{txn['note']}"
        )

"""
add_transaction(transactions)
add_transaction(transactions)
view_transactions(transactions)
"""

#Transaction Filters: filter_transaction(transactions, filters)
def filter_transaction(transactions, filters):
    """
    filter is a dict with any of the following keys:
    "type" : "income" or "expense
    "category" : e.g. "food" or "travel"
    "start_date" : "YYYY-MM-DD"
    "end_date" : "YYYY-MM-DD
    """
    result = transactions                 #starting with everything

    #Filter 1: by type
    if "type" in filters:
        result = [
            txn for txn in result
            if txn["type"] == filters["type"]
        ]

    #Filter 2: by category
    if "category" in filters:
        result = [
            txn for txn in result
            if txn["category"] == filters["category"]
        ]

    #Filter 3: by date range
    if "start_date" in filters or "end_date" in filters:
        start = datetime.strptime(
            filters.get("start_date", "2000-01-01"), "%Y-%m-%d"
        )
        end = datetime.strptime(
            filters.get('end_date', "2999-12-31"), "%Y-%m-%d"
        )
        result = [
            txn for txn in result
            if start <= datetime.strptime(txn["date"], "%Y-%m-%d") <= end
        ]

    if not result:
        print("No Match found.")
        return[]

    print(f"\n Found {len(result)} matching transaction(s):")
    view_transactions(result) #reuse the display function
    return(result)

#search menu for filter_transactions
def search_menu(transactions):
    """Interactive menu that builds the filter dict and calls filter_transactions."""
    print("\n--- Filter / Search ---")
    print("leave blank to skip any filter.\n")


    filters = {}

    t = input("Filter by type (income/expense): ").strip().lower()
    if t in VALID_CATEGORIES:
        filters["type"] = t

    c = input(f"Filter by category {VALID_CATEGORIES}: ").strip().lower()
    if c in VALID_CATEGORIES:
        filters["category"] = c
    
    sd =input("Start date (YYYY-MM-DD): ").strip()
    if sd:
        filters["start_date"] = sd

    ed = input("End date (YYYY-MM-DD): ").strip()
    if ed:
        filters["end_date"] = ed

    filter_transaction(transactions, filters)

add_transaction(transactions)