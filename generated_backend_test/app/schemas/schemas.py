from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Customer Schemas
# ==========================================

class CustomerBase(BaseModel):



    name: Optional[str] = None

    email: Optional[str] = None

    status: Optional[str] = None



class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):


    name: Optional[str] = None

    email: Optional[str] = None

    status: Optional[str] = None



class CustomerResponse(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Customercreate Schemas
# ==========================================

class CustomercreateBase(BaseModel):



    name: str

    email: str



class CustomercreateCreate(CustomercreateBase):
    pass

class CustomercreateUpdate(BaseModel):


    name: Optional[str] = None

    email: Optional[str] = None



class CustomercreateResponse(CustomercreateBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Customerstatus Schemas
# ==========================================

class CustomerstatusBase(BaseModel):


    pass


class CustomerstatusCreate(CustomerstatusBase):
    pass

class CustomerstatusUpdate(BaseModel):

    pass


class CustomerstatusResponse(CustomerstatusBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Product Schemas
# ==========================================

class ProductBase(BaseModel):



    name: Optional[str] = None

    price: Optional[float] = None



class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):


    name: Optional[str] = None

    price: Optional[float] = None



class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Ordercreate Schemas
# ==========================================

class OrdercreateBase(BaseModel):



    customer_id: int

    items: List[Dict[str, Any]]



class OrdercreateCreate(OrdercreateBase):
    pass

class OrdercreateUpdate(BaseModel):


    customer_id: Optional[int] = None

    items: Optional[List[Dict[str, Any]]] = None



class OrdercreateResponse(OrdercreateBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Orderitem Schemas
# ==========================================

class OrderitemBase(BaseModel):



    product_id: int

    quantity: int



class OrderitemCreate(OrderitemBase):
    pass

class OrderitemUpdate(BaseModel):


    product_id: Optional[int] = None

    quantity: Optional[int] = None



class OrderitemResponse(OrderitemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
