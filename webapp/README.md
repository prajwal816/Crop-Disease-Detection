# CropScan Web Application

A minimal, clean web interface for crop disease detection using an EfficientNetV2-S model trained on the Main19 PlantVillage subset.

## Features

- **19-class disease classification** across Bell Pepper, Corn, Potato, and Tomato
- **Temperature-calibrated confidence** with abstention below 70%
- **Lesion severity estimation** using HSV/Lab colour heuristics
- **Multilingual advisory** in English, Hindi, and Telugu via TF-IDF retrieval
- **Drag-and-drop** or click-to-upload image interface

## Setup

### 1. Backend

```bash
cd webapp/backend
pip install -r requirements.txt
```

Place the checkpoints in the repo-level `models/` folder (or set `MODELS_DIR`): `best_efficientnetv2s_main19.pt`, `best_efficientnet_b0_main19.pt`, `best_vit_b16_main19.pt`. Models that are missing are shown as unavailable in the UI. In the app you can run a single model, **Compare all 3** (side-by-side), or an **Ensemble** (average of calibrated probabilities).

```bash
uvicorn main:app --reload --port 8000
```

### 2. Frontend

Open `webapp/frontend/index.html` directly in a browser, or serve with:

```bash
python -m http.server 3000 --directory webapp/frontend
```

Then visit http://localhost:3000

## Architecture

```
webapp/
  backend/
    main.py             # FastAPI app with /health and /predict endpoints
    model.py            # EfficientNetV2-S loader + temperature-scaled inference
    severity.py         # HSV/Lab lesion-area severity proxy
    advisory.py         # TF-IDF RAG retriever for multilingual advisory
    knowledge_base.py   # 19-class x 3-language advisory content
    requirements.txt
  frontend/
    index.html          # Single-page interface
    style.css           # Design system
    app.js              # Client-side logic (ES module, no build step)
```

## Notes

- The backend starts in degraded mode (503 on `/predict`) if the checkpoint is missing
- Severity proxy is a computer-vision heuristic, not clinical severity
- Advisory content is hand-crafted and not expert-reviewed
