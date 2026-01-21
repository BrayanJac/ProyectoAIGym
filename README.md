# 🏋️ ProyectoAIGym - Entrenador Inteligente con IA

Un aplicación de entrenamiento inteligente que utiliza visión por computadora basada en IA para detectar y contar ejercicios en tiempo real. Usa el modelo YOLOv8 para detectar puntos de referencia del cuerpo humano (pose estimation).

## 🎯 Características

### Ejercicios de Brazos
- **Curl Derecho**: Detecta flexiones de bicep del brazo derecho
- **Curl Izquierdo**: Detecta flexiones de bicep del brazo izquierdo
- **Curl Ambos Brazos**: Detecta flexiones simultáneas de ambos brazos

### Ejercicios de Cuello
- **Flexión de Cuello**: Detecta movimientos adelante-atrás de la cabeza
- **Rotación de Cuello**: Detecta movimientos de rotación izquierda-derecha de la cabeza

## 🚀 Características Principales

- **Detección en Tiempo Real**: Utiliza visión por computadora para detectar movimientos
- **Conteo Automático**: Cuenta automáticamente las repeticiones completadas
- **Barra de Progreso Visual**: Muestra el porcentaje de progreso para cada repetición
- **Visualización de Puntos**: Muestra los puntos de referencia del cuerpo (esqueleto)
- **Pantallas de Descanso**: Temporizador entre series
- **Interfaz Moderna**: Tema oscuro con colores cian/azul profesionales
- **Configuración Flexible**: Ajusta repeticiones, series y tiempo de descanso

## 📋 Requisitos

- Python 3.9+
- Cámara web
- 2GB de RAM mínimo
- Conexión a internet (para descargar el modelo YOLOv8 la primera vez)

## 📦 Instalación

### 1. Clonar o descargar el repositorio
```bash
git clone <repositorio>
cd ProyectoAIGym
```

### 2. Crear un entorno virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Ejecutar la aplicación
```bash
python main.py
```

### Instrucciones de uso
1. Abre la aplicación ejecutando `main.py`
2. Selecciona el tipo de ejercicio deseado
3. Configura:
   - **Repeticiones**: Cantidad de repeticiones por serie
   - **Series**: Cantidad de series a realizar
   - **Descanso**: Segundos de descanso entre series
4. Pulsa el botón del ejercicio
5. La cámara se abrirá mostrando:
   - Tu esqueleto detectado en tiempo real
   - Barra de progreso para cada repetición
   - Contador de repeticiones completadas
6. Presiona **ESC** para salir de la cámara en cualquier momento

## 🎨 Interfaz

### Colores Utilizados (Tema Profesional)
- **Fondo**: Negro (#1a1a1a)
- **Acentos**: Cian (#00d4ff)
- **Botones**: Azul (#0099cc)
- **Esqueleto**:
  - Verde: Puntos principales (nariz, hombro)
  - Cian: Puntos secundarios (codo, orejas)
  - Naranja: Puntos terciarios (muñeca)
  - Cian claro: Líneas de conexión

## 📊 Cómo Funciona

### Detección de Ejercicios de Brazos
- Detecta el ángulo del codo usando los puntos: hombro → codo → muñeca
- **UP_ANGLE** (50°): Brazo flexionado
- **DOWN_ANGLE** (160°): Brazo extendido
- Una repetición se completa cuando: flexiona (↑) → extiende (↓)

### Detección de Ejercicios de Cuello

**Flexión de Cuello**
- Detecta la posición vertical de la nariz respecto a las orejas
- **THRESHOLD_UP** (0.85): Cabeza arriba
- **THRESHOLD_DOWN** (1.15): Cabeza abajo
- Una repetición: arriba → abajo

**Rotación de Cuello**
- Detecta la rotación horizontal usando distancias de nariz a orejas
- **THRESHOLD_LEFT** (1.3): Rotación a la izquierda
- **THRESHOLD_RIGHT** (0.7): Rotación a la derecha
- Una repetición: izquierda → derecha

## 📁 Estructura del Proyecto

```
ProyectoAIGym/
├── src/
│   ├── __init__.py                  # Inicializador del módulo
│   ├── main.py                      # Interfaz principal (GUI)
│   ├── exercises/
│   │   ├── __init__.py              # Inicializador de ejercicios
│   │   ├── curl_derecho.py          # Curl brazo derecho
│   │   ├── curl_izquierdo.py        # Curl brazo izquierdo
│   │   ├── curl_ambos.py            # Curl ambos brazos
│   │   ├── flexion_cuello.py        # Flexión de cuello
│   │   └── rotacion_cuello.py       # Rotación de cuello
│   └── utils/
│       ├── __init__.py              # Inicializador de utilidades
│       ├── geometry.py              # Funciones de geometría
│       └── visualization.py         # Funciones de visualización
├── yolov8n-pose.pt                  # Modelo de detección YOLO
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias
├── README.md                        # Este archivo
└── .gitignore                       # Archivos ignorados por Git
```

## 🛠️ Tecnologías Utilizadas

- **Python 3**: Lenguaje de programación
- **Tkinter**: Interfaz gráfica de usuario
- **OpenCV**: Procesamiento de video
- **YOLOv8**: Detección de poses (pose estimation)
- **NumPy**: Cálculos numéricos

## ⚙️ Configuración Recomendada

Para obtener los mejores resultados:
- Colócate frente a la cámara a una distancia de 1-2 metros
- Asegúrate de que la iluminación sea adecuada
- Usa ropa que contraste con el fondo
- Realiza los ejercicios con movimientos claros y fluidos
- La cámara debe capturar tu cuerpo de forma completa

## 🐛 Solución de Problemas

### La cámara no se abre
- Verifica que tu cámara web esté conectada y funcionando
- Comprueba los permisos de acceso a la cámara
- Reinicia la aplicación

### No detecta los movimientos
- Acércate más a la cámara
- Mejora la iluminación
- Realiza movimientos más amplios y claros

### Mensajes de error sobre dependencias
- Asegúrate de haber instalado todas las dependencias: `pip install -r requirements.txt`
- Verifica que estés en el entorno virtual correcto

## 📝 Notas

- El primer uso descargará el modelo YOLOv8 (~40MB), esto puede tardar según tu conexión
- El modelo se cachea localmente para usos futuros
- Los cálculos de pose utilizan puntos clave de COCO dataset

## 📄 Licencia

Este proyecto es para fines educativos.

## 👨‍💻 Autor

Proyecto desarrollado para la clase de Aplicaciones Basadas en el Conocimiento - Tercer Parcial

---

**¡Disfruta tu entrenamiento inteligente!** 💪