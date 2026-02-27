from fastapi import APIRouter, HTTPException
from schemas.geojson import GeoJSONRequest
from services.gee_service import analyze_ndvi

router = APIRouter()

@router.post("/analyze-health")
async def analyze_health(data: GeoJSONRequest):
    try:
        return analyze_ndvi(data.coordinates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
