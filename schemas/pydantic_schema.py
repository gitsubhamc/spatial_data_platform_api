from pydantic import BaseModel
from typing import List, Union


# Define Pydantic models
class PointModel(BaseModel):
    type: str = "Point"
    coordinates: List[float]

class MultiPolygonModel(BaseModel):
    type: str = "Polygon"
    coordinates: List[float]

class SpatialPointDataModel(BaseModel):
    name: str
    geometry: PointModel

class SpatialPolygonDataModel(BaseModel):
    name: str
    geometry: MultiPolygonModel