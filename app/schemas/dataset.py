from pydantic import BaseModel
from typing import Optional

class DatasetOut(BaseModel):
    id: int
    filename: str
    file_url: str
    status: str
    class Config:
        from_attributes = True # turn orm objects into pydantic modal
    
class CreateDatasetOut(BaseModel):
    id: int
    message: str
    