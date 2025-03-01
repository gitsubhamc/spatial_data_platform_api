from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
from contextlib import asynccontextmanager
from database.mongo_db import init_database
from schemas.pydantic_schema import *
from logger.logger import Logger

logger = Logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db
    client, db = await init_database()  # Initialize DB connection
    yield
    client.close()  # Cleanup DB connection
    logger.info("MongoDB connection closed")

# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)


# API Endpoints

@app.post("/spatial_data/point")
async def store_spatial_point(data: SpatialPointDataModel):
    result = await db.insert_one(data.dict())  # Async insertion
    return {"message": "Point data stored", "id": str(result.inserted_id)}

@app.post("/spatial_data/polygon")
async def store_spatial_polygon(data: SpatialPolygonDataModel):
    result = await db.insert_one(data.dict())  # Async insertion
    return {"message": "Polygon data stored", "id": str(result.inserted_id)}

@app.get("/spatial_data/points")
async def get_all_spatial_points(name: str = None):
    query = {"geometry.type": "Point"}
    if name:
        query["name"] = name
    data = await db.find(query, {"_id": 0}).to_list(None)  # Async query with to_list()
    if not data:
        raise HTTPException(status_code=404, detail="No Point data found")
    return {"data": data}

@app.get("/spatial_data/polygons")
async def get_all_spatial_polygons(name: str = None):
    query = {"geometry.type": "Polygon"}
    if name:
        query["name"] = name
    data = await db.find(query, {"_id": 0}).to_list(None)  # Async query with to_list()
    if not data:
        raise HTTPException(status_code=404, detail="No Polygon data found")
    return {"data": data}

@app.put("/spatial_data/point/{name}")
async def update_spatial_point(name: str, data: SpatialPointDataModel):
    result = await db.update_one({"name": name}, {"$set": data.dict()})  # Async update
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Point data not found")
    return {"message": "Point data updated"}

@app.put("/spatial_data/polygon/{name}")
async def update_spatial_polygon(name: str, data: SpatialPolygonDataModel):
    result = await db.update_one({"name": name}, {"$set": data.dict()})  # Async update
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Polygon data not found")
    return {"message": "Polygon data updated"}

@app.get("/spatial_data/near_point")
async def find_near_point(longitude: float, latitude: float, max_distance: int = 5000):
    query = {
        "geometry.type": "Point",
        "geometry": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                "$maxDistance": max_distance
            }
        }
    }
    data = await db["spatial_data"].find(query, {"_id": 0}).to_list(None)  # Async query with to_list()
    return {"data": data}

@app.get("/spatial_data/contains")
async def find_polygon_containing_point(longitude: float, latitude: float):
    query = {
        "geometry": {
            "$geoIntersects": {
                "$geometry": {"type": "Point", "coordinates": [longitude, latitude]}
            }
        }
    }
    data = await db.find(query, {"_id": 0}).to_list(None)  # Async query with to_list()
    return {"data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)