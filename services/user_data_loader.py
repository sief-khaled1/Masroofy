import os
from services.file_manager import FileManager
from models.account import Account
from models.transaction import Transaction
from models.category import Category
from models.budget import Budget
from models.saving_goal import SavingGoal

class UserDataLoader:
    def __init__(self):
        self.file_manager = FileManager()
        self.base_path = os.path.join(os.getcwd(), "data")

    def load_user_data(self, user):
        accounts_data = self.file_manager.load(os.path.join(self.base_path, "accounts.json"))
        categories_data = self.file_manager.load(os.path.join(self.base_path, "categories.json"))
        transactions_data = self.file_manager.load(os.path.join(self.base_path, "transactions.json"))
        budgets_data = self.file_manager.load(os.path.join(self.base_path, "budgets.json"))
        goals_data = self.file_manager.load(os.path.join(self.base_path, "saving_goals.json"))

        accounts = [Account.from_dict(data) for data in accounts_data if data["user_id"] == user.user_id]
        categories = [Category.from_dict(data) for data in categories_data if data["user_id"] == user.user_id]
        accounts_by_id = {account.account_id: account for account in accounts}
        categories_by_id = {category.category_id: category for category in categories}
        transactions = [Transaction.from_dict(data, accounts_by_id, categories_by_id) for data in transactions_data if data["user_id"] == user.user_id]
        budgets = [Budget.from_dict(data, categories_by_id.get(data["category_id"])) for data in budgets_data if data["user_id"] == user.user_id]
        savings_goals = [SavingGoal.from_dict(data) for data in goals_data if data["user_id"] == user.user_id]
        user.load_data(accounts, transactions, categories, budgets, savings_goals)