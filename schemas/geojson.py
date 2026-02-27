from pydantic import BaseModel
from typing import List

class GeoJSONRequest(BaseModel):
    coordinates: List[List[List[float]]]
