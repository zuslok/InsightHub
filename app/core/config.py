import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    MONGO_URL: str = os.getenv("MONGO_URL")
    MONGO_DB: str = os.getenv("MONGO_DB")
    MONGO_COLLECTION: str = os.getenv("MONGO_COLLECTION")
    POSTGRES_URL: str = os.getenv("POSTGRES_URL")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    APP_ENV: str = os.getenv("APP_ENV")
    APP_PORT: str = os.getenv("APP_PORT")
    APP_NAME: str = os.getenv("APP_NAME")
    MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB", 50))
    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION")
    S3_BUCKET: str = os.getenv("S3_BUCKET")
    S3_PREFIX: str = os.getenv("S3_PREFIX")
        
settings = Settings()