# batch_vs_stream.py
"""
BATCH VS STREAM PROCESSING — DATA ENGINEERING PROFESIONAL
=========================================================

Objetivo:
- Entender claramente la diferencia entre procesamiento batch y streaming
- Saber cuándo usar cada enfoque
- Elegir estructuras de datos adecuadas en cada caso
- Evitar errores típicos de juniors en pipelines de datos
"""

# =========================================================
# 1. DEFINICIONES CLARAS (SIN MARKETING)
# =========================================================

"""
BATCH PROCESSING:
- Procesas datos en bloques (lotes)
- Los datos ya existen antes de procesar
- Latencia alta, throughput alto
- Más simple, más barato, más común

STREAM PROCESSING:
- Procesas datos uno a uno o en micro-lotes
- Los datos llegan continuamente
- Latencia baja, complejidad alta
- Requiere control de estado y tiempo
"""

# =========================================================
# 2. PROCESAMIENTO BATCH (EJEMPLO REAL)
# =========================================================

# Caso típico:
# - Logs diarios
# - Ventas del día
# - ETL nocturno
# - Backups
# - Feature engineering offline

def procesar_batch(datos):
    """
    Simula procesamiento batch
    """
    resultado = []
    for d in datos:
        resultado.append(d * 2)  # transformación típica
    return resultado


# Dataset completo disponible
datos_batch = list(range(1, 11))

resultado_batch = procesar_batch(datos_batch)
print("Resultado batch:", resultado_batch)

"""
Características técnicas:
- Usas LISTS
- Memoria suficiente para cargar el dataset
- Operaciones O(n)
- Fácil de testear y depurar
"""

# =========================================================
# 3. PROCESAMIENTO STREAMING (EJEMPLO REAL)
# =========================================================

# Caso típico:
# - Eventos de usuario
# - Clickstream
# - Sensores
# - Logs en tiempo real
# - Sistemas de alertas

def generar_stream():
    """
    Simula llegada continua de datos
    """
    for i in range(1, 11):
        yield i


def procesar_stream(stream):
    """
    Procesa elementos uno a uno
    """
    for evento in stream:
        resultado = evento * 2
        print("Evento procesado:", resultado)


stream_datos = generar_stream()
procesar_stream(stream_datos)

"""
Características técnicas:
- Usas GENERATORS
- No tienes todo el dataset
- Memoria O(1)
- Procesamiento incremental
"""

# =========================================================
# 4. MICRO-BATCHING (HÍBRIDO PROFESIONAL)
# =========================================================

"""
Muy común en sistemas reales:
- Streaming + batches pequeños
- Kafka, Spark Streaming, Flink
"""

def procesar_micro_batch(lote):
    print("Micro-batch procesado:", lote)


buffer = []
BATCH_SIZE = 3

for evento in generar_stream():
    buffer.append(evento)
    if len(buffer) == BATCH_SIZE:
        procesar_micro_batch(buffer)
        buffer.clear()

# Procesar restos
if buffer:
    procesar_micro_batch(buffer)

"""
Ventajas:
- Reduce overhead
- Mantiene baja latencia
- Más fácil que streaming puro
"""

# =========================================================
# 5. ESTRUCTURAS DE DATOS ADECUADAS
# =========================================================

"""
BATCH:
- list
- dict
- pandas.DataFrame
- archivos (CSV, Parquet)

STREAM:
- generators
- deque
- contadores incrementales
- estados mínimos

MICRO-BATCH:
- list + clear()
- deque con maxlen
"""

from collections import deque

buffer_deque = deque(maxlen=5)
for evento in range(10):
    buffer_deque.append(evento)
    print("Buffer deque:", list(buffer_deque))

# =========================================================
# 6. ERRORES COMUNES DE JUNIORS
# =========================================================

"""
❌ Tratar streaming como batch (cargar todo en memoria)
❌ No pensar en latencia
❌ No controlar tamaño de buffers
❌ Usar listas infinitas
❌ No limpiar estado
"""

# Ejemplo de error:
# datos_stream = list(generar_stream())  # ❌ mata el streaming

# =========================================================
# 7. CUÁNDO USAR CADA UNO (DECISIÓN REAL)
# =========================================================

"""
Usa BATCH si:
✔ No necesitas tiempo real
✔ El dataset es finito
✔ Quieres simplicidad
✔ Coste bajo

Usa STREAM si:
✔ Necesitas reaccionar rápido
✔ Datos infinitos
✔ Alertas / tiempo real
✔ Métricas online

Usa MICRO-BATCH si:
✔ Quieres equilibrio
✔ Streaming a escala
✔ Sistemas distribuidos
"""

# =========================================================
# 8. MENTALIDAD PROFESIONAL
# =========================================================

"""
✔ Piensa en flujo de datos, no solo en código
✔ Diseña estructuras antes de programar
✔ Controla memoria y latencia
✔ Documenta si es batch o stream
✔ Testea con datos grandes
"""

print("Batch vs Stream comprendido a nivel profesional")
