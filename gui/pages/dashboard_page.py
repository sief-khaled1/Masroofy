import datetime
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.theme import COLORS, FONT
from gui.components import StatCard, SectionCard, page_header
from gui.utils import money

from services.finance_analyzer import FinanceAnalyzer

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.user = app.current_user

        page_header(self, "Dashboard", "Overview of your current financial month")

        today = datetime.date.today()
        income = FinanceAnalyzer.calc_monthly_income(self.user.transactions, today.month, today.year)
        expense = FinanceAnalyzer.calc_monthly_expense(self.user.transactions, today.month, today.year)
        net = FinanceAnalyzer.calc_net_savings(self.user.transactions, today.month, today.year)
        balance = FinanceAnalyzer.calc_total_balance(self.user.accounts)

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x")

        values = [
            ("Total Balance", money(balance), "Across all accounts"),
            ("Monthly Income", money(income), "This month"),
            ("Monthly Expenses", money(expense), "This month"),
            ("Net Savings", money(net), "Income - expenses")
        ]

        for title, value, subtitle in values:
            StatCard(cards, title, value, subtitle).pack(side="left", fill="both", expand=True, padx=(0, 10))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, pady=(18, 0))

        self.create_income_expense_chart(body, income, expense)
        self.create_category_chart(body, today.month, today.year)

    def create_income_expense_chart(self, master, income, expense):
        card = SectionCard(master)
        card.pack(side="left", fill="both", expand=True, padx=(0, 9))

        ctk.CTkLabel(card, text="Income vs Expenses", text_color=COLORS["text"], font=(FONT, 17, "bold")).pack(anchor="w", padx=18, pady=(16, 0))

        figure = Figure(figsize=(4.4, 3.2), dpi=90)
        ax = figure.add_subplot(111)
        ax.bar(["Income", "Expenses"], [income, expense])
        ax.set_ylabel("EGP")
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

    def create_category_chart(self, master, month, year):
        card = SectionCard(master)
        card.pack(side="left", fill="both", expand=True, padx=(9, 0))

        ctk.CTkLabel(card, text="Spending by Category", text_color=COLORS["text"], font=(FONT, 17, "bold")).pack(anchor="w", padx=18, pady=(16, 0))

        labels = []
        values = []

        for category in self.user.categories:
            spending = FinanceAnalyzer.calc_category_spending(self.user.transactions, category, month, year)
            if spending > 0:
                labels.append(category.name)
                values.append(spending)

        if not values:
            ctk.CTkLabel(card, text="No expense data for this month.", text_color=COLORS["muted"]).pack(expand=True)
            return

        figure = Figure(figsize=(4.4, 3.2), dpi=90)
        ax = figure.add_subplot(111)
        ax.pie(values, labels=labels, autopct="%1.0f%%")
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)
