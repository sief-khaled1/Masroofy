import datetime
from abc import ABC, abstractmethod
from models.account import Account
from models.category import Category


class Transaction(ABC):
    def __init__(self, transaction_id, user_id, amount, date):
        self.transaction_id = transaction_id
        self.user_id = user_id
        if amount <= 0:
            raise ValueError("Transaction amount must be positive")
        self.amount = amount
        if date > datetime.date.today():
            raise ValueError("Transaction date cannot be in the future")
        self.date = date

    @abstractmethod
    def execute(self):
        pass

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "date": self.date.isoformat()
        }

    @staticmethod
    def from_dict(data, accounts_by_id, categories_by_id):
        transaction_type = data.get("type")

        if transaction_type == "income":
            return Income.from_dict(data, accounts_by_id)

        elif transaction_type == "expense":
            return Expense.from_dict(data, accounts_by_id, categories_by_id)

        elif transaction_type == "transfer":
            return Transfer.from_dict(data, accounts_by_id, categories_by_id)

        else:
            raise ValueError("Invalid transaction type")


class Income(Transaction):
    def __init__(self, transaction_id, user_id, amount, date, destination_account: Account, source):
        super().__init__(transaction_id, user_id, amount, date)
        self.destination_account = destination_account
        self.source = source

    def execute(self):
        self.destination_account.deposit(self.amount)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "income",
             "destination_account_id": self.destination_account.account_id,
             "source": self.source
        })
        return data

    @staticmethod
    def from_dict(data, accounts_by_id, categories_by_id):
        destination_account = accounts_by_id.get(data.get("destination_account_id"))
        if destination_account is None:
            raise ValueError("Destination account not found")
        return Income(
            transaction_id=data.get("transaction_id"),
            user_id=data.get("user_id"), amount=data.get("amount"),
            date=datetime.date.fromisoformat(data.get("date")),
            destination_account=destination_account,
            source=data.get("source")
        )


class Expense(Transaction):
    def __init__(self, transaction_id, user_id, amount, date, source_account: Account, category: Category):
        super().__init__(transaction_id, user_id, amount, date)
        self.source_account = source_account
        self.category = category

    def execute(self):
        self.source_account.withdraw(self.amount)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "expense",
            "source_account_id": self.source_account.account_id,
            "category_id": self.category.category_id})
        return data

    @staticmethod
    def from_dict(data, accounts_by_id, categories_by_id):
        source_account = accounts_by_id.get(data.get("source_account_id"))
        category = categories_by_id.get(data.get("category_id"))
        if source_account is None:
            raise ValueError("Source account not found")
        if category is None:
            raise ValueError("Category not found")
        return Expense(
            transaction_id=data.get("transaction_id"),
            user_id=data.get("user_id"),
            amount=data.get("amount"),
            date=datetime.date.fromisoformat(data.get("date")),
            source_account=source_account, category=category
        )


class Transfer(Transaction):
    def __init__(self, transaction_id, user_id, amount, date, source_account: Account, destination_account: Account):
        super().__init__(transaction_id, user_id, amount, date)
        if source_account.account_id == destination_account.account_id:
            raise ValueError("Source and destination accounts cannot be the same")
        self.source_account = source_account
        self.destination_account = destination_account

    def execute(self):
        self.source_account.withdraw(self.amount)
        self.destination_account.deposit(self.amount)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "transfer",
            "source_account_id": self.source_account.account_id,
            "destination_account_id": self.destination_account.account_id
        })
        return data

    @staticmethod
    def from_dict(data, accounts_by_id, categories_by_id):
        source_account = accounts_by_id.get(data.get("source_account_id"))
        destination_account = accounts_by_id.get(data.get("destination_account_id"))
        if source_account is None or destination_account is None:
            raise ValueError("Account not found")
        return Transfer(
            transaction_id=data.get("transaction_id"),
            user_id=data.get("user_id"),
            amount=data.get("amount"),
            date=datetime.date.fromisoformat(data.get("date")),
            source_account=source_account, destination_account=destination_account
        )