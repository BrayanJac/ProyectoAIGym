from ultralytics import YOLO
import cv2
from utils import angle, speak_async, rest_screen

UP, DOWN, CONF = 50, 160, 0.5

def run_curl_derecho(target_reps, rest_time):
    model = YOLO("yolov8n-pose.pt")
    cap = cv2.VideoCapture(0)

    reps = 0
    state = "down"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        r = model(frame, verbose=False)

        if (
            reps < target_reps and
            r and
            r[0].keypoints is not None and
            len(r[0].keypoints.xy) > 0
        ):
            p = r[0].keypoints.xy[0]
            c = r[0].keypoints.conf[0]

            if min(c[6], c[8], c[10]) > CONF:
                ang = angle(p[6], p[8], p[10])

                if ang < UP and state == "down":
                    state = "up"

                if ang > DOWN and state == "up":
                    reps += 1
                    speak_async(reps)
                    state = "down"

        cv2.putText(frame,
                    f"Reps: {reps}/{target_reps}",
                    (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5, (0, 255, 0), 3)

        cv2.imshow("Curl Biceps Derecho", frame)

        if reps >= target_reps:
            rest_screen(cap, "Curl Biceps Derecho", rest_time)
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
