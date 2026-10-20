# Public-dataset training for Person 2

The importer and trainer run locally; no large image archives are downloaded
automatically. Dataset images/annotations are not included in this repository.

## 1. Obtain a subset with official metadata

Source: https://github.com/hukenovs/hagrid (HaGRIDv2).
Download links and archive sizes are under Downloads in that repository. Full
gesture archives are roughly 40 GB each; the full dataset is unnecessary for
this project. A locally available smaller subset works if it retains original
image IDs, source gesture directories and official annotations/user IDs. Do not
use a repack with unknown participant IDs or invented train/test splits.

Required initial source classes: `palm`, `like`, `fist`, `no_gesture`.
Optional extra negative classes: `peace`, `one`, `ok`.
`no_gesture` annotations attached to second hands in other selected folders are
also used. Only explicitly mapped classes are imported; other labels are skipped.

Download the official annotations archive linked by HaGRID and extract it.
Arrange or point the CLI to this layout (the directory names above the roots
can differ):

```text
data/hagrid/
  images/
    palm/<image-id>.jpg
    like/<image-id>.jpg
    fist/<image-id>.jpg
    no_gesture/<image-id>.jpg
  annotations/
    train/palm.json, like.json, fist.json, no_gesture.json
    val/palm.json, like.json, fist.json, no_gesture.json
    test/palm.json, like.json, fist.json, no_gesture.json
```

HaGRID's annotation `bboxes` are normalized xywh, `labels` are per hand, and
`user_id` identifies participants. Dataset code/license attribution:
https://github.com/hukenovs/hagrid/blob/master/license/en_us.pdf
Read its specific terms before redistributing dataset-derived artifacts, and
cite the dataset in the university report. Data, previews and models stay in
Git-ignored directories.

## 2. Check approximately 20 usable examples per class per split

From the project root in PowerShell, using the existing CV environment/model:

```powershell
.venv/Scripts/python import_hagrid.py --annotations data/hagrid/annotations --images data/hagrid/images --limit 20 --previews 20 --output data/hagrid_trial.csv
```

Open `data/hagrid_trial_previews/`. Yellow rectangles show the matched annotated
hand; green points show detected landmarks. Check that the label belongs to
that hand, especially in two-hand photos. No real photos have been checked by
the implementation's synthetic tests; inspect these before scaling.

The CLI uses MediaPipe IMAGE mode per independent photo, mirrors the full image
and bounding boxes just like the webcam, matches hands by mutual-best bounding
box IoU (minimum 0.2), then uses the same wrist/palm normalization and xyz order.
It does not substitute HaGRID's supplied 2D landmarks for our 3D features.

Inspect `data/hagrid_trial.import.json` for usable counts, participant counts and
skips (missing images, no detections, unmatched annotations, invalid landmarks).
Counts may fall below your requested limit. Skipped hard examples can bias
evaluation: report failures, not just classifier accuracy on successful hands.
Metadata is checked for participant/image overlap across splits before conversion.

## 3. Extract a larger subset

```powershell
.venv/Scripts/python import_hagrid.py --annotations data/hagrid/annotations --images data/hagrid/images --limit 1000 --per-person 10 --output data/hagrid_features.csv
```

`--limit` is per project class per split; this example allows up to 12,000 hands.
It limits extraction, not archive download size. Seeded record shuffling and
`--per-person` limit domination by a few people. Output contains `split`,
participant IDs, source image/label and 63 features. Existing output is never
overwritten: choose another filename to repeat a conversion.
To add extra negatives, include their images/annotations and pass
`--sources palm like fist no_gesture peace one ok`.

## 4. Train with validation, keeping final test scores untouched

```powershell
.venv/Scripts/python train_gestures.py --data data/hagrid_features.csv --output models/hagrid_gestures.joblib
.venv/Scripts/python main.py --model models/hagrid_gestures.joblib
```

The trainer detects the CSV split column, checks participant/image separation
and requires all four classes in each split. It fits only train rows and chooses
a confidence rejection threshold from 0.5..0.9 using validation macro F1.
Scores below the threshold map to OTHER, exactly as at runtime. The selected
threshold is stored in the model and automatically loaded by the webcam app.
It reports validation metrics by default; those are tuning results, not an
unbiased final score. Trees remain fixed at 200; no extra hyperparameter search.

After fixing preprocessing, classes, thresholds and model settings:

```powershell
.venv/Scripts/python train_gestures.py --data data/hagrid_features.csv --output models/hagrid_gestures.joblib --evaluate-test
```

The JSON report then includes `final_test` metrics. This command deterministically
retrains the same training split; it does not train on validation/test rows.
Do not keep adjusting settings based on final test outcomes. Existing webcam
CSV files without a split column retain the original grouped-holdout workflow.

## 5. Evaluate the real webcam

Test several new people, distances, lighting conditions and both hands. Count
intentional successes/misses and false triggers during ordinary movement.
Image-classifier scores omit landmark detection failures, motion interactions
and temporal gating, so they are not complete application accuracy.
Petting/waving remain separately tuned trajectory rules.

## Automated verification

```powershell
.venv/Scripts/python -m unittest -v test_cv_pipeline test_hagrid
```

These fixtures verify label matching, mirroring, import failures, previews,
split leakage checks, training/saving/loading and test-score withholding.
They do not claim real-data accuracy.
