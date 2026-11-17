"""
Crop Disease Detection API
FastAPI backend: image upload -> inference (single model / compare / ensemble)
-> severity -> advisory -> JSON response.

Start: uvicorn main:app --port 8000
Checkpoints: put the three .pt files in <repo>/models (or set MODELS_DIR).
"""
import io
import logging
from contextlib import asynccontextmanager
from typing import Optional

import torch
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image, ImageOps

from advisory import get_advisory
from model import get_display_name
from registry import COMPARE_ID, ENSEMBLE_ID, SPECS, Registry, summarize
from severity import compute_severity

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger("webapp")

# ---------------------------------------------------------------------------
# Confidence thresholds (match design spec)
# ---------------------------------------------------------------------------
ABSTAIN_THRESHOLD = 0.70   # below this -> abstain, no advisory
HIGH_THRESHOLD = 0.90      # at or above -> "High" tier
MAX_UPLOAD_BYTES = 10 * 1024 * 1024   # 10 MB

# ---------------------------------------------------------------------------
# Application state (populated by lifespan)
# ---------------------------------------------------------------------------
registry = Registry()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load every available checkpoint once at startup."""
    await run_in_threadpool(registry.load_all)
    if registry.any_loaded:
        logger.info("Ready - models loaded: %s", ", ".join(registry.models))
    else:
        logger.warning("No model checkpoints loaded. /predict will return HTTP 503.")
    yield
    logger.info("Shutting down.")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Crop Disease Detection API",
    description=(
        "Upload a leaf image to receive a predicted disease class, "
        "calibrated confidence, lesion severity proxy, and multilingual advisory. "
        "Choose a single model, compare all models, or use a probability-averaging ensemble."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _err(status: int, error: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"error": error, "message": message})


def _tier(conf: float) -> str:
    if conf >= HIGH_THRESHOLD:
        return "High"
    return "Medium" if conf >= ABSTAIN_THRESHOLD else "Low"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health", summary="Health check")
def health() -> dict:
    """Return service status and which model checkpoints are loaded."""
    return {
        "status": "ok",
        "model_loaded": registry.any_loaded,
        "models_loaded": list(registry.models),
    }


@app.get("/models", summary="List selectable models / modes")
def list_models() -> dict:
    return {"models": registry.describe(), "default": next(iter(registry.models), None)}


def _run_inference(mode: str, pil_image: Image.Image) -> dict:
    """Blocking inference for a single model, 'compare', or 'ensemble'."""
    if mode in registry.models:
        member_ids = [mode]
    elif mode in (ENSEMBLE_ID, COMPARE_ID):
        member_ids = list(registry.models)
        if len(member_ids) < 2:
            raise _err(503, "Not enough models",
                       f"'{mode}' needs at least two loaded models; only {len(member_ids)} available.")
    else:
        raise _err(422, "Unknown model",
                   f"Unknown model '{mode}'. Use one of: {', '.join(list(SPECS) + [COMPARE_ID, ENSEMBLE_ID])}.")

    probs = {mid: registry.probs(mid, pil_image) for mid in member_ids}
    per_model = []
    for mid in member_ids:
        r = summarize(probs[mid])
        per_model.append({
            "id": mid,
            "name": SPECS[mid].name,
            "label": r["label"],
            "display_label": get_display_name(r["label"]),
            "confidence": round(r["confidence"], 4),
            "calibrated": SPECS[mid].calibrated,
            "abstain": r["confidence"] < ABSTAIN_THRESHOLD,
            "top": r["top"],
        })

    if mode == ENSEMBLE_ID:
        avg = torch.stack(list(probs.values())).mean(dim=0)
        primary = summarize(avg)
        primary_id = ENSEMBLE_ID
        primary_name = "Ensemble (" + " + ".join(SPECS[m].short for m in member_ids) + ")"
    elif mode == COMPARE_ID:
        best = max(member_ids, key=lambda m: float(probs[m].max()))
        primary = summarize(probs[best])
        primary_id, primary_name = best, SPECS[best].name
    else:
        primary = summarize(probs[mode])
        primary_id, primary_name = mode, SPECS[mode].name

    labels = [p["label"] for p in per_model]
    return {
        "primary": primary, "primary_id": primary_id, "primary_name": primary_name,
        "per_model": per_model,
        "agreement": len(set(labels)) == 1,
        "agree_count": max(labels.count(l) for l in set(labels)),
    }


@app.post("/predict", summary="Predict crop disease from a leaf image")
async def endpoint_predict(
    file: UploadFile = File(...),
    model: Optional[str] = Form(default=None),
) -> JSONResponse:
    """
    Accept a leaf image (JPEG / PNG / WebP) and return a prediction.

    `model` selects the mode: `v2s`, `b0`, `vit` (single model), `compare`
    (run all models, headline = most confident) or `ensemble` (average of
    calibrated probabilities). Defaults to the first loaded model.
    """
    if not registry.any_loaded:
        raise _err(503, "Model not loaded",
                   "No model checkpoints are available. Place the .pt files in the models/ "
                   "folder (or set MODELS_DIR) and restart the server.")

    mode = (model or next(iter(registry.models))).strip().lower()
    if mode in SPECS and mode not in registry.models:
        raise _err(503, "Model not available",
                   f"{SPECS[mode].name} is not loaded ({registry.errors.get(mode, 'checkpoint missing')}).")

    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if not data:
        raise _err(422, "Empty file", "The uploaded file is empty.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise _err(413, "File too large", "Please upload an image smaller than 10 MB.")
    try:
        pil_image = Image.open(io.BytesIO(data))
        pil_image = ImageOps.exif_transpose(pil_image).convert("RGB")   # honour phone rotation
    except Exception as exc:
        logger.warning("Image decode failed: %s", exc)
        raise _err(422, "Invalid image",
                   "The uploaded file could not be decoded as an image. "
                   "Please upload a valid JPEG, PNG, or WebP file.")

    try:
        res = await run_in_threadpool(_run_inference, mode, pil_image)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected inference error")
        raise _err(500, "Inference failed",
                   "An internal error occurred during prediction. Please try again.")

    label = res["primary"]["label"]
    confidence = res["primary"]["confidence"]
    abstain = confidence < ABSTAIN_THRESHOLD
    lesion_ratio, severity_band = compute_severity(pil_image)
    advisory = get_advisory(label) if not abstain else None

    return JSONResponse(content={
        "mode":            mode,
        "model":           res["primary_id"],
        "model_name":      res["primary_name"],
        "label":           label,
        "display_label":   get_display_name(label),
        "confidence":      round(confidence, 4),
        "confidence_tier": _tier(confidence),
        "top":             res["primary"]["top"],
        "severity_band":   severity_band,
        "lesion_ratio":    lesion_ratio,
        "advisory":        advisory,
        "abstain":         abstain,
        "per_model":       res["per_model"] if len(res["per_model"]) > 1 else None,
        "agreement":       res["agreement"],
        "agree_count":     res["agree_count"],
    })


class AskAIRequest(BaseModel):
    prompt: str
    language: str = "en"
    context: Optional[str] = None


@app.post("/ask-ai", summary="Ask Gemini AI Agricultural Specialist")
async def endpoint_ask_ai(req: AskAIRequest) -> JSONResponse:
    """Provide intelligent multilingual advisory answers powered by Google Gemini."""
    from gemini_service import ask_gemini
    answer = await run_in_threadpool(
        ask_gemini, prompt=req.prompt, language=req.language, context_disease=req.context
    )
    return JSONResponse(content={"answer": answer})
