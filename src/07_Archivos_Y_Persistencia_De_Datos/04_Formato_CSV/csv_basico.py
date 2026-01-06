# csv_basico.py
# ==========================
# Lectura y escritura básica de archivos CSV en Python
# Explicación paso a paso y buenas prácticas profesionales

import csv
from pathlib import Path

# ---------------------------------------------------------
# 1️⃣ Qué es CSV
# ---------------------------------------------------------
# CSV (Comma Separated Values) es un formato simple de texto
# usado para almacenar datos tabulares.
# Cada fila es un registro y cada columna está separada por un delimitador.
# Ejemplo:
# nombre,edad,hobby
# Juan,30,futbol
# Ana,25,pintura

# CSV es ampliamente usado en:
# - Exportación de bases de datos
# - Datasets de ML
# - Intercambio de información entre sistemas

# ---------------------------------------------------------
# 2️⃣ Preparar archivo de ejemplo
# ---------------------------------------------------------
ruta_csv = Path("usuarios.csv")

# Creamos un CSV de ejemplo si no existe
if not ruta_csv.exists():
    with ruta_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)  # Crea un writer
        # Escribir cabecera
        writer.writerow(["nombre", "edad", "hobby"])
        # Escribir datos
        writer.writerow(["Juan", 30, "futbol"])
        writer.writerow(["Ana", 25, "pintura"])
        writer.writerow(["Luis", 28, "lectura"])

print(f"Archivo CSV de ejemplo creado en: {ruta_csv}")

# ---------------------------------------------------------
# 3️⃣ Leer CSV con csv.reader
# ---------------------------------------------------------
with ruta_csv.open("r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    cabecera = next(reader)  # Leer primera fila (cabecera)
    print("Cabecera:", cabecera)
    
    for i, fila in enumerate(reader):
        print(f"Fila {i}:", fila)
        # Convertir edad a entero
        nombre, edad, hobby = fila
        edad = int(edad)
        print(f"Usuario {nombre}, Edad {edad}, Hobby {hobby}")

# ---------------------------------------------------------
# 4️⃣ Escribir CSV con csv.writer
# ---------------------------------------------------------
# Agregar un nuevo usuario
nuevo_usuario = ["Carla", 22, "guitarra"]

with ruta_csv.open("a", newline="", encoding="utf-8") as f:  # 'a' = append
    writer = csv.writer(f)
    writer.writerow(nuevo_usuario)

print("Nuevo usuario agregado correctamente")

# ---------------------------------------------------------
# 5️⃣ Buenas prácticas profesionales
# ---------------------------------------------------------
# ✅ Usar newline="" al abrir archivos CSV para evitar líneas vacías en Windows
# ✅ Especificar encoding="utf-8" para compatibilidad internacional
# ✅ Validar los tipos de datos antes de escribir
# ✅ Manejar errores comunes:
#    - FileNotFoundError
#    - ValueError al convertir tipos
# ✅ Separar lógica de lectura/escritura de procesamiento de datos
# ✅ Usar csv.DictReader / DictWriter para mayor claridad y evitar errores con índices

# ---------------------------------------------------------
# 6️⃣ Ejemplo con DictReader y DictWriter (más robusto)
# ---------------------------------------------------------
with ruta_csv.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)  # Cada fila → diccionario {columna: valor}
    for row in reader:
        print(row)
        # Acceso seguro: row["edad"]
        edad = int(row["edad"])
        print(f"{row['nombre']} tiene {edad} años")

# Escritura con DictWriter
campos = ["nombre", "edad", "hobby"]
ruta_csv2 = Path("usuarios2.csv")
with ruta_csv2.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerow({"nombre": "Marta", "edad": 29, "hobby": "danza"})

print(f"Archivo CSV con DictWriter creado en: {ruta_csv2}")

# ---------------------------------------------------------
# 7️⃣ Resumen profesional
# ---------------------------------------------------------
# - csv.reader → filas como listas
# - csv.DictReader → filas como diccionarios
# - csv.writer → escribir listas
# - csv.DictWriter → escribir diccionarios
# - Siempre newline="" y encoding="utf-8"
# - Validar tipos y datos antes de escribir
# - Usar append 'a' para agregar, write 'w' para sobrescribir
# - Para datasets grandes, considerar streaming (leer línea por línea)
