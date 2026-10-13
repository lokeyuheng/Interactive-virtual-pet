# Person 2 — Gesture Recognition, Webcam Integration, and Evaluation

Based on `virtual_pet_project_summary.md`. Person 2 owns computer vision inputs and the running application; Person 1 owns photo preparation, rendering, and pet behaviour.

## Goal

Recognize stable user interactions from a webcam, send action events to the pet system, and demonstrate the complete application with quantitative evaluation.

## Owned files and outputs

- `main.py`: webcam loop, keyboard fallback, module integration, and application controls.
- `hand_features.py`: MediaPipe landmarks and shared feature preprocessing.
- `train_gestures.py`: model training and evaluation.
- `predict_gestures.py`: live predictions, confidence rejection, stabilization, and gesture cooldowns.
- `interaction_rules.py` (additional proposed module): petting, waving, and feeding-prop detection.
- `data/` and `models/`: labeled data, split metadata, saved model, and evaluation outputs.
- `requirements.txt` and run instructions.
- Model/system evaluation results and the CV section of the final report.

Coordinate extraction of existing rendering or behaviour code from `main.py` with Person 1 so edits do not conflict.

## Tasks in development order

### 1. Build webcam and landmark capture

- [ ] Open the webcam with OpenCV and handle missing cameras or failed frames cleanly.
- [ ] Extract 21 hand landmarks with MediaPipe Tasks Hand Landmarker.
- [ ] Normalize the 63 coordinates relative to wrist position and hand scale.
- [ ] Reuse exactly the same preprocessing for data collection and live inference.
- [ ] Define one coordinate convention for mirroring, hand positions, and the displayed frame.
- [ ] Integrate Person 1's renderer early, using keyboard actions while the classifier is in development.

**Done when:** a live webcam displays the pet and landmark capture works reliably enough to collect examples.

### 2. Collect and train the gesture model

- [ ] Start with `OPEN_PALM`, `THUMBS_UP`, `FIST`, and `OTHER/NONE`. Add `PEACE` or `POINTING` only if they serve a defined interaction.
- [ ] Coordinate data collection with both people and, where possible, additional participants under varied lighting, distances, and orientations.
- [ ] Aim initially for roughly 300 examples per main class plus negative examples; retain participant/session identifiers.
- [ ] Split by participant or recording session to avoid adjacent-frame leakage. Keep final test data separate from threshold tuning.
- [ ] Train a Random Forest; compare an SVM only if time allows or baseline performance needs improvement.
- [ ] Save the trained model with `joblib` and document feature order and label mappings.
- [ ] Report accuracy, per-class precision/recall/F1, and a confusion matrix.

**Done when:** the saved model can be loaded for live predictions and is evaluated on held-out participants or sessions.

### 3. Stabilize commands and add natural interactions

- [ ] Reject low-confidence predictions, require stability across multiple frames, and add cooldowns.
- [ ] Define behaviour when hands disappear or multiple hands are visible.
- [ ] Map thumbs-up to `JUMP`, fist to `SLEEP`, and open palm to `HAPPY`.
- [ ] Track gentle stroking near the pet's displayed bounds and emit `PET` events.
- [ ] Detect repeated rapid waving from hand trajectories and emit `ANGRY` events.
- [ ] Detect a designated coloured feeding prop with OpenCV colour segmentation; require appropriate proximity to emit `FEED`.
- [ ] Tune thresholds on validation examples and check false triggers in ordinary movement.

**Done when:** intentional interactions trigger appropriate reactions without repeatedly restarting them while a gesture is held.

### 4. Complete integration and evaluation

- [ ] Connect action events to Person 1's behaviour state machine and renderer.
- [ ] Keep keyboard controls for debugging and demo fallback.
- [ ] Provide clear startup, pet-image selection, exit, and camera-release behaviour.
- [ ] Record rendering FPS and detection-to-animation latency, with a documented measurement method.
- [ ] Test different users, lighting, backgrounds, distances, and hand orientations.
- [ ] Record false triggers, missed gestures, and repeated-trigger frequency over a documented trial set.
- [ ] Combine model results with Person 1's photo generality results in the report.
- [ ] Write reproducible setup, training, and demo instructions and rehearse the demo together.

**Done when:** a new run can load a prepared pet and model, recognize all required interactions, and produce a stable real-time demo with documented results.

## Shared interface — agree before coding

Use these proposed contracts with Person 1:

- Emit events containing `action` and `timestamp`, with optional `confidence` and hand position, to `behaviour.handle_event(event, now)`.
- Call `behaviour.update(now)` each frame, then pass its current state to `renderer.render(frame, state, now)`.
- Read `renderer.get_bounds()` as `(x, y, width, height)` in displayed frame pixels for proximity checks.
- Use one monotonic time source and the same displayed coordinate system throughout the application.

Shared action names: `IDLE`, `JUMP`, `HAPPY`, `ANGRY`, `SLEEP`, `PET`, and `FEED`. Person 2 owns recognition stabilization; Person 1 owns action duration and interruption rules. Agree together how cooldowns interact.

## Handoffs and collaboration

1. **First checkpoint:** deliver webcam capture, landmark collection, and the event format. Integrate Person 1's initial renderer with keyboard commands.
2. **Second checkpoint:** deliver the evaluated classifier and stabilized events; use Person 1's pet bounds to implement motion and feeding rules.
3. **Final checkpoint:** finish the application, robustness trials, metrics, run instructions, and joint demonstration.

Both people help collect gesture examples, test the integrated system, and prepare the presentation. Person 1 leads visual/photo evaluation; Person 2 leads CV/system evaluation.

## Scope boundary

Prioritize a trained static gesture classifier and rule-based motion interactions. LSTMs, additional classifier comparisons, and more gesture classes are optional after the MVP works. Person 1's articulated rig stretch goal must not block integration.
