from uuid import UUID

from app.models.interfaces import OrderObserver
from app.services.order_service import OrderService


class KitchenNotifier(OrderObserver):
    """
    Service responsible for notifying the kitchen about new orders.
    Implements the Observer pattern to react to order status changes.
    """
    
    def __init__(self, order_service: OrderService):
        self.order_service = order_service
        
    def update(self, order_id: UUID) -> None:
        """
        Called when an order's status changes.
        If the order is new, notify the kitchen.
        """
        order = self.order_service.get_order(order_id)
        if order and order.status.value == "created":
            # In a real application, this could send a notification to a kitchen display system
            print(f"KITCHEN NOTIFICATION: New order {order_id} received!")
            print(f"Order details: {len(order.dishes)} dishes, total: ${order.calculate_total():.2f}")
            
    def notify_order_ready(self, order_id: UUID) -> None:
        """Notify that an order is ready for delivery."""
        order = self.order_service.get_order(order_id)
        if order:
            print(f"KITCHEN NOTIFICATION: Order {order_id} is ready for delivery!") 