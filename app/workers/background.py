from sqlalchemy.orm import Session
from app.models.dataset import Dataset
from app.services.analyzer import analyze_dataset

def run_analysis(db: Session, dataset_id: int):
    ds = db.get(Dataset, dataset_id)
    if not ds:
        return
    ds.status = "processing"
    db.commit()
    
    try:
        analyze_dataset(dataset_id=ds.id, s3_url=ds.file_url)
        ds.status = "done"
    except Exception:
        ds.status = "failed"
    finally:
        db.commit()
        
