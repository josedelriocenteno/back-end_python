# csv_grande_memoria.py
# ==========================
# Lectura de CSV grandes en Python
# Evitar cargar todo en memoria → uso de streaming y generadores

import csv
from pathlib import Path
from typing import Dict, Generator, Any

# ---------------------------------------------------------
# 1️⃣ Problema: CSV muy grande
# ---------------------------------------------------------
# Si tenemos un CSV enorme (millones de filas) hacer:
# usuarios = list(csv.DictReader(f))
# puede saturar la memoria RAM
# → Necesitamos procesar fila por fila (streaming)

ruta_csv = Path("usuarios_grande.csv")

# ---------------------------------------------------------
# 2️⃣ Leer CSV en streaming con DictReader
# ---------------------------------------------------------
def leer_csv_streaming(ruta: Path) -> Generator[Dict[str, Any], None, None]:
    """
    Generador que devuelve filas de CSV una a una.
    Ideal para archivos grandes.
    """
    with ruta.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            yield fila  # Se devuelve fila a la vez, sin cargar todo en memoria

# Uso
for i, usuario in enumerate(leer_csv_streaming(ruta_csv)):
    # Validación mínima
    nombre = usuario.get("nombre", "Desconocido")
    edad_str = usuario.get("edad", "0")
    
    try:
        edad = int(edad_str)
    except ValueError:
        edad = 0
        print(f"Fila {i}: edad inválida → 0")
    
    # Procesamiento ejemplo
    print(f"{i}: {nombre} tiene {edad} años")

# ---------------------------------------------------------
# 3️⃣ Procesamiento por chunks (grupos de filas)
# ---------------------------------------------------------
def leer_csv_por_chunks(ruta: Path, chunk_size: int = 1000) -> Generator[list[Dict[str, Any]], None, None]:
    """
    Devuelve listas de filas de tamaño chunk_size.
    Útil para procesamiento en batch o base de datos.
    """
    chunk: list[Dict[str, Any]] = []
    with ruta.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            chunk.append(fila)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

# Ejemplo de uso por chunks
for i, batch in enumerate(leer_csv_por_chunks(ruta_csv, chunk_size=2)):
    print(f"Batch {i}:")
    for usuario in batch:
        print(usuario)

# ---------------------------------------------------------
# 4️⃣ Comparativa: carga completa vs streaming
# ---------------------------------------------------------
# | Estrategia        | Ventaja                    | Desventaja              |
# |------------------|----------------------------|------------------------|
# | Carga completa    | Fácil de usar             | Consume mucha RAM      |
# | Streaming/Generador | Memoria constante       | Más líneas de código   |
# | Chunks           | Equilibrio memoria/rapidez| Necesita lógica batch  |

# ---------------------------------------------------------
# 5️⃣ Buenas prácticas profesionales
# ---------------------------------------------------------
# ✅ Siempre usar streaming o chunks para CSV grandes
# ✅ Validar datos en cada fila antes de agregarlos a memoria
# ✅ Manejar errores de conversión (edad, números)
# ✅ Mantener encoding="utf-8" y newline="" al abrir archivos
# ✅ Separar lectura de procesamiento → modularidad
# ✅ Logging de filas corruptas o inválidas
# ✅ Para pipelines de data, procesar cada fila o batch y enviar a DB/ML

# ---------------------------------------------------------
# 6️⃣ Resumen
# ---------------------------------------------------------
# - Nunca cargar archivos enormes completos en memoria
# - Usar generadores (`yield`) o chunks para procesar datos
# - Validar cada fila en tiempo real
# - Mantener código limpio y modular
# - Esta técnica es aplicable a CSV, JSONL y otros formatos de datos grandes

print("✅ Lectura de CSV grandes lista, memoria protegida")
