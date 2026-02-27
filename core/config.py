import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASS_NAMES = [
    "BacterialBlights",
    "Healthy",
    "Mosaic",
    "RedRot",
    "Rust",
    "Yellow"
]

MODEL_PATH = "saved_models/final-efficientnet_transfer.pth"
GEE_PROJECT_ID = "aisugarcane"
