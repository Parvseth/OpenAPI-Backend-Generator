from pydantic import BaseModel

class CustomerCreate(BaseModel):

    name: string

    email: string
