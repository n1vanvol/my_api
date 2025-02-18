from pydantic import BaseModel
from typing import Optional

class Products(BaseModel):
    id: int
    name: str
    price: int
    category: str
    brand: str


class PostProducts(BaseModel):
    name: str
    price: int
    category: str
    brand: str