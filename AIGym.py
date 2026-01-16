from ultralytics import YOLO
import cv2
import numpy as np

# -------------------------------
# CONFIGURACIÓN
# -------------------------------

UP_ANGLE = 50        # codo flexionado
DOWN_ANGLE = 160     # brazo extendido
CONF_THRESHOLD = 0.5

# Esqueleto brazo derecho
SKELETON = [
    (6, 8),   # hombro - codo
    (8, 10)   # codo - muñeca
]

# -------------------------------
# FUNCIONES
# -------------------------------

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return np.degrees(np.arccos(cos_angle))


def is_valid_arm(conf):
    for i in [6, 8, 10]:
        if conf[i] < CONF_THRESHOLD:
            return False
    return True


def draw_skeleton(frame, kpts, conf):
    for i, (x, y) in enumerate(kpts):
        if conf[i] > CONF_THRESHOLD:
            cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 255), -1)

    for p1, p2 in SKELETON:
        if conf[p1] > CONF_THRESHOLD and conf[p2] > CONF_THRESHOLD:
            x1, y1 = kpts[p1]
            x2, y2 = kpts[p2]
            cv2.line(frame,
                     (int(x1), int(y1)),
                     (int(x2), int(y2)),
                     (0, 255, 0), 2)

# -------------------------------
# MODELO
# -------------------------------

model = YOLO("yolov8n-pose.pt")
cap = cv2.VideoCapture(0)

reps = 0
state = "down"

# -------------------------------
# LOOP PRINCIPAL
# -------------------------------

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.5, verbose=False)

    if results and results[0].keypoints is not None:
        kpts_xy = results[0].keypoints.xy
        kpts_conf = results[0].keypoints.conf

        if kpts_xy is not None and len(kpts_xy) > 0:
            kpts = kpts_xy[0]
            conf = kpts_conf[0]

            draw_skeleton(frame, kpts, conf)

            if is_valid_arm(conf):
                shoulder = kpts[6]
                elbow = kpts[8]
                wrist = kpts[10]

                elbow_angle = calculate_angle(shoulder, elbow, wrist)

                # SUBIDA
                if elbow_angle < UP_ANGLE and state == "down":
                    state = "up"

                # BAJADA = REP
                if elbow_angle > DOWN_ANGLE and state == "up":
                    reps += 1
                    state = "down"

                cv2.putText(frame, f"Angulo codo: {int(elbow_angle)}",
                            (30, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (255, 255, 255), 2)

            else:
                cv2.putText(frame, "Brazo no detectado",
                            (30, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)

    cv2.putText(frame, f"Reps: {reps}",
                (30, 100), cv2.FONT_HERSHEY_SIMPLEX,
                1.5, (0, 255, 0), 3)

    cv2.imshow("Curl de Biceps AI", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
