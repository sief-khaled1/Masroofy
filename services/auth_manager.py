from models.user import User
class AuthManager:
    def __init__(self,users):
        self.users = users
    
    def register(self,name,email,password,confirm_password):
        if not name:
            return "Name cannot be empty."
        if email.count('@') != 1 or email.startswith('@') or email.endswith('@'):
            return "Invalid email format."
        if email in self.users:
            return "Email already exists."
        if len(password) < 8:
            return "Password must be at least 8 characters long."
        if password != confirm_password:
            return "Passwords do not match."
        self.users[email] = User(user_id=len(self.users) + 1, name=name, email=email, password=password)
        return "User registered successfully."
    
    def login(self,email,password):
        user = self.users.get(email)
        if not user:
            return "Invalid email or password."
        if user.password != password:
            return "Invalid email or password."
        return user
    
    def change_password(self,user,current_password,new_password):
        if user.password != current_password:
            return "Current password is incorrect."
        if len(new_password) < 8:
            return "New password must be at least 8 characters long."
        user.password = new_password
        return "Password changed successfully."
    
