from pymongo import AsyncMongoClient
from backend.config.settings import get_settings

class MongoDB:
    _instance = None
    _mongo_client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_mongo_client(cls):
        if cls._mongo_client is None:
            raise Exception("Mongo client not ready")
        return cls._mongo_client

    @classmethod
    async def set_mongo_client(cls):
        try:
            mongo_url = get_settings().mongodb_url
            client = AsyncMongoClient(mongo_url)
            cls._mongo_client = client['test']
            print("MongoDB client set successfully")
        except Exception as e:
            print(f"Could not set mongo client: {e}")


def get_mongo_client():
    return MongoDB.get_mongo_client()

async def set_mongo_client():
    return await MongoDB.set_mongo_client()