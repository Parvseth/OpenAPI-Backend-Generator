from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db

router = APIRouter()


@router.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
        response = [{"id": customer.id, "name": customer.name, "email": customer.email} for customer in customers]
        return {"customers": response}


@router.post("/customers")
def post_customers(db: Session = Depends(get_db)):
    data = await request.json()
        customer = Customer(**data)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return {"id": customer.id, "name": customer.name, "email": customer.email}

