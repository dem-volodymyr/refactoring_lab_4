import pytest
from uuid import UUID

from app.models.dish import Dish


def test_dish_creation():
    """Test dish creation with required fields."""
    dish = Dish(name="Pizza", price=12.99)
    assert dish.name == "Pizza"
    assert dish.price == 12.99
    assert isinstance(dish.id, UUID)
    assert dish.description is None
    assert dish.category is None


def test_dish_creation_with_optional_fields():
    """Test dish creation with optional fields."""
    dish = Dish(
        name="Pasta",
        price=10.99,
        description="Delicious pasta with tomato sauce",
        category="Main Course"
    )
    assert dish.name == "Pasta"
    assert dish.price == 10.99
    assert dish.description == "Delicious pasta with tomato sauce"
    assert dish.category == "Main Course"


def test_dish_equality():
    """Test that two dishes with the same ID are considered equal."""
    dish1 = Dish(name="Pizza", price=12.99)
    dish2 = Dish(name="Pizza", price=12.99)
    
    # Two different dish objects should have different IDs
    assert dish1 != dish2
    
    # Copy the ID to create equal dishes
    dish2.id = dish1.id
    assert dish1 == dish2
    
    # A dish should not be equal to a non-dish object
    assert dish1 != "not a dish" 