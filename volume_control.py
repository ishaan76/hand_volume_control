import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import threading

# Volume Setup
devices = AudioUtilities.GetSpeakers()
activate = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(activate, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

# Shared state
latest_landmarks = None
lock = threading.Lock()

def on_result(result, output_image, timestamp_ms):
    global latest_landmarks
    with lock:
        latest_landmarks = result.hand_landmarks if result.hand_landmarks else None

# MediaPipe LIVE_STREAM Setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
    result_callback=on_result)

cap = cv2.VideoCapture(0)
timestamp = 0

with HandLandmarker.create_from_options(options) as landmarker:
    while True:
        success, img = cap.read()
        if not success:
            continue

        img = cv2.flip(img, 1)
        h, w, _ = img.shape

        # Send frame to detector
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        landmarker.detect_async(mp_image, timestamp)
        timestamp += 1

        # Use latest detected landmarks
        with lock:
            hand_landmarks = latest_landmarks

        if hand_landmarks:
            hand = hand_landmarks[0]
            lm_list = [[id, int(lm.x * w), int(lm.y * h)] for id, lm in enumerate(hand)]

            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Draw all landmarks
            for lm in lm_list:
                cv2.circle(img, (lm[1], lm[2]), 5, (255, 255, 255), cv2.FILLED)

            cv2.circle(img, (x1, y1), 12, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 12, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [30, 300], [minVol, maxVol])
            volBar = np.interp(length, [30, 300], [400, 150])
            volPer = np.interp(length, [30, 300], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)

            if length < 50:
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Gesture Volume Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()