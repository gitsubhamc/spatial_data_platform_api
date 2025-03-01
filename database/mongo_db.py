
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from logger.logger import Logger

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "spatial_db"

async def init_database():
    try:
        logger = Logger(__name__)
        # client = MongoClient(MONGO_URI)
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME]
        db=db["spatial_data"]
        await db["spatial_data"].create_index([("geometry", "2dsphere")])
        logger.info("Connected to MongoDB successfully")
        return client, db
    except Exception as e:
        logger.critical(f"Database initialization failed: {str(e)}")
        raise