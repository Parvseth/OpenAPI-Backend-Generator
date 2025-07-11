from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db

router = APIRouter()


@router.post("/orders")
def post_orders(db: Session = Depends(get_db)):
    data = await request.json()
        customer = db.query(Customer).filter(Customer.id == data["customer_id"]).first()
        if not customer:
            return JSONResponse(status_code=404, content={"message": "Customer not found"})
        product = db.query(Product).filter(Product.id == data["product_id"]).first()
        if not product:
            return JSONResponse(status_code=404, content={"message": "Product not found"})
        order = Order(customer_id=data["customer_id"], product_id=data["product_id"], quantity=data["quantity"])
        db.add(order)
        db.commit()
        db.refresh(order)
        return JSONResponse(status_code=201, content={"id": order.id, "customer_id": order.customer_id, "product_id": order.product_id, "quantity": order.quantity})

