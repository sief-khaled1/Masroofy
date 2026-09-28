import datetime
import customtkinter as ctk

from gui.theme import COLORS, FONT
from gui.components import SectionCard, page_header, show_message
from gui.utils import money
from services.finance_analyzer import SavingAnalyzer

class SavingsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.user = app.current_user

        page_header(self, "Saving Goals", "Create annual goals and monthly saving targets")

        ctk.CTkButton(self, text="+ New Goal", fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                      command=self.open_create).pack(anchor="e", pady=(0, 12))

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        self.render_goals()

    def render_goals(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.user.savings_goals:
            ctk.CTkLabel(self.list_frame, text="No saving goals yet.", text_color=COLORS["muted"]).pack(pady=80)
            return

        for goal in self.user.savings_goals:
            card = SectionCard(self.list_frame)
            card.pack(fill="x", pady=6)

            progress_value = SavingAnalyzer.calc_savings_progress(goal, self.user.transactions)
            progress = min(max(progress_value, 0), 100)

            ctk.CTkLabel(card, text=f"{goal.year} Saving Goal", font=(FONT, 16, "bold")).pack(anchor="w", padx=18, pady=(14, 2))
            ctk.CTkLabel(card, text=f"Target: {money(goal.target_amount)}", text_color=COLORS["text"]).pack(anchor="w", padx=18)
            ctk.CTkLabel(card, text=f"{progress:.1f}% complete", text_color=COLORS["primary"]).pack(anchor="w", padx=18, pady=(6, 3))

            bar = ctk.CTkProgressBar(card, width=430)
            bar.set(progress / 100)
            bar.pack(anchor="w", padx=18, pady=(0, 8))

            targets = ", ".join([f"{month}: {money(amount)}" for month, amount in sorted(goal.monthly_targets.items())]) or "No monthly targets yet"
            ctk.CTkLabel(card, text=targets, wraplength=650, justify="left", text_color=COLORS["muted"]).pack(anchor="w", padx=18, pady=(0, 12))

            buttons = ctk.CTkFrame(card, fg_color="transparent")
            buttons.pack(anchor="e", padx=18, pady=(0, 12))

            ctk.CTkButton(buttons, text="Add Monthly Target", width=145, command=lambda g=goal: self.add_target(g)).pack(side="left", padx=4)
            ctk.CTkButton(buttons, text="Delete", width=90, fg_color=COLORS["danger"], command=lambda g=goal: self.delete_goal(g)).pack(side="left", padx=4)

    def open_create(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("New Saving Goal")
        dialog.geometry("420x340")
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["background"])

        card = SectionCard(dialog)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text="New Saving Goal", font=(FONT, 20, "bold")).pack(pady=(22, 16))

        year = ctk.CTkEntry(card, placeholder_text=f"Year (e.g. {datetime.date.today().year})", width=300)
        amount = ctk.CTkEntry(card, placeholder_text="Annual target amount", width=300)
        year.pack(pady=8)
        amount.pack(pady=8)

        def submit():
            try:
                message = self.app.finance_manager.create_savings_goal(self.user, int(year.get()), float(amount.get()))
                dialog.destroy()
                show_message(self, "Saving Goal", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
                self.render_goals()
            except Exception as e:
                show_message(dialog, "Saving Goal", str(e), COLORS["danger"])

        ctk.CTkButton(card, text="Create Goal", width=300, fg_color=COLORS["primary"], command=submit).pack(pady=20)

    def add_target(self, goal):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Monthly Target")
        dialog.geometry("400x340")
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["background"])

        card = SectionCard(dialog)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text="Add Monthly Target", font=(FONT, 19, "bold")).pack(pady=(22, 16))

        month = ctk.CTkEntry(card, placeholder_text="Month number (1-12)", width=290)
        amount = ctk.CTkEntry(card, placeholder_text="Target amount", width=290)
        month.pack(pady=8)
        amount.pack(pady=8)

        def submit():
            try:
                message = self.app.finance_manager.add_to_savings_plan(self.user, goal, int(month.get()), float(amount.get()))
                dialog.destroy()
                show_message(self, "Saving Goal", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
                self.render_goals()
            except Exception as e:
                show_message(dialog, "Saving Goal", str(e), COLORS["danger"])

        ctk.CTkButton(card, text="Save Target", width=290, fg_color=COLORS["primary"], command=submit).pack(pady=18)

    def delete_goal(self, goal):
        try:
            self.app.finance_manager.delete_saving_goal(self.user, goal.goal_id)
            show_message(self, "Saving Goal", "Saving goal deleted successfully.", COLORS["success"])
            self.render_goals()
        except Exception as e:
            show_message(self, "Saving Goal", str(e), COLORS["danger"])
