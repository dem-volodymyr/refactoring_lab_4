from typing import List, Optional
from uuid import UUID

from app.models.customer import Customer
from app.services.order_database import OrderDatabase


class CustomerService:
    """
    Service for managing customers.
    Follows the Single Responsibility Principle by focusing only on customer operations.
    """
    
    def __init__(self):
        self.db = OrderDatabase()
        
    def create_customer(self, name: str, email: str, phone: Optional[str] = None, address: Optional[str] = None) -> Customer:
        """Create a new customer."""
        customer = Customer(name=name, email=email, phone=phone, address=address)
        self.db.add_customer(customer)
        return customer
        
    def get_customer(self, customer_id: UUID) -> Optional[Customer]:
        """Get a customer by ID."""
        return self.db.get_customer(customer_id)
        
    def get_all_customers(self) -> List[Customer]:
        """Get all customers."""
        return self.db.get_all_customers() 