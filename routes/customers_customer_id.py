from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db

router = APIRouter()


@router.get("/customers/{customer_id}")
def get_customers_customer_id(customer_id, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer is None:
            return JSONResponse(status_code=404, content={"error": "Customer not found"})
        return {"id": customer.id, "name": customer.name, "email": customer.email}

