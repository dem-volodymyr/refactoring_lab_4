import pytest
from uuid import uuid4

from app.models.dish import Dish
from app.models.menu import Menu


def test_empty_menu():
    """Test that a new menu is empty."""
    menu = Menu()
    assert len(menu.get_all_dishes()) == 0


def test_add_dish_to_menu():
    """Test adding a dish to the menu."""
    menu = Menu()
    dish = Dish(name="Pizza", price=12.99)
    
    menu.add_dish(dish)
    assert menu.contains_dish(dish)
    assert len(menu.get_all_dishes()) == 1


def test_add_duplicate_dish_to_menu():
    """Test that adding a duplicate dish doesn't actually add it twice."""
    menu = Menu()
    dish = Dish(name="Pizza", price=12.99)
    
    menu.add_dish(dish)
    menu.add_dish(dish)  # Try to add the same dish again
    
    assert len(menu.get_all_dishes()) == 1


def test_remove_dish_from_menu():
    """Test removing a dish from the menu."""
    menu = Menu()
    dish = Dish(name="Pizza", price=12.99)
    
    menu.add_dish(dish)
    assert menu.contains_dish(dish)
    
    result = menu.remove_dish(dish.id)
    assert result is True
    assert not menu.contains_dish(dish)
    assert len(menu.get_all_dishes()) == 0


def test_remove_nonexistent_dish_from_menu():
    """Test attempting to remove a dish that doesn't exist in the menu."""
    menu = Menu()
    result = menu.remove_dish(uuid4())
    assert result is False


def test_get_dish_by_id():
    """Test getting a dish by ID."""
    menu = Menu()
    dish = Dish(name="Pizza", price=12.99)
    
    menu.add_dish(dish)
    
    retrieved_dish = menu.get_dish(dish.id)
    assert retrieved_dish is not None
    assert retrieved_dish == dish


def test_get_nonexistent_dish_by_id():
    """Test attempting to get a dish that doesn't exist in the menu."""
    menu = Menu()
    retrieved_dish = menu.get_dish(uuid4())
    assert retrieved_dish is None


def test_get_dishes_by_category():
    """Test getting dishes by category."""
    menu = Menu()
    
    appetizer1 = Dish(name="Garlic Bread", price=5.99, category="Appetizer")
    appetizer2 = Dish(name="Bruschetta", price=7.99, category="Appetizer")
    main_course = Dish(name="Pizza", price=12.99, category="Main Course")
    
    menu.add_dish(appetizer1)
    menu.add_dish(appetizer2)
    menu.add_dish(main_course)
    
    appetizers = menu.get_dishes_by_category("Appetizer")
    assert len(appetizers) == 2
    assert appetizer1 in appetizers
    assert appetizer2 in appetizers
    
    main_courses = menu.get_dishes_by_category("Main Course")
    assert len(main_courses) == 1
    assert main_course in main_courses
    
    desserts = menu.get_dishes_by_category("Dessert")
    assert len(desserts) == 0 