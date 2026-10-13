# Interactive Virtual Pet

An animal photo becomes a transparent 2D pet that appears over a webcam feed and responds to hand gestures.

**Start here if you are Person 1.** This guide assumes Windows and no previous Git/GitHub experience. Use GitHub Desktop for sharing code and VS Code for writing it.

## Current project status

At the time this guide was written, `main.py` is empty. Running it will not display a pet yet. `requirements.txt` lists the planned dependencies; the application modules below still need to be built.

Read these documents for the project scope and assignments:

- [Project summary](virtual_pet_project_summary.md)
- [Person 1 task checklist](person_1_pet_system_tasks.md)
- [Person 2 task checklist](person_2_cv_integration_tasks.md)

## Who builds what?

| Person | Responsibility | Files they own |
| --- | --- | --- |
| Person 1 | Photo preparation, animations, pet behaviour, visual effects | `prepare_pet.py`, `pet_renderer.py`, `pet_behaviour.py`, `assets/` |
| Person 2 | Webcam, hand tracking, gesture model, interaction detection, integration | `main.py`, gesture/interaction modules, `data/`, `models/`, `requirements.txt` |

Person 2 detects an interaction and sends a command such as `JUMP`. Person 1's system receives that command and animates the pet. Both people help collect gesture data, test, and prepare the report.

## 1. Install the tools once

