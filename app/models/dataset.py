from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.postgres import Base

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    status = Column(String, default="pending") 
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())