from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.order import Order, OrderStatus
from app.services.kitchen_notifier import KitchenNotifier
from app.services.order_factory import OrderType
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])
order_service = OrderService()
kitchen_notifier = KitchenNotifier(order_service)


class OrderCreate(BaseModel):
    customer_id: UUID
    dish_ids: List[UUID]
    order_type: Optional[str] = OrderType.REGULAR.value


class OrderStatusUpdate(BaseModel):
    status: str


@router.post("/", response_model=dict)
def create_order(order: OrderCreate):
    """Create a new order."""
    try:
        # Convert string order type to enum
        order_type = OrderType(order.order_type)
        
        # Create the order
        new_order = order_service.create_order(
            customer_id=order.customer_id,
            dish_ids=order.dish_ids,
            order_type=order_type
        )
        
        # Attach kitchen notifier to the order
        new_order.attach(kitchen_notifier)
        
        # Notify observers (kitchen)
        new_order.notify()
        
        return {
            "id": new_order.id,
            "status": new_order.status.value,
            "total": new_order.calculate_total()
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid order type: {order.order_type}")


@router.get("/", response_model=List[dict])
def get_all_orders():
    """Get all orders."""
    orders = order_service.get_all_orders()
    return [
        {
            "id": order.id,
            "customer_id": order.customer_id,
            "status": order.status.value,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "total": order.calculate_total(),
            "dish_count": len(order.dishes)
        }
        for order in orders
    ]


@router.get("/{order_id}", response_model=dict)
def get_order(order_id: UUID):
    """Get an order by ID."""
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "status": order.status.value,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "dishes": order.dishes,
        "total": order.calculate_total()
    }


@router.patch("/{order_id}/status", response_model=dict)
def update_order_status(order_id: UUID, status_update: OrderStatusUpdate):
    """Update an order's status."""
    try:
        new_status = OrderStatus(status_update.status)
        success = order_service.update_order_status(order_id, new_status)
        
        if not success:
            raise HTTPException(status_code=404, detail="Order not found")
            
        return {"id": order_id, "status": new_status.value}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status_update.status}")


@router.post("/{order_id}/dishes/{dish_id}", response_model=dict)
def add_dish_to_order(order_id: UUID, dish_id: UUID):
    """Add a dish to an order."""
    success = order_service.add_dish_to_order(order_id, dish_id)
    
    if not success:
        raise HTTPException(
            status_code=400, 
            detail="Could not add dish to order. Order may not exist, dish may not exist, or order status may not allow modifications."
        )
        
    order = order_service.get_order(order_id)
    return {
        "id": order_id,
        "total": order.calculate_total(),
        "dish_count": len(order.dishes)
    }


@router.delete("/{order_id}/dishes/{dish_id}", response_model=dict)
def remove_dish_from_order(order_id: UUID, dish_id: UUID):
    """Remove a dish from an order."""
    success = order_service.remove_dish_from_order(order_id, dish_id)
    
    if not success:
        raise HTTPException(
            status_code=400, 
            detail="Could not remove dish from order. Order may not exist, dish may not be in the order, or order status may not allow modifications."
        )
        
    order = order_service.get_order(order_id)
    return {
        "id": order_id,
        "total": order.calculate_total(),
        "dish_count": len(order.dishes)
    } 