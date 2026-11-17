"""
registry.py - multi-model registry (EfficientNetV2-S, EfficientNet-B0, ViT-B/16)
plus a probability-averaging ensemble.

Each model keeps the preprocessing and calibration temperature it was
trained / calibrated with:

  id        architecture        input   eval transform             temperature
  v2s       EfficientNetV2-S    384     Resize 432 -> CenterCrop   0.616  (notebook 06)
  b0        EfficientNet-B0     224     Resize 256 -> CenterCrop   1.569  (notebook 04)
  vit       ViT-B/16            224     Resize 256 -> CenterCrop   1.0    (no fitted T in notebooks)

Checkpoints are searched for in: $MODELS_DIR, <repo>/models, and this directory.
"""
from __future__ import annotations

import gc
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import model as base  # CLASS_NAMES, constants, torch import guard

logger = logging.getLogger("registry")

if base.HAS_TORCH:
    import torch
    import torch.nn as nn
    import torchvision.models as tvm
    import torchvision.transforms as T

HERE = Path(__file__).resolve().parent
SEARCH_DIRS = [
    Path(p) for p in (
        os.environ.get("MODELS_DIR"),
        HERE.parents[1] / "models",
        HERE,
    ) if p
]


@dataclass(frozen=True)
class ModelSpec:
    id: str
    name: str
    short: str
    filename: str
    input_size: int
    resize: int
    temperature: float
    calibrated: bool = True


SPECS: dict[str, ModelSpec] = {
    "v2s": ModelSpec("v2s", "EfficientNetV2-S", "V2-S", "best_efficientnetv2s_main19.pt", 384, 432, 0.616),
    "b0": ModelSpec("b0", "EfficientNet-B0", "B0", "best_efficientnet_b0_main19.pt", 224, 256, 1.569),
    "vit": ModelSpec("vit", "ViT-B/16", "ViT", "best_vit_b16_main19.pt", 224, 256, 1.0, calibrated=False),
}
ORDER = ["v2s", "b0", "vit"]
ENSEMBLE_ID = "ensemble"
COMPARE_ID = "compare"


def _build(spec_id: str):
    if spec_id == "v2s":
        net = tvm.efficientnet_v2_s(weights=None)
        net.classifier = nn.Sequential(nn.Dropout(0.35), nn.Linear(net.classifier[1].in_features, base.NUM_CLASSES))
    elif spec_id == "b0":
        net = tvm.efficientnet_b0(weights=None)
        net.classifier = nn.Sequential(nn.Dropout(0.3), nn.Linear(net.classifier[1].in_features, base.NUM_CLASSES))
    else:
        net = tvm.vit_b_16(weights=None, image_size=224)
        net.heads.head = nn.Sequential(nn.Dropout(0.30), nn.Linear(net.heads.head.in_features, base.NUM_CLASSES))
    return net


def _find(spec: ModelSpec) -> Optional[Path]:
    if spec.id == "v2s":
        env = os.environ.get("MODEL_PATH")
        if env and Path(env).exists():
            return Path(env)
    for d in SEARCH_DIRS:
        p = d / spec.filename
        if p.is_file():
            return p
    return None


def _transform(spec: ModelSpec):
    return T.Compose([
        T.Resize((spec.resize, spec.resize)),
        T.CenterCrop(spec.input_size),
        T.ToTensor(),
        T.Normalize(base.IMAGENET_MEAN, base.IMAGENET_STD),
    ])


@dataclass
class Loaded:
    spec: ModelSpec
    net: object
    transform: object
    path: Path


@dataclass
class Registry:
    models: dict[str, Loaded] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)

    # -- loading -----------------------------------------------------------
    def load_all(self) -> None:
        if not base.HAS_TORCH:
            logger.warning("PyTorch not installed - no models can be loaded.")
            return
        torch.set_num_threads(max(1, (os.cpu_count() or 2) // 2))
        for mid in ORDER:
            spec = SPECS[mid]
            path = _find(spec)
            if path is None:
                self.errors[mid] = f"checkpoint '{spec.filename}' not found"
                logger.warning("%s: %s", spec.name, self.errors[mid])
                continue
            try:
                ck = torch.load(path, map_location="cpu", weights_only=False)
                sd = ck["model_state_dict"] if isinstance(ck, dict) and "model_state_dict" in ck else ck
                net = _build(mid)
                net.load_state_dict(sd, strict=True)
                net.eval()
                del ck, sd
                gc.collect()
                self.models[mid] = Loaded(spec, net, _transform(spec), path)
                logger.info("Loaded %s from %s", spec.name, path)
            except Exception as exc:  # keep the server up with whatever loads
                self.errors[mid] = str(exc)[:200]
                logger.exception("Failed to load %s", spec.name)

    # -- info --------------------------------------------------------------
    @property
    def any_loaded(self) -> bool:
        return bool(self.models)

    def describe(self) -> list[dict]:
        out = []
        for mid in ORDER:
            s = SPECS[mid]
            out.append({
                "id": mid, "name": s.name, "short": s.short,
                "available": mid in self.models,
                "input_size": s.input_size,
                "temperature": s.temperature,
                "calibrated": s.calibrated,
                "error": self.errors.get(mid),
            })
        n = len(self.models)
        out.append({"id": COMPARE_ID, "name": "Compare all", "available": n >= 2, "members": list(self.models)})
        out.append({"id": ENSEMBLE_ID, "name": "Ensemble", "available": n >= 2, "members": list(self.models)})
        return out

    # -- inference ---------------------------------------------------------
    def probs(self, mid: str, pil_image) -> "torch.Tensor":
        """Calibrated class probabilities, shape (19,)."""
        m = self.models[mid]
        x = m.transform(pil_image.convert("RGB")).unsqueeze(0)
        with torch.no_grad():
            logits = m.net(x) / m.spec.temperature
            return torch.softmax(logits, dim=1)[0]


def summarize(probs, k: int = 3) -> dict:
    """Top-1 + top-k from a probability vector."""
    top = torch.topk(probs, k=min(k, probs.numel()))
    idx = top.indices.tolist()
    val = top.values.tolist()
    return {
        "label": base.CLASS_NAMES[idx[0]],
        "confidence": float(val[0]),
        "top": [{"label": base.CLASS_NAMES[i], "confidence": round(float(v), 4)} for i, v in zip(idx, val)],
    }
