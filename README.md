# Gesture Volume Control 

Control your system volume using just your hand in front of a webcam. No touching required.

## Demo
> Pinch your thumb and index finger together → volume goes down  
> Spread them apart → volume goes up

## Tech Stack
- Python
- OpenCV
- MediaPipe
- NumPy
- pycaw

## How It Works
The webcam feed is processed frame by frame using OpenCV. MediaPipe detects 21 hand landmarks in real time. The code tracks landmark 4 (thumb tip) and landmark 8 (index fingertip), calculates the distance between them, and maps that distance to a volume range using NumPy. pycaw communicates with the Windows audio API to set the volume.

## Requirements
- Python 3.11
- Windows OS (pycaw is Windows only)
- Webcam

## Installation
**Step 1 — Download the project file**  
Click the green **Code** button on this page → **Download ZIP**. Extract it, or directly download `volume_control.py`.

**Step 2 — Install dependencies**  
Open terminal in the project folder and run:
```
pip install opencv-python mediapipe numpy pycaw comtypes
```

**Step 3 — Run**
```
py -3.11 volume_control.py
```

## Notes
- Make sure your webcam is connected and accessible
- Works best in decent lighting
- Built and tested on Windows 11
