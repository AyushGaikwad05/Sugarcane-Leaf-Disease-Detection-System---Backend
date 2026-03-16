# services/chat_services.py
from google import genai # Note the change in import path
from services.current_weather import CurrentWeather
from core.config import settings

# Initialize the official Google GenAI client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

class ChatService:
    @staticmethod
    async def get_farmer_response(question: str, lat: float, lon: float):
        # 1. Fetch live farm context
        farm_data = await CurrentWeather.get_live_weather(lat, lon)
        
        system_context = f"""
        You are an expert Sugarcane Agriculture Assistant for a farm of Sugarcane.
        The farmer's current live data is:
        - Temperature: {farm_data.get('temperature')}
        - Humidity: {farm_data.get('humidity')}
        - Soil Moisture: {farm_data.get('soil_moisture')}
        
        Instructions: Answer ONLY questions related to sugarcane or irrigation.
        """
        
        try:
            # 2. Generate response using the new SDK syntax
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                contents=f"{system_context}\n\nFarmer Question: {question}"
            )
            return response.text
        except Exception as e:
            return f"Error connecting to AI: {str(e)}"