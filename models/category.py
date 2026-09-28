from models.user import User


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
    
    def rename_category(self, user:User, category:Category, name):
        if any(c.category_id != category.category_id and c.name.casefold() == name.strip().casefold() for c in user.categories):
            return "Category already exists."
        result = category.rename(name.strip())
        self._save_user_data("categories.json", user.user_id, user.categories)
        return result
    
    def activate_category(self, user:User, category:Category):
        result = category.activate()
        self._save_user_data("categories.json", user.user_id, user.categories)
        return result
    
    def deactivate_category(self, user:User, category:Category):
        result = category.deactivate()
        self._save_user_data("categories.json", user.user_id, user.categories)
        return result
    
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