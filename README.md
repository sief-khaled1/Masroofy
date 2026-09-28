# Masroufy

**Masroufy** is a desktop personal finance and saving management application built with Python using Object-Oriented Programming principles.

The system helps users manage their money across cash, bank, and wallet accounts, record financial transactions, create budgets, track saving goals, and view financial analytics through a graphical desktop interface.

## Features

- User registration and login
- Separate financial data for each user
- Cash, bank, and wallet accounts
- Income, expense, and transfer transactions
- Expense categories with custom category support
- Monthly overall and category budgets
- Annual saving goals with monthly saving targets
- Total balance calculation
- Monthly income and expense analysis
- Net saving calculation
- Budget usage and remaining amount tracking
- Saving progress, shortfall, and surplus analysis
- JSON-based data persistence
- Desktop GUI built with CustomTkinter
- Dashboard charts using Matplotlib

## Project Structure

```text
Masroofy/
│
├── data/
│   ├── users.json
│   ├── accounts.json
│   ├── transactions.json
│   ├── categories.json
│   ├── budgets.json
│   └── saving_goals.json
│
├── models/
│   ├── account.py
│   ├── budget.py
│   ├── category.py
│   ├── saving_goal.py
│   ├── transaction.py
│   └── user.py
│
├── services/
│   ├── auth_manager.py
│   ├── file_manager.py
│   ├── finance_analyzer.py
│   ├── finance_manager.py
│   └── user_data_loader.py
│
├── gui/
│   ├── pages/
│   ├── app.py
│   ├── components.py
│   ├── main_layout.py
│   ├── theme.py
│   └── utils.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Main OOP Design

### Account Hierarchy

`Account` is an abstract base class.

Concrete account types:

- `CashAccount`
- `BankAccount`
- `WalletAccount`

The account hierarchy is responsible for balance protection, deposits, withdrawals, activation status, and account-specific display information.

### Transaction Hierarchy

`Transaction` is an abstract base class.

Concrete transaction types:

- `Income`
- `Expense`
- `Transfer`

Each transaction type implements its own `execute()` behavior.

### Other Domain Classes

- `User`
- `Category`
- `Budget`
- `SavingGoal`

## Service Classes

### AuthManager

Handles:

- Registration
- Login
- Password changes

### FinanceManager

Coordinates state-changing financial operations such as:

- Adding income
- Adding expenses
- Transfers
- Creating accounts
- Creating categories
- Creating and updating budgets
- Creating saving goals
- Updating monthly saving plans
- Saving updated user data

### FinanceAnalyzer

Provides read-only financial calculations such as:

- Total balance
- Monthly income
- Monthly expenses
- Net saving
- Category spending

### BudgetAnalyzer

Provides:

- Budget spending
- Remaining budget
- Usage percentage
- Budget exceeded status

### SavingAnalyzer

Provides:

- Saved amount
- Saving progress
- Monthly shortfall
- Monthly surplus
- Required saving calculations

### FileManager

Handles JSON file reading and writing.

### UserDataLoader

Loads saved data and rebuilds relationships between users, accounts, categories, transactions, budgets, and saving goals.

## OOP Concepts Used

The project demonstrates:

- **Encapsulation** — account balance is protected and modified through controlled methods.
- **Abstraction** — `Account` and `Transaction` are abstract base classes.
- **Inheritance** — specialized accounts and transactions inherit from their base classes.
- **Polymorphism** — methods such as `execute()` and `get_display_name()` behave differently depending on the concrete object.
- **Composition / Association** — users are associated with accounts, transactions, categories, budgets, and saving goals.
- **Exception Handling** — invalid amounts, insufficient balances, invalid dates, and other invalid operations are handled safely.
- **Separation of Concerns** — models, services, persistence, analytics, and GUI responsibilities are separated.

## Persistence

Masroufy uses JSON files for data persistence.

Objects are converted to dictionaries using `to_dict()` before saving and reconstructed using `from_dict()` when loading.

Related records are connected using IDs such as:

- `user_id`
- `account_id`
- `category_id`
- `budget_id`
- `goal_id`
- `transaction_id`

## GUI

The desktop interface is built using **CustomTkinter**.

The interface includes:

- Login and registration
- Dashboard
- Accounts
- Transactions
- Budgets
- Saving goals
- Categories

The dashboard uses **Matplotlib** for financial charts.

## Installation

Make sure Python is installed, then install the project dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

From the project root directory:

```bash
python main.py
```

## Requirements

Main external libraries:

- `customtkinter`
- `matplotlib`

## Business Rules

- Opening balance cannot be negative.
- Transaction amounts must be positive.
- Account balances cannot become negative.
- Inactive accounts cannot be used for deposits or withdrawals.
- Future-dated transactions are not allowed.
- Transfer source and destination accounts must be different.
- Transfers do not count as income or expenses.
- Budget amounts must be positive.
- Only one overall budget is allowed for the same month and year.
- Duplicate category budgets for the same category and month are not allowed.
- Saving targets must be positive.
- Financial calculations are derived from stored transactions rather than duplicated as separate state.

## Technologies

- Python
- Object-Oriented Programming
- CustomTkinter
- Matplotlib
- JSON
- Git / GitHub

## Project Goal

The main goal of Masroufy is to demonstrate a complete and usable Object-Oriented Programming application that combines domain modeling, inheritance, abstraction, polymorphism, file persistence, business rules, analytics, and a desktop GUI.
