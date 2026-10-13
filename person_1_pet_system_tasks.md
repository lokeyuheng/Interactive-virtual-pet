
# Person 1 — Photo Preparation, Animation, and Pet Behaviour

Based on `virtual_pet_project_summary.md`. Person 1 owns the visual pet system; Person 2 owns computer vision inputs, the webcam application, and model evaluation.

## Goal

Turn an animal photo into a transparent, animated 2D pet that accepts action commands and behaves consistently across different animal images.

## Owned files and outputs

- `prepare_pet.py`: photo import, background removal, and image normalization.
- `pet_renderer.py`: transparent compositing, animation transforms, and visual effects.
- `pet_behaviour.py`: action state machine, happiness, energy, and hunger.
- `assets/`: prepared pet images and any visual or sound assets.
- Photo generality results and the pet-system section of the final report.

These are proposed modules to create or extract from the existing prototype. Coordinate edits to the existing `main.py` with Person 2, who owns that file.

## Tasks in development order

### 1. Prepare animal photos

- [ ] Accept an image path and remove the background with `rembg` or a pretrained segmentation model.
- [ ] Save a transparent RGBA PNG; handle unreadable images and unsuccessful extraction with a clear error.
- [ ] Crop excess transparent space, preserve aspect ratio, and standardize display size and baseline.
- [ ] Prepare representative cat, dog, and rabbit photos for the demo.

**Done when:** each test image produces a usable transparent pet with consistent placement and sizing.

### 2. Build the shared animation renderer

- [ ] Render the pet over a supplied OpenCV frame using alpha compositing.
- [ ] Implement idle/breathe, jump, happy/bounce, angry/shake, and sleep animations using whole-image transforms.
- [ ] Use elapsed time for animation timing so speed remains consistent at different frame rates.
- [ ] Clip the image safely at frame edges and expose the pet's current displayed bounds.
- [ ] Add hearts and a sleep overlay; add sound only after the core system works.
- [ ] Provide a small keyboard-driven demo or callable interface so animation can be developed before the gesture model is ready.

**Done when:** all five animations work on every prepared animal image without pet-specific code.

### 3. Implement behaviour and interaction responses

- [ ] Define action durations, transitions back to idle, and which actions can interrupt others.
- [ ] Track happiness, energy, and hunger with bounded values and simple time-based changes.
- [ ] Handle petting and feeding events supplied by Person 2: petting increases happiness; feeding decreases hunger.
- [ ] Ensure repeated events do not continuously restart an animation; coordinate this with Person 2's gesture cooldowns.
- [ ] Make feeding and petting responses visible in the demo.

**Done when:** the pet responds predictably to valid events and stays stable when events repeat.

### 4. Validate and document

- [ ] Test several photos with different animal shapes, sizes, and backgrounds.
- [ ] Record extraction success, visual quality, and whether every animation remains legible.
- [ ] Help Person 2 measure rendering FPS and detection-to-animation latency.
- [ ] Document preparation steps, animation design, behaviour rules, and whole-image animation limitations.

## Shared interface — agree before coding

Use these as proposed contracts and confirm exact signatures together:

- `prepare_pet(input_path, output_path)` produces a transparent PNG.
- `behaviour.handle_event(event, now)` accepts an event containing `action` and `timestamp`, with optional `confidence` and hand position.
- `behaviour.update(now)` advances the state and exposes the current action and needs.
- `renderer.render(frame, state, now)` returns the composited frame.
- `renderer.get_bounds()` returns `(x, y, width, height)` in displayed frame pixels for Person 2's proximity rules.

Shared action names: `IDLE`, `JUMP`, `HAPPY`, `ANGRY`, `SLEEP`, `PET`, and `FEED`. `PET` and `FEED` are interaction events; they may reuse existing animations plus effects.

## Handoffs and collaboration

1. **First checkpoint:** provide a transparent test asset, renderer interface, and working keyboard animations. Person 2 can integrate with placeholder gesture events.
2. **Second checkpoint:** accept stabilized gesture events and publish accurate pet bounds for petting and feeding detection.
3. **Final checkpoint:** finish needs logic, photo testing, and visual polish; run the integrated demo together.

Both people help collect gesture examples, test with different users and lighting, and prepare the final demonstration. Person 2 maintains shared dependency and run instructions; send them any new dependencies.

## Scope boundary

Complete the 2D whole-image MVP first. Articulated rigs are a stretch goal only after integration and evaluation are complete. Automatic 3D reconstruction is outside the required scope.
