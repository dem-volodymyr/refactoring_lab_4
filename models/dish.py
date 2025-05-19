from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4


class Dish(BaseModel):
    """Represents a dish in the restaurant menu."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None
    
    def __eq__(self, other):
        if not isinstance(other, Dish):
            return False
        return self.id == other.id 