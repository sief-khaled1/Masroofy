class User:
    def __init__(self,user_id,name,email,password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
    
    def update_name(self,name):
        if name:
            self.name = name
            return True
        return False
      
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password")
        )