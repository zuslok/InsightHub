from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.dataset import Dataset
from app.schemas.dataset import CreateDatasetOut
from app.services.s3_service import upload_bytes_to_s3
from app.workers.background import run_analysis

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/", response_model=CreateDatasetOut)
async def upload_dataset(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    size_mb = (file.size or 0) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_MB:
        raise HTTPException(status_code=413, detail="File too large")
    
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")
    
    #Upload to S3
    s3_url = upload_bytes_to_s3(content, file.filename)
    
    # Persist metadata
    ds = Dataset(filename=file.filename, file_url=s3_url, status="pending")
    db.add(ds)
    db.commit()
    db.refresh(ds) # for getting id after commit
    
    # Trigger background analysis(sync lightweight worker)
    run_analysis(db, ds.id)
    
    return {"id": ds.id, "message": "Upload received and analysis started"}