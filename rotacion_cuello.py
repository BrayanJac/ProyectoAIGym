from ultralytics import YOLO
import cv2
import numpy as np
from utils import speak_async, rest_screen

# Configuración para detectar rotación de cuello
# Usamos la distancia horizontal entre orejas
CONF = 0.5
THRESHOLD_LEFT = 1.3   # Cabeza girada a la izquierda (oreja izq más visible)
THRESHOLD_RIGHT = 0.7  # Cabeza girada a la derecha (oreja der más visible)

def run_rotacion_cuello(target_reps, rest_time):
    model = YOLO("yolov8n-pose.pt")
    cap = cv2.VideoCapture(0)

    reps = 0
    state = "center"

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
            if min(c[0], c[3], c[4]) > CONF:
                nariz_x = p[0][0]
                oreja_izq_x = p[3][0]
                oreja_der_x = p[4][0]

                # Calculamos el centro entre las orejas
                centro_orejas = (oreja_izq_x + oreja_der_x) / 2

                # Distancia de la nariz al centro
                distancia_izq = abs(nariz_x - oreja_izq_x)
                distancia_der = abs(nariz_x - oreja_der_x)

                # Ratio para determinar rotación
                ratio = distancia_izq / distancia_der if distancia_der > 0 else 1.0

                # Dibuja puntos de referencia
                cv2.circle(frame, (int(p[0][0]), int(p[0][1])), 5, (0, 255, 0), -1)  # nariz
                cv2.circle(frame, (int(p[3][0]), int(p[3][1])), 5, (255, 0, 0), -1)  # oreja izq
                cv2.circle(frame, (int(p[4][0]), int(p[4][1])), 5, (0, 0, 255), -1)  # oreja der

                # Línea entre orejas
                cv2.line(frame, 
                        (int(oreja_izq_x), int(p[3][1])),
                        (int(oreja_der_x), int(p[4][1])),
                        (255, 255, 0), 2)

                # Estado: cabeza girada a la izquierda
                if ratio > THRESHOLD_LEFT and state == "center":
                    state = "left"

                # Estado: cabeza girada a la derecha (completa repetición)
                elif ratio < THRESHOLD_RIGHT and state == "left":
                    reps += 1
                    speak_async(reps)
                    state = "center"

                # Volver al centro desde derecha
                elif ratio > THRESHOLD_RIGHT and ratio < THRESHOLD_LEFT and state == "left":
                    state = "center"

                # Mostrar ratio para debug
                cv2.putText(frame,
                            f"Ratio: {ratio:.2f}",
                            (30, 140),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255, 255, 255), 2)

                # Indicador de dirección
                direccion = "IZQUIERDA" if ratio > THRESHOLD_LEFT else "DERECHA" if ratio < THRESHOLD_RIGHT else "CENTRO"
                cv2.putText(frame,
                            f"Dir: {direccion}",
                            (30, 170),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 255), 2)

        cv2.putText(frame,
                    f"Reps: {reps}/{target_reps}",
                    (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5, (0, 255, 0), 3)

        cv2.putText(frame,
                    "Rotacion de Cuello",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 0), 2)

        cv2.imshow("Rotacion de Cuello", frame)

        if reps >= target_reps:
            rest_screen(cap, "Rotacion de Cuello", rest_time)
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
