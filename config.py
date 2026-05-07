MODEL_PATH = "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"

NUM_HANDS = 2
MIN_HAND_DETECTION_CONFIDENCE = 0.7
MIN_HAND_PRESENCE_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7

CHORDS = ["C", "G", "Am", "Em", "F", "D"]
WHEEL_DISPLAY_SIZE = 350
WHEEL_CENTER = (230, 519)  # lower-left area of 1280x720
LABEL_RADIUS = 115  # px from wheel center to chord text
SEGMENT_0_CENTER_ANGLE = 212  # degrees, in screen angle (right=0, clockwise positive)
CHORD_TEXT_COLOR = (220, 210, 190)
CHORD_TEXT_ACTIVE_COLOR = (0, 220, 255)

WINDOW_NAME = "GuitarCV - Phase 2"
