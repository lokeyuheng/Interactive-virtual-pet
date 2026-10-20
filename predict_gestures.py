"""Classifier loading and time-based command stabilization."""
from hand_features import FEATURE_VERSION, normalize_landmarks

ACTION_MAP = {"THUMBS_UP": "JUMP", "FIST": "SLEEP", "OPEN_PALM": "HAPPY"}


class GesturePredictor:
    def __init__(self, path, confidence=None):
        import joblib
        bundle = joblib.load(path)  # Only load trusted local model files.
        if bundle.get("feature_version") != FEATURE_VERSION:
            raise ValueError("Model preprocessing does not match this application")
        self.model = bundle["model"]
        self.threshold = bundle.get("confidence_threshold", 0.75) if confidence is None else confidence

    def predict(self, points):
        probabilities = self.model.predict_proba([normalize_landmarks(points)])[0]
        index = probabilities.argmax()
        score = float(probabilities[index])
        return (str(self.model.classes_[index]) if score >= self.threshold else "OTHER", score)


class CommandGate:
    def __init__(self, stable_seconds=0.3, release_seconds=0.25, cooldown=1.0):
        self.stable = stable_seconds
        self.release = release_seconds
        self.cooldown = cooldown
        self.candidate = None
        self.since = 0.0
        self.latched = False
        self.neutral_since = None
        self.last_event = float("-inf")

    def update(self, label, now):
        if label not in ACTION_MAP:
            if self.neutral_since is None:
                self.neutral_since = now
            if now - self.neutral_since >= self.release:
                self.latched = False
            self.candidate = None
            return None
        self.neutral_since = None
        if label != self.candidate:
            self.candidate, self.since = label, now
        if (not self.latched and now - self.since >= self.stable
                and now - self.last_event >= self.cooldown):
            self.latched, self.last_event = True, now
            return {"action": ACTION_MAP[label], "timestamp": now}
        return None
