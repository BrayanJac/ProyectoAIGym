from ultralytics import YOLO
import cv2
import numpy as np
from utils import speak_async, rest_screen

# Configuración para detectar flexión de cuello
# Usamos la distancia vertical entre nariz y oreja
CONF = 0.5
THRESHOLD_UP = 0.85    # Cabeza hacia arriba/atrás (nariz más arriba que oreja)
THRESHOLD_DOWN = 1.15  # Cabeza hacia abajo/adelante (nariz más abajo que oreja)

def run_flexion_cuello(target_reps, rest_time):
    model = YOLO("yolov8n-pose.pt")
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

            # Keypoints: 0-nariz, 3-oreja_izq, 4-oreja_der
            # Usamos nariz (0) y promedio de orejas (3,4)
            if min(c[0], c[3], c[4]) > CONF:
                nariz_y = p[0][1]
                oreja_y = (p[3][1] + p[4][1]) / 2

                # Calculamos ratio de posición
                ratio = nariz_y / oreja_y if oreja_y > 0 else 1.0

                # Dibuja puntos de referencia
                cv2.circle(frame, (int(p[0][0]), int(p[0][1])), 5, (0, 255, 0), -1)  # nariz
                cv2.circle(frame, (int(p[3][0]), int(p[3][1])), 5, (255, 0, 0), -1)  # oreja izq
                cv2.circle(frame, (int(p[4][0]), int(p[4][1])), 5, (255, 0, 0), -1)  # oreja der

                # Estado: cabeza hacia arriba
                if ratio < THRESHOLD_UP and state == "neutral":
                    state = "up"

                # Estado: cabeza hacia abajo (completa repetición)
                if ratio > THRESHOLD_DOWN and state == "up":
                    reps += 1
                    speak_async(reps)
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
