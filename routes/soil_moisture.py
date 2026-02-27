from fastapi import APIRouter, HTTPException
from services.weather_services import WeatherService

router = APIRouter()

@router.get("/soil-moisture")
async def get_soil_moisture(lat: float, lon: float):
    """
    Returns latest soil moisture values.
    """
    data = await WeatherService.fetch_soil_moisture(lat, lon)

    if "error" in data:
        raise HTTPException(status_code=500, detail="Failed to fetch soil moisture")

    return {
        "location": {"lat": lat, "lon": lon},
        "soil_moisture": data,
        "status": "Success"
    }