import cv2
import math
import time
import numpy as np
import config

def draw_strings(frame, vibration_progress):
    overlay = frame.copy()
    xs = np.linspace(config.STRINGS_X_START, config.STRINGS_X_END, 40)
    for i in range(6):
        y = config.STRINGS_Y_POSITIONS[i]
        thick = config.STRING_THICKNESSES[i]
        color = config.STRING_COLORS[i]
        pts = []
        for x in xs:
            y_off = 0
            if vibration_progress > 0:
                decay = 1.0 - (i / 10.0)
                amp = vibration_progress * 12 * decay
                y_off = math.sin(x * 0.03 + time.time() * 15) * amp
            pts.append([int(x), int(y + y_off)])
        pts = np.array(pts, np.int32).reshape((-1, 1, 2))
        cv2.polylines(overlay, [pts], False, color, thick + 6)
    cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
    for i in range(6):
        y = config.STRINGS_Y_POSITIONS[i]
        thick = config.STRING_THICKNESSES[i]
        color = config.STRING_COLORS[i]
        pts = []
        for x in xs:
            y_off = 0
            if vibration_progress > 0:
                decay = 1.0 - (i / 10.0)
                amp = vibration_progress * 12 * decay
                y_off = math.sin(x * 0.03 + time.time() * 15) * amp
            pts.append([int(x), int(y + y_off)])
        pts = np.array(pts, np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], False, color, thick)

def detect_strum(right_landmarks, prev_y, last_strum_time):
    if right_landmarks is None:
        return False, None, None, last_strum_time
    curr_y = right_landmarks[1]
    now = time.time() * 1000
    strummed, direction = False, None
    if prev_y is not None:
        if abs(curr_y - prev_y) > config.STRUM_THRESHOLD and (now - last_strum_time) > config.STRUM_COOLDOWN_MS:
            strummed = True
            direction = "down" if curr_y > prev_y else "up"
            last_strum_time = now
    return strummed, direction, curr_y, last_strum_time

def get_vibration_progress(last_strum_time):
    if last_strum_time == 0:
        return 0.0
    elapsed = (time.time() * 1000) - last_strum_time
    if elapsed >= config.VIBRATION_DURATION_MS:
        return 0.0
    return 1.0 - (elapsed / config.VIBRATION_DURATION_MS)
