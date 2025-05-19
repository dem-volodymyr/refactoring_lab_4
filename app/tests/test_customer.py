import pytest
from uuid import UUID

from app.models.customer import Customer


def test_customer_creation():
    """Test customer creation with required fields."""
    customer = Customer(name="John Doe", email="john@example.com")
    assert customer.name == "John Doe"
    assert customer.email == "john@example.com"
    assert isinstance(customer.id, UUID)
    assert customer.phone is None
    assert customer.address is None


def test_customer_creation_with_optional_fields():
    """Test customer creation with optional fields."""
    customer = Customer(
        name="Jane Smith",
        email="jane@example.com",
        phone="555-1234",
        address="123 Main St, Anytown, USA"
    )
    assert customer.name == "Jane Smith"
    assert customer.email == "jane@example.com"
    assert customer.phone == "555-1234"
    assert customer.address == "123 Main St, Anytown, USA" 