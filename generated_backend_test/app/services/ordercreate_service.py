from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import models
from app.schemas import schemas
from pydantic import model_dump

class OrdercreateService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.Ordercreate]:
        return self.db.query(models.Ordercreate).offset(skip).limit(limit).all()

    def get_by_id(self, item_id: int) -> models.Ordercreate:
        item = self.db.query(models.Ordercreate).filter(models.Ordercreate.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ordercreate with id {item_id} not found"
            )
        return item

    def create(self, data: schemas.OrdercreateCreate) -> models.Ordercreate:
        try:
            db_item = models.Ordercreate(**model_dump(data))
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def update(self, item_id: int, data: schemas.OrdercreateUpdate) -> models.Ordercreate:
        db_item = self.get_by_id(item_id)
        update_data = model_dump(data, exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, item_id: int) -> Dict[str, str]:
        db_item = self.get_by_id(item_id)
        self.db.delete(db_item)
        self.db.commit()
        return {"message": f"Ordercreate {item_id} deleted successfully"}