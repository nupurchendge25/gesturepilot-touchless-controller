# GesturePilot – Touchless Computer Controller

GesturePilot is a computer vision project that enables touchless computer control using real-time hand tracking. It uses a webcam, MediaPipe, OpenCV, and PyAutoGUI to control cursor movement, clicking, dragging, and scrolling through hand gestures.

## Features

- **Real-time hand tracking** using MediaPipe.
- **Cursor movement** controlled by the index fingertip.
- **Adaptive cursor smoothing** to improve responsiveness and reduce jitter.
- **Clicking** using a thumb-and-index-finger pinch.
- **Drag and drop** by holding the pinch gesture.
- **Gesture-based scrolling** using a predefined combination of finger positions.
- **Pause and resume** cursor control using a keyboard shortcut.
- **Canny edge detection** to demonstrate edge detection in computer vision.
- **Grayscale conversion** for image processing.
- **Pixel-value analysis** to display BGR values at the index fingertip.
- **FPS display** to monitor processing performance.
- **Safe exit and cleanup** to release the mouse button and close the webcam.

## Tech Stack

- Python 3.10
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## Requirements

- Windows computer
- Python 3.10
- Webcam
- VS Code or another Python-compatible editor
- Git

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nupurchendge25/gesturepilot-touchless-controller.git
   cd gesturepilot-touchless-controller
   ```

2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Activate the virtual environment:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   If you use Git Bash instead of PowerShell, run:

   ```bash
   source .venv/Scripts/activate
   ```

4. Install the required dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the Project

Run the following command from the project directory:

```bash
python main.py
```

A webcam window named `GesturePilot` will open and display the detected hand landmarks, cursor-control region, current status, FPS, and fingertip pixel values.

## Controls

| Input | Action |
|---|---|
| Move index fingertip | Move cursor |
| Quickly pinch thumb and index finger | Click |
| Hold the pinch gesture | Start dragging |
| Release the pinch | Release drag or complete a click |
| Raise index and middle fingers while keeping ring and little fingers down | Enter scroll mode |
| Move the index finger vertically in scroll mode | Scroll up or down |
| `P` | Pause or resume cursor control |
| `C` | Toggle Canny edge detection |
| `Q` | Quit the application |

## How It Works

1. **Image acquisition:** OpenCV captures frames from the webcam and resizes them to 640 × 480 pixels.
2. **Color-space conversion:** Frames are converted from BGR to RGB for MediaPipe processing.
3. **Hand tracking:** MediaPipe identifies hand landmarks, including the thumb, index finger, middle finger, ring finger, and little finger.
4. **Cursor mapping:** The index fingertip coordinates are mapped to screen coordinates within a defined control region.
5. **Cursor smoothing:** Adaptive movement factors and a small dead zone help balance responsiveness and stability.
6. **Click and drag:** The distance between the thumb and index fingertip determines whether a pinch is active. A quick pinch triggers a click, while holding it initiates dragging.
7. **Scrolling:** A predefined finger configuration activates scroll mode, and vertical index-finger movement determines the scroll direction and amount.
8. **Image processing:** The application converts frames to grayscale and optionally applies Canny edge detection.
9. **Display and monitoring:** OpenCV displays the webcam feed, hand landmarks, fingertip BGR pixel values, status information, and estimated FPS.

## Safety

- Keep the webcam unobstructed and your hand visible.
- Press `P` to pause cursor control when necessary.
- Move the cursor to the top-left corner of the screen to activate PyAutoGUI's failsafe.
- Press `Q` while the webcam window is active to exit.
- Avoid using the application for actions where accidental mouse input could cause harm.

## Future Improvements

- Configurable gesture sensitivity through an interface.
- Improved cursor calibration and movement filtering.
- Customizable gesture mappings.
- More robust hand-pose recognition.
- Additional gesture-based shortcuts.

## License

No license has been specified yet. Add a `LICENSE` file if you intend to distribute the project under a particular open-source license.
