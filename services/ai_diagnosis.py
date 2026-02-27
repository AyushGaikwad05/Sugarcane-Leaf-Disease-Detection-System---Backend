import torch
import cv2
import numpy as np
import io
from PIL import Image

from models.disease_model import load_disease_model
from utils.image_utils import preprocess_image
from core.config import DEVICE, CLASS_NAMES

# ===============================
# Load model once
# ===============================
model = load_disease_model()

# ===============================
# Thresholds (tunable)
# ===============================
MIN_ACCEPTABLE_SCORE = 0.4
WARNING_SCORE = 0.6
CONFIDENCE_THRESHOLD = 0.65


# ===============================
# Leaf Quality Scoring (Soft Validation)
# ===============================
def leaf_quality_score(image_bytes: bytes) -> float:
    """
    Returns a score between 0 and 1 indicating likelihood of a valid leaf image.
    Uses soft scoring instead of hard rejection.
    """

    try:
        image = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        score = 0.0

        # 1️⃣ Brightness check (soft)
        brightness = np.mean(gray)
        if 50 <= brightness <= 200:
            score += 0.3

        # 2️⃣ Blur check (soft)
        blur = cv2.Laplacian(gray, cv2.CV_64F).var()
        if blur > 80:
            score += 0.3

        # 3️⃣ Green dominance check (very soft)
        r_mean = np.mean(image[:, :, 0])
        g_mean = np.mean(image[:, :, 1])
        b_mean = np.mean(image[:, :, 2])

        # allow slight variation (not strict green dominance)
        if g_mean >= r_mean * 0.9 and g_mean >= b_mean * 0.9:
            score += 0.4

        return score

    except Exception:
        return 0.0


# ===============================
# Main Prediction Function
# ===============================
def predict_disease(image_bytes: bytes):
    """
    Predicts sugarcane disease with:
    - Soft leaf validation
    - Confidence gating
    - User-friendly warnings
    """

    # Step 1️⃣: Calculate quality score
    quality_score = leaf_quality_score(image_bytes)

    # ❌ Completely unrelated image
    if quality_score < MIN_ACCEPTABLE_SCORE:
        return {
            "status": "Rejected",
            "message": "Leaf not detected. Please upload a clear sugarcane leaf image."
        }

    # ⚠️ Low-quality but possible leaf
    if quality_score < WARNING_SCORE:
        return {
            "status": "Warning",
            "message": "Image quality is low. Please upload a clearer leaf image for accurate results."
        }

    # Step 2️⃣: Proceed with disease classification
    tensor = preprocess_image(image_bytes).to(DEVICE)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)
        conf, idx = torch.max(probs, dim=1)

    confidence = conf.item()

    # ❌ Model uncertain
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "status": "Warning",
            "message": "Unable to confidently identify disease. Please try another image."
        }

    # ✅ Valid prediction
    return {
        "status": "Success",
        "disease": CLASS_NAMES[idx.item()],
        "confidence": f"{confidence * 100:.2f}%"
    }