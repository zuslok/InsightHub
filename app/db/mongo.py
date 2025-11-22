from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_URL)
mongo_db = client[settings.MONGO_DB]
analysis_collection = mongo_db[settings.MONGO_COLLECTION]

analysis_collection.create_index("dataset_id")