from fastapi import APIRouter, HTTPException
from services.weather_services import WeatherService

router = APIRouter()

@router.get("/risk-assessment")
async def get_risk_assessment(lat: float, lon: float, planting_date: str):
    """
    Endpoint to get proactive disease risk based on coordinates and planting date.
    Example planting_date: '2025-11-01'
    """
    weather_data = await WeatherService.fetch_agri_weather(lat, lon)
    
    if "error" in weather_data:
        raise HTTPException(status_code=500, detail="Failed to fetch weather data")
        
    risk_analysis = WeatherService.calculate_risk(weather_data, planting_date)
    
    return {
        "location": {"lat": lat, "lon": lon},
        "weather": weather_data,
        "risk_analysis": risk_analysis
    }