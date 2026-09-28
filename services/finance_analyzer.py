import datetime
from calendar import month

from models.budget import Budget
from models.transaction import Income, Expense
class FinanceAnalyzer:
    @staticmethod
    def calc_total_balance(accounts):
        return sum(account.balance for account in accounts)
    @staticmethod
    def calc_monthly_income(transactions, month, year):
        return sum(transaction.amount for transaction in transactions
                   if transaction.date.month == month and transaction.date.year == year and isinstance(transaction, Income))
    @staticmethod
    def calc_monthly_expense(transactions, month, year):
        return sum(transaction.amount for transaction in transactions
                   if transaction.date.month == month and transaction.date.year == year and isinstance(transaction, Expense))
    @staticmethod
    def calc_net_savings(transactions, month, year):
        return FinanceAnalyzer.calc_monthly_income(transactions, month, year) - FinanceAnalyzer.calc_monthly_expense(
            transactions, month, year)
    @staticmethod
    def calc_category_spending(transactions, category, month, year):
        return sum(transaction.amount for transaction in transactions if
                   transaction.date.month == month and transaction.date.year == year and isinstance(transaction, Expense)
                   and transaction.category.category_id == category.category_id)

class BudgetAnalyzer:
    @staticmethod
    def calc_budget_spending(budget, transactions):
        if budget.is_overall():
            budget = FinanceAnalyzer.calc_monthly_expense(transactions, budget.month, budget.year)
        else:
            budget = FinanceAnalyzer.calc_category_spending(transactions, budget.category, budget.month, budget.year)
        return budget
    @staticmethod
    def calc_budget_remaining(budget, transactions):
        return budget.amount - BudgetAnalyzer.calc_budget_spending(budget, transactions)
    @staticmethod
    def calc_budget_percentage(budget, transactions):
        return (BudgetAnalyzer.calc_budget_spending(budget, transactions) / budget.amount)*100
    @staticmethod
    def is_budget_exceeded(budget, transactions):
        return BudgetAnalyzer.calc_budget_remaining(budget, transactions) < 0

class SavingAnalyzer:
    @staticmethod
    def calc_saved_sofar(goal, transactions):
        return sum(FinanceAnalyzer.calc_net_savings(transactions, month, goal.year) for month in goal.monthly_targets)
    @staticmethod
    def calc_savings_progress(goal, transactions):
        return (SavingAnalyzer.calc_saved_sofar(goal, transactions) / goal.target_amount)*100
    @staticmethod
    def calc_savings_shortfall(goal, transactions, month):
        month = int(month)
        if month not in goal.monthly_targets:
            raise ValueError("Month is not in the saving plan")
        return max(goal.monthly_targets.get(month) - FinanceAnalyzer.calc_net_savings(transactions, month, goal.year) ,0)
    @staticmethod
    def calc_savings_surplus(goal, transactions, month):
        month = int(month)
        if month not in goal.monthly_targets:
            raise ValueError("Month is not in the saving plan")
        return max(FinanceAnalyzer.calc_net_savings(transactions, month, goal.year) - goal.monthly_targets.get(month),0)
    @staticmethod
    def calc_req_monthly(goal, transactions):
        remaining_cost = goal.target_amount - SavingAnalyzer.calc_saved_sofar(goal, transactions)
        if goal.year < datetime.date.today().year:
            raise ValueError("Saving goal year has already passed")
        remaining_months = len([goal.monthly_targets] if goal.year > datetime.date.today().year else [month for month in goal.monthly_targets if month >= datetime.date.today().month])
        if remaining_cost <= 0:
            return 0
        if remaining_months <= 0:
            raise ValueError("Months cannot be negative or zero")
        req = remaining_cost / remaining_months
        return req
