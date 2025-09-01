from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings

class MongoClient:
    def __init__(self) -> None:
        # Usa a URL completa do settings
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.get_database_url())

    def get(self) -> AsyncIOMotorClient:
        return self.client


db_client = MongoClient()
