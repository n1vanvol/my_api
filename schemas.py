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


class ProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    category: str | None = None
    brand: str | None = None
