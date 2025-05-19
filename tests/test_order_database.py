import pytest

from app.models.customer import Customer
from app.models.dish import Dish
from app.models.order import Order
from app.services.order_database import OrderDatabase


def test_singleton_pattern():
    """Test that OrderDatabase follows the Singleton pattern."""
    db1 = OrderDatabase()
    db2 = OrderDatabase()
    
    # Both variables should reference the same object
    assert db1 is db2


def test_orders_crud():
    """Test CRUD operations for orders."""
    db = OrderDatabase()
    
    # Reset state between tests
    db._initialize()
    
    # Create a customer and dishes
    customer = Customer(name="John Doe", email="john@example.com")
    dish1 = Dish(name="Pizza", price=12.99)
    dish2 = Dish(name="Salad", price=8.99)
    
    # Create an order
    order = Order(customer.id, [dish1, dish2])
    
    # Add the order to the database
    db.add_order(order)
    
    # Get the order from the database
    retrieved_order = db.get_order(order.id)
    assert retrieved_order is not None
    assert retrieved_order.id == order.id
    
    # Get all orders
    all_orders = db.get_all_orders()
    assert len(all_orders) == 1
    assert all_orders[0].id == order.id
    
    # Update the order
    order.add_dish(Dish(name="Soda", price=2.49))
    db.update_order(order)
    
    updated_order = db.get_order(order.id)
    assert len(updated_order.dishes) == 3
    
    # Delete the order
    result = db.delete_order(order.id)
    assert result is True
    assert db.get_order(order.id) is None
    assert len(db.get_all_orders()) == 0
    
    # Try to delete a non-existent order
    result = db.delete_order(order.id)
    assert result is False


def test_customers_crud():
    """Test CRUD operations for customers."""
    db = OrderDatabase()
    
    # Reset state between tests
    db._initialize()
    
    # Create a customer
    customer = Customer(name="John Doe", email="john@example.com")
    
    # Add the customer to the database
    db.add_customer(customer)
    
    # Get the customer from the database
    retrieved_customer = db.get_customer(customer.id)
    assert retrieved_customer is not None
    assert retrieved_customer.id == customer.id
    
    # Get all customers
    all_customers = db.get_all_customers()
    assert len(all_customers) == 1
    assert all_customers[0].id == customer.id


def test_menu_operations():
    """Test operations for the menu."""
    db = OrderDatabase()
    
    # Reset state between tests
    db._initialize()
    
    # Get the menu
    menu = db.get_menu()
    assert menu is not None
    assert len(menu.get_all_dishes()) == 0
    
    # Add a dish to the menu
    dish = Dish(name="Pizza", price=12.99)
    db.add_dish_to_menu(dish)
    
    # Check that the dish was added
    assert len(menu.get_all_dishes()) == 1
    assert menu.contains_dish(dish) 