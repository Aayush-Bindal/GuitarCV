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

# Strings area
STRINGS_X_START = 820
STRINGS_X_END = 1220
STRINGS_Y_POSITIONS = [500, 524, 548, 572, 596, 620]  # top=low E, bottom=high e
STRING_THICKNESSES = [4, 3, 3, 2, 2, 1]               # top=thickest, bottom=thinnest
STRING_COLORS = [
    (80,  150, 190),   # low E   - warm amber
    (100, 165, 200),   # A       - amber
    (120, 175, 210),   # D       - amber
    (150, 185, 215),   # G       - amber
    (192, 192, 192),   # B       - distinct silver
    (220, 220, 220),   # high e  - bright silver
]
STRING_GLOW_COLOR = (60, 120, 180)
STRUM_THRESHOLD = 18       # px delta Y to trigger strum
STRUM_COOLDOWN_MS = 400
VIBRATION_DURATION_MS = 600

WINDOW_NAME = "GuitarCV - Phase 2"
