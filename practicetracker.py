import json
import os
from datetime import datetime, date


DATA_FILE = "tracker.json"

VALID_TYPE = ["income", "expense"]

VALID_CATEGORY = ["food", "travel", "rent", "salary", "shopping", "health", "other"]

transactions = []

budgets = {}

#transaction

transaction_1 = {
    "type": "expense",
    "category": "shopping",
    "date": "2026-03-02",
    "amount": "20000",
    "note": "groceries for the month",
}

transaction_2 = {
    "type": "income",
    "category": "salary",
    "date": "2026-02-28",
    "amount": "200000",
    "note": "salary credited",
}


