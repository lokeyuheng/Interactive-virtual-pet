"""Group-held-out training. Threshold tuning requires separate validation data."""
import argparse
import csv
import json
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GroupShuffleSplit
from hand_features import FEATURE_NAMES, FEATURE_VERSION


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/gesture_dataset.csv")
    parser.add_argument("--output", default="models/pet_gesture_model.joblib")
    parser.add_argument("--group-by", choices=["participant", "session"], default="participant")
    args = parser.parse_args()
    with open(args.data, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        parser.error("Dataset is empty")
    x = np.array([[float(r[k]) for k in FEATURE_NAMES] for r in rows])
    y = np.array([r["label"] for r in rows])
    groups = np.array([r["participant"] if args.group_by == "participant" else
                       r["participant"] + "/" + r["session"] for r in rows])
    if len(set(groups)) < 2:
        parser.error("Collect at least two independent groups; preferably several participants")
    train, test = next(GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42).split(x, y, groups))
    required = {"OPEN_PALM", "THUMBS_UP", "FIST", "OTHER"}
    if not required.issubset(set(y[train])) or not required.issubset(set(y[test])):
        parser.error("Each split must contain all four classes. Collect every class in every group.")
    model = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42, n_jobs=1)
    model.fit(x[train], y[train])
    predictions = model.predict(x[test])
    report = {"accuracy": accuracy_score(y[test], predictions),
              "classification_report": classification_report(y[test], predictions, output_dict=True, zero_division=0),
              "labels": model.classes_.tolist(),
              "confusion_matrix": confusion_matrix(y[test], predictions, labels=model.classes_).tolist(),
              "group_by": args.group_by, "train_groups": sorted(set(groups[train])),
              "test_groups": sorted(set(groups[test])),
              "train_rows": train.tolist(), "test_rows": test.tolist()}
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_version": FEATURE_VERSION,
                 "feature_names": FEATURE_NAMES}, path)
    path.with_suffix(".evaluation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(classification_report(y[test], predictions, zero_division=0))
    print(f"Saved {path}; held-out accuracy: {report['accuracy']:.3f}")


if __name__ == "__main__":
    main()
