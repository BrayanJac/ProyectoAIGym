import time
import cv2
import numpy as np


def rest_screen(cap, exercise_name, seconds):
    w, h = 640, 480
    start = time.time()

    while time.time() - start < seconds:
        remaining = seconds - int(time.time() - start)

        frame = np.zeros((h, w, 3), dtype=np.uint8)
        cv2.putText(frame, "DESCANSO", (180, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

        cv2.putText(frame, f"{remaining} s", (250, 260),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)

        cv2.imshow(exercise_name, frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break


def draw_progress_bar(frame, current_angle, up_angle, down_angle):
    bar_x = 20
    bar_y = 200
    bar_width = 40
    bar_height = 200
    
    # Calcular porcentaje (0 a 100)
    angle_range = down_angle - up_angle
    if current_angle < up_angle:
        percentage = 0
    elif current_angle > down_angle:
        percentage = 100
    else:
        percentage = ((current_angle - up_angle) / angle_range) * 100
    
    # Dibujar marco de la barra
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 255, 255), 2)
    
    # Dibujar barra rellena (progreso)
    fill_height = int((percentage / 100) * bar_height)
    if fill_height > 0:
        cv2.rectangle(frame, 
                     (bar_x, bar_y + bar_height - fill_height), 
                     (bar_x + bar_width, bar_y + bar_height), 
                     (0, 255, 0), -1)
    
    # Escribir porcentaje
    cv2.putText(frame, f"{int(percentage)}%", (bar_x - 10, bar_y + bar_height + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


def draw_flexion_progress_bar(frame, current_ratio, threshold_up, threshold_down):
    bar_x = 20
    bar_y = 200
    bar_width = 40
    bar_height = 200
    
    # Calcular porcentaje (0 a 100)
    ratio_range = threshold_down - threshold_up
    if current_ratio < threshold_up:
        percentage = 0
    elif current_ratio > threshold_down:
        percentage = 100
    else:
        percentage = ((current_ratio - threshold_up) / ratio_range) * 100
    
    # Dibujar marco de la barra
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 255, 255), 2)
    
    # Dibujar barra rellena (progreso)
    fill_height = int((percentage / 100) * bar_height)
    if fill_height > 0:
        cv2.rectangle(frame, 
                     (bar_x, bar_y + bar_height - fill_height), 
                     (bar_x + bar_width, bar_y + bar_height), 
                     (0, 255, 0), -1)
    
    # Escribir porcentaje
    cv2.putText(frame, f"{int(percentage)}%", (bar_x - 10, bar_y + bar_height + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


def draw_rotation_progress_bar(frame, current_ratio, threshold_left, threshold_right):
    bar_x = 20
    bar_y = 200
    bar_width = 40
    bar_height = 200
    
    # Calcular porcentaje (0 a 100)
    ratio_range = threshold_left - threshold_right
    if current_ratio < threshold_right:
        percentage = 0
    elif current_ratio > threshold_left:
        percentage = 100
    else:
        percentage = ((current_ratio - threshold_right) / ratio_range) * 100
    
    # Dibujar marco de la barra
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 255, 255), 2)
    
    # Dibujar barra rellena (progreso)
    fill_height = int((percentage / 100) * bar_height)
    if fill_height > 0:
        cv2.rectangle(frame, 
                     (bar_x, bar_y + bar_height - fill_height), 
                     (bar_x + bar_width, bar_y + bar_height), 
                     (0, 255, 0), -1)
    
    # Escribir porcentaje
    cv2.putText(frame, f"{int(percentage)}%", (bar_x - 10, bar_y + bar_height + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
