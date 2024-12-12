from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text, Date
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = "Customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    # contact_mech = relationship("ContactMech", back_populates="Customer")

class ContactMech(Base):
    __tablename__ = "Contact_Mech"

    contact_mech_id = Column(Integer, primary_key=True, index=True)
    street_address = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    postal_code = Column(String(20), nullable=False)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    customer_id = Column(Integer, ForeignKey("Customer.customer_id"), nullable=False)
    # customer = relationship("Customer", back_populates="ContactMech")


class Product(Base):
    __tablename__ = "Product"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    color = Column(String(30), nullable=True)
    size = Column(String(10), nullable=True)


class Order_Header(Base):
    __tablename__ = "Order_Header"

    order_id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date, nullable=False)

    customer_id = Column(Integer, ForeignKey("Customer.customer_id"), nullable=False)
    shipping_contact_mech_id = Column(Integer, ForeignKey("Contact_Mech.contact_mech_id"), nullable=False)
    billing_contact_mech_id = Column(Integer, ForeignKey("Contact_Mech.contact_mech_id"), nullable=False)

    Order_Items = relationship("Order_Items", back_populates="Order_Header")

    __allow_unmapped__ = True

class Order_Items(Base):
    __tablename__ = "Order_Items"

    order_item_seq_id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)

    order_id = Column(Integer, ForeignKey("Order_Header.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Product.product_id"), nullable=False)

    Order_Header = relationship("Order_Header", back_populates="Order_Items")
    # product = relationship("Product", back_populates="Order_Items")

    __allow_unmapped__ = True