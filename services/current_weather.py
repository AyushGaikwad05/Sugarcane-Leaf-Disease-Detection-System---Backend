import requests

class CurrentWeather:
    @staticmethod
    async def get_live_weather(lat: float, lon: float):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m", 
                "relative_humidity_2m", 
                "cloud_cover", 
                "wind_speed_10m",
                "soil_moisture_0_to_7cm"
            ],
            "timezone": "auto"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get("current", {})
            
            # SAFE EXTRACTION: Check if soil_moisture exists before multiplying
            raw_moisture = data.get('soil_moisture_0_to_7cm')
            formatted_moisture = f"{int(raw_moisture * 100)}%" if raw_moisture is not None else "N/A"
            
            return {
                "temperature": f"{data.get('temperature_2m')}°C",
                "humidity": f"{data.get('relative_humidity_2m')}%",
                "cloud_cover": f"{data.get('cloud_cover')}%",
                "wind_speed": f"{data.get('wind_speed_10m')} km/h",
                "soil_moisture": formatted_moisture,
                "status": "Success"
            }
        except Exception as e:
            return {"status": "Error", "message": str(e)}