from abc import ABC, abstractmethod
from typing import Any, List
from uuid import UUID

from app.models.dish import Dish


class OrderObserver(ABC):
    """Interface for classes that need to be notified of order events."""
    
    @abstractmethod
    def update(self, order_id: UUID) -> None:
        """Called when an order status changes."""
        pass


class OrderSubject(ABC):
    """Interface for classes that can notify observers of order events."""
    
    @abstractmethod
    def attach(self, observer: OrderObserver) -> None:
        """Attach an observer to this subject."""
        pass
        
    @abstractmethod
    def detach(self, observer: OrderObserver) -> None:
        """Detach an observer from this subject."""
        pass
        
    @abstractmethod
    def notify(self) -> None:
        """Notify all observers of an event."""
        pass


class OrderFactory(ABC):
    """Interface for factories that create orders."""
    
    @abstractmethod
    def create_order(self, customer_id: UUID, dishes: List[Dish]) -> Any:
        """Create a new order."""
        pass 