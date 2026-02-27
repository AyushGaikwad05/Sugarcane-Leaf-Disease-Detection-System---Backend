import requests
import datetime

class WeatherService:
    @staticmethod
    async def fetch_agri_weather(lat: float, lon: float):
        """Fetches agricultural weather data including soil moisture from Open-Meteo."""
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "cloud_cover", "soil_moisture_0_to_7cm"],
            "timezone": "auto",
            "forecast_days": 1
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get("current", {})
            
            return {
                "temp": data.get("temperature_2m"),
                "humidity": data.get("relative_humidity_2m"),
                "clouds": data.get("cloud_cover"),
                "soil_moisture": data.get("soil_moisture_0_to_7cm")
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def calculate_risk(weather_data: dict, planting_date_str: str):
        """Calculates disease risk based on weather and the crop calendar."""
        # 1. Calculate Crop Age
        p_date = datetime.datetime.strptime(planting_date_str, "%Y-%m-%d")
        crop_age = (datetime.datetime.now() - p_date).days
        
        temp = weather_data.get("temp")
        humidity = weather_data.get("humidity")
        soil_moisture = weather_data.get("soil_moisture")
        
        risk_report = {
            "status": "Low Risk",
            "alerts": [],
            "irrigation_needed": False,
            "crop_age": crop_age
        }

        # Logic for Red Rot (Grand Growth stage + high humidity/temp)
        if 120 <= crop_age <= 270:
            if humidity and humidity > 85 and temp and temp > 28:
                risk_report["status"] = "HIGH RISK"
                risk_report["alerts"].append("Weather ideal for Red Rot outbreak. Inspect lower stalks.")

        # Logic for Irrigation Management
        if soil_moisture and soil_moisture < 0.25:
            risk_report["irrigation_needed"] = True
            risk_report["alerts"].append("Soil moisture critical. Initiate irrigation to avoid wilting.")

        return risk_report
    
    @staticmethod
    async def fetch_soil_moisture(lat: float, lon: float):
        """
        Fetches latest soil moisture from Open-Meteo hourly data.
        """
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": [
                "soil_moisture_0_to_7cm",
                "soil_moisture_7_to_28cm"
            ],
            "forecast_days": 1,
            "timezone": "auto"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get("hourly", {})

            soil_surface = data.get("soil_moisture_0_to_7cm", [])
            soil_root = data.get("soil_moisture_7_to_28cm", [])

            latest_surface = soil_surface[-1] if soil_surface else None
            latest_root = soil_root[-1] if soil_root else None

            return {
                "soil_moisture_surface": latest_surface,
                "soil_moisture_root_zone": latest_root
            }

        except Exception as e:
            return {"error": str(e)}