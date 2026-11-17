"""
gemini_service.py - Google Gemini AI Agricultural Advisory and Translation Service

Uses the user-provided Gemini API key to deliver dynamic agricultural consultations,
treatment explanations, and vernacular translation in English, Hindi, and Telugu.
"""

import json
import logging
import os
import urllib.request
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Load API key from env or .env file
ENV_PATH = Path(__file__).resolve().parent / ".env"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY and ENV_PATH.exists():
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                GEMINI_API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

MODELS_TO_TRY = [
    "gemini-3.1-flash-lite-preview",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite",
]


def ask_gemini(
    prompt: str,
    language: str = "en",
    context_disease: Optional[str] = None
) -> str:
    """Query Gemini for expert agricultural advisory or translation in the requested language."""
    if not GEMINI_API_KEY:
        return "Gemini API key is not configured. Please add GEMINI_API_KEY to your .env file."

    lang_instruction = {
        "hi": "Respond entirely in clear, simple Hindi (हिंदी) that an Indian farmer can easily understand.",
        "te": "Respond entirely in clear, simple Telugu (తెలుగు) that a farmer in Andhra Pradesh or Telangana can easily understand.",
        "en": "Respond in simple, clear, actionable English suitable for farmers and agriculturalists."
    }.get(language, "Respond in English.")

    system_context = (
        "You are an expert, compassionate agricultural scientist and crop disease specialist. "
        "Your advice should be practical, safe, eco-friendly, and easy for farmers to implement. "
        "Avoid recommending dangerous unapproved chemicals. Emphasize organic, cultural, and standard IPM practices. "
        f"{lang_instruction}"
    )

    if context_disease:
        full_prompt = (
            f"{system_context}\n\n"
            f"Context: The crop/disease diagnosed is: {context_disease}\n"
            f"Farmer's Question: {prompt}\n\n"
            "Please provide a helpful, concise, well-structured answer with bullet points if appropriate."
        )
    else:
        full_prompt = (
            f"{system_context}\n\n"
            f"Farmer's Question: {prompt}\n\n"
            "Please provide a helpful, concise, well-structured answer."
        )

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 800,
        }
    }

    last_error = None
    for model_id in MODELS_TO_TRY:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={GEMINI_API_KEY}"
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
        except Exception as e:
            last_error = e
            logger.warning("Gemini model %s query failed: %s", model_id, e)

    return f"Unable to fetch AI response at this moment: {last_error}"
