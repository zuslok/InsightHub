from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetOut

router = APIRouter(prefix = "/datasets", tags=["datasets"])

@router.get("/", response_model=List[DatasetOut])
def list_datasets(db: Session = Depends(get_db)):
    return db.query(Dataset).order_by(Dataset.id.desc()).all()

@router.get("/{dataset_id}", response_model=DatasetOut)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    ds = db.get(Dataset, dataset_id)
    if not ds:
        return {"id": 0, "filename": "", "file_url": "", "status": "not_found"}
    return ds