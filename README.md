#Smart Personal Expense Tracker A menu-driven console application to track personal income and expenses, built in Python as a self-study project for data analytics skill development.
## Features:-
1. Add income/expense transactions with full input validation
2. View all transactions in a clean, aligned console table
3. Filter/search by type, category, or date range (combinable)
4. Summary report — total income, expenses, net savings, savings % 
5. Category-wise spend breakdown, ranked by highest spend
6. Monthly P&L summary (YYYY-MM grouping)
7. Per-category budget setting with 3-state alerts (OK / Near Limit / Over)
8. JSON persistence — data survives app restarts
## How to run ```bash # No external libraries needed — pure Python 3 python Exp_Tracker.py ``` 
## Menu options | Option | Function |
1. | Add a transaction | 
2. | View all transactions | 
3. | Filter / Search | 
4. | Summary report | 
5. | Category report | 
6. | Set category budget | 
7. | Check budget status | 
8. | Save & Exit | 
## Python concepts demonstrated - Data structures: list of dicts, nested dicts, tuple unpacking - Input validation: whitelist checks, try/except, optional-with-default - List comprehensions and generator expressions - Dictionary accumulation pattern - Sorting with lambda key functions - f-string column alignment and number formatting - File I/O with JSON, context managers, corruption recovery - Event loop pattern (while True + dispatcher + break)
## Project context - Built as Top Mentor DA/DS project, targeting a transition into Finance Data Analyst / FP&A roles. ## Author Akshay Kumar — Senior Accountant transitioning into Finance Data Analytics.