1. Create a free account at [GitHub](https://github.com/).
2. Send your GitHub username to the repository owner and ask them to add you as a collaborator. Accept the invitation so you can upload changes.
3. Install [GitHub Desktop](https://desktop.github.com/) and sign in with that account. This handles Git without terminal commands.
4. Install [VS Code](https://code.visualstudio.com/) and its **Python** extension published by Microsoft.
5. Install [Python](https://www.python.org/downloads/windows/). If its installer offers **Add Python to PATH**, enable it. Coordinate the Python version with Person 2 so both computers use the same version supported by the project dependencies.

## 2. Copy the project onto your computer

This is called **cloning**. Do it once, then work inside that folder.

1. Open GitHub Desktop.
2. Select **File → Clone repository → URL**.
3. Enter `https://github.com/lokeyuheng/Interactive-virtual-pet`.
4. Choose a local folder you can find easily, then click **Clone**.
5. Use **Repository → Open in Visual Studio Code**, or open that cloned folder through **File → Open Folder** in VS Code.

Do not use **Download ZIP** for collaboration: a ZIP does not include the Git connection used to share changes.

## 3. Create your working branch

A **branch** is your own line of work inside the project. Your teammate can develop their part on another branch.

1. In GitHub Desktop, select the repository's default branch under **Current Branch**. It is usually called `main`; use the name actually shown in this repository.
2. Click **Fetch origin**, then **Pull origin** if that button appears, to download the latest work.
3. Select **Branch → New branch**.
4. Name it `codex/person-1-pet-system` and create it from the updated default branch.
5. Click **Publish branch** to upload the branch to GitHub.

Check that **Current Branch** shows your branch before editing. For later independent features, create a fresh branch from the updated default branch, for example `codex/person-1-jump-animation`.

## 4. Set up Python in the project folder

In VS Code, select **Terminal → New Terminal**. Use a PowerShell terminal opened in the cloned project folder. Run each command separately:

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `py` is unavailable but `python --version` works, replace `py` with `python` in the first two commands. If neither works, finish the Python installation and restart VS Code.

`.venv` is a private Python environment for this project. These commands use it directly, so you do not need to activate it or change PowerShell security settings.

In VS Code, press **Ctrl+Shift+P**, choose **Python: Select Interpreter**, and select `.venv\Scripts\python.exe`. If it is absent, use the option to enter its path.

If installation fails, send Person 2 the exact error and your Python version. Agree on any dependency changes before editing `requirements.txt`.

## 5. Keep temporary files out of Git

Before your first commit, check for an existing `.gitignore` in the project root. If there is none, create it in VS Code with these lines. If one exists, add only missing rules:

```gitignore
.venv/
__pycache__/
*.pyc
.env
```

Commit `.gitignore`, but do not commit the environment folder. Review the changed-file list in GitHub Desktop before every commit. Only share animal photos that you have agreed to include in the project.

## 6. Your first coding milestone: show one pet

Start small: display one transparent pet image in an OpenCV window. You do not need Person 2's gesture classifier yet.

1. Create `assets/` and put a transparent animal PNG inside it as `assets/pet.png`. A manually prepared PNG is fine for this first milestone.
2. Create `pet_renderer.py` to load the image and blend it onto a background frame using the PNG's alpha channel.
3. Create `demo_pet.py` as your own test program. Give it a plain background first; webcam integration belongs to Person 2.
4. Make the window close with Escape and release any resources when it exits.
5. Run your demo once you have implemented it:

```powershell
.\.venv\Scripts\python.exe demo_pet.py
```

**Success:** the animal appears with a transparent background and the window closes correctly. `demo_pet.py` is a file you create, not a demo already supplied by this repository.

## 7. Add animations one at a time

Use the same transparent image and change its position, scale, or angle every frame.

| Order | Feature | Implementation idea |
| --- | --- | --- |
| 1 | Idle | Slight periodic breathing scale or vertical bob |
| 2 | Jump | Move upward and back down over a fixed duration |
| 3 | Happy | Small repeated bounces, then hearts |
| 4 | Angry | Brief rapid horizontal shaking |
| 5 | Sleep | Slight tilt and a Zzz overlay |

Use elapsed time rather than counting frames. For a jump, `progress` runs from 0 to 1, and the vertical offset can be `height * sin(pi * progress)`. Return to idle when the animation finishes. Always transform the original image, so repeated resizing does not gradually damage its quality.

Add keyboard controls to `demo_pet.py`: for example, **1** for idle, **2** for jump, **3** for happy, **4** for angry, and **5** for sleep. This lets you verify reactions before gestures are ready.

After animations work:

- Build `prepare_pet.py` for automatic background removal, cropping, and consistent sizing.
- Build `pet_behaviour.py` to track the current action, action start time, hunger, happiness, and energy.
- Add `PET` and `FEED` responses and try cat, dog, and rabbit images.

## 8. Agree on the connection with Person 2

Before building too much, confirm these proposed interfaces together:

```text
prepare_pet(input_path, output_path) → transparent PNG
behaviour.handle_event(event, now) → accept a command
behaviour.update(now) → advance behaviour and expose state
renderer.render(frame, state, now) → composited frame
renderer.get_bounds() → (x, y, width, height) in displayed pixels
```

Use action names `IDLE`, `JUMP`, `HAPPY`, `ANGRY`, `SLEEP`, `PET`, and `FEED`. An event includes an action and timestamp. Use the same monotonic clock for event and animation timing. Person 2 needs the pet bounds to recognize stroking or feeding near the pet, including while it moves.

Keep your standalone demo working. Person 2 connects your modules to the webcam loop in `main.py`. Tell each other before changing a shared interface or editing the other person's files.

## 9. Save and share your work

Saving in VS Code only saves files on your computer. A **commit** records a checkpoint locally; **push** uploads it to GitHub.

After completing a small working piece:

1. Save your files in VS Code and run your demo.
2. Open GitHub Desktop and check that you are on your Person 1 branch.
3. Review the **Changes** list and the highlighted edits. Include only files relevant to your work.
4. Enter a short summary, such as `Add transparent pet rendering`.
5. Click **Commit to [your branch]**.
6. Click **Push origin**. If the branch is new, the button may be **Publish branch**.

Make small commits, such as `Add jump animation` or `Add sleep state`. Commit working progress regularly, rather than waiting until the whole project is finished.

## 10. Ask to combine your changes

A **pull request (PR)** lets your teammate review your branch before it is combined with the shared default branch.

1. Push your changes first.
2. In GitHub Desktop, use **Preview Pull Request** / **Create Pull Request**, or **Branch → Create Pull Request**.
3. On GitHub, check that the destination (**base**) is the shared default branch and the source (**compare**) is your Person 1 branch.
4. Write a title such as `Add pet renderer and keyboard animation demo`.
5. Explain what works, how to run it, which controls to use, and anything unfinished.
6. Create the PR and share its link with Person 2 for review. Agree who merges it after review.

Pushing alone does not put your changes into the default branch. Merging the PR does that.

After it is merged, commit any remaining local work before switching branches. Select the default branch, fetch and pull the merged changes, and create a fresh feature branch for your next task.

## Everyday routine

1. Open GitHub Desktop and confirm your repository and branch.
2. Fetch and pull changes available for your current branch.
3. Open VS Code, implement one small task, and test it.
4. Save, review, commit, and push.
5. Create or update a PR when the feature is ready for integration.

Pulling your feature branch does not automatically include new work merged into the default branch. To bring that work into an active feature branch, commit your changes first, then use **Branch → Merge into current branch** and select the updated default branch. Ask Person 2 to help with your first merge if conflicts appear.

## Common problems

| Problem | What to do |
| --- | --- |
| Cannot push / permission denied | Check your GitHub account and that you accepted the collaborator invitation. |
| `ModuleNotFoundError` | Run with `.venv\Scripts\python.exe` and install requirements using that same interpreter. |
| Running `main.py` does nothing | It was empty when this guide was created; run your implemented `demo_pet.py` until integration is ready. |
| Pet image is not found | Open the project root in VS Code and check `assets/pet.png` exists. |
| Pet has a solid rectangle around it | Check that the PNG actually contains transparency and that the renderer uses its alpha channel. |
| GitHub Desktop shows thousands of files | Check `.gitignore` before committing; `.venv` should be excluded. |
| Git reports a merge conflict | Both branches changed overlapping lines. Keep your work, inspect the conflict together, and agree which code to keep. Do not discard changes just to remove the message. |

## Person 1's first-session checklist

- [ ] Accept the repository invitation and clone with GitHub Desktop.
- [ ] Create and publish your Person 1 branch.
- [ ] Set up `.venv`, dependencies, and `.gitignore`.
- [ ] Read the Person 1 task file and agree on interfaces with Person 2.
- [ ] Display one transparent PNG using your own renderer and demo.
- [ ] Test it, commit, and push your first milestone.

Official GitHub references: [GitHub Desktop guide](https://docs.github.com/en/desktop), [committing changes](https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop), and [creating a pull request](https://docs.github.com/en/desktop/working-with-your-remote-repository-on-github-or-github-enterprise/creating-an-issue-or-pull-request-from-github-desktop).
