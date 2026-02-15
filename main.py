import ee
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import io
import datetime
import requests
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Smart Sugarcane API - Agile V2")




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =================================================================
# SPRINT 1: AI DIAGNOSIS ENGINE (Disease Model)
# =================================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class_names = ['BacterialBlights', 'Healthy', 'Mosaic', 'RedRot', 'Rust', 'Yellow']

# Reconstruct Model Architecture
disease_model = models.efficientnet_b1(weights=None)
in_features = disease_model.classifier[1].in_features
disease_model.classifier = nn.Sequential(
    nn.Dropout(0.45),
    nn.Linear(in_features, 256),
    nn.SiLU(),
    nn.Dropout(0.35),
    nn.Linear(256, len(class_names))
)

# Load your specific weights
try:
    disease_model.load_state_dict(torch.load("saved_models/final-efficientnet_transfer.pth", map_location=device))
    disease_model.to(device)
    disease_model.eval()
    print("✅ Sprint 1: AI Disease Model Loaded")
except Exception as e:
    print(f"❌ Sprint 1 Error: {e}")

# Preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.post("/api/v1/diagnose")
async def diagnose(file: UploadFile = File(...)):
    """AI Image Analysis for Sugarcane Diseases"""
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content)).convert("RGB")
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = disease_model(input_tensor)
            probs = torch.softmax(outputs, dim=1)
            conf, idx = torch.max(probs, dim=1)
        
        return {
            "disease": class_names[idx.item()],
            "confidence": f"{conf.item() * 100:.2f}%"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =================================================================
# SPRINT 2: PREDICTIVE RISK FRAMEWORK (Weather & Calendar)
# =================================================================
# Replace with your actual OpenWeatherMap API Key
# WEATHER_API_KEY = "YOUR_OPENWEATHER_KEY"

# @app.get("/api/v1/risk-assessment")
# async def get_risk(lat: float, lon: float, planting_date: str):
#     """Predictive Risk based on Crop Calendar & Weather"""
#     try:
#         # Calculate Crop Age
#         p_date = datetime.datetime.strptime(planting_date, "%Y-%m-%d")
#         age_days = (datetime.datetime.now() - p_date).days
        
#         # Fetch Real-time Weather
#         weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
#         weather_data = requests.get(weather_url).json()
#         humidity = weather_data['main']['humidity']
#         temp = weather_data['main']['temp']

#         # Proactive Risk Logic (Digital Calendar)
#         risk_level = "Low"
#         alert = "Crop is stable."

#         # Risk Rule: Red Rot triggers in Grand Growth phase with high humidity
#         if 120 <= age_days <= 270:
#             if humidity > 85 and temp > 28:
#                 risk_level = "High"
#                 alert = "Conditions ideal for Red Rot. Inspect lower stalks."
        
#         return {
#             "crop_age": f"{age_days} days",
#             "weather": {"temp": temp, "humidity": humidity},
#             "risk_level": risk_level,
#             "alert": alert
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Weather/Calendar error")

# =================================================================
# SPRINT 3: SATELLITE MONITORING (NDVI Integration)
# =================================================================
try:
    ee.Initialize(project='aisugarcane')
    print("✅ Sprint 3: Google Earth Engine Connected")
except Exception as e:
    print(f"❌ Sprint 3 Error: {e}")

class GeoJSONRequest(BaseModel):
    coordinates: List[List[List[float]]]

@app.post("/api/v1/analyze-health")
async def analyze_health(data: GeoJSONRequest):
    """GIS-based Health Monitoring using NDVI"""
    try:
        geometry = ee.Geometry.Polygon(data.coordinates)
        s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
            .filterBounds(geometry)
            .filterDate('2025-06-01', '2026-02-15')
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
            .sort('system:time_start', False))

        image = s2.first()
        if not image:
            return {"error": "No clear imagery found."}

        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI').clip(geometry)
        stats = ndvi.reduceRegion(reducer=ee.Reducer.mean(), geometry=geometry, scale=10).getInfo()
        mean_val = stats.get('NDVI', 0)

        # Generate Heatmap URL for Flutter
        vis_params = {'min': 0, 'max': 1, 'palette': ['red', 'yellow', 'green']}
        map_id = ee.Image(ndvi).getMapId(vis_params)

        return {
            "mean_ndvi": round(mean_val, 3),
            "status": "Stressed" if mean_val < 0.4 else "Healthy",
            "map_url": map_id['tile_fetcher'].url_format
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =================================================================
# SPRINT 4: SYSTEM FUSION (Final UI Endpoints)
# =================================================================
@app.get("/")
def read_root():
    return {"status": "Smart Sugarcane API Online", "Sprint": "4 - Fusion Complete"}