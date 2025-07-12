from pydantic import BaseModel
from uuid import UUID, uuid4


class Product(BaseModel):
    id: UUID
    name: str
    description: str

    def __repr__(self):
        return f"ID: {self.id} | Name: {self.name} | Description: {self.description}"

    def __str__(self):
        return f"ID: {self.id} | Name: {self.name} | Description: {self.description}"


class Offer(BaseModel):
    id: UUID
    price: int
    items_in_stock: int

    def __repr__(self):
        return f"ID: {self.id} | Price: {self.price} | In stock: {self.items_in_stock}"
    
    def __str__(self):
        return f"ID: {self.id} | Price: {self.price} | In stock: {self.items_in_stock}"
