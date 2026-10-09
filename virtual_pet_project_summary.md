# Photo-to-Virtual-Pet: Computer Vision Project Summary

## 1. Project concept

Build an interactive virtual pet system that transforms a user-uploaded photo of a real animal into an on-screen pet. The pet appears over a live webcam feed and responds to hand gestures, motions, and simple interactions.

**Core idea:** A user uploads a cat, dog, rabbit, or other animal photo; the application removes its background, prepares it as an animated character, and controls its reactions through computer vision.

**Target scope:** Medium-difficulty university project with a fun live demonstration. Prioritize a working 2D system rather than full 3D reconstruction.

## 2. Main features

- **Photo import:** Accept an image of a real pet.
- **Background removal:** Isolate the animal and export a transparent PNG.
- **Reusable animations:** Idle/breathe, jump, bounce/happy, shake/angry, and sleep.
- **Webcam interaction:** Recognize user commands, then trigger animations.
- **Pet personality:** Optional hunger, happiness, and energy states, with playful reactions.
- **Multiple animals:** Reuse one animation interface for different pet images.

### Example interactions

| User input | Pet reaction | Recognition approach |
| --- | --- | --- |
| Thumbs-up | Jump | Static hand gesture classifier |
| Fist | Sleep | Static hand gesture classifier |
| Open palm | Happy / greet | Static hand gesture classifier |
| Gentle stroking near pet | Hearts / purr | Hand position + motion rules |
| Repeated rapid waving | Annoyed / shake | Hand trajectory + thresholds |
| Present a designated coloured feeding prop | Eat / increase fullness | OpenCV colour segmentation |

Gesture-to-action mappings are customizable. Hand proximity must be computed relative to the pet's on-screen position.

## 3. End-to-end pipeline

```text
Pet photo
  -> Animal foreground segmentation / background removal
  -> Transparent pet PNG
  -> Image normalization and animation setup
  -> Pet renderer over webcam frames

Webcam frames
  -> OpenCV capture
  -> MediaPipe hand landmarks
  -> Gesture classifier / motion rules
  -> Debounced action events
  -> Pet behaviour state machine
  -> Animation controller
  -> Composited webcam display
```

**Separation of responsibilities:** The gesture classifier detects user commands. Python controls the pet's mood and animations. There is no need to train an AI model to perform basic sprite animation.

## 4. Universal animation approach

### Version A — Recommended MVP: whole-image animation

Each pet is a single transparent image. The same controller applies translation, scaling, and small rotations regardless of animal species.

| Action | Transform |
| --- | --- |
| Idle | Slight periodic scale change / bobbing |
| Jump | Up-and-down arc, e.g. a sine trajectory |
| Happy | Short repeated bounces and heart particles |
| Angry | Fast horizontal shake |
| Sleep | Slight tilt or shrink plus “Zzz” overlay |

**Advantages:** No drawing, rigging, or pet-specific training. The existing OpenCV prototype already follows this design.

**Limitation:** The animal moves as one rigid cutout; limbs and tails do not move independently.

### Version B — Optional upgrade: reusable skeletal rigs

For more natural motion, segment the image into parts (head, torso, limbs, tail), locate attachment points, and deform or rotate parts according to a template.

- A **quadruped rig** may be shared by many cats, dogs, and rabbits, with per-animal adjustments.
- Birds, fish, and snakes need different anatomy-specific rigs.
- A **universal behaviour API** (for example, `pet.perform("move")`) can map to walking, hopping, swimming, or slithering depending on rig type.
- If automatic part segmentation or pose fitting fails, use simple whole-image animation or manual correction.

A literally universal anatomical skeleton is not realistic. Use universal *commands* with a small number of body templates, rather than forcing all species into one rig.

## 5. Model training: hand gestures

**Recommended starting model:** MediaPipe hand landmarks + Random Forest (optionally compare with SVM or a small neural network).

