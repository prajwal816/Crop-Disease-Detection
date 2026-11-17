"""
RAG advisory retriever for the Main19 crop disease classifier.
Ported from notebook 11: rag_multilingual_advisory.ipynb

Uses TF-IDF with bigrams over English KB text.
Prioritises exact class-name lookup; falls back to nearest-neighbour retrieval.
"""
import logging
from typing import Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from knowledge_base import ADVISORY_KB

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Five advisory section keys (must match knowledge_base.py)
# ---------------------------------------------------------------------------
ADVISORY_SECTIONS = ["symptoms", "monitoring", "immediate_actions", "prevention", "escalation"]
ADVISORY_LANGUAGES = ["en", "hi", "te"]

# ---------------------------------------------------------------------------
# Fallback advisory (used when no KB match is found)
# ---------------------------------------------------------------------------
FALLBACK: dict[str, dict[str, str]] = {
    "en": {
        "symptoms": "No specific advisory available for this class.",
        "monitoring": "Scout the crop regularly and document any changes.",
        "immediate_actions": "Avoid handling plants unnecessarily and maintain field hygiene.",
        "prevention": "Use clean planting material, practice crop rotation, and maintain good agronomic practices.",
        "escalation": "Consult a local agricultural extension officer or plant-health specialist.",
    },
    "hi": {
        "symptoms": "इस वर्ग के लिए कोई विशेष सलाह उपलब्ध नहीं है।",
        "monitoring": "फसल की नियमित निगरानी करें और किसी भी बदलाव को दर्ज करें।",
        "immediate_actions": "पौधों को अनावश्यक रूप से न छुएँ और खेत की स्वच्छता बनाए रखें।",
        "prevention": "स्वच्छ रोपण सामग्री का उपयोग करें, फसल चक्र अपनाएँ।",
        "escalation": "स्थानीय कृषि विस्तार अधिकारी से परामर्श लें।",
    },
    "te": {
        "symptoms": "ఈ తరగతికి నిర్దిష్ట సలహా అందుబాటులో లేదు.",
        "monitoring": "పంటను క్రమం తప్పకుండా పర్యవేక్షించండి మరియు ఏదైనా మార్పులను నమోదు చేయండి.",
        "immediate_actions": "మొక్కలను అనవసరంగా తాకకండి మరియు పొలం పరిశుభ్రత నిర్వహించండి.",
        "prevention": "శుభ్రమైన నాటు సామగ్రిని ఉపయోగించండి, పంట మార్పిడి చేయండి.",
        "escalation": "స్థానిక వ్యవసాయ విస్తరణ అధికారిని సంప్రదించండి.",
    },
}

# ---------------------------------------------------------------------------
# Build TF-IDF index at module load time
# (matches notebook 11 approach: 1-gram + bigram, lowercase)
# ---------------------------------------------------------------------------
_corpus: list[str] = []
_keys: list[str] = []
_vectorizer: Optional[TfidfVectorizer] = None
_tfidf_matrix = None


def _build_retrieval_document(cls_name: str, en_entry: dict[str, str]) -> str:
    """Combine label + all English sections into one retrieval document."""
    return " ".join([
        cls_name.replace("__", " "),
        en_entry.get("symptoms", ""),
        en_entry.get("monitoring", ""),
        en_entry.get("immediate_actions", ""),
        en_entry.get("prevention", ""),
        en_entry.get("escalation", ""),
    ])


def _build_index() -> None:
    global _corpus, _keys, _vectorizer, _tfidf_matrix
    _corpus = []
    _keys = []
    for cls_name, langs in ADVISORY_KB.items():
        en_entry = langs.get("en", {})
        doc = _build_retrieval_document(cls_name, en_entry)
        _corpus.append(doc)
        _keys.append(cls_name)
    _vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
    )
    _tfidf_matrix = _vectorizer.fit_transform(_corpus)
    logger.info("Advisory TF-IDF index built: %d entries, vocab=%d",
                len(_keys), len(_vectorizer.vocabulary_))


# Build at import time (fast - no network, no disk I/O)
try:
    _build_index()
except Exception:
    logger.exception("Failed to build advisory TF-IDF index")


def _make_fallback() -> dict[str, dict[str, str]]:
    """Return a full three-language fallback advisory dict."""
    return {lang: dict(FALLBACK[lang]) for lang in ADVISORY_LANGUAGES}


def get_advisory(class_name: str) -> dict[str, dict[str, str]]:
    """
    Return advisory for all three languages.

    Priority:
    1. Exact class-name lookup in ADVISORY_KB.
    2. TF-IDF nearest-neighbour (cosine similarity > 0.1).
    3. Generic fallback text in en / hi / te.

    Return shape: { "en": {section: text}, "hi": {...}, "te": {...} }
    """
    # 1. Exact match
    if class_name in ADVISORY_KB:
        return ADVISORY_KB[class_name]

    # 2. TF-IDF nearest-neighbour
    if _vectorizer is not None and _tfidf_matrix is not None:
        try:
            query = class_name.replace("_", " ").replace("__", " ")
            query_vec = _vectorizer.transform([query])
            sims = cosine_similarity(query_vec, _tfidf_matrix).flatten()
            best_idx = int(np.argmax(sims))
            if sims[best_idx] > 0.1:
                best_cls = _keys[best_idx]
                logger.warning(
                    "Advisory fallback via TF-IDF: '%s' -> '%s' (sim=%.3f)",
                    class_name, best_cls, sims[best_idx]
                )
                return ADVISORY_KB[best_cls]
        except Exception:
            logger.exception("TF-IDF advisory lookup failed for '%s'", class_name)

    # 3. Generic fallback
    logger.warning("No advisory match found for '%s'; using generic fallback", class_name)
    return _make_fallback()
