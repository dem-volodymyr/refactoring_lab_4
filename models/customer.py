from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4


class Customer(BaseModel):
    """Represents a customer who places orders."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None 