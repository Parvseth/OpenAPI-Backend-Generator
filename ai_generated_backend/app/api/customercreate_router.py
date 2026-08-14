from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.services.customercreate_service import CustomercreateService

router = APIRouter(prefix="/customer_creates", tags=["Customercreate"])

@router.get("/", response_model=List[schemas.CustomercreateResponse])
def list_customer_creates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List all customer_creates with pagination."""
    service = CustomercreateService(db)
    return service.get_all(skip=skip, limit=limit)

@router.post("/", response_model=schemas.CustomercreateResponse, status_code=status.HTTP_201_CREATED)
def create_customercreate(
    payload: schemas.CustomercreateCreate,
    db: Session = Depends(get_db)
):
    """Create a new Customercreate."""
    service = CustomercreateService(db)
    return service.create(payload)

@router.get("/{item_id}", response_model=schemas.CustomercreateResponse)
def get_customercreate(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get a Customercreate by ID."""
    service = CustomercreateService(db)
    return service.get_by_id(item_id)

@router.put("/{item_id}", response_model=schemas.CustomercreateResponse)
def update_customercreate(
    item_id: int,
    payload: schemas.CustomercreateUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing Customercreate."""
    service = CustomercreateService(db)
    return service.update(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_customercreate(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete a Customercreate."""
    service = CustomercreateService(db)
    return service.delete(item_id)
