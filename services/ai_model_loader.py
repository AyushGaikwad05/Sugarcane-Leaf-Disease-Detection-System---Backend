import torch
import torch.nn as nn
from torchvision import models
from core.config import settings

def load_disease_model():
    # 1. Initialize EfficientNet-B1 without pre-trained weights
    model = models.efficientnet_b1(weights=None)
    in_features = model.classifier[1].in_features

    # 2. Reconstruct the custom classifier from your project specs
    model.classifier = nn.Sequential(
        nn.Dropout(0.45),
        nn.Linear(in_features, 256),
        nn.SiLU(),
        nn.Dropout(0.35),
        nn.Linear(256, len(settings.CLASS_NAMES)) # Uses length from your config
    )

    # 3. Load the .pth file using settings for path and device
    try:
        model.load_state_dict(torch.load(settings.MODEL_PATH, map_location=settings.DEVICE))
        model.to(settings.DEVICE)
        model.eval()
        print(f"✅ Disease model loaded successfully on {settings.DEVICE}")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None