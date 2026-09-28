class SavingGoal:
    def __init__(self, goal_id, user_id, year, target_amount, monthly_targets=None):
        self.__goal_id = goal_id
        self.__user_id = user_id
        self.__year = year
        if target_amount <= 0:
            raise ValueError("Target amount must be positive")
        self.__target_amount = target_amount
        self.__monthly_targets = monthly_targets if monthly_targets is not None else {}

    @property
    def goal_id(self):
        return self.__goal_id
    @property
    def user_id(self):
        return self.__user_id
    @property
    def target_amount(self):
        return self.__target_amount
    @property
    def monthly_targets(self):
        return self.__monthly_targets
    @property
    def year(self):
        return self.__year

    def add_monthly_target(self, month, amount):
        if amount <= 0:
            raise ValueError("Target amount must be positive")
        if 1 <= month <= 12:
            self.__monthly_targets[month] = amount
        else:
            raise ValueError("Month must be between 1 and 12")

    def update_target_amount(self, new_amount):
        if new_amount <= 0:
            raise ValueError("Target amount must be positive")
        self.__target_amount = new_amount

    def to_dict(self):
        return {
            "goal_id": self.goal_id,
            "user_id": self.user_id,
            "year": self.year,
            "target_amount": self.target_amount,
            "monthly_targets": self.monthly_targets
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["goal_id"], data["user_id"], data["year"], data["target_amount"], {int(month): float(amount) for month, amount in data["monthly_targets"].items()})