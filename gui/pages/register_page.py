import customtkinter as ctk
from gui.theme import COLORS, FONT
from gui.components import SectionCard, show_message

class RegisterPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=COLORS["background"], corner_radius=0)
        self.app = app

        card = SectionCard(self)
        card.configure(width=440, height=570)
        card.place(relx=.5, rely=.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="Create Account", text_color=COLORS["text"], font=(FONT, 27, "bold")).pack(pady=(34, 22))

        self.name = ctk.CTkEntry(card, width=320, height=42, placeholder_text="Full name")
        self.email = ctk.CTkEntry(card, width=320, height=42, placeholder_text="Email")
        self.password = ctk.CTkEntry(card, width=320, height=42, placeholder_text="Password", show="•")
        self.confirm = ctk.CTkEntry(card, width=320, height=42, placeholder_text="Confirm password", show="•")

        for entry in [self.name, self.email, self.password, self.confirm]:
            entry.pack(pady=7)

        ctk.CTkButton(card, text="Register", width=320, height=44, fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                      command=self.register).pack(pady=(18, 8))

        ctk.CTkButton(card, text="Back to login", width=320, fg_color="transparent", text_color=COLORS["primary"],
                      command=app.show_login).pack()

    def register(self):
        message = self.app.register(self.name.get().strip(), self.email.get().strip(), self.password.get(), self.confirm.get())
        color = COLORS["success"] if message == "User registered successfully." else COLORS["danger"]
        show_message(self, "Register", message, color)

        if message == "User registered successfully.":
            self.after(700, self.app.show_login)
