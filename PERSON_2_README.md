# Person 2: CV pipeline

Python 3.10 is available on this machine. From the project root in PowerShell:

```powershell
py -3.10 -m venv .venv
.venv/Scripts/python -m pip install -r requirements-cv.txt
New-Item -ItemType Directory -Force models
Invoke-WebRequest 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task' -OutFile models/hand_landmarker.task
.venv/Scripts/python main.py
```

The camera preview mirrors frames before landmark extraction. All positions and
renderer bounds use these displayed pixels. Without a classifier, tracking and
keyboard actions still work. `--keyboard-only` bypasses MediaPipe and its model.
`--camera 1` selects another camera. Q/Escape exits and releases resources.
The default pet is explicitly a placeholder for Person 1's renderer.

## Collect real data

```powershell
.venv/Scripts/python collect_gestures.py --participant p01 --session day1
```

Select 1=open palm, 2=thumbs up, 3=fist, 4=OTHER. Press R to start/stop
recording. Changing labels stops recording. Only exactly one visible hand is
recorded, at most once per 150 ms. OTHER means a visible hand in an unrelated
pose; absent hands are handled separately and are not artificial feature rows.
Collect every class in each session. Vary people, lighting, orientation and
distance; aim initially for 300 examples per main class across several groups.
Participant/session identifiers are saved with the shared 63 normalized features.
Data/models are ignored by Git. Obtain participant agreement before collection.

## Train and run

```powershell
.venv/Scripts/python train_gestures.py
.venv/Scripts/python main.py
```

Training holds out participants (25% of groups, seed 42), rejects splits missing
required classes, and saves a model plus JSON metrics, confusion matrix, group
IDs and row indices. `--group-by session` is available when participant holdout
is infeasible; state that limitation in your report. Never tune thresholds on
the final test split: reserve separate validation sessions. Only load trusted
joblib files. Baseline confidence is 0.75, stability 0.3 s, release 0.25 s and
cooldown 1 s. Held gestures remain latched until a neutral interval.

## Person 1 adapter

Pass `--adapter your_module`. That module must expose `create_pet()` returning
`(behaviour, renderer)`. Behaviour exposes `state`, `handle_event(event, now)` and
`update(now)`. Renderer exposes `render(frame, state, now)` returning the frame
and `get_bounds()` returning `(x, y, width, height)` in displayed pixels.
Bounds should describe the currently displayed pet, including animated movement.
Use monotonic seconds. Events contain action, timestamp and optional confidence.
Actions: JUMP, HAPPY, SLEEP, PET, ANGRY, FEED. Recognition owns stabilization;
Person 1 owns duration/interruption rules. Keyboard J/H/S/A/P/F bypasses CV.

Motion rules track index fingertip positions over one second. Missing/multiple
hands clear history. Waving takes precedence over gentle petting; motion events
take precedence over feeding and static gestures. These initial pixel thresholds
need validation at the demo's camera resolution. Feeding uses a green prop with
HSV (40,100,70)..(85,255,255), area >=500 pixels, near the pet for >=0.4 seconds.
Tune for lighting; green backgrounds can cause false detections. Motion/feed
events have a two-second cooldown; a held feeding prop can feed repeatedly.

## Evaluate

Run deterministic preprocessing, stabilization and motion checks with
`.venv/Scripts/python -m unittest -v test_cv_pipeline`.

`data/live_metrics.csv` logs FPS, per-frame processing time, actions and time from
event creation to completion of rendering. This excludes camera acquisition,
gesture stabilization, display refresh and physical movement onset, so it is
not end-to-end interaction latency. Measure that separately using annotated
video or timed trials. Record intentional attempts, successful reactions,
misses, false/repeated triggers and trial duration across users/conditions.
No real-data accuracy or live-camera performance is claimed before those trials.

MediaPipe implementation follows the official Tasks VIDEO interface:
https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python
