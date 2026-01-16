import pyttsx3
from multiprocessing import Process, Queue
import time
import cv2
import numpy as np

# -----------------------------
# COLA GLOBAL DE VOZ
# -----------------------------
voice_queue = Queue()
voice_proc = None


# -----------------------------
# PROCESO DE VOZ
# -----------------------------
def voice_worker(q):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)

    while True:
        text = q.get()
        if text == "__STOP__":
            break
        engine.say(text)
        engine.runAndWait()


# -----------------------------
# INICIAR VOZ (EXPLÍCITO)
# -----------------------------
def start_voice():
    global voice_proc
    if voice_proc is None or not voice_proc.is_alive():
        voice_proc = Process(target=voice_worker, args=(voice_queue,), daemon=True)
        voice_proc.start()


# -----------------------------
# HABLAR (NO BLOQUEANTE)
# -----------------------------
def speak_async(text):
    voice_queue.put(str(text))


# -----------------------------
# PANTALLA DE DESCANSO
# -----------------------------
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

# ================== GEOMETRÍA ==================

def angle(a, b, c):
    a, b, c = map(np.array, (a, b, c))
    ba = a - b
    bc = c - b
    cosang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosang, -1, 1)))