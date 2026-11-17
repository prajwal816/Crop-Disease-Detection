"""
model.py - EfficientNetV2-S loader and inference with temperature scaling.

The checkpoint is expected to be a dict with key "model_state_dict" (produced
by the training loop in notebook 05).  The classifier head matches the
architecture used in that notebook: Dropout(p=0.35) + Linear(in_features, 19).

Temperature T=0.616 was fitted in notebook 06.
"""

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import torch
    import torch.nn as nn
    import torchvision.models as models
    import torchvision.transforms as T
    HAS_TORCH = True
except ImportError:
    torch = None
    nn = None
    models = None
    T = None
    HAS_TORCH = False

from PIL import Image

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CHECKPOINT_PATH: Path = Path(os.environ.get("MODEL_PATH", "best_efficientnetv2s_main19.pt"))

TEMPERATURE: float = 0.616
NUM_CLASSES: int = 19

# Exact order that matches the training label encoder (notebook 05 / class_to_idx)
CLASS_NAMES: list[str] = [
    "bell_pepper__bacterial_spot",
    "bell_pepper__healthy",
    "corn__cercospora_leaf_spot_gray_leaf_spot",
    "corn__common_rust",
    "corn__healthy",
    "corn__northern_leaf_blight",
    "potato__early_blight",
    "potato__healthy",
    "potato__late_blight",
    "tomato__bacterial_spot",
    "tomato__early_blight",
    "tomato__healthy",
    "tomato__late_blight",
    "tomato__leaf_mold",
    "tomato__septoria_leaf_spot",
    "tomato__spider_mites_two_spotted_spider_mite",
    "tomato__target_spot",
    "tomato__tomato_mosaic_virus",
    "tomato__tomato_yellow_leaf_curl_virus",
]

# ImageNet statistics used during training
IMAGENET_MEAN: list[float] = [0.485, 0.456, 0.406]
IMAGENET_STD: list[float] = [0.229, 0.224, 0.225]

# Eval transform mirrors notebook 06: resize longer edge to 432, then centre-crop to 384
RESIZE_SIZE: int = 432
INPUT_SIZE: int = 384

# ---------------------------------------------------------------------------
# Eval transform (defined once to avoid repeated construction)
# ---------------------------------------------------------------------------

if HAS_TORCH:
    _eval_transform = T.Compose([
        T.Resize((RESIZE_SIZE, RESIZE_SIZE)),
        T.CenterCrop(INPUT_SIZE),
        T.ToTensor(),
        T.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])
else:
    _eval_transform = None


# ---------------------------------------------------------------------------
# ModelState
# ---------------------------------------------------------------------------

@dataclass
class ModelState:
    """Holds the loaded model (or None) and a flag indicating readiness."""
    model: Optional[object] = field(default=None)
    loaded: bool = False


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_model() -> ModelState:
    """Load the EfficientNetV2-S checkpoint and return a ready ModelState.

    Returns a ModelState with ``loaded=False`` when the checkpoint file is
    absent - the application continues to serve non-prediction endpoints.
    """
    state = ModelState()

    if not HAS_TORCH:
        logger.warning(
            "PyTorch is not installed in the current environment. "
            "Install torch and torchvision to enable inference."
        )
        return state

    if not CHECKPOINT_PATH.exists():
        logger.warning(
            "Model checkpoint not found at '%s'. "
            "Upload best_efficientnetv2s_main19.pt and restart to enable /predict.",
            CHECKPOINT_PATH,
        )
        return state

    # Build architecture - must match notebook 05 exactly
    net = models.efficientnet_v2_s(weights=None)
    in_features: int = net.classifier[1].in_features
    net.classifier = nn.Sequential(
        nn.Dropout(p=0.35),
        nn.Linear(in_features, NUM_CLASSES),
    )

    # Load weights - checkpoint is a dict produced by notebook 05
    ckpt = torch.load(CHECKPOINT_PATH, map_location="cpu", weights_only=False)
    if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
        net.load_state_dict(ckpt["model_state_dict"])
    else:
        # Fallback: treat checkpoint as a bare state_dict
        logger.warning(
            "Checkpoint has no 'model_state_dict' key - loading as bare state_dict."
        )
        net.load_state_dict(ckpt)

    net.eval()
    state.model = net
    state.loaded = True
    logger.info("Model loaded from '%s'.", CHECKPOINT_PATH)
    return state


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------

def predict(state: ModelState, pil_image: Image.Image) -> tuple[str, float]:
    """Run a single-image forward pass and return (class_name, probability).

    The returned probability is calibrated via temperature scaling (T=0.616).

    Raises
    ------
    RuntimeError
        When called with a ModelState whose ``loaded`` flag is False.
    """
    if not state.loaded or state.model is None:
        raise RuntimeError("Model not loaded")

    tensor = _eval_transform(pil_image.convert("RGB")).unsqueeze(0)  # (1, 3, 384, 384)

    with torch.no_grad():
        logits = state.model(tensor)                   # (1, 19)
        logits_scaled = logits / TEMPERATURE
        probs = torch.softmax(logits_scaled, dim=1)    # (1, 19)

    top_idx: int = int(probs.argmax(dim=1).item())
    return CLASS_NAMES[top_idx], float(probs[0, top_idx])


# ---------------------------------------------------------------------------
# Display-name helper
# ---------------------------------------------------------------------------

def get_display_name(class_name: str) -> str:
    """Convert a snake_case class name to a human-readable label.

    Examples
    --------
    >>> get_display_name("tomato__early_blight")
    'Tomato: Early Blight'
    >>> get_display_name("bell_pepper__healthy")
    'Bell Pepper: Healthy'
    >>> get_display_name("corn__cercospora_leaf_spot_gray_leaf_spot")
    'Corn: Cercospora Leaf Spot Gray Leaf Spot'
    """
    if "__" in class_name:
        crop_part, condition_part = class_name.split("__", 1)
    else:
        # No separator - treat the whole string as the condition
        crop_part, condition_part = "", class_name

    def _title(s: str) -> str:
        return " ".join(word.capitalize() for word in s.split("_"))

    crop_title = _title(crop_part)
    condition_title = _title(condition_part)

    if crop_title:
        return f"{crop_title}: {condition_title}"
    return condition_title
