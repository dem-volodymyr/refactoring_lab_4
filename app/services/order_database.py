from typing import Dict, List, Optional
from uuid import UUID

from app.models.customer import Customer
from app.models.dish import Dish
from app.models.menu import Menu
from app.models.order import Order


class OrderDatabase:
    """
    Singleton database for storing orders, customers, and the menu.
    Ensures that there is only one instance of the database throughout the application.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OrderDatabase, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self):
        """Initialize the database."""
        self._orders: Dict[UUID, Order] = {}
        self._customers: Dict[UUID, Customer] = {}
        self._menu = Menu()
        
    # Order methods
    def add_order(self, order: Order) -> None:
        """Add an order to the database."""
        self._orders[order.id] = order
        
    def get_order(self, order_id: UUID) -> Optional[Order]:
        """Get an order by ID."""
        return self._orders.get(order_id)
        
    def get_all_orders(self) -> List[Order]:
        """Get all orders."""
        return list(self._orders.values())
        
    def update_order(self, order: Order) -> bool:
        """Update an existing order."""
        if order.id in self._orders:
            self._orders[order.id] = order
            return True
        return False
        
    def delete_order(self, order_id: UUID) -> bool:
        """Delete an order by ID."""
        if order_id in self._orders:
            del self._orders[order_id]
            return True
        return False
            
    # Customer methods
    def add_customer(self, customer: Customer) -> None:
        """Add a customer to the database."""
        self._customers[customer.id] = customer
        
    def get_customer(self, customer_id: UUID) -> Optional[Customer]:
        """Get a customer by ID."""
        return self._customers.get(customer_id)
        
    def get_all_customers(self) -> List[Customer]:
        """Get all customers."""
        return list(self._customers.values())
        
    # Menu methods
    def get_menu(self) -> Menu:
        """Get the menu."""
        return self._menu
        
    def add_dish_to_menu(self, dish: Dish) -> None:
        """Add a dish to the menu."""
        self._menu.add_dish(dish) 