import json
import os
import datetime

DATA_FILES = [
    "users.json",
    "accounts.json",
    "transactions.json",
    "categories.json",
    "budgets.json",
    "saving_goals.json"
]

def ensure_data_files():
    data_path = os.path.join(os.getcwd(), "data")
    os.makedirs(data_path, exist_ok=True)

    for filename in DATA_FILES:
        path = os.path.join(data_path, filename)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, "w") as f:
                json.dump([], f, indent=4)

def parse_date(value):
    if not value.strip():
        return datetime.date.today()
    return datetime.date.fromisoformat(value.strip())

def money(value):
    return f"EGP {value:,.2f}"

def month_name(month):
    return datetime.date(2000, month, 1).strftime("%B")
