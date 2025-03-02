# mongo_db.py
from motor.motor_asyncio import AsyncIOMotorClient
from logger.logger import Logger
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
db = None

async def init_database():
    try:
        global db
        logger = Logger(__name__)
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME][COLLECTION_NAME]
        await db.create_index([("geometry", "2dsphere")])
        logger.info("Connected to MongoDB successfully")
        return client, db
    except Exception as e:
        logger.critical(f"Database initialization failed: {str(e)}")
        raise
