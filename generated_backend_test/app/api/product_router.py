from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Product"])

@router.get("/", response_model=List[schemas.ProductResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List all products with pagination."""
    service = ProductService(db)
    return service.get_all(skip=skip, limit=limit)

@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new Product."""
    service = ProductService(db)
    return service.create(payload)

@router.get("/{item_id}", response_model=schemas.ProductResponse)
def get_product(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get a Product by ID."""
    service = ProductService(db)
    return service.get_by_id(item_id)

@router.put("/{item_id}", response_model=schemas.ProductResponse)
def update_product(
    item_id: int,
    payload: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing Product."""
    service = ProductService(db)
    return service.update(item_id, payload)

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_product(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete a Product."""
    service = ProductService(db)
    return service.delete(item_id)
