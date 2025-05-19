import pytest
from uuid import uuid4

from app.models.dish import Dish
from app.models.order import Order
from app.services.order_factory import (
    OrderType,
    RegularOrderFactory,
    BulkOrderFactory,
    ExpressOrderFactory,
    OrderFactoryProvider
)


def test_regular_order_factory():
    """Test the RegularOrderFactory."""
    factory = RegularOrderFactory()
    customer_id = uuid4()
    dishes = [Dish(name="Pizza", price=12.99)]
    
    order = factory.create_order(customer_id, dishes)
    
    assert isinstance(order, Order)
    assert order.customer_id == customer_id
    assert len(order.dishes) == 1
    assert order.dishes[0].name == "Pizza"


def test_bulk_order_factory():
    """Test the BulkOrderFactory."""
    factory = BulkOrderFactory()
    customer_id = uuid4()
    dishes = [
        Dish(name="Pizza", price=12.99),
        Dish(name="Pasta", price=10.99),
        Dish(name="Salad", price=8.99)
    ]
    
    order = factory.create_order(customer_id, dishes)
    
    assert isinstance(order, Order)
    assert order.customer_id == customer_id
    assert len(order.dishes) == 3


def test_express_order_factory():
    """Test the ExpressOrderFactory."""
    factory = ExpressOrderFactory()
    customer_id = uuid4()
    dishes = [Dish(name="Pizza", price=12.99)]
    
    order = factory.create_order(customer_id, dishes)
    
    assert isinstance(order, Order)
    assert order.customer_id == customer_id
    assert len(order.dishes) == 1


def test_order_factory_provider_regular():
    """Test the OrderFactoryProvider with regular order type."""
    factory = OrderFactoryProvider.get_factory(OrderType.REGULAR)
    assert isinstance(factory, RegularOrderFactory)


def test_order_factory_provider_bulk():
    """Test the OrderFactoryProvider with bulk order type."""
    factory = OrderFactoryProvider.get_factory(OrderType.BULK)
    assert isinstance(factory, BulkOrderFactory)


def test_order_factory_provider_express():
    """Test the OrderFactoryProvider with express order type."""
    factory = OrderFactoryProvider.get_factory(OrderType.EXPRESS)
    assert isinstance(factory, ExpressOrderFactory) 