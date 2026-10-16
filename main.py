"""Person 2 webcam app. Renderer/behaviour can be supplied by an adapter module."""
import argparse
import csv
import importlib
import time
from pathlib import Path

from hand_features import FEATURE_NAMES, HandTracker, normalize_landmarks
from interaction_rules import InteractionRules
from predict_gestures import CommandGate, GesturePredictor

LABEL_KEYS = {ord("1"): "OPEN_PALM", ord("2"): "THUMBS_UP", ord("3"): "FIST", ord("4"): "OTHER"}
ACTION_KEYS = {ord("j"): "JUMP", ord("h"): "HAPPY", ord("s"): "SLEEP",
               ord("a"): "ANGRY", ord("p"): "PET", ord("f"): "FEED"}


class PreviewPet:
    """Integration placeholder, replaced with Person 1's adapter."""
    def __init__(self):
        self.state = "IDLE"
        self.until = 0
        self.bounds = (0, 0, 160, 160)

    def handle_event(self, event, now):
        self.state, self.until = event["action"], now + 1.5

    def update(self, now):
        if now >= self.until:
            self.state = "IDLE"

    def get_bounds(self):
        return self.bounds

    def render(self, frame, state, now):
        import cv2
        height, width = frame.shape[:2]
        self.bounds = (width // 2 - 80, max(0, height - 190), 160, 160)
        x, y, w, h = self.bounds
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 220, 255), 2)
        cv2.putText(frame, "PET PLACEHOLDER", (x, y-12), 0, 0.45, (0, 220, 255), 1)
        cv2.putText(frame, str(state), (x+10, y+85), 0, 0.6, (0, 220, 255), 2)
        return frame


def main(collect=False):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--hand-model", default="models/hand_landmarker.task")
    parser.add_argument("--model", default="models/pet_gesture_model.joblib")
    parser.add_argument("--keyboard-only", action="store_true")
    parser.add_argument("--adapter", help="Module exposing create_pet() -> (behaviour, renderer)")
    parser.add_argument("--participant")
    parser.add_argument("--session")
    parser.add_argument("--data", default="data/gesture_dataset.csv")
    parser.add_argument("--metrics", default="data/live_metrics.csv")
    args = parser.parse_args()
    if collect and (not args.participant or not args.session or args.keyboard_only):
        parser.error("Collection requires --participant and --session, with hand tracking enabled")
    import cv2
    tracker = camera = dataset = metrics = None
    try:
        if not args.keyboard_only:
            tracker = HandTracker(args.hand_model)
        predictor = (GesturePredictor(args.model)
                     if not collect and tracker and Path(args.model).is_file() else None)
        if args.adapter:
            behaviour, renderer = importlib.import_module(args.adapter).create_pet()
        else:
            behaviour = renderer = PreviewPet()
        gate, rules = CommandGate(), InteractionRules()
        if collect:
            path = Path(args.data)
            path.parent.mkdir(parents=True, exist_ok=True)
            exists = path.is_file() and path.stat().st_size > 0
            fields = ["participant", "session", "timestamp", "label"] + FEATURE_NAMES
            if exists:
                with path.open(newline="", encoding="utf-8") as existing:
                    if next(csv.reader(existing), None) != fields:
                        raise ValueError("Existing dataset has an incompatible header")
            dataset = path.open("a", newline="", encoding="utf-8")
            writer = csv.writer(dataset)
            if not exists:
                writer.writerow(fields)
        metric_path = Path(args.metrics)
        metric_path.parent.mkdir(parents=True, exist_ok=True)
        has_metrics = metric_path.exists() and metric_path.stat().st_size > 0
        metrics = metric_path.open("a", newline="", encoding="utf-8")
        metric_writer = csv.writer(metrics)
        if not has_metrics:
            metric_writer.writerow(["timestamp", "fps", "processing_ms", "action", "event_to_render_ms"])
        camera = cv2.VideoCapture(args.camera)
        if not camera.isOpened():
            raise RuntimeError(f"Cannot open camera {args.camera}")
        label, recording, count, last_sample = "OTHER", False, 0, float("-inf")
        last_frame, last_metric = time.monotonic(), 0.0
        while True:
            ok, frame = camera.read()
            if not ok:
                raise RuntimeError("Camera stopped returning frames")
            started = time.monotonic()
            frame = cv2.flip(frame, 1)
            camera_frame = frame.copy()
            hands = tracker.detect(frame, started) if tracker else []
            # Reject multiple hands to prevent mixing identities and trajectories.
            hand = hands[0] if len(hands) == 1 else None
            prediction, confidence = (predictor.predict(hand) if hand is not None and predictor else ("OTHER", 0.0))
            event = gate.update(prediction, started)
            if hand is not None:
                height, width = frame.shape[:2]
                for p in hand:
                    cv2.circle(frame, (int(p[0]*width), int(p[1]*height)), 3, (0, 255, 0), -1)
                point = (float(hand[8, 0]*width), float(hand[8, 1]*height))
                if collect and recording and started - last_sample >= 0.15:
                    writer.writerow([args.participant, args.session, started, label, *normalize_landmarks(hand)])
                    dataset.flush()
                    last_sample, count = started, count + 1
            else:
                point = None
            if not collect:
                motion = rules.motion(point, renderer.get_bounds(), started)
                feed = rules.feeding(camera_frame, renderer.get_bounds(), started)
                event = motion or feed or event
            if event:
                event["confidence"] = confidence if event["action"] in ("JUMP", "SLEEP", "HAPPY") else None
                behaviour.handle_event(event, started)
            behaviour.update(started)
            frame = renderer.render(frame, behaviour.state, started)
            finished = time.monotonic()
            fps = 1 / max(finished - last_frame, 1e-6)
            last_frame = finished
            if event or finished - last_metric >= 1:
                metric_writer.writerow([started, fps, (finished-started)*1000,
                                        event["action"] if event else "",
                                        (finished-event["timestamp"])*1000 if event else ""])
                metrics.flush()
                last_metric = finished
            status = (f"{label} recording={recording} samples={count} | 1-4 label, R record" if collect
                      else f"{prediction} {confidence:.2f} | model={'loaded' if predictor else 'none'}")
            cv2.putText(frame, status, (10, 25), 0, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"{fps:.1f} FPS | Q exit | J/H/S/A/P/F actions", (10, 48), 0, 0.5, (255,255,255), 1)
            cv2.imshow("Virtual pet - Person 2", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27) or cv2.getWindowProperty("Virtual pet - Person 2", cv2.WND_PROP_VISIBLE) < 1:
                break
            if collect:
                if key in LABEL_KEYS:
                    label = LABEL_KEYS[key]
                    recording = False
                elif key == ord("r"):
                    recording = not recording
            elif key in ACTION_KEYS:
                now = time.monotonic()
                behaviour.handle_event({"action": ACTION_KEYS[key], "timestamp": now}, now)
    except (RuntimeError, ValueError, FileNotFoundError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    finally:
        if camera is not None:
            camera.release()
        if tracker is not None:
            tracker.close()
        for file in (dataset, metrics):
            if file is not None:
                file.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
