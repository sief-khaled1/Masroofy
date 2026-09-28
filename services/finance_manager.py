from models.budget import Budget
from models.user import User
from models.account import Account,BankAccount,WalletAccount,CashAccount
from models.transaction import Income,Expense,Transfer
from models.category import Category
from services.file_manager import FileManager
from models.saving_goal import SavingGoal
import os

class FinanceManager:
    @staticmethod
    def save_user_data( filename, user_id, items):
        path = os.path.join(os.getcwd(), "data", filename)
        data = FileManager().load(path)
        data = [item for item in data if item.get("user_id") != user_id]
        data.extend([item.to_dict() for item in items])
        FileManager().save(path, data)

    @staticmethod
    def generate_id(items, id_attribute):
        return max((getattr(item, id_attribute) for item in items), default=0) + 1

    def add_income(self, user : User, amount,source,account:Account,date):
        if amount <= 0:
            return "Income amount must be positive."
        income = Income(transaction_id=len(user.transactions) + 1, user_id=user.user_id, amount=amount, date=date, destination_account=account, source=source)
        income.execute()
        user.transactions.append(income)
        self.save_user_data("transactions.json", user.user_id, user.transactions)
        return "Income added successfully."

    def add_expense(self, user:User,amount,account:Account,category:Category,date):
        if amount <= 0:
            return "Expense amount must be positive."
        expense = Expense(transaction_id=len(user.transactions) + 1,user_id=user.user_id,amount=amount,date=date,source_account=account,category=category)
        expense.execute()
        user.transactions.append(expense)
        self.save_user_data("transactions.json", user.user_id, user.transactions)
        return "Expense added successfully."

    def transfer(self, user:User,amount,source:Account,destination:Account,date):
        if amount <= 0:
            return "Transfer amount must be positive."
        transfer=Transfer(transaction_id=self.generate_id(user.transactions, "transaction_id"), user_id=user.user_id, amount=amount, date=date, source_account=source, destination_account=destination)
        transfer.execute()
        user.transactions.append(transfer)
        self.save_user_data("transactions.json", user.user_id, user.transactions)
        return "Transfer added successfully."

    def create_account(self, user:User,account_type,opening_balance):
        if opening_balance < 0:
            return "Opening balance cannot be negative."
        if account_type.lower() == "bank":
            account = BankAccount(account_id=self.generate_id(user.accounts, "account_id"), user_id=user.user_id, opening_balance=opening_balance,bank_name="Bank")
        elif account_type.lower() == "cash":
            account = CashAccount(account_id=self.generate_id(user.accounts, "account_id"), user_id=user.user_id, opening_balance=opening_balance)
        elif account_type.lower() == "wallet":
            account = WalletAccount(account_id=self.generate_id(user.accounts, "account_id"), user_id=user.user_id, opening_balance=opening_balance, provider_name="Wallet")
        else:
            return "Invalid account type."
        user.accounts.append(account)
        self.save_user_data("accounts.json", user.user_id, user.accounts)
        return "Account created successfully."
    
    def create_category(self, user:User, name):
        if not name.strip():
            return "Category name cannot be empty."
        if any(category.name.casefold() == name.strip().casefold() for category in user.categories):
            return "Category already exists."
        category = Category(category_id=self._generate_id(user.categories, "category_id"), user_id=user.user_id, name=name.strip())
        user.categories.append(category)
        self._save_user_data("categories.json", user.user_id, user.categories)
        return "Category created successfully."

    def deactivate_account(self, account:Account, user:User):
        if not account.is_active:
            return "Account is already inactive."
        account.deactivate()
        self.save_user_data("accounts.json", user.user_id, user.accounts)
        return "Account deactivated successfully."

    def create_budget(self, user:User,amount,month,year,category:Category):
        if amount <= 0:
            return "Budget amount must be positive."
        for budget in user.budgets:
            if budget.month == month and budget.year == year:
                if not budget.is_overall() and category is not None and budget.category.category_id == category.category_id:
                    return "Budget already exists for this category."
        budget = Budget(budget_id=self.generate_id(user.budgets, "budget_id"), user_id=user.user_id, amount=amount, month=month, year=year, category=category)
        user.budgets.append(budget)
        self.save_user_data("budgets.json", user.user_id, user.budgets)
        return "Budget created successfully."

    def update_budget(self, budget:Budget,amount,user:User):
        if amount <= 0:
            return "Budget amount must be positive."
        budget.update_amount(amount)
        self.save_user_data("budgets.json", user.user_id, user.budgets)
        return "Budget updated successfully."

    def create_savings_goal(self, user: User, year, amount):
        if amount <= 0:
            return "Savings goal amount must be positive."
        goal = SavingGoal(goal_id=self.generate_id(user.savings_goals, "goal_id"), user_id=user.user_id, year=year, target_amount=amount)
        user.savings_goals.append(goal)
        self.save_user_data("saving_goals.json", user.user_id, user.savings_goals)
        return "Savings goal created successfully."

    def add_to_savings_plan(self, user: User, goal: SavingGoal, month, amount):
        if amount <= 0:
            return "Savings plan amount must be positive."
        goal.add_monthly_target(month, amount)
        self.save_user_data("saving_goals.json", user.user_id, user.savings_goals)
        return "Amount added to savings plan successfully."

    def delete_budget(self, user: User, budget_id):
        for budget in user.budgets:
            if budget.budget_id == budget_id:
                user.budgets.remove(budget)
                self.save_user_data("budgets.json", user.user_id, user.budgets)
                return
        raise ValueError("Budget not found")

    def delete_saving_goal(self, user: User, goal_id):
        for goal in user.savings_goals:
            if goal.goal_id == goal_id:
                user.savings_goals.remove(goal)
                self.save_user_data("saving_goals.json", user.user_id, user.savings_goals)
                return
        raise ValueError("Saving goal not found")