"""Convert official HaGRID image annotations to the webcam feature contract."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import random
import numpy as np
from hand_features import FEATURE_NAMES, FEATURE_VERSION, ImageHandTracker, normalize_landmarks

LABELS = {"palm": "OPEN_PALM", "like": "THUMBS_UP", "fist": "FIST",
          "no_gesture": "OTHER", "peace": "OTHER", "one": "OTHER", "ok": "OTHER"}
FIELDS = ["participant", "session", "timestamp", "label", "split", "source_image", "source_label", *FEATURE_NAMES]


def mirror_box(box):
    x, y, w, h = box
    return (1-x-w, y, w, h)


def iou(a, b):
    x, y = max(a[0], b[0]), max(a[1], b[1])
    right, bottom = min(a[0]+a[2], b[0]+b[2]), min(a[1]+a[3], b[1]+b[3])
    intersection = max(0, right-x) * max(0, bottom-y)
    return intersection / max(a[2]*a[3] + b[2]*b[3] - intersection, 1e-12)


def match_hands(hands, boxes, min_iou=0.2):
    """Conservative mutual-best association; never assign a hand twice."""
    if not hands or not boxes:
        return {}
    hand_boxes = []
    for hand in hands:
        low, high = hand[:, :2].min(axis=0), hand[:, :2].max(axis=0)
        hand_boxes.append((*low, *(high-low)))
    scores = np.array([[iou(h, b) for b in boxes] for h in hand_boxes])
    matches = {}
    for hand_index in range(len(hands)):
        box_index = int(scores[hand_index].argmax())
        if (scores[hand_index, box_index] >= min_iou
                and scores[:, box_index].argmax() == hand_index):
            matches[box_index] = hand_index
    return matches


def load_records(root, sources):
    records, user_splits, image_splits = [], {}, {}
    for split in ("train", "val", "test"):
        for source in sources:
            path = root / split / f"{source}.json"
            if not path.is_file():
                raise ValueError(f"Missing annotation file: {path}")
            entries = json.loads(path.read_text(encoding="utf-8"))
            for image_id, entry in sorted(entries.items()):
                user = str(entry.get("user_id", "")).strip()
                boxes, labels = entry.get("bboxes", []), entry.get("labels", [])
                if not user or len(boxes) != len(labels) or not boxes:
                    raise ValueError(f"Invalid user/boxes/labels: {path}: {image_id}")
                if user in user_splits and user_splits[user] != split:
                    raise ValueError(f"Participant leakage across splits: {user}")
                if image_id in image_splits and image_splits[image_id] != split:
                    raise ValueError(f"Image leakage across splits: {image_id}")
                for box in boxes:
                    if (len(box) != 4 or not np.isfinite(box).all()
                            or min(box) < 0 or box[2] <= 0 or box[3] <= 0
                            or box[0]+box[2] > 1.001 or box[1]+box[3] > 1.001):
                        raise ValueError(f"Invalid normalized xywh box: {image_id}")
                user_splits[user], image_splits[image_id] = split, split
                records.append((split, source, image_id, user, boxes, labels))
    return records


def convert(args, tracker):
    import cv2
    records = load_records(args.annotations, args.sources)
    random.Random(args.seed).shuffle(records)
    counts, by_user, reasons = Counter(), Counter(), Counter()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation protects existing features and audit results.
    with args.output.open("x", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writeheader()
        preview_counts = Counter()
        for split, source, image_id, user, boxes, labels in records:
            eligible = [i for i, label in enumerate(labels) if label in LABELS
                        and counts[split, LABELS[label]] < args.limit
                        and by_user[split, LABELS[label], user] < args.per_person]
            if not eligible:
                continue
            # Official directory layout: images/<gesture>/<image-id>.jpg
            image_path = args.images / source / f"{image_id}.jpg"
            if not image_path.resolve().is_relative_to(args.images.resolve()):
                raise ValueError("Image path escapes dataset root")
            frame = cv2.imread(str(image_path)) if image_path.is_file() else None
            if frame is None:
                reasons["missing_or_unreadable_image"] += 1
                continue
            frame = cv2.flip(frame, 1)  # Exactly the webcam's displayed convention.
            mirrored = [mirror_box(box) for box in boxes]
            hands = tracker.detect(frame)
            matches = match_hands(hands, mirrored, args.min_iou)
            if not hands:
                reasons["no_hand_detected"] += 1
            for i in eligible:
                label = LABELS[labels[i]]
                if counts[split, label] >= args.limit or by_user[split, label, user] >= args.per_person:
                    continue
                if i not in matches:
                    reasons["unmatched_annotation"] += 1
                    continue
                try:
                    features = normalize_landmarks(hands[matches[i]])
                except ValueError:
                    reasons["invalid_landmarks"] += 1
                    continue
                writer.writerow(dict(participant=f"hagrid:{user}", session="hagrid",
                                     timestamp="", label=label, split=split,
                                     source_image=f"{source}/{image_id}", source_label=labels[i],
                                     **dict(zip(FEATURE_NAMES, features))))
                counts[split, label] += 1
                by_user[split, label, user] += 1
                if preview_counts[split, label] < args.previews:
                    preview = frame.copy()
                    height, width = preview.shape[:2]
                    x, y, w, h = mirrored[i]
                    cv2.rectangle(preview, (int(x*width), int(y*height)),
                                  (int((x+w)*width), int((y+h)*height)), (0, 255, 255), 2)
                    for p in hands[matches[i]]:
                        cv2.circle(preview, (int(p[0]*width), int(p[1]*height)), 3, (0, 255, 0), -1)
                    cv2.putText(preview, f"{split} {labels[i]} -> {label}", (15, 35), 0, 0.7, (0,255,255), 2)
                    folder = args.output.parent / (args.output.stem + "_previews")
                    folder.mkdir(exist_ok=True)
                    cv2.imwrite(str(folder / f"{split}_{label}_{preview_counts[split,label]}.jpg"), preview)
                    preview_counts[split, label] += 1
    report = {"feature_version": FEATURE_VERSION, "seed": args.seed,
              "counts": {f"{s}/{label}": counts[s, label] for s in ("train", "val", "test")
                         for label in sorted(set(LABELS.values()))},
              "participants": {f"{s}/{label}": sum(1 for key in by_user if key[:2] == (s, label))
                               for s, label in counts},
              "skips": dict(reasons), "mirrored": True, "min_iou": args.min_iou,
              "source": "https://github.com/hukenovs/hagrid", "source_classes": args.sources}
    args.output.with_suffix(".import.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", type=Path, required=True, help="Root containing train/val/test JSON folders")
    parser.add_argument("--images", type=Path, required=True, help="Root containing gesture image folders")
    parser.add_argument("--sources", nargs="+", choices=sorted(LABELS), default=["palm", "like", "fist", "no_gesture"])
    parser.add_argument("--hand-model", default="models/hand_landmarker.task")
    parser.add_argument("--output", type=Path, default=Path("data/hagrid_features.csv"))
    parser.add_argument("--limit", type=int, default=1000, help="Maximum usable hands per project class per split")
    parser.add_argument("--per-person", type=int, default=10)
    parser.add_argument("--previews", type=int, default=5, help="Saved annotated images per class per split")
    parser.add_argument("--min-iou", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.limit < 1 or args.per_person < 1 or args.previews < 0 or not 0 < args.min_iou <= 1:
        parser.error("Invalid limits or IoU")
    tracker = None
    try:
        # Validate metadata before constructing the model or touching output.
        load_records(args.annotations, args.sources)
        tracker = ImageHandTracker(args.hand_model)
        convert(args, tracker)
    except (ValueError, FileExistsError, FileNotFoundError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    finally:
        if tracker:
            tracker.close()


if __name__ == "__main__":
    main()
