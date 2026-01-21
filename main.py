import tkinter as tk
from tkinter import messagebox
import threading

from utils import speak_async, start_voice
from curl_derecho import run_curl_derecho
from curl_izquierdo import run_curl_izquierdo
from curl_ambos import run_curl_ambos
from flexion_cuello import run_flexion_cuello
from rotacion_cuello import run_rotacion_cuello


# -----------------------------
# FUNCIÓN PRINCIPAL
# -----------------------------
def start_exercise(exercise_type):
    try:
        reps = int(entry_reps.get())
        series = int(entry_series.get())
        rest = int(entry_rest.get())
    except ValueError:
        messagebox.showerror("Error", "Ingresa solo números válidos")
        return

    if reps <= 0 or series <= 0 or rest <= 0:
        messagebox.showerror("Error", "Valores mayores a 0")
        return

    def workout():
        root.withdraw()
        speak_async("Entrenamiento iniciado")

        for s in range(1, series + 1):
            speak_async(f"Serie {s}")

            if exercise_type == "derecho":
                run_curl_derecho(reps, rest)

            elif exercise_type == "izquierdo":
                run_curl_izquierdo(reps, rest)

            elif exercise_type == "ambos":
                run_curl_ambos(reps, rest)

            elif exercise_type == "flexion_cuello":
                run_flexion_cuello(reps, rest)

            elif exercise_type == "rotacion_cuello":
                run_rotacion_cuello(reps, rest)

        speak_async("Entrenamiento finalizado")
        root.deiconify()

        messagebox.showinfo(
            "Finalizado",
            "Entrenamiento terminado.\nPuedes elegir otro ejercicio."
        )

    # 🔹 THREAD (OBLIGATORIO)
    threading.Thread(target=workout, daemon=True).start()


# -----------------------------
# PROGRAMA PRINCIPAL
# -----------------------------
if __name__ == "__main__":
    start_voice()

    root = tk.Tk()
    root.title("Entrenador Inteligente")
    root.geometry("420x620")
    root.resizable(False, False)

    tk.Label(root, text="Entrenador Inteligente",
             font=("Arial", 18, "bold")).pack(pady=15)

    frame_inputs = tk.Frame(root)
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="Repeticiones").grid(row=0, column=0)
    entry_reps = tk.Entry(frame_inputs, width=10, justify="center")
    entry_reps.grid(row=0, column=1)

    tk.Label(frame_inputs, text="Series").grid(row=1, column=0)
    entry_series = tk.Entry(frame_inputs, width=10, justify="center")
    entry_series.grid(row=1, column=1)

    tk.Label(frame_inputs, text="Descanso (s)").grid(row=2, column=0)
    entry_rest = tk.Entry(frame_inputs, width=10, justify="center")
    entry_rest.grid(row=2, column=1)

    entry_reps.insert(0, "10")
    entry_series.insert(0, "3")
    entry_rest.insert(0, "10")

    tk.Label(root, text="Selecciona ejercicio",
             font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Curl Derecho", width=30,
              command=lambda: start_exercise("derecho")).pack(pady=5)

    tk.Button(root, text="Curl Izquierdo", width=30,
              command=lambda: start_exercise("izquierdo")).pack(pady=5)

    tk.Button(root, text="Curl Ambos", width=30,
              command=lambda: start_exercise("ambos")).pack(pady=5)

    tk.Label(root, text="Ejercicios de Cuello",
             font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(root, text="Flexión de Cuello", width=30,
              command=lambda: start_exercise("flexion_cuello")).pack(pady=5)

    tk.Button(root, text="Rotación de Cuello", width=30,
              command=lambda: start_exercise("rotacion_cuello")).pack(pady=5)

    tk.Label(root, text="ESC para salir de cámara",
             font=("Arial", 9), fg="gray").pack(side="bottom", pady=10)

    root.mainloop()
