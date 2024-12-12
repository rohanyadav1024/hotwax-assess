# This file contains the Pydantic models for the FastAPI application
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime, time

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    status: str

    class Config:
        orm_mode = True

class UpdateOrderItem(BaseModel):
    quantity: Optional[int] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True

class Order(BaseModel):
    order_date: date
    customer_id: int
    shipping_contact_mech_id: int
    billing_contact_mech_id: int
    order_items: List[OrderItem]

    class Config:
        orm_mode = True


class ShippingDetails(BaseModel):
    street_address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None

class BillingDetails(BaseModel):
    street_address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None


class UpdateOrder(BaseModel):
    shipping_id: Optional[int] = None
    billing_id: Optional[int] = None
    shipping_details: Optional[ShippingDetails] = None
    billing_details: Optional[BillingDetails] = None

    class Config:
        orm_mode = True