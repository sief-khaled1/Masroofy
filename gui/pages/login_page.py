import customtkinter as ctk
from gui.theme import COLORS, FONT
from gui.components import SectionCard, show_message

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=COLORS["background"], corner_radius=0)
        self.app = app

        card = SectionCard(self)
        card.configure(width=420, height=470)
        card.place(relx=.5, rely=.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="Masroofy", text_color=COLORS["primary"], font=(FONT, 31, "bold")).pack(pady=(42, 6))
        ctk.CTkLabel(card, text="Personal finance made simple", text_color=COLORS["muted"], font=(FONT, 13)).pack(pady=(0, 28))

        self.email = ctk.CTkEntry(card, width=315, height=44, placeholder_text="Email")
        self.email.pack(pady=8)

        self.password = ctk.CTkEntry(card, width=315, height=44, placeholder_text="Password", show="•")
        self.password.pack(pady=8)

        ctk.CTkButton(card, text="Login", width=315, height=44, fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                      command=self.login).pack(pady=(20, 10))

        ctk.CTkButton(card, text="Create account", width=315, height=40, fg_color="transparent", border_width=1,
                      border_color=COLORS["primary"], text_color=COLORS["primary"], hover_color=COLORS["surface_alt"],
                      command=app.show_register).pack()

    def login(self):
        message = self.app.login(self.email.get().strip(), self.password.get())

        if message != "Login successful.":
            show_message(self, "Login", message, COLORS["danger"])
