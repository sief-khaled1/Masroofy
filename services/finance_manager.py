from models.budget import Budget
from models.user import User
from models.account import Account,BankAccount,WalletAccount,CashAccount
from models.transaction import Income,Expense,Transfer
from models.category import Category
class FinanceManager:
    def add_income(self,user : User, amount,source,account:Account,date):
        if amount <= 0:
            return "Income amount must be positive."
        income = Income(transaction_id=len(user.transactions) + 1, user_id=user.user_id, amount=amount, date=date, destination_account=account, source=source)
        income.execute()
        user.transactions.append(income)
        return "Income added successfully."
    
    def add_expense(self,user:User,amount,account:Account,category:Category,date):
        if amount <= 0:
            return "Expense amount must be positive."
        expense = Expense(transaction_id=len(user.transactions) + 1,user_id=user.user_id,amount=amount,date=date,source_account=account,category=category)
        expense.execute()
        user.transactions.append(expense)
        return "Expense added successfully."
    
    def transfer(self,user:User,amount,source:Account,destination:Account,date):
        if amount <= 0:
            return "Transfer amount must be positive."
        transfer=Transfer(transaction_id=len(user.transactions) + 1, user_id=user.user_id, amount=amount, date=date, source_account=source, destination_account=destination)
        transfer.execute()
        user.transactions.append(transfer)
        return "Transfer added successfully."
    
    def create_account(self,user:User,account_type,opening_balance):
        if opening_balance < 0:
            return "Opening balance cannot be negative."
        if account_type.lower() == "bank":
            account = BankAccount(account_id=len(user.accounts) + 1, user_id=user.user_id, opening_balance=opening_balance,bank_name="Bank")
        elif account_type.lower() == "cash":
            account = CashAccount(account_id=len(user.accounts) + 1, user_id=user.user_id, opening_balance=opening_balance)
        elif account_type.lower() == "wallet":
            account = WalletAccount(account_id=len(user.accounts) + 1, user_id=user.user_id, opening_balance=opening_balance, provider_name="Wallet")   
        else:
            return "Invalid account type."
        user.accounts.append(account)
        return "Account created successfully."
    
    def deactivate_account(self,account:Account):
        if not account.is_active:
            return "Account is already inactive."
        account.deactivate()
        return "Account deactivated successfully."
    
    def create_budget(user:User,amount,month,year,category:Category):
        if amount <= 0:
            return "Budget amount must be positive."
        budget = Budget(budget_id=len(user.budgets) + 1, user_id=user.user_id, amount=amount, month=month, year=year, category=category)
        user.budgets.append(budget)
        return "Budget created successfully."
    
    def update_budget(self,budget:Budget,amount):
        if amount <= 0:
            return "Budget amount must be positive."
        budget.amount = amount
        return "Budget updated successfully."
    
    def create_savings_goal(user:User,year,target,amount):
        if amount <= 0:
            return "Savings goal amount must be positive."
        goal = SavingsGoal(goal_id=len(user.savings_goals) + 1, user_id=user.user_id, year=year,target_amount=amount,monthly_target=target)
        user.savings_goals.append(goal)
        return "Savings goal created successfully."
    
    def add_to_savings_plan(self,goal:SavingsGoal,month,amount):
        if amount <= 0:
            return "Savings plan amount must be positive."
        goal.amount += amount
        return "Amount added to savings plan successfully."
    
    