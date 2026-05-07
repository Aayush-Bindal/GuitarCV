import cv2
import mediapipe as mp
import urllib.request
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import config

# ── Hand connections (pairs of landmark indices to draw bones) ────────────────
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),         # Thumb
    (0,5),(5,6),(6,7),(7,8),         # Index
    (0,9),(9,10),(10,11),(11,12),    # Middle
    (0,13),(13,14),(14,15),(15,16),  # Ring
    (0,17),(17,18),(18,19),(19,20),  # Pinky
    (5,9),(9,13),(13,17),            # Palm
]

class HandTracker:
    def __init__(self):
        self.latest_result = None
        
        if not os.path.exists(config.MODEL_PATH):
            print("Downloading hand landmarker model...")
            urllib.request.urlretrieve(config.MODEL_URL, config.MODEL_PATH)
            print("Done.")

        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=config.MODEL_PATH),
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_hands=config.NUM_HANDS,
            min_hand_detection_confidence=config.MIN_HAND_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=config.MIN_HAND_PRESENCE_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
            result_callback=self._result_callback,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def _result_callback(self, result, output_image, timestamp_ms):
        self.latest_result = result

    def process_frame(self, frame, timestamp):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        self.landmarker.detect_async(mp_image, timestamp)

    def draw_results(self, frame):
        if self.latest_result and self.latest_result.hand_landmarks:
            for i, hand_landmarks in enumerate(self.latest_result.hand_landmarks):
                self._draw_hand(frame, hand_landmarks)

                # Label near wrist
                label = "Left" if self.latest_result.handedness[i][0].display_name == "Right" else "Right"
                h, w = frame.shape[:2]
                wrist = hand_landmarks[0]
                cx, cy = int(wrist.x * w), int(wrist.y * h)
                cv2.putText(
                    frame, label,
                    (cx - 30, cy + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2, cv2.LINE_AA,
                )

    def _draw_hand(self, frame, landmarks):
        h, w = frame.shape[:2]
        points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

        # Draw connections
        for a, b in HAND_CONNECTIONS:
            cv2.line(frame, points[a], points[b], (255, 255, 255), 2)

        # Draw landmark dots
        for pt in points:
            cv2.circle(frame, pt, 4, (0, 255, 0), -1)

    def close(self):
        self.landmarker.close()
