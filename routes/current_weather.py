from fastapi import APIRouter, HTTPException
from services.current_weather import CurrentWeather

router = APIRouter()

@router.get("/current-weather")
async def read_current_weather(lat: float, lon: float):
    """Simple API for the farmer's dashboard with no alerts."""
    data = await CurrentWeather.get_live_weather(lat, lon)
    
    if data["status"] == "Error":
        raise HTTPException(status_code=500, detail=data["message"])
        
    return data