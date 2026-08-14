from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"



    id = Column(Integer, primary_key=True, index=True, autoincrement=True)



    name = Column(String)



    email = Column(String)



    status = Column(String)




class Customercreate(Base):
    __tablename__ = "customer_creates"



    id = Column(Integer, primary_key=True, index=True, autoincrement=True)



    name = Column(String, nullable=False)



    email = Column(String, nullable=False)




class Customerstatus(Base):
    __tablename__ = "customer_statuss"



    id = Column(Integer, primary_key=True, index=True, autoincrement=True)




class Product(Base):
    __tablename__ = "products"



    id = Column(Integer, primary_key=True, index=True, autoincrement=True)



    name = Column(String)



    price = Column(Float)




class Ordercreate(Base):
    __tablename__ = "order_creates"



    id = Column(Integer, primary_key=True, index=True, autoincrement=True)



    customer_id = Column(Integer, nullable=False)



    items = Column(JSON, nullable=False)




class Orderitem(Base):
    __tablename__ = "order_items"



    id = Column(Integer, primary_key=True, index=True, autoincrement=True)



    product_id = Column(Integer, nullable=False)



    quantity = Column(Integer, nullable=False)
