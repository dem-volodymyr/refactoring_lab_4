from typing import List, Optional
from uuid import UUID

from app.models.dish import Dish
from app.models.order import Order, OrderStatus
from app.services.order_database import OrderDatabase
from app.services.order_factory import OrderFactoryProvider, OrderType


class OrderService:
    """
    Service for managing orders.
    Follows the Single Responsibility Principle by focusing only on order operations.
    """
    
    def __init__(self):
        self.db = OrderDatabase()
        
    def create_order(self, customer_id: UUID, dish_ids: List[UUID], order_type: OrderType = OrderType.REGULAR) -> Order:
        """Create a new order for a customer with the given dishes."""
        # Get the dishes from the menu
        dishes = []
        menu = self.db.get_menu()
        
        for dish_id in dish_ids:
            dish = menu.get_dish(dish_id)
            if dish:
                dishes.append(dish)
                
        # Use the factory to create the order
        factory = OrderFactoryProvider.get_factory(order_type)
        order = factory.create_order(customer_id, dishes)
        
        # Save the order to the database
        self.db.add_order(order)
        
        return order
        
    def get_order(self, order_id: UUID) -> Optional[Order]:
        """Get an order by ID."""
        return self.db.get_order(order_id)
        
    def get_all_orders(self) -> List[Order]:
        """Get all orders."""
        return self.db.get_all_orders()
        
    def update_order_status(self, order_id: UUID, status: OrderStatus) -> bool:
        """Update an order's status."""
        order = self.db.get_order(order_id)
        if order:
            order.update_status(status)
            return True
        return False
        
    def add_dish_to_order(self, order_id: UUID, dish_id: UUID) -> bool:
        """Add a dish to an existing order."""
        order = self.db.get_order(order_id)
        menu = self.db.get_menu()
        
        if order and order.status == OrderStatus.CREATED:
            dish = menu.get_dish(dish_id)
            if dish:
                order.add_dish(dish)
                return True
        return False
        
    def remove_dish_from_order(self, order_id: UUID, dish_id: UUID) -> bool:
        """Remove a dish from an existing order."""
        order = self.db.get_order(order_id)
        
        if order and order.status == OrderStatus.CREATED:
            return order.remove_dish(dish_id)
        return False
        
    def calculate_order_total(self, order_id: UUID) -> Optional[float]:
        """Calculate the total price of an order."""
        order = self.db.get_order(order_id)
        if order:
            return order.calculate_total()
        return None 