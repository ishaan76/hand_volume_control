# Gesture Volume Control 🖐️

Control your system volume using just your hand gestures via webcam.

## Tech Stack
- Python
- OpenCV
- MediaPipe
- pycaw

## How it works
Uses webcam to detect hand landmarks in real time.
Distance between thumb and index finger controls the volume.
Pinch = low volume, spread apart = high volume.

## How to run
py -3.11 volume_control.py
