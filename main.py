import cv2
import config
from hands import HandTracker

def main():
    tracker = HandTracker()
    cap = cv2.VideoCapture(0)
    timestamp = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        timestamp += 1
        
        # Send to landmarker
        tracker.process_frame(frame, timestamp)
        
        # Draw results
        tracker.draw_results(frame)

        cv2.imshow(config.WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
