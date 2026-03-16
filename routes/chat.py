from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chat_services import ChatService

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    lat: float
    lon: float

@router.post("/chat")
async def chat_with_assistant(request: ChatRequest):
    """
    Personalized AI chat that knows the farmer's current soil and weather.
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    answer = await ChatService.get_farmer_response(
        request.question, 
        request.lat, 
        request.lon
    )
    
    return {"answer": answer}