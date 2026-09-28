import datetime
import customtkinter as ctk

from gui.theme import COLORS, FONT
from gui.components import SectionCard, page_header, show_message
from gui.utils import money, month_name
from services.finance_analyzer import BudgetAnalyzer

class BudgetsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.user = app.current_user

        page_header(self, "Budgets", "Set monthly overall or category limits")

        ctk.CTkButton(self, text="+ New Budget", fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                      command=self.open_create).pack(anchor="e", pady=(0, 12))

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        self.render_budgets()

    def render_budgets(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.user.budgets:
            ctk.CTkLabel(self.list_frame, text="No budgets yet.", text_color=COLORS["muted"]).pack(pady=80)
            return

        for budget in self.user.budgets:
            card = SectionCard(self.list_frame)
            card.pack(fill="x", pady=6)

            name = "Overall Budget" if budget.is_overall() else budget.category.name
            spending = BudgetAnalyzer.calc_budget_spending(budget, self.user.transactions)
            remaining = BudgetAnalyzer.calc_budget_remaining(budget, self.user.transactions)
            percentage = BudgetAnalyzer.calc_budget_percentage(budget, self.user.transactions)

            ctk.CTkLabel(card, text=name, font=(FONT, 16, "bold")).pack(anchor="w", padx=18, pady=(14, 2))
            ctk.CTkLabel(card, text=f"{month_name(budget.month)} {budget.year}", text_color=COLORS["muted"]).pack(anchor="w", padx=18)
            ctk.CTkLabel(card, text=f"{money(spending)} spent of {money(budget.amount)}", text_color=COLORS["text"]).pack(anchor="w", padx=18, pady=(8, 3))

            progress = ctk.CTkProgressBar(card, width=420)
            progress.set(min(max(percentage / 100, 0), 1))
            progress.pack(anchor="w", padx=18, pady=6)

            ctk.CTkLabel(card, text=f"Remaining: {money(remaining)}", text_color=COLORS["danger"] if remaining < 0 else COLORS["success"]).pack(anchor="w", padx=18, pady=(0, 12))

            buttons = ctk.CTkFrame(card, fg_color="transparent")
            buttons.pack(anchor="e", padx=18, pady=(0, 12))

            ctk.CTkButton(buttons, text="Update", width=90, command=lambda b=budget: self.update_budget(b)).pack(side="left", padx=4)
            ctk.CTkButton(buttons, text="Delete", width=90, fg_color=COLORS["danger"], command=lambda b=budget: self.delete_budget(b)).pack(side="left", padx=4)

    def open_create(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("New Budget")
        dialog.geometry("440x500")
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["background"])

        card = SectionCard(dialog)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text="New Budget", font=(FONT, 20, "bold")).pack(pady=(22, 16))

        amount = ctk.CTkEntry(card, placeholder_text="Amount", width=310)
        month = ctk.CTkEntry(card, placeholder_text="Month number (1-12)", width=310)
        year = ctk.CTkEntry(card, placeholder_text=f"Year (e.g. {datetime.date.today().year})", width=310)

        categories = {"Overall": None}
        categories.update({category.name: category for category in self.user.categories if category.is_active})
        category = ctk.CTkOptionMenu(card, values=list(categories.keys()), width=310)

        for widget in [amount, month, year, category]:
            widget.pack(pady=7)

        def submit():
            try:
                message = self.app.finance_manager.create_budget(self.user, float(amount.get()), int(month.get()), int(year.get()), categories[category.get()])
                dialog.destroy()
                show_message(self, "Budget", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
                self.render_budgets()
            except Exception as e:
                show_message(dialog, "Budget", str(e), COLORS["danger"])

        ctk.CTkButton(card, text="Create Budget", width=310, fg_color=COLORS["primary"], command=submit).pack(pady=18)

    def update_budget(self, budget):
        dialog = ctk.CTkInputDialog(text="New budget amount:", title="Update Budget")
        value = dialog.get_input()

        if value is None:
            return

        try:
            message = self.app.finance_manager.update_budget(budget, float(value), self.user)
            show_message(self, "Budget", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
            self.render_budgets()
        except Exception as e:
            show_message(self, "Budget", str(e), COLORS["danger"])

    def delete_budget(self, budget):
        try:
            self.app.finance_manager.delete_budget(self.user, budget.budget_id)
            show_message(self, "Budget", "Budget deleted successfully.", COLORS["success"])
            self.render_budgets()
        except Exception as e:
            show_message(self, "Budget", str(e), COLORS["danger"])
