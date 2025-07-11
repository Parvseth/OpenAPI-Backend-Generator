from pydantic import BaseModel

class Customer(BaseModel):

    id: integer

    name: string

    email: string

    status: str
