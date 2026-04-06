# services/chat_services.py
from google import genai # Note the change in import path
from services.current_weather import CurrentWeather
from core.config import settings

# Initialize the official Google GenAI client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

class ChatService:
    @staticmethod
    async def get_farmer_response(question: str, lat: float, lon: float):
        from core.trigger_data import SUGARCANE_TRIGGERS_JSON
        from core.pest_data import PEST_MANAGEMENT_JSON
        
        # 1. Fetch live farm context
        farm_data = await CurrentWeather.get_live_weather(lat, lon)
        
        system_context = f"""
        You are an expert Sugarcane Agriculture Assistant for a farm of Sugarcane.
        The farmer's current live data is:
        - Temperature: {farm_data.get('temperature')}
        - Humidity: {farm_data.get('humidity')}
        - Rainfall: {farm_data.get('rainfall', '0 mm')}
        - Soil Moisture: {farm_data.get('soil_moisture')}
        
        CRITICAL INSTRUCTION: You MUST use ONLY the following trigger conditions and control logic when advising on diseases or pests:
        {SUGARCANE_TRIGGERS_JSON}
        
        CRITICAL BEHAVIOR:
        1. ONLY provide disease warnings or chemical controls if the user explicitly asks about diseases, pests, health, sprays, or recommendations.
        2. Do NOT proactively list diseases or warnings if the user is just greeting you or asking a general question (e.g., "Who are you?").
        3. Answer ONLY questions related to sugarcane or irrigation.
        
        PEST MANAGEMENT GUIDELINES:
        {PEST_MANAGEMENT_JSON}
        You MUST use this data to advise on pest management IF AND ONLY IF the user explicitly asks about pests or treatments.
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