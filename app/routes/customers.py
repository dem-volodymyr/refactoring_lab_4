from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from app.models.customer import Customer
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])
customer_service = CustomerService()


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None


@router.post("/", response_model=Customer)
def create_customer(customer: CustomerCreate):
    """Create a new customer."""
    return customer_service.create_customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )


@router.get("/", response_model=List[Customer])
def get_all_customers():
    """Get all customers."""
    return customer_service.get_all_customers()


@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: UUID):
    """Get a customer by ID."""
    customer = customer_service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer 