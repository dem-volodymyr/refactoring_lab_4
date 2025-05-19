from datetime import datetime
from enum import Enum
from typing import List, Set
from uuid import UUID, uuid4

from app.models.dish import Dish
from app.models.interfaces import OrderObserver, OrderSubject


class OrderStatus(Enum):
    CREATED = "created"
    PROCESSING = "processing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(OrderSubject):
    """
    Represents a customer order.
    Implements the Observer pattern to notify interested parties of order status changes.
    """
    
    def __init__(self, customer_id: UUID, dishes: List[Dish]):
        self.id: UUID = uuid4()
        self.customer_id: UUID = customer_id
        self.dishes: List[Dish] = dishes.copy()
        self.status: OrderStatus = OrderStatus.CREATED
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = self.created_at
        self._observers: Set[OrderObserver] = set()
        
    def attach(self, observer: OrderObserver) -> None:
        """Attach an observer to this order."""
        self._observers.add(observer)
        
    def detach(self, observer: OrderObserver) -> None:
        """Detach an observer from this order."""
        self._observers.discard(observer)
        
    def notify(self) -> None:
        """Notify all observers of a status change."""
        for observer in self._observers:
            observer.update(self.id)
            
    def update_status(self, status: OrderStatus) -> None:
        """Update the status of this order and notify observers."""
        self.status = status
        self.updated_at = datetime.now()
        self.notify()
        
    def calculate_total(self) -> float:
        """Calculate the total price of this order."""
        return sum(dish.price for dish in self.dishes)
        
    def add_dish(self, dish: Dish) -> None:
        """Add a dish to this order."""
        self.dishes.append(dish)
        self.updated_at = datetime.now()
        
    def remove_dish(self, dish_id: UUID) -> bool:
        """Remove a dish from this order by its ID."""
        for i, dish in enumerate(self.dishes):
            if dish.id == dish_id:
                self.dishes.pop(i)
                self.updated_at = datetime.now()
                return True
        return False 