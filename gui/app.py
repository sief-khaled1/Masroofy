import os
import customtkinter as ctk

from models.user import User
from models.category import Category
from services.auth_manager import AuthManager
from services.file_manager import FileManager
from services.finance_manager import FinanceManager
from services.user_data_loader import UserDataLoader

from gui.theme import COLORS
from gui.utils import ensure_data_files
from gui.pages.login_page import LoginPage
from gui.pages.register_page import RegisterPage
from gui.main_layout import MainLayout

class MasroofyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("Masroofy")
        self.geometry("1240x780")
        self.minsize(1050, 680)
        self.configure(fg_color=COLORS["background"])

        ensure_data_files()

        self.file_manager = FileManager()
        self.finance_manager = FinanceManager()
        self.user_loader = UserDataLoader()
        self.users = self.load_users()
        self.auth_manager = AuthManager(self.users)
        self.current_user = None

        self.show_login()

    def load_users(self):
        path = os.path.join(os.getcwd(), "data", "users.json")
        data = self.file_manager.load(path)
        return {item["email"]: User.from_dict(item) for item in data}

    def save_users(self):
        path = os.path.join(os.getcwd(), "data", "users.json")
        self.file_manager.save(path, [user.to_dict() for user in self.users.values()])

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.current_user = None
        self.clear()
        LoginPage(self, self).pack(fill="both", expand=True)

    def show_register(self):
        self.clear()
        RegisterPage(self, self).pack(fill="both", expand=True)

    def login(self, email, password):
        result = self.auth_manager.login(email, password)

        if isinstance(result, str):
            return result

        self.current_user = self.user_loader.load_user_data(result)
        self.ensure_default_categories()
        self.show_main()
        return "Login successful."

    def register(self, name, email, password, confirm_password):
        result = self.auth_manager.register(name, email, password, confirm_password)

        if result == "User registered successfully.":
            self.save_users()

        return result

    def ensure_default_categories(self):
        if self.current_user.categories:
            return

        for name in Category.default_categories:
            self.finance_manager.create_category(self.current_user, name)

    def show_main(self):
        self.clear()
        MainLayout(self, self).pack(fill="both", expand=True)
