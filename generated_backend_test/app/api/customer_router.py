from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customer"])

@router.get("/", response_model=List[schemas.CustomerResponse])
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List all customers with pagination."""
    service = CustomerService(db)
    return service.get_all(skip=skip, limit=limit)

@router.post("/", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    """Create a new Customer."""
    service = CustomerService(db)
    return service.create(payload)

@router.get("/{item_id}", response_model=schemas.CustomerResponse)
def get_customer(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get a Customer by ID."""
    service = CustomerService(db)
    return service.get_by_id(item_id)

@router.put("/{item_id}", response_model=schemas.CustomerResponse)
def update_customer(
    item_id: int,
    payload: schemas.CustomerUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing Customer."""
    service = CustomerService(db)
    return service.update(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_customer(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete a Customer."""
    service = CustomerService(db)
    return service.delete(item_id)
