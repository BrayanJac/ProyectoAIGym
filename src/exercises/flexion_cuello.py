from ultralytics import YOLO
import cv2
import numpy as np
import os
from src.utils import rest_screen, draw_flexion_progress_bar

CONF = 0.5
THRESHOLD_UP = 0.85
THRESHOLD_DOWN = 1.15
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../yolov8n-pose.pt")


def run_flexion_cuello(target_reps, rest_time):
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(0)

    reps = 0
    state = "neutral"

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

            if min(c[0], c[3], c[4]) > CONF:
                nariz_y = p[0][1]
                oreja_y = (p[3][1] + p[4][1]) / 2

                ratio = nariz_y / oreja_y if oreja_y > 0 else 1.0

                # Dibuja puntos de referencia
                cv2.circle(frame, (int(p[0][0]), int(p[0][1])), 5, (0, 255, 0), -1)  # nariz - verde
                cv2.circle(frame, (int(p[3][0]), int(p[3][1])), 5, (0, 255, 255), -1)  # oreja izq - cian
                cv2.circle(frame, (int(p[4][0]), int(p[4][1])), 5, (0, 165, 255), -1)  # oreja der - naranja
                
                # Dibujar barra de progreso
                draw_flexion_progress_bar(frame, ratio, THRESHOLD_UP, THRESHOLD_DOWN)

                if ratio < THRESHOLD_UP and state == "neutral":
                    state = "up"

                if ratio > THRESHOLD_DOWN and state == "up":
                    reps += 1
                    state = "neutral"

                # Mostrar ratio para debug
                cv2.putText(frame,
                            f"Ratio: {ratio:.2f}",
                            (30, 140),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255, 255, 255), 2)

        cv2.putText(frame,
                    f"Reps: {reps}/{target_reps}",
                    (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5, (0, 255, 0), 3)

        cv2.putText(frame,
                    "Flexion de Cuello",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 0), 2)

        cv2.imshow("Flexion de Cuello", frame)

        if reps >= target_reps:
            rest_screen(cap, "Flexion de Cuello", rest_time)
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
