import customtkinter as ctk
from gui.theme import COLORS, FONT

from gui.pages.dashboard_page import DashboardPage
from gui.pages.accounts_page import AccountsPage
from gui.pages.transactions_page import TransactionsPage
from gui.pages.budgets_page import BudgetsPage
from gui.pages.savings_page import SavingsPage
from gui.pages.categories_page import CategoriesPage

class MainLayout(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=COLORS["background"], corner_radius=0)
        self.app = app

        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=COLORS["navy"], corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ctk.CTkFrame(self, fg_color=COLORS["background"], corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(self.sidebar, text="MASROOFY", text_color="white", font=(FONT, 25, "bold")).pack(pady=(30, 6))
        ctk.CTkLabel(self.sidebar, text=app.current_user.name, text_color=COLORS["secondary"], font=(FONT, 12)).pack(pady=(0, 24))

        pages = [
            ("Dashboard", DashboardPage),
            ("Accounts", AccountsPage),
            ("Transactions", TransactionsPage),
            ("Budgets", BudgetsPage),
            ("Saving Goals", SavingsPage),
            ("Categories", CategoriesPage)
        ]

        for text, page in pages:
            ctk.CTkButton(self.sidebar, text=text, anchor="w", height=42, fg_color="transparent", hover_color=COLORS["primary"],
                          command=lambda p=page: self.show_page(p)).pack(fill="x", padx=14, pady=4)

        ctk.CTkButton(self.sidebar, text="Logout", anchor="w", height=42, fg_color="transparent", hover_color=COLORS["danger"],
                      command=app.show_login).pack(side="bottom", fill="x", padx=14, pady=22)

        self.show_page(DashboardPage)

    def show_page(self, page):
        for widget in self.content.winfo_children():
            widget.destroy()

        page(self.content, self.app).pack(fill="both", expand=True, padx=28, pady=24)

    def refresh_page(self, page):
        self.show_page(page)
