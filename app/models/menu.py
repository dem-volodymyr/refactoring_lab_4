from typing import List, Optional
from uuid import UUID

from app.models.dish import Dish


class Menu:
    """
    Represents a collection of available dishes.
    Follows the Single Responsibility Principle by only managing dishes in the menu.
    """
    
    def __init__(self):
        self._dishes: List[Dish] = []
        
    def add_dish(self, dish: Dish) -> None:
        """Add a dish to the menu if it doesn't already exist."""
        if not self.contains_dish(dish):
            self._dishes.append(dish)
            
    def remove_dish(self, dish_id: UUID) -> bool:
        """Remove a dish from the menu by its ID."""
        for i, dish in enumerate(self._dishes):
            if dish.id == dish_id:
                self._dishes.pop(i)
                return True
        return False
        
    def get_dish(self, dish_id: UUID) -> Optional[Dish]:
        """Get a dish from the menu by its ID."""
        for dish in self._dishes:
            if dish.id == dish_id:
                return dish
        return None
        
    def contains_dish(self, dish: Dish) -> bool:
        """Check if a dish is in the menu."""
        return dish in self._dishes
        
    def get_all_dishes(self) -> List[Dish]:
        """Get all dishes in the menu."""
        return self._dishes.copy()
        
    def get_dishes_by_category(self, category: str) -> List[Dish]:
        """Get all dishes in a specific category."""
        return [dish for dish in self._dishes if dish.category == category] 