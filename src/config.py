# Configuraciones Globales para ProyectoAIGym
# Curl - Configuración de ángulos
CURL_UP_ANGLE = 50          # Ángulo brazo flexionado
CURL_DOWN_ANGLE = 160       # Ángulo brazo extendido
CURL_CONFIDENCE = 0.5       # Confianza mínima para detectar puntos

# Flexión de Cuello - Configuración de ratios
FLEXION_THRESHOLD_UP = 0.85      # Ratio cabeza arriba
FLEXION_THRESHOLD_DOWN = 1.15    # Ratio cabeza abajo
FLEXION_CONFIDENCE = 0.5         # Confianza mínima

# Rotación de Cuello - Configuración de ratios
ROTATION_THRESHOLD_LEFT = 1.3    # Ratio cabeza girada izquierda
ROTATION_THRESHOLD_RIGHT = 0.7   # Ratio cabeza girada derecha
ROTATION_CONFIDENCE = 0.5        # Confianza mínima

# Rutas de Modelos
MODEL_NAME = "yolov8n-pose.pt"
MODEL_RELATIVE_PATH = "../yolov8n-pose.pt"

# Interfaz Gráfica - Colores
GUI_COLORS = {
    "BG_COLOR": "#1a1a1a",
    "ACCENT_COLOR": "#00d4ff",
    "BUTTON_COLOR": "#0099cc",
    "BUTTON_HOVER": "#00ccff",
    "TEXT_COLOR": "#ffffff",
    "LABEL_COLOR": "#cccccc",
    "ERROR_COLOR": "#ff6b6b",
    "SUCCESS_COLOR": "#51cf66",
}

# Interfaz Gráfica - Fuentes
GUI_FONTS = {
    "TITLE_FONT": ("Segoe UI", 24, "bold"),
    "HEADING_FONT": ("Segoe UI", 12, "bold"),
    "LABEL_FONT": ("Segoe UI", 10),
    "BUTTON_FONT": ("Segoe UI", 10, "bold"),
    "SMALL_FONT": ("Segoe UI", 9),
}

# Interfaz Gráfica - Dimensiones
GUI_DIMENSIONS = {
    "WINDOW_WIDTH": 500,
    "WINDOW_HEIGHT": 750,
    "TITLE_HEIGHT": 80,
}

# OpenCV - Colores BGR (Nota: OpenCV usa BGR en lugar de RGB)
OPENCV_COLORS = {
    "GREEN": (0, 255, 0),           # Nariz/Hombro
    "CYAN": (0, 255, 255),          # Codo/Orejas
    "ORANGE": (0, 165, 255),        # Muñeca
    "CYAN_LIGHT": (0, 200, 255),    # Líneas de conexión
    "WHITE": (255, 255, 255),       # Marco de barras
    "BLACK": (0, 0, 0),             # Fondo
    "YELLOW": (0, 255, 255),        # Texto status
}

# Configuración de Descanso
REST_WINDOW_WIDTH = 640
REST_WINDOW_HEIGHT = 480

# Valores por Defecto
DEFAULT_REPETITIONS = 10
DEFAULT_SERIES = 2
DEFAULT_REST_TIME = 10  # segundos
