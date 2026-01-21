import sys
import os
import tkinter as tk
from tkinter import messagebox
import threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.exercises import (
    run_curl_derecho,
    run_curl_izquierdo,
    run_curl_ambos,
    run_flexion_cuello,
    run_rotacion_cuello,
)


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

        for s in range(1, series + 1):
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

        root.deiconify()

        messagebox.showinfo(
            "Finalizado",
            "Entrenamiento terminado.\nPuedes elegir otro ejercicio."
        )

    threading.Thread(target=workout, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Entrenador Inteligente AI Gym")
    root.update_idletasks()

    # Centrar ventana
    window_width = 500
    window_height = 750

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)
    
    # Paleta de colores
    BG_COLOR = "#1a1a1a"
    ACCENT_COLOR = "#00d4ff"
    BUTTON_COLOR = "#0099cc"
    BUTTON_HOVER = "#00ccff"
    TEXT_COLOR = "#ffffff"
    LABEL_COLOR = "#cccccc"
    
    root.config(bg=BG_COLOR)
    
    # Título principal
    title_frame = tk.Frame(root, bg=ACCENT_COLOR, height=80)
    title_frame.pack(fill=tk.X, padx=0, pady=0)
    title_frame.pack_propagate(False)
    
    tk.Label(title_frame, 
             text="Entrenador Inteligente",
             font=("Segoe UI", 24, "bold"),
             bg=ACCENT_COLOR,
             fg="#000000").pack(pady=15)
    
    # Frame de inputs
    input_label = tk.Label(root, 
                           text="Configuración de Entrenamiento",
                           font=("Segoe UI", 12, "bold"),
                           bg=BG_COLOR,
                           fg=ACCENT_COLOR)
    input_label.pack(pady=(20, 10))
    
    frame_inputs = tk.Frame(root, bg=BG_COLOR)
    frame_inputs.pack(pady=10, padx=20)
    
    # Entrada de repeticiones
    tk.Label(frame_inputs, text="Repeticiones:", font=("Segoe UI", 10), 
             bg=BG_COLOR, fg=LABEL_COLOR).grid(row=0, column=0, sticky="w", pady=8)
    entry_reps = tk.Entry(frame_inputs, width=15, justify="center",
                         font=("Segoe UI", 11),
                         bg="#2a2a2a", fg=ACCENT_COLOR, 
                         insertbackground=ACCENT_COLOR,
                         relief=tk.FLAT, bd=2)
    entry_reps.grid(row=0, column=1, padx=10, pady=8)
    
    # Entrada de series
    tk.Label(frame_inputs, text="Series:", font=("Segoe UI", 10),
             bg=BG_COLOR, fg=LABEL_COLOR).grid(row=1, column=0, sticky="w", pady=8)
    entry_series = tk.Entry(frame_inputs, width=15, justify="center",
                           font=("Segoe UI", 11),
                           bg="#2a2a2a", fg=ACCENT_COLOR,
                           insertbackground=ACCENT_COLOR,
                           relief=tk.FLAT, bd=2)
    entry_series.grid(row=1, column=1, padx=10, pady=8)
    
    # Entrada de descanso
    tk.Label(frame_inputs, text="Descanso (s):", font=("Segoe UI", 10),
             bg=BG_COLOR, fg=LABEL_COLOR).grid(row=2, column=0, sticky="w", pady=8)
    entry_rest = tk.Entry(frame_inputs, width=15, justify="center",
                         font=("Segoe UI", 11),
                         bg="#2a2a2a", fg=ACCENT_COLOR,
                         insertbackground=ACCENT_COLOR,
                         relief=tk.FLAT, bd=2)
    entry_rest.grid(row=2, column=1, padx=10, pady=8)
    
    # Valores por defecto
    entry_reps.insert(0, "10")
    entry_series.insert(0, "2")
    entry_rest.insert(0, "10")
    
    # Estilo de botones
    button_style = {
        "font": ("Segoe UI", 10, "bold"),
        "width": 35,
        "bg": BUTTON_COLOR,
        "fg": TEXT_COLOR,
        "relief": tk.FLAT,
        "padx": 10,
        "pady": 8,
        "cursor": "hand2",
        "activebackground": BUTTON_HOVER,
        "activeforeground": TEXT_COLOR
    }
    
    # Ejercicios de brazos
    tk.Label(root, text="Ejercicios de Brazos",
             font=("Segoe UI", 12, "bold"),
             bg=BG_COLOR,
             fg=ACCENT_COLOR).pack(pady=(20, 10))
    
    tk.Button(root, text="Curl Derecho", command=lambda: start_exercise("derecho"), **button_style).pack(pady=5)
    tk.Button(root, text="Curl Izquierdo", command=lambda: start_exercise("izquierdo"), **button_style).pack(pady=5)
    tk.Button(root, text="Curl Ambos Brazos", command=lambda: start_exercise("ambos"), **button_style).pack(pady=5)
    
    # Ejercicios de cuello
    tk.Label(root, text="Ejercicios de Cuello",
             font=("Segoe UI", 12, "bold"),
             bg=BG_COLOR,
             fg=ACCENT_COLOR).pack(pady=(20, 10))
    
    tk.Button(root, text="Flexión de Cuello", command=lambda: start_exercise("flexion_cuello"), **button_style).pack(pady=5)
    tk.Button(root, text="Rotación de Cuello", command=lambda: start_exercise("rotacion_cuello"), **button_style).pack(pady=5)
    
    # Footer
    tk.Label(root, text="Presiona ESC para salir de la cámara",
             font=("Segoe UI", 9), 
             bg=BG_COLOR,
             fg="#666666").pack(side="bottom", pady=15)

    root.mainloop()

