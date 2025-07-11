from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db

router = APIRouter()


@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
        response = [{"id": product.id, "name": product.name, "price": product.price} for product in products]
        return {"products": response}

