"""
Lesion grounding and visible severity proxy.
Ported from notebook 09: lesion_grounding_severity_proxy.ipynb

This is a computer-vision heuristic, NOT clinical severity.
Thresholds: Low < 5%, Medium 5-20%, High >= 20% lesion/leaf ratio.
"""
import logging
import numpy as np
import cv2
from PIL import Image

logger = logging.getLogger(__name__)

TARGET_SIZE = 384
MILD_THRESHOLD = 0.05    # 5%
MODERATE_THRESHOLD = 0.20  # 20%


def _pil_to_rgb(pil_image: Image.Image) -> np.ndarray:
    return np.array(pil_image.convert("RGB"))


def _keep_largest_component(mask: np.ndarray) -> np.ndarray:
    mask_u8 = mask.astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask_u8, connectivity=8)
    if n <= 1:
        return mask.astype(bool)
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    return (labels == largest)


def _clean_mask(mask: np.ndarray, kernel_size: int = 7, keep_largest: bool = True) -> np.ndarray:
    from scipy import ndimage
    u8 = mask.astype(np.uint8)
    k = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    u8 = cv2.morphologyEx(u8, cv2.MORPH_OPEN, k)
    u8 = cv2.morphologyEx(u8, cv2.MORPH_CLOSE, k)
    filled = ndimage.binary_fill_holes(u8 > 0)
    if keep_largest:
        filled = _keep_largest_component(filled.astype(np.uint8))
    return filled.astype(bool)


def estimate_leaf_mask(rgb: np.ndarray) -> np.ndarray:
    """Estimate visible leaf region using HSV + Lab colour separation (from nb09)."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]
    lab_a = lab[:, :, 1]
    lab_b = lab[:, :, 2]
    coloured = (sat >= 20) & (val >= 25)
    lab_tissue = (lab_a >= 90) & (lab_a <= 175) & (lab_b >= 80) & (lab_b <= 205)
    candidate = coloured & lab_tissue
    candidate = _clean_mask(candidate, kernel_size=7, keep_largest=True)
    if candidate.mean() < 0.03:
        # fallback
        fallback = (sat >= 18) & (val >= 20)
        candidate = _clean_mask(fallback, kernel_size=7, keep_largest=True)
    return candidate


def estimate_lesion_mask(rgb: np.ndarray, leaf_mask: np.ndarray) -> np.ndarray:
    """Conservative lesion-area proxy within leaf region (from nb09)."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    r = rgb[:, :, 0].astype(np.float32)
    g = rgb[:, :, 1].astype(np.float32)
    b = rgb[:, :, 2].astype(np.float32)
    hue = hsv[:, :, 0]
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]
    lab_a = lab[:, :, 1]
    lab_b = lab[:, :, 2]
    excess_green = 2 * g - r - b
    local_mean = cv2.GaussianBlur(gray, (0, 0), sigmaX=7)
    local_diff = cv2.absdiff(gray, local_mean)
    brown_yellow = (hue >= 8) & (hue <= 32) & (sat >= 55) & (val >= 35) & (val <= 210) & (excess_green < 15)
    dark_abnormality = (val >= 35) & (val <= 135) & (sat >= 35) & (local_diff >= 18) & (lab_a >= 105) & (lab_b >= 110)
    chlorosis = (lab_b >= 140) & (lab_a >= 95) & (sat >= 40) & (local_diff >= 14) & (excess_green < 25)
    lesion = (brown_yellow | dark_abnormality | chlorosis) & leaf_mask
    # Remove border
    border = 8
    lesion[:border, :] = False
    lesion[-border:, :] = False
    lesion[:, :border] = False
    lesion[:, -border:] = False
    # Remove small components
    u8 = lesion.astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(u8, connectivity=8)
    cleaned = np.zeros_like(u8)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 45:
            cleaned[labels == i] = 1
    lesion = _clean_mask(cleaned > 0, kernel_size=3, keep_largest=False)
    return lesion & leaf_mask


def compute_severity(pil_image: Image.Image) -> tuple[float, str]:
    """
    Return (lesion_ratio, severity_band).
    severity_band: "Low" | "Medium" | "High" | "Unknown"
    Falls back to (0.0, "Unknown") on any error or empty mask.
    """
    try:
        rgb = _pil_to_rgb(pil_image.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS))
        leaf = estimate_leaf_mask(rgb)
        leaf_px = int(leaf.sum())
        if leaf_px == 0:
            return 0.0, "Unknown"
        lesion = estimate_lesion_mask(rgb, leaf)
        lesion_px = int(lesion.sum())
        ratio = lesion_px / leaf_px
        # Clamp to [0,1]
        ratio = max(0.0, min(1.0, ratio))
        if ratio < MILD_THRESHOLD:
            band = "Low"
        elif ratio < MODERATE_THRESHOLD:
            band = "Medium"
        else:
            band = "High"
        return round(ratio, 4), band
    except Exception:
        logger.exception("Severity computation failed")
        return 0.0, "Unknown"
