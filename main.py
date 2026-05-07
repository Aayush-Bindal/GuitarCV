import cv2
import mediapipe as mp
import urllib.request
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ── Model Setup ──────────────────────────────────────────────────────────────
MODEL_PATH = "hand_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
)

if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Done.")

# ── Hand connections (pairs of landmark indices to draw bones) ────────────────
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),         # Thumb
    (0,5),(5,6),(6,7),(7,8),         # Index
    (0,9),(9,10),(10,11),(11,12),    # Middle
    (0,13),(13,14),(14,15),(15,16),  # Ring
    (0,17),(17,18),(18,19),(19,20),  # Pinky
    (5,9),(9,13),(13,17),            # Palm
]

def draw_hand(frame, landmarks):
    h, w = frame.shape[:2]
    points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    # Draw connections
    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, points[a], points[b], (255, 255, 255), 2)

    # Draw landmark dots
    for pt in points:
        cv2.circle(frame, pt, 4, (0, 255, 0), -1)

# ── Result Storage ────────────────────────────────────────────────────────────
latest_result = None

def result_callback(result, output_image, timestamp_ms):
    global latest_result
    latest_result = result

# ── HandLandmarker Init ───────────────────────────────────────────────────────
options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=vision.RunningMode.LIVE_STREAM,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7,
    result_callback=result_callback,
)
landmarker = vision.HandLandmarker.create_from_options(options)

# ── Webcam Loop ───────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
timestamp = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror the frame
    frame = cv2.flip(frame, 1)

    # Send to landmarker
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    timestamp += 1
    landmarker.detect_async(mp_image, timestamp)

    # Draw results
    if latest_result and latest_result.hand_landmarks:
        for i, hand_landmarks in enumerate(latest_result.hand_landmarks):

            # Draw skeleton
            draw_hand(frame, hand_landmarks)

            # Label near wrist
            label = "Left" if latest_result.handedness[i][0].display_name == "Right" else "Right"
            h, w = frame.shape[:2]
            wrist = hand_landmarks[0]
            cx, cy = int(wrist.x * w), int(wrist.y * h)
            cv2.putText(
                frame, label,
                (cx - 30, cy + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 255, 255), 2, cv2.LINE_AA,
            )

    cv2.imshow("GuitarCV - Phase 1", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ── Cleanup ───────────────────────────────────────────────────────────────────
cap.release()
landmarker.close()
cv2.destroyAllWindows()