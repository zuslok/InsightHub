from fastapi import FastAPI
from app.core.config import settings
from app.db.postgres import Base, engine

from app.routes import health, analytics, datasets, upload

# Create tables if not exist (for demo; prod: Alembic recommended)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.include_router(router=health.router)
app.include_router(router=datasets.router)
app.include_router(router=upload.router)
app.include_router(router=analytics.router)

@app.get("/")
def root():
    return {"message": "InsightHub backend is running 🚀"}