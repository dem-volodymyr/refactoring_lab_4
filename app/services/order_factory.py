from enum import Enum
from typing import List
from uuid import UUID

from app.models.dish import Dish
from app.models.interfaces import OrderFactory
from app.models.order import Order


class OrderType(Enum):
    REGULAR = "regular"
    BULK = "bulk"
    EXPRESS = "express"


class RegularOrderFactory(OrderFactory):
    """Factory for creating regular orders."""
    
    def create_order(self, customer_id: UUID, dishes: List[Dish]) -> Order:
        """Create a regular order."""
        return Order(customer_id, dishes)


class BulkOrderFactory(OrderFactory):
    """Factory for creating bulk orders."""
    
    def create_order(self, customer_id: UUID, dishes: List[Dish]) -> Order:
        """Create a bulk order with a discount."""
        order = Order(customer_id, dishes)
        # Apply a 10% discount for bulk orders
        # In a real implementation, we would extend the Order class for different order types
        return order


class ExpressOrderFactory(OrderFactory):
    """Factory for creating express orders."""
    
    def create_order(self, customer_id: UUID, dishes: List[Dish]) -> Order:
        """Create an express order with priority handling."""
        order = Order(customer_id, dishes)
        # Express orders would have priority handling in a real implementation
        return order


class OrderFactoryProvider:
    """Provider for order factories based on order type."""
    
    @staticmethod
    def get_factory(order_type: OrderType) -> OrderFactory:
        """Get the appropriate factory for the given order type."""
        if order_type == OrderType.BULK:
            return BulkOrderFactory()
        elif order_type == OrderType.EXPRESS:
            return ExpressOrderFactory()
        else:
            return RegularOrderFactory()


 