import json
import os
from datetime import datetime, date

# The Constants:
DATA_FILE = "expense_data.json"
VALID_TYPES = ["income", "expense"]
VALID_CATEGORIES = ["food", "travel", "rent", "salary", "shopping", "health", "other"]

# GLobal Data Stores
transactions = []
budgets = {}

# Sample Transaction (for reference) -
"""
{
    "type": "expense",
    "category": "food",
    "amount": "250.0",
    "date": "2026-01-30",
    "note": "lunch",
}
"""
# Data Persistence

def save_data(transactions, budgets, filename=DATA_FILE):
    data = {"transactions": transactions, "budgets": budgets}
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"  ✓ Data saved → {filename} ({len(transactions)} transactions)")

def load_data(filename=DATA_FILE):
    if not os.path.isfile(filename):
        print(" No saved data found. Starting fresh")
        return [], {}
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        t = data.get("transactions", [])
        b = data.get("budgets", {})
        print(f" ✓ Data loaded from {filename} ({len(t)} transactions) and {len(b)} budgets")
        return t, b
    except (json.JSONDecodeError, KeyError):
        print(" ⚠ Saved file is corrupted. Starting fresh.")
        return [], {}

# entry point

if __name__ == "__main__":
    transactions, budgets = load_data()
    print("Loaded",len(transactions), "transactions.")

def add_transaction(transactions):
    print("\n--- Add New Transaction ---")

    #Transaction Type
    while True:
        t_type = input(f"Type ({'/'.join(VALID_TYPES)}): ").strip().lower()
        if t_type in VALID_TYPES:
            break
        print(f"Invalid. Choose from: {VALID_TYPES}")

    #Category
    while True:
        print(f" Categories: {', '.join(VALID_CATEGORIES)}")
        category = input("Category: ").strip().lower()
        if category in VALID_CATEGORIES:
            break
        print(f"Invalid. Choose from: {VALID_CATEGORIES}")

    #Amount
    while True:
        try:
            amount = float(input("Amount (₹): "))
            if amount <= 0:
                print("Amount must be positive.")
                continue
            break
        except ValueError:
            print(" Enter a valid number.")

    #date
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
            print(" error. Use format YYYY-MM-DD. Example: 2026-06-07")

    #Note
    note = input("Note (optional): ").strip()

    #The Transaction Dictionary

    transaction = {
        "type": t_type,
        "category": category,
        "amount": amount,
        "date": t_date,
        "note": note
    }

    #Append added transaction to the list
    transactions.append(transaction)
    print(f" Transaction added! Total records: {len(transactions)}")

def view_transactions(transactions):
    print("\n--- All Transactions ---")

    # Guard Clause
    if not transactions:
        print(" No Transactions found.")
        return

    #Header row
    print(f"{'#':<4} {'Date':<12} {'Type':<9} {'Category':<10} {'Amount':>10}  {'Note':>10}")
    print("-" * 70)

    # Data rows
    for i, txn in enumerate(transactions, start=1):
        print(
            f"{i:<4} "
            f"{txn['date']:<12} "
            f"{txn['type']:<9} "
            f"{txn['category']:<10} "
            f"₹{txn['amount']:>12,.2f}  "
            f"{txn['note']:<10}"
        )
"""
add_transaction(transactions)
view_transactions(transactions)
"""
def filter_transactions(transactions, filters):
    """
    filters is a dict with any of these optional keys:
      "type"       : "income" or "expense"
      "category"   : e.g. "food"
      "start_date" : "YYYY-MM-DD"
      "end_date"   : "YYYY-MM-DD"
    """
    result = transactions       #starts with everything

    #Filter 1: by type
    if "type" in filters:
        result = [
            txn for txn in result
            if txn ["type"] == filters["type"]
        ]

    #Filter 2: by category
    if "category" in filters:
        result = [
            txn for txn in result
            if txn["category"] == filters["category"]
        ]

    # filter 3: By date range
    if "start_date" in filters or "end_date" in filters:
        start = datetime.strptime(
            filters.get("start_date", "2000-01-01"), '%Y-%m-%d')
        end = datetime.strptime(
            filters.get("end_date", "2999-12-31"), '%Y-%m-%d'
        )
        result = [
            txn for txn in result
            if start <= datetime.strptime(txn["date"], "%Y-%m-%d") <= end
        ]

    # Result
    if not result:
        print("No transactions match your criteria.")
        return[]

    print(f"\n Found {len(result)} matching transaction(s).")
    view_transactions(result)  #reuse display function!
    return result

