class Budget:
    def __init__(self, budget_id, user_id, amount, month, year, category=None):
        self.__budget_id = budget_id
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__user_id = user_id
        self.__amount = amount
        if 1 <= month <= 12:
            self.__month = month
        else:
            raise ValueError("Month must be in range [1,12]")
        self.__year = year
        self.__category = category

    @property
    def budget_id(self):
        return self.__budget_id

    @property
    def month(self):
        return self.__month

    @property
    def year(self):
        return self.__year

    @property
    def category_name(self):
        return self.__category.name if self.__category is not None else None

    @property
    def category(self):
        return self.__category

    @property
    def amount(self):
        return self.__amount

    @property
    def user_id(self):
        return self.__user_id

    def is_overall(self):
        return self.__category is None

    def update_amount(self, new_amount):
        if new_amount <= 0:
            raise ValueError("Amount must be positive")
        self.__amount = new_amount

    def to_dict(self):
        return {
            "budget_id": self.__budget_id,
            "user_id": self.__user_id,
            "amount": self.__amount,
            "month": self.__month,
            "year": self.__year,
            "category_id": self.__category.category_id if self.__category is not None else None
        }

    @classmethod
    def from_dict(cls, data, category=None):
        return cls(data["budget_id"], data["user_id"], data["amount"], data["month"], data["year"], category)