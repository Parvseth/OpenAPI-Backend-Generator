from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.services.orderitem_service import OrderitemService

router = APIRouter(prefix="/order_items", tags=["Orderitem"])

@router.get("/", response_model=List[schemas.OrderitemResponse])
def list_order_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List all order_items with pagination."""
    service = OrderitemService(db)
    return service.get_all(skip=skip, limit=limit)

@router.post("/", response_model=schemas.OrderitemResponse, status_code=status.HTTP_201_CREATED)
def create_orderitem(
    payload: schemas.OrderitemCreate,
    db: Session = Depends(get_db)
):
    """Create a new Orderitem."""
    service = OrderitemService(db)
    return service.create(payload)

@router.get("/{item_id}", response_model=schemas.OrderitemResponse)
def get_orderitem(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get a Orderitem by ID."""
    service = OrderitemService(db)
    return service.get_by_id(item_id)

@router.put("/{item_id}", response_model=schemas.OrderitemResponse)
def update_orderitem(
    item_id: int,
    payload: schemas.OrderitemUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing Orderitem."""
    service = OrderitemService(db)
    return service.update(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_orderitem(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete a Orderitem."""
    service = OrderitemService(db)
    return service.delete(item_id)
