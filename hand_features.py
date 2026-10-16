"""Shared feature contract: wrist-relative xyz, divided by palm length."""
from pathlib import Path
import numpy as np

FEATURE_VERSION = "wrist-palm-xyz-v1"
FEATURE_NAMES = [f"{axis}{i}" for i in range(21) for axis in "xyz"]


def normalize_landmarks(points):
    points = np.asarray(points, dtype=np.float32)
    if points.shape != (21, 3) or not np.isfinite(points).all():
        raise ValueError("Expected 21 finite xyz landmarks")
    relative = points - points[0]
    scale = np.linalg.norm(relative[9])
    if scale < 1e-6:
        raise ValueError("Degenerate hand landmarks")
    return (relative / scale).reshape(63)


class HandTracker:
    def __init__(self, model_path):
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        if not Path(model_path).is_file():
            raise FileNotFoundError(f"Missing hand model: {model_path}. See PERSON_2_README.md")
        self.mp = mp
        self.last_ms = -1
        self.detector = vision.HandLandmarker.create_from_options(
            vision.HandLandmarkerOptions(
                base_options=python.BaseOptions(model_asset_path=str(model_path)),
                running_mode=vision.RunningMode.VIDEO, num_hands=2))

    def detect(self, frame, now):
        import cv2
        timestamp = max(self.last_ms + 1, int(now * 1000))
        self.last_ms = timestamp
        result = self.detector.detect_for_video(
            self.mp.Image(image_format=self.mp.ImageFormat.SRGB,
                          data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), timestamp)
        return [np.array([[p.x, p.y, p.z] for p in hand], dtype=np.float32)
                for hand in result.hand_landmarks]

    def close(self):
        self.detector.close()
