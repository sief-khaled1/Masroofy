from models.user import User
from models.account import Account,BankAccount,WalletAccount,CashAccount
from models.transaction import Income,Expense,Transfer
from models.category import Category
class FinanceManager:
    def add_income(self,user : User,amount : Account,source,account,date):
        if amount <= 0:
            return "Income amount must be positive."
        income = Income(transaction_id=len(user.transactions) + 1, user_id=user.user_id, amount=amount, date=date, destination_account=account, source=source)
        income.execute()
        user.transactions.append(income)
        return "Income added successfully."
    
    def add_expense(self,user:User,amount:Account,category:Category,date):
        if amount <= 0:
            return "Expense amount must be positive."
        expense = Expense(transaction_id=len(user.transactions) + 1, user_id=user.user_id, amount=amount, date=date, category=category)
        expense.execute()
        user.transactions.append(expense)
        return "Expense added successfully."
    
    def transfer(self,user:User,amount,source:Account,destination:Account,date):
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
        pass
    
    def update_budget(self,budget:Budget,amount):
        pass
    
    def create_savings_goal(user:User,year,target,amount):
        pass
    
    def add_to_savings_plan(self,goal:SavingsGoal,month,amount):
        pass
    
    
    