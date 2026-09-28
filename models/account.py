from abc import ABC, abstractmethod
class InsufficientBalanceError(Exception):
    pass

class Account(ABC):
    def __init__(self, account_id, opening_balance, user_id, is_active=True):
        self.__account_id = account_id
        if opening_balance >= 0:
            self.__balance = opening_balance
        else:
            raise ValueError("The opening balance cannot be negative")
        self.__user_id = user_id
        self.__is_active = is_active

    @property
    def balance(self):
        return self.__balance

    @property
    def account_id(self):
        return self.__account_id

    @property
    def is_active(self):
        return self.__is_active

    def deactivate(self):
        if self.__balance != 0:
            raise ValueError("Account with balance cannot be deactivated")
        self.__is_active = False

    def activate(self):
        self.__is_active = True

    def can_withdraw(self, amount):
        return 0 < amount <= self.__balance

    def withdraw(self, amount):
        if not self.__is_active:
            raise ValueError("Inactive account cannot be used")
        if amount <= 0:
            raise ValueError("The amount must be greater than 0")
        if self.can_withdraw(amount):
            self.__balance -= amount
        else:
            raise InsufficientBalanceError("Insufficient funds")
        return self.__balance

    def deposit(self, amount):
        if not self.__is_active:
            raise ValueError("Inactive account cannot be used")
        if amount <= 0:
            raise ValueError("The amount must be greater than 0")
        self.__balance += amount
        return self.__balance

    @abstractmethod
    def get_display_name(self):
        pass

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'balance': self.balance,
            'user_id': self.__user_id,
            'is_active': self.__is_active,
        }

    @classmethod
    def from_dict(cls, data):
        account_type = data["type"].casefold()
        if account_type == "cash":
            return CashAccount(data["account_id"], data["balance"], data["user_id"], data["is_active"])
        elif account_type == "bank":
            return BankAccount(data["account_id"], data["balance"], data["user_id"], data["bank_name"], data["is_active"])
        elif account_type == "wallet":
            return WalletAccount(data["account_id"], data["balance"], data["user_id"], data["provider_name"], data["is_active"])
        else:
            raise ValueError("Invalid account type")

class CashAccount(Account):
    def get_display_name(self):
        return "Cash"

    def to_dict(self):
        data = super().to_dict()
        data['type'] = self.get_display_name()
        return data


class BankAccount(Account):
    def __init__(self, account_id, opening_balance, user_id, bank_name, is_active=True):
        super().__init__(account_id, opening_balance, user_id, is_active)
        if bank_name.strip() == "":
            raise ValueError("Bank name cannot be empty")
        self.__bank_name = bank_name

    @property
    def bank_name(self):
        return self.__bank_name

    def get_display_name(self):
        return f"Bank - {self.bank_name}"

    def to_dict(self):
        data = super().to_dict()
        data['type'] = "Bank"
        data['bank_name'] = self.bank_name
        return data

class WalletAccount(Account):
    def __init__(self, account_id, opening_balance, user_id, provider_name, is_active=True):
        super().__init__(account_id, opening_balance, user_id, is_active)
        if provider_name.strip() == "":
            raise ValueError("Provider name cannot be empty")
        self.__provider_name = provider_name

    @property
    def provider_name(self):
        return self.__provider_name

    def get_display_name(self):
        return f"Wallet - {self.provider_name}"

    def to_dict(self):
        data = super().to_dict()
        data['type'] = "Wallet"
        data['provider_name'] = self.provider_name
        return data