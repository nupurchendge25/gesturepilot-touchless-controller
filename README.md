# GesturePilot — Touchless Computer Controller

Control your computer's mouse using real-time hand tracking and computer vision. GesturePilot uses your webcam to track your index fingertip and detect pinch gestures, enabling touchless cursor movement, clicking, and dragging.

## Features

- **Real-time hand tracking** using MediaPipe.
- **Cursor movement** controlled by the index fingertip.
- **Clicking** using a thumb-and-index-finger pinch.
- **Drag and drop** by holding the pinch gesture.
- **Pause and resume** mouse control using a keyboard shortcut.
- **Safe exit and cleanup** to release the mouse button and close the webcam.

## Tech Stack

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## Requirements

- Windows computer
- Python 3.10
- Webcam
- VS Code or another Python-compatible editor

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/gesturepilot-touchless-controller.git
   cd gesturepilot-touchless-controller
   ```

2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run the Project

```powershell
python main.py
```

A webcam window named `GesturePilot` will open.

## Controls

| Input | Action |
|---|---|
| Move index fingertip | Move cursor |
| Pinch thumb and index finger | Click |
| Hold pinch while moving | Drag and drop |
| `P` | Pause or resume control |
| `Q` | Quit |

## Safety

- Keep the webcam unobstructed and your hand visible.
- Press `P` to pause control when needed.
- Move the cursor to the top-left corner of the screen to activate PyAutoGUI's failsafe.
- Press `Q` in the webcam window to exit.

## How It Works

1. OpenCV captures webcam frames.
2. MediaPipe detects hand landmarks.
3. The index fingertip position is mapped to screen coordinates.
4. Cursor smoothing reduces abrupt movement.
5. The distance between the thumb and index fingertip determines whether a pinch is active.
6. PyAutoGUI performs the corresponding mouse actions.

## Future Improvements

- Gesture-based scrolling
- Configurable gesture sensitivity
- Improved cursor calibration and smoothing
- On-screen gesture instructions

## License

No license has been specified yet.
