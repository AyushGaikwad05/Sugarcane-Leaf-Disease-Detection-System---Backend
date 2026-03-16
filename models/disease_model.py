import torch
import torch.nn as nn
from torchvision import models
# Import the settings object instead of individual variables
from core.config import settings 

def load_disease_model():
    # 1. Reconstruct architecture based on EfficientNet-B1
    model = models.efficientnet_b1(weights=None)
    in_features = model.classifier[1].in_features

    # 2. Map the classifier to your settings.CLASS_NAMES length
    model.classifier = nn.Sequential(
        nn.Dropout(0.45),
        nn.Linear(in_features, 256),
        nn.SiLU(),
        nn.Dropout(0.35),
        nn.Linear(256, len(settings.CLASS_NAMES)) # Access via settings object
    )

    # 3. Load weights using the device and path from settings
    model.load_state_dict(torch.load(settings.MODEL_PATH, map_location=settings.DEVICE))
    model.to(settings.DEVICE)
    model.eval()

    print(f"✅ Disease model loaded on {settings.DEVICE}")
    return model