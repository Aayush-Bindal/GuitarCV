import cv2
import config
import wheel
from hands import HandTracker

def main():
    tracker = HandTracker()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    base_img, glow_img = wheel.load_wheel_images()
    timestamp = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        timestamp += 1
        
        tracker.process_frame(frame, timestamp)
        
        active_index = -1
        if tracker.latest_result and tracker.latest_result.hand_landmarks:
            for i, hand_landmarks in enumerate(tracker.latest_result.hand_landmarks):
                # Right means Left after flip
                if tracker.latest_result.handedness[i][0].display_name == "Right":
                    h, w = frame.shape[:2]
                    knuckle = (int(hand_landmarks[5].x * w), int(hand_landmarks[5].y * h))
                    fingertip = (int(hand_landmarks[8].x * w), int(hand_landmarks[8].y * h))
                    active_index = wheel.get_active_segment(knuckle, fingertip)
                    break
        
        frame = wheel.composite_wheel(frame, base_img, glow_img, config.WHEEL_CENTER, active_index)
        chord_name = "No chord" if active_index == -1 else config.CHORDS[active_index]

        wheel.draw_chord_labels(frame, active_index)
        tracker.draw_results(frame)

        (tw, th), _ = cv2.getTextSize(chord_name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)
        h, w = frame.shape[:2]
        cv2.putText(frame, chord_name, (w//2 - tw//2, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

        cv2.imshow(config.WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
