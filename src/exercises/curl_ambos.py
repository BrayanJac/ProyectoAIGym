from ultralytics import YOLO
import cv2
import os
from src.utils import angle, rest_screen, draw_progress_bar

UP, DOWN, CONF = 50, 160, 0.5
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../yolov8n-pose.pt")


def run_curl_ambos(target_reps, rest_time):
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(0)

    repsL, repsR = 0, 0
    stateL, stateR = "down", "down"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        r = model(frame, verbose=False)

        if (
            r and
            r[0].keypoints is not None and
            len(r[0].keypoints.xy) > 0
        ):
            p = r[0].keypoints.xy[0]
            c = r[0].keypoints.conf[0]

            # IZQUIERDO
            if repsL < target_reps and min(c[5], c[7], c[9]) > CONF:
                # Dibuja puntos de referencia brazo izquierdo
                cv2.circle(frame, (int(p[5][0]), int(p[5][1])), 5, (0, 255, 0), -1)  # hombro - verde
                cv2.circle(frame, (int(p[7][0]), int(p[7][1])), 5, (0, 255, 255), -1)  # codo - cian
                cv2.circle(frame, (int(p[9][0]), int(p[9][1])), 5, (0, 165, 255), -1)  # muñeca - naranja
                
                # Dibuja líneas del brazo izquierdo
                cv2.line(frame, (int(p[5][0]), int(p[5][1])), (int(p[7][0]), int(p[7][1])), (0, 200, 255), 2)
                cv2.line(frame, (int(p[7][0]), int(p[7][1])), (int(p[9][0]), int(p[9][1])), (0, 200, 255), 2)
                
                angL = angle(p[5], p[7], p[9])
                
                # Dibujar barra de progreso para brazo izquierdo
                draw_progress_bar(frame, angL, UP, DOWN)

                if angL < UP and stateL == "down":
                    stateL = "up"

                if angL > DOWN and stateL == "up":
                    repsL += 1
                    stateL = "down"

            # DERECHO
            if repsR < target_reps and min(c[6], c[8], c[10]) > CONF:
                # Dibuja puntos de referencia brazo derecho
                cv2.circle(frame, (int(p[6][0]), int(p[6][1])), 5, (0, 255, 0), -1)  # hombro - verde
                cv2.circle(frame, (int(p[8][0]), int(p[8][1])), 5, (0, 255, 255), -1)  # codo - cian
                cv2.circle(frame, (int(p[10][0]), int(p[10][1])), 5, (0, 165, 255), -1)  # muñeca - naranja
                
                # Dibuja líneas del brazo derecho
                cv2.line(frame, (int(p[6][0]), int(p[6][1])), (int(p[8][0]), int(p[8][1])), (0, 200, 255), 2)
                cv2.line(frame, (int(p[8][0]), int(p[8][1])), (int(p[10][0]), int(p[10][1])), (0, 200, 255), 2)
                
                angR = angle(p[6], p[8], p[10])
                
                # Dibujar barra de progreso para brazo derecho (modificar posición x)
                bar_x_right = 60
                bar_y = 200
                bar_width = 40
                bar_height = 200
                
                angle_range = DOWN - UP
                if angR < UP:
                    percentage = 0
                elif angR > DOWN:
                    percentage = 100
                else:
                    percentage = ((angR - UP) / angle_range) * 100
                
                cv2.rectangle(frame, (bar_x_right, bar_y), (bar_x_right + bar_width, bar_y + bar_height), (0, 255, 255), 2)
                fill_height = int((percentage / 100) * bar_height)
                if fill_height > 0:
                    cv2.rectangle(frame, 
                                 (bar_x_right, bar_y + bar_height - fill_height), 
                                 (bar_x_right + bar_width, bar_y + bar_height), 
                                 (0, 255, 0), -1)
                cv2.putText(frame, f"{int(percentage)}%", (bar_x_right - 10, bar_y + bar_height + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if angR < UP and stateR == "down":
                    stateR = "up"

                if angR > DOWN and stateR == "up":
                    repsR += 1
                    stateR = "down"

        cv2.putText(frame, f"Izq: {repsL}/{target_reps}",
                    (30, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    1.3, (255, 0, 0), 3)

        cv2.putText(frame, f"Der: {repsR}/{target_reps}",
                    (30, 140), cv2.FONT_HERSHEY_SIMPLEX,
                    1.3, (0, 255, 0), 3)

        if repsL >= target_reps and repsR >= target_reps:
            rest_screen(cap, "Curl Ambos Brazos", rest_time)
            break

        cv2.imshow("Curl Ambos Brazos", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
