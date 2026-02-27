import torch
import torch.nn as nn
from torchvision import models

from core.config import DEVICE, CLASS_NAMES, MODEL_PATH

def load_disease_model():
    model = models.efficientnet_b1(weights=None)
    in_features = model.classifier[1].in_features

    model.classifier = nn.Sequential(
        nn.Dropout(0.45),
        nn.Linear(in_features, 256),
        nn.SiLU(),
        nn.Dropout(0.35),
        nn.Linear(256, len(CLASS_NAMES))
    )

    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()

    print("✅ Disease model loaded")
    return model
