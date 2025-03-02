# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.mongo_db import init_database
from logger.logger import Logger

logger = Logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logger.info("MongoDB connection closed")

# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

from routes.routes import router
# Include the router with all routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
