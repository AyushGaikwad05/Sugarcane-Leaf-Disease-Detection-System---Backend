import torch
import cv2
import numpy as np
import io
from PIL import Image

# Correct imports for your folder structure
from core.config import settings 
from services.ai_model_loader import load_disease_model 
from utils.image_utils import preprocess_image

# Load model once using the new loader
model = load_disease_model()

# Thresholds
MIN_ACCEPTABLE_SCORE = 0.4
WARNING_SCORE = 0.6
CONFIDENCE_THRESHOLD = 0.65

def leaf_quality_score(image_bytes: bytes) -> float:
    # ... (Keep your existing quality logic here) ...
    try:
        image = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        score = 0.0
        # Brightness, Blur, and Green check
        if 50 <= np.mean(gray) <= 200: score += 0.3
        if cv2.Laplacian(gray, cv2.CV_64F).var() > 80: score += 0.3
        if np.mean(image[:, :, 1]) >= np.mean(image[:, :, 0]) * 0.9: score += 0.4
        return score
    except: return 0.0

def predict_disease(image_bytes: bytes):
    quality_score = leaf_quality_score(image_bytes)

    if quality_score < MIN_ACCEPTABLE_SCORE:
        return {"status": "Rejected", "message": "Leaf not detected."}

    # Use settings.DEVICE for tensor placement
    tensor = preprocess_image(image_bytes).to(settings.DEVICE)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)
        conf, idx = torch.max(probs, dim=1)

    confidence = conf.item()

    if confidence < CONFIDENCE_THRESHOLD:
        return {"status": "Warning", "message": "Low confidence prediction."}

    # Use settings.CLASS_NAMES for the final label
    return {
        "status": "Success",
        "disease": settings.CLASS_NAMES[idx.item()],
        "confidence": f"{confidence * 100:.2f}%"
    }