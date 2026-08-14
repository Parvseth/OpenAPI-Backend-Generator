from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.services.customerstatus_service import CustomerstatusService

router = APIRouter(prefix="/customer_statuss", tags=["Customerstatus"])

@router.get("/", response_model=List[schemas.CustomerstatusResponse])
def list_customer_statuss(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List all customer_statuss with pagination."""
    service = CustomerstatusService(db)
    return service.get_all(skip=skip, limit=limit)

@router.post("/", response_model=schemas.CustomerstatusResponse, status_code=status.HTTP_201_CREATED)
def create_customerstatus(
    payload: schemas.CustomerstatusCreate,
    db: Session = Depends(get_db)
):
    """Create a new Customerstatus."""
    service = CustomerstatusService(db)
    return service.create(payload)

@router.get("/{item_id}", response_model=schemas.CustomerstatusResponse)
def get_customerstatus(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get a Customerstatus by ID."""
    service = CustomerstatusService(db)
    return service.get_by_id(item_id)

@router.put("/{item_id}", response_model=schemas.CustomerstatusResponse)
def update_customerstatus(
    item_id: int,
    payload: schemas.CustomerstatusUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing Customerstatus."""
    service = CustomerstatusService(db)
    return service.update(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_customerstatus(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete a Customerstatus."""
    service = CustomerstatusService(db)
    return service.delete(item_id)
