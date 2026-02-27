from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.diagnosis import router as diagnosis_router
from routes.satellite import router as satellite_router
from routes.weather import router as weather_router
from routes.current_weather import router as current_weather_router 
from routes.soil_moisture import router as soil_router
app = FastAPI(title="Smart Sugarcane API - Agile V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://farmiq-prototype.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnosis_router, prefix="/api/v1")
app.include_router(satellite_router, prefix="/api/v1")
app.include_router(weather_router, prefix="/api/v1", tags=["Weather"])
app.include_router(current_weather_router, prefix="/api/v1", tags=["Dashboard"])
app.include_router(soil_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "status": "Smart Sugarcane API Online",
        "Sprint": "4 - Fusion Complete"
    }
