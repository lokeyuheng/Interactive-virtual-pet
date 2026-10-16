# TripoSR feasibility trial

Goal: decide whether photo-derived 3D animals are suitable before dividing the project between two people. This experiment is separate from the webcam application.

## Setup on Windows (CPU)

Use Python 3.10 for this experiment: upstream pins several older packages. Python 3.13 is installed on this computer, but has not been validated with those pins. Install Git and Visual Studio Build Tools with the **Desktop development with C++** workload and CMake; upstream torchmcubes requires a native build.

From the project root in PowerShell:

```powershell
py -3.10 -m venv experiments/triposr/.venv
$trialPython = 'experiments/triposr/.venv/Scripts/python.exe'
& $trialPython -m pip install --upgrade pip setuptools wheel
git clone https://github.com/VAST-AI-Research/TripoSR.git experiments/triposr/vendor/TripoSR
& $trialPython -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
& $trialPython -m pip install -r experiments/triposr/vendor/TripoSR/requirements.txt
& $trialPython -m pip install onnxruntime
& $trialPython experiments/triposr/trial.py --check
& $trialPython experiments/triposr/trial.py
```

Skip the clone command if the source is already downloaded. First inference downloads model weights and background-removal weights. Internet access and free disk space are required. CPU generation speed must be measured on your machine; no interactive-speed promise is assumed.

The default trial uses the upstream chair example to check installation. Then test a real animal:

```powershell
& $trialPython experiments/triposr/trial.py --image 'C:/path/to/pet.jpg'
```

Start with a clear full-body image of one animal, with visible legs and tail and little occlusion. Default extraction resolution is 128 for an initial CPU trial; use `--resolution 256` for a higher resolution comparison. This changes mesh extraction, not the model's understanding of the animal.

## Inspect and decide

Each run gets a separate directory under `outputs/`, containing a log, metadata and, if successful, `0/mesh.glb`. Import the GLB into Blender and inspect the front, sides and back. Generation produces a static mesh; animation requires a separate rig or whole-model transforms.

Test at least three animal photos and record results in `evaluation.csv`. Count failed attempts as well as successes. Check likeness, recognizable anatomy, disconnected/fused legs, underside/back quality, runtime and how much manual cleanup is needed.

Proceed with 3D if the quality is acceptable and cleanup/animation fit the deadline. Reconstruct assets ahead of the webcam demo; the webcam loop should load saved models. Keep 2D as fallback if reconstruction or rigging remains unreliable.

## Shared contract before splitting

- CV module emits JUMP, HAPPY, SLEEP, PET and FEED events.
- Pet module exposes `perform(action)`, `update(dt)` and screen bounds for proximity detection.
- Webcam coordinates use the displayed mirrored frame consistently.
- CV handles stable detections/repeated gesture suppression; pet behaviour handles animation duration and allowed state transitions.
- First integration milestone: keyboard triggers a jump on a saved model, then one gesture triggers the same action.

Person 1 can own gesture recognition and evaluation. Person 2 can own asset preparation, 3D rendering, animation and pet behaviour. Both should approve this feasibility trial before committing to the 3D scope.

Official sources: https://github.com/VAST-AI-Research/TripoSR and its run.py/requirements.txt. See vendor/TripoSR/LICENSE for upstream licensing.