1. Capture webcam recordings of gestures from several people, distances, orientations, and lighting conditions.
2. Use MediaPipe Hand Landmarker to extract **21 landmarks × 3 coordinates = 63 features** per hand.
3. Normalize coordinates relative to the wrist and hand scale; apply the same preprocessing at inference.
4. Label examples for `OPEN_PALM`, `THUMBS_UP`, `FIST`, `PEACE`, `POINTING`, and `OTHER/NONE` as needed.
5. Collect roughly **300 examples per main class**, with additional negative examples, as an initial target rather than a guarantee of accuracy.
6. Split the dataset by **participant or recording session** to avoid train/test leakage from adjacent frames.
7. Train a Random Forest (`scikit-learn`) and evaluate precision, recall, F1, confusion matrix, and live inference latency.
8. Save the model with `joblib` and use it on each detected hand in the webcam application.

For live use, reject low-confidence predictions and require a stable gesture over multiple frames. Add cooldowns so holding a gesture doesn't repeatedly restart an animation. Tune thresholds using validation data.

**Dynamic interactions:** Petting or waving can initially use tracked hand trajectories and rules. Sequence models (such as LSTMs) are optional only if more complex actions justify them.

## 6. Suggested technology stack

| Component | Tools |
| --- | --- |
| Webcam and compositing | Python, OpenCV, NumPy |
| Photo background removal | `rembg` or a pretrained animal segmentation model |
| Hand landmarks | MediaPipe Tasks Hand Landmarker |
| Gesture recognition | scikit-learn Random Forest / SVM |
| Model storage | `joblib` |
| Animation | OpenCV transformations + transparent PNG assets; optionally Pygame |
| Optional skeletal animation | Part masks, joint geometry, 2D warping, or a dedicated animation engine |

Basic whole-image animation and static gesture recognition do **not** require 3D modelling, LSTMs, or a custom animal-generation model.

## 7. Proposed application structure

```text
virtual_pet/
├── main.py                 # Webcam loop and integration
├── prepare_pet.py          # Photo segmentation -> pet.png
├── pet_renderer.py         # Alpha compositing and animation transforms
├── pet_behaviour.py        # Mood, action states, cooldowns
├── hand_features.py        # Landmark preprocessing
├── train_gestures.py       # Model training and evaluation
├── predict_gestures.py     # Live gesture prediction
├── assets/
│   └── pet.png             # Imported pet image
├── data/
│   └── gesture_dataset.csv
└── models/
    └── pet_gesture_model.pkl
```

## 8. Development roadmap

**Phase 1 — Photo-to-pet MVP**
- Upload a clear photo, remove the background, and overlay the pet on webcam frames.
- Implement keyboard-controlled idle, jump, happy, angry, and sleep animations.

**Phase 2 — Train CV interaction model**
- Collect and label hand-landmark data.
- Train and evaluate the static gesture classifier.
- Replace keyboard shortcuts with stabilized gesture-triggered events.

**Phase 3 — Add natural interactions**
- Detect stroking motion near the pet and a simple feeding prop.
- Add mood/energy/hunger logic, visual effects, and sound.

**Phase 4 — Universalization and evaluation**
- Test several animal photos with varied sizes, shapes, and backgrounds.
- Standardize their displayed size and baseline; ensure identical actions work across images.
- Optionally add a quadruped-specific articulated animation rig.

## 9. Evaluation for university assessment

Evaluate both the CV model and the overall user experience:

- **Gesture recognition:** Accuracy, per-class precision/recall/F1, confusion matrix.
- **Responsiveness:** Detection-to-animation latency and rendering FPS.
- **Robustness:** Different users, lighting, backgrounds, camera distances, and hand orientations.
- **Interaction stability:** False triggers, missed gestures, and repeated-trigger frequency.
- **Photo generality:** Successful foreground extraction and legible animations across cat/dog/rabbit and other test photos.

Possible research question: **How reliably can a photo-based virtual pet system recognize human gestures and deliver consistent real-time interactions across different pet images?**

## 10. Final recommended scope

Build a **2D photo-based universal virtual pet** with:

1. Photo import and automatic foreground removal.
2. One shared whole-image animation controller for all animals.
3. A trained hand-gesture classifier (MediaPipe landmarks + Random Forest).
4. Rule-based petting / feeding interactions.
5. Simple happiness, energy, and hunger mechanics.
6. A real-time OpenCV webcam demo and quantitative evaluation.

**Stretch goal:** Add anatomy-specific 2D rigs for articulated head/tail/limb movement. Do not make automatic 3D reconstruction or flawless universal animal skeleton fitting a requirement for the MVP.
