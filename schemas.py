from typing import List, Optional
from pydantic import BaseModel

# USER
class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        from_attributes = True

# MENU
class MenuItemCreate(BaseModel):
    name: str
    price: float
    image: Optional[str] = None
    description: Optional[str] = None

class MenuItemResponse(MenuItemCreate):
    id: int
    name:str
    price:float
    image: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# CART
class CartItemCreate(BaseModel):
    item_id: int
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    item_id: int
    quantity: int

    class Config:
        from_attributes = True


# ORDER
class OrderItem(BaseModel):
    item_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    order_type: Optional[str] = None
    address: Optional[str] = None
    seat_number: Optional[str] = None
    items: List[OrderItem]


class OrderResponse(BaseModel):
    id: int
    total: float
    status: str
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    order_type: Optional[str] = None
    address: Optional[str] = None
    seat_number: Optional[str] = None

    class Config:
        from_attributes = True