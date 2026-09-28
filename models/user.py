class User:
    def __init__(self,user_id,name,email,password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.transactions = []
        self.accounts = []
        self.savings_goals = []
        self.categories = []
        self.budgets = []

    def load_data(self, accounts, transactions, categories, budgets, savings_goals):
        self.accounts = accounts
        self.transactions = transactions
        self.categories = categories
        self.budgets = budgets
        self.savings_goals = savings_goals
    
    def update_name(self,name):
        if name:
            self.name = name
            return True
        return False
      
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password")
        )