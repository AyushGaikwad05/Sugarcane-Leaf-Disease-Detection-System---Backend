import ee
from core.config import GEE_PROJECT_ID

ee.Initialize(project=GEE_PROJECT_ID)
print("✅ Google Earth Engine initialized")

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