def search_menu(transactions):
    """Interactive menu that builds the filters dict and calls filter_transactions."""
    print("\n--- Filter / Search ---")
    print("Leave blank to skip any filter.\n")

    filters = {}

    t = input("Filter by type (income/expense): ").strip().lower()
    if t in VALID_TYPES:
        filters["type"] = t

    c = input(f"Filter by category {VALID_CATEGORIES}: ").strip().lower()
    if c in VALID_CATEGORIES:
        filters["category"] = c

    sd = input("Start date (YYYY-MM-DD): ").strip()
    if sd:
        filters["start_date"] = sd

    ed = input("End date (YYYY-MM-DD): ").strip()
    if ed:
        filters["end_date"] = ed

    filter_transactions(transactions, filters)
"""
add_transaction(transactions)
add_transaction(transactions)
add_transaction(transactions)
filter_transactions(transactions, {"category": "shopping"})
"""

def calculate_summary(transactions):
    print("\n--- Summary Report ---")

    if not transactions:
        print(" No transactions to summarise.")
        return

    #Step 1: Separate income and expense totals
    total_income = sum(
        txn["amount"] for txn in transactions
        if txn["type"] == "income"
    )
    total_expense = sum(
        txn["amount"] for txn in transactions
        if txn["type"] == "expense"
    )

    #Step 2: Net Savings
    net_savings = total_income - total_expense

    #Step 3: Print the P&L
    print(f" Total Income:  ₹{total_income:>12,.2f}")
    print(f" Total Expense : ₹{total_expense:>12,.2f}")
    print(f" {'-' * 28}")
    print(f" Net Savings: ₹{net_savings:>12,.2f}")

    #Step 4: Colour-code savings
    if net_savings < 0:
        print(f" ⚠ Warning: You are ₹{abs(net_savings):,.2f} over your income!")
    elif net_savings == 0:
        print(" Breaking even.")
    else:
        print(f" Saving ₹{net_savings:,.2f} ({(net_savings / total_income) * 100:,.2f}% of income)")

    return total_income, total_expense, net_savings

