from fastapi import APIRouter, HTTPException
from app.db.mongo import analysis_collection

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/{dataset_id}")
def get_analytics(dataset_id: int):
    doc = analysis_collection.find_one({"dataset_id": dataset_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="No analytics found")
    return doc