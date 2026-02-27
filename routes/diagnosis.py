from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ai_diagnosis import predict_disease

router = APIRouter()

@router.post("/diagnose")
async def diagnose(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        return predict_disease(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
