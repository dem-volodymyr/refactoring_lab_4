from typing import List, Optional
from uuid import UUID

from app.models.dish import Dish
from app.models.menu import Menu
from app.services.order_database import OrderDatabase


class MenuService:
    """
    Service for managing the menu.
    Follows the Single Responsibility Principle by focusing only on menu operations.
    """
    
    def __init__(self):
        self.db = OrderDatabase()
        
    def get_menu(self) -> Menu:
        """Get the menu."""
        return self.db.get_menu()
        
    def add_dish(self, name: str, price: float, description: Optional[str] = None, category: Optional[str] = None) -> Dish:
        """Add a dish to the menu."""
        dish = Dish(name=name, price=price, description=description, category=category)
        self.db.add_dish_to_menu(dish)
        return dish
        
    def get_dish(self, dish_id: UUID) -> Optional[Dish]:
        """Get a dish by ID."""
        return self.db.get_menu().get_dish(dish_id)
        
    def get_all_dishes(self) -> List[Dish]:
        """Get all dishes in the menu."""
        return self.db.get_menu().get_all_dishes()
        
    def get_dishes_by_category(self, category: str) -> List[Dish]:
        """Get all dishes in a specific category."""
        return self.db.get_menu().get_dishes_by_category(category) 