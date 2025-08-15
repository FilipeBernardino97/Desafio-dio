from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

class MongoClient:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.DATABASE_URL)
        self.db = self.client.store_api

    def __del__(self):
        self.client.close()

db_client = MongoClient()