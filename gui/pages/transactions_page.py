import customtkinter as ctk

from models.transaction import Income, Expense, Transfer
from gui.theme import COLORS, FONT
from gui.components import SectionCard, page_header, show_message
from gui.utils import money, parse_date

class TransactionsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.user = app.current_user

        page_header(self, "Transactions", "Income, expenses and transfers")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(0, 12))

        ctk.CTkButton(actions, text="+ Income", fg_color=COLORS["success"], command=self.open_income).pack(side="left", padx=(0, 8))
        ctk.CTkButton(actions, text="+ Expense", fg_color=COLORS["danger"], command=self.open_expense).pack(side="left", padx=(0, 8))
        ctk.CTkButton(actions, text="Transfer", fg_color=COLORS["primary"], command=self.open_transfer).pack(side="left")

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        self.render_transactions()

    def account_options(self):
        return {f"{account.account_id} - {account.get_display_name()}": account for account in self.user.accounts if account.is_active}

    def category_options(self):
        return {f"{category.category_id} - {category.name}": category for category in self.user.categories if category.is_active}

    def render_transactions(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.user.transactions:
            ctk.CTkLabel(self.list_frame, text="No transactions yet.", text_color=COLORS["muted"]).pack(pady=80)
            return

        for transaction in reversed(self.user.transactions):
            card = SectionCard(self.list_frame)
            card.pack(fill="x", pady=5)

            if isinstance(transaction, Income):
                title = f"Income · {transaction.source}"
                detail = transaction.destination_account.get_display_name()
                color = COLORS["success"]
                amount = f"+ {money(transaction.amount)}"
            elif isinstance(transaction, Expense):
                title = f"Expense · {transaction.category.name}"
                detail = transaction.source_account.get_display_name()
                color = COLORS["danger"]
                amount = f"- {money(transaction.amount)}"
            else:
                title = "Transfer"
                detail = f"{transaction.source_account.get_display_name()} → {transaction.destination_account.get_display_name()}"
                color = COLORS["primary"]
                amount = money(transaction.amount)

            ctk.CTkLabel(card, text=title, font=(FONT, 15, "bold"), text_color=COLORS["text"]).pack(anchor="w", padx=16, pady=(12, 2))
            ctk.CTkLabel(card, text=detail, text_color=COLORS["muted"]).pack(anchor="w", padx=16)
            ctk.CTkLabel(card, text=str(transaction.date), text_color=COLORS["muted"], font=(FONT, 11)).pack(anchor="w", padx=16, pady=(2, 12))
            ctk.CTkLabel(card, text=amount, text_color=color, font=(FONT, 16, "bold")).place(relx=.97, rely=.5, anchor="e")

    def build_dialog(self, title):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("430x480")
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["background"])

        card = SectionCard(dialog)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text=title, font=(FONT, 20, "bold")).pack(pady=(22, 16))
        return dialog, card

    def open_income(self):
        accounts = self.account_options()

        if not accounts:
            show_message(self, "Income", "Create an active account first.", COLORS["danger"])
            return

        dialog, card = self.build_dialog("Add Income")
        amount = ctk.CTkEntry(card, placeholder_text="Amount", width=310)
        source = ctk.CTkEntry(card, placeholder_text="Source (Salary, Freelance...)", width=310)
        account = ctk.CTkOptionMenu(card, values=list(accounts.keys()), width=310)
        date = ctk.CTkEntry(card, placeholder_text="Date YYYY-MM-DD (blank = today)", width=310)

        for widget in [amount, source, account, date]:
            widget.pack(pady=7)

        def submit():
            try:
                message = self.app.finance_manager.add_income(self.user, float(amount.get()), source.get().strip() or "Other", accounts[account.get()], parse_date(date.get()))
                dialog.destroy()
                show_message(self, "Income", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
                self.render_transactions()
            except Exception as e:
                show_message(dialog, "Income", str(e), COLORS["danger"])

        ctk.CTkButton(card, text="Add Income", width=310, fg_color=COLORS["success"], command=submit).pack(pady=18)

    def open_expense(self):
        accounts = self.account_options()
        categories = self.category_options()

        if not accounts or not categories:
            show_message(self, "Expense", "You need an active account and category first.", COLORS["danger"])
            return

        dialog, card = self.build_dialog("Add Expense")
        amount = ctk.CTkEntry(card, placeholder_text="Amount", width=310)
        account = ctk.CTkOptionMenu(card, values=list(accounts.keys()), width=310)
        category = ctk.CTkOptionMenu(card, values=list(categories.keys()), width=310)
        date = ctk.CTkEntry(card, placeholder_text="Date YYYY-MM-DD (blank = today)", width=310)

        for widget in [amount, account, category, date]:
            widget.pack(pady=7)

        def submit():
            try:
                message = self.app.finance_manager.add_expense(self.user, float(amount.get()), accounts[account.get()], categories[category.get()], parse_date(date.get()))
                dialog.destroy()
                show_message(self, "Expense", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
                self.render_transactions()
            except Exception as e:
                show_message(dialog, "Expense", str(e), COLORS["danger"])

        ctk.CTkButton(card, text="Add Expense", width=310, fg_color=COLORS["danger"], command=submit).pack(pady=18)

    def open_transfer(self):
        accounts = self.account_options()

        if len(accounts) < 2:
            show_message(self, "Transfer", "Create at least two active accounts first.", COLORS["danger"])
            return

        dialog, card = self.build_dialog("Transfer Money")
        amount = ctk.CTkEntry(card, placeholder_text="Amount", width=310)
        source = ctk.CTkOptionMenu(card, values=list(accounts.keys()), width=310)
        destination = ctk.CTkOptionMenu(card, values=list(accounts.keys()), width=310)
        date = ctk.CTkEntry(card, placeholder_text="Date YYYY-MM-DD (blank = today)", width=310)

        for widget in [amount, source, destination, date]:
            widget.pack(pady=7)

        def submit():
            try:
                message = self.app.finance_manager.transfer(self.user, float(amount.get()), accounts[source.get()], accounts[destination.get()], parse_date(date.get()))
                dialog.destroy()
                show_message(self, "Transfer", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
                self.render_transactions()
            except Exception as e:
                show_message(dialog, "Transfer", str(e), COLORS["danger"])

        ctk.CTkButton(card, text="Transfer", width=310, fg_color=COLORS["primary"], command=submit).pack(pady=18)