def category_report(transactions):
    print("\n--- Category Report ---")





    if not transactions:
        print(" No transactions to report.")
        return

    #Step 1: Accumulate spend per category
    category_totals = {}
    for txn in transactions:
        if txn["type"] == "expense":
            cat = txn["category"]
            if cat not in category_totals:
                category_totals[cat] = 0
            category_totals[cat] += txn["amount"]

    if not category_totals:
        print(" No expense transactions found.")

    #step 2: Sort by highest spend
    sorted_cats = sorted(
        category_totals.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    #Step 3: Print ranked breakdown
    print(f" {'Category':<12} {'Spent':>12}")
    print(f" {'-' * 26}")
    for rank, (cat, total) in enumerate(sorted_cats, start=1):
        print(f" {rank}. {cat:10} ₹{total:>10,.2f}")

    #Step 4: Highest Expense category
    top_cat, top_amt = sorted_cats[0]
    print(f"\n ▶Highest Spend Category: {top_cat.title()} at ₹{top_amt:,.2f}")


    #Step 5: Monthly breakdown
    print("\n  --- Monthly Summary ---")
    monthly_total = {}
    for txn in transactions:
        month = txn ["date"][:7]
        if month not in monthly_total:
            monthly_total[month] = {"income": 0, "expense": 0}
        monthly_total[month][txn["type"]] += txn["amount"]

    print(f" {'Month':<10} {'Income':>12} {'Expense':>12} {'Net':>12}")
    print(f" {'-' * 48}")
    for month in sorted(monthly_total):
        inc = monthly_total[month]["income"]
        exp = monthly_total[month]["expense"]
        net = inc - exp
        print(f" {month:<10} ₹{inc:>10,.2f} ₹{exp:>10,.2f} ₹{net:>10,.2f}")

def set_budget(budgets):
    print("\n--- Set Category Budget ---")
    print(f"Valid categories: {', '.join(VALID_CATEGORIES)}")
    print("Enter 'done' when finished.\n")

    while True:
        #Step 1: Ask for category
        cat = input("Category (or 'done'): ").strip().lower()
        if cat == "done":
            break
        if cat not in VALID_CATEGORIES:
            print(f" Invalid category.")
            continue

        #Step 2: Ask for budget amount
        try:
            limit = float(input(f"Monthly budget for '{cat}' (₹): "))
            if limit <= 0:
                print("Budget cannot be negative.")
                continue
        except ValueError:
            print(" Enter a valid number.")
            continue

        # Step 3: Store in budgets dict
        budgets[cat] = limit
        print(f" Budget set: {cat} → ₹{limit:,.2f} ")

    print(f"\n Active budgets: {len(budgets)} categor{'y' if len(budgets)==1 else 'ies'}")
    return budgets

def check_budget(transactions, budgets):
    print("\n--- Budget Status ---")

    #Guard: no budgets set yet
    if not budgets:
        print(" No budgets set. Use option 5 to set budgets.")
        return

    #Step 1: Compute actual spend per category
    # (same accumulation pattern as Stage 4)
    actual = {}
    for txn in transactions:
        if txn["type"] == "expense":
            cat = txn["category"]
            if cat not in actual:
                actual[cat] = 0
            actual[cat] += txn["amount"]

    #Step 2: Print header
    print(f" {'Category':<12} {'Budget':>10} {'Spent':>12} {'Remaining':>12} Status")
    print(f" {'-' * 58}")

    #Step 3: Compare budget vs actual, row by row
    alerts = []
    for cat, limit in budgets.items():
        spent = actual.get(cat, 0)
        remaining = limit - spent
        pct = (spent / limit) * 100

        #Determine status
        if spent > limit:
            status = "⚠ OVER"
            alerts.append((cat, spent, limit, spent - limit))
        elif pct >= 85:
            status = "◈ NEAR LIMIT"
        else:
            status = "✓ OK"

        print(
            f"  {cat:<12} "
            f"₹{limit:>8,.0f} "
            f"₹{spent:>8,.0f} "
            f"₹{remaining:>8,.0f}  "
            f"{status}"
        )

    #Step 4: Print consolidated alerts at the bottom
    if alerts:
        print(f"\n {'─' * 40}")
        print(" ⚠  BUDGET ALERTS")
        print(f" {'-' * 40}")
        for cat, spent, limit, overby in alerts:
            print(
                f" {cat.title()}: over budget by ₹{overby:,.2f} "
                f"(spent in ₹{spent:,.2f}  vs limit ₹{limit:,.2f})"
            )
def show_menu():
    print("\n====Smart Expense Tracker====")

    menu_options = [
        "1. Add Transactions",
        "2. View All Transactions",
        "3. Filter / Search",
        "4. Summary Report",
        "5. Category Report",
        "6. Set Category Budget",
        "7. Check Budget Status",
        "8. Exit"
    ]

    for options in menu_options:
        print(options)

def main():
    #Startup: Load persisted data
    global transactions, budgets
    transactions, budgets = load_data()

    #Main event loop
    while True:
        show_menu()

    #Get User choice
        choice = input(" Choose an option (1 to 8): ").strip()
        if choice == "1": add_transaction(transactions)
        elif choice == "2": view_transactions(transactions)
        elif choice == "3": search_menu(transactions)
        elif choice == "4": calculate_summary(transactions)
        elif choice == "5": category_report(transactions)
        elif choice == "6": set_budget(budgets)
        elif choice == "7": check_budget(transactions, budgets)
        elif choice == "8":
            save_data(transactions, budgets)
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice. Enter number from 1 to 8.")

if __name__ == "__main__":
    main()



