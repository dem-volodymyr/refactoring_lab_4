from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.dish import Dish
from app.services.menu_service import MenuService

router = APIRouter(prefix="/dishes", tags=["dishes"])
menu_service = MenuService()


class DishCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None


@router.post("/", response_model=Dish)
def create_dish(dish: DishCreate):
    """Create a new dish."""
    return menu_service.add_dish(
        name=dish.name,
        price=dish.price,
        description=dish.description,
        category=dish.category
    )


@router.get("/", response_model=List[Dish])
def get_all_dishes():
    """Get all dishes."""
    return menu_service.get_all_dishes()


@router.get("/{dish_id}", response_model=Dish)
def get_dish(dish_id: UUID):
    """Get a dish by ID."""
    dish = menu_service.get_dish(dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@router.get("/category/{category}", response_model=List[Dish])
def get_dishes_by_category(category: str):
    """Get all dishes in a category."""
    return menu_service.get_dishes_by_category(category) 