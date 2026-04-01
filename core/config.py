import os
import torch
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Settings:
    # 1. Device Configuration
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 2. Model Metadata
    CLASS_NAMES = [
        "Deficiencies",
        "Healthy",
        "Mawa",
        "Pest infestation",
        "Rust",
        "Smut"
    ]

    # 3. Paths & Project IDs
    MODEL_PATH = os.getenv("MODEL_PATH", "saved_models/sugarcane_efficientnet_b1_final.pth")
    GEE_PROJECT_ID = os.getenv("GEE_PROJECT_ID", "aisugarcane")
    GEE_JSON_PATH = os.getenv("GEE_JSON_PATH", "GEE_SERVICE_ACC.json")
    # 4. API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# CRITICAL: This creates the 'settings' object that other files import
settings = Settings()