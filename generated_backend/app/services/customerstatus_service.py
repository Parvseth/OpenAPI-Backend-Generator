from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import models
from app.schemas import schemas

class CustomerstatusService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.Customerstatus]:
        return self.db.query(models.Customerstatus).offset(skip).limit(limit).all()

    def get_by_id(self, item_id: int) -> models.Customerstatus:
        item = self.db.query(models.Customerstatus).filter(models.Customerstatus.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customerstatus with id {item_id} not found"
            )
        return item

    def create(self, data: schemas.CustomerstatusCreate) -> models.Customerstatus:
        ##################################################
        # Developer Customization Starts Here
        # TODO: Add domain business rules & validation
        ##################################################

        # AI Generated Business Logic Block:
        try:
            db_item = models.Customerstatus(**data.dict())
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))


    def update(self, item_id: int, data: schemas.CustomerstatusUpdate) -> models.Customerstatus:
        db_item = self.get_by_id(item_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, item_id: int) -> Dict[str, str]:
        db_item = self.get_by_id(item_id)
        self.db.delete(db_item)
        self.db.commit()
        return {"message": f"Customerstatus {item_id} deleted successfully"}
