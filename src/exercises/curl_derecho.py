from ultralytics import YOLO
import cv2
import os
from src.utils import angle, rest_screen, draw_progress_bar

UP, DOWN, CONF = 50, 160, 0.5
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../yolov8n-pose.pt")


def run_curl_derecho(target_reps, rest_time):
    model = YOLO(MODEL_PATH)
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
                # Dibuja puntos de referencia
                cv2.circle(frame, (int(p[6][0]), int(p[6][1])), 5, (0, 255, 0), -1)  # hombro - verde
                cv2.circle(frame, (int(p[8][0]), int(p[8][1])), 5, (0, 255, 255), -1)  # codo - cian
                cv2.circle(frame, (int(p[10][0]), int(p[10][1])), 5, (0, 165, 255), -1)  # muñeca - naranja
                
                # Dibuja líneas del brazo
                cv2.line(frame, (int(p[6][0]), int(p[6][1])), (int(p[8][0]), int(p[8][1])), (0, 200, 255), 2)
                cv2.line(frame, (int(p[8][0]), int(p[8][1])), (int(p[10][0]), int(p[10][1])), (0, 200, 255), 2)
                
                ang = angle(p[6], p[8], p[10])
                
                # Dibujar barra de progreso
                draw_progress_bar(frame, ang, UP, DOWN)

                if ang < UP and state == "down":
                    state = "up"

                if ang > DOWN and state == "up":
                    reps += 1
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
