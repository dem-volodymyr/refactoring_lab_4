import pytest
from uuid import UUID, uuid4
from datetime import datetime

from app.models.dish import Dish
from app.models.interfaces import OrderObserver
from app.models.order import Order, OrderStatus


class MockOrderObserver(OrderObserver):
    """Mock observer for testing the Observer pattern."""
    
    def __init__(self):
        self.updated_order_ids = []
        
    def update(self, order_id: UUID) -> None:
        """Record that this observer was notified about the given order."""
        self.updated_order_ids.append(order_id)


def test_order_creation():
    """Test order creation."""
    customer_id = uuid4()
    dishes = [
        Dish(name="Pizza", price=12.99),
        Dish(name="Salad", price=8.99)
    ]
    
    order = Order(customer_id, dishes)
    
    assert order.customer_id == customer_id
    assert len(order.dishes) == 2
    assert order.status == OrderStatus.CREATED
    assert isinstance(order.id, UUID)
    assert isinstance(order.created_at, datetime)
    assert order.updated_at == order.created_at


def test_calculate_total():
    """Test calculating the total price of an order."""
    customer_id = uuid4()
    dishes = [
        Dish(name="Pizza", price=12.99),
        Dish(name="Salad", price=8.99),
        Dish(name="Soda", price=2.49)
    ]
    
    order = Order(customer_id, dishes)
    
    # Check that the total is the sum of the dish prices
    assert order.calculate_total() == pytest.approx(12.99 + 8.99 + 2.49)


def test_add_dish():
    """Test adding a dish to an order."""
    customer_id = uuid4()
    dishes = [Dish(name="Pizza", price=12.99)]
    
    order = Order(customer_id, dishes)
    original_updated_at = order.updated_at
    
    # Add a new dish
    new_dish = Dish(name="Salad", price=8.99)
    order.add_dish(new_dish)
    
    assert len(order.dishes) == 2
    assert new_dish in order.dishes
    assert order.updated_at > original_updated_at


def test_remove_dish():
    """Test removing a dish from an order."""
    customer_id = uuid4()
    dish1 = Dish(name="Pizza", price=12.99)
    dish2 = Dish(name="Salad", price=8.99)
    dishes = [dish1, dish2]
    
    order = Order(customer_id, dishes)
    original_updated_at = order.updated_at
    
    # Remove a dish
    result = order.remove_dish(dish1.id)
    
    assert result is True
    assert len(order.dishes) == 1
    assert dish1 not in order.dishes
    assert dish2 in order.dishes
    assert order.updated_at > original_updated_at


def test_remove_nonexistent_dish():
    """Test attempting to remove a dish that isn't in the order."""
    customer_id = uuid4()
    dishes = [Dish(name="Pizza", price=12.99)]
    
    order = Order(customer_id, dishes)
    original_updated_at = order.updated_at
    
    # Try to remove a dish that isn't in the order
    result = order.remove_dish(uuid4())
    
    assert result is False
    assert len(order.dishes) == 1
    assert order.updated_at == original_updated_at


def test_observer_pattern():
    """Test the Observer pattern implementation."""
    customer_id = uuid4()
    dishes = [Dish(name="Pizza", price=12.99)]
    
    order = Order(customer_id, dishes)
    
    # Create and attach observers
    observer1 = MockOrderObserver()
    observer2 = MockOrderObserver()
    
    order.attach(observer1)
    order.attach(observer2)
    
    # Notify observers
    order.notify()
    
    # Check that both observers were notified
    assert len(observer1.updated_order_ids) == 1
    assert observer1.updated_order_ids[0] == order.id
    assert len(observer2.updated_order_ids) == 1
    assert observer2.updated_order_ids[0] == order.id
    
    # Detach an observer and notify again
    order.detach(observer1)
    order.notify()
    
    # Check that only the attached observer was notified again
    assert len(observer1.updated_order_ids) == 1  # No change
    assert len(observer2.updated_order_ids) == 2


def test_update_status():
    """Test updating the status of an order."""
    customer_id = uuid4()
    dishes = [Dish(name="Pizza", price=12.99)]
    
    order = Order(customer_id, dishes)
    observer = MockOrderObserver()
    order.attach(observer)
    
    original_updated_at = order.updated_at
    
    # Update status
    order.update_status(OrderStatus.PROCESSING)
    
    assert order.status == OrderStatus.PROCESSING
    assert order.updated_at > original_updated_at
    assert len(observer.updated_order_ids) == 1
    assert observer.updated_order_ids[0] == order.id