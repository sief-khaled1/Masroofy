class Category:
    def __init__(self,category_id,user_id,name,is_default=False,is_active=True):
        self.category_id = category_id
        self.user_id = user_id
        if not name:
            raise ValueError("Category name cannot be empty")
        self.name = name
        self.is_default = is_default
        self.is_active = is_active
    
    default_categories = ["Food","Transportation","Shopping","Bills","Health","Education","Entertainment","Other"]
    
    def rename(self,name):
        if self.is_default:
            return "Default categories cannot be renamed"
        if not name:
            return "Category name cannot be empty"
        self.name = name
        return "Category renamed successfully."
    
    def activate(self):
        if self.is_active:
            return "Category is already active."
        self.is_active = True
        return "Category activated successfully."
    
    def deactivate(self):
        if not self.is_active:
            return "Category is already inactive."
        self.is_active = False
        return "Category deactivated successfully."
    
    def to_dict(self):
        return {
            "category_id": self.category_id,
            "user_id": self.user_id,
            "name": self.name,
            "is_default": self.is_default,
            "is_active": self.is_active
        }
    
    @staticmethod
    def from_dict(data):
        return Category(
            category_id=data.get("category_id"),
            user_id=data.get("user_id"),
            name=data.get("name"),
            is_default=data.get("is_default", False),
            is_active=data.get("is_active", True)
        )