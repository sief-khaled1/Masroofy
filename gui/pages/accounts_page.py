import customtkinter as ctk
from gui.theme import COLORS, FONT
from gui.components import SectionCard, page_header, show_message
from gui.utils import money

class AccountsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.user = app.current_user

        page_header(self, "Accounts", "Cash, bank accounts and wallets")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(0, 12))

        ctk.CTkButton(actions, text="+ Add Account", fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                      command=self.open_add_account).pack(side="right")

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        self.render_accounts()

    def render_accounts(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.user.accounts:
            ctk.CTkLabel(self.list_frame, text="No accounts yet.", text_color=COLORS["muted"]).pack(pady=80)
            return

        for account in self.user.accounts:
            card = SectionCard(self.list_frame)
            card.pack(fill="x", pady=6)

            ctk.CTkLabel(card, text=account.get_display_name(), font=(FONT, 16, "bold"), text_color=COLORS["text"]).pack(anchor="w", padx=18, pady=(14, 2))
            ctk.CTkLabel(card, text=money(account.balance), font=(FONT, 20, "bold"), text_color=COLORS["primary"]).pack(anchor="w", padx=18)
            status = "Active" if account.is_active else "Inactive"
            ctk.CTkLabel(card, text=status, text_color=COLORS["success"] if account.is_active else COLORS["muted"]).pack(anchor="w", padx=18, pady=(3, 12))

            if account.is_active:
                ctk.CTkButton(card, text="Deactivate", width=110, fg_color="transparent", border_width=1, border_color=COLORS["danger"],
                              text_color=COLORS["danger"], hover_color=COLORS["surface_alt"],
                              command=lambda a=account: self.deactivate(a)).pack(anchor="e", padx=18, pady=(0, 14))

    def open_add_account(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Account")
        dialog.geometry("420x360")
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["background"])

        card = SectionCard(dialog)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text="Add Account", font=(FONT, 19, "bold")).pack(pady=(24, 16))

        account_type = ctk.CTkOptionMenu(card, values=["cash", "bank", "wallet"], width=300)
        account_type.pack(pady=8)

        balance = ctk.CTkEntry(card, placeholder_text="Opening balance", width=300)
        balance.pack(pady=8)

        def submit():
            try:
                amount = float(balance.get())
                message = self.app.finance_manager.create_account(self.user, account_type.get(), amount)
                dialog.destroy()
                show_message(self, "Account", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
                self.render_accounts()
            except Exception as e:
                show_message(dialog, "Account", str(e), COLORS["danger"])

        ctk.CTkButton(card, text="Create Account", width=300, fg_color=COLORS["primary"], command=submit).pack(pady=20)

    def deactivate(self, account):
        try:
            message = self.app.finance_manager.deactivate_account(account, self.user)
            show_message(self, "Account", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
            self.render_accounts()
        except Exception as e:
            show_message(self, "Account", str(e), COLORS["danger"])
