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

REQUIRED = {"OPEN_PALM", "THUMBS_UP", "FIST", "OTHER"}


def predefined_split(rows):
    if any(r.get("split") not in {"train", "val", "test"} for r in rows):
        raise ValueError("Every row needs split=train, val or test")
    for field in ("participant", "source_image"):
        seen = {}
        for row in rows:
            value = row.get(field)
            if field == "participant" and not value:
                raise ValueError("Missing participant ID")
            if value and value in seen and seen[value] != row["split"]:
                raise ValueError(f"{field} leakage across splits: {value}")
            if value:
                seen[value] = row["split"]
    return {split: np.array([i for i, row in enumerate(rows) if row["split"] == split], dtype=int)
            for split in ("train", "val", "test")}


def evaluate(model, x, y, threshold):
    probabilities = model.predict_proba(x)
    predictions = model.classes_[probabilities.argmax(axis=1)].copy()
    predictions[probabilities.max(axis=1) < threshold] = "OTHER"
    return {"accuracy": accuracy_score(y, predictions),
            "classification_report": classification_report(y, predictions, output_dict=True, zero_division=0),
            "labels": model.classes_.tolist(),
            "confusion_matrix": confusion_matrix(y, predictions, labels=model.classes_).tolist()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/gesture_dataset.csv")
    parser.add_argument("--output", default="models/pet_gesture_model.joblib")
    parser.add_argument("--group-by", choices=["participant", "session"], default="participant")
    parser.add_argument("--evaluate-test", action="store_true", help="Evaluate final untouched test split after settings are fixed")
    args = parser.parse_args()
    with open(args.data, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        parser.error("Dataset is empty")
    x = np.array([[float(r[k]) for k in FEATURE_NAMES] for r in rows])
    y = np.array([r["label"] for r in rows])
    if not np.isfinite(x).all() or not set(y).issubset(REQUIRED):
        parser.error("Features must be finite and labels must use the four project classes")
    groups = np.array([r["participant"] if args.group_by == "participant" else
                       r["participant"] + "/" + r["session"] for r in rows])
    predefined = "split" in rows[0]
    validation = None
    if predefined:
        try:
            splits = predefined_split(rows)
        except ValueError as exc:
            parser.error(str(exc))
        train, validation, test = (splits[s] for s in ("train", "val", "test"))
        checked = [train, validation, test]
    else:
        if len(set(groups)) < 2:
            parser.error("Collect at least two independent groups; preferably several participants")
        train, test = next(GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42).split(x, y, groups))
        checked = [train, test]
    if any(not REQUIRED.issubset(set(y[index])) for index in checked):
        parser.error("Every split must contain all four classes. Check the import report or collect more examples.")
    model = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42, n_jobs=1)
    model.fit(x[train], y[train])
    threshold = 0.75
    validation_scores = {}
    if validation is not None:
        # Tune rejection only on validation; never choose settings from test scores.
        for candidate in (0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9):
            metrics = evaluate(model, x[validation], y[validation], candidate)
            validation_scores[candidate] = metrics["classification_report"]["macro avg"]["f1-score"]
        threshold = max(validation_scores, key=lambda t: (validation_scores[t], -abs(t-0.75)))
    evaluation_indices = validation if predefined else test
    report = {**evaluate(model, x[evaluation_indices], y[evaluation_indices], threshold),
              "evaluation_split": "val" if predefined else "group_holdout",
              "threshold": threshold, "validation_threshold_macro_f1": validation_scores,
              "group_by": args.group_by, "train_groups": sorted(set(groups[train])),
              "test_groups": sorted(set(groups[test])),
              "train_rows": train.tolist(), "test_rows": test.tolist()}
    if predefined:
        report["group_by"] = "official_participant_split"
        report["validation_rows"] = validation.tolist()
        report["validation_groups"] = sorted(set(groups[validation]))
        if args.evaluate_test:
            report["final_test"] = evaluate(model, x[test], y[test], threshold)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_version": FEATURE_VERSION,
                 "feature_names": FEATURE_NAMES, "confidence_threshold": threshold}, path)
    path.with_suffix(".evaluation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["classification_report"], indent=2))
    print(f"Saved {path}; {report['evaluation_split']} accuracy: {report['accuracy']:.3f}; threshold: {threshold}")
    if predefined and not args.evaluate_test:
        print("Final test scores withheld. Use --evaluate-test only after fixing your settings.")


if __name__ == "__main__":
    main()
