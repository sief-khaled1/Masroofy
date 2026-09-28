import customtkinter as ctk
from gui.theme import COLORS, FONT

class StatCard(ctk.CTkFrame):
    def __init__(self, master, title, value, subtitle=""):
        super().__init__(master, fg_color=COLORS["surface"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        ctk.CTkLabel(self, text=title, text_color=COLORS["muted"], font=(FONT, 13)).pack(anchor="w", padx=18, pady=(16, 4))
        ctk.CTkLabel(self, text=value, text_color=COLORS["text"], font=(FONT, 23, "bold")).pack(anchor="w", padx=18)
        if subtitle:
            ctk.CTkLabel(self, text=subtitle, text_color=COLORS["muted"], font=(FONT, 11)).pack(anchor="w", padx=18, pady=(5, 15))
        else:
            ctk.CTkLabel(self, text="", font=(FONT, 11)).pack(pady=(5, 15))

class SectionCard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["surface"], corner_radius=14, border_width=1, border_color=COLORS["border"])

def page_header(master, title, subtitle=""):
    ctk.CTkLabel(master, text=title, text_color=COLORS["text"], font=(FONT, 28, "bold")).pack(anchor="w")
    ctk.CTkLabel(master, text=subtitle, text_color=COLORS["muted"], font=(FONT, 13)).pack(anchor="w", pady=(2, 18))

def show_message(master, title, message, color=None):
    dialog = ctk.CTkToplevel(master)
    dialog.title(title)
    dialog.geometry("420x210")
    dialog.resizable(False, False)
    dialog.transient(master.winfo_toplevel())
    dialog.grab_set()
    dialog.configure(fg_color=COLORS["background"])

    card = SectionCard(dialog)
    card.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(card, text=title, font=(FONT, 18, "bold"), text_color=color or COLORS["text"]).pack(pady=(28, 10))
    ctk.CTkLabel(card, text=message, wraplength=340, text_color=COLORS["muted"], font=(FONT, 13)).pack(padx=20)
    ctk.CTkButton(card, text="OK", width=110, fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], command=dialog.destroy).pack(pady=22)
