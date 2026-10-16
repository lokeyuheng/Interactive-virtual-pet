"""Deterministic checks; these do not measure real-world recognition accuracy."""
import unittest
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import numpy as np
from hand_features import normalize_landmarks
from predict_gestures import CommandGate
from interaction_rules import InteractionRules


class PipelineTests(unittest.TestCase):
    def test_training_and_saved_model_contract(self):
        # Synthetic fixtures verify plumbing only, never recognition quality.
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory) / "examples.csv"
            model = Path(directory) / "model.joblib"
            from hand_features import FEATURE_NAMES
            with data.open("w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["participant", "session", "timestamp", "label", *FEATURE_NAMES])
                for participant in range(4):
                    for index, label in enumerate(["OTHER", "FIST", "OPEN_PALM", "THUMBS_UP"]):
                        for sample in range(5):
                            writer.writerow([participant, "s1", sample, label, *([index] * 63)])
            result = subprocess.run([sys.executable, "train_gestures.py", "--data", str(data),
                                     "--output", str(model)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            from predict_gestures import GesturePredictor
            GesturePredictor(model)
            report = json.loads(model.with_suffix(".evaluation.json").read_text())
            self.assertFalse(set(report["train_groups"]) & set(report["test_groups"]))

    def test_features_ignore_translation_and_uniform_scale(self):
        points = np.arange(63, dtype=float).reshape(21, 3)
        np.testing.assert_allclose(normalize_landmarks(points),
                                   normalize_landmarks(points * 3 + 10), atol=1e-6)

    def test_invalid_hand_rejected(self):
        with self.assertRaises(ValueError):
            normalize_landmarks(np.zeros((21, 3)))

    def test_held_command_needs_release(self):
        gate = CommandGate()
        self.assertIsNone(gate.update("FIST", 0))
        self.assertEqual(gate.update("FIST", 0.4)["action"], "SLEEP")
        self.assertIsNone(gate.update("FIST", 4))
        gate.update("OTHER", 4.1)
        gate.update("OTHER", 4.4)
        gate.update("FIST", 4.5)
        self.assertEqual(gate.update("FIST", 4.9)["action"], "SLEEP")

    def test_wave_and_tracking_loss(self):
        rules = InteractionRules()
        events = [rules.motion((x, 50), (0, 0, 200, 200), i*0.15)
                  for i, x in enumerate([20, 130, 20, 130, 20, 130])]
        self.assertTrue(any(e and e["action"] == "ANGRY" for e in events))
        rules.motion(None, (0, 0, 200, 200), 1)
        self.assertEqual(len(rules.history), 0)

    def test_pet_must_be_near_pet(self):
        rules = InteractionRules()
        events = [rules.motion((x, 500), (0, 0, 200, 200), i*0.15)
                  for i, x in enumerate([30, 45, 60, 75, 60, 45])]
        self.assertFalse(any(events))


if __name__ == "__main__":
    unittest.main()
