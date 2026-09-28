import customtkinter as ctk
from gui.theme import COLORS, FONT
from gui.components import SectionCard, page_header, show_message

class CategoriesPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.user = app.current_user

        page_header(self, "Categories", "Organize your expenses")

        ctk.CTkButton(self, text="+ Add Category", fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                      command=self.add_category).pack(anchor="e", pady=(0, 12))

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        self.render_categories()

    def save_categories(self):
        self.app.finance_manager.save_user_data("categories.json", self.user.user_id, self.user.categories)

    def render_categories(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for category in self.user.categories:
            card = SectionCard(self.list_frame)
            card.pack(fill="x", pady=5)

            ctk.CTkLabel(card, text=category.name, font=(FONT, 15, "bold"), text_color=COLORS["text"]).pack(side="left", padx=18, pady=18)
            ctk.CTkLabel(card, text="Active" if category.is_active else "Inactive",
                         text_color=COLORS["success"] if category.is_active else COLORS["muted"]).pack(side="left", padx=8)

            buttons = ctk.CTkFrame(card, fg_color="transparent")
            buttons.pack(side="right", padx=14)

            ctk.CTkButton(buttons, text="Rename", width=85, command=lambda c=category: self.rename(c)).pack(side="left", padx=4)
            text = "Deactivate" if category.is_active else "Activate"
            ctk.CTkButton(buttons, text=text, width=100, fg_color=COLORS["danger"] if category.is_active else COLORS["success"],
                          command=lambda c=category: self.toggle(c)).pack(side="left", padx=4)

    def add_category(self):
        dialog = ctk.CTkInputDialog(text="Category name:", title="Add Category")
        name = dialog.get_input()

        if not name:
            return

        try:
            message = self.app.finance_manager.create_category(self.user, name)
            show_message(self, "Category", message, COLORS["success"] if "successfully" in message else COLORS["danger"])
            self.render_categories()
        except Exception as e:
            show_message(self, "Category", str(e), COLORS["danger"])

    def rename(self, category):
        dialog = ctk.CTkInputDialog(text="New category name:", title="Rename Category")
        name = dialog.get_input()

        if not name:
            return

        if any(c.category_id != category.category_id and c.name.casefold() == name.strip().casefold() for c in self.user.categories):
            show_message(self, "Category", "Category already exists.", COLORS["danger"])
            return

        try:
            category.rename(name)
            self.save_categories()
            self.render_categories()
        except Exception as e:
            show_message(self, "Category", str(e), COLORS["danger"])

    def toggle(self, category):
        if category.is_active:
            category.deactivate()
        else:
            category.activate()

        self.save_categories()
        self.render_categories()
