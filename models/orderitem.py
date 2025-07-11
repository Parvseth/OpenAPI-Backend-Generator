from pydantic import BaseModel

class OrderItem(BaseModel):

    product_id: integer

    quantity: integer
