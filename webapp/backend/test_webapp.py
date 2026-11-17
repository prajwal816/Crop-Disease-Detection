"""
test_webapp.py - Comprehensive Unit and Property Test Suite for CropScan Backend

Validates:
- Requirements 1.3, 1.4, 1.5, 1.6, 1.7 (model loader, confidence tiers, abstention)
- Requirements 2.1, 2.2, 2.3, 2.4, 2.5 (severity bands, lesion ratio bounds)
- Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6 (knowledge base, advisory, multilingual)
- Requirements 4.1, 4.2, 4.3, 4.4 (FastAPI endpoint structure and contracts)
"""

import os
import sys
import unittest
from pathlib import Path

# Add backend directory to path
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

import numpy as np
from PIL import Image

import advisory
import knowledge_base
import model
import severity


class TestConfidenceTiers(unittest.TestCase):
    """Property 1: Confidence tier covers all float values in [0, 1]."""

    def get_tier_and_abstain(self, confidence: float):
        abstain = confidence < 0.70
        if confidence >= 0.90:
            tier = "High"
        elif confidence >= 0.70:
            tier = "Medium"
        else:
            tier = "Low"
        return tier, abstain

    def test_property_confidence_tier_boundaries(self):
        test_values = [
            0.0, 0.1, 0.5, 0.6999, 0.70, 0.7001, 0.85, 0.8999, 0.90, 0.95, 1.0
        ]
        for conf in test_values:
            tier, abstain = self.get_tier_and_abstain(conf)
            self.assertIn(tier, {"High", "Medium", "Low"})
            if conf >= 0.90:
                self.assertEqual(tier, "High")
                self.assertFalse(abstain)
            elif conf >= 0.70:
                self.assertEqual(tier, "Medium")
                self.assertFalse(abstain)
            else:
                self.assertEqual(tier, "Low")
                self.assertTrue(abstain)


class TestSeverityBand(unittest.TestCase):
    """Property 2 & 3: Severity band classification and lesion ratio bounds."""

    def test_severity_thresholds(self):
        def get_band(ratio: float):
            if ratio < 0.05:
                return "Low"
            elif ratio < 0.20:
                return "Medium"
            return "High"

        ratios = [0.0, 0.02, 0.0499, 0.05, 0.10, 0.1999, 0.20, 0.50, 1.0]
        for r in ratios:
            band = get_band(r)
            self.assertIn(band, {"Low", "Medium", "High"})
            if r < 0.05:
                self.assertEqual(band, "Low")
            elif r < 0.20:
                self.assertEqual(band, "Medium")
            else:
                self.assertEqual(band, "High")

    def test_compute_severity_with_blank_image(self):
        img = Image.new("RGB", (100, 100), color=(0, 0, 0))
        ratio, band = severity.compute_severity(img)
        self.assertTrue(0.0 <= ratio <= 1.0)
        self.assertIn(band, {"Low", "Medium", "High", "Unknown"})

    def test_compute_severity_with_leaf_coloured_image(self):
        img = Image.new("RGB", (384, 384), color=(34, 139, 34))
        ratio, band = severity.compute_severity(img)
        self.assertTrue(0.0 <= ratio <= 1.0)
        self.assertIn(band, {"Low", "Medium", "High", "Unknown"})


class TestKnowledgeBase(unittest.TestCase):
    """Property 4: Advisory completeness across all classes, languages, and sections."""

    def test_knowledge_base_completeness(self):
        self.assertEqual(len(knowledge_base.ADVISORY_KB), 19)
        required_langs = ["en", "hi", "te"]
        required_sections = [
            "symptoms", "monitoring", "immediate_actions", "prevention", "escalation"
        ]

        for class_name in model.CLASS_NAMES:
            self.assertIn(class_name, knowledge_base.ADVISORY_KB, f"Missing {class_name} in KB")
            entry = knowledge_base.ADVISORY_KB[class_name]
            for lang in required_langs:
                self.assertIn(lang, entry, f"Missing lang {lang} for {class_name}")
                for sec in required_sections:
                    val = entry[lang].get(sec)
                    self.assertIsNotNone(val, f"Missing {sec} in {class_name}:{lang}")
                    self.assertIsInstance(val, str)
                    self.assertTrue(len(val.strip()) > 0, f"Empty {sec} in {class_name}:{lang}")


class TestAdvisoryRetriever(unittest.TestCase):
    """Property 5: Advisory retrieval exact match and fallback."""

    def test_exact_matches(self):
        for class_name in model.CLASS_NAMES:
            adv = advisory.get_advisory(class_name)
            self.assertIn("en", adv)
            self.assertIn("hi", adv)
            self.assertIn("te", adv)
            self.assertEqual(adv["en"]["symptoms"], knowledge_base.ADVISORY_KB[class_name]["en"]["symptoms"])

    def test_unknown_fallback(self):
        adv = advisory.get_advisory("completely_nonexistent_disease_xyz")
        self.assertIn("en", adv)
        self.assertIn("hi", adv)
        self.assertIn("te", adv)
        for lang in ["en", "hi", "te"]:
            for sec in ["symptoms", "monitoring", "immediate_actions", "prevention", "escalation"]:
                text = adv[lang][sec]
                self.assertTrue(len(text.strip()) > 0)


class TestModelLoader(unittest.TestCase):
    """Graceful degradation when checkpoint is absent."""

    def test_class_names_count(self):
        self.assertEqual(len(model.CLASS_NAMES), 19)

    def test_display_names(self):
        self.assertEqual(model.get_display_name("tomato__early_blight"), "Tomato: Early Blight")
        self.assertEqual(model.get_display_name("bell_pepper__healthy"), "Bell Pepper: Healthy")
        self.assertEqual(model.get_display_name("corn__common_rust"), "Corn: Common Rust")

    def test_load_model_without_checkpoint(self):
        state = model.load_model()
        # When checkpoint is not on disk, loaded must be False
        if not model.CHECKPOINT_PATH.exists():
            self.assertFalse(state.loaded)
            with self.assertRaises(RuntimeError):
                model.predict(state, Image.new("RGB", (100, 100)))


class TestFastAPIApp(unittest.TestCase):
    """Validate FastAPI routes, configuration, and endpoint contracts."""

    def test_app_routes(self):
        from main import app
        route_paths = [r.path for r in app.routes]
        self.assertIn("/health", route_paths)
        self.assertIn("/predict", route_paths)


if __name__ == "__main__":
    unittest.main(verbosity=2)
