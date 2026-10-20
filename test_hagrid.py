"""HaGRID fixtures test conversion and leakage prevention, not gesture accuracy."""
import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import cv2
import numpy as np
from hand_features import FEATURE_NAMES
from import_hagrid import convert, load_records, match_hands, mirror_box
from train_gestures import predefined_split


def hand_at(x):
    return np.array([[x + (i % 5)*0.06, 0.22 + (i//5)*0.1, i*0.001]
                     for i in range(21)], dtype=np.float32)


class HagridTests(unittest.TestCase):
    def test_mirrored_annotation_matching(self):
        boxes = [mirror_box([0.1, 0.2, 0.3, 0.5]), mirror_box([0.6, 0.2, 0.3, 0.5])]
        self.assertEqual(match_hands([hand_at(0.12), hand_at(0.62)], boxes), {1: 0, 0: 1})
        self.assertEqual(match_hands([], boxes), {})

    def test_user_and_image_leakage_rejected(self):
        for field in ("participant", "source_image"):
            rows = [{"participant": "a", "source_image": "x", "split": "train"},
                    {"participant": "b", "source_image": "y", "split": "val"}]
            rows[1][field] = rows[0][field]
            with self.assertRaisesRegex(ValueError, "leakage"):
                predefined_split(rows)

    def test_import_features_previews_and_failure_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            images, annotations = root / "images", root / "annotations"
            (images / "palm").mkdir(parents=True)
            for split in ("train", "val", "test"):
                (annotations / split).mkdir(parents=True)
                entries = {}
                for suffix in ("ok", "missing"):
                    image_id = f"{split}_{suffix}"
                    entries[image_id] = dict(user_id=split, labels=["palm"], bboxes=[[0.1, 0.2, 0.3, 0.5]])
                    if suffix == "ok":
                        cv2.imwrite(str(images / "palm" / f"{image_id}.jpg"), np.zeros((100, 100, 3), np.uint8))
                (annotations / split / "palm.json").write_text(json.dumps(entries))
            class FakeTracker:
                def detect(self, frame):
                    return [hand_at(0.62)]
            args = argparse.Namespace(annotations=annotations, images=images, sources=["palm"],
                                      output=root / "features.csv", seed=42, limit=20,
                                      per_person=10, min_iou=0.2, previews=1)
            convert(args, FakeTracker())
            with args.output.open() as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(len(rows), 3)
            self.assertEqual({r["split"] for r in rows}, {"train", "val", "test"})
            self.assertTrue(all(r["label"] == "OPEN_PALM" for r in rows))
            self.assertEqual(len(list((root / "features_previews").glob("*.jpg"))), 3)
            report = json.loads(args.output.with_suffix(".import.json").read_text())
            self.assertEqual(report["skips"]["missing_or_unreadable_image"], 3)
            with self.assertRaises(FileExistsError):
                convert(args, FakeTracker())
            bad = json.loads((annotations / "val/palm.json").read_text())
            bad["val_ok"]["user_id"] = "train"
            (annotations / "val/palm.json").write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError, "leakage"):
                load_records(annotations, ["palm"])

    def test_official_split_training_and_threshold_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data, output = root / "data.csv", root / "model.joblib"
            with data.open("w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["participant", "session", "split", *FEATURE_NAMES, "label"])
                for split in ("train", "val", "test"):
                    for i, label in enumerate(["OTHER", "FIST", "THUMBS_UP", "OPEN_PALM"]):
                        writer.writerow([split, "fixture", split, *([i]*63), label])
            command = [sys.executable, "train_gestures.py", "--data", str(data), "--output", str(output)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.with_suffix(".evaluation.json").read_text())
            self.assertEqual(report["evaluation_split"], "val")
            self.assertNotIn("final_test", report)
            from predict_gestures import GesturePredictor
            self.assertEqual(GesturePredictor(output).threshold, report["threshold"])
            result = subprocess.run([*command, "--evaluate-test"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.with_suffix(".evaluation.json").read_text())
            self.assertIn("final_test", report)


if __name__ == "__main__":
    unittest.main()
