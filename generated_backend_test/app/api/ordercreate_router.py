from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.services.ordercreate_service import OrdercreateService

router = APIRouter(prefix="/order_creates", tags=["Ordercreate"])

@router.get("/", response_model=List[schemas.OrdercreateResponse])
def list_order_creates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List all order_creates with pagination."""
    service = OrdercreateService(db)
    return service.get_all(skip=skip, limit=limit)

@router.post("/", response_model=schemas.OrdercreateResponse, status_code=status.HTTP_201_CREATED)
def create_ordercreate(
    payload: schemas.OrdercreateCreate,
    db: Session = Depends(get_db)
):
    """Create a new Ordercreate."""
    service = OrdercreateService(db)
    return service.create(payload)

@router.get("/{item_id}", response_model=schemas.OrdercreateResponse)
def get_ordercreate(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get a Ordercreate by ID."""
    service = OrdercreateService(db)
    return service.get_by_id(item_id)

@router.put("/{item_id}", response_model=schemas.OrdercreateResponse)
def update_ordercreate(
    item_id: int,
    payload: schemas.OrdercreateUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing Ordercreate."""
    service = OrdercreateService(db)
    return service.update(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_ordercreate(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete a Ordercreate."""
    service = OrdercreateService(db)
    return service.delete(item_id)
