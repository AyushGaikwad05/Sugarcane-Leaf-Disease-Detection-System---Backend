import os
import json
import ee
from google.auth import crypt

# ===========================
# Initialize Google Earth Engine with service account JSON
# ===========================

# Load JSON from environment variable
try:
    service_account_info = json.loads(os.environ["GEE_SERVICE_ACCOUNT_JSON"])
except KeyError:
    raise EnvironmentError("GEE_SERVICE_ACCOUNT_JSON environment variable not set.")

# ee.ServiceAccountCredentials expects a path to a file OR the private_key string
# We'll write the JSON to a temporary file in-memory for initialization
import tempfile

with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f:
    json.dump(service_account_info, f)
    temp_key_path = f.name

# Create credentials using temporary JSON file
credentials = ee.ServiceAccountCredentials(
    service_account_info["client_email"],
    key_file=temp_key_path
)

ee.Initialize(credentials, project=service_account_info["project_id"])
print("✅ Google Earth Engine initialized")

# ===========================
# NDVI Analysis Function
# ===========================
def analyze_ndvi(coordinates):
    geometry = ee.Geometry.Polygon(coordinates)

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(geometry)
        .filterDate("2025-06-01", "2026-02-15")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .sort("system:time_start", False)
    )

    image = collection.first()
    if image is None:
        return {"mean_ndvi": 0, "status": "No Image Found", "map_url": None}

    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI").clip(geometry)

    stats = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=10
    ).getInfo()

    mean_ndvi = stats.get("NDVI", 0)

    vis = {"min": 0, "max": 1, "palette": ["red", "yellow", "green"]}
    map_id = ndvi.getMapId(vis)

    return {
        "mean_ndvi": round(mean_ndvi, 3),
        "status": "Stressed" if mean_ndvi < 0.4 else "Healthy",
        "map_url": map_id["tile_fetcher"].url_format
    }