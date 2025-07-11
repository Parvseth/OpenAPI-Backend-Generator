from pydantic import BaseModel

class Product(BaseModel):

    id: integer

    name: string

    price: number
