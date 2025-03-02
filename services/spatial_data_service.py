# services/spatial_data_service.py
from schemas.pydantic_schema import SpatialPointDataModel, SpatialPolygonDataModel

class SpatialDataService:

    @staticmethod
    async def store_spatial_point(db, data: SpatialPointDataModel):
        return await db.insert_one(data.dict())

    @staticmethod
    async def store_spatial_polygon(db, data: SpatialPolygonDataModel):
        return await db.insert_one(data.dict())

    @staticmethod
    async def get_all_spatial_data(db, type: str , name: str = None):
        query = {"geometry.type": str(type)}
        if name:
            query["name"] = name
        return await db.find(query, {"_id": 0}).to_list(None)

    @staticmethod
    async def update_spatial_point(db, name: str, data: SpatialPointDataModel):
        result = await db.update_one({"name": name}, {"$set": data.dict()})
        if result.matched_count == 0:
            return None
        return result

    @staticmethod
    async def update_spatial_polygon(db, name: str, data: SpatialPolygonDataModel):
        result = await db.update_one({"name": name}, {"$set": data.dict()})
        if result.matched_count == 0:
            return None
        return result

    @staticmethod
    async def find_near_point(db, longitude: float, latitude: float, max_distance: int = 5000):
        query = {
            "geometry.type": "Point",
            "geometry": {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                    "$maxDistance": max_distance
                }
            }
        }
        return await db["spatial_data"].find(query, {"_id": 0}).to_list(None)
