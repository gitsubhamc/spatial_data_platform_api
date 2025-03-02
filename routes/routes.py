# routes.py
from fastapi import APIRouter, HTTPException , status
from schemas.pydantic_schema import SpatialPointDataModel, SpatialPolygonDataModel
from services.spatial_data_service import SpatialDataService
from database.mongo_db import init_database

router = APIRouter()

# Initialize the database connection
@router.on_event("startup")
async def on_startup():
    global db
    _, db = await init_database()  # We only need to fetch `db` here


@router.post("/spatial_data/point")
async def store_spatial_point(data: SpatialPointDataModel):
    try:
        result = await SpatialDataService.store_spatial_point(db, data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
    return {"message": "Point data stored", "id": str(result.inserted_id)}

@router.post("/spatial_data/polygon")
async def store_spatial_polygon(data: SpatialPolygonDataModel):

    try:
        result = await SpatialDataService.store_spatial_polygon(db, data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
    return {"message": "Polygon data stored", "id": str(result.inserted_id)}

@router.get("/spatial_data/{type}")
async def get_all_spatial_points(type: str = 'Polygon' , name: str = None):

    data = await SpatialDataService.get_all_spatial_data(db, type, name)
    if not data:
        raise HTTPException(status_code=404, detail="No Point data found")
    return {"data": data}

@router.put("/spatial_data/point/{name}")
async def update_spatial_point(name: str, data: SpatialPointDataModel):

    result = await SpatialDataService.update_spatial_point(db, name, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Point data not found")
    return {"message": "Point data updated"}

@router.put("/spatial_data/polygon/{name}")
async def update_spatial_polygon(name: str, data: SpatialPolygonDataModel):

    result = await SpatialDataService.update_spatial_polygon(db, name, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Polygon data not found")
    return {"message": "Polygon data updated"}

@router.get("/spatial_data/near_point")
async def find_near_point(longitude: float, latitude: float, max_distance: int = 5000):
    try:
        data = await SpatialDataService.find_near_point(db, longitude, latitude, max_distance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
    return {"data": data}
