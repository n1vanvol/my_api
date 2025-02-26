from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
class Products(BaseModel):
    id: int
    name: str
    price: int
    category: str
    brand: str
    
    class Config:
        from_attributes = True


class PostProducts(BaseModel):
    name: str
    price: int
    category: str
    brand: str
    
    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    category: str | None = None
    brand: str | None = None



class User(BaseModel):
    
    email: EmailStr
    password: str

    class Config:
        from_attributes = True



class UserInfo(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserIn(BaseModel):
    sub: str


class Token(BaseModel):
    access_token: str
    token_type: str