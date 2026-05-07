import cv2
import math
import numpy as np
import config

def load_wheel_images():
    base_img = cv2.imread('assets/base.png', cv2.IMREAD_UNCHANGED)
    glow_img = cv2.imread('assets/glow.png', cv2.IMREAD_UNCHANGED)
    sz = (config.WHEEL_DISPLAY_SIZE, config.WHEEL_DISPLAY_SIZE)
    return cv2.resize(base_img, sz), cv2.resize(glow_img, sz)

def get_active_segment(knuckle, fingertip):
    dx, dy = fingertip[0] - knuckle[0], fingertip[1] - knuckle[1]
    if math.hypot(dx, dy) < 25:
        return -1
    angle = math.degrees(math.atan2(dy, dx)) % 360
    base = (config.SEGMENT_0_CENTER_ANGLE - 30) % 360
    rel_angle = (angle - base) % 360
    return int(rel_angle // 60) % 6

def rotate_image(img, angle_degrees):
    h, w = img.shape[:2]
    matrix = cv2.getRotationMatrix2D((w // 2, h // 2), -angle_degrees, 1.0)
    return cv2.warpAffine(img, matrix, (w, h), flags=cv2.INTER_LINEAR, 
                          borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))

def composite_wheel(frame, base_img, glow_img, center, active_index):
    def blend(f, img):
        h, w = img.shape[:2]
        x1, y1 = center[0] - w//2, center[1] - h//2
        x2, y2 = x1 + w, y1 + h
        fh, fw = f.shape[:2]
        fx1, fy1, fx2, fy2 = max(0, x1), max(0, y1), min(fw, x2), min(fh, y2)
        wx1, wy1, wx2, wy2 = fx1 - x1, fy1 - y1, fx2 - x1, fy2 - y1
        if fx1 < fx2 and fy1 < fy2:
            alpha = np.expand_dims(img[wy1:wy2, wx1:wx2, 3] / 255.0, axis=-1)
            rgb = img[wy1:wy2, wx1:wx2, :3]
            f[fy1:fy2, fx1:fx2] = f[fy1:fy2, fx1:fx2] * (1 - alpha) + rgb * alpha
            
    blend(frame, base_img)
    if 0 <= active_index <= 5:
        rot_glow = rotate_image(glow_img, active_index * 60)
        blend(frame, rot_glow)
    return frame

def draw_chord_labels(frame, active_index):
    for i, chord in enumerate(config.CHORDS):
        angle = math.radians(config.SEGMENT_0_CENTER_ANGLE + i * 60)
        x = int(config.WHEEL_CENTER[0] + config.LABEL_RADIUS * math.cos(angle))
        y = int(config.WHEEL_CENTER[1] + config.LABEL_RADIUS * math.sin(angle))
        color = config.CHORD_TEXT_ACTIVE_COLOR if i == active_index else config.CHORD_TEXT_COLOR
        scale, thick = (0.85, 2) if i == active_index else (0.75, 1)
        (tw, th), _ = cv2.getTextSize(chord, cv2.FONT_HERSHEY_SIMPLEX, scale, thick)
        cv2.putText(frame, chord, (x - tw//2, y + th//2),
                    cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick)
